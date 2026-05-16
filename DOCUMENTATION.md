# Permit Setu — Complete Documentation

> An AI assistant that helps Bengaluru architects get building plan approvals on the first try.

---

## Table of Contents

- [Part 1 — In Plain English](#part-1--in-plain-english)
  - [The Problem](#the-problem)
  - [What Permit Setu Does](#what-crossbeam-india-does)
  - [Who This Is For](#who-this-is-for)
  - [What Makes It Different](#what-makes-it-different)
- [Part 2 — How It Works (User's Perspective)](#part-2--how-it-works-users-perspective)
  - [Flow 2 — Pre-Submission Checklist](#flow-2--pre-submission-checklist)
  - [Flow 1 — Corrections Letter Interpreter](#flow-1--corrections-letter-interpreter)
- [Part 3 — Tech Stack Explained](#part-3--tech-stack-explained)
  - [Programming Language and Framework](#programming-language-and-framework)
  - [The AI Brain — Azure OpenAI](#the-ai-brain--azure-openai)
  - [Reading PDFs](#reading-pdfs)
  - [Frontend](#frontend)
  - [Configuration](#configuration)
- [Part 4 — Architecture and the Skills Layer](#part-4--architecture-and-the-skills-layer)
  - [Big-Picture Diagram](#big-picture-diagram)
  - [The Skills Layer](#the-skills-layer)
  - [The Vision Pipeline](#the-vision-pipeline)
  - [Why Two Agents in Flow 1](#why-two-agents-in-flow-1)
- [Part 5 — Setup and Troubleshooting](#part-5--setup-and-troubleshooting)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration-1)
  - [Running](#running)
  - [Common Errors](#common-errors)
- [Part 6 — Glossary and FAQ](#part-6--glossary-and-faq)
  - [Glossary](#glossary)
  - [Frequently Asked Questions](#frequently-asked-questions)

---

# Part 1 — In Plain English

## The Problem

Imagine you're a homeowner in Bengaluru. You want to build a small house on a 30 ft × 40 ft plot in Whitefield. You hire an architect. The architect draws up the plans, you sign them, and they get submitted to BBMP (the city's building authority — recently restructured as the Greater Bengaluru Authority, or GBA).

Three weeks later, the city sends back a letter. Not an approval. A "corrections letter" with seven numbered objections.

Some examples of what the letter might say:

- *"Front setback shown is 0.6 m. Minimum required is 0.75 m as per the amended Zonal Regulations dated 5-6 January 2026."*
- *"FAR calculation does not include the staircase core area."*
- *"EV charging infrastructure not indicated in the parking layout."*
- *"Architect's empanelment certificate number is not legible on the title block."*

Your architect now has to:

1. **Understand each objection** — every rule cited, every section reference
2. **Look up the actual code** — KTCP Act 1961, Section 17, Zonal Regulations 2026, BBMP Bye-Laws…
3. **Decide who fixes what** — drafting team, structural engineer, the owner (you)
4. **Redraw the affected sheets** — typically 3-5 plan sheets need updating
5. **Write a formal response letter** in BBMP's expected format
6. **Resubmit** and hope nothing else gets flagged this round

This back-and-forth usually takes **3 to 4 weeks per round**. And it happens to **35-40% of first-time submissions** in Bengaluru. A single setback error can cost ₹12 lakh in reconstruction if the building was already started.

### Why this happens

- The rules are voluminous: a small residential project touches at least 6 different regulatory documents.
- The rules keep changing: Karnataka rolled out major zonal-regulation updates on **5 January 2026**. The Greater Bengaluru Authority replaced parts of BBMP under the 2024 governance act. E-Khata became mandatory in July 2025.
- Each plan checker interprets rules slightly differently across BBMP's 8 zones.
- Most architects are running 5-10 projects simultaneously. They don't have time to read every new notification.

This is not a problem AI is going to solve overnight. But AI can absolutely help an architect get to a clean first submission, and respond to corrections in hours instead of days.

## What Permit Setu Does

Permit Setu is a small piece of software that runs on your laptop. It has two main jobs.

### Job 1 — Pre-Submission Checklist

You enter your project details into a form:

- Plot size (e.g., 30 ft × 40 ft)
- Zone (residential, mixed-use, etc.)
- Khata type (A, B, or E)
- Road width facing the plot
- Number of floors you want to build
- Built-up area

You click "Generate Compliance Checklist." Within 30 seconds, you get back a structured report that says:

- **You're eligible to submit (or you're not — and here's why)**
- The exact setbacks required for your plot size (front, side, rear)
- Your maximum FAR and built-up area
- Parking requirements (including the new 2026 EV charging rule)
- Documents you'll need (E-Khata, ePID, latest tax receipt, etc.)
- NOCs you may need (fire, structural, RWH)
- Estimated approval timeline
- The likely "gotchas" specific to your project

Think of it like getting a 30-minute consultation with a senior architect-cum-liaison-agent, except it costs almost nothing and you get the answer in 30 seconds.

### Job 2 — Corrections Letter Interpreter

You get a corrections letter from BBMP. You upload:

- The corrections-letter PDF
- Your submitted architectural plan PDF (the actual drawings — site plan, floor plans, elevations)

You click "Generate Response Package." Within 60-120 seconds, you get back four things:

1. **A response letter**, drafted in BBMP's formal format, with each of the city's objections quoted and responded to with the correct rule citations. Ready to copy-paste.

2. **A corrections report** — an internal dashboard showing each objection, what category it falls in (easy fix, needs the owner's input, needs your structural engineer), and what action to take.

3. **A scope of work** for your drafting team — a checklist of exactly which sheets need updating and what to change on each one.

4. **Per-sheet markup instructions** — for example: *Sheet A1: increase front setback dimension to 0.75 m; add EV charging legend to parking schedule.*

Plus a list of questions the agent thinks you should ask the owner before resubmitting.

The magic ingredient here is that **the agent reads your actual plan drawings** — not just the text. It opens each sheet, extracts the visible setback dimensions, the FAR calculation table, the parking layout, the building elevation, and flags compliance issues it can see.

## Who This Is For

- **Licensed architects** running 5-50 residential projects a year in Bengaluru — especially those using the Nambike Nakshe self-certification track where the architect personally bears the rejection risk.
- **Liaison agents and permit consultants** who shepherd permits as a service.
- **Design-build firms** managing dozens of projects in parallel (BrickNBolt, YV Homes, EcoPro, Sribha Infra, etc.).
- **Software engineers and ML practitioners** who want to study an end-to-end LLM-agent project grounded in real-world regulations.
- **Government officials** evaluating how AI could speed up plan-checking on the city side.

## What Makes It Different

Three things set Permit Setu apart from a generic ChatGPT conversation:

**1. It's grounded in actual Karnataka law.** The AI doesn't make up rules. It reads from 9 carefully curated reference documents covering the KTCP Act 1961, the 2026 amended Zonal Regulations, the Nambike Nakshe scheme, FAR/setback/parking tables, and khata rules. When BBMP changes a rule, you update one markdown file — no model retraining.

**2. It reads your drawings, not just text.** Architectural PDFs are mostly graphics — dimension lines, title blocks, elevation views, FAR calculation tables. Plain text extraction misses 90% of the content. Permit Setu converts each page to a high-resolution image and uses a vision-capable AI model to read it like a human would.

**3. It runs on your machine, with your Azure account.** Your corrections letters and plan PDFs never leave your computer except as direct API calls to your own Azure OpenAI deployment. No third-party SaaS. No data sold to anyone. No subscription. Pay only what Azure charges you per call (typically ₹15-25 per checklist, ₹50-150 per corrections case).

---

# Part 2 — How It Works (User's Perspective)

Let's walk through both flows step-by-step as if you were sitting in front of the screen.

## Flow 2 — Pre-Submission Checklist

### Step 1 — Open the app

You've already installed and configured the application (covered in Part 5). You run the command `python main.py`, and your browser opens `http://127.0.0.1:8000`.

You see a dark-themed web page with two tabs at the top: "Flow 2 — Pre-Submission Checklist" and "Flow 1 — Corrections Letter Interpreter." Flow 2 is open by default.

### Step 2 — Fill in your project details

A form asks you for:

| Field | Example |
|---|---|
| Plot dimensions | 30x40 |
| Plot area in sq ft | 1200 |
| Land use zone | R (Residential single-family) |
| Khata type | A-Khata (with E-Khata) |
| Road width facing plot in ft | 30 |
| Construction type | New construction |
| Proposed floors | G+2 |
| Proposed built-up area in sq ft | 2000 |
| Number of dwelling units | 1 |
| Location | Whitefield, Bengaluru |
| Special conditions | None |

All fields are pre-filled with sensible defaults so you can just click the button to see a sample run.

### Step 3 — Click "Generate Compliance Checklist"

A status bar shows *"Running compliance check (this can take 20-60 seconds)…"* The button is disabled while the request is in flight.

Behind the scenes:

1. Your browser sends the form data to `/api/checklist` on the local server.
2. The server loads 8 markdown skill files (about 22,000 characters of Karnataka rules) into memory.
3. It builds a structured prompt: *"You are a BBMP/GBA compliance expert. Here are the rules. Here is the project. Produce a JSON checklist."*
4. The prompt + your project details are sent to your Azure OpenAI deployment (e.g., gpt-5.2).
5. The model thinks for 20-40 seconds, then returns a JSON object.
6. The server parses the JSON and sends it back to your browser.
7. The browser renders each top-level key as a nicely formatted section.

### Step 4 — Read the output

You see something like:

> **SUMMARY**
> Your 30x40 ft plot in Whitefield qualifies for the Nambike Nakshe (self-certification) track under the amended 2026 Zonal Regulations. With G+2 construction and 2,000 sq ft built-up, you're within the 1.75 FAR limit. Key risks: ensure front setback is 0.75 m minimum, include EV charging conduit in parking design, attach latest E-Khata.
>
> **SUBMISSION TRACK**
> Nambike Nakshe
>
> **ELIGIBILITY CHECK**
> eligible_to_submit: true
> blockers: (none)
>
> **APPLICABLE RULES**
> - Front setback: 0.75 m
> - Side setback: 0.6 m (either side, sites ≤ 600 sq ft); for 1200 sq ft, 0.9 m each
> - Rear setback: 1.5 m
> - Max FAR: 1.75
> - Max height: G+2 standard / G+3 with FAR
> - Parking: 1 car + 2 two-wheeler minimum
> - EV parking: yes (20% of total spaces must have EV-charging readiness)
> - OC required: No (built-up ≤ 1,200 sq ft exemption applies)
>
> **DOCUMENTS REQUIRED**
> - E-Khata + ePID
> - Latest property tax receipt (FY 2025-26)
> - Plot survey sketch
> - Architectural drawings (A1-A8)
> - Architect's self-certification under Nambike Nakshe
>
> **GOTCHAS**
> - Stilt parking is recommended — it doesn't count toward FAR
> - The 0.6 m setback only applies to plots ≤ 600 sq ft; your 1200 sq ft plot needs 0.9 m sides
> - EV charging is new in 2026 — many architects forget this
>
> **ESTIMATED TIMELINE: 30-45 days**
> **ESTIMATED FEES: ₹35,000-₹50,000 (BBMP scrutiny + betterment)**
>
> **NEXT ACTIONS**
> 1. Confirm e-khata is in owner's name and active
> 2. Update parking schedule to include EV charging legend
> 3. Verify front setback is 0.75 m on Sheet A1
> 4. Prepare structural NOC if G+3 conversion is planned
> 5. Submit via bpas.bbmpgov.in under Nambike Nakshe track

You copy the relevant parts into your project documentation. Time elapsed: less than a minute.

### Step 5 — Try variations

If you change the khata to "B-Khata" and re-submit, the output flips: `eligible_to_submit: false`, with the top blocker being *"Cannot submit — B-Khata is not eligible for building plan approval. Convert to A-Khata first via the 100-day conversion drive that began November 2025."*

If you change the road width to 14 ft, the output adds the new GBA 2026 road-width relaxation note (12-15 ft minimum is now permitted, where the old rule was 30 ft).

The agent reasons over the rules — it doesn't just pattern-match.

## Flow 1 — Corrections Letter Interpreter

### Step 1 — Switch tabs

Click "Flow 1 — Corrections Letter Interpreter" at the top.

### Step 2 — Upload your files

Two file pickers:

- **Corrections letter PDF (required)** — the letter from BBMP/GBA listing the objections.
- **Plan PDF (optional)** — the architectural drawings you submitted. If you upload this, the agent will read each plan sheet with vision.

A checkbox **"Use vision (gpt-4o) to read plan PDF"** is on by default. Two cost-control fields appear below it:

- **Max plan pages to read** (default 8) — caps how many pages get sent to the vision API.
- **Vision detail level** (default "auto") — controls how carefully the model looks at each image.

Plus the same project-context fields (plot size, zone, etc.) so the agent knows what kind of project it's responding about.

### Step 3 — Click "Generate Response Package"

Status: *"Reading PDFs (vision-mode if plan attached) and generating response… this can take 60-120 seconds."*

What happens behind the scenes is more involved than Flow 2:

1. The corrections letter is converted to text using `pypdf` (a text-extraction library). Corrections letters are typed, so this works perfectly.
2. The plan PDF is converted to images using `PyMuPDF` — each page is rendered at 150 DPI, downscaled to a maximum of 2048 pixels on the longest edge, and JPEG-encoded.
3. Each image is base64-encoded (a way to package binary data as text) and sent to Azure OpenAI's vision API along with a system prompt instructing the model to act as a senior plan reviewer.
4. The vision model returns a JSON "sheet manifest" — for each plan sheet, what's drawn on it, what measurements are visible, and what compliance issues it spotted.
5. This sheet manifest, plus the corrections-letter text, plus the relevant Karnataka rule skills, get fed into a second AI call — the "corrections agent."
6. The corrections agent produces the four-part response package.
7. Both results (the sheet manifest AND the response package) are sent back to your browser.

### Step 4 — Review the output

You see a long rendered page with sections like:

> **PLAN VISION RESULT**
> *(The sheet-by-sheet analysis from the vision pass)*
>
> Sheet A1 — Cover Sheet + Site Plan
> - Plot dimensions: 30 ft × 40 ft
> - Front setback (visible on drawing): **0.6 m** ⚠
> - Rear setback: 1.5 m
> - Side setback (left): 0.9 m
> - Side setback (right): 0.9 m
> - FAR achieved: 1.75
> - Parking: 1 car + 2 two-wheeler, **no EV charging shown** ⚠
> - Height: G+2 (Stilt + 2 floors)
>
> Compliance flags:
> - Front setback of 0.6 m is below the 0.75 m minimum under 2026 Zonal Regulations
> - EV charging infrastructure not indicated
>
> **CORRECTIONS RESPONSE**
>
> Case summary: BBMP/GBA has raised 7 objections, primarily around setback compliance, FAR calculation methodology, EV parking provisions, and supporting documentation. Most are auto-fixable through plan revision; objection 6 (structural certificate) requires a registered structural engineer.
>
> Objection 1 — verbatim: "The front setback shown in the plan is 0.6 m, which is below the minimum prescribed setback of 0.75 m as per the amended Zonal Regulations dated 5-6 January 2026."
> - Category: code conflict
> - Cited rule: KTCP Act §19; Zonal Regulations Jan 5-6 2026
> - Analysis: The plan shows 0.6 m which is the old rule for sites ≤ 600 sq ft. For your 1,200 sq ft plot, the new minimum is 0.75 m.
> - Recommended response: "We confirm the revised plans (Sheets A1, A2, A3) now show a front setback of 0.75 m in compliance with the amended Zonal Regulations dated 5-6 January 2026."
> - Supporting docs: Revised Sheet A1 with updated setback dimension
>
> *(continues for all 7 objections)*
>
> RESPONSE LETTER (ready to copy-paste):
>
> Date: [...]
> To, The Assistant Director of Town Planning, Mahadevapura Zone, BBMP/GBA
> Subject: Response to corrections letter dated 22 April 2026 for Application No. BPA/MDP/2026/04/0782
>
> Sir/Madam, With reference to your corrections letter dated 22 April 2026 regarding the above-captioned application, we submit the following point-wise responses…
>
> *(full formal letter with numbered responses to each objection)*
>
> CORRECTIONS REPORT
> *(markdown dashboard with status of each objection, who owns it, target date)*
>
> SCOPE OF WORK
> *(drafting checklist organized by sheet — what to update on each)*
>
> SHEET ANNOTATIONS
> A1: ["increase front setback dimension to 0.75 m", "update FAR table to include staircase core", "add EV charging legend"]
> A2: ["add RWH pit on south-west corner of site plan"]
> A3: ["reprint with empanelment number clearly readable"]
>
> OPEN QUESTIONS FOR OWNER
> - "Confirm whether the planned future G+3 conversion will use the same structural design"
> - "Do you have the latest FY 2025-26 property tax receipt available?"

You can copy the response letter, hand the scope-of-work to your drafting team, and use the sheet annotations as a checklist while you revise. What might have taken 6-8 hours of careful work now takes 90 seconds plus 1-2 hours of revision.

---

# Part 3 — Tech Stack Explained

This section covers what each piece of software does, why we chose it, and how it fits in. I'll use analogies where helpful.

## Programming Language and Framework

### Python 3.10+

Python is the programming language used throughout the project. It's the most common language in the AI/ML world because:

- It has excellent libraries for working with AI models (the official Azure OpenAI SDK is written for Python first)
- It's easy to read — even if you've never coded, you can usually guess what a Python line does
- It runs anywhere — Windows, Mac, Linux

**Analogy:** Python is the "lingua franca" of AI engineering — like English in international business. You'll find Python everywhere AI gets done.

### FastAPI (version 0.115.4)

FastAPI is a "web framework" — software that makes it easy to build APIs (Application Programming Interfaces). An API is just a way for two computers to talk to each other.

In this project, FastAPI does two things:

1. It serves the web UI (the page you see in your browser).
2. It handles the requests your browser sends when you click "Generate Compliance Checklist."

**Analogy:** Think of FastAPI as the receptionist at a hotel. It listens at the front desk for incoming requests, figures out who should handle each one (the checklist agent? the corrections agent?), passes the request along, and brings back the response.

**Why FastAPI specifically?** It's modern (built for Python 3 from the ground up), fast (used by Netflix, Microsoft, and Uber), and it auto-generates documentation pages (you'll see this at `http://127.0.0.1:8000/docs`).

### Uvicorn (version 0.32.0)

Uvicorn is the "server" that runs FastAPI. FastAPI is the receptionist; Uvicorn is the building the receptionist works in. You don't usually interact with Uvicorn directly — you just run `python main.py` and Uvicorn starts up automatically.

## The AI Brain — Azure OpenAI

This is the most important piece. It's where the actual "thinking" happens.

### What is Azure OpenAI?

Microsoft Azure offers a service called **Azure OpenAI** that lets you use OpenAI's models (GPT-4o, GPT-5.2, etc.) through Microsoft's infrastructure. The benefits over using OpenAI directly:

- **Enterprise compliance** — Microsoft signs agreements that satisfy Indian DPDP Act, EU GDPR, HIPAA, etc.
- **Data residency** — your data stays in the Azure region you choose (Mumbai, Pune, Hyderabad)
- **No training on your data** — Microsoft contractually commits that your inputs aren't used to train their models
- **Unified billing** — appears on the same invoice as your other Azure services

### What model are we using?

You configured your deployment as `gpt-5.2` in eastus2. Models like GPT-5.2 (and GPT-4o, GPT-5, o1, o3) are called **Large Language Models (LLMs)** — AI systems trained on a huge fraction of the public internet that can read text, understand it, and generate new text in response.

The model knows English (and many other languages), can write in different styles, can reason through problems, and — crucially for this project — can **also look at images**.

### What is "vision"?

Some AI models (gpt-4o, gpt-4o-mini, gpt-5.2) can accept images as input, not just text. You send them a picture and they describe what's in it, read any text visible in the image, and answer questions about it.

For Permit Setu, this is essential. Architectural plan PDFs are mostly drawings. A vision-capable model can look at a site plan and tell you:

- *"This plot is 30 ft by 40 ft, oriented with the long edge running north-south"*
- *"The front setback dimension shown is 0.6 m, which is below the current minimum"*
- *"There's a parking schedule in the bottom-right that shows 1 car and 2 two-wheeler spaces, but no EV charging provision"*

A text-only model would see nothing — because that information lives in dimension lines and tables drawn as vector graphics, not as searchable text.

### How does the model know Karnataka law?

It doesn't — at least not in detail. GPT-5.2 was trained on a huge corpus of internet text. It knows broadly that Indian building permits exist. But it doesn't know the specifics of the 5 January 2026 amended Zonal Regulations.

So we **give it the rules as part of the prompt**. This is called "providing context" or "grounding." Every time we make a request, we prepend the relevant rule sections from our skills layer (see Part 4) so the model can reference them while answering.

This is far better than fine-tuning (training a custom model) because:

- Updates are instant — change a markdown file, the next request sees the new rule
- We can audit exactly what the model was told
- There's no chance of "stale" knowledge from outdated training data

### API version

You're using API version `2024-12-01-preview`. The API version controls which features are available:

- JSON-mode (forcing the model to return valid JSON) — supported on 2024-08-01-preview and later
- Vision (image inputs) — supported on 2024-04-01-preview and later
- `max_completion_tokens` (the new parameter name for reasoning models) — supported on 2024-09-01-preview and later

`2024-12-01-preview` is the most modern preview and has all features. If you have issues, falling back to `2024-10-21` (GA / stable) is the safe option.

## Reading PDFs

We use two different libraries for reading PDFs because PDFs come in two flavors.

### pypdf (version 5.1.0) — for text-based PDFs

`pypdf` is a Python library that opens a PDF and extracts the text content. It's fast, free, and works perfectly for documents that contain real text — like a corrections letter typed in MS Word and saved as PDF.

**Analogy:** pypdf is like an OCR-free copy-paste — if the original document had text, pypdf gets it back. But it can't "see" what's in a picture or a hand-drawn line.

### PyMuPDF (version 1.24.13) — for converting PDFs to images

`PyMuPDF` (also called "fitz") is a more powerful library. It can:

- Extract text (like pypdf)
- Read images embedded in a PDF
- **Render any PDF page as a picture (a PNG or JPEG image)**

We use this third capability for plan PDFs. Each page gets rendered as a high-resolution JPEG, which we then send to the vision-capable AI model.

### Pillow (version 11.0.0) — for image manipulation

Pillow is the standard Python library for working with images. We use it to:

- Resize images that are too large (the AI model has size limits)
- Convert images to JPEG (smaller file size than PNG for photographic content)
- Adjust quality vs. file size

**Why we resize:** A plan PDF page rendered at 300 DPI can be 5000×7000 pixels. The OpenAI vision API works best with images ≤ 2048 pixels on the longest edge. So we downsize while preserving readability.

## Frontend

The web page you see at `http://127.0.0.1:8000` is built with:

- **HTML** — the structure of the page (headings, forms, buttons)
- **CSS** — the styling (dark theme, fonts, layout)
- **JavaScript** — the interactivity (submitting forms, displaying results)

There's no React, Vue, or Angular framework — just plain "vanilla" web technologies. This was a deliberate choice:

- No build step required (no `npm install`, no compilation)
- The HTML/CSS/JS files are tiny (about 15 KB combined) and load instantly
- Anyone who knows basic web technology can read and modify the code

The downside: if you wanted a complex interactive dashboard later, you'd probably switch to React. For this prototype, vanilla is the right call.

## Configuration

### python-dotenv (version 1.0.1)

This library reads a file called `.env` (with no name before the dot) at startup. The `.env` file contains your secrets: API keys, deployment names, endpoints. Keeping them in `.env` instead of the code means:

- You can share the code on GitHub without leaking your credentials
- You can swap from one Azure account to another by editing one file
- Different team members can use different credentials

The `.env` file is listed in `.gitignore`, which tells the version-control system (Git) to never accidentally commit it.

### pydantic (version 2.9.2)

Pydantic validates data. When your browser sends a form submission to `/api/checklist`, FastAPI uses pydantic to check that:

- All required fields are present
- They're the right types (numbers are numbers, text is text)
- Defaults are applied where you didn't fill in a value

If anything is wrong, pydantic returns a clear error message instead of crashing.

### Other dependencies

- `python-multipart` — for handling file uploads (used by Flow 1)
- `httpx` (pinned to `<0.28`) — the HTTP client the OpenAI library uses internally; a specific version is required to avoid a known bug
- `jinja2` — templating library (used internally by FastAPI for static file serving)

---

# Part 4 — Architecture and the Skills Layer

This section explains how all the pieces fit together. I'll start with a big-picture diagram, then drill into the two most interesting parts: the skills layer and the vision pipeline.

## Big-Picture Diagram

Here's what happens when you click "Generate Compliance Checklist":

```
   ┌──────────────────────────────────────────────────────────┐
   │  Your browser at http://127.0.0.1:8000                   │
   │  (Fills form → clicks button)                            │
   └──────────────────┬───────────────────────────────────────┘
                      │  POST /api/checklist (JSON)
                      ▼
   ┌──────────────────────────────────────────────────────────┐
   │  FastAPI server (main.py)                                │
   │  - Validates form via pydantic                           │
   │  - Routes to checklist_agent.run_checklist_agent()       │
   └──────────────────┬───────────────────────────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────────────────────────┐
   │  app/agents/checklist_agent.py                           │
   │  1. Loads 8 skills from app/skills/files/*.md            │
   │  2. Concatenates them into the system prompt             │
   │  3. Builds a user message with your project details      │
   │  4. Calls call_chat() in azure_client.py                 │
   └──────────────────┬───────────────────────────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────────────────────────┐
   │  app/azure_client.py                                     │
   │  - Constructs AzureOpenAI client from .env config        │
   │  - Sends request with max_completion_tokens + JSON mode  │
   └──────────────────┬───────────────────────────────────────┘
                      │  HTTPS over the internet
                      ▼
   ┌──────────────────────────────────────────────────────────┐
   │  Azure OpenAI in eastus2                                 │
   │  - gpt-5.2 model thinks about the request                │
   │  - Returns a JSON object                                 │
   └──────────────────┬───────────────────────────────────────┘
                      │  HTTPS response
                      ▼
              (Back through azure_client → checklist_agent →
               FastAPI → browser, which renders the JSON)
```

Flow 1 (corrections interpreter) is similar but adds a vision step before the corrections agent:

```
              Upload corrections-letter PDF + plan PDF
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │  main.py /api/corrections                                │
   │  - Extracts text from corrections letter (pypdf)         │
   │  - Renders plan PDF pages to images (PyMuPDF)            │
   └──────────────────┬───────────────────────────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────────────────────────┐
   │  plan_vision_agent.py                                    │
   │  Sends N images to Azure OpenAI vision API               │
   │  Returns sheet-by-sheet manifest with measurements       │
   └──────────────────┬───────────────────────────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────────────────────────┐
   │  corrections_agent.py                                    │
   │  Takes: corrections text + vision summary + skills       │
   │  Returns: 4-part response package                        │
   └──────────────────┬───────────────────────────────────────┘
                      │
                      ▼
              Final JSON to browser, rendered
```

## The Skills Layer

This is the most important architectural choice in Permit Setu.

### The problem

LLMs are smart but they don't know your specific domain. GPT-5.2 doesn't know:

- The exact minimum front setback under the amended Karnataka Zonal Regulations as of 5 January 2026
- That E-Khata is mandatory as of 1 July 2025
- That the GBA road-width relaxation allows construction on 12-15 ft roads

We need to tell the model these things. The naive approach is to write one huge prompt. But:

- Huge prompts cost more (you pay per token)
- They're hard to maintain (one wrong word and the model behavior changes)
- They become impossible to update (which paragraph governs setbacks? Which one is about parking?)

### The solution: a directory of markdown files

Instead of one big prompt, we have **9 separate markdown files** in `app/skills/files/`, each covering one domain:

| File | Covers |
|---|---|
| `ktcp-act-1961.md` | The Karnataka Town and Country Planning Act — the foundation legislation |
| `zonal-regulations-2026.md` | The amended zonal regulations effective Jan 5-6, 2026 |
| `setback-table.md` | Quick-reference table of setbacks by plot size and zone |
| `far-table.md` | Floor Area Ratio limits by zone, with examples |
| `parking-norms.md` | Car/two-wheeler/EV parking requirements |
| `khata-rules.md` | A-Khata / B-Khata / E-Khata distinctions |
| `nambike-nakshe.md` | The self-certification track for small residential plots |
| `decision-tree-router.md` | A flowchart that walks through which rules apply to which project |
| `corrections-workflow.md` | How to format a response letter, by-the-book |

Each file is plain English (with the occasional table). Anyone — including a non-engineer — can edit them.

### How they get used

A small Python file called `skill_loader.py` provides three functions:

- `list_available_skills()` — returns the names of all skill files
- `load_skill(name)` — loads a single file as a string
- `load_skills([names])` — loads multiple files and concatenates them with clear separators

Each agent declares which skills it needs at the top:

```python
# In checklist_agent.py
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
```

When the agent runs, it loads these skills and embeds them in the system prompt.

### Why this matters

**1. Updates are trivial.** Karnataka changes the FAR rules for RM-2 zones. You open `far-table.md`, edit one line, save. The next request uses the new rule. No code change, no model retraining, no deployment.

**2. Auditability.** Lawyers and city officials can read exactly what the AI was told. The rules aren't hidden inside a black-box model — they're in plain markdown files.

**3. Selective loading.** Flow 2 needs setback rules but not the corrections workflow. Flow 1 needs the corrections workflow but uses the setback rules differently. By loading only what each flow needs, we save tokens (money) and reduce noise.

**4. Composability.** Want to add a new flow for "Pre-Demolition Compliance Check"? Reuse `khata-rules.md` and `ktcp-act-1961.md`, add one new file `demolition-rules.md`, and you're done.

This pattern — **skills as structured external knowledge files** — was popularized by Anthropic's Claude in 2024-2025 and is now a standard pattern for grounding LLMs in specialized domains.

## The Vision Pipeline

Now let's dig into how plan PDFs get read.

### The challenge

An architectural plan PDF looks like this when you open it in Adobe Reader:

- Cover sheet with title block, FAR calculation table, owner info
- Site plan with the plot outline, building footprint, setback dimensions, north arrow, road indication
- Floor plans (ground, first, second) with room layouts, doors, windows, dimension lines
- Elevations (north, south, east, west) showing the building's external appearance
- Sections (vertical cross-sections through the building)
- Plumbing, electrical, structural details

If you ask `pypdf` to extract text from this, you might get back a few stray labels — but you'll miss:

- Any dimension shown as a number with a line below it
- Any value in the FAR calculation table
- The setback measurements
- The text inside the title block
- Everything that's drawn rather than typed

That's because in a CAD-exported PDF, most "text" is actually vector graphics — lines arranged to look like numbers. They're not stored as searchable strings.

### The solution: render and look

Here's what `pdf_utils.pdf_to_base64_images()` does, step by step:

**Step 1 — Open the PDF.** Using PyMuPDF, we open the PDF as a document object.

**Step 2 — For each page (capped at 8 pages by default):**

  a. Calculate a rendering matrix. PDFs natively use 72 DPI (dots per inch). To render at 150 DPI, we scale by 150/72 ≈ 2.08.

  b. Generate a pixmap (a grid of pixel values) at the new resolution.

  c. Convert the pixmap to a Pillow Image object.

  d. If the image is wider than 2048 pixels on the longest edge, resize it down (the vision API charges more for huge images, and there's no benefit beyond 2048).

  e. Save the image to an in-memory buffer as JPEG at 85% quality. JPEG is much smaller than PNG for plan drawings.

  f. Base64-encode the JPEG bytes. Base64 is a way to represent binary data as a long string of letters and digits. The API expects images as base64 because it travels well over HTTP.

  g. Wrap the base64 string in a "data URL" — a special format that says *"here's an inline image of type image/jpeg, base64-encoded:"* followed by the data.

**Step 3 — Return the list of data URLs.**

The resulting list is something like:

```python
[
  "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",  # page 1, ~150 KB
  "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",  # page 2, ~140 KB
  "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ...",  # page 3, ~100 KB
]
```

### Sending to the vision API

In `azure_client.call_vision()`, we build the OpenAI multimodal message format:

```python
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Analyze these plan sheets..."},
    {"type": "image_url", "image_url": {"url": "<data URL for page 1>", "detail": "auto"}},
    {"type": "image_url", "image_url": {"url": "<data URL for page 2>", "detail": "auto"}},
    ...
  ]
}
```

The `detail` field controls how thoroughly the model examines each image:

- `low` — the model gets a low-resolution thumbnail, costs ~85 tokens per image. Good for "is this an architectural drawing?"
- `high` — the model gets the full high-res image, costs ~765 tokens per image. Good for "what does this setback dimension say?"
- `auto` — the model decides based on image size. Usually picks high for plan PDFs.

For a typical 3-page residential plan set with `detail: auto`, the vision call costs roughly $0.03-0.10 USD depending on model and image size.

### What the vision model returns

`plan_vision_agent.py` instructs the model to return a structured JSON object with:

- `sheet_manifest` — for each page: sheet number, sheet title, drawing types, key measurements (setbacks, FAR, parking), compliance flags
- `overall_observations` — a one-paragraph summary of the plan set
- `compliance_red_flags` — high-level issues spanning multiple sheets
- `missing_required_sheets` — sheets the model expected to see but didn't

This structured output is then passed as `plan_summary` to the corrections agent.

## Why Two Agents in Flow 1

You might wonder why we don't just send everything (corrections letter + plan images + rules) to one big model call. Two reasons:

**1. Different jobs, different prompts.** The vision agent is told to read drawings like a senior plan reviewer. The corrections agent is told to draft formal response letters like a paralegal. Each has a focused, specialized system prompt. Mixing them would make the prompt long and confusing for the model.

**2. Cost and latency.** The vision call costs more per token because of the images. If we put everything in one call, every retry, every reasoning step pays the image cost. By doing vision once, summarizing into a compact text manifest, and then doing the corrections work in text-only mode, we save 30-60% on cost.

This pattern — **decompose into specialist agents, pass structured intermediate outputs between them** — is the dominant architecture for modern LLM applications. It's also how Anthropic's original CrossBeam was built.

---

# Part 5 — Setup and Troubleshooting

## Prerequisites

- **A Windows, Mac, or Linux computer** with at least 4 GB RAM
- **Python 3.10 or later** installed. To check: open a terminal and run `python --version`. If it says `Python 3.10.x` or higher, you're good. If not, download from [python.org](https://www.python.org/downloads/).
- **An Azure account** with an active subscription
- **An Azure OpenAI resource** with a chat-capable deployment. Most users will use `gpt-4o`, `gpt-4o-mini`, or `gpt-5.2`. The deployment must be in a region that supports your chosen model.
- **About 15 minutes** for first-time setup

## Installation

Open a terminal (PowerShell on Windows, Terminal on Mac/Linux) and navigate to where you want the project:

```bash
cd C:\Users\YourName\Projects     # Windows
# or
cd ~/projects                     # Mac/Linux
```

If you received the project as a folder, navigate into it. If you're cloning from a repository:

```bash
git clone <repository-url>
cd crossbeam-india
```

Create a virtual environment. This is a Python sandbox where this project's dependencies live without affecting the rest of your system:

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate
```

When the virtual environment is active, you'll see `(.venv)` at the start of your prompt.

Install all required Python libraries:

```bash
pip install -r requirements.txt
```

This downloads about 20 libraries totalling roughly 80 MB. Takes 1-3 minutes depending on your internet.

## Configuration

You need to tell Permit Setu how to reach your Azure OpenAI deployment.

Copy the template file:

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` in a text editor (Notepad, VS Code, anything). You'll see:

```
AZURE_OPENAI_ENDPOINT=https://YOUR_RESOURCE_NAME.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_VISION_DEPLOYMENT_NAME=
AZURE_OPENAI_API_VERSION=2024-10-21
```

Fill in the four credential lines:

### 1. AZURE_OPENAI_ENDPOINT

In the Azure Portal, navigate to your Azure OpenAI resource → click "Keys and Endpoint" in the left menu → copy the value labeled **Endpoint**. It looks like `https://something.openai.azure.com/` or `https://something.cognitiveservices.azure.com/`.

### 2. AZURE_OPENAI_API_KEY

On the same page, copy either **KEY 1** or **KEY 2**. Both work. Treat this like a password — never commit it to GitHub, never share in chat.

### 3. AZURE_OPENAI_DEPLOYMENT_NAME

This is **not** the model name. It's the deployment name you (or your Azure admin) chose when deploying the model.

To find it: in the Azure Portal, navigate to **Azure AI Foundry** (or **Azure OpenAI Studio** in older interfaces) → click **Deployments** → find your active deployment and copy the **Name** column. It might be `gpt-4o`, `my-gpt4`, `production-deployment`, or anything else — whatever was chosen when the deployment was created.

### 4. AZURE_OPENAI_VISION_DEPLOYMENT_NAME (optional)

If your main deployment is already vision-capable (gpt-4o, gpt-4o-mini, gpt-5.2), leave this blank. If you have a separate deployment for vision, set it here.

### 5. AZURE_OPENAI_API_VERSION

Default `2024-10-21` works for most cases. Use `2024-12-01-preview` if you need the latest features.

Save the file and close the editor.

## Running

Before the first real run, verify everything is installed correctly:

```bash
python smoke_test.py
```

You should see:

```
============================================================
1. Module imports
============================================================
  [OK]  Import all Permit Setu modules
...
  ALL CHECKS PASSED. You can now configure .env and run: python main.py
```

Now start the server:

```bash
python main.py
```

You should see:

```
============================================================
Permit Setu: BBMP/GBA Building Plan Compliance Assistant
============================================================
Starting server at http://127.0.0.1:8000
Azure OpenAI text deployment:   gpt-5.2
Azure OpenAI vision deployment: gpt-5.2
Azure OpenAI API version:       2024-12-01-preview
============================================================
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Open your browser to **http://127.0.0.1:8000**.

The badge in the top-right corner should say *"Azure OpenAI ready · gpt-5.2 · 2024-12-01-preview"* in green. If it's red, check the message and adjust `.env`.

To stop the server, press **Ctrl+C** in the terminal.

## Common Errors

### "Missing or unset environment variables"

You haven't created `.env` (only `.env.example`), or you left placeholder values. Open `.env` and fill in real Azure OpenAI credentials.

### "Client.__init__() got an unexpected keyword argument 'proxies'"

The httpx library is too new for the current openai SDK. Run:

```bash
pip install "httpx>=0.27,<0.28" --upgrade
```

(This pin is already in `requirements.txt`, so a fresh `pip install -r requirements.txt --upgrade` fixes it.)

### "404 Resource not found"

The deployment name in `.env` doesn't match any deployment in your Azure resource. Open Azure AI Foundry → Deployments → copy the exact name, paste it back. Case-sensitive.

### "401 Unauthorized" or "403 Forbidden"

The API key is wrong, expired, or rotated. Copy a fresh key from Azure Portal → Keys and Endpoint.

### "Unsupported parameter: 'max_tokens' is not supported with this model"

Your deployment is a reasoning model (gpt-5.x, o1, o3) that requires `max_completion_tokens` instead. This should be fixed in the current code — make sure you have the latest `azure_client.py`. If you customized it, replace `max_tokens` with `max_completion_tokens` and remove explicit `temperature=` parameters.

### "InvalidRequestError: 'response_format' of type 'json_object' is not supported"

Your API version is too old. Set `AZURE_OPENAI_API_VERSION=2024-08-01-preview` or later in `.env`.

### "image_url is not supported by this model"

Your deployment isn't vision-capable. Either:

- Deploy `gpt-4o` or `gpt-4o-mini` and set `AZURE_OPENAI_VISION_DEPLOYMENT_NAME` to it, **or**
- Untick "Use vision" in the Flow 1 form to fall back to text-only

### "Connection error" / "Could not resolve host"

You're either offline, behind a corporate firewall that blocks Azure, or on a VPN that's mis-routing requests. Check `ping <your-endpoint-domain>` from a terminal. If your network is the issue, try disabling the VPN or using a different network.

### Long response times (60-120 seconds)

This is normal for the corrections flow. Vision calls add overhead. To speed up development:

- Use `gpt-4o-mini` instead of `gpt-4o` (3-5× faster, ~70% as accurate)
- Lower `max_plan_pages` (e.g., 3 instead of 8)
- Set `vision_detail=low` in the Flow 1 form

### The UI loads but every button does nothing

Open the browser developer console (F12 in most browsers, then "Console" tab). You'll see the actual error. Usually it's a network issue between your browser and the server, or a CORS error if you opened the page from a different origin (don't open the HTML file directly — always go through `http://127.0.0.1:8000`).

---

# Part 6 — Glossary and FAQ

## Glossary

### Building and Permit Terms

**ADU (Accessory Dwelling Unit)** — A secondary residential unit on a single-family residential lot. Common in California; called by different names in India.

**A-Khata** — A property record issued by BBMP for properties that comply with all rules (taxation, planning, zoning). Required for building plan approval, bank loans, and utility connections.

**B-Khata** — A property record for properties with violations or unauthorized layouts. Building plan approval is not possible with B-Khata.

**BBMP** — Bruhat Bengaluru Mahanagara Palike. The city corporation of Bengaluru. Recently restructured under the GBA Act 2024.

**BPAS** — Building Plan Approval System. The online portal at `bpas.bbmpgov.in` where plans are submitted.

**E-Khata** — The electronic version of an A-Khata. Mandatory for all BBMP plan approvals as of 1 July 2025.

**ePID** — Electronic Property ID. A unique identifier tied to an E-Khata.

**FAR (Floor Area Ratio)** — The ratio of total built-up area to plot area. If FAR = 1.75 and the plot is 1,200 sq ft, you can build up to 2,100 sq ft total floor area across all floors.

**FSI (Floor Space Index)** — Same thing as FAR; different jurisdictions use different terms.

**GBA (Greater Bengaluru Authority)** — A new authority empowered by the Greater Bengaluru Governance Act, 2024. Replaced BBMP for many approval functions starting in 2026.

**KTCP Act** — Karnataka Town and Country Planning Act, 1961. The foundational state legislation governing urban planning and building approvals in Karnataka.

**Nambike Nakshe** — Kannada for "Trusted Map." A self-certification track for small residential plots (up to 50×80 ft) where a licensed architect personally certifies the plan, bypassing detailed pre-approval scrutiny.

**OC (Occupancy Certificate)** — A document issued after construction confirming the building was built per the sanctioned plan. Required before utility connections — except for houses ≤ 1,200 sq ft under the new 2026 exemption.

**RMP (Revised Master Plan)** — Bengaluru's master plan governing land use, zoning, and development controls. RMP 2015 is in force; RMP 2031 is in draft.

**RWH (Rainwater Harvesting)** — A pit or system to collect rainwater. Mandatory for new constructions in BBMP limits.

**Sakala Mission** — A Karnataka government initiative guaranteeing citizen-service timelines. Under Sakala, BBMP must respond to a plan submission within 30 working days or the plan is deemed approved.

**Setback** — The minimum distance the building must be set back from each boundary of the plot (front, rear, sides).

**Stilt** — An open ground floor used for parking, where columns support the upper floors. Doesn't count toward FAR.

**Zonal Regulations** — Detailed building rules organized by land-use zone (R for single-family, RM for mixed-use, C for commercial, etc.).

### AI and Software Terms

**API (Application Programming Interface)** — A way for two pieces of software to communicate. Azure OpenAI's API is what we use to send prompts and receive responses.

**Base64** — A way to encode binary data (like images) as text. Used because text travels well over the internet, while binary data can get corrupted by intermediate systems.

**Base prompt / System prompt** — The instructions given to an LLM before the user's question, setting up its role and constraints. In Permit Setu, the skills layer is bundled into the system prompt.

**Bytecode** — Compiled Python code stored in `__pycache__` folders. Speeds up imports. Safe to delete.

**FastAPI** — A Python framework for building web APIs.

**HTTP/HTTPS** — The protocol used by web browsers and APIs. HTTPS is HTTP encrypted with TLS for security.

**JSON (JavaScript Object Notation)** — A format for structured data. Looks like `{"key": "value", "list": [1, 2, 3]}`. The format LLMs return when JSON-mode is enabled.

**JSON mode** — A feature in newer OpenAI / Azure OpenAI APIs that forces the model to return only valid JSON.

**LLM (Large Language Model)** — An AI model trained on huge amounts of text. Examples: GPT-4o, GPT-5.2, Claude Opus, Gemini.

**Multimodal** — An AI model that accepts more than one type of input (e.g., text + images).

**OpenAI SDK** — A library that wraps the OpenAI / Azure OpenAI API. We use the Python version (`openai` package).

**Prompt** — The text input given to an LLM.

**Reasoning model** — A newer type of LLM (gpt-5.x, o1, o3) that internally reasons through problems before responding. Higher accuracy on complex tasks but slower and more expensive.

**Skills layer** — A pattern where domain knowledge lives in structured external files (in our case, markdown files) and gets loaded into the system prompt as needed.

**Token** — A unit roughly equivalent to a syllable or short word. LLMs charge per token. A 4-word sentence is about 5-7 tokens.

**Vision API** — An API call that includes images as input. Requires a vision-capable model deployment.

**Virtual environment (venv)** — A Python sandbox isolating one project's dependencies from the rest of the system.

## Frequently Asked Questions

### Is this a finished product I can sell to architects?

No. It's a prototype that demonstrates what's possible. To turn it into a real product you'd need: authentication, audit logging, persistent storage, billing, multi-tenancy, professional indemnity insurance for the AI's outputs, and validation by Karnataka legal counsel. None of that is built. Treat it as an MVP that proves the architecture works.

### How much does each call cost?

It depends on which Azure OpenAI deployment you use. Rough estimates as of 2026:

- **Flow 2 checklist** with gpt-4o: ₹15-25 per request (input + output tokens, no images)
- **Flow 1 corrections (text-only)** with gpt-4o: ₹30-50 per request
- **Flow 1 corrections with vision** (8 plan pages): ₹80-200 per request

Reasoning models like gpt-5.2 cost more per token but use fewer tokens because they reason more efficiently. Net cost is usually within 20-50% of gpt-4o.

### Can I use OpenAI directly instead of Azure OpenAI?

Yes, with a small code change. In `app/azure_client.py`, replace `AzureOpenAI` with `OpenAI` and adjust the parameters. The skills layer, vision pipeline, and agent logic all work identically.

We chose Azure OpenAI because it has better enterprise compliance, Indian data residency options, and unified billing with other Azure services.

### Can I use a different LLM (Claude, Gemini, local Llama)?

Yes, but it requires more code changes. The agents call `call_chat()` and `call_vision()` — you'd need to swap the implementations of these functions to use a different SDK. The skills layer and the agents themselves are model-agnostic.

For Claude (Anthropic), use the `anthropic` Python SDK. For Gemini, use `google-generativeai`. For local models, use `ollama` or `vllm`.

### Is my data safe?

Your data (form inputs, uploaded PDFs) never leaves your computer except as direct HTTPS calls to your Azure OpenAI deployment. Azure contractually commits that:

- Your inputs are not used to train Microsoft's or OpenAI's models
- Your inputs are stored only transiently (typically 30 days) for abuse-monitoring purposes
- You can opt out of even that retention if you're enterprise-eligible

The `.env` file containing your API key is in `.gitignore`, so it won't accidentally get committed to a public repo. **But the code itself never encrypts anything** — if someone has access to your laptop, they can read your `.env`.

### Will this work for cities other than Bengaluru?

Not out of the box. The skills layer is Karnataka-specific. To adapt to (say) Mumbai under MCGM and DCPR 2034, you'd:

1. Replace `app/skills/files/*.md` with Mumbai-specific rules
2. Update the agent system prompts to reference the new authority (e.g., "MCGM" instead of "BBMP/GBA")
3. Possibly add city-specific NOC checks (e.g., MHADA for redevelopment in Mumbai)

The architecture is portable. The content is the work.

### What's the difference between this and ChatGPT?

ChatGPT is a generic chatbot. Permit Setu is a focused application that:

- Is **grounded** in specific Karnataka rules (not just generic knowledge)
- Has **structured outputs** (JSON checklists, formal letters) you can use directly
- **Reads architectural drawings** with vision, not just text
- **Runs locally** with your data staying on your machine
- Has **specific agent prompts** tuned for one job, not a generalist assistant

You could prompt ChatGPT with the same skills layer manually and get similar results — but you'd have to do that every time, and the outputs wouldn't be structured for automation.

### Is the AI ever wrong?

Yes, sometimes. LLMs hallucinate — they occasionally state things confidently that aren't quite right. Permit Setu mitigates this by:

- Grounding the model in real rule files (the skills layer)
- Asking for structured outputs that are easier to verify
- Forcing the model to cite specific rule sections

But you **must always verify the output before submitting to BBMP**. The architect, not the AI, is the legal signatory. Use Permit Setu as a junior assistant that helps you draft and check — not as the final word.

### How do I update for a new BBMP notification?

Open `app/skills/files/` in any text editor. Find the relevant markdown file (e.g., `zonal-regulations-2026.md` for changes to setbacks or FAR). Edit the text. Save. Done. The next request to the agent will use the updated rule.

For a totally new domain (say, fire safety NOC rules), create a new file `fire-safety.md`, add it to the relevant agent's `SKILLS = [...]` list in `app/agents/*.py`, save. No restart needed if `python main.py` is running with auto-reload.

### Can I deploy this for my team to use?

Not as-is. The current setup binds to `127.0.0.1` (your own machine only) and has no authentication. To deploy for a team you'd want to:

1. Host the FastAPI app on a server (Azure App Service, Cloud Run, etc.) in the `ap-south-1` (Mumbai) region for DPDP Act compliance
2. Put it behind an authentication layer (Microsoft Entra ID works natively with Azure OpenAI)
3. Add per-user usage tracking
4. Add persistent storage so people can revisit past audits
5. Set up CI/CD so updates to the skills layer can be reviewed before going live

That's another 1-2 weeks of work on top of the current prototype.

### Where do I report bugs or suggest features?

If this is on a GitHub repository, open an Issue. If not, document the bug clearly (steps to reproduce, what you expected, what happened) and email the maintainer.

For features, prioritize ones that are useful across many architects, not just your specific project. The most valuable contributions tend to be:

- New skill files covering more jurisdictions
- Better PDF rendering for edge-case plan formats
- Improved corrections-letter format compatibility (different BBMP zones format their letters slightly differently)

---

## Final Note

This documentation aims to be readable by someone who has never written code before, AND useful as a reference for someone who's about to deploy Permit Setu in production. If anything is unclear in either direction, that's a documentation bug — please flag it.

The project is small (about 1,500 lines of Python plus 27,000 characters of Karnataka rules in markdown), but the architecture is designed to grow. Adding a new city, a new flow, or a new compliance domain doesn't require rewriting the codebase — it just requires writing more markdown.

Good luck building.
