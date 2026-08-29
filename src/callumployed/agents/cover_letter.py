import json
import re
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict

from callumployed.agents.posting_link_classifier import ChatModelFactory, build_chat_model
from callumployed.config import LlmSettings


class CoverLetterModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class CoverLetterDraft(CoverLetterModel):
    latex: str
    summary: str
    example_ids: list[int] = []


class ApplicantProfile(CoverLetterModel):
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    institution: str = ""
    degree: str = ""

    @property
    def full_name(self) -> str:
        configured_name = " ".join(
            part for part in (self.first_name, self.last_name) if part
        ).strip()
        return configured_name or "Applicant"

    @property
    def latex_sender_block(self) -> str:
        lines = [self.full_name, self.institution, self.degree, self.email]
        return "\\\\\n".join(_escape_latex_profile_value(line) for line in lines if line)


class CoverLetterSearchTool(Protocol):
    def __call__(self, query: str, *, limit: int = 3) -> list[dict[str, object]]: ...


MAX_COVER_LETTER_SEARCH_QUERY_CHARS = 24000
MAX_ROLE_CONTEXT_CHARS = 12000
MAX_RESUME_CONTEXT_CHARS = 16000
MAX_OTHER_EXPERIENCE_CONTEXT_CHARS = 16000
MAX_COVER_LETTER_EXAMPLE_CONTEXT_CHARS = 12000
MAX_REGENERATION_TWEAKS_CHARS = 3000
MAX_PREVIOUS_COVER_LETTER_CHARS = 12000

_PERSON_NAME = r"[A-Z][A-Za-z'’-]+(?:[ \t]+[A-Z][A-Za-z'’-]+){1,3}"
_TITLE_CASE_PERSON_NAME = r"[A-Z][a-z'’-]+(?:[ \t]+[A-Z][a-z'’-]+){1,3}"
_HIRING_CONTACT_PATTERNS = (
    re.compile(
        rf"(?m)^\s*(?i:hiring manager|recruiter|contact(?: person)?)\s*[:\-]\s*"
        rf"(?P<name>{_PERSON_NAME})\b"
    ),
    re.compile(
        rf"(?i:\bcontact)\s+(?P<name>{_TITLE_CASE_PERSON_NAME})\b"
        r"(?=\s+(?i:for|at|with|regarding)\b|[.,;\n])"
    ),
)
_NON_PERSON_CONTACT_NAMES = {
    "Hiring Team",
    "Our Team",
    "Recruiting Team",
    "Talent Acquisition",
}
_NON_PERSON_CONTACT_TOKENS = {
    "acquisition",
    "analyst",
    "architect",
    "apply",
    "careers",
    "coordinator",
    "department",
    "designer",
    "developer",
    "details",
    "director",
    "engineer",
    "human",
    "intern",
    "job",
    "lead",
    "now",
    "product",
    "project",
    "resources",
    "senior",
    "software",
    "specialist",
    "team",
}


def _bounded_context_text(value: object, limit: int) -> str:
    text = str(value or "")
    if len(text) <= limit:
        return text
    marker = "\n...[context truncated]...\n"
    if limit <= len(marker):
        return text[:limit]
    available = limit - len(marker)
    head_length = available * 2 // 3
    return f"{text[:head_length]}{marker}{text[-(available - head_length):]}"


def find_named_hiring_contact(description: object) -> str | None:
    text = str(description or "")
    for pattern in _HIRING_CONTACT_PATTERNS:
        match = pattern.search(text)
        if match is None:
            continue
        name = " ".join(match.group("name").split())
        name_tokens = {token.casefold() for token in name.split()}
        if (
            name not in _NON_PERSON_CONTACT_NAMES
            and name_tokens.isdisjoint(_NON_PERSON_CONTACT_TOKENS)
        ):
            return name
    return None


