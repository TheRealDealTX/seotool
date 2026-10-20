"""Attic Ventilation Calculator — IRC R806.2 net free area (1/150 and 1/300),
intake/exhaust split and vent counts.
Script: static/assets/js/tools/attic-ventilation-calculator.js
"""

from content.ui import num, select, seg, rng, group, prices

SLUG = "attic-ventilation-calculator"

form = (
    group("Attic",
          seg("area_mode", "Attic size", [("sqft", "I know the square footage"), ("dims", "Length × width")], "sqft"),
          num("attic_sqft", "Vented attic floor area", 2000, unit="sq ft", min=0, show="area_mode=sqft", cls="full",
              help="The ceiling area below the attic, not the roof area. Usually the heated footprint plus any garage that shares the attic."),
          num("att_len", "Attic length", 50, unit="ft", min=0, show="area_mode=dims"),
          num("att_wid", "Attic width", 40, unit="ft", min=0, show="area_mode=dims"),
          seg("rule", "Code ratio (IRC R806.2)",
              [("150", "1/150 standard"), ("300", "1/300 balanced")], "300",
              tip="1/300 is allowed when 40–50% of the vent area is high on the roof (within 3 ft of the ridge) and the rest is low intake. In climate zones 6–8 it also needs a Class I or II vapor retarder."),
          rng("intake_pct", "Intake share of total", 50, 30, 80, 5, "%",
              help="Exhaust gets the rest. 50/50 is balanced; more intake than exhaust is fine and often recommended."),
          ),
    group("Vent products",
          select("exhaust", "Exhaust (upper) vents",
                 [("ridge", "Ridge vent"), ("box", "Box / static vents"), ("turbine", "Turbine vents"), ("power", "Power attic fan")],
                 "ridge"),
          select("intake", "Intake (lower) vents",
                 [("soffit", "Continuous soffit vent"), ("soffit_ind", "Individual soffit vents"), ("edge", "Edge / fascia intake vent")],
                 "soffit"),
          num("ridge_len", "Ridge length available", 40, unit="ft", min=0, show="exhaust=ridge",
              help="Total ridge where a slot can be cut, stopping 6–12 in. short of ends and hip intersections."),
          num("fan_cfm", "Fan rating", 1200, unit="CFM", min=0, show="exhaust=power"),
          num("eave_len", "Eave length available", 120, unit="ft", min=0, show="intake=soffit|edge",
              help="Total length of eaves with open soffit or room for an edge vent."),
          ),
    prices("Vent specs (net free area)",
           num("ridge_nfa", "Ridge vent", 18, unit="sq in/ft", min=0,
               tip="Printed on the product. Most shingle-over ridge vents are 12.5–18 sq in per linear foot."),
           num("box_nfa", "Box / static vent", 50, unit="sq in each", min=0),
           num("turbine_nfa", "12 in. turbine", 110, unit="sq in each", min=0),
           num("soffit_nfa", "Continuous soffit", 9, unit="sq in/ft", min=0,
               tip="Perforated vinyl or aluminum soffit varies widely (about 4–10 sq in/ft). Check the panel's NFA rating."),
           num("soffit_ind_nfa", "16×8 soffit vent", 56, unit="sq in each", min=0),
           num("edge_nfa", "Edge / fascia intake", 9, unit="sq in/ft", min=0),
           num("cfm_per_sf", "Power fan sizing", 0.7, unit="CFM/sq ft", min=0, step="0.05"),
           num("cfm_per_intake", "Intake for power fans", 300, unit="CFM per sq ft NFA", min=1),
           note="Use the net free area (NFA) printed on the product label, not the opening size. Screens and louvers reduce it."),
)

