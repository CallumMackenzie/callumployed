class ScrapingError(Exception):
    """Base exception for career-page scraping failures."""


class NavigationError(ScrapingError):
    """Raised when a careers page cannot be rendered."""


class BlockedNavigationError(NavigationError):
    """Raised when a site blocks a browser profile or request."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ExtractionError(ScrapingError):
    """Raised when rendered page content cannot be parsed."""


class ClassificationError(ScrapingError):
    """Raised when optional agent classification fails."""
