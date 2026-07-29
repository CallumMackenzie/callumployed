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


class CoverLetterSearchTool(Protocol):
    def __call__(self, query: str, *, limit: int = 3) -> list[dict[str, object]]: ...


SYSTEM_PROMPT = """
You generate a role-specific LaTeX cover letter for a job application.

Always use the provided resume context and job context. Use retrieved past cover
letters as the primary writing-style reference. Match the user's voice from
those examples: sentence length, directness, level of technical specificity,
paragraph rhythm, and closing style. Do not copy company-specific claims that do
not apply to the current job.
When regeneration tweaks are provided, treat them as direct user feedback and
apply them while preserving the resume/job truthfulness constraints. When a
previous_cover_letter_context block is provided, treat regeneration_tweaks as
feedback on that exact prior draft. Identify what the feedback is asking you to
change, what previous draft text you are operating on, and then produce the full
updated LaTeX document.

Integrate the context deliberately:
- use job_context for the company, role title, location, and strongest role
  requirements
- use resume_context only for claims that are directly supported by the resume
- use cover_letter_example_tool_results for writing style, paragraph rhythm,
  specificity, and closing style, not for facts about the current role
- use regeneration_tweaks as direct edit instructions when present
- when previous_cover_letter_context is present, revise the previous draft
  deliberately instead of starting from scratch; preserve strong targeted
  material, remove or rewrite the parts contradicted by the feedback, and keep
  the final letter grounded in resume_context and job_context
- select the 2-3 strongest overlaps between the resume and posting; do not try
  to mention every relevant technology or project
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
- the sender/contact header must contain only: Callum Mackenzie, University of
  British Columbia, BSc Computer Science \\& Statistics, and
  callum@camackenzie.com
- do not include the user's personal website, GitHub, LinkedIn, phone number,
  or extra links in the sender/contact header
- use proper LaTeX line breaks (`\\`) for stacked header/contact/signature
  lines; never use a single trailing backslash as a line break
- do not put manual `\\` line breaks after body paragraphs; separate body
  paragraphs with blank lines
- do not use the fullpage or parskip packages
- do not use LaTeX's built-in \\address{...} sender block
- escape LaTeX special characters in body text, including `\\&` for ampersands
  such as `R\\&D` and `\\%` for percentages such as `50\\%`
- include opening and closing lines
- keep paragraphs visually separated with vertical space
- ensure the generated PDF fits on one page at 11pt; keep the body to 3 short
  paragraphs plus the opening and closing, roughly 225-275 words total
- keep it concise, specific, and honest
- mention only experience supported by the resume
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
\\setlength{\\parskip}{0.85em}
\\setlength{\\parindent}{0pt}
\\pagestyle{empty}
\\begin{document}
Callum Mackenzie\\\\
University of British Columbia\\\\
BSc Computer Science \\& Statistics\\\\
callum@camackenzie.com\\\\[12pt]
<recipient/company lines>\\\\[12pt]

Dear Hiring Team,

<three short body paragraphs>

Sincerely,\\\\[12pt]
Callum Mackenzie
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
        tweaks: str | None = None,
        previous_cover_letter_latex: str | None = None,
    ) -> CoverLetterDraft:
        queries = [
            " ".join(
                [
                    str(role.get("title") or ""),
                    str(role.get("description") or ""),
                    resume_content,
                ]
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
                role=role,
                resume_content=resume_content,
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


def build_cover_letter_prompt(
    *,
    role: dict[str, Any],
    resume_content: str,
    cover_letter_examples: list[dict[str, object]],
    tweaks: str | None = None,
    previous_cover_letter_latex: str | None = None,
) -> str:
    payload = {
        "job_context": {
            "id": role.get("id"),
            "company_id": role.get("company_id"),
            "company_name": role.get("company_name"),
            "title": role.get("title"),
            "url": role.get("role_url"),
            "location": role.get("location"),
            "description": role.get("description"),
        },
        "resume_context": {
            "format": "latex",
            "content": resume_content,
        },
        "cover_letter_example_tool_results": cover_letter_examples,
    }
    if tweaks:
        payload["regeneration_tweaks"] = tweaks
    if tweaks and previous_cover_letter_latex:
        payload["previous_cover_letter_context"] = {
            "purpose": "revise this prior draft according to regeneration_tweaks",
            "draft_latex": previous_cover_letter_latex,
        }
    return f"{SYSTEM_PROMPT}\n\nContext:\n{json.dumps(payload, indent=2, sort_keys=True)}"


async def generate_cover_letter(
    *,
    role: dict[str, Any],
    resume_content: str,
    search_tool: CoverLetterSearchTool,
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
        tweaks=tweaks,
        previous_cover_letter_latex=previous_cover_letter_latex,
    )
