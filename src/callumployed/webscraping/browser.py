from collections.abc import Sequence
from pathlib import Path

from platformdirs import user_data_path
from playwright.async_api import BrowserContext, Page, Playwright, async_playwright
from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright_stealth import Stealth  # type: ignore[import-untyped]

from callumployed.webscraping.errors import BlockedNavigationError, NavigationError
from callumployed.webscraping.models import RenderedPageState

DEFAULT_TIMEOUT_MS = 30_000
CONTENT_SETTLE_MIN_WAIT_MS = 3_000
CONTENT_SETTLE_TIMEOUT_MS = 8_000
CONTENT_SETTLE_POLL_MS = 1_000
LAZY_SCROLL_STEP_DELAY_MS = 350
ROLE_PAGE_CONTENT_SETTLE_MIN_WAIT_MS = 500
ROLE_PAGE_CONTENT_SETTLE_TIMEOUT_MS = 1_500
ROLE_PAGE_CONTENT_SETTLE_POLL_MS = 250
ROLE_PAGE_LAZY_SCROLL_STEP_DELAY_MS = 75
PROFILE_DIR_NAME = "browser-profile"


async def render_careers_page(
    url: str,
    *,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
    blocked_resource_types: Sequence[str] = (),
    stealth: bool = True,
    external_browser_port: int | None = None,
    fallback_to_managed_browser: bool = True,
    content_settle_min_wait_ms: int = CONTENT_SETTLE_MIN_WAIT_MS,
    content_settle_timeout_ms: int = CONTENT_SETTLE_TIMEOUT_MS,
    content_settle_poll_ms: int = CONTENT_SETTLE_POLL_MS,
    lazy_scroll_step_delay_ms: int = LAZY_SCROLL_STEP_DELAY_MS,
) -> RenderedPageState:
    blocked_types = set(blocked_resource_types)
    playwright_context = Stealth().use_async(async_playwright()) if stealth else async_playwright()

    try:
        async with playwright_context as playwright:
            if external_browser_port is not None:
                try:
                    browser = await playwright.chromium.connect_over_cdp(
                        f"http://127.0.0.1:{external_browser_port}"
                    )
                except PlaywrightError as exc:
                    if not fallback_to_managed_browser:
                        raise NavigationError(
                            "Could not connect to external browser CDP port "
                            f"{external_browser_port}"
                        ) from exc
                    return await _render_with_managed_browser(
                        playwright,
                        url,
                        timeout_ms=timeout_ms,
                        blocked_types=blocked_types,
                        content_settle_min_wait_ms=content_settle_min_wait_ms,
                        content_settle_timeout_ms=content_settle_timeout_ms,
                        content_settle_poll_ms=content_settle_poll_ms,
                        lazy_scroll_step_delay_ms=lazy_scroll_step_delay_ms,
                    )
                context = browser.contexts[0] if browser.contexts else await browser.new_context()
                return await _render_with_context(
                    context,
                    url,
                    timeout_ms=timeout_ms,
                    blocked_types=blocked_types,
                    content_settle_min_wait_ms=content_settle_min_wait_ms,
                    content_settle_timeout_ms=content_settle_timeout_ms,
                    content_settle_poll_ms=content_settle_poll_ms,
                    lazy_scroll_step_delay_ms=lazy_scroll_step_delay_ms,
                )

            return await _render_with_managed_browser(
                playwright,
                url,
                timeout_ms=timeout_ms,
                blocked_types=blocked_types,
                content_settle_min_wait_ms=content_settle_min_wait_ms,
                content_settle_timeout_ms=content_settle_timeout_ms,
                content_settle_poll_ms=content_settle_poll_ms,
                lazy_scroll_step_delay_ms=lazy_scroll_step_delay_ms,
            )
    except NavigationError:
        raise
    except PlaywrightTimeoutError as exc:
        raise NavigationError(f"Timed out while navigating to {url}") from exc
    except PlaywrightError as exc:
        raise NavigationError(f"Failed to render {url}: {exc}") from exc


def managed_browser_profile_path() -> Path:
    return user_data_path("callumployed", appauthor=False) / PROFILE_DIR_NAME


