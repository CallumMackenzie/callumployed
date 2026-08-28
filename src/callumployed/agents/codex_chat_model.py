import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class CodexStructuredChatModel:
    """Minimal structured-output adapter backed by the standalone Codex CLI.

    Codex authenticates through its own OAuth state. OPENAI_API_KEY is removed
    from the child environment so a depleted Platform key cannot shadow that
    OAuth session.
    """

    def __init__(self, *, output_model: type[BaseModel] | None = None, model: str | None = None):
        self.output_model = output_model
        self.model = model

    def with_structured_output(self, output_model: type[BaseModel]) -> "CodexStructuredChatModel":
        return CodexStructuredChatModel(output_model=output_model, model=self.model)

    async def ainvoke(self, prompt: Any) -> Any:
        if self.output_model is None:
            raise RuntimeError("Codex CLI calls require a structured output model")

        rendered_prompt = _render_prompt(prompt)
        instruction = (
            "Complete this generation task without using tools, reading files, or modifying the "
            "workspace. Return only JSON that matches the supplied output schema.\n\n"
            f"{rendered_prompt}"
        )
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)

        with tempfile.TemporaryDirectory(prefix="callumployed-codex-") as temporary_directory:
            temporary_path = Path(temporary_directory)
            schema_path = temporary_path / "schema.json"
            output_path = temporary_path / "result.json"
            schema_path.write_text(
                json.dumps(_codex_output_schema(self.output_model)),
                encoding="utf-8",
            )
            command = [
                "codex",
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--ignore-rules",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(output_path),
            ]
            if self.model:
                command.extend(("--model", self.model))
            command.append("-")

            try:
                process = await asyncio.create_subprocess_exec(
                    *command,
                    cwd=temporary_path,
                    env=env,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            except FileNotFoundError as exc:
                raise RuntimeError(
                    "Codex CLI provider is selected, but the codex executable is not installed"
                ) from exc

            stdout, stderr = await process.communicate(instruction.encode())
            if process.returncode != 0:
                diagnostic = (stderr or stdout).decode(errors="replace").strip()
                if len(diagnostic) > 2_000:
                    diagnostic = diagnostic[-2_000:]
                raise RuntimeError(
                    f"Codex CLI generation failed with exit code {process.returncode}: {diagnostic}"
                )
            if not output_path.exists():
                raise RuntimeError("Codex CLI generation completed without a structured result")
            return self.output_model.model_validate_json(output_path.read_text(encoding="utf-8"))


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
