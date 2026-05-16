"""Plan Vision Agent — reads architectural plan PDFs with Azure OpenAI vision.

Architectural plan PDFs are mostly raster/vector drawings — title blocks,
floor plans, elevations, sections, dimension lines, FAR tables — that
text extraction misses entirely. This agent renders each plan sheet to an
image and asks a vision-capable Azure OpenAI deployment (e.g., gpt-4o) to:

  1. Identify what's on each sheet
  2. Extract visible measurements (setbacks, plot dims, FAR table values)
  3. Flag obvious compliance red flags

The output is a structured sheet manifest the corrections agent can
reason over.
"""
from __future__ import annotations

import json
from typing import Dict, Any

from app.azure_client import call_vision
from app.pdf_utils import pdf_to_base64_images, get_pdf_page_count
from app.skills.skill_loader import load_skills


# Load BBMP-specific rules so the vision model can flag obvious issues
VISION_SKILLS = [
    "setback-table",
    "far-table",
    "parking-norms",
    "zonal-regulations-2026",
]


SYSTEM_PROMPT_TEMPLATE = """You are a senior Bengaluru architectural draftsperson and BBMP/GBA plan reviewer with 20+ years of experience.

You will be shown one or more architectural plan sheets from a residential project in BBMP/GBA limits. Carefully read each sheet (title blocks, dimension lines, notes, FAR tables, schedules).

For each sheet, identify:
  1. Sheet number and title (usually in the title block — bottom-right or bottom-center)
  2. What is drawn on the sheet (site plan, ground floor plan, first floor plan, elevations, sections, plumbing, electrical, structural, etc.)
  3. Visible measurements relevant to BBMP compliance:
     - Plot dimensions (e.g., 30 ft x 40 ft)
     - Setbacks: front, rear, side(s) - in metres or feet exactly as shown
     - FAR table values if visible (plot area, total built-up, ratio)
     - Number of car/2-wheeler parking spaces, dimensions
     - Building height, number of floors
     - Road width facing plot

You have authoritative reference to the following Karnataka rules. Use them to flag potential compliance issues you can see:

{skills}

---

OUTPUT REQUIREMENTS:
Return a SINGLE JSON object with this exact schema:

{{
  "sheet_manifest": [
    {{
      "page_index": 0,
      "sheet_number": "A1 or similar (or 'unknown' if not visible)",
      "sheet_title": "e.g., 'Site Plan & Cover Sheet'",
      "drawing_types": ["site plan", "key map", "title block"],
      "key_measurements": {{
        "plot_dimensions": "30 ft x 40 ft",
        "plot_area_sqft": "1200",
        "front_setback": "0.75 m",
        "rear_setback": "1.5 m",
        "side_setback_left": "0.9 m",
        "side_setback_right": "0.9 m",
        "road_width": "30 ft",
        "far_value": "1.75",
        "total_built_up_sqft": "2100",
        "floors": "G+2",
        "parking_spaces": "1 car + 2 two-wheeler"
      }},
      "compliance_flags": [
        "Potential issue: front setback shows 0.6 m which is below the 0.75 m minimum per Jan 2026 Zonal Regulations"
      ],
      "notes": "Any observations not captured above; mention if text is illegible or measurements are absent"
    }}
  ],
  "overall_observations": "1-2 paragraph summary of the plan set as a whole",
  "compliance_red_flags": [
    "High-level potential compliance issues spanning the full set"
  ],
  "missing_required_sheets": [
    "Sheets that you would expect but don't see (e.g., 'No structural drawing for G+3 project')"
  ]
}}

IMPORTANT:
- Quote measurements EXACTLY as drawn. Do not convert units unless asked.
- If a measurement is not visible or unclear, write "not visible" rather than guessing.
- Do NOT fabricate sheet numbers, dimensions, or compliance flags.
- It is acceptable to have empty arrays or "not visible" values where you genuinely cannot tell.
"""