body = """
<h2 id="how-it-works">How attic ventilation is sized</h2>
<p>Attic ventilation in the International Residential Code (IRC section R806.2) is sized by <strong>net free area</strong>
(NFA): the open area that air can actually move through once screens and louvers are taken out. The code sets a minimum
ratio of NFA to the vented attic floor area:</p>
<ul>
  <li><strong>1/150</strong>: 1 sq ft of NFA for every 150 sq ft of attic floor. This always satisfies the code.</li>
  <li><strong>1/300</strong>: half as much, allowed when the vents are balanced, with not less than 40% and not more than
  50% of the required area in the upper part of the attic (no more than 3 ft below the ridge, measured vertically) and
  the rest low, at the eaves. In climate zones 6, 7 and 8 the 1/300 option also requires a Class I or II vapor retarder
  on the warm side of the ceiling.</li>
</ul>
<p>The calculator converts the attic area to square inches, applies the ratio, splits the result between intake and
exhaust, and divides by the NFA of the products you pick to get linear feet or a vent count.</p>
<div class="formula">Total NFA (sq in)  = attic floor sq ft × 144 ÷ 150   (or ÷ 300 when balanced)
Exhaust NFA        = total × exhaust share          (40–50% for the 1/300 rule)
Intake NFA         = total − exhaust NFA
Ridge vent (ft)    = exhaust NFA ÷ NFA per ft       Box vents = exhaust NFA ÷ NFA each
Soffit vent (ft)   = intake NFA ÷ NFA per ft        Power fan CFM ≈ attic sq ft × 0.7</div>
<h3 id="worked-example">Worked example</h3>
<p>A 2,000 sq ft attic at 1/300 needs 2,000 × 144 ÷ 300 = 960 sq in of NFA: 480 sq in of exhaust and 480 sq in of
intake. With an 18 sq in/ft ridge vent that is 27 ft of ridge vent (480 ÷ 18 = 26.7), and with 9 sq in/ft continuous
soffit it is 54 ft of soffit vent. Using 50 sq in box vents instead of a ridge vent takes 10 vents. At 1/150 every
number doubles.</p>

<h2 id="texas">Why ventilation matters in Texas</h2>
<p>On a July afternoon an unvented or poorly vented attic under dark shingles in Dallas, Houston or San Antonio can run
well above 140°F. That heat bakes the shingles from below, cooks the asphalt and shortens the roof's life, and it
pushes heat back through the ceiling into the living space and the ductwork that usually runs through Texas attics.
Along the Gulf Coast, moving moist air out of the attic also helps keep the deck dry.</p>
<p>Ventilation is also a warranty issue. The major shingle manufacturers require attic ventilation that meets code (or
their own published guidelines) for the full limited warranty, and some reduce coverage when it does not. If you are
replacing a roof, the re-roof is the cheapest time to correct ventilation.</p>
<p>Most of Texas is in IECC climate zones 2 and 3, with the Panhandle in zone 4, so the climate-zone 6–8 vapor-retarder
condition on the 1/300 rule does not come into play here. Cities adopt different code editions and amendments, so
check local code before you rely on the 1/300 ratio.</p>

<h2 id="nfa-reference">Typical net free area by vent type</h2>
<div class="table-wrap"><table><thead><tr><th>Vent</th><th>Typical NFA</th><th>Position</th></tr></thead><tbody>
<tr><td>Shingle-over ridge vent</td><td>12.5–18 sq in per ft</td><td>Exhaust</td></tr>
<tr><td>Box / static (low-profile) vent</td><td>40–60 sq in each</td><td>Exhaust</td></tr>
<tr><td>12 in. turbine</td><td>about 110 sq in each</td><td>Exhaust</td></tr>
<tr><td>Power attic fan</td><td>Rated in CFM, not NFA</td><td>Exhaust</td></tr>
<tr><td>Continuous soffit strip or perforated soffit</td><td>4–10 sq in per ft</td><td>Intake</td></tr>
<tr><td>16 × 8 in. louvered soffit vent</td><td>about 56 sq in each</td><td>Intake</td></tr>
<tr><td>Edge / fascia intake vent</td><td>9–10 sq in per ft</td><td>Intake</td></tr>
</tbody></table></div>
<p>These are typical values. The NFA printed on the actual product is what counts, which is why every spec in the
calculator is editable.</p>

<h2 id="mistakes">Common ventilation mistakes</h2>
<ul>
  <li><strong>Mixing exhaust types.</strong> A ridge vent plus box vents, turbines or a gable fan on the same attic lets the
  exhaust vents pull air from each other instead of from the soffits. Use one type of exhaust per attic space.</li>
  <li><strong>Too little intake.</strong> Exhaust can only move what intake lets in. Intake should be at least equal to
  exhaust; when it is short, exhaust vents can pull conditioned air out of the house or draw rain through the ridge.</li>
  <li><strong>Blocked soffits.</strong> Insulation blown over the top plate often seals the soffit vents. Baffles (rafter
  vents) keep the air channel open.</li>
  <li><strong>Power fans with passive exhaust.</strong> A powered fan next to a ridge vent short-circuits: it pulls outside
  air in through the ridge. Power fans also need generous intake, roughly 1 sq ft of NFA per 300 CFM by common
  manufacturer guidance, or they depressurize the attic and pull air from the house.</li>
  <li><strong>Counting gable vents as upper vents.</strong> Gable louvers sit low on the end walls and are a poor partner
  for a ridge vent. Many installers close them off when a balanced soffit-and-ridge system goes in.</li>
</ul>

<h2 id="using-results">How to use the result</h2>
<p>Hand the linear feet and vent counts to your roofer, or check them against the vent lines on a contractor or insurance
estimate. On an insurance claim, code-required ventilation on a replaced roof is often covered as part of the code
upgrade if your policy has ordinance-or-law coverage; check your policy. The
<a href="/tools/shingle-calculator/">shingle &amp; materials calculator</a> puts the vents into a full material list, and
the <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a> prices the whole job.</p>
"""

