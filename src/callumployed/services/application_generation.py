from __future__ import annotations

import json
from typing import Any

MAX_APPLICATION_CONTEXT_CHARS = 180_000
TRUNCATION_MARKER = "\n[... truncated by Callumployed ...]\n"


def _bounded_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    if limit <= len(TRUNCATION_MARKER):
        return TRUNCATION_MARKER[:limit]
    available = limit - len(TRUNCATION_MARKER)
    head_length = available * 2 // 3
    tail_length = available - head_length
    return value[:head_length] + TRUNCATION_MARKER + value[-tail_length:]


def build_application_prompt(
    *,
    task: str,
    role: dict[str, Any],
    master_resume: str,
    tailored_resume: str | None,
    cover_letter: str | None,
    cover_letter_examples: list[dict[str, Any]],
    experience_sections: list[dict[str, Any]],
    role_context: list[dict[str, Any]],
    question: str | None = None,
    deterministic_instructions: str | None = None,
    previous_output: str | None = None,
) -> str:
    web_policy = (
        "Web search is unavailable. Use only the saved application materials and saved role. "
        "Keep source authority internal; do not mention sources, context, evidence checks, "
        "prompts, generation, or supplied materials in the user-facing answer."
        if task == "answer_question"
        else (
            "Web search is unavailable. Use only the saved application materials and saved role "
            "as factual authorities."
        )
    )
    output_contract = {
        "answer_question": '{"answer":"..."}',
        "resume": '{"latex":"complete LaTeX document","summary":"short summary","sources":[]}',
        "cover_letter": '{"latex":"complete LaTeX document","example_ids":[],"sources":[]}',
    }.get(task, '{"answer":"..."}')
    fixed_sections = [
        "CALLUMPLOYED APPLICATION GENERATION TASK",
        f"Task: {task}",
        "Return strict JSON only, with no markdown fence or commentary.",
        f"Required JSON shape: {output_contract}",
        (
            "Write the answer using professional prose with normal sentence capitalization. "
            "Preserve the exact capitalization of names, acronyms, products, and technologies."
            if task == "answer_question"
            else "Preserve professional capitalization in all user-facing prose."
        ),
        web_policy,
        (
            "SOURCE AUTHORITY POLICY: Saved application materials and the saved role are the only "
            "authorities. You must not invent applicant facts, metrics, experience, education, "
            "skills, referrals, outcomes, company claims, or job requirements. Preserve exact "
            "saved facts."
        ),
        *(
            [
                (
                    "APPLICATION ANSWER CONTRACT: Write in first person as the applicant. Answer "
                    "the employer's question directly in polished prose ready to paste unchanged. "
                    "Keep source authority internal. Do not volunteer a disclaimer about missing "
                    "experience. For a question offering multiple alternatives, answer with the "
                    "supported alternatives and silently omit unsupported ones; do not infer that "
                    "no events are planned merely because future plans are absent. If the question "
                    "explicitly asks about entirely unsupported experience, answer plainly and "
                    "briefly without guessing, then pivot only to relevant supported experience. "
                    "Do not include citations or URLs unless requested."
                )
            ]
            if task == "answer_question"
            else []
        ),
    ]
    variable_sections = [
        (
            "Deterministic Callumployed instructions:",
            deterministic_instructions or "(none)",
            8,
        ),
        (
            "Exact saved role JSON:",
            json.dumps(role, ensure_ascii=False, default=str),
            20,
        ),
        ("Question:", question or "(not applicable)", 5),
        ("Master resume (authoritative applicant document):", master_resume, 45),
        ("Current tailored resume:", tailored_resume or "(none)", 18),
        ("Current cover letter:", cover_letter or "(none)", 18),
        ("Prior generated output for bounded revision:", previous_output or "(none)", 18),
        ("Saved cover-letter examples:", _json_material(cover_letter_examples), 10),
        (
            "All bounded indexed experience-note sections:",
            _json_material(experience_sections),
            15,
        ),
        ("Saved role-context chunks:", _json_material(role_context), 10),
    ]
    empty_variable_sections = [f"{label}\n" for label, _value, _weight in variable_sections]
    overhead = len("\n\n".join([*fixed_sections, *empty_variable_sections]))
    available = MAX_APPLICATION_CONTEXT_CHARS - overhead
    if available < 0:
        raise RuntimeError("Application prompt fixed contract exceeds its context ceiling.")
    total_weight = sum(weight for _label, _value, weight in variable_sections)
    bounded_sections = [
        f"{label}\n{_bounded_text(value, available * weight // total_weight)}"
        for label, value, weight in variable_sections
    ]
    prompt = "\n\n".join([*fixed_sections, *bounded_sections])
    if len(prompt) > MAX_APPLICATION_CONTEXT_CHARS:
        raise RuntimeError("Application prompt exceeded its context ceiling after budgeting.")
    return prompt


def _json_material(items: list[dict[str, Any]]) -> str:
    return json.dumps(items, ensure_ascii=False, default=str, separators=(",", ":"))
