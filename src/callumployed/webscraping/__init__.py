"""Career-page scraping and extraction helpers."""

from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    LinkCandidate,
)
from callumployed.webscraping.scanner import scan_careers_page

__all__ = [
    "CareersPageScanResult",
    "DiscoveredJobLink",
    "ExtractionConfidence",
    "LinkCandidate",
    "scan_careers_page",
]
