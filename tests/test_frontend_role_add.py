from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import expect, sync_playwright

import callumployed.web.server as web_server
from callumployed.data import db
from callumployed.data.models import Company
from callumployed.data.repositories import (
    add_company,
    get_role,
    list_companies,
    list_company_career_pages,
)
from callumployed.web.server import LocalThreadingHTTPServer, create_handler


@pytest.mark.browser
def test_role_form_suggests_saved_companies_but_accepts_and_creates_a_new_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH",
        str(tmp_path / "frontend-role-company.sqlite3"),
    )
    with db.connect() as connection:
        db.run_migrations(connection)
        add_company(connection, Company(name="Existing Company"))
    monkeypatch.setattr(
        web_server,
        "_try_resolve_company_with_central_store",
        lambda *_args, **_kwargs: None,
    )

    async def fake_run_rescan_role(
        role_id: int,
        *,
        browser_profile_manager: object,
        update_status: bool,
    ) -> dict[str, object]:
        assert browser_profile_manager is not None
        assert update_status is False
        with db.connect() as connection:
            role = get_role(connection, role_id)
        return {"role": role.model_copy(update={"title": "Platform Intern"})}

    monkeypatch.setattr(web_server, "run_rescan_role", fake_run_rescan_role)
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{server.server_address[1]}")
            expect(
                page.locator('#role-company-options option[value="Existing Company"]')
            ).to_be_attached()

            page.locator("#role-url-input").fill(
                "https://new-company.example/jobs/platform-intern"
            )
            page.locator("#role-company-input").fill("New Company")
            page.locator('#role-add-form button[type="submit"]').click()

            expect(page.locator("#role-add-status")).to_contain_text(
                "platform intern added to Interested"
            )
            expect(
                page.locator('#role-company-options option[value="Existing Company"]')
            ).to_be_attached()
            expect(
                page.locator('#role-company-options option[value="New Company"]')
            ).to_be_attached()
            browser.close()

        with db.connect() as connection:
            companies = list_companies(connection)
            assert [company.name for company in companies] == [
                "Existing Company",
                "New Company",
            ]
            new_company = companies[1]
            assert new_company.id is not None
            assert list_company_career_pages(connection, new_company.id) == []
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
