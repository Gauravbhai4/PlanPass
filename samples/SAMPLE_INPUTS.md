# Permit Setu — Sample Inputs

Three ready-to-paste test cases for **Flow 2 (Pre-Submission Checklist)** and instructions for **Flow 1 (Corrections Letter Interpreter)** using the included sample PDFs.

---

## Flow 2 — Pre-Submission Checklist

Open the UI at `http://127.0.0.1:8000`, click the "Flow 2 — Pre-Submission Checklist" tab, and paste these values into the form.

---

### Test Case 1 — "Compliant 30x40 Stilt+G+2 in Whitefield"

A typical small-plot Bengaluru residential project that should pass with green flags.

| Field | Value |
|---|---|
| Plot dimensions | `30x40` |
| Plot area (sq ft) | `1200` |
| Land use zone | `R (Residential single-family)` |
| Khata type | `A-Khata (with E-Khata)` |
| Road width facing plot (ft) | `30` |
| Construction type | `New construction` |
| Proposed floors | `G+2` |
| Proposed built-up area (sq ft) | `2000` |
| Number of dwelling units | `1` |
| Location | `Whitefield, Bengaluru` |
| Special conditions | `None` |

**Expected output:** submission_track = "Nambike Nakshe", eligible_to_submit = true. Should call out the FAR check (2000 / 1200 = 1.67 within 1.75 limit), front setback of 0.75m, EV parking requirement, RWH provision needed.

---

### Test Case 2 — "B-Khata Blocker"

A common real-world scenario: owner has B-Khata and doesn't realize their plan can't even be submitted.

| Field | Value |
|---|---|
| Plot dimensions | `30x50` |
| Plot area (sq ft) | `1500` |
| Land use zone | `R (Residential single-family)` |
| Khata type | `B-Khata` |
| Road width facing plot (ft) | `25` |
| Construction type | `New construction` |
| Proposed floors | `G+3` |
| Proposed built-up area (sq ft) | `3000` |
| Number of dwelling units | `1` |
| Location | `HSR Layout, Bengaluru` |
| Special conditions | `None` |

**Expected output:** eligible_to_submit = **false**. Top blocker should be "B-Khata not eligible — convert to A-Khata first". Should mention the 100-day conversion drive that started Nov 1, 2025.

---

### Test Case 3 — "Marginal Case: Narrow Road + Stilt+4"

Tests whether the agent correctly applies the new GBA 2026 road-width relaxation.

| Field | Value |
|---|---|
| Plot dimensions | `40x60` |
| Plot area (sq ft) | `2400` |
| Land use zone | `RM-1 (Residential mixed low density)` |
| Khata type | `A-Khata (with E-Khata)` |
| Road width facing plot (ft) | `14` |
| Construction type | `New construction` |
| Proposed floors | `Stilt+4` |
| Proposed built-up area (sq ft) | `5000` |
| Number of dwelling units | `4` |
| Location | `Indiranagar, Bengaluru` |
| Special conditions | `Adjacent to existing residential building on east side` |

**Expected output:** Should call out that the 14ft road is in the new 12-15ft relaxation range (post-Jan 2026), so construction is permitted but with height restrictions. May flag Stilt+4 as marginal at this road width. Should mention OC is required (built-up > 1,200 sq ft). Should require Fire NOC (G+3 and above) and structural engineer NOC.

---

## Flow 1 — Corrections Letter Interpreter

Open the "Flow 1 — Corrections Letter Interpreter" tab and upload the sample PDFs.

### Files to upload

Both included in the `samples/` folder:

1. **`Sample_BBMP_Corrections_Letter.pdf`** — a realistic 2-page BBMP corrections letter with 7 numbered objections (setback violation, FAR calculation issue, missing EV parking, missing tax receipt, missing RWH pit, missing structural certificate, illegible empanelment number).

2. **`Sample_Plan_Sheets.pdf`** — a 3-page mock plan set:
   - Sheet A1: Cover Sheet + Site Plan (with FAR table, parking schedule, and the **intentional 0.6 m front setback** the corrections letter complains about)
   - Sheet A2: Ground Floor Plan (stilt parking layout)
   - Sheet A3: North Elevation (3D massing)

### Form fields to fill

| Field | Value |
|---|---|
| Corrections letter PDF | (upload) `samples/Sample_BBMP_Corrections_Letter.pdf` |
| Plan PDF (optional - will be read with vision) | (upload) `samples/Sample_Plan_Sheets.pdf` |
| Plot dimensions | `30x40` |
| Land use zone | `R (Residential)` |
| Khata type | `A-Khata` |
| Location | `Whitefield, Bengaluru` |
| Use vision (gpt-4o) to read plan PDF | (checked - default) |
| Max plan pages to read | `8` |
| Vision detail level | `auto` |

Click **"Generate Response Package"**. Takes 60-120 seconds.

### What the agent should return

A JSON object with:

- **`plan_vision_result`** — sheet manifest from gpt-5.2 vision pass:
  - Sheet A1: should extract plot dims (30 ft x 40 ft), setbacks (0.6m front — flagged!), FAR (1.75), parking (1 car + 2 two-wheeler, no EV), height G+2.
  - Sheet A2: stilt parking layout, foyer, stair.
  - Sheet A3: elevation with 8.5m total height.
  - `compliance_red_flags`: front setback below 0.75m, no EV charging, no RWH pit visible.

- **`corrections_response`** — full response package:
  - `case_summary` — 1-2 paragraphs.
  - `objections[]` — each of the 7 objections categorized (auto-fixable / needs engineer / documentation).
  - `response_letter` — full formal letter ready to copy-paste.
  - `corrections_report` — markdown status dashboard.
  - `scope_of_work` — drafting task list by sheet.
  - `sheet_annotations` — JSON of per-sheet markup instructions (e.g., `A1: ["increase front setback to 0.75 m", "add EV charging legend to parking schedule"]`).
  - `open_questions_for_owner` — e.g., "Confirm whether the planned future G+3 conversion will use the same structural design".

---

## Tip — How to demo Flow 1 quickly without the plan PDF

If you want to skip the vision step (saves ~30 seconds and a few cents):
- Only upload the corrections letter PDF
- Untick "Use vision"

The agent still produces a full response package — just without the per-sheet extracted measurements from the plan.
