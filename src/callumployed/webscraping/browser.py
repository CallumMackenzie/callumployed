from collections.abc import Sequence

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from callumployed.webscraping.errors import NavigationError
from callumployed.webscraping.models import RenderedPageState

BLOCKED_RESOURCE_TYPES = {"font", "image", "media", "stylesheet"}
DEFAULT_TIMEOUT_MS = 15_000


async def render_careers_page(
    url: str,
    *,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
    blocked_resource_types: Sequence[str] = tuple(BLOCKED_RESOURCE_TYPES),
) -> RenderedPageState:
    blocked_types = set(blocked_resource_types)

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            try:
                context = await browser.new_context(ignore_https_errors=True)
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
                response = await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                if response is None:
                    raise NavigationError(f"No response while navigating to {url}")
                if response.status >= 400:
                    raise NavigationError(f"Navigation to {url} returned HTTP {response.status}")

                await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 5_000))
                title = await page.title()
                html = await page.content()
                visible_text = await page.locator("body").inner_text(timeout=2_000)
                return RenderedPageState(
                    url=url,
                    final_url=page.url,
                    title=title or None,
                    html=html,
                    visible_text=visible_text or None,
                )
            finally:
                await browser.close()
    except NavigationError:
        raise
    except PlaywrightTimeoutError as exc:
        raise NavigationError(f"Timed out while navigating to {url}") from exc
    except PlaywrightError as exc:
        raise NavigationError(f"Failed to render {url}: {exc}") from exc
