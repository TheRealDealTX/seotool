"""Metal Roof Calculator — panel takeoff, trim, fasteners/clips and installed cost.

Script: static/assets/js/tools/metal-roof-calculator.js
"""

from content.ui import num, select, seg, switch, text, group, prices, rows
from siteconfig import TEXAS_REGIONS, US_REGIONS, WASTE

SLUG = "metal-roof-calculator"

PITCH_OPTS = [(0.25, "1/4 in 12"), (0.5, "1/2 in 12"), (1, "1/12"), (2, "2/12")] + \
             [(r, f"{r}/12" + (" (walkable)" if r <= 6 else " (steep)" if r <= 9 else " (very steep)")) for r in range(3, 15)]
REGION_OPTS = ([(r["key"], f"Texas — {r['name']}") for r in TEXAS_REGIONS]
               + [(r["key"], r["name"]) for r in US_REGIONS])
MW = WASTE["metal"]

plane_fields = (
    text("name", "Plane", autoname="Plane", row=True)
    + select("shape", "Shape", [("rect", "Rectangle"), ("tri", "Triangle (hip end)")], "rect", row=True)
    + num("eave", "Eave length", 40, unit="ft", min=0, row=True)
    + num("slope", "Slope length", 16, unit="ft", min=0, row=True)
    + num("n", "Identical", 1, min=1, step=1, row=True)
)

