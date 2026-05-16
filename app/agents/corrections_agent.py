"""Flow 1: BBMP Corrections Letter Interpreter Agent.

Takes a corrections letter (PDF text) and an optional plan summary, and
produces a four-part response package:
  1. response_letter - professional letter back to BBMP/GBA
  2. corrections_report - per-objection status dashboard
  3. scope_of_work - drafting task list for the CAD team
  4. sheet_annotations - JSON per-sheet markup instructions
"""
from typing import Dict, Any, Optional
import json

from app.azure_client import call_chat
from app.skills.skill_loader import load_skills


CORRECTIONS_SKILLS = [
    "ktcp-act-1961",
    "zonal-regulations-2026",
    "setback-table",
    "far-table",
    "parking-norms",
    "khata-rules",
    "corrections-workflow",
]


SYSTEM_PROMPT = """You are Permit Setu, an expert BBMP/GBA building plan corrections-response specialist. ("Setu" means "bridge" — you are the bridge between the architect and city approval.)

You will be given a BBMP/GBA corrections letter (extracted text from the original PDF). Your job is to:

1. Parse each numbered objection in the letter
2. Categorize each objection (auto-fixable / needs homeowner input / needs engineer / code conflict / documentation / disputable)
3. Cross-reference against Karnataka law and the 2026 zonal regulations
4. Generate a complete response package

You have authoritative access to the following Karnataka law and BBMP procedure references. Use them as the source of truth.

{skills}

---

OUTPUT RULES:
Produce a single JSON object matching this exact schema:

{{
  "case_summary": "1-2 paragraph summary of the case and BBMP's overall concerns",
  "objections": [
    {{
      "number": 1,
      "verbatim": "exact text of the objection quoted from the letter",
      "category": "auto-fixable" | "needs homeowner input" | "needs engineer" | "code conflict" | "documentation" | "disputable",
      "cited_rule": "e.g., KTCP Act §17, or BBMP Bye-Laws clause X",
      "agent_analysis": "what the objection means in plain language",
      "recommended_response": "what the architect should respond",
      "supporting_docs_needed": ["..."]
    }}
  ],
  "response_letter": "Full formal response letter in BBMP format, ready to copy-paste. Use the exact format from the corrections-workflow skill.",
  "corrections_report": "A markdown-formatted status dashboard showing each objection, category, action, and owner.",
  "scope_of_work": "A markdown-formatted task list for the architect's CAD/drafting team, organized by sheet.",
  "sheet_annotations": {{
    "A1": ["instruction 1", "instruction 2"],
    "A2": ["..."]
  }},
  "open_questions_for_owner": ["questions the architect needs the homeowner to answer before resubmission"]
}}

Always cite specific rule sections. Always quote objections verbatim. Be specific and actionable.
"""


USER_PROMPT_TEMPLATE = """Here is the BBMP/GBA corrections letter text:

==== CORRECTIONS LETTER (EXTRACTED FROM PDF) ====
{corrections_text}
==== END CORRECTIONS LETTER ====

{plan_summary_block}

Project context (provided by the architect):
{project_context}

Now produce the complete JSON response package.
"""


def run_corrections_agent(
    corrections_text: str,
    plan_summary: Optional[str] = None,
    project_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Run the corrections-interpreter flow.

    Args:
        corrections_text: Text extracted from the BBMP corrections-letter PDF
        plan_summary: Optional summary of the plan set (extracted text or
            architect-provided description)
        project_context: Optional dict with project details (plot size,
            zone, etc.)

    Returns:
        Parsed JSON dict containing the full response package.
    """
    skills_text = load_skills(CORRECTIONS_SKILLS)
    system_prompt = SYSTEM_PROMPT.format(skills=skills_text)

    plan_summary_block = ""
    if plan_summary:
        plan_summary_block = (
            "\n==== PLAN SUMMARY (extracted from plan PDF) ====\n"
            + plan_summary
            + "\n==== END PLAN SUMMARY ====\n"
        )

    context_str = "None provided."
    if project_context:
        context_str = "\n".join(
            f"- {k}: {v}" for k, v in project_context.items() if v
        )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        corrections_text=corrections_text,
        plan_summary_block=plan_summary_block,
        project_context=context_str,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    raw_response = call_chat(
        messages=messages,
        max_completion_tokens=6000,
        response_format={"type": "json_object"},
    )

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse model response as JSON",
            "raw_response": raw_response,
        }
