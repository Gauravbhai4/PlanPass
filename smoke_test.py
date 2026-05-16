"""Permit Setu smoke test.

Run this after `pip install -r requirements.txt` to verify your install:
    python smoke_test.py

It exercises:
  - All module imports (syntax + dependency check)
  - Skills directory load (no Azure calls)
  - PDF -> image rendering (no Azure calls)
It does NOT call Azure OpenAI, so it's safe to run before configuring .env.
"""
import sys
import io
from pathlib import Path


def section(label):
    print()
    print("=" * 60)
    print(label)
    print("=" * 60)


def check(label, fn):
    try:
        fn()
        print(f"  [OK]  {label}")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"  [FAIL] {label}: {type(e).__name__}: {e}")
        return False


def main() -> int:
    failures = 0

    section("1. Module imports")
    # Stub the env so config.validate() can be called later if needed
    import os
    os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://stub.openai.azure.com/")
    os.environ.setdefault("AZURE_OPENAI_API_KEY", "stub-key-for-smoke-test")

    def _imp():
        global pdf_utils, azure_client, skill_loader
        global checklist_agent, corrections_agent, plan_vision_agent, main_module
        from app import config  # noqa: F401
        from app import pdf_utils  # noqa: F401
        from app import azure_client  # noqa: F401
        from app.skills import skill_loader  # noqa: F401
        from app.agents import checklist_agent  # noqa: F401
        from app.agents import corrections_agent  # noqa: F401
        from app.agents import plan_vision_agent  # noqa: F401
        import main as main_module  # noqa: F401
    if not check("Import all Permit Setu modules", _imp):
        failures += 1

    section("2. Skills layer")
    from app.skills.skill_loader import list_available_skills, load_all_skills, load_skills

    def _skills_listed():
        skills = list_available_skills()
        assert len(skills) >= 8, f"Expected >=8 skill files, found {len(skills)}: {skills}"
        print(f"        ({len(skills)} skill files: {', '.join(skills)})")
    if not check("List available skills", _skills_listed):
        failures += 1

    def _skills_loaded():
        text = load_all_skills()
        assert len(text) > 5000, f"Expected substantial skill content, got {len(text)} chars"
        print(f"        ({len(text):,} chars of Karnataka rule reference)")
    if not check("Concatenate all skills", _skills_loaded):
        failures += 1

    section("3. PDF -> image rendering (no Azure call)")
    try:
        import fitz  # PyMuPDF
        from PIL import Image  # noqa: F401
        deps_ok = True
    except ImportError as e:
        print(f"  [SKIP] PyMuPDF or Pillow not installed: {e}")
        print("         Run: pip install -r requirements.txt")
        deps_ok = False

    if deps_ok:
        # Create a tiny in-memory PDF using PyMuPDF
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # A4
        page.insert_text(
            (50, 100),
            "Permit Setu smoke test plan sheet\nSheet A1 - Site Plan\nFront setback: 0.75m",
            fontsize=12,
        )
        pdf_bytes = doc.tobytes()
        doc.close()
        print(f"        (built a {len(pdf_bytes)}-byte test PDF)")

        from app.pdf_utils import (
            extract_text_from_bytes,
            pdf_to_images,
            pdf_to_base64_images,
            get_pdf_page_count,
        )

        def _text():
            text = extract_text_from_bytes(pdf_bytes)
            assert "smoke test" in text.lower(), f"Text extraction failed: {text!r}"
        if not check("Text extraction (pypdf)", _text):
            failures += 1

        def _page_count():
            n = get_pdf_page_count(pdf_bytes)
            assert n == 1, f"Expected 1 page, got {n}"
        if not check("PDF page count (PyMuPDF)", _page_count):
            failures += 1

        def _images():
            imgs = pdf_to_images(pdf_bytes, dpi=100, max_pages=1)
            assert len(imgs) == 1, f"Expected 1 image, got {len(imgs)}"
            assert imgs[0].size[0] > 0 and imgs[0].size[1] > 0
            print(f"        (rendered image size: {imgs[0].size})")
        if not check("PDF -> PIL Image (PyMuPDF)", _images):
            failures += 1

        def _b64():
            urls = pdf_to_base64_images(pdf_bytes, dpi=100, max_pages=1)
            assert len(urls) == 1
            assert urls[0].startswith("data:image/jpeg;base64,"), urls[0][:50]
            print(f"        (data URL length: {len(urls[0]):,} chars)")
        if not check("PDF -> base64 data URL", _b64):
            failures += 1

    section("4. FastAPI app routes")
    try:
        import main as m

        def _routes():
            paths = [r.path for r in m.app.routes if hasattr(r, "path")]
            required = ["/api/health", "/api/checklist", "/api/corrections", "/"]
            for r in required:
                assert r in paths, f"Missing route: {r}"
            print(f"        (routes: {', '.join(sorted(set(paths)))})")
        if not check("All required routes registered", _routes):
            failures += 1
    except Exception as e:  # noqa: BLE001
        print(f"  [FAIL] FastAPI import: {e}")
        failures += 1

    section("Summary")
    if failures == 0:
        print("  ALL CHECKS PASSED. You can now configure .env and run: python main.py")
        return 0
    else:
        print(f"  {failures} check(s) failed. See messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
