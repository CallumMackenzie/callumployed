import re

GRADUATE_DEGREE_ROLE_PATTERN = re.compile(
    r"\b(?:ph\.?\s*d\.?|phd|doctorate|doctoral|mba|m\.?\s*sc\.?)\b",
    re.I,
)
MASTER_DEGREE_PATTERN = re.compile(r"\b(?:master'?s|masters)\b", re.I)
BACHELOR_OR_MASTER_PATTERN = re.compile(
    r"\b(?:bachelor'?s|bachelors|bs|b\.?\s*s\.?|ba|b\.?\s*a\.?)"
    r"(?:\s*/\s*|\s+or\s+|\s+and\s+)"
    r"(?:master'?s|masters|ms|m\.?\s*s\.?|m\.?\s*sc\.?)\b|"
    r"\b(?:master'?s|masters|ms|m\.?\s*s\.?|m\.?\s*sc\.?)"
    r"(?:\s*/\s*|\s+or\s+|\s+and\s+)"
    r"(?:bachelor'?s|bachelors|bs|b\.?\s*s\.?|ba|b\.?\s*a\.?)\b",
    re.I,
)
HARDWARE_ROLE_PATTERN = re.compile(r"\bhardware\b", re.I)
HARDWARE_SOFTWARE_ESCAPE_PATTERN = re.compile(
    r"\b(?:software|firmware|sde|swe|developer)\b",
    re.I,
)
SOFTWARE_KEYWORD_PATTERN = re.compile(
    r"\b(?:"
    r"software|ai|artificial intelligence|ml|machine learning|developer|swe|sde|"
    r"development|firmware|backend|back-end|frontend|front-end|full[ -]?stack|"
    r"mobile|ios|android|web|platform|infrastructure|infra|data|cloud|systems|"
    r"llm|foundation model|multimodal|speech model|vision model|"
    r"security|devops|site reliability|sre|distributed systems|compiler|"
    r"programming|coding|automation|qa|quality assurance|test engineering"
    r")\b",
    re.I,
)
INTERN_INTENT_PATTERN = re.compile(
    r"\b(?:interns?|internships?|co[- ]?ops?|student|students|university|campus|"
    r"new grad|new graduate|early(?:[+\s_-]|%20)+talent)\b",
    re.I,
)
CANADA_LOCATION_PATTERN = re.compile(
    r"\b(?:canada|vancouver|calgary|toronto|waterloo|ottawa|montreal|montr[eé]al|"
    r"british columbia|ontario|quebec|bc|on|qc)\b",
    re.I,
)
USA_LOCATION_PATTERN = re.compile(
    r"\b(?:united states|usa|u\.s\.a\.|u\.s\.|us|new york|nyc|chicago|"
    r"palo alto|san francisco|san mateo|santa clara|santa clarita|"
    r"mountain view|menlo park|los gatos|san jose|seattle|los angeles|"
    r"austin|bellevue|carrollton|fremont|miami|california|texas|"
    r"washington|ca|ny|il|tx|wa|fl)\b",
    re.I,
)
INTERNATIONAL_LOCATION_PATTERN = re.compile(
    r"\b(?:brazil|london|amsterdam|netherlands|the netherlands|singapore|"
    r"hong kong|shanghai|sydney|mumbai|india|china|australia|uk|"
    r"united kingdom)\b",
    re.I,
)


def location_matches_filter(location: str | None, location_filter: str) -> bool:
    normalized_filter = location_filter.strip().lower().replace("-", "_")
    if normalized_filter == "all":
        return True

    categories = location_categories(location)
    if not categories:
        return False
    if normalized_filter == "canada":
        return "canada" in categories
    if normalized_filter == "usa":
        return "usa" in categories
    if normalized_filter == "north_america":
        return bool(categories & {"canada", "usa"})
    if normalized_filter == "international":
        return "international" in categories
    return True


def location_categories(location: str | None) -> set[str]:
    if not location:
        return set()
    categories: set[str] = set()
    if CANADA_LOCATION_PATTERN.search(location):
        categories.add("canada")
    if USA_LOCATION_PATTERN.search(location):
        categories.add("usa")
    if INTERNATIONAL_LOCATION_PATTERN.search(location):
        categories.add("international")
    return categories


def is_graduate_degree_role(title: str | None, description: str | None) -> bool:
    text = " ".join(part for part in (title, description) if part)
    if GRADUATE_DEGREE_ROLE_PATTERN.search(text):
        return True
    if not MASTER_DEGREE_PATTERN.search(text):
        return False
    return not bool(BACHELOR_OR_MASTER_PATTERN.search(text))


def is_hardware_only_role(title: str | None) -> bool:
    if not title:
        return False
    return bool(HARDWARE_ROLE_PATTERN.search(title)) and not bool(
        HARDWARE_SOFTWARE_ESCAPE_PATTERN.search(title)
    )


def has_software_keyword(title: str | None, description: str | None) -> bool:
    text = " ".join(part for part in (title, description) if part)
    return bool(SOFTWARE_KEYWORD_PATTERN.search(text))


def has_intern_keyword(title: str | None) -> bool:
    text = title or ""
    return bool(INTERN_INTENT_PATTERN.search(text))
