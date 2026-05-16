/* Permit Setu · Dashboard logic */

// =========================
// View switching
// =========================
const PAGE_META = {
  dashboard:   { title: "Dashboard",                  sub: "AI-powered BBMP / GBA building plan compliance assistant" },
  checklist:   { title: "Pre-Submission Check",       sub: "Apply the 2026 Zonal Regulations to your project before you submit." },
  corrections: { title: "Corrections Response",       sub: "Read your plan PDF with vision and draft a full response package." },
  samples:     { title: "Sample Library",             sub: "Pre-built test cases that exercise different code paths." },
  rules:       { title: "Karnataka Rules",            sub: "Quick reference for the skills the agent is grounded in." },
  about:       { title: "About",                      sub: "Tech stack, inspiration, and project status." },
};

function showView(name) {
  document.querySelectorAll(".nav-item").forEach(b => b.classList.toggle("active", b.dataset.view === name));
  document.querySelectorAll(".view").forEach(v => v.classList.toggle("active", v.id === `view-${name}`));
  const meta = PAGE_META[name] || PAGE_META.dashboard;
  document.getElementById("page-title").textContent = meta.title;
  document.getElementById("page-sub").textContent = meta.sub;
  window.scrollTo({ top: 0, behavior: "instant" });
}

document.querySelectorAll(".nav-item").forEach(b => b.addEventListener("click", () => showView(b.dataset.view)));
document.querySelectorAll("[data-go]").forEach(b => b.addEventListener("click", () => showView(b.dataset.go)));

// =========================
// Health check
// =========================
(async function checkHealth() {
  const card = document.getElementById("health-card");
  const dot  = card.querySelector(".health-dot");
  const stat = card.querySelector(".health-status");
  const sub  = card.querySelector(".health-sub");
  try {
    const r = await fetch("/api/health");
    const d = await r.json();
    if (d.config_ok) {
      dot.className = "health-dot ok";
      stat.textContent = "Connected";
      sub.textContent = `${d.deployment} · ${d.api_version}`;
      const dashDep = document.getElementById("dash-deployment");
      const dashApi = document.getElementById("dash-apiversion");
      if (dashDep) dashDep.textContent = d.deployment || "—";
      if (dashApi) dashApi.textContent = d.api_version || "—";
    } else {
      dot.className = "health-dot err";
      stat.textContent = "Config issue";
      sub.textContent = d.config_message || "Check .env";
    }
  } catch (e) {
    dot.className = "health-dot err";
    stat.textContent = "Server unreachable";
    sub.textContent = "Restart python main.py";
  }
})();

// =========================
// Sample loaders for Flow 2
// =========================
const SAMPLES = {
  compliant: {
    plot_dimensions: "30x40",
    plot_area_sqft: "1200",
    zone: "R (Residential single-family)",
    khata_type: "A-Khata (with E-Khata)",
    road_width_ft: "30",
    construction_type: "New construction",
    proposed_floors: "G+2",
    built_up_area_sqft: "2000",
    num_units: "1",
    location: "Whitefield, Bengaluru",
    special_conditions: "None",
  },
  blocker: {
    plot_dimensions: "30x50",
    plot_area_sqft: "1500",
    zone: "R (Residential single-family)",
    khata_type: "B-Khata",
    road_width_ft: "25",
    construction_type: "New construction",
    proposed_floors: "G+3",
    built_up_area_sqft: "3000",
    num_units: "1",
    location: "HSR Layout, Bengaluru",
    special_conditions: "None",
  },
  marginal: {
    plot_dimensions: "40x60",
    plot_area_sqft: "2400",
    zone: "RM-1 (Residential mixed low density)",
    khata_type: "A-Khata (with E-Khata)",
    road_width_ft: "14",
    construction_type: "New construction",
    proposed_floors: "Stilt+4",
    built_up_area_sqft: "5000",
    num_units: "4",
    location: "Indiranagar, Bengaluru",
    special_conditions: "Adjacent to existing residential building on east side",
  },
};

function applySample(name) {
  const data = SAMPLES[name];
  if (!data) return;
  const form = document.getElementById("checklist-form");
  for (const [k, v] of Object.entries(data)) {
    const el = form.elements[k];
    if (el) el.value = v;
  }
}