async def _render_with_managed_browser(
    playwright: Playwright,
    url: str,
    *,
    timeout_ms: int,
    blocked_types: set[str],
    content_settle_min_wait_ms: int,
    content_settle_timeout_ms: int,
    content_settle_poll_ms: int,
    lazy_scroll_step_delay_ms: int,
) -> RenderedPageState:
    profile_path = managed_browser_profile_path()
    profile_path.mkdir(parents=True, exist_ok=True)
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(profile_path),
        headless=False,
        ignore_https_errors=True,
    )
    try:
        return await _render_with_context(
            context,
            url,
            timeout_ms=timeout_ms,
            blocked_types=blocked_types,
            content_settle_min_wait_ms=content_settle_min_wait_ms,
            content_settle_timeout_ms=content_settle_timeout_ms,
            content_settle_poll_ms=content_settle_poll_ms,
            lazy_scroll_step_delay_ms=lazy_scroll_step_delay_ms,
        )
    finally:
        await context.close()


async def _render_with_context(
    context: BrowserContext,
    url: str,
    *,
    timeout_ms: int,
    blocked_types: set[str],
    content_settle_min_wait_ms: int = CONTENT_SETTLE_MIN_WAIT_MS,
    content_settle_timeout_ms: int = CONTENT_SETTLE_TIMEOUT_MS,
    content_settle_poll_ms: int = CONTENT_SETTLE_POLL_MS,
    lazy_scroll_step_delay_ms: int = LAZY_SCROLL_STEP_DELAY_MS,
) -> RenderedPageState:
    context.set_default_timeout(timeout_ms)
    context.set_default_navigation_timeout(timeout_ms)

    async def route_handler(route: object) -> None:
        request = route.request  # type: ignore[attr-defined]
        if request.resource_type in blocked_types:
            await route.abort()  # type: ignore[attr-defined]
            return
        await route.continue_()  # type: ignore[attr-defined]

    await context.route("**/*", route_handler)
    page = await context.new_page()
    try:
        response = await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        if response is None:
            raise NavigationError(f"No response while navigating to {url}")
        if is_blocked_status(response.status):
            raise BlockedNavigationError(
                navigation_error_message(url, response.status),
                status_code=response.status,
            )
        if response.status >= 400:
            raise NavigationError(navigation_error_message(url, response.status))

        await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 15_000))
        await _wait_for_dynamic_content(
            page,
            timeout_ms=timeout_ms,
            content_settle_min_wait_ms=content_settle_min_wait_ms,
            content_settle_timeout_ms=content_settle_timeout_ms,
            content_settle_poll_ms=content_settle_poll_ms,
            lazy_scroll_step_delay_ms=lazy_scroll_step_delay_ms,
        )
        title = await page.title()
        html = await page.content()
        visible_text = await page.locator("body").inner_text(timeout=5_000)
        return RenderedPageState(
            url=url,
            final_url=page.url,
            title=title or None,
            html=html,
            visible_text=visible_text or None,
        )
    finally:
        await page.close()


async def _wait_for_dynamic_content(
    page: Page,
    *,
    timeout_ms: int,
    content_settle_min_wait_ms: int = CONTENT_SETTLE_MIN_WAIT_MS,
    content_settle_timeout_ms: int = CONTENT_SETTLE_TIMEOUT_MS,
    content_settle_poll_ms: int = CONTENT_SETTLE_POLL_MS,
    lazy_scroll_step_delay_ms: int = LAZY_SCROLL_STEP_DELAY_MS,
) -> None:
    total_wait_ms = min(timeout_ms, content_settle_timeout_ms)
    initial_wait_ms = min(content_settle_min_wait_ms, total_wait_ms)
    await _trigger_lazy_loading_scroll(page, lazy_scroll_step_delay_ms=lazy_scroll_step_delay_ms)
    await page.wait_for_timeout(initial_wait_ms)

    elapsed_ms = initial_wait_ms
    previous_state: tuple[int, int, int] | None = None
    stable_observations = 0
    while elapsed_ms < total_wait_ms:
        state = await page.evaluate(
            """
            () => [
                document.querySelectorAll('a[href], button').length,
                Array.from(document.querySelectorAll('a[href]'))
                    .map((anchor) => anchor.getAttribute('href') || '')
                    .sort()
                    .join('|')
                    .length,
                document.body ? document.body.innerText.length : 0
            ]
            """
        )
        current_state = (int(state[0]), int(state[1]), int(state[2]))
        if current_state == previous_state:
            stable_observations += 1
            if stable_observations >= 2:
                return
        else:
            stable_observations = 0
            previous_state = current_state

        wait_ms = min(content_settle_poll_ms, total_wait_ms - elapsed_ms)
        await page.wait_for_timeout(wait_ms)
        elapsed_ms += wait_ms


