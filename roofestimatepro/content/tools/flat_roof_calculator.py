"""Flat & Commercial Roof Calculator — low-slope systems, insulation and installed cost.

Script: static/assets/js/tools/flat-roof-calculator.js
Prices follow the shared low-slope ranges in the brief (Texas 2026, DFW baseline).
"""

from content.ui import num, select, seg, switch, text, group, prices, rows
from siteconfig import TEXAS_REGIONS, US_REGIONS

SLUG = "flat-roof-calculator"

# key, name, low, high ($/sf installed), service life
SYSTEMS = [
    ("tpo_ma", "TPO 60-mil, mechanically attached", 7.00, 10.00, "20–25 yrs"),
    ("tpo_fa", "TPO 60-mil, fully adhered", 8.00, 11.50, "20–25 yrs"),
    ("pvc", "PVC 60-mil", 9.00, 13.00, "25–30 yrs"),
    ("epdm_fa", "EPDM 60-mil, fully adhered", 7.00, 10.50, "25–30 yrs"),
    ("modbit", "Modified bitumen, 2-ply", 7.50, 11.00, "15–20 yrs"),
    ("bur", "Built-up roof (BUR)", 7.50, 11.50, "20–30 yrs"),
    ("silicone", "Silicone coating restoration", 3.50, 6.00, "10–15 yrs (renewable)"),
    ("acrylic", "Acrylic coating restoration", 2.75, 5.00, "8–12 yrs"),
]
MEMBRANES = "tpo_ma|tpo_fa|pvc|epdm_fa|modbit|bur"
COATINGS = "silicone|acrylic"
REGION_OPTS = ([(r["key"], f"Texas — {r['name']}") for r in TEXAS_REGIONS]
               + [(r["key"], r["name"]) for r in US_REGIONS])

section_fields = (
    text("name", "Section", autoname="Section", row=True)
    + num("l", "Length", 120, unit="ft", min=0, row=True)
    + num("w", "Width", 80, unit="ft", min=0, row=True)
    + num("a", "Or area", 0, unit="sq ft", min=0, row=True)
)

ROW_CSS = (
    "<style>"
    "[data-rows=sections]>.row-item{grid-template-columns:minmax(0,1.4fr) repeat(3,minmax(0,1fr)) 44px}"
    "@media (max-width:560px){[data-rows=sections]>.row-item{grid-template-columns:repeat(2,minmax(0,1fr))}"
    "[data-rows=sections]>.row-item>.field:first-child{grid-column:1/-1}"
    "[data-rows=sections]>.row-item>.row-del{justify-self:end}}"
    "</style>"
)

