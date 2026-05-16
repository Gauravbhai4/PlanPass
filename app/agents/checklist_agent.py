"""Flow 2: Pre-Submission Checklist Agent.

Takes plot details from the architect and returns a BBMP/GBA-compliance
checklist using the Karnataka skills layer.
"""
from typing import Dict, Any
import json

from app.azure_client import call_chat
from app.skills.skill_loader import load_skills


CHECKLIST_SKILLS = [
    "zonal-regulations-2026",
    "setback-table",
    "far-table",
    "khata-rules",
    "nambike-nakshe",
    "parking-norms",
    "ktcp-act-1961",
    "decision-tree-router",
]


SYSTEM_PROMPT = """You are Permit Setu, an expert BBMP/GBA (Greater Bengaluru Authority) building plan compliance assistant. ("Setu" means "bridge" — you are the bridge between the architect and city approval.)

Your job is to review a residential project proposal and produce a comprehensive pre-submission checklist using the official Karnataka rules in your knowledge base below. The architect or owner will use your output to ensure compliance BEFORE submitting to the BPAS portal.

You have access to the following Karnataka skill reference files. Use them as your authoritative source. Cite specific rules and section numbers when relevant.

{skills}

---

OUTPUT RULES:
1. ALWAYS produce output in valid JSON matching this exact schema:
{{
  "summary": "One-paragraph executive summary of compliance posture",
  "submission_track": "Nambike Nakshe" | "Standard Review",
  "eligibility_check": {{
    "eligible_to_submit": true | false,
    "blockers": ["list of blockers if any"]
  }},
  "applicable_rules": {{
    "front_setback_m": "0.75",
    "side_setback_m": "0.6",
    "rear_setback_m": "0",
    "max_far": "1.75",
    "max_height": "G+2",
    "max_built_up_sqft": "2100",
    "parking_required": "1 car",
    "ev_parking_required": "Yes / No",
    "oc_required": "Yes / No"
  }},
  "documents_required": ["E-Khata", "ePID", "..."],
  "nocs_required": ["Fire NOC if G+3+", "..."],
  "gotchas": ["specific risks the architect should not miss"],
  "estimated_timeline_days": "30-45",
  "estimated_fees_inr": "Approximate fee breakdown",
  "next_actions": ["ordered list of what to do next"]
}}

2. Use actual values from the rules, not placeholders. If a value depends on something you don't know, state the dependency.
3. Be specific. Cite the rule section (e.g., "KTCP Act §17", "GBA 2026 Zonal Regulations clause X").
4. Flag B-Khata as an automatic blocker.
5. Flag the January 2026 zonal regulation changes as relevant when they apply.
"""


USER_PROMPT_TEMPLATE = """Please review this Bengaluru residential project and produce the pre-submission compliance checklist.

PROJECT DETAILS:
- Plot dimensions: {plot_dimensions}
- Plot area: {plot_area_sqft} sq ft
- Land use zone: {zone}
- Khata type: {khata_type}
- Road width facing plot: {road_width_ft} ft
- Proposed construction type: {construction_type}
- Proposed floors: {proposed_floors}
- Proposed built-up area: {built_up_area_sqft} sq ft
- Number of dwelling units: {num_units}
- Project location (area in Bengaluru): {location}
- Special conditions: {special_conditions}

Produce the complete JSON checklist now.
"""


def run_checklist_agent(project_details: Dict[str, Any]) -> Dict[str, Any]:
    """Run the pre-submission checklist flow.

    Args:
        project_details: Dict with project fields (see USER_PROMPT_TEMPLATE).

    Returns:
        Parsed JSON dict containing the full compliance checklist.
    """
    skills_text = load_skills(CHECKLIST_SKILLS)
    system_prompt = SYSTEM_PROMPT.format(skills=skills_text)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        plot_dimensions=project_details.get("plot_dimensions", "Not specified"),
        plot_area_sqft=project_details.get("plot_area_sqft", "Not specified"),
        zone=project_details.get("zone", "R (Residential)"),
        khata_type=project_details.get("khata_type", "Not specified"),
        road_width_ft=project_details.get("road_width_ft", "Not specified"),
        construction_type=project_details.get("construction_type", "New construction"),
        proposed_floors=project_details.get("proposed_floors", "Not specified"),
        built_up_area_sqft=project_details.get("built_up_area_sqft", "Not specified"),
        num_units=project_details.get("num_units", "1"),
        location=project_details.get("location", "Bengaluru"),
        special_conditions=project_details.get("special_conditions", "None"),
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    raw_response = call_chat(
        messages=messages,
        max_completion_tokens=4000,
        response_format={"type": "json_object"},
    )

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse model response as JSON",
            "raw_response": raw_response,
        }
