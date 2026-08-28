import asyncio
import subprocess
from pathlib import Path
from typing import cast

import pytest

from callumployed.webscraping.errors import BlockedNavigationError, NavigationError
from callumployed.webscraping.models import RenderedPageState
from callumployed.webscraping.profile_manager import (
    BrowserProfileManager,
    find_default_brave_browser_executable,
    find_default_brave_user_data_dir,
)


class FakeProcess:
    def __init__(self) -> None:
        self.closed = False
        self.killed = False

    def poll(self) -> int | None:
        return 0 if self.closed else None

    def terminate(self) -> None:
        self.closed = True

    def wait(self, timeout: float | None = None) -> int:
        return 0

    def kill(self) -> None:
        self.killed = True
        self.closed = True


def _fake_process() -> subprocess.Popen[bytes]:
    return cast(subprocess.Popen[bytes], FakeProcess())


def _template(tmp_path: Path) -> Path:
    template = tmp_path / "template"
    template.mkdir()
    (template / "Cookies").write_text("warm-session", encoding="utf-8")
    (template / "RunningChromeVersion").write_text("ignore me", encoding="utf-8")
    (template / "SingletonLock").write_text("ignore me", encoding="utf-8")
    return template


def test_find_default_brave_user_data_dir_uses_current_user_home(tmp_path: Path) -> None:
    brave_dir = tmp_path / "Library/Application Support/BraveSoftware/Brave-Browser"
    brave_dir.mkdir(parents=True)

    assert find_default_brave_user_data_dir(home=tmp_path) == brave_dir


def test_find_default_brave_user_data_dir_reports_checked_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="could not find Brave user data directory") as error:
        find_default_brave_user_data_dir(home=tmp_path)

    assert str(tmp_path / ".config/BraveSoftware/Brave-Browser") in str(error.value)


def test_find_default_brave_browser_executable_prefers_current_user_home(
    tmp_path: Path,
) -> None:
    executable = tmp_path / "Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    executable.parent.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n", encoding="utf-8")

    assert find_default_brave_browser_executable(home=tmp_path) == str(executable)


def test_profile_manager_clones_template_and_builds_brave_command(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []

    def launcher(command: list[str]) -> subprocess.Popen[bytes]:
        commands.append(command)
        return _fake_process()

    manager = BrowserProfileManager(
        root=tmp_path / "manager",
        launcher=launcher,
    )
    manager._wait_for_cdp = lambda *_args, **_kwargs: None  # type: ignore[method-assign]
    monkeypatch.setattr("callumployed.webscraping.profile_manager._find_free_port", lambda: 9330)
    template_path = _template(tmp_path)
    manager.create_pool(
        "tesla",
        template_path=template_path,
        size=2,
        browser_executable="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    )

    lease = manager.acquire("tesla")
    lease.close()
    assert (lease.record.path / "Cookies").read_text(encoding="utf-8") == "warm-session"
    assert not (lease.record.path / "RunningChromeVersion").exists()
    assert not (lease.record.path / "SingletonLock").exists()
    (template_path / "Cookies").write_text("refreshed-session", encoding="utf-8")
    refreshed_lease = manager.acquire("tesla")
    refreshed_lease.close()

    assert lease.port == 9330
    assert lease.record.path.name == "tesla-001"
    assert refreshed_lease.record.path == lease.record.path
    assert (refreshed_lease.record.path / "Cookies").read_text(
        encoding="utf-8"
    ) == "refreshed-session"
    assert commands == [
        [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "--remote-debugging-port=9330",
            f"--user-data-dir={lease.record.path}",
            "--headless=new",
        ],
        [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "--remote-debugging-port=9330",
            f"--user-data-dir={lease.record.path}",
            "--headless=new",
        ],
    ]


def test_profile_manager_omits_headless_flag_when_disabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []

    def launcher(command: list[str]) -> subprocess.Popen[bytes]:
        commands.append(command)
        return _fake_process()

    manager = BrowserProfileManager(
        root=tmp_path / "manager",
        launcher=launcher,
        headless=False,
    )
    manager._wait_for_cdp = lambda *_args, **_kwargs: None  # type: ignore[method-assign]
    monkeypatch.setattr("callumployed.webscraping.profile_manager._find_free_port", lambda: 9331)
    manager.create_pool(
        "tesla",
        template_path=_template(tmp_path),
        size=1,
        browser_executable="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    )

    lease = manager.acquire("tesla")
    lease.close()

    assert commands == [
        [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "--remote-debugging-port=9331",
            f"--user-data-dir={lease.record.path}",
        ]
    ]


def test_render_with_pool_discards_only_blocked_profiles(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manager = BrowserProfileManager(
        root=tmp_path / "manager",
        launcher=lambda _command: _fake_process(),
    )
    manager._wait_for_cdp = lambda *_args, **_kwargs: None  # type: ignore[method-assign]
    ports = iter([9440, 9441])
    monkeypatch.setattr(
        "callumployed.webscraping.profile_manager._find_free_port",
        lambda: next(ports),
    )
    manager.create_pool("tesla", template_path=_template(tmp_path), size=2)
    rendered_ports: list[int] = []

    async def fake_render(
        url: str,
        *,
        external_browser_port: int,
        fallback_to_managed_browser: bool,
    ) -> RenderedPageState:
        rendered_ports.append(external_browser_port)
        assert fallback_to_managed_browser is False
        if external_browser_port == 9440:
            raise BlockedNavigationError("blocked", status_code=403)
        return RenderedPageState(url=url, final_url=url, html="<a href='/jobs/1'>Software</a>")

    page = asyncio.run(
        manager.render_with_pool("tesla", fake_render, "https://www.tesla.com/careers")
    )
    profiles = {profile.name: profile for profile in manager.list_profiles("tesla")}

    assert page.final_url == "https://www.tesla.com/careers"
    assert rendered_ports == [9440, 9441]
    assert profiles["tesla-001"].status == "blocked"
    assert profiles["tesla-001"].blocked_reason == "blocked"
    assert not profiles["tesla-001"].path.exists()
    assert (tmp_path / "manager" / "discarded" / "tesla" / "tesla-001").exists()
    assert profiles["tesla-002"].status == "available"
    assert profiles["tesla-002"].path.exists()


def test_render_with_pool_does_not_discard_on_non_blocked_errors(tmp_path: Path) -> None:
    manager = BrowserProfileManager(
        root=tmp_path / "manager",
        launcher=lambda _command: _fake_process(),
    )
    manager._wait_for_cdp = lambda *_args, **_kwargs: None  # type: ignore[method-assign]
    manager.create_pool("tesla", template_path=_template(tmp_path), size=1)

    async def fake_render(
        url: str,
        *,
        external_browser_port: int,
        fallback_to_managed_browser: bool,
    ) -> RenderedPageState:
        raise NavigationError("temporary browser failure")

    with pytest.raises(NavigationError):
        asyncio.run(manager.render_with_pool("tesla", fake_render, "https://example.com"))

    profile = manager.list_profiles("tesla")[0]
    assert profile.status == "available"
    assert profile.path.exists()