form = (
    ROW_CSS,    rows("sections", section_fields, start=1, add_label="Add a roof section",
         legend="Roof sections (length × width, or enter the area)"),
    group("Parapets & edges",
          num("par_lf", "Parapet walls", 280, unit="ln ft", min=0,
              help="Total length of walls that rise above the roof. Membrane runs up the wall and under the coping."),
          num("par_h", "Parapet height", 2, unit="ft", min=0, step="0.5"),
          num("edge_lf", "Roof edge without parapet", 120, unit="ln ft", min=0,
              help="Gets edge metal (drip edge / gravel stop) or gutter edge."),
          switch("coping", "New coping cap on parapets", True),
          ),
    group("Roof system",
          select("system", "System", [(k, n) for k, n, *_ in SYSTEMS], "tpo_ma", cls="full"),
          select("layers", "Existing layers to tear off", [(0, "None (recover)"), (1, "1 layer"), (2, "2 layers"), (3, "3 layers")],
                 1, numeric=True, show=f"system={MEMBRANES}"),
          select("ins_layers", "Polyiso insulation layers", [(0, "None"), (1, "1 layer"), (2, "2 layers"), (3, "3 layers")],
                 2, numeric=True, show=f"system={MEMBRANES}"),
          num("ins_in", "Thickness per layer", 2.2, unit="in", min=0, max=6, step="0.1", show=f"system={MEMBRANES}",
              help="Two layers of 2.2 in polyiso is about R-25."),
          select("cover", "Cover board", [("hdiso", "1/2 in HD polyiso"), ("gyp", "1/2 in gypsum"), ("none", "None")], "hdiso",
                 show=f"system={MEMBRANES}", tip="A cover board protects the insulation from foot traffic and hail."),
          switch("tapered", "Add tapered insulation for drainage", False, show=f"system={MEMBRANES}"),
          num("mils", "Coating thickness (dry)", 20, unit="mils", min=1, max=60, show=f"system={COATINGS}",
              help="Silicone is usually specified at 20–25 dry mils."),
          num("solids", "Volume solids", 96, unit="%", min=10, max=100, show=f"system={COATINGS}",
              help="From the product data sheet. Silicone ~90–96%, acrylic ~50–60%."),
          num("wet_pct", "Wet insulation to replace", 5, unit="%", min=0, max=100, show=f"system={COATINGS}",
              help="From a moisture survey. A coating must go over a dry roof."),
          ),
    group("Details & location",
          num("drains", "Drains &amp; scuppers", 4, min=0, step=1),
          num("pens", "Penetrations", 8, min=0, step=1, help="Pipes, curbs, vents and supports to flash."),
          num("crickets", "Crickets", 2, min=0, step=1, help="Tapered diverters behind curbs and between drains."),
          select("region", "Project location", REGION_OPTS, "dfw", cls="full"),
          ),
    prices("Edit unit prices & coverage",
           num("sys_price", "System, installed", 8.50, pre="$", unit="/sf", min=0, step="0.05",
               tip="Membrane or coating installed with labor and O&P, excluding tear-off and insulation. Refills at the midpoint of the range when you change systems."),
           num("lab_share", "Labor share of installed prices", 55, unit="%", min=0, max=100,
               tip="The regional factor is applied to this share of each installed price."),
           num("tear_price", "Tear-off, per layer", 2.25, pre="$", unit="/sf", min=0, step="0.05"),
           num("ins_price", "Polyiso, per inch thick", 1.10, pre="$", unit="/sf", min=0, step="0.05"),
           num("ins_r", "Polyiso R-value per inch", 5.7, min=0, step="0.1"),
           num("p_hdiso", "HD polyiso cover board", 0.85, pre="$", unit="/sf", min=0, step="0.05"),
           num("p_gyp", "Gypsum cover board", 1.05, pre="$", unit="/sf", min=0, step="0.05"),
           num("p_taper", "Tapered insulation (avg.)", 1.25, pre="$", unit="/sf", min=0, step="0.05"),
           num("roll_w", "Membrane roll width", 10, unit="ft", min=1, step="0.01"),
           num("roll_l", "Membrane roll length", 100, unit="ft", min=1, step="0.1"),
           num("overlap", "Seam overlap &amp; waste", 8, unit="%", min=0, max=40),
           num("board_sf", "Insulation board size", 32, unit="sf", min=1, tip="4×8 board = 32 sf; 4×4 = 16 sf."),
           num("fpb", "Fasteners per board, field", 8, min=0, step=1),
           num("fpb_perim", "Fasteners per board, perimeter/corner", 12, min=0, step=1),
           num("perim_pct", "Share of roof in perimeter/corner zones", 20, unit="%", min=0, max=100),
           num("ma_spacing", "Seam fastener spacing (MA)", 12, unit="in", min=3),
           num("adh_cov", "Bonding adhesive coverage", 60, unit="sf/gal", min=1,
               tip="Finished square feet of membrane per gallon, both surfaces coated."),
           num("wet_price", "Wet insulation replacement", 9.00, pre="$", unit="/sf", min=0, step="0.25"),
           num("p_drain", "Drain or scupper", 650, pre="$", unit="each", min=0),
           num("p_pen", "Penetration flashing", 175, pre="$", unit="each", min=0),
           num("p_edge", "Edge metal", 12, pre="$", unit="/ln ft", min=0),
           num("p_coping", "Coping cap", 18, pre="$", unit="/ln ft", min=0),
           num("p_cricket", "Cricket", 450, pre="$", unit="each", min=0),
           note="All prices are installed, Texas 2026, DFW baseline, including labor and contractor O&amp;P."),
)