faqs = [
    ("How much attic ventilation do I need?",
     "<p>At least 1 sq ft of net free area for every 150 sq ft of attic floor, or 1 per 300 when the vents are balanced "
     "between high exhaust (40–50%) and low intake. A 2,000 sq ft attic needs 960 sq in at 1/300 or 1,920 sq in at "
     "1/150.</p>"),
    ("What is the 1/300 rule for attic ventilation?",
     "<p>IRC R806.2 allows 1 sq ft of vent area per 300 sq ft of attic when 40–50% of the required area is in the upper "
     "portion of the attic, within 3 ft of the ridge, and the balance is low intake. In climate zones 6–8 it also "
     "requires a Class I or II vapor retarder on the ceiling. Check your local code edition.</p>"),
    ("How many feet of ridge vent do I need?",
     "<p>Divide the exhaust NFA by the ridge vent's NFA per foot. For a 2,000 sq ft attic at 1/300 with an 18 sq in/ft "
     "ridge vent, 480 sq in ÷ 18 = 27 ft. If your ridge is shorter than that, use a higher-NFA vent rather than adding "
     "another type of exhaust.</p>"),
    ("Can I use box vents and a ridge vent together?",
     "<p>Generally no. Shingle and vent manufacturers advise one type of exhaust per attic, because a mix lets the vents "
     "short-circuit each other. When converting to a ridge vent, the old box vents are usually removed and the holes "
     "decked over.</p>"),
    ("Should intake be more than exhaust?",
     "<p>Intake should be at least equal to exhaust. Slightly more intake is fine and is what many manufacturers "
     "recommend. Less intake than exhaust is the most common ventilation problem.</p>"),
    ("Does a power attic fan replace passive vents?",
     "<p>It replaces the exhaust side only, and it is sized in CFM, typically about 0.7 CFM per sq ft of attic floor. It "
     "still needs plenty of intake, and it should not run alongside a ridge vent or other passive exhaust.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Attic Ventilation Calculator (1/150 & 1/300) | Roof Estimate Pro",
    "description": "Free attic ventilation calculator. Net free area for the IRC 1/150 and 1/300 rules, intake/exhaust split, and feet of ridge and soffit vent or vent counts.",
    "h1": "Attic Ventilation Calculator",
    "lede": "Size attic ventilation to IRC R806.2: net free area for the 1/150 or balanced 1/300 rule, the intake and exhaust split, and how many feet of ridge and soffit vent or how many box vents, turbines or fans it takes.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["shingle-calculator", "roof-square-footage-calculator", "roof-replacement-cost-calculator"],
}
