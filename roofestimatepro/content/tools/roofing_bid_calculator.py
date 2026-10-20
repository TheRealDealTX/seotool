"""Roofing Bid & Profit Calculator — for contractors: direct costs, overhead,
markup or margin, commission, card/financing fees and warranty reserve to a
bid price, price per square and break-even.
Script: static/assets/js/tools/roofing-bid-calculator.js
"""

from content.ui import num, seg, group, prices

SLUG = "roofing-bid-calculator"

form = (
    group("Job size",
          num("squares", "Roof size", 30, unit="squares", min=0, step=0.1,
              help="Squares of roof (100 sq ft each), not including waste. Used for price per square."),
          ),
    group("Direct job costs",
          num("c_mat", "Materials (incl. sales tax)", 6600, pre="$", min=0, step=1,
              tip="Shingles or panels, underlayment, accessories, flashing, fasteners and delivery, with Texas sales tax."),
          num("c_lab", "Labor (crew or sub)", 4800, pre="$", min=0, step=1,
              tip="Install and tear-off labor, plus payroll burden if you use your own crew."),
          num("c_dump", "Dump / disposal", 650, pre="$", min=0, step=1),
          num("c_equip", "Equipment rental", 300, pre="$", min=0, step=1,
              help="Dumpster, lift, roof loader, fall protection."),
          num("c_permit", "Permits & inspections", 350, pre="$", min=0, step=1),
          num("c_misc", "Misc. & subcontractors", 500, pre="$", min=0, step=1,
              help="Gutters, carpentry, skylights, HVAC flashings, cleanup."),
          ),
    group("Overhead",
          seg("oh_mode", "How do you allocate overhead?",
              [("pct", "% of direct cost"), ("annual", "Annual overhead ÷ jobs")], "pct"),
          num("oh_pct", "Overhead rate", 12, unit="% of cost", min=0, max=100, step=0.5, show="oh_mode=pct",
              tip="Office, insurance, vehicles, salaries not tied to one job, marketing, software."),
          num("oh_annual", "Annual overhead", 300000, pre="$", min=0, step=100, show="oh_mode=annual"),
          num("oh_jobs", "Jobs per year", 120, min=1, step=1, show="oh_mode=annual"),
          ),
    group("Profit & selling costs",
          seg("p_mode", "Profit target entered as",
              [("margin", "Net margin (% of price)"), ("markup", "Markup (% of cost)")], "margin",
              tip="Margin is profit as a share of the selling price. Markup is profit as a share of your cost."),
          num("profit", "Desired net profit", 10, unit="%", min=0, max=80, step=0.5),
          num("commission", "Sales commission", 8, unit="% of price", min=0, max=50, step=0.5),
          num("fees", "Financing / card fees", 0, unit="% of price", min=0, max=20, step=0.1,
              help="Card processing is often about 3%; dealer fees on financed jobs run much higher."),
          num("warranty", "Warranty reserve", 1, unit="% of price", min=0, max=10, step=0.1),
          ),
    prices("Sensitivity table margins",
           num("s1", "Margin 1", 15, unit="%", min=0, max=90),
           num("s2", "Margin 2", 20, unit="%", min=0, max=90),
           num("s3", "Margin 3", 25, unit="%", min=0, max=90),
           num("s4", "Margin 4", 30, unit="%", min=0, max=90),
           num("s5", "Margin 5", 35, unit="%", min=0, max=90),
           cols=3,
           note="Gross margin targets (price minus direct costs, as a % of price) shown in the sensitivity table."),
)

