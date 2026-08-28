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


class HermesGenerationError(RuntimeError):
    pass


class HermesGenerationInterrupted(HermesGenerationError):
    pass


class HermesSessionRunner:
    """Run bounded, traceable Hermes CLI sessions for persisted application jobs."""

    def __init__(
        self,
        *,
        executable: str | None = None,
        cwd: Path | None = None,
        timeout_seconds: int = 600,
    ) -> None:
        self.executable = executable or resolve_hermes_executable()
        self.cwd = cwd
        self.timeout_seconds = timeout_seconds
        self._lock = threading.Lock()
        self._processes: set[subprocess.Popen[str]] = set()
        self._stopping = False

    def start(self, prompt: str, *, model: str, source: str) -> HermesGenerationResult:
        return self._run(
            [
                self.executable,
                "chat",
                "-q",
                prompt,
                "-Q",
                "--source",
                source,
                "--pass-session-id",
                "--max-turns",
                "2",
                "--ignore-rules",
                "-m",
                model,
            ]
        )

    def resume(self, session_id: str, prompt: str, *, model: str) -> HermesGenerationResult:
        result = self._run(
            [
                self.executable,
                "chat",
                "-q",
                prompt,
                "-Q",
                "--resume",
                session_id,
                "--no-restore-cwd",
                "--pass-session-id",
                "--max-turns",
                "2",
                "--ignore-rules",
                "-m",
                model,
            ]
        )
        if result.session_id != session_id:
            raise HermesGenerationError("Hermes resumed into an unexpected session.")
        return result

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

    def _run(self, command: list[str]) -> HermesGenerationResult:
        with self._lock:
            if self._stopping:
                raise HermesGenerationInterrupted("Hermes generation is shutting down.")
        process = subprocess.Popen(
            command,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
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
            raise HermesGenerationError("Hermes generation timed out.") from error
        finally:
            with self._lock:
                self._processes.discard(process)
        with self._lock:
            stopping = self._stopping
        if stopping:
            raise HermesGenerationInterrupted("Hermes generation was interrupted by shutdown.")
        if process.returncode != 0:
            detail = _bounded_error(stderr or stdout)
            raise HermesGenerationError(f"Hermes generation failed: {detail}")
        # Hermes CLI writes session metadata to stderr while -Q writes the final
        # response to stdout. Preserve both so every artifact keeps its real session.
        return parse_hermes_generation_output(f"{stderr}\n{stdout}")


def resolve_hermes_executable() -> str:
    """Resolve Hermes even when a GUI launcher supplies a minimal PATH."""
    configured = os.environ.get("CALLUMPLOYED_HERMES_EXECUTABLE")
    if configured:
        return str(Path(configured).expanduser())
    discovered = shutil.which("hermes")
    if discovered:
        return discovered
    hermes_home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")).expanduser()
    candidates = (
        hermes_home / "hermes-agent" / "venv" / "bin" / "hermes",
        Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "hermes",
        Path.home() / ".local" / "bin" / "hermes",
    )
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return "hermes"


def parse_hermes_generation_output(output: str) -> HermesGenerationResult:
    match = re.search(r"(?m)^session_id:\s*([A-Za-z0-9_-]+)\s*$", output)
    if match is None:
        raise HermesGenerationError("Hermes did not return a traceable session ID.")
    content = output[match.end() :].strip()
    if not content:
        raise HermesGenerationError("Hermes returned an empty generation result.")
    return HermesGenerationResult(session_id=match.group(1), content=content)


def parse_json_response(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, count=1)
        stripped = re.sub(r"\s*```$", "", stripped, count=1)
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError as error:
        start = stripped.find("{")
        if start < 0:
            raise HermesGenerationError("Hermes did not return valid JSON.") from error
        try:
            payload, _ = json.JSONDecoder().raw_decode(stripped[start:])
        except json.JSONDecodeError as nested_error:
            raise HermesGenerationError("Hermes did not return valid JSON.") from nested_error
    if not isinstance(payload, dict):
        raise HermesGenerationError("Hermes returned JSON that was not an object.")
    return payload


def _bounded_error(value: str) -> str:
    cleaned = " ".join(value.strip().split())
    if not cleaned:
        return "unknown CLI error"
    return cleaned[-500:]
