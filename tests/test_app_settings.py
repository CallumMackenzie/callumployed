from pathlib import Path

import pytest

from callumployed.data import db
from callumployed.services.app_settings import SETTING_KEYS, get_settings, set_setting
from callumployed.web.server import build_config_payload


def test_shared_settings_cover_every_web_setting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "settings.sqlite3"))

    web_settings = {
        setting["key"]: setting["value"] for setting in build_config_payload()["settings"]
    }
    with db.connect() as connection:
        shared_settings = get_settings(connection)

    assert set(SETTING_KEYS) == set(web_settings)
    assert shared_settings == web_settings


def test_shared_settings_can_modify_every_current_setting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "settings-write.sqlite3"))
    requested: dict[str, str | bool] = {
        "applicant_first_name": "Callum",
        "applicant_last_name": "Mackenzie",
        "applicant_email": "callum@example.com",
        "applicant_phone": "+1 250 555 0123",
        "applicant_institution": "University of Victoria",
        "applicant_degree": "BEng Software Engineering",
        "cover_letter_model": "gpt-5.6-terra",
        "autoprep_tailor_resume": False,
        "autoprep_resume_prompt": "Tailor truthfully.",
        "autoprep_cover_letter_prompt": "Use current evidence.",
        "llm_provider": "codex",
        "scan_headless": False,
        "scan_schedule_enabled": False,
        "scan_schedule_time": "06:15",
        "include_graduate_degree_roles": True,
        "include_hardware_roles": True,
        "require_software_keywords": False,
        "internship_mode": False,
        "location_filter": "canada",
    }

    with db.connect() as connection:
        db.run_migrations(connection)
        for key, value in requested.items():
            set_setting(connection, key, value)
        saved = get_settings(connection)

    assert saved == requested