document.querySelectorAll("[data-sample]").forEach(b =>
  b.addEventListener("click", () => applySample(b.dataset.sample))
);

document.querySelectorAll("[data-sample-link]").forEach(b =>
  b.addEventListener("click", () => {
    applySample(b.dataset.sampleLink);
    showView("checklist");
  })
);

// =========================
// Upload tile filename display
// =========================
document.querySelectorAll(".upload-tile input[type=file]").forEach(input => {
  input.addEventListener("change", () => {
    const tile = input.closest(".upload-tile");
    const label = tile.querySelector(".upload-filename");
    if (input.files && input.files.length > 0) {
      const f = input.files[0];
      label.textContent = `${f.name} · ${(f.size / 1024).toFixed(1)} KB`;
      tile.classList.add("has-file");
    } else {
      label.textContent = "No file selected";
      tile.classList.remove("has-file");
    }
  });
});

// =========================
// Status helper
// =========================
function setStatus(elId, message, type) {
  const el = document.getElementById(elId);
  el.textContent = message;
  el.className = "status " + (type || "");
}

// =========================
// Smart result renderers
// =========================
function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function makeCard(title, bodyHtml, headExtra = "") {
  return `
    <div class="result-card">
      <div class="result-card-head">
        <div class="result-card-title">${escapeHtml(title)}</div>
        ${headExtra}
      </div>
      <div class="result-card-body">${bodyHtml}</div>
    </div>`;
}

function kvGrid(obj) {
  const rows = Object.entries(obj).map(([k, v]) => {
    let display;
    if (Array.isArray(v)) display = v.map(x => escapeHtml(String(x))).join(", ");
    else if (typeof v === "object" && v !== null) display = `<code>${escapeHtml(JSON.stringify(v))}</code>`;
    else display = escapeHtml(String(v));
    const keyLabel = k.replace(/_/g, " ");
    return `<div class="kv"><div class="kv-key">${escapeHtml(keyLabel)}</div><div class="kv-val">${display}</div></div>`;
  });
  return `<div class="kv-grid">${rows.join("")}</div>`;
}

function bulletList(items) {
  if (!Array.isArray(items) || items.length === 0) return `<p style="color:var(--text-mute);font-size:13px">(none)</p>`;
  return `<ul class="bullet-list">${items.map(i => `<li>${escapeHtml(typeof i === "string" ? i : JSON.stringify(i))}</li>`).join("")}</ul>`;
}

function eligibilityBanner(check) {
  if (!check) return "";
  const pass = check.eligible_to_submit === true;
  const blockersText = (check.blockers && check.blockers.length)
    ? check.blockers.map(b => `<li>${escapeHtml(b)}</li>`).join("")
    : "<li>No blockers.</li>";
  return `
    <div class="eligibility-banner ${pass ? "pass" : "fail"}">
      <div class="eligibility-icon">${pass ? "✓" : "✗"}</div>
      <div>
        <div class="eligibility-title">${pass ? "Eligible to submit" : "Cannot submit yet"}</div>
        <div class="eligibility-sub">${pass ? "All blockers cleared. Proceed via the indicated track." : "Resolve the blockers below before submitting."}</div>
      </div>
    </div>
    ${!pass ? `<ul class="bullet-list">${blockersText}</ul>` : ""}`;
}

function copyBtn(textId) {
  return `<button class="copy-btn" data-copy-target="${textId}">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    Copy
  </button>`;
}

function attachCopyHandlers(root) {
  root.querySelectorAll(".copy-btn").forEach(b => {
    b.addEventListener("click", async () => {
      const targetId = b.dataset.copyTarget;
      const target = document.getElementById(targetId);
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.textContent);
        b.classList.add("copied");
        const orig = b.innerHTML;
        b.textContent = "Copied!";
        setTimeout(() => { b.innerHTML = orig; b.classList.remove("copied"); }, 1500);
      } catch (e) { /* ignore */ }
    });
  });
}

