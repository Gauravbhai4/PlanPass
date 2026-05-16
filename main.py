"""Permit Setu FastAPI entry point.

Run locally with:
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
or simply:
    python main.py
"""
# v0.2.0 - vision-enabled corrections flow
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from app.config import settings
from app.agents.checklist_agent import run_checklist_agent
from app.agents.corrections_agent import run_corrections_agent
from app.agents.plan_vision_agent import (
    run_plan_vision_agent,
    vision_summary_to_text,
)
from app.pdf_utils import extract_text_from_bytes


app = FastAPI(
    title="Permit Setu",
    description="Your bridge to BBMP / GBA approval — AI-powered building plan compliance assistant",
    version="0.2.0",
)


# ----- Models -----

class ChecklistRequest(BaseModel):
    plot_dimensions: str = "30x40"
    plot_area_sqft: str = "1200"
    zone: str = "R (Residential)"
    khata_type: str = "A-Khata"
    road_width_ft: str = "30"
    construction_type: str = "New construction"
    proposed_floors: str = "G+2"
    built_up_area_sqft: str = "2000"
    num_units: str = "1"
    location: str = "Whitefield, Bengaluru"
    special_conditions: str = "None"


# ----- API Routes -----

@app.get("/api/health")
async def health():
    """Health check that also reports config status."""
    try:
        settings.validate()
        config_ok = True
        config_msg = "Azure OpenAI configured"
    except ValueError as e:
        config_ok = False
        config_msg = str(e)

    return {
        "status": "ok",
        "config_ok": config_ok,
        "config_message": config_msg,
        "deployment": settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        "vision_deployment": (
            settings.AZURE_OPENAI_VISION_DEPLOYMENT_NAME
            or settings.AZURE_OPENAI_DEPLOYMENT_NAME
        ),
        "api_version": settings.AZURE_OPENAI_API_VERSION,
    }


@app.post("/api/checklist")
async def checklist_endpoint(req: ChecklistRequest):
    """Flow 2: Generate a pre-submission compliance checklist."""
    try:
        result = run_checklist_agent(req.model_dump())
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")


@app.post("/api/corrections")
async def corrections_endpoint(
    corrections_pdf: UploadFile = File(...),
    plan_pdf: Optional[UploadFile] = File(None),
    plot_dimensions: str = Form("30x40"),
    zone: str = Form("R (Residential)"),
    khata_type: str = Form("A-Khata"),
    location: str = Form("Bengaluru"),
    use_vision: bool = Form(True),
    max_plan_pages: int = Form(8),
    vision_detail: str = Form("auto"),
):
    """Flow 1: Interpret a BBMP corrections letter and produce a response package.

    If a plan PDF is uploaded, it is read via vision (gpt-4o) to extract a
    structured sheet manifest with measurements and compliance flags. That
    structured summary is fed into the corrections agent alongside the
    extracted corrections-letter text.

    Form fields:
        - corrections_pdf: REQUIRED, the BBMP corrections letter PDF
        - plan_pdf: OPTIONAL, the submitted plan PDF
        - use_vision: if True (default) and plan_pdf provided, run the vision agent
        - max_plan_pages: cap on plan pages sent to vision API (cost control)
        - vision_detail: "auto" | "low" | "high"
        - plot_dimensions, zone, khata_type, location: project context
    """
    if not corrections_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="corrections_pdf must be a .pdf file"
        )

    # Extract corrections letter text
    corrections_bytes = await corrections_pdf.read()
    try:
        corrections_text = extract_text_from_bytes(corrections_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract text from corrections PDF: {e}",
        )

    plan_summary = None
    vision_result = None
    if plan_pdf is not None and plan_pdf.filename:
        plan_bytes = await plan_pdf.read()

        if use_vision:
            # Run the vision agent over the plan PDF first
            try:
                vision_result = run_plan_vision_agent(
                    plan_pdf_bytes=plan_bytes,
                    max_pages=max_plan_pages,
                    detail=vision_detail,
                )
            except Exception as e:  # noqa: BLE001
                vision_result = {"error": f"Vision agent crashed: {e}"}

            if vision_result and "error" not in vision_result:
                plan_summary = vision_summary_to_text(vision_result)
            else:
                # Fall back to text extraction if vision failed
                try:
                    plan_summary = extract_text_from_bytes(plan_bytes)
                except Exception as e:  # noqa: BLE001
                    plan_summary = f"[Could not extract plan PDF text: {e}]"
                if vision_result and "error" in vision_result:
                    plan_summary = (
                        f"[Vision agent error: {vision_result['error']}]\n\n"
                        "Falling back to raw text extraction:\n\n"
                        + (plan_summary or "")
                    )
        else:
            # Vision disabled — text-only fallback
            try:
                plan_summary = extract_text_from_bytes(plan_bytes)
            except Exception as e:  # noqa: BLE001
                plan_summary = f"[Could not extract plan PDF text: {e}]"

        if plan_summary and len(plan_summary) > 30000:
            plan_summary = plan_summary[:30000] + "\n...[truncated]"

    project_context = {
        "plot_dimensions": plot_dimensions,
        "zone": zone,
        "khata_type": khata_type,
        "location": location,
    }

    try:
        agent_result = run_corrections_agent(
            corrections_text=corrections_text,
            plan_summary=plan_summary,
            project_context=project_context,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    # Include the raw vision result so the UI can show it
    response = {"corrections_response": agent_result}
    if vision_result is not None:
        response["plan_vision_result"] = vision_result

    return JSONResponse(content=response)


# ----- Static / UI -----

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    """Serve the main UI page."""
    return FileResponse(str(STATIC_DIR / "index.html"))


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Permit Setu — Your bridge to BBMP / GBA approval")
    print("=" * 60)
    print(f"Starting server at http://{settings.APP_HOST}:{settings.APP_PORT}")
    print(f"Azure OpenAI text deployment:   {settings.AZURE_OPENAI_DEPLOYMENT_NAME}")
    print(
        f"Azure OpenAI vision deployment: "
        f"{settings.AZURE_OPENAI_VISION_DEPLOYMENT_NAME or settings.AZURE_OPENAI_DEPLOYMENT_NAME}"
    )
    print(f"Azure OpenAI API version:       {settings.AZURE_OPENAI_API_VERSION}")
    print("=" * 60)
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
