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


@pytest.mark.parametrize(
    ("environment_provider", "persisted_provider", "expected"),
    [
        ("unsupported-provider", None, "openai"),
        (" CoDeX ", None, "codex"),
        ("openai", "legacy-provider", "openai"),
        ("openai", " CoDeX ", "codex"),
    ],
)
def test_shared_settings_normalize_provider_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    environment_provider: str,
    persisted_provider: str | None,
    expected: str,
) -> None:
    monkeypatch.setenv("CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "provider-source.sqlite3"))
    monkeypatch.setenv("CALLUMPLOYED_LLM_PROVIDER", environment_provider)

    with db.connect() as connection:
        db.run_migrations(connection)
        if persisted_provider is not None:
            app_settings.set_config_value(connection, "llm_provider", persisted_provider)
        settings = get_settings(connection)
        llm_settings = app_settings.configured_llm_settings(connection)

    assert settings["llm_provider"] == expected
    assert llm_settings.provider == expected


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


def test_shared_settings_preserve_hyphenated_applicant_names(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH",
        str(tmp_path / "hyphenated-applicant-name.sqlite3"),
    )

    with db.connect() as connection:
        db.run_migrations(connection)
        assert set_setting(connection, "applicant_last_name", "Smith-Jones") == "Smith-Jones"
        assert get_settings(connection)["applicant_last_name"] == "Smith-Jones"


def test_shared_settings_reject_retired_application_generation_backend(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH", str(tmp_path / "application-backend-retired.sqlite3")
    )

    with db.connect() as connection:
        db.run_migrations(connection)
        assert "application_generation_backend" not in SETTING_KEYS
        assert "application_generation_backend" not in get_settings(connection)
        with pytest.raises(ValueError, match="Unknown setting"):
            set_setting(connection, "application_generation_backend", "hermes")


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
