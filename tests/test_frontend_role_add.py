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


@pytest.mark.browser
def test_company_form_allows_selecting_a_tier_during_creation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH",
        str(tmp_path / "frontend-company-tier.sqlite3"),
    )
    db.ensure_initialized()
    monkeypatch.setattr(
        web_server,
        "_try_resolve_company_with_central_store",
        lambda *_args, **_kwargs: None,
    )
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{server.server_address[1]}")
            page.locator("#manage-companies-button").click()

            style_script = """
                element => {
                    const style = getComputedStyle(element);
                    return {
                        height: element.getBoundingClientRect().height,
                        border: style.border,
                        borderRadius: style.borderRadius,
                        padding: style.padding,
                        backgroundColor: style.backgroundColor,
                        color: style.color,
                    };
                }
            """
            company_input = page.locator("#company-name-input")
            tier_input = page.locator("#company-tier-input")
            assert tier_input.evaluate(style_script) == company_input.evaluate(style_script)
            company_box = company_input.bounding_box()
            tier_box = tier_input.bounding_box()
            button_box = page.locator('#company-create-form button[type="submit"]').bounding_box()
            assert company_box is not None and tier_box is not None and button_box is not None
            assert abs(tier_box["y"] - company_box["y"]) < 1
            assert abs(button_box["y"] - company_box["y"]) < 1

            company_input.fill("Rivian")
            page.locator("#company-url-input").fill("jobs.ashbyhq.com/rivianvw.tech")
            tier_input.select_option("3")
            page.locator('#company-create-form button[type="submit"]').click()

            expect(page.locator("#company-create-status")).to_have_text("company added.")
            browser.close()

        with db.connect() as connection:
            [company] = list_companies(connection)
        assert company.name == "Rivian"
        assert company.prestige_tier == "3"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
