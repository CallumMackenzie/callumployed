import asyncio
import copy
import fcntl
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Any, cast

import httpx
from pydantic import BaseModel

CHATGPT_CODEX_RESPONSES_URL = "https://chatgpt.com/backend-api/codex/responses"
CHATGPT_OAUTH_TOKEN_URL = "https://auth.openai.com/oauth/token"
CHATGPT_OAUTH_CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
DEFAULT_CODEX_MODEL = "gpt-5.6-terra"


class CodexStructuredChatModel:
    """Structured output through ChatGPT subscription OAuth and direct HTTP.

    This adapter never invokes a local Codex or ChatGPT executable and never
    reads ``OPENAI_API_KEY``. It uses the user's ChatGPT OAuth credential store
    to call the subscription-backed Codex Responses endpoint directly.
    """

    def __init__(
        self,
        *,
        output_model: type[BaseModel] | None = None,
        model: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.output_model = output_model
        self.model = model or DEFAULT_CODEX_MODEL
        self.transport = transport

    def with_structured_output(self, output_model: type[BaseModel]) -> "CodexStructuredChatModel":
        return CodexStructuredChatModel(
            output_model=output_model,
            model=self.model,
            transport=self.transport,
        )

    async def ainvoke(self, prompt: Any) -> Any:
        if self.output_model is None:
            raise RuntimeError("ChatGPT subscription calls require a structured output model")

        auth_path, auth = _load_subscription_auth()
        payload = _responses_payload(
            model=self.model,
            prompt=_render_prompt(prompt),
            output_model=self.output_model,
        )
        async with httpx.AsyncClient(transport=self.transport, timeout=180.0) as client:
            status, result = await _request_structured_result(client, auth, payload)
            if status == 401:
                auth = await _refresh_subscription_auth_safely(client, auth_path, auth)
                status, result = await _request_structured_result(client, auth, payload)

        if status == 401:
            raise RuntimeError(
                "ChatGPT subscription authentication expired. Sign in to ChatGPT again."
            )
        if status >= 400:
            raise RuntimeError(f"ChatGPT subscription generation failed with HTTP {status}")
        if not result:
            raise RuntimeError("ChatGPT subscription generation completed without a result")
        return self.output_model.model_validate_json(result)


def _auth_path() -> Path:
    configured = os.environ.get("CALLUMPLOYED_CHATGPT_AUTH_PATH", "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".codex" / "auth.json"


def _load_subscription_auth() -> tuple[Path, dict[str, Any]]:
    path = _auth_path()
    return path, _read_subscription_auth(path)


def _read_subscription_auth(path: Path) -> dict[str, Any]:
    try:
        raw_auth = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(
            "ChatGPT subscription authentication is not available. Sign in to ChatGPT first."
        ) from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("ChatGPT subscription authentication could not be read") from exc

    if not isinstance(raw_auth, dict):
        raise RuntimeError("ChatGPT subscription authentication has an invalid structure")
    auth = cast(dict[str, Any], raw_auth)

    tokens = auth.get("tokens")
    if auth.get("auth_mode") != "chatgpt" or not isinstance(tokens, dict):
        raise RuntimeError("The available authentication is not a ChatGPT subscription session")
    if not _required_string(tokens, "access_token"):
        raise RuntimeError("ChatGPT subscription authentication has no access token")
    if not _account_id(tokens):
        raise RuntimeError("ChatGPT subscription authentication has no account identifier")
    return auth


async def _request_structured_result(
    client: httpx.AsyncClient,
    auth: dict[str, Any],
    payload: dict[str, Any],
) -> tuple[int, str]:
    tokens = auth["tokens"]
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "ChatGPT-Account-Id": _account_id(tokens),
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "User-Agent": "callumployed/0.1",
        "originator": "callumployed",
    }
    chunks: list[str] = []
    completed = False
    async with client.stream(
        "POST",
        CHATGPT_CODEX_RESPONSES_URL,
        headers=headers,
        json=payload,
    ) as response:
        if response.status_code >= 400:
            await response.aread()
            return response.status_code, ""
        async for line in response.aiter_lines():
            if not line.startswith("data:"):
                continue
            raw_event = line.removeprefix("data:").strip()
            if not raw_event or raw_event == "[DONE]":
                continue
            try:
                event = json.loads(raw_event)
            except json.JSONDecodeError:
                continue
            event_type = event.get("type")
            if event_type == "response.output_text.delta":
                chunks.append(str(event.get("delta", "")))
            elif event_type == "response.completed":
                completed = True
            elif event_type in {"error", "response.failed"}:
                raise RuntimeError("ChatGPT subscription generation failed while streaming")
    if not completed:
        raise RuntimeError("ChatGPT subscription generation stream ended before completion")
    return 200, "".join(chunks)


async def _refresh_subscription_auth_safely(
    client: httpx.AsyncClient,
    path: Path,
    failed_auth: dict[str, Any],
) -> dict[str, Any]:
    lock_file = await _acquire_auth_lock(path)
    try:
        current_auth = _read_subscription_auth(path)
        if _token_identity(current_auth) != _token_identity(failed_auth):
            return current_auth
        try:
            return await _refresh_subscription_auth(client, path, current_auth)
        except RuntimeError:
            latest_auth = _read_subscription_auth(path)
            if _token_identity(latest_auth) != _token_identity(current_auth):
                return latest_auth
            raise
    finally:
        _release_auth_lock(lock_file)


async def _refresh_subscription_auth(
    client: httpx.AsyncClient,
    path: Path,
    auth: dict[str, Any],
) -> dict[str, Any]:
    tokens = auth["tokens"]
    refresh_token = _required_string(tokens, "refresh_token")
    if not refresh_token:
        raise RuntimeError(
            "ChatGPT subscription authentication expired and cannot be refreshed. Sign in again."
        )
    response = await client.post(
        CHATGPT_OAUTH_TOKEN_URL,
        headers={"Content-Type": "application/json"},
        json={
            "client_id": CHATGPT_OAUTH_CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    if not response.is_success:
        raise RuntimeError(
            "ChatGPT subscription authentication expired and refresh failed. Sign in again."
        )
    refreshed = response.json()
    access_token = refreshed.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise RuntimeError("ChatGPT subscription token refresh returned no access token")

    latest_auth = _read_subscription_auth(path)
    if _token_identity(latest_auth) != _token_identity(auth):
        return latest_auth

    updated_auth = copy.deepcopy(auth)
    updated_tokens = updated_auth["tokens"]
    updated_tokens["access_token"] = access_token
    new_refresh_token = refreshed.get("refresh_token")
    if isinstance(new_refresh_token, str) and new_refresh_token:
        updated_tokens["refresh_token"] = new_refresh_token
    id_token = refreshed.get("id_token")
    if isinstance(id_token, str) and id_token:
        updated_tokens["id_token"] = id_token
    updated_auth["last_refresh"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    _write_auth_atomically(path, updated_auth)
    return updated_auth


def _token_identity(auth: dict[str, Any]) -> tuple[str, str]:
    tokens = auth.get("tokens")
    if not isinstance(tokens, dict):
        return "", ""
    return (
        _required_string(tokens, "access_token"),
        _required_string(tokens, "refresh_token"),
    )


async def _acquire_auth_lock(path: Path) -> IO[str]:
    lock_path = path.with_name(f".{path.name}.callumployed.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    lock_file = os.fdopen(descriptor, "a+", encoding="utf-8")
    try:
        while True:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                await asyncio.sleep(0.05)
    except BaseException:
        lock_file.close()
        raise
    return lock_file


def _release_auth_lock(lock_file: IO[str]) -> None:
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
    finally:
        lock_file.close()


def _write_auth_atomically(path: Path, auth: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".auth-", suffix=".json", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(auth, file)
            file.write("\n")
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _required_string(values: dict[str, Any], key: str) -> str:
    value = values.get(key)
    return value if isinstance(value, str) and value else ""


def _account_id(tokens: dict[str, Any]) -> str:
    account_id = tokens.get("account_id")
    return account_id if isinstance(account_id, str) else ""


def _responses_payload(
    *,
    model: str,
    prompt: str,
    output_model: type[BaseModel],
) -> dict[str, Any]:
    return {
        "model": model,
        "instructions": (
            "Complete this generation task without using tools, reading files, or modifying the "
            "workspace. Return only JSON that matches the supplied output schema."
        ),
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            }
        ],
        "tools": [],
        "tool_choice": "none",
        "parallel_tool_calls": False,
        "reasoning": {"effort": "low", "summary": "auto"},
        "store": False,
        "stream": True,
        "include": [],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "callumployed_output",
                "strict": True,
                "schema": _codex_output_schema(output_model),
            }
        },
    }


def _codex_output_schema(output_model: type[BaseModel]) -> dict[str, Any]:
    schema = output_model.model_json_schema()

    def normalize(value: Any) -> None:
        if isinstance(value, dict):
            value.pop("default", None)
            properties = value.get("properties")
            if isinstance(properties, dict):
                value["required"] = list(properties)
                value["additionalProperties"] = False
            for nested in value.values():
                normalize(nested)
        elif isinstance(value, list):
            for nested in value:
                normalize(nested)

    normalize(schema)
    return schema


def _render_prompt(prompt: Any) -> str:
    if isinstance(prompt, str):
        return prompt
    if isinstance(prompt, (list, tuple)):
        rendered_messages: list[str] = []
        for message in prompt:
            role = getattr(message, "type", None) or getattr(message, "role", None) or "message"
            content = getattr(message, "content", message)
            rendered_messages.append(f"[{role}]\n{content}")
        return "\n\n".join(rendered_messages)
    return str(prompt)