form = (
    group("Panel",
          select("panel", "Panel profile",
                 [("ss16", "Standing seam, 16 in"), ("ss12", "Standing seam, 12 in"), ("ss18", "Standing seam, 18 in"),
                  ("rpanel", "R-panel / PBR, 36 in"), ("5v", "5V crimp, 24 in")], "ss16", cls="full"),
          num("cov_in", "Coverage width", 16, unit="in", min=6, max=48,
              tip="Net width each panel covers after side laps. Refills when you change the profile; edit for other products."),
          seg("gauge", "Gauge", [(29, "29 ga"), (26, "26 ga"), (24, "24 ga")], 24, numeric=True, cls="",
              tip="Lower number = thicker steel. 24 ga is standard for residential standing seam; 26 or 29 ga for R-panel."),
          select("pitch", "Roof pitch", PITCH_OPTS, 6, numeric=True,
                 tip="Used for the minimum-slope check and the steep-roof labor adjustment."),
          num("overhang_in", "Overhang / hem allowance", 3, unit="in", min=0, max=24,
              help="Added to every panel's cut length for eave overhang and hems."),
          ),
    group("Roof size",
          seg("size_mode", "How do you want to size the roof?",
              [("planes", "Plane by plane"), ("total", "Total area")], "planes"),
          num("total_sf", "Roof area", 2400, unit="sq ft", min=0, show="size_mode=total"),
          num("panel_len", "Typical panel length", 16, unit="ft", min=1, show="size_mode=total",
              help="Eave-to-ridge length of a typical panel."),
          seg("complexity", "Roof complexity",
              [("simple", f"Simple ({MW['simple']}%)"), ("moderate", f"Some hips/valleys ({MW['moderate']}%)"),
               ("complex", f"Cut-up ({MW['complex']}%)")], "moderate", show="size_mode=total"),
          ),
    '<div data-show="size_mode=planes">',
    rows("planes", plane_fields, start=2, add_label="Add a roof plane",
         legend="Roof planes (eave length × eave-to-ridge slope length)"),
    '<p class="help" style="margin:-6px 0 16px">Use <em>Identical</em> for matching planes (two sides of a gable = 2). '
    'Split a hip-roof trapezoid into a rectangle (ridge length) plus one triangle whose base is the two corners together.</p></div>',
    group("Trim (linear feet)",
          num("eave_lf", "Eave", 124, unit="ln ft", min=0),
          num("rake_lf", "Rake / gable", 92, unit="ln ft", min=0),
          num("ridge_lf", "Ridge &amp; hip", 50, unit="ln ft", min=0),
          num("valley_lf", "Valley", 0, unit="ln ft", min=0),
          num("wall_lf", "Sidewall / endwall", 24, unit="ln ft", min=0),
          select("und", "Underlayment",
                 [("ht", "High-temp synthetic (10 sq / roll)"), ("htsa", "High-temp peel &amp; stick (2 sq / roll)"),
                  ("syn", "Standard synthetic (10 sq / roll)")], "ht", cls="full"),
          ),
    group("Labor & location",
          select("region", "Project location", REGION_OPTS, "dfw", cls="full"),
          switch("tear_on", "Include tear-off of existing roof", True),
          select("layers", "Layers to tear off", [(1, "1 layer"), (2, "2 layers"), (3, "3 layers")], 1, numeric=True,
                 show="tear_on=true"),
          ),
    prices("Edit unit prices & coverage",
           num("p_ss", "Standing seam panel (26 ga)", 3.60, pre="$", unit="/sf", min=0, step="0.01"),
           num("p_rpanel", "R-panel / PBR (26 ga)", 1.75, pre="$", unit="/sf", min=0, step="0.01"),
           num("p_5v", "5V crimp (26 ga)", 1.95, pre="$", unit="/sf", min=0, step="0.01"),
           num("g29", "29 ga multiplier", 0.85, unit="×", min=0, step="0.01"),
           num("g26", "26 ga multiplier", 1.00, unit="×", min=0, step="0.01"),
           num("g24", "24 ga multiplier", 1.30, unit="×", min=0, step="0.01"),
           num("trim_len", "Trim piece length", 10.5, unit="ft", min=1, step="0.5"),
           num("trim_lap", "Trim end lap", 4, unit="in", min=0),
           num("p_eave", "Eave trim", 18, pre="$", unit="/piece", min=0),
           num("p_rake", "Rake trim", 22, pre="$", unit="/piece", min=0),
           num("p_ridge", "Ridge / hip cap", 32, pre="$", unit="/piece", min=0),
           num("p_valley", "Valley", 38, pre="$", unit="/piece", min=0),
           num("p_wall", "Sidewall / endwall", 24, pre="$", unit="/piece", min=0),
           num("p_closure", "Foam / Z closure", 2.75, pre="$", unit="each", min=0, step="0.01"),
           num("p_ht", "High-temp synthetic", 135, pre="$", unit="/roll", min=0),
           num("cov_ht", "High-temp synthetic coverage", 10, unit="sq/roll", min=0.5),
           num("p_htsa", "High-temp peel &amp; stick", 150, pre="$", unit="/roll", min=0),
           num("cov_htsa", "Peel &amp; stick coverage", 2, unit="sq/roll", min=0.5),
           num("p_syn", "Standard synthetic", 95, pre="$", unit="/roll", min=0),
           num("cov_syn", "Standard synthetic coverage", 10, unit="sq/roll", min=0.5),
           num("screws_sq", "Panel screws per square", 80, min=0, step=1, tip="Exposed-fastener panels. Coastal high-wind designs often call for more."),
           num("p_screws", "Panel screws", 42, pre="$", unit="/bag of 250", min=0),
           num("clip_in", "Clip spacing", 24, unit="in", min=6, tip="Along each seam. Coastal wind designs often require 12 in or less near edges."),
           num("p_clip", "Standing seam clip", 0.65, pre="$", unit="each", min=0, step="0.01"),
           num("p_pancake", "Clip / trim screws", 30, pre="$", unit="/bag of 250", min=0),
           num("p_butyl", "Butyl tape (45 ft roll)", 12, pre="$", unit="/roll", min=0),
           num("p_sealant", "Tube sealant", 9, pre="$", unit="/tube", min=0),
           num("lab_ss", "Labor, standing seam", 420, pre="$", unit="/sq", min=0),
           num("lab_ef", "Labor, exposed fastener", 210, pre="$", unit="/sq", min=0),
           num("tear1", "Tear-off, first layer", 75, pre="$", unit="/sq", min=0),
           num("tear_add", "Each extra layer", 45, pre="$", unit="/sq", min=0),
           num("tax", "Sales tax on materials", 8.25, unit="%", min=0, max=15),
           num("op", "Overhead &amp; profit", 20, unit="%", min=0, max=60),
           note="Panel prices are per square foot of panel ordered (coverage width × cut length). Labor is scaled by pitch and region."),
)