def run_plan_vision_agent(
    plan_pdf_bytes: bytes,
    max_pages: int = 8,
    dpi: int = 150,
    detail: str = "auto",
) -> Dict[str, Any]:
    """Run the vision agent over a plan PDF.

    Args:
        plan_pdf_bytes: The plan PDF as raw bytes (e.g., from UploadFile.read()).
        max_pages: Cap on pages sent to vision API (cost control).
        dpi: Render resolution (150 = readable + cheap; 200+ for fine detail).
        detail: "auto" | "low" | "high" — passed to the vision API per image.

    Returns:
        Parsed JSON dict with sheet_manifest and compliance flags.
        On parse failure, returns {"error": ..., "raw_response": ...}.
    """
    if not plan_pdf_bytes:
        return {"error": "Empty plan PDF bytes"}

    try:
        total_pages = get_pdf_page_count(plan_pdf_bytes)
    except Exception as e:  # noqa: BLE001
        return {"error": f"Could not open plan PDF: {e}"}

    pages_to_render = min(total_pages, max_pages)

    try:
        image_urls = pdf_to_base64_images(
            plan_pdf_bytes,
            dpi=dpi,
            max_pages=max_pages,
            max_dimension=2048,
            use_jpeg=True,
            jpeg_quality=85,
        )
    except Exception as e:  # noqa: BLE001
        return {"error": f"Failed to render plan PDF to images: {e}"}

    if not image_urls:
        return {"error": "No pages rendered from plan PDF"}

    skills_text = load_skills(VISION_SKILLS)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(skills=skills_text)

    user_text = (
        f"Analyzing {len(image_urls)} plan sheet(s) from a Bengaluru "
        f"residential project (total pages in PDF: {total_pages}; "
        f"rendered: {pages_to_render}). "
        "Produce the structured JSON sheet manifest and compliance "
        "observations per the schema in the system prompt."
    )

    try:
        raw = call_vision(
            system_prompt=system_prompt,
            user_text=user_text,
            image_data_urls=image_urls,
            max_completion_tokens=4000,
            detail=detail,
            response_format={"type": "json_object"},
        )
    except Exception as e:  # noqa: BLE001
        return {
            "error": f"Vision API call failed: {e}",
            "hint": (
                "Make sure your AZURE_OPENAI_VISION_DEPLOYMENT_NAME (or main "
                "deployment) is a vision-capable model such as gpt-4o, "
                "gpt-4o-mini, or gpt-4-turbo with vision."
            ),
        }

    try:
        result = json.loads(raw)
        # Add metadata so the corrections agent knows what it's looking at
        result["_meta"] = {
            "total_pages_in_pdf": total_pages,
            "pages_rendered": pages_to_render,
            "dpi": dpi,
            "detail": detail,
        }
        return result
    except json.JSONDecodeError:
        return {
            "error": "Vision response was not valid JSON",
            "raw_response": raw,
        }


def vision_summary_to_text(vision_result: Dict[str, Any]) -> str:
    """Flatten a vision-agent result into a compact text summary for the
    text-only corrections agent to consume.
    """
    if "error" in vision_result:
        return f"[Vision agent error: {vision_result['error']}]"

    lines = []
    obs = vision_result.get("overall_observations")
    if obs:
        lines.append("OVERALL OBSERVATIONS:")
        lines.append(obs)
        lines.append("")

    sheets = vision_result.get("sheet_manifest", [])
    if sheets:
        lines.append("SHEET MANIFEST:")
        for s in sheets:
            sn = s.get("sheet_number", "?")
            st = s.get("sheet_title", "")
            lines.append(f"- Sheet {sn} ({st})")
            dtypes = s.get("drawing_types") or []
            if dtypes:
                lines.append(f"    Drawings: {', '.join(dtypes)}")
            km = s.get("key_measurements") or {}
            for k, v in km.items():
                lines.append(f"    {k}: {v}")
            for flag in s.get("compliance_flags") or []:
                lines.append(f"    ⚠ {flag}")
            note = s.get("notes")
            if note:
                lines.append(f"    Notes: {note}")
        lines.append("")

    flags = vision_result.get("compliance_red_flags") or []
    if flags:
        lines.append("OVERALL COMPLIANCE RED FLAGS:")
        for f in flags:
            lines.append(f"- {f}")
        lines.append("")

    missing = vision_result.get("missing_required_sheets") or []
    if missing:
        lines.append("MISSING / EXPECTED SHEETS:")
        for m in missing:
            lines.append(f"- {m}")

    return "\n".join(lines) if lines else "[Vision agent returned no observations]"