def _systems_table():
    trs = "".join(f"<tr><td>{n}</td><td>${lo:.2f}–${hi:.2f}</td><td>${(lo + hi) / 2:.2f}</td><td>{life}</td></tr>"
                  for _, n, lo, hi, life in SYSTEMS)
    return ('<div class="table-wrap"><table><thead><tr><th>System</th><th>Installed $/sf</th><th>Calculator default</th>'
            f'<th>Typical service life</th></tr></thead><tbody>{trs}</tbody></table></div>')


body = f"""
<h2 id="how-it-works">How the flat roof calculator works</h2>
<p>Commercial and low-slope roofs are priced per square foot of roof, then built up layer by layer: tear-off,
insulation, cover board, the membrane or coating, and the details (wall flashing, drains, penetrations, edge metal
and crickets). This calculator follows that order and shows the material quantities a crew would load: membrane
rolls, insulation boards, fasteners and plates, adhesive or coating pails.</p>
<ol>
  <li><strong>Roof area</strong> is the sum of your sections. Add each wing or level as its own row.</li>
  <li><strong>Parapet flashing</strong> adds membrane area: wall length × (wall height + 1 ft for the field lap and
  the wrap over the top under the coping).</li>
  <li><strong>System price</strong> is applied to field plus flashing area. Insulation, cover board and tear-off are
  priced on the field area.</li>
  <li><strong>Region</strong> adjusts the labor share of each price (55% by default) for your part of Texas; tear-off
  is treated as all labor.</li>
</ol>
<div class="formula">Membrane area   = roof area + parapet length × (height + 1 ft)
Rolls           = ⌈membrane area × plies × (1 + overlap %) ÷ (roll width × roll length)⌉
R-value         = layers × inches × 5.7 (polyiso) + cover board
Boards          = ⌈roof area × 1.03 ÷ 32⌉ per layer (4×8)
Adhesive (gal)  = membrane area ÷ coverage (sf/gal)
Coating (gal)   = area × dry mils ÷ (1,604 × volume solids)
Installed price × (1 − labor share + labor share × region factor)</div>
<p>The 1,604 figure is a constant: one U.S. gallon spread over 1,604 sq ft makes a wet film 1 mil (0.001 in) thick.
Dividing by the volume solids converts wet film to the dry film the specification calls for. At 20 dry mils and 96%
solids, silicone takes about 1.3 gallons per square.</p>

<h2 id="systems">Low-slope roof systems compared</h2>
{_systems_table()}
<p><strong>TPO</strong> is the most common choice on Texas commercial roofs: white, heat-welded seams, and a
good price. Mechanically attached is cheapest; fully adhered costs more but is quieter in wind and better on
irregular decks. <strong>PVC</strong> costs more and resists grease and chemicals, so it is the usual pick for
restaurants. <strong>EPDM</strong> is a durable rubber with a long track record; black EPDM runs hot unless coated.
<strong>Modified bitumen</strong> and <strong>BUR</strong> are multi-ply asphalt systems that take foot traffic well
and are common on smaller buildings and older Texas strip centers.</p>

<h2 id="drainage">Drainage and ponding</h2>
<p>A "flat" roof should not be flat. The International Building Code requires a minimum slope of 1/4 inch per foot
(2%) for new low-slope roofs, and most membrane warranties exclude damage from ponding water, usually defined as water
still standing 48 hours after rain. A 40-foot run at 1/4 inch per foot drops 10 inches, which is why tapered
insulation and crickets are often the most valuable line on a commercial re-roof.</p>
<p>Count every drain, scupper and overflow. Parapet roofs need a secondary (overflow) drainage path sized for heavy
rain, a real consideration in Houston and the Gulf Coast. If the calculator sees parapets with no drains, it warns you.</p>

<h2 id="texas-heat">Texas heat, hail and reflectivity</h2>
<p>A black roof in a Texas summer can exceed 170°F; a clean white TPO, PVC or coating stays far cooler, cutting
cooling loads and slowing membrane aging. ENERGY STAR and Cool Roof Rating Council listings publish solar
reflectance numbers to compare products. Dirt lowers reflectivity over time, so wash white roofs every few years.</p>
<p>Hail is the other Texas factor. Thicker membranes (60 or 80 mil), a high-density cover board and fully adhered
attachment all improve hail resistance. If the old roof is torn off to the deck, the energy code generally calls for
current insulation levels, about R-25 continuous above the deck in most of Texas (climate zones 2–3) and R-30 in the
Panhandle (zone 4) under recent IECC editions. Local amendments and reroofing exceptions vary, so confirm with the
building official.</p>

<h2 id="restoration">Restoration vs. replacement</h2>
<p>A silicone or acrylic coating over a sound existing roof often costs half as much as a tear-off, adds a new
reflective surface and can usually be recoated later rather than torn off. It only works if the roof underneath is
dry and the deck is sound. Get an infrared or nuclear moisture survey first; wet insulation must be cut out and
replaced, which the calculator prices separately. As a rule of thumb, once more than about a quarter of the roof is
wet, replacement is the better value.</p>
<p>Silicone tolerates ponding better than acrylic; acrylic is cheaper but should only go on roofs that drain well.
Neither coating fixes structural ponding, and neither belongs on a roof with active deck damage.</p>

<div class="callout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Need a full commercial takeoff?</strong> Our <a href="/services/commercial-roof-estimates/">commercial roof
estimates</a> are built line by line from your measurements, core cuts and photos, in Xactimate.</p></div>
"""