body = """
<h2 id="how-it-works">How the metal roof calculator works</h2>
<p>Metal panels are ordered to length, one panel per coverage width, so a metal takeoff starts with the roof planes
rather than a single square-foot number. For each plane you enter the eave length and the slope length (eave to ridge),
and the calculator works out:</p>
<ol>
  <li><strong>Panels per plane</strong> = eave length ÷ panel coverage width, rounded up.</li>
  <li><strong>Cut length</strong> = slope length plus the overhang/hem allowance, rounded up to the inch.</li>
  <li><strong>Panel footage</strong> = panels × cut length × the number of identical planes. Triangular hip ends use
  half the footage plus one panel, because each diagonal cut leaves an offcut that fits the other side.</li>
  <li><strong>Trim</strong> is ordered in 10'6" pieces lapped about 4 inches, so each piece nets roughly 10'2".</li>
  <li><strong>Fasteners</strong> are figured per square for exposed-fastener panels, or as clips along every seam for
  standing seam.</li>
</ol>
<div class="formula">Panels       = ⌈eave length × 12 ÷ coverage width (in)⌉
Cut length   = slope length + overhang allowance
Panel sq ft  = panels × cut length × coverage width ÷ 12
Clips        = panels × (⌈cut length × 12 ÷ clip spacing⌉ + 1)
Screws       = squares × screws per square (exposed fastener)
Trim pieces  = ⌈trim ln ft ÷ (10.5 ft − end lap)⌉
Installed    = (materials + tax + labor × pitch × region + tear-off) × (1 + O&amp;P)</div>
<p>If you only know the total area, switch to <em>Total area</em>, give a typical panel length, and the calculator
adds a waste factor (5% simple, 8% with some hips and valleys, 12% cut-up) instead of counting each plane.</p>

<h2 id="panel-types">Standing seam vs. exposed fastener</h2>
<div class="table-wrap"><table><thead><tr><th>Profile</th><th>Coverage</th><th>Fastening</th><th>Typical minimum slope</th><th>Installed, Texas 2026</th></tr></thead><tbody>
<tr><td>Standing seam (snap-lock)</td><td>12–18 in</td><td>Concealed clips</td><td>3/12 (some 1/2:12, per manufacturer)</td><td>$1,100–$1,700/sq</td></tr>
<tr><td>Standing seam (mechanically seamed)</td><td>12–18 in</td><td>Concealed clips</td><td>1/4:12</td><td>Upper end of $1,100–$1,700/sq</td></tr>
<tr><td>R-panel / PBR</td><td>36 in</td><td>Exposed screws</td><td>1/2:12 with lap sealant; 3/12 without</td><td>$650–$950/sq</td></tr>
<tr><td>5V crimp</td><td>24 in</td><td>Exposed screws</td><td>About 3/12</td><td>$650–$950/sq</td></tr>
</tbody></table></div>
<p><strong>Exposed-fastener</strong> panels (R-panel, PBR, 5V) are screwed through the face into the deck or purlins.
They cost about half as much and go on fast, but every screw has a rubber washer that will dry out in the Texas sun.
Plan on checking and replacing screws every 10–15 years.</p>
<p><strong>Standing seam</strong> panels are held by clips hidden under the seams, so there are no holes through the
weather surface. The clips let each panel slide as it heats and cools. That is the main reason standing seam lasts
longer and costs more, and it is why its labor rate here is about double.</p>
<p>The building code sets the minimums: lapped, non-soldered panels need 3/12, or 1/2:12 with applied lap sealant, and
standing seam systems can go to 1/4:12. The panel manufacturer's own minimum controls if it is stricter. The
calculator warns you when your pitch is below the profile's typical limit.</p>

<h2 id="texas-hail">Texas hail: Class 4 metal and cosmetic damage exclusions</h2>
<p>Most metal panels carry a UL 2218 Class 4 impact rating, and many Texas insurers offer a premium discount for a
Class 4 roof. Class 4 means the panel resisted a 2-inch steel ball dropped in a lab without cracking through. It does
not mean the panel will not dent.</p>
<p>That matters because many Texas homeowner policies now carry a <em>cosmetic damage exclusion</em> (or a
cosmetic-damage endorsement) for metal roofs. Under that wording, hail dents that change the look of the roof but do
not let water in are not covered. Damage that affects function, such as punctures, split seams, cracked paint that
exposes steel or bent trim that lets water in, generally remains covered. The exact definition varies by carrier and
policy form, so read the declarations page and endorsements, or ask your agent, before you assume a dented metal roof
will be paid for.</p>
<div class="callout callout--peach"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>
<p><strong>Heavier gauge dents less.</strong> 24 gauge steel resists hail dents noticeably better than 26 or 29 gauge.
If your policy has a cosmetic exclusion, the extra cost of 24 gauge is the cheapest hail protection you can buy.</p></div>

<h2 id="heat">Texas heat, expansion and underlayment</h2>
<p>A dark metal roof in a Texas summer can reach 150–180°F on the surface. Steel grows about 1/8 to 3/16 inch over a
20-foot panel between a cool night and a hot afternoon, and far more over a long commercial run. Standing seam clips
and slotted trim fasteners let the metal move; exposed-fastener panels move against their screws, which is what
elongates the holes over time.</p>
<p>That heat also cooks the underlayment. Standard asphalt felt can soften and stick to the panels, so most standing
seam manufacturers call for a high-temperature underlayment rated around 240–260°F. It is good practice under
exposed-fastener panels too. Light colors and cool-roof (ENERGY STAR-rated) paints reduce attic heat. Kynar/PVDF
finishes hold their color far longer than SMP in Texas UV.</p>

<h2 id="using-results">Using the results</h2>
<p>The table gives a supplier-ready cut list: number of panels and cut length for each plane, plus trim pieces,
closures, clips or screws, butyl tape and underlayment rolls. Installed cost adds labor scaled for pitch and region,
optional tear-off, tax and overhead &amp; profit. If you need a full Xactimate-format metal roof estimate for a claim,
our <a href="/services/xactimate-roof-estimates/">estimating team</a> can build one from your measurements.</p>
"""