def _bounded_context_items(
    items: list[dict[str, Any]],
    total_content_limit: int,
    *,
    include_similarity: bool = False,
) -> list[dict[str, object]]:
    if not items:
        return []
    item_limit = max(1, total_content_limit // len(items))
    bounded_items: list[dict[str, object]] = []
    for item in items:
        bounded_item: dict[str, object] = {
            "id": item.get("id"),
            "filename": item.get("filename"),
            "content": _bounded_context_text(item.get("content"), item_limit),
        }
        if item.get("updated_at") is not None:
            bounded_item["updated_at"] = item.get("updated_at")
        if include_similarity and item.get("similarity") is not None:
            bounded_item["similarity"] = item.get("similarity")
        bounded_items.append(bounded_item)
    return bounded_items


SYSTEM_PROMPT = """
You generate a role-specific LaTeX cover letter for a job application.

Always use the provided resume context and job context. Use retrieved past cover
letters as the primary writing-style reference. Match the user's voice from
those examples: sentence length, directness, level of technical specificity,
paragraph rhythm, and closing style. Do not copy company-specific claims that do
not apply to the current job.
When provided, other_experience_context contains role-relevant projects / employment history
pages retrieved from the indexed application materials; those details may or may not already
be on the resume. Review every retrieved page before drafting.
First identify the strongest concrete evidence in those pages, compare it with
the posting requirements, and deliberately use the most relevant evidence when
it strengthens the letter. Do not treat this context as decorative or ignore it
in favor of generic prose. If none of the retrieved evidence is genuinely
relevant, rely on the resume instead rather than forcing a weak connection. You
may use indexed experience that is not already on the resume, but do not imply
it appears on the resume unless resume_context also supports it.
When regeneration tweaks are provided, treat them as direct user feedback and
apply them while preserving the resume/job truthfulness constraints. When a
previous_cover_letter_context block is provided, treat regeneration_tweaks as
feedback on that exact prior draft. Identify what the feedback is asking you to
change, what previous draft text you are operating on, and then produce the full
updated LaTeX document.

Integrate the context deliberately:
- use job_context for the company, role title, location, and retrieved local role
  requirements; never infer requirements not present in those retrieved chunks
- use resume_context only for claims that are directly supported by the resume
- use other_experience_context for additional truthful projects or employment
  history that could strengthen the cover letter even if it is not already in
  resume_context; explicitly prefer items that match job_context requirements
- use cover_letter_example_tool_results for writing style, paragraph rhythm,
  specificity, and closing style, not for facts about the current role
- use regeneration_tweaks as direct edit instructions when present
- when previous_cover_letter_context is present, revise the previous draft
  deliberately instead of starting from scratch; preserve strong targeted
  material, remove or rewrite the parts contradicted by the feedback, and keep
  the final letter grounded in resume_context and job_context
- select the 2-3 strongest overlaps between the resume and posting; do not try
  to mention every relevant technology or project
- synthesize those experiences into smooth prose in the user's voice; do not dump
  resume bullets into paragraphs or awkwardly combine unrelated experiences
- tailor every body paragraph to the specific position; a paragraph that could
  be sent unchanged to another company is too generic
- the first body paragraph must name the exact company and role, then connect
  the user's interest to concrete work, team, domain, or requirements from
  job_context.description
- the remaining body paragraphs must pair specific resume evidence with
  specific responsibilities or requirements from the posting
- reuse 1-2 distinctive phrases from the posting when they are truthful and
  natural, but do not invent company facts or unsupported enthusiasm
- avoid generic filler such as "your mission", "innovative technology",
  "cutting-edge", "strong background", or "fast-paced environment" unless the
  phrase is tied to a concrete posting detail

The output must be a complete LaTeX letter document, not a plain body. Format it
like a professional letter and mirror the useful structure/style patterns from
the retrieved examples:
- use the simple professional LaTeX cover-letter template shape: 11pt
  letterpaper, 1in margins, sender block, recipient/date block, opening,
  concise body paragraphs, and closing/signature
- use a compact article-based letter layout when needed; avoid LaTeX letter
  class spacing if it risks spilling past one page
- keep the sender/contact header left-aligned at the top of the page
- the sender/contact header must contain only the non-empty name, institution,
  degree, and email values in applicant_profile; copy those identity values
  exactly and never infer identity details from examples, the resume, or prior drafts
- do not include the user's personal website, GitHub, LinkedIn, phone number,
  or extra links in the sender/contact header
- use proper LaTeX line breaks (`\\`) for stacked header/contact/signature
  lines; never use a single trailing backslash as a line break
- inspect the complete job description for an explicitly named hiring contact,
  recruiter, or hiring manager. If one is clearly identified, address that person
  as `Dear <name>,`; otherwise use `Dear Hiring Manager,`. Never use
  `Dear Hiring Team,`, and never guess a person's name
- keep the salutation in its own flush-left paragraph. Never place the first body
  sentence on the same line or in the same LaTeX paragraph as the salutation
- do not put manual `\\` line breaks after body paragraphs; separate body
  paragraphs with blank lines
- do not use the fullpage or parskip packages
- do not use LaTeX's built-in \\address{...} sender block
- escape LaTeX special characters in body text, including `\\&` for ampersands
  such as `R\\&D` and `\\%` for percentages such as `50\\%`
- include opening and closing lines
- keep paragraphs visually separated with vertical space
- ensure the generated PDF fits on one page at 11pt and uses the page effectively;
  write 3-4 cohesive body paragraphs, roughly 325-400 words total, with enough
  source-supported detail to avoid a large empty lower half of the page
- keep it concise, specific, and honest
- mention only experience supported by resume_context or other_experience_context
- align wording with the posting's strongest requirements
- never use em dashes. Do not emit Unicode em dashes, en dashes, horizontal
  bars, LaTeX --- sequences, LaTeX -- sequences, `\\textemdash`, or
  `\\textendash`. If resume, job, or example text contains dash punctuation,
  rewrite it with commas, semicolons, parentheses, or short sentences instead
- use plain ASCII apostrophes and quotes in body text; do not emit smart quotes
  or hidden/control characters

Use this exact LaTeX scaffold for the `latex` field, replacing only the
recipient lines, greeting if needed, and body paragraphs:
\\documentclass[letterpaper,11pt]{article}
\\usepackage[margin=1in]{geometry}
\\usepackage[hidelinks]{hyperref}
\\setlength{\\parskip}{0.55em}
\\setlength{\\parindent}{1.5em}
\\pagestyle{empty}
\\begin{document}
\\noindent <applicant_profile.latex_sender_block>\\par
\\vspace{1.1em}
\\noindent <recipient/company lines, including date>\\par
\\vspace{1.1em}

\\noindent Dear <explicitly named hiring contact, or Hiring Manager>,\\par
\\vspace{0.35em}

<three or four concise body paragraphs>

\\vspace{0.35em}
\\noindent Sincerely,\\\\[12pt]
<applicant_profile.signature_name>
\\end{document}

Do not include resume-only packages or commands such as `fancyhdr`, `titlesec`,
`fullpage`, `parskip`, `\\pdfgentounicode`, `glyphtounicode`, or
`\\input{glyphtounicode}`.

Return only JSON matching:
{"latex":"...","summary":"short generation note","example_ids":[1,2]}
""".strip()


class CoverLetterAgent:
    settings: LlmSettings
    chat_model_factory: ChatModelFactory | None
    search_tool: CoverLetterSearchTool

    def __init__(
        self,
        *,
        search_tool: CoverLetterSearchTool,
        settings: LlmSettings | None = None,
        chat_model_factory: ChatModelFactory | None = None,
    ) -> None:
        self.settings = settings or LlmSettings()
        self.chat_model_factory = chat_model_factory
        self.search_tool = search_tool

    async def generate(
        self,
        *,
        role: dict[str, Any],
        resume_content: str,
        applicant_profile: ApplicantProfile | None = None,
        other_experience_context: list[dict[str, Any]] | None = None,
        role_context: list[dict[str, Any]] | None = None,
        tweaks: str | None = None,
        previous_cover_letter_latex: str | None = None,
    ) -> CoverLetterDraft:
        bounded_experience_context = _bounded_context_items(
            other_experience_context or [],
            MAX_OTHER_EXPERIENCE_CONTEXT_CHARS,
        )
        other_experience_text = " ".join(
            str(item.get("content") or "") for item in bounded_experience_context
        )
        role_context_text = " ".join(
            str(item.get("content") or "") for item in (role_context or [])
        )
        queries = [
            _bounded_context_text(
                " ".join(
                    [
                        str(role.get("title") or ""),
                        role_context_text,
                        resume_content,
                        other_experience_text,
                    ]
                ),
                MAX_COVER_LETTER_SEARCH_QUERY_CHARS,
            ),
            " ".join(
                [
                    str(role.get("title") or ""),
                    str(role.get("company_name") or ""),
                    str(role.get("location") or ""),
                ]
            ),
        ]
        examples_by_id: dict[int, dict[str, object]] = {}
        for query in queries:
            for example in self.search_tool(query, limit=3):
                example_id = example.get("id")
                if isinstance(example_id, int):
                    examples_by_id[example_id] = example

        model = (
            self.chat_model_factory(self.settings)
            if self.chat_model_factory is not None
            else build_chat_model(self.settings).with_structured_output(CoverLetterDraft)
        )
        result = await model.ainvoke(
            build_cover_letter_prompt(
                applicant_profile=applicant_profile or ApplicantProfile(),
                role=role,
                resume_content=resume_content,
                other_experience_context=other_experience_context,
                role_context=role_context,
                cover_letter_examples=list(examples_by_id.values()),
                tweaks=tweaks,
                previous_cover_letter_latex=previous_cover_letter_latex,
            )
        )
        draft = CoverLetterDraft.model_validate(result)
        return draft.model_copy(
            update={
                "latex": strip_cover_letter_dash_punctuation(draft.latex),
                "summary": strip_cover_letter_dash_punctuation(draft.summary),
            }
        )


def strip_cover_letter_dash_punctuation(text: str) -> str:
    content = re.sub(r"\\text(?:em|en)dash(?:\{\})?", ", ", text)
    content = re.sub(r"\s*(?:\u2013|\u2014|\u2015|---|--)\s*", ", ", content)
    content = re.sub(r",\s*,+", ",", content)
    content = re.sub(r"\s+,", ",", content)
    content = re.sub(r",\s+", ", ", content)
    content = re.sub(r",\s*([.;:!?])", r"\1", content)
    return content


def _escape_latex_profile_value(value: str) -> str:
    escaped = value.replace("\\", r"\textbackslash{}")
    for character, replacement in (
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
    ):
        escaped = escaped.replace(character, replacement)
    return escaped


def build_cover_letter_prompt(
    *,
    applicant_profile: ApplicantProfile,
    role: dict[str, Any],
    resume_content: str,
    other_experience_context: list[dict[str, Any]] | None = None,
    role_context: list[dict[str, Any]] | None = None,
    cover_letter_examples: list[dict[str, object]],
    tweaks: str | None = None,
    previous_cover_letter_latex: str | None = None,
) -> str:
    payload = {
        "applicant_profile": {
            **applicant_profile.model_dump(),
            "full_name": applicant_profile.full_name,
            "signature_name": applicant_profile.full_name,
            "latex_sender_block": applicant_profile.latex_sender_block,
        },
        "job_context": {
            "id": role.get("id"),
            "company_id": role.get("company_id"),
            "company_name": role.get("company_name"),
            "title": role.get("title"),
            "url": role.get("role_url"),
            "location": role.get("location"),
            "description": _bounded_context_text(
                role.get("description"), MAX_ROLE_CONTEXT_CHARS
            ),
            "named_hiring_contact": find_named_hiring_contact(role.get("description")),
            "role_context_chunks": _bounded_context_items(
                role_context or [], MAX_ROLE_CONTEXT_CHARS, include_similarity=True
            ),
        },
        "resume_context": {
            "format": "latex",
            "content": _bounded_context_text(resume_content, MAX_RESUME_CONTEXT_CHARS),
        },
        "other_experience_context": _bounded_context_items(
            other_experience_context or [],
            MAX_OTHER_EXPERIENCE_CONTEXT_CHARS,
        ),
        "cover_letter_example_tool_results": _bounded_context_items(
            cover_letter_examples,
            MAX_COVER_LETTER_EXAMPLE_CONTEXT_CHARS,
            include_similarity=True,
        ),
    }
    if tweaks:
        payload["regeneration_tweaks"] = _bounded_context_text(
            tweaks, MAX_REGENERATION_TWEAKS_CHARS
        )
    if tweaks and previous_cover_letter_latex:
        payload["previous_cover_letter_context"] = {
            "purpose": "revise this prior draft according to regeneration_tweaks",
            "draft_latex": _bounded_context_text(
                previous_cover_letter_latex, MAX_PREVIOUS_COVER_LETTER_CHARS
            ),
        }
    return f"{SYSTEM_PROMPT}\n\nContext:\n{json.dumps(payload, indent=2, sort_keys=True)}"


async def generate_cover_letter(
    *,
    role: dict[str, Any],
    resume_content: str,
    search_tool: CoverLetterSearchTool,
    applicant_profile: ApplicantProfile | None = None,
    other_experience_context: list[dict[str, Any]] | None = None,
    role_context: list[dict[str, Any]] | None = None,
    tweaks: str | None = None,
    previous_cover_letter_latex: str | None = None,
    settings: LlmSettings | None = None,
    chat_model_factory: ChatModelFactory | None = None,
) -> CoverLetterDraft:
    return await CoverLetterAgent(
        search_tool=search_tool,
        settings=settings,
        chat_model_factory=chat_model_factory,
    ).generate(
        role=role,
        resume_content=resume_content,
        applicant_profile=applicant_profile,
        other_experience_context=other_experience_context,
        role_context=role_context,
        tweaks=tweaks,
        previous_cover_letter_latex=previous_cover_letter_latex,
    )
