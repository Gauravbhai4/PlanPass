# Decision Tree Router — Which Track and Rules Apply?

This is the master decision tree for any BBMP/GBA residential building plan. The agent uses this to route every project to the right rule set.

## Step 1 — Khata Check

```
Is the property A-Khata with active E-Khata + ePID?
├── YES → Continue to Step 2
└── NO  → STOP. Cannot submit plan.
          → Required action: B-Khata to A-Khata conversion
          → Reference: khata-rules skill
```

## Step 2 — Road Width Check

```
What is the verified road width facing the plot?
├── < 12 ft  → STOP. Construction not permitted on this road.
├── 12-15 ft → Limited construction; refer to GBA 2026 relaxation
│              → Max permissible height: G+2 typically
├── 15-30 ft → Standard residential; G+3 typical
├── 30-40 ft → G+4 stilt+4 possible
└── > 40 ft  → Higher density permitted; check zonal FAR table
```

## Step 3 — Plot Size Check

```
What is the plot area (sq ft)?
├── ≤ 600 sq ft
│   ├── Setbacks: 0.75m front, 0.6m one side, NO rear
│   ├── Height: typically G+1, possibly G+2
│   ├── Track: Nambike Nakshe if A-Khata
│   └── OC exemption: YES (if total built-up ≤ 1,200 sq ft)
│
├── 600 - 1,200 sq ft (e.g., 20x40 or 30x40)
│   ├── Setbacks: see setback-table — 0.9m-1.2m front, 0.9m sides, 1.5m rear
│   ├── Height: G+2 typical, G+3 with premium FSI
│   ├── Track: Nambike Nakshe
│   └── OC exemption: possibly YES (depends on built-up)
│
├── 1,200 - 2,400 sq ft (e.g., 30x40, 30x50, 40x60)
│   ├── Setbacks: 1.2-1.5m front, 0.9-1.2m sides, 1.5-1.8m rear
│   ├── Height: G+3 standard, G+4 with FAR available
│   ├── Track: Nambike Nakshe still valid up to 4,000 sq ft
│   └── OC exemption: only if built-up ≤ 1,200 sq ft
│
├── 2,400 - 4,000 sq ft (e.g., 40x60, 50x80)
│   ├── Setbacks: 1.5-1.8m front, 1.2-1.5m sides, 1.8-2.4m rear
│   ├── Height: G+4 standard
│   ├── Track: Nambike Nakshe (upper limit 50x80)
│   └── OC exemption: NO if built-up > 1,200 sq ft
│
└── > 4,000 sq ft
    ├── Setbacks: percentage-based; consult zonal regulation
    ├── Track: STANDARD review (not Nambike Nakshe)
    ├── OC: MANDATORY
    └── Often requires structural engineer NOC
```

## Step 4 — Zone Check

```
What is the Land Use designation (per RMP 2015)?
├── R   (Single-family residential) → Base FAR 1.75
├── RM-1 (Mixed-use, low density)   → Base FAR 2.25
├── RM-2 (Mixed-use, high density)  → Base FAR 2.75-3.25
├── C   (Commercial)                → Out of scope for residential flow
└── I   (Industrial)                → Residential not permitted
```

## Step 5 — Construction Type

```
What type of construction?
├── New construction       → Full plan + structural NOC if G+2+
├── Vertical extension     → Existing plan compliance + structural NOC
├── Horizontal extension   → Setback re-verification critical
├── Renovation only        → Often no plan needed (check threshold)
└── Demolition + rebuild   → Demolition permit + fresh plan
```

## Step 6 — Special Modifiers

Apply these AFTER routing:

- [ ] **Heritage zone or conservation area?** → Standard track only, additional NOC
- [ ] **Within 100m of a lake/water body?** → Buffer rules apply (KSPCB clearance)
- [ ] **Within 500m of an SEZ or industrial area?** → Additional NOC may apply
- [ ] **Tree felling required?** → BBMP Forest Cell NOC
- [ ] **G+3 or above?** → Fire NOC mandatory
- [ ] **Basement?** → BBMP basement parking NOC + structural NOC

## Final Output of Routing

The agent should produce:
1. Eligible submission track (Nambike Nakshe / Standard)
2. Applicable setback / FAR / height limits
3. Required NOCs and clearances
4. Estimated timeline (30 days deemed-approval under Sakala)
5. Estimated fees
6. Critical risks specific to this project
