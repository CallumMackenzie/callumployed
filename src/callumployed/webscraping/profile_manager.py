import json
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from platformdirs import user_data_path

from callumployed.webscraping.errors import BlockedNavigationError
from callumployed.webscraping.models import RenderedPageState

DEFAULT_BROWSER_EXECUTABLE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
DEFAULT_POOL_SIZE = 3
PROFILE_MANAGER_DIR_NAME = "browser-profile-manager"
REGISTRY_FILENAME = "registry.json"
ACTIVE_PROFILE_DIR_NAME = "profiles"
DISCARDED_PROFILE_DIR_NAME = "discarded"

RenderFunction = Callable[..., Awaitable[RenderedPageState]]


@dataclass(frozen=True)
class BrowserProfileRecord:
    pool: str
    name: str
    path: Path
    status: str
    blocked_reason: str | None = None
    blocked_at: float | None = None


@dataclass(frozen=True)
class BrowserProfileLease:
    record: BrowserProfileRecord
    process: subprocess.Popen[bytes]
    port: int

    def close(self) -> None:
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)


class BrowserProfileManager:
    """Template-backed browser profile pool for external CDP browser scans."""

    def __init__(
        self,
        *,
        root: Path | None = None,
        launcher: Callable[[list[str]], subprocess.Popen[bytes]] | None = None,
    ) -> None:
        self.root = (
            root or user_data_path("callumployed", appauthor=False) / PROFILE_MANAGER_DIR_NAME
        )
        self.launcher = launcher or self._default_launcher

    @property
    def registry_path(self) -> Path:
        return self.root / REGISTRY_FILENAME

    def create_pool(
        self,
        name: str,
        *,
        template_path: Path,
        size: int = DEFAULT_POOL_SIZE,
        browser_executable: str = DEFAULT_BROWSER_EXECUTABLE,
    ) -> None:
        if size < 1:
            raise ValueError("browser profile pool size must be at least 1")
        if not template_path.exists() or not template_path.is_dir():
            raise ValueError(f"template profile directory does not exist: {template_path}")

        registry = self._load_registry()
        pool = registry["pools"].get(name)
        profiles = (
            pool.get("profiles", {}) if isinstance(pool, dict) else {}
        )
        registry["pools"][name] = {
            "template_path": str(template_path),
            "browser_executable": browser_executable,
            "size": size,
            "profiles": self._ensure_profile_records(
                name,
                size=size,
                profiles=profiles,
            ),
        }
        self._save_registry(registry)

    def list_profiles(self, pool_name: str | None = None) -> list[BrowserProfileRecord]:
        registry = self._load_registry()
        records: list[BrowserProfileRecord] = []
        for name, pool in registry["pools"].items():
            if pool_name is not None and name != pool_name:
                continue
            records.extend(
                self._record_from_registry(name, profile_name, profile)
                for profile_name, profile in pool.get("profiles", {}).items()
            )
        return sorted(records, key=lambda record: (record.pool, record.name))

    def acquire(self, pool_name: str) -> BrowserProfileLease:
        registry = self._load_registry()
        pool = self._pool(registry, pool_name)
        for profile_name, profile in pool["profiles"].items():
            if profile.get("status") == "blocked":
                continue
            record = self._record_from_registry(pool_name, profile_name, profile)
            self._ensure_profile_copy(pool_name, profile_name, Path(pool["template_path"]))
            port = _find_free_port()
            process = self.launcher(
                [
                    str(pool["browser_executable"]),
                    f"--remote-debugging-port={port}",
                    f"--user-data-dir={record.path}",
                ]
            )
            self._wait_for_cdp(port, process)
            return BrowserProfileLease(record=record, process=process, port=port)
        raise RuntimeError(f"no available browser profiles in pool: {pool_name}")

    async def render_with_pool(
        self,
        pool_name: str,
        render: RenderFunction,
        url: str,
        *,
        render_options: Mapping[str, Any] | None = None,
    ) -> RenderedPageState:
        last_blocked_error: BlockedNavigationError | None = None
        max_attempts = len(self.list_profiles(pool_name))
        for _attempt in range(max_attempts):
            lease = self.acquire(pool_name)
            try:
                return await render(
                    url,
                    **(render_options or {}),
                    external_browser_port=lease.port,
                    fallback_to_managed_browser=False,
                )
            except BlockedNavigationError as error:
                last_blocked_error = error
                self.mark_blocked(
                    pool_name,
                    lease.record.name,
                    reason=str(error),
                )
            finally:
                lease.close()
        if last_blocked_error is not None:
            raise last_blocked_error
        raise RuntimeError(f"no available browser profiles in pool: {pool_name}")

    def mark_blocked(
        self,
        pool_name: str,
        profile_name: str,
        *,
        reason: str,
    ) -> BrowserProfileRecord:
        registry = self._load_registry()
        pool = self._pool(registry, pool_name)
        profile = pool["profiles"].get(profile_name)
        if not isinstance(profile, dict):
            raise LookupError(f"browser profile not found: {pool_name}/{profile_name}")

        profile["status"] = "blocked"
        profile["blocked_reason"] = reason
        profile["blocked_at"] = time.time()
        active_path = self._profile_path(pool_name, profile_name)
        discarded_path = self._discarded_profile_path(pool_name, profile_name)
        if active_path.exists():
            discarded_path.parent.mkdir(parents=True, exist_ok=True)
            if discarded_path.exists():
                shutil.rmtree(discarded_path)
            shutil.move(str(active_path), str(discarded_path))
        self._save_registry(registry)
        return self._record_from_registry(pool_name, profile_name, profile)

    def _ensure_profile_records(
        self,
        pool_name: str,
        *,
        size: int,
        profiles: object,
    ) -> dict[str, dict[str, object]]:
        existing = profiles if isinstance(profiles, dict) else {}
        records: dict[str, dict[str, object]] = {}
        for index in range(size):
            profile_name = f"{pool_name}-{index + 1:03d}"
            existing_record = existing.get(profile_name)
            if isinstance(existing_record, dict):
                records[profile_name] = {
                    **existing_record,
                    "path": str(self._profile_path(pool_name, profile_name)),
                }
                continue
            records[profile_name] = {
                "path": str(self._profile_path(pool_name, profile_name)),
                "status": "available",
            }
        return records

    def _ensure_profile_copy(self, pool_name: str, profile_name: str, template_path: Path) -> None:
        profile_path = self._profile_path(pool_name, profile_name)
        if profile_path.exists():
            return
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(template_path, profile_path, ignore=_browser_profile_copy_ignore)

    def _profile_path(self, pool_name: str, profile_name: str) -> Path:
        return self.root / ACTIVE_PROFILE_DIR_NAME / pool_name / profile_name

    def _discarded_profile_path(self, pool_name: str, profile_name: str) -> Path:
        return self.root / DISCARDED_PROFILE_DIR_NAME / pool_name / profile_name

    def _record_from_registry(
        self,
        pool_name: str,
        profile_name: str,
        profile: Mapping[str, object],
    ) -> BrowserProfileRecord:
        blocked_at = profile.get("blocked_at")
        if blocked_at is not None and not isinstance(blocked_at, int | float):
            raise ValueError(
                f"invalid browser profile blocked timestamp: {pool_name}/{profile_name}"
            )
        return BrowserProfileRecord(
            pool=pool_name,
            name=profile_name,
            path=Path(str(profile["path"])),
            status=str(profile.get("status", "available")),
            blocked_reason=(
                str(profile["blocked_reason"]) if profile.get("blocked_reason") else None
            ),
            blocked_at=float(blocked_at) if blocked_at is not None else None,
        )

    def _pool(self, registry: dict[str, Any], pool_name: str) -> dict[str, Any]:
        pool = registry["pools"].get(pool_name)
        if not isinstance(pool, dict):
            raise LookupError(f"browser profile pool not found: {pool_name}")
        return pool

    def _load_registry(self) -> dict[str, Any]:
        if not self.registry_path.exists():
            return {"pools": {}}
        with self.registry_path.open("r", encoding="utf-8") as file:
            registry = json.load(file)
        if not isinstance(registry, dict) or not isinstance(registry.get("pools"), dict):
            raise ValueError(f"invalid browser profile registry: {self.registry_path}")
        return registry

    def _save_registry(self, registry: Mapping[str, object]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.registry_path.open("w", encoding="utf-8") as file:
            json.dump(registry, file, indent=2, sort_keys=True)
            file.write("\n")

    def _wait_for_cdp(
        self,
        port: int,
        process: subprocess.Popen[bytes],
        *,
        timeout_seconds: float = 10.0,
    ) -> None:
        deadline = time.monotonic() + timeout_seconds
        url = f"http://127.0.0.1:{port}/json/version"
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"browser process exited before CDP was ready on port {port}")
            try:
                with urllib.request.urlopen(url, timeout=0.5) as response:
                    if response.status == 200:
                        return
            except (OSError, urllib.error.URLError):
                pass
            time.sleep(0.2)
        raise RuntimeError(f"timed out waiting for browser CDP on port {port}")

    @staticmethod
    def _default_launcher(command: list[str]) -> subprocess.Popen[bytes]:
        return subprocess.Popen(command)


def _browser_profile_copy_ignore(_directory: str, names: list[str]) -> set[str]:
    volatile_names = {
        "SingletonCookie",
        "SingletonLock",
        "SingletonSocket",
    }
    return {
        name
        for name in names
        if name in volatile_names or name.endswith(".lock") or name.startswith("Crashpad")
    }


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])