faqs = [
    ("How do I calculate how many metal roof panels I need?",
     "<p>Divide each roof plane's eave length (in inches) by the panel's coverage width and round up. A 40-foot eave with "
     "16-inch standing seam needs 30 panels; with 36-inch R-panel it needs 14. Each panel is cut to the slope length plus "
     "a few inches of overhang.</p>"),
    ("How much does a metal roof cost in Texas in 2026?",
     "<p>Exposed-fastener R-panel and 5V typically run $650–$950 per square installed, and standing seam $1,100–$1,700 "
     "per square, with tear-off. A 24-square house is roughly $16,000–$23,000 for R-panel and $27,000–$41,000 for "
     "standing seam.</p>"),
    ("How many screws per square for a metal roof?",
     "<p>About 70–90 panel screws per square for R-panel or 5V on purlins or deck, depending on the fastening pattern. "
     "Coastal high-wind designs can require more. Standing seam uses clips instead, typically every 24 inches along each "
     "seam.</p>"),
    ("What is the minimum pitch for a metal roof?",
     "<p>Lapped exposed-fastener panels need 3/12, or 1/2:12 with lap sealant; standing seam systems can go as low as "
     "1/4:12 if mechanically seamed. Snap-lock standing seam is commonly limited to 3/12. The manufacturer's minimum "
     "always controls.</p>"),
    ("Will insurance pay for hail dents on a metal roof in Texas?",
     "<p>It depends on your policy. Many Texas policies exclude cosmetic damage to metal roofs, meaning dents that do not "
     "affect the roof's ability to shed water. Functional damage is generally still covered. Read your endorsements or "
     "have us <a href=\"/services/insurance-claim-estimate-review/\">review the carrier's estimate</a>.</p>"),
    ("Can metal roofing go over shingles?",
     "<p>Often, yes, if the deck is sound, there is only one layer of shingles and local code allows it. Many installers "
     "add purlins or a slip sheet. Turn off tear-off in the calculator to price it that way, and check the panel "
     "manufacturer's requirements.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Metal Roof Calculator: Panels, Trim & Cost | Roof Estimate Pro",
    "description": "Free metal roof calculator: standing seam or R-panel counts and cut lengths, trim pieces, clips or screws, underlayment and installed cost at Texas 2026 prices.",
    "h1": "Metal Roof Calculator",
    "lede": "Plane-by-plane panel counts and cut lengths, trim in 10'6\" pieces, clips or screws, closures, high-temp underlayment and installed cost for standing seam, R-panel and 5V, with editable Texas 2026 prices.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-pitch-calculator", "roof-replacement-cost-calculator", "roof-insurance-claim-calculator"],
}