body = """
<h2 id="how-it-works">How this roofing bid calculator works</h2>
<p>The calculator builds a bid from the bottom up, the way most roofing contractors price a retail job:</p>
<ol>
  <li><strong>Direct costs</strong> are everything this job would not have without the job: materials with tax, labor,
  disposal, equipment, permits and subcontractors.</li>
  <li><strong>Overhead</strong> is the cost of running the company: office, insurance, vehicles, non-job salaries,
  marketing and software. Allocate it either as a percentage of direct cost or as your annual overhead divided by the
  number of jobs you expect to complete in a year.</li>
  <li><strong>Selling costs</strong> scale with the contract price: sales commission, card or financing fees and a
  warranty reserve.</li>
  <li><strong>Net profit</strong> is what is left after all of the above. Enter it as a margin (share of the price) or
  as a markup (share of your cost).</li>
</ol>
<div class="formula">Cost base C   = direct costs + overhead
Selling costs = (commission % + fees % + warranty %) × price
Margin mode:  price = C ÷ (1 − selling % − net margin %)
Markup mode:  price = C × (1 + markup %) ÷ (1 − selling %)
Break-even    = C ÷ (1 − selling %)</div>
<p>Because commission and fees are a share of the final price, the calculator solves for the price instead of adding
them on top. Adding 8% commission to a finished price leaves you short, because the commission is then paid on the
commission too.</p>

<h2 id="markup-vs-margin">Markup vs. margin</h2>
<p>Markup is profit divided by cost. Margin is profit divided by price. The same dollars of profit give a smaller
margin than markup, and confusing the two is one of the most common reasons roofing companies underprice work.</p>
<div class="table-wrap"><table><thead><tr><th>Markup on cost</th><th>Equals margin on price</th><th>Price on $10,000 cost</th></tr></thead><tbody>
<tr><td>10%</td><td>9.1%</td><td>$11,000</td></tr>
<tr><td>20%</td><td>16.7%</td><td>$12,000</td></tr>
<tr><td>25%</td><td>20.0%</td><td>$12,500</td></tr>
<tr><td>33.3%</td><td>25.0%</td><td>$13,333</td></tr>
<tr><td>42.9%</td><td>30.0%</td><td>$14,286</td></tr>
<tr><td>50%</td><td>33.3%</td><td>$15,000</td></tr>
<tr><td>66.7%</td><td>40.0%</td><td>$16,667</td></tr>
</tbody></table></div>
<div class="formula">Margin = markup ÷ (1 + markup)        Markup = margin ÷ (1 − margin)</div>
<p>If you want a 30% margin, you cannot add 30% to your cost; that only gives 23.1%. You need to divide cost by 0.70,
which is a 42.9% markup.</p>

<h3 id="op-convention">Insurance "10 and 10" overhead &amp; profit</h3>
<p>On insurance work, Xactimate-style estimates add 10% overhead and 10% profit, each calculated on the line-item
subtotal, for 20% of cost. That is a 20% markup, or a 16.7% margin, before commission. If you instead compound them
(10% overhead on cost, then 10% profit on cost plus overhead), you get 1.10 × 1.10 = 1.21, a 21% markup.</p>
<p><strong>This calculator compounds.</strong> In markup mode, overhead is added to direct cost first and the markup is
applied to direct cost plus overhead. Set overhead to 10% and markup to 10% with no selling costs and the price is
exactly 1.21 × direct cost. To reproduce the insurance convention (20% on cost, not compounded), set overhead to 0%
and markup to 20%.</p>
<p>Whether O&amp;P is owed on a claim, and on which trades, depends on the policy and the job. A roof-only claim often
gets O&amp;P only when a general contractor is reasonably needed to coordinate several trades. Our
<a href="/tools/roof-insurance-claim-calculator/">insurance claim calculator</a> shows how O&amp;P affects the check.</p>

<h2 id="typical-margins">Typical roofing overhead and margins</h2>
<p>There is no single right number; these are commonly reported ranges for residential roofing companies, and your
own books should set yours:</p>
<div class="table-wrap"><table><thead><tr><th>Measure</th><th>Typical range</th></tr></thead><tbody>
<tr><td>Overhead (% of revenue)</td><td>10–20%; higher for companies with sales teams and heavy marketing</td></tr>
<tr><td>Gross margin (price minus direct job costs)</td><td>25–45% on retail re-roofs</td></tr>
<tr><td>Net profit margin</td><td>5–15%; storm-restoration years can run higher or lower</td></tr>
<tr><td>Sales commission</td><td>About 5–12% of contract price, or a split of gross profit</td></tr>
<tr><td>Card processing</td><td>About 2.5–3.5% of the amount charged</td></tr>
</tbody></table></div>
<p>The safest way to set overhead is from last year's books: total overhead divided by total revenue, or divided by the
number of jobs completed. A company that does 120 jobs with $300,000 of overhead needs $2,500 from every job before it
earns anything.</p>

<h2 id="price-per-square">Price per square in Texas</h2>
<p>Price per square is the number homeowners and adjusters compare, so check it before you send the bid. For 2026, most
Texas retail bids for architectural shingles fall around $450–$650 per square installed with one layer of tear-off,
Class 4 impact-resistant shingles about $550–$800 and standing seam metal about $1,100–$1,700. Labor rates vary by
region and spike in the months after a large hail event. If your price per square lands well above the market range,
look at overhead per job and commission before you cut margin; if it lands well below, check that disposal, permits,
decking allowances and drip edge are in your direct costs.</p>
<p>To build the direct cost side, use the <a href="/tools/shingle-calculator/">shingle &amp; materials calculator</a> for a
material takeoff and the <a href="/tools/roof-replacement-cost-calculator/">replacement cost calculator</a> for a
full itemized retail estimate. If you want an Xactimate-format estimate built for an insurance job, see
<a href="/services/xactimate-roof-estimates/">Xactimate roof estimates</a>.</p>

<div class="callout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
<p><strong>Know your break-even price.</strong> It is the lowest price that pays every cost, including overhead and
commission, with zero profit. Never discount below it to win a job.</p></div>
"""