// =========================
// Alert summary builder
// =========================
function buildAlertSummary(groups) {
  // groups = [{kind: "critical"|"action"|"info"|"ok", title, items: [string|{text, meta?}]}]
  const nonEmpty = groups.filter(g => g.items && g.items.length > 0);
  if (nonEmpty.length === 0) return "";

  const totalCounts = nonEmpty.map(g => `<span style="color:${
    g.kind === "critical" ? "var(--red)" :
    g.kind === "action" ? "var(--amber)" :
    g.kind === "info" ? "var(--blue)" : "var(--green)"
  }">● ${g.items.length} ${g.title.toLowerCase()}</span>`).join("");

  const sections = nonEmpty.map(g => {
    const icon =
      g.kind === "critical" ? "!" :
      g.kind === "action" ? "⚠" :
      g.kind === "info" ? "i" : "✓";
    const rows = g.items.map(it => {
      const text = typeof it === "string" ? it : it.text;
      return `<div class="alert-row"><span class="alert-bullet">→</span><span>${escapeHtml(text)}</span></div>`;
    }).join("");
    return `<div class="alert-group ${g.kind}">
      <div class="alert-group-head">
        <span class="alert-icon-pill">${icon}</span>
        <span>${escapeHtml(g.title)}</span>
        <span class="alert-group-count">${g.items.length} item${g.items.length === 1 ? "" : "s"}</span>
      </div>
      <div class="alert-list">${rows}</div>
    </div>`;
  }).join("");

  return `<div class="alert-summary">
    <div class="alert-summary-head">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" style="color:var(--accent)"><polygon points="12 2 19 21 12 17 5 21 12 2"/></svg>
      <h3>At a glance</h3>
      <div class="summary-counts">${totalCounts}</div>
    </div>
    <div class="alert-summary-body">${sections}</div>
  </div>`;
}

