from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class HermesGenerationResult:
    session_id: str
    content: str
    metadata: dict[str, Any] | None = None


class HermesGenerationError(RuntimeError):
    pass


class HermesGenerationInterrupted(HermesGenerationError):
    pass


class _ProcessRunner:
    runtime_name = "Application agent"

    def __init__(
        self, *, executable: str, cwd: Path | None = None, timeout_seconds: int = 600
    ) -> None:
        self.executable = executable
        self.cwd = cwd
        self.timeout_seconds = timeout_seconds
        self._lock = threading.Lock()
        self._processes: set[subprocess.Popen[str]] = set()
        self._stopping = False

    def stop(self) -> None:
        with self._lock:
            self._stopping = True
            processes = list(self._processes)
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    def _execute(self, command: list[str]) -> tuple[str, str]:
        with self._lock:
            if self._stopping:
                raise HermesGenerationInterrupted(f"{self.runtime_name} is shutting down.")
        process = subprocess.Popen(
            command, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        with self._lock:
            if self._stopping:
                process.terminate()
            self._processes.add(process)
        try:
            stdout, stderr = process.communicate(timeout=self.timeout_seconds)
        except subprocess.TimeoutExpired as error:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            raise HermesGenerationError(f"{self.runtime_name} generation timed out.") from error
        finally:
            with self._lock:
                self._processes.discard(process)
        with self._lock:
            stopping = self._stopping
        if stopping:
            raise HermesGenerationInterrupted(f"{self.runtime_name} was interrupted by shutdown.")
        if process.returncode != 0:
            raise HermesGenerationError(
                f"{self.runtime_name} generation failed: {_bounded_error(stderr or stdout)}"
            )
        return stdout, stderr


class HermesSessionRunner(_ProcessRunner):
    """Run bounded, traceable Hermes CLI sessions without invoking a shell."""

    runtime_name = "Hermes"

    def __init__(
        self, *, executable: str | None = None, cwd: Path | None = None, timeout_seconds: int = 600
    ) -> None:
        super().__init__(
            executable=executable or resolve_hermes_executable(),
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )

    def start(
        self,
        prompt: str,
        *,
        model: str | None = None,
        source: str = "callumployed",
        allow_web: bool = True,
    ) -> HermesGenerationResult:
        del model  # Runtime owns model routing; retained for compatibility with historical callers.
        command = [
            self.executable,
            "chat",
            "-q",
            prompt,
            "-Q",
            "--pass-session-id",
            "--max-turns",
            "8",
            "--source",
            source,
            "-t",
            "web" if allow_web else "none",
            "--ignore-rules" if allow_web else "--safe-mode",
        ]
        return self._run(command)

    def resume(
        self,
        session_id: str,
        prompt: str,
        *,
        model: str | None = None,
        allow_web: bool = True,
    ) -> HermesGenerationResult:
        del model
        result = self._run(
            [
                self.executable,
                "chat",
                "-q",
                prompt,
                "-Q",
                "--pass-session-id",
                "--max-turns",
                "8",
                "--ignore-rules" if allow_web else "--safe-mode",
                "--source",
                "callumployed",
                "-t",
                "web" if allow_web else "none",
                "--resume",
                session_id,
                "--no-restore-cwd",
            ]
        )
        if result.session_id != session_id:
            raise HermesGenerationError("Hermes resumed into an unexpected session.")
        return result

    def _run(self, command: list[str]) -> HermesGenerationResult:
        stdout, stderr = self._execute(command)
        return parse_hermes_generation_streams(stdout, stderr)


class OpenClawSessionRunner(_ProcessRunner):
    """Run OpenClaw with a stable session key, never through a shell."""

    runtime_name = "OpenClaw"

    def __init__(
        self,
        *,
        executable: str | None = None,
        cwd: Path | None = None,
        timeout_seconds: int = 600,
        agent_id: str | None = None,
    ) -> None:
        super().__init__(
            executable=executable or resolve_openclaw_executable(),
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )
        self.agent_id = agent_id

    def start(self, prompt: str, *, session_key: str) -> HermesGenerationResult:
        safe_key = safe_openclaw_session_key(session_key, agent_id=self.agent_id or "main")
        return self._run(prompt, safe_key)

    def resume(self, session_key: str, prompt: str) -> HermesGenerationResult:
        return self._run(
            prompt,
            safe_openclaw_session_key(session_key, agent_id=self.agent_id or "main"),
        )

    def _run(self, prompt: str, session_key: str) -> HermesGenerationResult:
        # OpenClaw's supported non-interactive contract accepts --message, not a
        # message-file option. Passing an argv list keeps metacharacters inert.
        stdout, stderr = self._execute(
            [
                self.executable,
                "agent",
                *(["--agent", self.agent_id] if self.agent_id else []),
                "--message",
                prompt,
                "--session-key",
                session_key,
                "--json",
                "--timeout",
                str(self.timeout_seconds),
            ]
        )
        payload = _decode_json_object(stdout, runtime="OpenClaw")
        content = _extract_openclaw_content(payload)
        if not content:
            raise HermesGenerationError("OpenClaw returned an empty generation result.")
        return HermesGenerationResult(session_id=session_key, content=content, metadata=payload)


def resolve_hermes_executable() -> str:
    configured = os.environ.get("CALLUMPLOYED_HERMES_EXECUTABLE")
    if configured:
        return str(Path(configured).expanduser())
    discovered = shutil.which("hermes")
    if discovered:
        return discovered
    hermes_home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")).expanduser()
    candidates = (
        hermes_home / "hermes-agent" / "venv" / "bin" / "hermes",
        hermes_home / "venv" / "bin" / "hermes",
    )
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return "hermes"


def resolve_openclaw_executable() -> str:
    configured = os.environ.get("CALLUMPLOYED_OPENCLAW_EXECUTABLE")
    if configured:
        return str(Path(configured).expanduser())
    return shutil.which("openclaw") or "openclaw"


def openclaw_agent_id(mode: str) -> str:
    key = (
        "CALLUMPLOYED_OPENCLAW_RESEARCH_AGENT"
        if mode == "research"
        else "CALLUMPLOYED_OPENCLAW_GENERATION_AGENT"
    )
    default = "callumployed-research" if mode == "research" else "callumployed-generation"
    return os.environ.get(key, default).strip() or default


def require_openclaw_agent_policy(mode: str, *, timeout_seconds: float = 5.0) -> str:
    executable = resolve_openclaw_executable()
    agent_id = openclaw_agent_id(mode)
    try:
        completed = subprocess.run(
            [executable, "config", "get", "agents.list", "--json"],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        agents = json.loads(completed.stdout) if completed.returncode == 0 else []
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        raise HermesGenerationError(
            f"OpenClaw agent policy check failed: {_bounded_error(str(error))}"
        ) from error
    agent = next(
        (item for item in agents if isinstance(item, dict) and item.get("id") == agent_id), None
    )
    tools = agent.get("tools", {}) if isinstance(agent, dict) else {}
    also_allow = set(tools.get("alsoAllow", [])) if isinstance(tools, dict) else set()
    if mode == "generation":
        valid = tools.get("profile") == "minimal" and not also_allow and "allow" not in tools
    else:
        valid = (
            tools.get("profile") == "minimal"
            and also_allow == {"web_search", "web_fetch"}
            and "allow" not in tools
        )
    if not valid:
        raise HermesGenerationError(
            f"OpenClaw agent '{agent_id}' is missing or does not have "
            f"Callumployed's bounded {mode} tool policy."
        )
    return agent_id


def runtime_availability(*, timeout_seconds: float = 3.0) -> dict[str, dict[str, Any]]:
    openclaw = _cli_availability("OpenClaw", resolve_openclaw_executable(), timeout_seconds)
    if openclaw.get("available"):
        try:
            require_openclaw_agent_policy("generation", timeout_seconds=timeout_seconds)
            require_openclaw_agent_policy("research", timeout_seconds=timeout_seconds)
        except HermesGenerationError as error:
            openclaw = {"available": False, "reason": str(error)}
    return {
        "openai": {"available": True, "reason": "Built-in application generation backend."},
        "hermes": _cli_availability("Hermes", resolve_hermes_executable(), timeout_seconds),
        "openclaw": openclaw,
    }


def _cli_availability(name: str, executable: str, timeout_seconds: float) -> dict[str, Any]:
    path = Path(executable).expanduser()
    if not path.is_file() and shutil.which(executable) is None:
        return {"available": False, "reason": f"{name} executable was not found."}
    try:
        completed = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {
            "available": False,
            "reason": f"{name} version check failed: {_bounded_error(str(error))}",
        }
    detail = _bounded_error(completed.stderr or completed.stdout)
    if completed.returncode != 0:
        return {"available": False, "reason": f"{name} is installed but unavailable: {detail}"}
    return {
        "available": True,
        "reason": detail or f"{name} is available.",
        "executable": executable,
    }


def safe_openclaw_session_key(value: str, *, agent_id: str = "main") -> str:
    value = re.sub(r"^agent:[^:]+:", "", value)
    safe = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:80] or "callumployed"
    safe_agent = re.sub(r"[^a-z0-9_-]+", "-", agent_id.lower()).strip("-") or "main"
    return f"agent:{safe_agent}:{safe}"


def parse_hermes_generation_streams(stdout: str, stderr: str) -> HermesGenerationResult:
    match = re.search(r"(?m)^session_id:\s*([A-Za-z0-9_-]+)\s*$", stderr)
    if match is None:
        match = re.search(r"(?m)^session_id:\s*([A-Za-z0-9_-]+)\s*$", stdout)
    if match is None:
        raise HermesGenerationError("Hermes did not return a traceable session ID.")
    content = stdout.strip()
    if not content:
        raise HermesGenerationError("Hermes returned an empty generation result.")
    # -Q may emit either direct content or a JSON response envelope.
    try:
        envelope = json.loads(content)
    except json.JSONDecodeError:
        envelope = None
    if isinstance(envelope, dict) and isinstance(envelope.get("content"), str):
        content = envelope["content"].strip()
    return HermesGenerationResult(session_id=match.group(1), content=content)


def parse_hermes_generation_output(output: str) -> HermesGenerationResult:
    match = re.search(r"(?m)^session_id:\s*([A-Za-z0-9_-]+)\s*$", output)
    if match is None:
        raise HermesGenerationError("Hermes did not return a traceable session ID.")
    return parse_hermes_generation_streams(output[match.end() :], output[: match.end()])


def parse_json_response(content: str) -> dict[str, Any]:
    return _decode_json_object(content, runtime="Application agent")


def _decode_json_object(content: str, *, runtime: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, count=1)
        stripped = re.sub(r"\s*```$", "", stripped, count=1)
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError as error:
        start = stripped.find("{")
        if start < 0:
            raise HermesGenerationError(f"{runtime} did not return valid JSON.") from error
        try:
            payload, _ = json.JSONDecoder().raw_decode(stripped[start:])
        except json.JSONDecodeError as nested_error:
            raise HermesGenerationError(f"{runtime} did not return valid JSON.") from nested_error
    if not isinstance(payload, dict):
        raise HermesGenerationError(f"{runtime} returned JSON that was not an object.")
    return payload


def _extract_openclaw_content(payload: dict[str, Any]) -> str:
    for key in ("content", "message", "response", "result", "text"):
        value = payload.get(key)
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, dict):
            nested = _extract_openclaw_content(value)
            if nested:
                return nested
    for list_key in ("payloads", "messages"):
        messages = payload.get(list_key)
        if not isinstance(messages, list):
            continue
        for item in reversed(messages):
            if isinstance(item, dict):
                nested = _extract_openclaw_content(item)
                if nested:
                    return nested
    return ""


def _bounded_error(value: str) -> str:
    cleaned = " ".join(value.strip().split())
    return cleaned[-500:] if cleaned else "unknown CLI error"
