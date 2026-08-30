from pathlib import Path

import pytest

import callumployed.services.app_settings as app_settings
from callumployed.data import db
from callumployed.data.repositories import get_config_value
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
        "application_generation_backend": "hermes",
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


@pytest.mark.parametrize("backend", ["openai", "hermes", "openclaw"])
def test_shared_settings_preserve_every_application_generation_backend(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    backend: str,
) -> None:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH", str(tmp_path / f"application-backend-{backend}.sqlite3")
    )

    with db.connect() as connection:
        db.run_migrations(connection)
        assert set_setting(connection, "application_generation_backend", backend) == backend
        assert get_settings(connection)["application_generation_backend"] == backend


def test_applicant_profile_settings_debounce_durable_cover_letter_refresh(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "profile-debounce.sqlite3"))
    monkeypatch.setattr(app_settings.time, "time", lambda: 100.0)

    with db.connect() as connection:
        db.run_migrations(connection)
        set_setting(connection, "applicant_first_name", "Callum")
        assert get_config_value(
            connection, app_settings.APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY
        ) == "130.0"

        monkeypatch.setattr(app_settings.time, "time", lambda: 200.0)
        set_setting(connection, "applicant_first_name", "Callum")
        assert get_config_value(
            connection, app_settings.APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY
        ) == "130.0"

        set_setting(connection, "applicant_first_name", "Cal")
        assert get_config_value(
            connection, app_settings.APPLICANT_PROFILE_REPREP_DUE_CONFIG_KEY
        ) == "230.0"