faqs = [
    ("How much does a flat roof cost per square foot in Texas?",
     "<p>For 2026 in DFW, TPO runs about $7.00–$11.50 per sq ft installed, PVC $9.00–$13.00, EPDM $7.00–$10.50 and "
     "modified bitumen $7.50–$11.00, before tear-off ($1.50–$3.00 per sq ft per layer) and insulation. Coating "
     "restorations run $2.75–$6.00 per sq ft.</p>"),
    ("How many rolls of TPO do I need?",
     "<p>Divide the roof area plus wall flashing by the roll size and add 8–10% for seam overlap and waste. A 10×100 ft "
     "roll covers 1,000 sq ft, so a 9,600 sq ft roof with parapets needs about 11–12 rolls.</p>"),
    ("How do I calculate gallons of roof coating?",
     "<p>Gallons = area × dry mils ÷ (1,604 × volume solids). A 10,000 sq ft roof at 20 dry mils of 96%-solids silicone "
     "needs about 130 gallons, or 26 five-gallon pails, plus a little for laps and detail work.</p>"),
    ("What R-value does a commercial roof need in Texas?",
     "<p>Under recent IECC editions, insulation entirely above the deck is about R-25 continuous in most of Texas and "
     "R-30 in the Panhandle. Polyiso is about R-5.7 per inch, so R-25 takes roughly 4.4 inches. Local code and "
     "reroofing exceptions vary.</p>"),
    ("Is a roof coating as good as a new roof?",
     "<p>Not as a replacement for a failed roof. A coating restores a sound, dry roof for 8–15 years and can be "
     "renewed. If the insulation is widely wet or the deck is damaged, replacement is the better value.</p>"),
    ("What is the minimum slope for a flat roof?",
     "<p>New low-slope roofs need at least 1/4 inch per foot (2%) under the building code, achieved with framing or "
     "tapered insulation. Water standing more than 48 hours is considered ponding and is often excluded from warranties.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Flat Roof Calculator: TPO, EPDM & Coatings | Roof Estimate Pro",
    "description": "Free flat roof calculator for TPO, PVC, EPDM, mod-bit, BUR and coatings: rolls, insulation boards, R-value, fasteners and installed cost at Texas 2026 prices.",
    "h1": "Flat & Commercial Roof Calculator",
    "lede": "Price a low-slope roof layer by layer: tear-off, polyiso insulation and R-value, cover board, membrane or coating, parapet flashing, drains and edge metal, with rolls, boards, fasteners and adhesive counted for you.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-square-footage-calculator", "roof-replacement-cost-calculator", "roofing-bid-calculator"],
}
