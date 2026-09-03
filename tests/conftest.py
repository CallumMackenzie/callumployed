import pytest


@pytest.fixture(autouse=True)
def prevent_live_central_metrics_publish(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "callumployed.services.scan_workflow.publish_scan_metrics",
        lambda _company, _scan_run: None,
    )
    monkeypatch.setattr(
        "callumployed.cli._try_resolve_company_with_central_store",
        lambda *_args, **_kwargs: None,
    )