async def _trigger_lazy_loading_scroll(
    page: Page,
    *,
    lazy_scroll_step_delay_ms: int = LAZY_SCROLL_STEP_DELAY_MS,
) -> None:
    await page.evaluate(
        """
        async (stepDelayMs) => {
            const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
            const collected = new Map();
            const collectLinks = () => {
                for (const anchor of document.querySelectorAll('a[href]')) {
                    const href = anchor.getAttribute('href');
                    if (!href || collected.has(href)) {
                        continue;
                    }
                    collected.set(href, {
                        href,
                        text: anchor.innerText || anchor.textContent || '',
                        ariaLabel: anchor.getAttribute('aria-label') || '',
                        title: anchor.getAttribute('title') || '',
                        className: anchor.getAttribute('class') || '',
                        id: anchor.getAttribute('id') || '',
                    });
                }
            };
            const appendCollectedLinks = () => {
                let container = document.querySelector('[data-callumployed-collected-links]');
                if (!container) {
                    container = document.createElement('div');
                    container.setAttribute('data-callumployed-collected-links', 'lazy-scroll');
                    container.setAttribute('hidden', '');
                    document.body.appendChild(container);
                }
                const existingHrefs = new Set(
                    Array.from(document.querySelectorAll('a[href]'))
                        .map((anchor) => anchor.getAttribute('href') || '')
                );
                for (const link of collected.values()) {
                    if (existingHrefs.has(link.href)) {
                        continue;
                    }
                    const anchor = document.createElement('a');
                    anchor.setAttribute('href', link.href);
                    anchor.setAttribute('data-callumployed-collected-link', 'lazy-scroll');
                    if (link.ariaLabel) anchor.setAttribute('aria-label', link.ariaLabel);
                    if (link.title) anchor.setAttribute('title', link.title);
                    if (link.className) anchor.setAttribute('class', link.className);
                    if (link.id) anchor.setAttribute('id', link.id);
                    anchor.textContent = link.text;
                    container.appendChild(anchor);
                }
            };
            const scrollWindow = async () => {
                const viewportHeight = Math.max(window.innerHeight || 0, 600);
                const stepSize = Math.max(Math.floor(viewportHeight * 0.8), 400);
                let previousY = -1;
                for (
                    let position = 0;
                    position <= document.body.scrollHeight;
                    position += stepSize
                ) {
                    window.scrollTo(0, position);
                    await delay(stepDelayMs);
                    collectLinks();
                    if (window.scrollY === previousY && position > 0) {
                        break;
                    }
                    previousY = window.scrollY;
                }
                window.scrollTo(0, Math.max(0, document.body.scrollHeight));
                await delay(stepDelayMs);
                collectLinks();
            };
            const scrollScrollableElements = async () => {
                const elements = Array.from(document.querySelectorAll('body *'))
                    .filter((element) => {
                        const style = window.getComputedStyle(element);
                        return element.scrollHeight > element.clientHeight + 100
                            && /(auto|scroll)/.test(style.overflowY);
                    })
                    .sort((left, right) => right.scrollHeight - left.scrollHeight)
                    .slice(0, 5);
                for (const element of elements) {
                    const stepSize = Math.max(Math.floor(element.clientHeight * 0.8), 300);
                    let previousTop = -1;
                    for (let position = 0; position <= element.scrollHeight; position += stepSize) {
                        element.scrollTop = position;
                        await delay(stepDelayMs);
                        collectLinks();
                        if (element.scrollTop === previousTop && position > 0) {
                            break;
                        }
                        previousTop = element.scrollTop;
                    }
                    element.scrollTop = 0;
                }
            };
            collectLinks();
            await scrollWindow();
            await scrollScrollableElements();
            appendCollectedLinks();
            window.scrollTo(0, 0);
            await delay(stepDelayMs);
            collectLinks();
            appendCollectedLinks();
        }
        """,
        lazy_scroll_step_delay_ms,
    )


def navigation_error_message(url: str, status: int) -> str:
    message = f"Navigation to {url} returned HTTP {status}"
    if is_blocked_status(status):
        message += (
            ". This site may require a fresh browser profile; try scanning with a "
            "browser profile pool."
        )
    return message


def is_blocked_status(status: int) -> bool:
    return status in {401, 403, 407, 429}