// =========================
// Render Checklist (Flow 2) result
// =========================
function renderChecklist(json, container) {
  container.innerHTML = "";

  if (json.error) {
    container.innerHTML = makeCard("Error", `<pre>${escapeHtml(json.error)}</pre>${json.raw_response ? `<details style="margin-top:10px"><summary style="cursor:pointer;color:var(--text-mute);font-size:12px">Show raw response</summary><pre style="margin-top:8px;background:var(--surface-2);padding:10px;border-radius:6px;font-size:12px;white-space:pre-wrap">${escapeHtml(json.raw_response)}</pre></details>` : ""}`);
    return;
  }

  // ===== Build the at-a-glance alert summary =====
  const critical = [];
  const action = [];
  const info = [];
  const ok = [];

  if (json.eligibility_check) {
    if (json.eligibility_check.eligible_to_submit === false) {
      critical.push("Cannot submit yet — see blockers below");
      (json.eligibility_check.blockers || []).forEach(b => critical.push(b));
    } else if (json.eligibility_check.eligible_to_submit === true) {
      ok.push("Eligible to submit" + (json.submission_track ? ` via ${json.submission_track}` : ""));
    }
  }

  (json.gotchas || []).forEach(g => action.push(g));

  if (json.documents_required && json.documents_required.length) {
    info.push(`${json.documents_required.length} document(s) required — see list below`);
  }
  if (json.nocs_required && json.nocs_required.length) {
    info.push(`${json.nocs_required.length} NOC(s) required — see list below`);
  }

  if (json.applicable_rules) {
    const r = json.applicable_rules;
    if (r.front_setback_m || r.max_far) {
      const bits = [];
      if (r.front_setback_m) bits.push(`Front setback ${r.front_setback_m} m`);
      if (r.max_far) bits.push(`Max FAR ${r.max_far}`);
      if (r.max_height) bits.push(`Max height ${r.max_height}`);
      if (bits.length) ok.push(bits.join(" · "));
    }
  }

  if (json.estimated_timeline_days) {
    info.push(`Estimated timeline: ${json.estimated_timeline_days} days`);
  }
  if (json.estimated_fees_inr) {
    info.push(`Estimated fees: ${json.estimated_fees_inr}`);
  }

  const alertHtml = buildAlertSummary([
    { kind: "critical", title: "Blockers",       items: critical },
    { kind: "action",   title: "Watch out for",  items: action },
    { kind: "info",     title: "Need to prepare",items: info },
    { kind: "ok",       title: "Compliant",      items: ok },
  ]);

  // ===== Detail cards (in 2-col grid) =====
  const cards = [];

  if (json.summary) {
    cards.push({ span2: true, html: makeCard("Summary", `<p>${escapeHtml(json.summary)}</p>`) });
  }

  if (json.submission_track || json.eligibility_check) {
    let banner = "";
    if (json.eligibility_check) banner = eligibilityBanner(json.eligibility_check);
    const trackBody = json.submission_track ? `<p style="margin-top:8px"><strong style="color:var(--accent)">Submission track:</strong> ${escapeHtml(json.submission_track)}</p>` : "";
    cards.push({ span2: true, html: makeCard("Eligibility & track", banner + trackBody) });
  }

  if (json.applicable_rules && Object.keys(json.applicable_rules).length) {
    cards.push({ span2: true, html: makeCard("Applicable rules", kvGrid(json.applicable_rules)) });
  }

  if (json.documents_required) {
    cards.push({ html: makeCard("Documents required", bulletList(json.documents_required)) });
  }
  if (json.nocs_required) {
    cards.push({ html: makeCard("NOCs required", bulletList(json.nocs_required)) });
  }
  if (json.gotchas) {
    cards.push({ html: makeCard("Gotchas to watch for", bulletList(json.gotchas)) });
  }

  const meta = {};
  if (json.estimated_timeline_days) meta["Timeline (days)"] = json.estimated_timeline_days;
  if (json.estimated_fees_inr) meta["Estimated fees (INR)"] = json.estimated_fees_inr;
  if (Object.keys(meta).length) {
    cards.push({ html: makeCard("Timeline & cost", kvGrid(meta)) });
  }

  if (json.next_actions) {
    const items = (json.next_actions || []).map((a, i) =>
      `<li><strong style="color:var(--accent)">${i + 1}.</strong> ${escapeHtml(typeof a === "string" ? a : JSON.stringify(a))}</li>`).join("");
    cards.push({ span2: true, html: makeCard("Next actions", `<ol style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px">${items}</ol>`) });
  }

  const renderedKeys = new Set(["summary", "submission_track", "eligibility_check", "applicable_rules", "documents_required", "nocs_required", "gotchas", "estimated_timeline_days", "estimated_fees_inr", "next_actions"]);
  Object.entries(json).filter(([k]) => !renderedKeys.has(k)).forEach(([k, v]) => {
    const body = (typeof v === "object" && v !== null)
      ? (Array.isArray(v) ? bulletList(v) : kvGrid(v))
      : `<p>${escapeHtml(String(v))}</p>`;
    cards.push({ html: makeCard(k.replace(/_/g, " "), body) });
  });

  const gridHtml = `<div class="result-grid">${cards.map(c => c.html.replace('class="result-card"', c.span2 ? 'class="result-card span-2"' : 'class="result-card"')).join("")}</div>`;

  container.innerHTML = alertHtml + gridHtml;
}