faqs = [
    ("What is the difference between markup and margin in roofing?",
     "<p>Markup is profit as a percentage of cost; margin is profit as a percentage of the selling price. A 20% markup "
     "gives a 16.7% margin, and a 30% margin needs a 42.9% markup. Margin = markup ÷ (1 + markup).</p>"),
    ("What profit margin should a roofing company make?",
     "<p>Commonly reported ranges for residential roofing are roughly 25–45% gross margin and 5–15% net profit after "
     "overhead. Your own overhead, sales model and market set the right number; use last year's books.</p>"),
    ("How do I calculate overhead per roofing job?",
     "<p>Divide annual overhead (everything not tied to a specific job) by the number of jobs you complete in a year, or "
     "by annual direct costs to get a percentage. $300,000 over 120 jobs is $2,500 per job.</p>"),
    ("Is 10 and 10 overhead and profit 20% or 21%?",
     "<p>In Xactimate-style insurance estimates, 10% overhead and 10% profit are each figured on the subtotal, so it is "
     "20% of cost. If profit is figured on cost plus overhead, it compounds to 21%. This calculator compounds; set "
     "overhead to 0% and markup to 20% to match the insurance convention.</p>"),
    ("Why does commission change the price so much?",
     "<p>Commission is paid on the final contract price, so it has to be built into the price rather than added on top. "
     "At 8% commission, every $1 of cost and profit needs about $1.087 of price.</p>"),
    ("What is a good price per square for a roof in Texas?",
     "<p>For 2026, most Texas retail bids for architectural shingles fall around $450–$650 per square installed with "
     "tear-off. Class 4 shingles run about $550–$800 and standing seam metal $1,100–$1,700.</p>"),
]

TOOL = {
    "slug": SLUG,
    "title": "Roofing Bid Calculator: Markup vs Margin | Roof Estimate Pro",
    "description": "Free roofing bid calculator for contractors: overhead, markup vs margin, commission, card fees and warranty reserve to a bid price and price per square.",
    "h1": "Roofing Bid & Profit Calculator",
    "lede": "Price a roofing job from direct costs up: overhead, markup or margin, sales commission, card fees and warranty reserve, solved to a bid price, price per square and break-even, with a margin sensitivity table.",
    "form": form,
    "body": body,
    "faqs": faqs,
    "related": ["roof-replacement-cost-calculator", "shingle-calculator", "roof-insurance-claim-calculator"],
}
