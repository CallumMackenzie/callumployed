from collections.abc import Iterator
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import Page, sync_playwright

import callumployed.web.server as web_server
from callumployed.data import db
from callumployed.web.server import LocalThreadingHTTPServer, create_handler


@pytest.fixture
def settings_page(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[Page]:
    monkeypatch.setenv(
        "CALLUMPLOYED_DATABASE_PATH",
        str(tmp_path / "profile-settings-draft.sqlite3"),
    )
    monkeypatch.setattr(web_server, "get_central_passkey", lambda: None)
    with db.connect() as connection:
        db.run_migrations(connection)
    server = LocalThreadingHTTPServer(("127.0.0.1", 0), create_handler())
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{server.server_address[1]}")
            page.locator("#settings-open").click()
            page.locator('[name="applicant_first_name"]').wait_for()
            yield page
            browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.mark.browser
def test_saving_profile_field_preserves_another_fields_in_progress_draft(
    settings_page: Page,
) -> None:
    page = settings_page

    response_payload = page.evaluate("async () => (await fetch('/api/config')).json()")
    page.evaluate(
        """
        (payload) => {
          const originalFetch = window.fetch.bind(window);
          let releaseSave;
          window.fetch = (url, options = {}) => {
            if (url === "/api/config" && options.method === "POST") {
              return new Promise((resolve) => {
                releaseSave = () => resolve(new Response(JSON.stringify(payload), {
                  status: 200,
                  headers: { "Content-Type": "application/json" },
                }));
              });
            }
            return originalFetch(url, options);
          };
          window.releaseProfileSettingsSave = () => releaseSave();
        }
        """,
        response_payload,
    )

    page.locator('[name="applicant_first_name"]').evaluate(
        "element => { element.value = 'Edited'; }"
    )
    page.locator('[name="applicant_last_name"]').evaluate(
        "element => { element.value = 'Unsaved draft'; }"
    )
    page.locator('[name="applicant_first_name"]').dispatch_event("change")
    assert page.locator("#settings-status").text_content() == "saving settings..."
    assert page.locator('[name="applicant_last_name"]').is_enabled()

    page.evaluate("window.releaseProfileSettingsSave()")
    page.locator("#settings-status").get_by_text("settings saved.").wait_for()

    assert page.locator('[name="applicant_last_name"]').input_value() == "Unsaved draft"


@pytest.mark.browser
def test_failed_profile_save_does_not_revert_a_newer_draft(settings_page: Page) -> None:
    page = settings_page
    page.evaluate(
        """
        () => {
          const originalFetch = window.fetch.bind(window);
          let releaseSave;
          window.fetch = (url, options = {}) => {
            if (url === "/api/config" && options.method === "POST") {
              return new Promise((resolve) => {
                releaseSave = () => resolve(new Response("", { status: 500 }));
              });
            }
            return originalFetch(url, options);
          };
          window.releaseProfileSettingsSave = () => releaseSave();
        }
        """
    )

    first_name = page.locator('[name="applicant_first_name"]')
    first_name.evaluate("element => { element.value = 'Submitted'; }")
    first_name.dispatch_event("change")
    first_name.evaluate("element => { element.value = 'Newer draft'; }")

    page.evaluate("window.releaseProfileSettingsSave()")
    page.locator("#settings-status").get_by_text("could not save settings.").wait_for()

    assert first_name.input_value() == "Newer draft"
