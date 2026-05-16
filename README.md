# Permit Setu

**AI-powered BBMP / GBA building plan compliance assistant for Bengaluru architects.**

Permit Setu helps licensed architects (especially those using the Nambike Nakshe self-certification track) verify residential plans against current Karnataka rules **before** submitting to the BPAS portal, and respond to BBMP corrections letters when they come back.

This is a local, runnable prototype built on Python + FastAPI + Azure OpenAI.

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- An **Azure OpenAI** resource with at least one chat-model deployment (e.g., `gpt-4o`, `gpt-4o-mini`, or `gpt-4-turbo`)
  - You'll need: endpoint URL, API key, deployment name, and API version
- 5 minutes

### 1. Clone / open this folder

```bash
cd crossbeam-india
```

### 2. Create a virtual environment and install dependencies

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI credentials

Copy `.env.example` to `.env`:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your real values:

```
AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE_NAME.openai.azure.com/
AZURE_OPENAI_API_KEY=your-real-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o            # the DEPLOYMENT name, not the model name
AZURE_OPENAI_VISION_DEPLOYMENT_NAME=           # optional - leave blank to reuse main deployment
AZURE_OPENAI_API_VERSION=2024-10-21
```

#### Where to find these in Azure

1. Go to [Azure Portal](https://portal.azure.com/) → your **Azure OpenAI** resource
2. **Keys and Endpoint** blade → copy `Endpoint` and `KEY 1`
3. **Model deployments** blade → note the **Deployment name** (this is what you set as `AZURE_OPENAI_DEPLOYMENT_NAME`)
4. API version: `2024-10-21` is a stable GA version that supports JSON-mode AND vision

#### Vision support (required for reading plan PDFs)

Flow 1 (corrections interpreter) can read your architectural plan PDFs page-by-page using Azure OpenAI vision. Your deployment must be a vision-capable model:

| Model | Vision support |
|-------|---------------|
| **gpt-4o** | Yes (recommended) |
| **gpt-4o-mini** | Yes (cheaper, slightly less accurate) |
| **gpt-4-turbo** (with vision) | Yes |
| gpt-35-turbo / gpt-4 (text-only) | No |

If your main deployment is already vision-capable, leave `AZURE_OPENAI_VISION_DEPLOYMENT_NAME` blank. If you have a separate deployment for vision (e.g., `gpt-4o-mini` for vision and `gpt-4o` for text), set it explicitly.

If you don't have a vision-capable deployment, untick **"Use vision (gpt-4o) to read plan PDF"** in the UI and the system falls back to text-only extraction.

### 4. Run the server

```bash
python main.py
```

You should see:

```
============================================================
Permit Setu: BBMP/GBA Building Plan Compliance Assistant
============================================================
Starting server at http://127.0.0.1:8000
...
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 5. Open the UI

Open your browser to **http://127.0.0.1:8000**

The page shows two tabs:

- **Flow 2 — Pre-Submission Checklist**: enter plot details and get a complete BBMP/GBA compliance checklist
- **Flow 1 — Corrections Letter Interpreter**: upload a BBMP corrections letter PDF and get a full response package back

A sample corrections letter text is available at `samples/sample_corrections_letter.txt` — convert it to PDF (any quick TXT→PDF tool) to demo Flow 1.

---

## Project Structure

```
crossbeam-india/
├── main.py                       # FastAPI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Azure OpenAI config template
├── .gitignore
├── README.md
├── app/
│   ├── config.py                 # Loads env vars
│   ├── azure_client.py           # Azure OpenAI client wrapper (text + vision)
│   ├── pdf_utils.py              # PDF text extraction + PDF->image rendering
│   ├── agents/
│   │   ├── checklist_agent.py    # Flow 2 logic
│   │   ├── corrections_agent.py  # Flow 1 logic
│   │   └── plan_vision_agent.py  # Flow 1 vision: reads plan sheets as images
│   └── skills/
│       ├── skill_loader.py
│       └── files/                # The "skills layer" - Karnataka rules as markdown
│           ├── zonal-regulations-2026.md
│           ├── setback-table.md
│           ├── far-table.md
│           ├── parking-norms.md
│           ├── khata-rules.md
│           ├── nambike-nakshe.md
│           ├── ktcp-act-1961.md
│           ├── decision-tree-router.md
│           └── corrections-workflow.md
├── static/
│   ├── index.html                # UI page
│   ├── style.css
│   └── app.js
└── samples/
    └── sample_corrections_letter.txt
```

---

## How It Works

### Skills-First Design

The agent's knowledge of Karnataka building rules lives in `app/skills/files/` as plain markdown. These files encode the January 2026 amended Zonal Regulations, the KTCP Act 1961, setback/FAR/parking tables, khata rules, and the Nambike Nakshe self-certification process.

When a flow runs, the relevant skills are concatenated and passed to Azure OpenAI as the **system prompt**. The model reasons over them to produce structured JSON outputs.

This means: to update for a new BBMP notification, you only edit the markdown file — no code changes needed.

### Flow 2 — Pre-Submission Checklist

`app/agents/checklist_agent.py`

The architect enters plot details (size, zone, khata type, road width, etc.). The agent loads all rule skills, applies the decision-tree router, and returns a JSON checklist covering:

- Submission track (Nambike Nakshe vs. Standard Review)
- Eligibility blockers (e.g., B-Khata → cannot submit)
- Applicable setbacks, FAR, height, parking
- Documents and NOCs required
- Project-specific "gotchas"
- Estimated timeline and fees
- Ordered next-actions

### Flow 1 — Corrections Letter Interpreter (with Vision)

`app/agents/corrections_agent.py` + `app/agents/plan_vision_agent.py`

The architect uploads (a) the BBMP corrections-letter PDF and optionally (b) the plan PDF.

**Pipeline:**

1. **Corrections letter** → `pypdf` extracts text (corrections letters are typed and text-extractable).
2. **Plan PDF** → if uploaded with vision enabled, `PyMuPDF` renders each page to a JPEG at 150 DPI, downsized to ≤2048px on the longest edge, base64-encoded. Each image is sent to the Azure OpenAI vision deployment (`gpt-4o`) with a system prompt instructing the model to act as a senior BBMP plan reviewer. The model returns a structured JSON **sheet manifest** with extracted measurements (setbacks, FAR, parking) and compliance flags it can see.
3. The vision summary + corrections text + Karnataka rule skills are all fed into the **corrections agent**, which parses each objection, categorizes it (auto-fixable / needs homeowner input / etc.), cross-references the cited rule, and produces four artifacts:

   - **Response letter** in BBMP format, ready to copy-paste
   - **Corrections report** — markdown status dashboard
   - **Scope of work** — drafting task list for the CAD team
   - **Sheet annotations** — JSON of per-sheet markup instructions
   - Plus open questions the architect needs the homeowner to answer

**Cost control:** the UI exposes `max_plan_pages` (default 8) and `vision_detail` (`auto`/`low`/`high`). A typical 15-page Bengaluru residential plan capped at 8 pages with `detail=auto` costs roughly **$0.10-0.30** per case using gpt-4o pricing.

**Vision off:** untick the "Use vision" checkbox and the system falls back to text-only extraction from the plan PDF (which usually returns very little because plan PDFs are mostly graphics).

---

## Production Notes

This is a **local prototype** — for real deployment you'd want:

- **Data residency**: host in Azure South India (Central / South) for DPDP Act 2023 compliance
- **Auth**: add an architect login layer (Microsoft Entra ID works natively with Azure OpenAI)
- **Plan-image vision**: extend `pdf_utils.py` to use pdf-to-image + Azure OpenAI vision-capable deployments (e.g., `gpt-4o`) for reading architectural drawings, not just text
- **Persistence**: add Postgres / Cosmos DB to save sessions and let architects revisit past audits
- **Audit trail**: log every agent decision with full prompt + response for liability defense
- **BPAS integration**: scrape or API-integrate `bpas.bbmpgov.in` to pull live application status

---

## Troubleshooting

### "Missing or unset environment variables"

You haven't created `.env` (only `.env.example`), or you left placeholder values. Open `.env` and fill in real Azure OpenAI credentials.

### "404 Resource not found" from Azure OpenAI

Your `AZURE_OPENAI_DEPLOYMENT_NAME` doesn't match an actual deployment in your Azure resource. Go to Azure OpenAI Studio → Deployments → copy the exact name shown there.

### "InvalidRequestError: 'response_format' of type 'json_object' is not supported"

Upgrade `AZURE_OPENAI_API_VERSION` to `2024-08-01-preview` or later. JSON-mode requires a recent API version.

### "InvalidRequestError: image_url is not supported by this model"

Your deployment isn't vision-capable. Either:
- Deploy `gpt-4o` or `gpt-4o-mini` in Azure OpenAI Studio and set `AZURE_OPENAI_VISION_DEPLOYMENT_NAME` to it, or
- Untick "Use vision" in the Flow 1 form to fall back to text-only extraction.

### Plan PDF gives no useful information even with vision

- Confirm the PDF is not encrypted/password-protected
- Check the rendering DPI — at 150 DPI fine dimension text on a 30x40 plan can be hard to read; try `vision_detail=high` or modify `dpi=200` in `app/agents/plan_vision_agent.py`
- Plans scanned at low quality (under 200 DPI scanner setting) will struggle — get the architect to share the native CAD-exported PDF, not a scan

### Server starts but / page is blank

Check the browser console. The badge in the top right will say "Config issue" if Azure isn't reachable.

### Long response times (60-90 sec)

This is normal for the corrections flow — the model is reading the full rules + corrections letter and writing a long structured response. Use a faster deployment (`gpt-4o-mini`) for snappier responses during development.

---

## License

This is a prototype derived from the original CrossBeam (California ADU permit assistant) architecture. Adapt freely for your purposes.
