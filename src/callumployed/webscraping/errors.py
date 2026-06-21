class ScrapingError(Exception):
    """Base exception for career-page scraping failures."""


class NavigationError(ScrapingError):
    """Raised when a careers page cannot be rendered."""


class ExtractionError(ScrapingError):
    """Raised when rendered page content cannot be parsed."""


class ClassificationError(ScrapingError):
    """Raised when optional agent classification fails."""
