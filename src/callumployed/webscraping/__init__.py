"""Career-page scraping and extraction helpers."""

from callumployed.webscraping.models import (
    CareersPageScanResult,
    DiscoveredJobLink,
    ExtractionConfidence,
    LinkCandidate,
    RolePageAssessment,
)
from callumployed.webscraping.role_page_classifier import assess_role_page
from callumployed.webscraping.scanner import scan_careers_page

__all__ = [
    "CareersPageScanResult",
    "DiscoveredJobLink",
    "ExtractionConfidence",
    "LinkCandidate",
    "RolePageAssessment",
    "assess_role_page",
    "scan_careers_page",
]
