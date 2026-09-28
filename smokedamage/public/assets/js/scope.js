/* Smoke Damage Scope Calculator — builds a documentation scope from answers.
   Runs entirely in the browser; nothing is sent anywhere. */
(function () {
  "use strict";
  var form = document.getElementById("scope-form");
  var out = document.getElementById("scope-result");
  if (!form || !out) return;
  var track = window.sdTrack || function () {};

  function val(name) {
    var el = form.elements[name];
    if (!el) return "";
    if (el.length !== undefined && el.tagName !== "SELECT" && el.tagName !== "INPUT") {
      for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value;
      return "";
    }
    return el.value || "";
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var COMMERCIAL = ["Office", "Retail", "Restaurant", "Warehouse", "Commercial", "Multifamily"];

  function build(a) {
    var areas = [], records = [], questions = [];
    var add = function (list, text, hi) { if (!list.some(function (x) { return x.t === text; })) list.push({ t: text, hi: !!hi }); };
    var yes = function (v) { return v === "Yes"; };
    var maybe = function (v) { return v === "Yes" || v === "Unsure"; };
    var level = function (v) { return { None: 0, Light: 1, Moderate: 2, Heavy: 3, Unsure: 1.5 }[v] || 0; };
    var commercial = COMMERCIAL.indexOf(a.ptype) > -1;
    var residential = !commercial && a.ptype !== "Other" && a.ptype !== "";
    var soot = level(a.soot), odor = level(a.odor);
    var exteriorOnly = a.origin === "Wildfire / exterior smoke" || a.origin === "Neighboring property";

    // Areas — the structure
    add(areas, "Walls — each affected room, including rooms away from the fire", soot >= 1 || odor >= 1);
    add(areas, "Ceilings — including ceiling texture and light fixtures", soot >= 1);
    add(areas, "Trim, baseboards and doors", soot >= 2);
    if (a.origin === "Kitchen" || a.origin === "Appliance" || soot >= 2) add(areas, "Cabinetry — interiors and exteriors", a.origin === "Kitchen");
    if (a.origin === "Kitchen" || a.origin === "Appliance") add(areas, "Countertops, backsplash and range hood", true);
    add(areas, "Flooring and carpet (including pad)", soot >= 2 || maybe(a.water));
    if (soot >= 1 || odor >= 1) add(areas, "Upholstery and soft furnishings", odor >= 2);
    if (soot >= 1 || odor >= 2) add(areas, "Window coverings — blinds, drapes and shades", false);
    if (maybe(a.hvac) || maybe(a.vents)) {
      add(areas, "HVAC system — air handler, filters and returns", yes(a.hvac));
      add(areas, "Supply registers and return grilles in every room", yes(a.vents));
      add(areas, "Ductwork (supply and return runs)", yes(a.hvac) && yes(a.vents));
    }
    if (a.origin === "Attic" || a.origin === "Electrical" || yes(a.flame) || soot >= 2 || yes(a.hvac)) {
      add(areas, "Attic space, framing and roof decking underside", a.origin === "Attic");
      add(areas, "Insulation (attic and any exposed wall cavities)", a.origin === "Attic" || yes(a.flame));
    }
    if (yes(a.flame) || a.flame === "Unsure") add(areas, "Direct fire and heat damage — framing, drywall, roofing, electrical", yes(a.flame));
    if (a.origin === "Garage") add(areas, "Garage structure, door and stored items", true);
    if (a.origin === "Fireplace") add(areas, "Fireplace surround, mantel, chimney area and adjoining walls", true);
    if (exteriorOnly || a.origin === "Garage" || yes(a.flame)) add(areas, "Exterior surfaces — siding, trim, soffits, fencing, outbuildings", exteriorOnly);
    if (maybe(a.water)) add(areas, "Water damage from fire suppression — drywall, insulation, flooring, lower cabinets", yes(a.water));
    if (yes(a.flame) || maybe(a.water)) add(areas, "Debris removal and any demolition already performed", false);

    // Areas — contents
    var c = { None: 0, Some: 1, Many: 2, Most: 3, Unsure: 1 }[a.contents] || 0;
    if (c > 0 || soot >= 2 || odor >= 2) {
      add(areas, "Electronics — TVs, computers, gaming, audio, small electronics", c >= 1);
      add(areas, "Appliances — kitchen and laundry", a.origin === "Kitchen" || a.origin === "Appliance");
      add(areas, "Furniture — upholstered and hard furniture", c >= 2);
      if (residential) {
        add(areas, "Clothing, shoes and accessories (closets and dressers)", c >= 2 || odor >= 2);
        add(areas, "Linens, bedding, towels and mattresses", odor >= 2);
        add(areas, "Books, papers, photos and media", false);
        add(areas, "Artwork, decor and collectibles", false);
        add(areas, "Kitchenware, dishes and pantry items", a.origin === "Kitchen");
        add(areas, "Children's items and toys", false);
      }
      add(areas, "Stored property — closets, garage, storage rooms", false);
    }
    if (commercial) {
      add(areas, "Business personal property and equipment", true);
      add(areas, "Inventory and stock (by location and SKU where possible)", c >= 1);
      add(areas, "Tenant improvements and fixtures", false);
      if (a.ptype === "Restaurant") add(areas, "Commercial kitchen equipment, hoods and food stock", true);
      if (a.ptype === "Multifamily") add(areas, "Common areas, corridors and each affected unit (unit-by-unit log)", true);
    }
    if (residential && (yes(a.flame) || soot >= 2 || odor >= 2 || maybe(a.water))) add(areas, "Temporary housing / additional living expenses (if the home is not livable)", yes(a.flame));
    if (commercial) add(areas, "Business income and extra operating expenses (where the policy provides it)", true);

    // Records
    add(records, "Your full insurance policy, including declarations page and endorsements", true);
    add(records, "Photos and video of every affected room — wide shots and close-ups", true);
    add(records, "Fire department incident number / report and any fire marshal information", yes(a.flame));
    add(records, "All letters and emails from the insurance company, and a log of calls", true);
    if (["Already inspected", "Partially paid", "Denied", "Delayed", "Underpaid", "Closed"].indexOf(a.status) > -1) {
      add(records, "The carrier's estimate(s) and any line-item scope", true);
      add(records, "Payment letters and explanation of payments", a.status === "Partially paid" || a.status === "Underpaid");
    }
    if (a.status === "Denied") add(records, "The denial letter and any policy provisions it cites", true);
    if (a.status === "Delayed") add(records, "Dates of every request, submission and response (a claim timeline)", true);
    if (maybe(a.hvac) || maybe(a.vents)) add(records, "HVAC service records and any inspection or cleaning reports", yes(a.vents));
    add(records, "Mitigation, cleaning or board-up invoices and scopes", maybe(a.water) || soot >= 2);
    if (c > 0) {
      add(records, "Contents inventory: item, quantity, brand/model, age, condition, replacement cost", true);
      add(records, "Receipts, credit card and bank statements, online order history", true);
      add(records, "Photos of items and labels / serial numbers", false);
    }
    if (residential) add(records, "Receipts for hotel, rent, meals, mileage and other extra living costs", yes(a.flame));
    if (commercial) {
      add(records, "Financial statements, sales records and payroll for the affected period", true);
      add(records, "Inventory records, invoices and equipment lists", true);
      add(records, "Lease and any tenant-improvement documents", false);
    }
    if (a.ptype === "Apartment / rental" || a.ptype === "Multifamily") add(records, "Leases, rent rolls and tenant notices", false);
    add(records, "Any engineer, hygienist, HVAC or restoration reports you've received", false);

    // Questions
    add(questions, "Which rooms and areas has the insurer's estimate included — and which has it left out?", true);
    if (odor >= 1) add(questions, "How is persistent odor being documented, and does anything need specialist input?", odor >= 2);
    if (maybe(a.hvac)) add(questions, "Has the HVAC system been evaluated, and is it reflected in the claim?", yes(a.hvac));
    if (c > 0) add(questions, "Which contents are being treated as cleanable versus non-salvageable, and on what basis?", true);
    add(questions, "Does the policy pay replacement cost or actual cash value, and how is depreciation handled?", c > 0);
    if (maybe(a.water)) add(questions, "Is water damage from firefighting documented alongside the smoke and fire damage?", false);
    if (residential) add(questions, "What does the policy provide for additional living expenses, and for how long?", yes(a.flame));
    if (commercial) add(questions, "Does the policy include business income or extra expense coverage, and what records are needed?", true);
    if (exteriorOnly) add(questions, "How will smoke that entered from an outside fire be documented for this property?", true);
    var statusQ = {
      "Not yet reported": ["What should I know before reporting the claim?", true],
      "New claim": ["What should happen before and during the insurer's inspection?", true],
      "Already inspected": ["Does the carrier's estimate match the conditions we documented?", true],
      "Partially paid": ["What was paid, what is still open, and is depreciation recoverable?", true],
      "Denied": ["What exactly is the stated basis for the denial, and what could a re-review consider?", true],
      "Delayed": ["What is the insurer waiting on, and what has already been provided?", true],
      "Underpaid": ["Which line items, rooms or contents differ from the documented damage?", true],
      "Closed": ["Can the claim be reopened or supplemented under the policy's terms?", true],
      "Unsure": ["Where does the claim actually stand today, and what are the next steps?", true]
    }[a.status];
    if (statusQ) add(questions, statusQ[0], statusQ[1]);
    add(questions, "Are there policy deadlines or conditions (proof of loss, repair timelines) to keep in mind?", false);

    return { areas: areas, records: records, questions: questions, commercial: commercial };
  }

  function list(items) {
    items = items.slice().sort(function (x, y) { return (y.hi ? 1 : 0) - (x.hi ? 1 : 0); });
    return "<ul>" + items.map(function (i) { return '<li class="' + (i.hi ? "hi" : "") + '">' + esc(i.t) + (i.hi ? ' <span class="sr-only">(priority)</span>' : "") + "</li>"; }).join("") + "</ul>";
  }
  function plain(title, items) { return title + "\n" + items.map(function (i) { return "- " + i.t + (i.hi ? " (priority)" : ""); }).join("\n"); }

  form.addEventListener("reset", function () { out.hidden = true; out.innerHTML = ""; });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var a = { ptype: val("ptype"), size: val("size"), rooms: val("rooms"), origin: val("origin"), flame: val("flame"), soot: val("soot"), odor: val("odor"),
      hvac: val("hvac"), vents: val("vents"), contents: val("contents"), water: val("water"), status: val("status") };
    var r = build(a);
    var summaryBits = [a.ptype || "Property", a.size ? Number(a.size).toLocaleString() + " sq ft" : "", a.rooms ? a.rooms + " affected rooms/areas" : "", a.origin ? "origin: " + a.origin : "", a.status ? "claim: " + a.status : ""].filter(Boolean);
    var date = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    out.innerHTML =
      '<div class="tool-card">' +
      '<div class="result-summary"><h3>Your Smoke Damage Documentation Scope</h3><p>' + esc(summaryBits.join(" · ")) + " — generated " + esc(date) + '. Bold items are likely priorities based on your answers.</p></div>' +
      '<div class="result-cols">' +
      '<div class="result-col"><h3>1. Areas to Document</h3>' + list(r.areas) + "</div>" +
      '<div class="result-col"><h3>2. Records to Gather</h3>' + list(r.records) + "</div>" +
      '<div class="result-col"><h3>3. Questions to Discuss During the Claim Review</h3>' + list(r.questions) + "</div>" +
      "</div>" +
      '<div class="tool-actions no-print">' +
      '<a class="btn" id="scope-review" href="#">Request a Free Claim Review</a>' +
      '<button class="btn btn-outline" type="button" id="scope-print">Print</button>' +
      '<button class="btn btn-outline" type="button" id="scope-pdf">Save as PDF</button>' +
      '<a class="btn btn-outline" id="scope-email" href="#">Email results</a>' +
      "</div>" +
      '<p class="disclaimer-box" style="margin-top:18px"><strong>Disclaimer</strong>This tool provides general organizational information only. It is not a coverage determination, a remediation recommendation, a health assessment, a structural assessment, a damage valuation, or legal advice.</p>' +
      "</div>";
    out.hidden = false;
    out.focus();
    out.scrollIntoView({ behavior: "smooth", block: "start" });
    track("calculator_complete", { tool: "scope", claim_status: a.status, property_type: a.ptype });

    var text = "SMOKE DAMAGE DOCUMENTATION SCOPE (" + date + ")\n" + summaryBits.join(" · ") + "\n\n" +
      plain("AREAS TO DOCUMENT", r.areas) + "\n\n" + plain("RECORDS TO GATHER", r.records) + "\n\n" + plain("QUESTIONS FOR THE CLAIM REVIEW", r.questions) +
      "\n\nGeneral organizational information only — not a coverage determination, remediation recommendation, health or structural assessment, damage valuation, or legal advice.\nSmokeDamage.com · +1 (844) 537-1427";
    var damage = [];
    if (a.soot && a.soot !== "None") damage.push("Soot");
    if (a.odor && a.odor !== "None") damage.push("Odor");
    if (a.flame === "Yes") damage.push("Fire");
    if (a.hvac === "Yes" || a.vents === "Yes") damage.push("HVAC");
    if (a.contents && a.contents !== "None") damage.push("Contents");
    if (a.water === "Yes") damage.push("Water From Fire Suppression");
    if (r.commercial) damage.push("Commercial Loss");
    damage.push("Smoke");
    var statusMap = { "Not yet reported": "Not Yet Filed", "New claim": "Claim Filed", "Already inspected": "Already Inspected", "Partially paid": "Partially Paid",
      "Denied": "Denied", "Delayed": "Delayed", "Underpaid": "Underpaid", "Closed": "Closed Claim", "Unsure": "Not Sure" };

    document.getElementById("scope-review").addEventListener("click", function (ev) {
      ev.preventDefault();
      var brief = "From the Smoke Damage Scope Calculator: " + summaryBits.join(", ") + ". Soot: " + (a.soot || "n/a") + "; odor: " + (a.odor || "n/a") + "; HVAC running: " + (a.hvac || "n/a") + "; contents affected: " + (a.contents || "n/a") + ".";
      try { sessionStorage.setItem("sd_scope_summary", brief); } catch (x) { /* ignore */ }
      track("calculator_to_form", { tool: "scope" });
      location.href = "/contact/?source=scope-calculator&status=" + encodeURIComponent(statusMap[a.status] || "") + "&damage=" + encodeURIComponent(damage.join(","));
    });
    document.getElementById("scope-print").addEventListener("click", function () { window.print(); });
    document.getElementById("scope-pdf").addEventListener("click", function () {
      alert("In the print window, choose “Save as PDF” as the destination.");
      window.print();
    });
    var mail = document.getElementById("scope-email");
    mail.href = "mailto:?subject=" + encodeURIComponent("My Smoke Damage Documentation Scope") + "&body=" + encodeURIComponent(text.slice(0, 1800));
    mail.addEventListener("click", function () { track("scope_email_self"); });
  });
})();
