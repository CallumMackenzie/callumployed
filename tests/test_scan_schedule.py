from datetime import UTC, datetime, timedelta

import pytest

from callumployed.data import db
from callumployed.services.scan_schedule import (
    DEFAULT_SCAN_SCHEDULE_TIME,
    clean_scan_schedule_time,
    get_scan_schedule,
    is_daily_scan_due,
    set_scan_schedule_enabled,
    set_scan_schedule_time,
)


def test_scan_schedule_defaults_and_persistence() -> None:
    connection = db.connect(":memory:")
    db.run_migrations(connection)

    assert get_scan_schedule(connection) == (False, DEFAULT_SCAN_SCHEDULE_TIME, None)
    set_scan_schedule_enabled(connection, True)
    assert set_scan_schedule_time(connection, "06:15") == "06:15"
    assert get_scan_schedule(connection) == (True, "06:15", None)


@pytest.mark.parametrize("value", ["4:30", "24:00", "04:60", "nope"])
def test_scan_schedule_rejects_invalid_times(value: str) -> None:
    with pytest.raises(ValueError, match="24-hour HH:MM"):
        clean_scan_schedule_time(value)


def test_daily_scan_due_once_after_local_time() -> None:
    now = datetime(2026, 8, 30, 12, 0, tzinfo=UTC).astimezone()
    today = now.date().isoformat()
    scheduled_time = now.strftime("%H:%M")
    missed_time = (now - timedelta(minutes=1)).strftime("%H:%M")

    assert is_daily_scan_due(
        now=now,
        enabled=True,
        scheduled_time=scheduled_time,
        last_run_date=None,
    )
    assert not is_daily_scan_due(
        now=now,
        enabled=True,
        scheduled_time=scheduled_time,
        last_run_date=today,
    )
    assert not is_daily_scan_due(
        now=now,
        enabled=False,
        scheduled_time=scheduled_time,
        last_run_date=None,
    )
    assert not is_daily_scan_due(
        now=now,
        enabled=True,
        scheduled_time=missed_time,
        last_run_date=None,
    )
