from __future__ import annotations

import re
import sqlite3
from datetime import datetime

from callumployed.data.repositories import get_config_value, set_config_value

SCAN_SCHEDULE_ENABLED_CONFIG_KEY = "scan_schedule_enabled"
SCAN_SCHEDULE_TIME_CONFIG_KEY = "scan_schedule_time"
SCAN_SCHEDULE_LAST_RUN_DATE_CONFIG_KEY = "scan_schedule_last_run_date"
DEFAULT_SCAN_SCHEDULE_ENABLED = False
DEFAULT_SCAN_SCHEDULE_TIME = "04:30"
_TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def get_scan_schedule(connection: sqlite3.Connection) -> tuple[bool, str, str | None]:
    configured_enabled = get_config_value(connection, SCAN_SCHEDULE_ENABLED_CONFIG_KEY)
    enabled = (
        DEFAULT_SCAN_SCHEDULE_ENABLED
        if configured_enabled is None
        else configured_enabled.strip().lower() == "true"
    )
    time_value = clean_scan_schedule_time(
        get_config_value(connection, SCAN_SCHEDULE_TIME_CONFIG_KEY)
        or DEFAULT_SCAN_SCHEDULE_TIME
    )
    last_run_date = get_config_value(connection, SCAN_SCHEDULE_LAST_RUN_DATE_CONFIG_KEY)
    return enabled, time_value, last_run_date


def set_scan_schedule_enabled(connection: sqlite3.Connection, enabled: bool) -> None:
    set_config_value(
        connection,
        SCAN_SCHEDULE_ENABLED_CONFIG_KEY,
        "true" if enabled else "false",
    )


def set_scan_schedule_time(connection: sqlite3.Connection, value: str) -> str:
    cleaned = clean_scan_schedule_time(value)
    set_config_value(connection, SCAN_SCHEDULE_TIME_CONFIG_KEY, cleaned)
    return cleaned


def clean_scan_schedule_time(value: str) -> str:
    cleaned = value.strip()
    if not _TIME_PATTERN.fullmatch(cleaned):
        raise ValueError("scan schedule time must use 24-hour HH:MM format")
    return cleaned


def is_daily_scan_due(
    *,
    now: datetime,
    enabled: bool,
    scheduled_time: str,
    last_run_date: str | None,
) -> bool:
    local_now = now.astimezone()
    return (
        enabled
        and last_run_date != local_now.date().isoformat()
        and local_now.strftime("%H:%M") == clean_scan_schedule_time(scheduled_time)
    )
