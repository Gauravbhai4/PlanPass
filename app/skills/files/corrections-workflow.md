# BBMP Corrections Letter — Response Workflow

When BBMP/GBA issues an objections letter on a submitted plan, the architect must respond with a corrections package. This file teaches the agent how to walk that workflow.

## Typical Structure of a BBMP Corrections Letter

1. Application number and date
2. Owner/applicant details
3. Site details (PID, ward, zone)
4. List of objections, usually numbered (1, 2, 3...)
5. Each objection cites a specific rule or law section
6. Deadline for response (typically 15-30 days)
7. Signature of plan checker / Asst. Director of Town Planning (ADTP)

## Categorizing Each Objection

For every objection in the letter, classify it as one of:

| Category | Examples | Architect Action |
|----------|---------|------------------|
| **Auto-fixable** | Missing sheet number, incorrect title block, missing signature, missing FAR table on cover sheet | Architect fixes in drafting, no homeowner input needed |
| **Needs homeowner input** | "Confirm whether parking will be stilt or surface", "Provide latest property tax receipt", "Confirm number of dwelling units" | Architect cannot resolve alone; needs information |
| **Needs structural/MEP engineer** | "Provide structural stability certificate", "Re-verify load calculations for G+3" | Architect coordinates with consultant |
| **Code conflict** | "FAR exceeds zonal limit", "Setback insufficient" | Plan needs design revision, possibly reducing scope |
| **Documentation only** | "Submit latest e-khata", "Submit Form A self-declaration" | Architect collects and uploads |
| **Disputable** | "Site appears to be in conservation zone" (when it isn't) | Architect writes a clarification with supporting docs |

## Standard Response Letter Format

```
[Date]
To,
The Assistant Director of Town Planning
[Zone] Zone, BBMP/GBA
[Address]

Subject: Response to corrections letter dated [DATE] for Application No. [APPNO]
        Site: [PID / Property address]

Sir/Madam,

With reference to your corrections letter dated [DATE] regarding the above
captioned application, we submit the following point-wise responses:

Objection 1: [Quote the objection verbatim]
Response 1:  [Cite the rule complied with, reference the revised drawing
              sheet, attach proof]

Objection 2: [Quote]
Response 2:  [Response]

...

We confirm the revised plans are in full compliance with:
- Karnataka Town and Country Planning Act, 1961
- Revised Master Plan (RMP) 2015 with amended Zonal Regulations effective
  January 5-6, 2026
- BBMP Building Bye-Laws 2003 (as amended)

Submitted herewith:
1. Revised plan set (Sheets [A1 to An])
2. Latest E-Khata and ePID
3. Latest property tax receipt
4. [Other supporting docs]

We request you to kindly accept the revised plans and proceed with the
sanction.

Yours sincerely,
[Architect name]
Council of Architecture Reg. No: [CoA-XXXXX]
BBMP/GBA Empanelment No: [EMP-XXXXX]
```

## Tone and Drafting Rules

- **Always quote the objection verbatim** before responding
- **Cite the specific rule or section** the response complies with
- **Reference the exact drawing sheet number** where the change appears
- **Use formal English** — never colloquial or apologetic
- **Do not argue** — even if BBMP cited the wrong rule, comply where possible and politely clarify only where necessary
- **Number the responses to match the objection numbering**

## Common Mistakes Architects Make in Response Letters

1. Generic responses ("The plan has been revised") without citing the specific rule
2. Missing the revised sheet number reference
3. Not attaching the supporting document the objection asked for
4. Submitting a complete redraw instead of marking the specific changes
5. Missing the deadline (BBMP can dismiss the application if no response in 30 days)
6. Forgetting to update the title block date and revision number

## Output Package the Agent Should Produce

For each corrections case, the agent generates:

1. **`response_letter.md`** — The formal response letter in BBMP format
2. **`corrections_report.md`** — Internal status dashboard: each objection, category, action taken, who is responsible
3. **`scope_of_work.md`** — Drafting task list for the architect's CAD team (which sheets need updating, what to change on each)
4. **`sheet_annotations.json`** — Per-sheet markup instructions: `{ "A1": ["update title block date to ...", "add FAR table"], "A3": ["increase front setback to 1.2m"] }`
