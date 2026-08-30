from __future__ import annotations

import re

import turso

from callumployed.config import LlmSettings
from callumployed.data.repositories import (
    get_config_value,
    get_location_filter,
    set_config_value,
    set_include_graduate_degree_roles,
    set_include_hardware_roles,
    set_internship_mode,
    set_location_filter,
    set_require_software_keywords,
    should_include_graduate_degree_roles,
    should_include_hardware_roles,
    should_require_software_keywords,
    should_use_internship_mode,
)
from callumployed.services.scan_schedule import (
    SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
    SCAN_SCHEDULE_TIME_CONFIG_KEY,
    get_scan_schedule,
    set_scan_schedule_enabled,
    set_scan_schedule_time,
)
from callumployed.webscraping.profile_manager import BrowserProfileManager

APPLICANT_KEYS = (
    "applicant_first_name",
    "applicant_last_name",
    "applicant_email",
    "applicant_phone",
    "applicant_institution",
    "applicant_degree",
)
BOOL_KEYS = (
    "autoprep_tailor_resume",
    "scan_headless",
    SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
    "include_graduate_degree_roles",
    "include_hardware_roles",
    "require_software_keywords",
    "internship_mode",
)
TEXT_KEYS = (
    *APPLICANT_KEYS,
    "cover_letter_model",
    "autoprep_resume_prompt",
    "autoprep_cover_letter_prompt",
    "llm_provider",
    SCAN_SCHEDULE_TIME_CONFIG_KEY,
    "location_filter",
)
SETTING_KEYS = (*TEXT_KEYS, *BOOL_KEYS)

DEFAULT_COVER_LETTER_MODEL = "gpt-4.1-mini"
DEFAULT_AUTOPREP_RESUME_PROMPT = (
    "Tailor this resume truthfully for the saved role context. Preserve every employer, "
    "project, education entry, date, and link while actively improving the wording. "
    "Do not invent claims or awkwardly combine unrelated experiences."
)
DEFAULT_AUTOPREP_COVER_LETTER_PROMPT = (
    "Review the indexed application materials as well as the resume and job description. "
    "Write a balanced, company-specific cover letter using the strongest 2-3 source-supported "
    "examples. Explain the task or problem, action taken, and result delivered; demonstrate "
    "relevant soft skills through evidence rather than generic claims. For AI-related roles, "
    "use a source-supported, independently directed AI application and its outcome when "
    "available, naming Hermes when the source supports it. Close by thanking the reader and "
    "inviting an interview. Do not invent experience, referrals, company research, outcomes, "
    "or metrics."
)
SUPPORTED_LLM_PROVIDERS = {"openai", "codex"}
SUPPORTED_COVER_LETTER_MODELS = {
    "gpt-5.6-terra",
    "gpt-5.6-luna",
    "gpt-5.6-sol",
    "gpt-4.1-mini",
}


def get_settings(connection: turso.Connection) -> dict[str, str | bool]:
    schedule_enabled, schedule_time, _ = get_scan_schedule(connection)
    environment_provider = LlmSettings().provider
    return {
        **{key: get_config_value(connection, key) or "" for key in APPLICANT_KEYS},
        "cover_letter_model": get_config_value(connection, "cover_letter_model")
        or DEFAULT_COVER_LETTER_MODEL,
        "autoprep_tailor_resume": _config_bool(
            get_config_value(connection, "autoprep_tailor_resume"), default=True
        ),
        "autoprep_resume_prompt": get_config_value(connection, "autoprep_resume_prompt")
        or DEFAULT_AUTOPREP_RESUME_PROMPT,
        "autoprep_cover_letter_prompt": get_config_value(
            connection, "autoprep_cover_letter_prompt"
        )
        or DEFAULT_AUTOPREP_COVER_LETTER_PROMPT,
        "llm_provider": get_config_value(connection, "llm_provider") or environment_provider,
        "scan_headless": _config_bool(
            get_config_value(connection, "scan_headless"), default=False
        ),
        SCAN_SCHEDULE_ENABLED_CONFIG_KEY: schedule_enabled,
        SCAN_SCHEDULE_TIME_CONFIG_KEY: schedule_time,
        "include_graduate_degree_roles": should_include_graduate_degree_roles(connection),
        "include_hardware_roles": should_include_hardware_roles(connection),
        "require_software_keywords": should_require_software_keywords(connection),
        "internship_mode": should_use_internship_mode(connection),
        "location_filter": get_location_filter(connection),
    }


def set_setting(connection: turso.Connection, key: str, value: object) -> str | bool:
    if key not in SETTING_KEYS:
        expected = ", ".join(sorted(SETTING_KEYS))
        raise ValueError(f"Unknown setting: {key}. Expected one of: {expected}")
    if key in BOOL_KEYS:
        cleaned_bool = parse_bool(value)
        if key == "include_graduate_degree_roles":
            set_include_graduate_degree_roles(connection, cleaned_bool)
        elif key == "include_hardware_roles":
            set_include_hardware_roles(connection, cleaned_bool)
        elif key == "require_software_keywords":
            set_require_software_keywords(connection, cleaned_bool)
        elif key == "internship_mode":
            set_internship_mode(connection, cleaned_bool)
        elif key == SCAN_SCHEDULE_ENABLED_CONFIG_KEY:
            set_scan_schedule_enabled(connection, cleaned_bool)
        else:
            set_config_value(connection, key, "true" if cleaned_bool else "false")
        return cleaned_bool

    cleaned = _clean_text_setting(key, value)
    if key == "location_filter":
        set_location_filter(connection, cleaned)
    elif key == SCAN_SCHEDULE_TIME_CONFIG_KEY:
        set_scan_schedule_time(connection, cleaned)
    else:
        set_config_value(connection, key, cleaned)
    return cleaned


def configured_browser_profile_manager(connection: turso.Connection) -> BrowserProfileManager:
    headless = bool(get_settings(connection)["scan_headless"])
    return BrowserProfileManager(headless=headless)


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError("Boolean settings accept: true/false, yes/no, on/off, or 1/0")


def _clean_text_setting(key: str, value: object) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{key} must be text")
    cleaned = " ".join(value.split()) if key in APPLICANT_KEYS else value.strip()
    if key in {"applicant_first_name", "applicant_last_name"}:
        cleaned = re.sub(r"[^A-Za-z]", "", cleaned)
    if key == "applicant_email" and cleaned:
        local, separator, domain = cleaned.partition("@")
        if not separator or not local or "." not in domain:
            raise ValueError("applicant_email must be a valid email address")
    if key == "applicant_phone" and cleaned:
        if re.search(r"[^0-9+().\- ]", cleaned):
            raise ValueError("applicant_phone contains unsupported characters")
        if not 7 <= sum(character.isdigit() for character in cleaned) <= 15:
            raise ValueError("applicant_phone must contain 7 to 15 digits")
    if key in APPLICANT_KEYS and len(cleaned) > 300:
        raise ValueError(f"{key} is too long")
    if key == "cover_letter_model" and cleaned not in SUPPORTED_COVER_LETTER_MODELS:
        raise ValueError("Choose a supported cover letter model")
    if key == "llm_provider" and cleaned not in SUPPORTED_LLM_PROVIDERS:
        raise ValueError("llm_provider must be one of: codex, openai")
    if key in {"autoprep_resume_prompt", "autoprep_cover_letter_prompt"} and len(cleaned) > 8000:
        raise ValueError("Autoprep prompts must be 8,000 characters or fewer")
    return cleaned


def _config_bool(value: str | None, *, default: bool) -> bool:
    return default if value is None else value.lower() in {"1", "true", "yes", "on"}
