import pytest
from pydantic import ValidationError

from callumployed.models import Event, EventSource, Role, RoleStatus, ScanRun, ScanStatus


def test_role_status_values_match_planned_lifecycle() -> None:
    assert [status.value for status in RoleStatus] == [
        "discovered",
        "interested",
        "disinterested",
        "prepared",
        "applied",
        "OA",
        "interview",
        "rejected",
        "offer",
        "closed",
        "archived",
    ]


def test_role_defaults_to_discovered() -> None:
    role = Role(company_id=1, title="Software Engineer", role_url="https://example.com/jobs/1")

    assert role.role_status is RoleStatus.DISCOVERED


def test_scan_run_defaults_to_running() -> None:
    scan_run = ScanRun(company_id=1)

    assert scan_run.scan_status is ScanStatus.RUNNING


def test_event_source_rejects_future_sources_for_now() -> None:
    with pytest.raises(ValidationError):
        Event(
            company_id=1,
            role_id=1,
            event_type="status_changed",
            source="mailbox",
            summary="Mailbox integration comes later.",
        )


def test_event_source_values_are_minimal() -> None:
    assert [source.value for source in EventSource] == ["manual", "scan"]