// =========================
// Render Corrections (Flow 1) result
// =========================
function renderCorrections(json, container) {
  container.innerHTML = "";

  const v = json.plan_vision_result;
  const c = json.corrections_response;

  // Top-level error
  if (json.error || c?.error) {
    const msg = json.error || c.error;
    container.innerHTML = makeCard("Error", `<pre>${escapeHtml(msg)}</pre>`);
    return;
  }

  // ===== Build the at-a-glance alert summary =====
  const critical = [];
  const action = [];
  const info = [];
  const ok = [];

  if (c?.objections) {
    c.objections.forEach(o => {
      const cat = (o.category || "").toLowerCase();
      const numLabel = o.number ? `#${o.number} ` : "";
      const summary = o.verbatim
        ? (o.verbatim.length > 110 ? o.verbatim.slice(0, 110) + "…" : o.verbatim)
        : (o.agent_analysis || "");
      const line = `${numLabel}${summary}`;
      if (cat.includes("code conflict") || cat.includes("disputable")) critical.push(line);
      else if (cat.includes("engineer") || cat.includes("homeowner") || cat.includes("input")) action.push(line);
      else if (cat.includes("documentation") || cat.includes("auto-fixable") || cat.includes("auto fixable")) info.push(line);
      else action.push(line);
    });
  }

  if (v && !v.error) {
    (v.compliance_red_flags || []).forEach(f => critical.push(`Plan-vision: ${f}`));
    (v.missing_required_sheets || []).forEach(m => action.push(`Missing sheet: ${m}`));
    (v.sheet_manifest || []).forEach(s => {
      (s.compliance_flags || []).forEach(f => {
        const sn = s.sheet_number || "?";
        action.push(`Sheet ${sn}: ${f}`);
      });
    });
  }

  if (c?.objections && c.objections.length) {
    ok.push(`${c.objections.length} objection(s) parsed and categorized`);
  }
  if (c?.response_letter) {
    ok.push("Response letter drafted — ready to copy");
  }

  const alertHtml = buildAlertSummary([
    { kind: "critical", title: "Critical / code conflicts", items: critical },
    { kind: "action",   title: "Action required",           items: action },
    { kind: "info",     title: "For your information",      items: info },
    { kind: "ok",       title: "Done by the agent",         items: ok },
  ]);

  // ===== Detail cards =====
  const cards = [];

  let html = "";

  // ---------- Vision result ----------
  if (v && !v.error) {
    if (v.overall_observations) {
      html += makeCard("Plan vision · overall observations", `<p>${escapeHtml(v.overall_observations)}</p>`);
    }
    if (v.sheet_manifest && v.sheet_manifest.length) {
      const sheets = v.sheet_manifest.map(s => {
        const meas = s.key_measurements || {};
        const measHtml = Object.keys(meas).length ? kvGrid(meas) : "";
        const flagsHtml = s.compliance_flags && s.compliance_flags.length
          ? `<div style="margin-top:10px"><strong style="color:var(--amber);font-size:12px;text-transform:uppercase;letter-spacing:0.4px">Flags</strong>${bulletList(s.compliance_flags)}</div>`
          : "";
        const drawingsHtml = s.drawing_types && s.drawing_types.length
          ? `<div style="margin-bottom:10px;color:var(--text-dim);font-size:12.5px">Drawings: ${s.drawing_types.map(escapeHtml).join(", ")}</div>`
          : "";
        const notesHtml = s.notes ? `<p style="margin-top:8px;font-size:12.5px;color:var(--text-mute);font-style:italic">${escapeHtml(s.notes)}</p>` : "";
        return `<div class="objection-item">
          <div class="objection-head">
            <span class="obj-num">${escapeHtml(s.sheet_number || "?")}</span>
            <strong>${escapeHtml(s.sheet_title || "")}</strong>
          </div>
          ${drawingsHtml}${measHtml}${flagsHtml}${notesHtml}
        </div>`;
      }).join("");
      html += makeCard("Plan vision · sheet manifest", sheets);
    }
    if (v.compliance_red_flags && v.compliance_red_flags.length) {
      html += makeCard("Plan vision · overall red flags", bulletList(v.compliance_red_flags));
    }
    if (v.missing_required_sheets && v.missing_required_sheets.length) {
      html += makeCard("Plan vision · missing sheets", bulletList(v.missing_required_sheets));
    }
  } else if (v && v.error) {
    html += makeCard("Plan vision · error", `<p style="color:var(--amber)">${escapeHtml(v.error)}</p>${v.hint ? `<p style="color:var(--text-mute);margin-top:8px">${escapeHtml(v.hint)}</p>` : ""}`);
  }

  // ---------- Corrections response ----------
  if (c) {
    if (c.case_summary) {
      html += makeCard("Case summary", `<p>${escapeHtml(c.case_summary)}</p>`);
    }

    if (c.objections && c.objections.length) {
      const objs = c.objections.map(o => {
        const cat = (o.category || "").replace(/\s+/g, "-").toLowerCase();
        const responseHtml = o.recommended_response ? `<div class="obj-detail"><strong>Recommended response:</strong> ${escapeHtml(o.recommended_response)}</div>` : "";
        const docsHtml = o.supporting_docs_needed && o.supporting_docs_needed.length
          ? `<div class="obj-detail"><strong>Supporting docs:</strong> ${o.supporting_docs_needed.map(escapeHtml).join(", ")}</div>`
          : "";
        return `<div class="objection-item">
          <div class="objection-head">
            <span class="obj-num">#${escapeHtml(String(o.number || ""))}</span>
            <span class="category-badge ${cat}">${escapeHtml(o.category || "")}</span>
            ${o.cited_rule ? `<span style="color:var(--text-mute);font-size:12px;margin-left:auto">${escapeHtml(o.cited_rule)}</span>` : ""}
          </div>
          ${o.verbatim ? `<div class="obj-verbatim">"${escapeHtml(o.verbatim)}"</div>` : ""}
          ${o.agent_analysis ? `<div class="obj-detail"><strong>Analysis:</strong> ${escapeHtml(o.agent_analysis)}</div>` : ""}
          ${responseHtml}
          ${docsHtml}
        </div>`;
      }).join("");
      html += makeCard(`Objections (${c.objections.length})`, objs);
    }

    if (c.response_letter) {
      const id = "letter-text-" + Date.now();
      html += makeCard("Response letter (ready to copy)",
        `<div id="${id}" class="letter-preview">${escapeHtml(c.response_letter)}</div>`,
        copyBtn(id));
    }

    if (c.corrections_report) {
      const id = "rep-" + Date.now();
      html += makeCard("Corrections report",
        `<pre id="${id}" style="white-space:pre-wrap;font-family:var(--font-sans);font-size:13.5px;line-height:1.6">${escapeHtml(c.corrections_report)}</pre>`,
        copyBtn(id));
    }

    if (c.scope_of_work) {
      const id = "sow-" + Date.now();
      html += makeCard("Scope of work for drafting team",
        `<pre id="${id}" style="white-space:pre-wrap;font-family:var(--font-sans);font-size:13.5px;line-height:1.6">${escapeHtml(c.scope_of_work)}</pre>`,
        copyBtn(id));
    }

    if (c.sheet_annotations && Object.keys(c.sheet_annotations).length) {
      const rows = Object.entries(c.sheet_annotations).map(([sheet, items]) => {
        const list = Array.isArray(items) ? items : [String(items)];
        return `<div class="objection-item">
          <div class="objection-head"><span class="obj-num">${escapeHtml(sheet)}</span></div>
          ${bulletList(list)}
        </div>`;
      }).join("");
      html += makeCard("Per-sheet annotations", rows);
    }

    if (c.open_questions_for_owner && c.open_questions_for_owner.length) {
      html += makeCard("Open questions for the owner", bulletList(c.open_questions_for_owner));
    }
  }

  if (!html) {
    html = makeCard("Raw response", `<pre style="background:var(--surface-2);padding:14px;border-radius:6px;font-size:12px;white-space:pre-wrap">${escapeHtml(JSON.stringify(json, null, 2))}</pre>`);
  }

  container.innerHTML = alertHtml + html;
  attachCopyHandlers(container);
}

// =========================
// Form submissions
// =========================
document.getElementById("checklist-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = Object.fromEntries(new FormData(form).entries());
  const outputDiv = document.getElementById("checklist-output");
  outputDiv.innerHTML = "";
  setStatus("checklist-status", "Running compliance check (20-60s)…", "loading");
  form.querySelector("button[type=submit]").disabled = true;
  try {
    const res = await fetch("/api/checklist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errText}`);
    }
    const json = await res.json();
    renderChecklist(json, outputDiv);
    setStatus("checklist-status", "Compliance check complete.", "success");
  } catch (err) {
    setStatus("checklist-status", err.message, "error");
  } finally {
    form.querySelector("button[type=submit]").disabled = false;
  }
});

document.getElementById("corrections-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const fd = new FormData(form);
  if (!fd.has("use_vision")) fd.set("use_vision", "false");
  else fd.set("use_vision", "true");
  const outputDiv = document.getElementById("corrections-output");
  outputDiv.innerHTML = "";
  setStatus("corrections-status", "Reading PDFs and generating response (60-120s)…", "loading");
  form.querySelector("button[type=submit]").disabled = true;
  try {
    const res = await fetch("/api/corrections", { method: "POST", body: fd });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errText}`);
    }
    const json = await res.json();
    renderCorrections(json, outputDiv);
    setStatus("corrections-status", "Response package generated.", "success");
  } catch (err) {
    setStatus("corrections-status", err.message, "error");
  } finally {
    form.querySelector("button[type=submit]").disabled = false;
  }
});
