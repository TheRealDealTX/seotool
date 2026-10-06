"""Markup and FAQs for the interactive renter tools. Behavior lives in
static/assets/js/tools.js, keyed by each page's data-tool attribute."""


def _num(name, label, value, prefix="$", step="1", suffix="", min_="0", hint=""):
    pre = f'<span class="affix">{prefix}</span>' if prefix else ""
    suf = f'<span class="affix">{suffix}</span>' if suffix else ""
    h = f"<small>{hint}</small>" if hint else ""
    return (f'<label class="field"><span>{label}</span><span class="input">{pre}'
            f'<input type="number" inputmode="decimal" name="{name}" value="{value}" min="{min_}" step="{step}">{suf}</span>{h}</label>')


def _range(name, label, value, lo, hi, step, fmt="%"):
    return (f'<label class="field"><span>{label} <output data-for="{name}"></output></span>'
            f'<input type="range" name="{name}" min="{lo}" max="{hi}" step="{step}" value="{value}" data-fmt="{fmt}"></label>')


TOOL_HTML = {
    "rent-affordability-calculator": f"""
<div class="calc">
  <form class="calc-in" data-form>
    <div class="seg" role="group" aria-label="Income period"><button type="button" class="is-on" data-period="year">Yearly income</button><button type="button" data-period="month">Monthly income</button></div>
    {_num("income", "Gross income (before tax)", 60000, step="100")}
    {_num("debts", "Monthly debt payments", 350, hint="Car, student loans, credit card minimums")}
    {_num("utilities", "Expected utilities per month", 150)}
    {_range("pct", "Share of income for housing", 30, 20, 50, 1)}
  </form>
  <div class="calc-out">
    <div class="gauge" data-gauge><svg viewBox="0 0 200 120" aria-hidden="true"><path class="g-track" d="M20 110 A80 80 0 0 1 180 110"/><path class="g-fill" d="M20 110 A80 80 0 0 1 180 110"/></svg>
      <div class="gauge-label"><small>Comfortable rent</small><strong data-out="rent">$0</strong><span data-out="rentNote"></span></div></div>
    <div class="result-rows">
      <div><span>30% rule</span><strong data-out="r30"></strong></div>
      <div><span>50/30/20 budget (needs share, after debts)</span><strong data-out="r5030"></strong></div>
      <div><span>Landlord 40× income test (max rent)</span><strong data-out="r40"></strong></div>
      <div><span>Debt-to-income with this rent</span><strong data-out="dti"></strong></div>
    </div>
    <p class="calc-note" data-out="advice"></p>
  </div>
</div>""",

    "rent-split-calculator": f"""
<div class="calc">
  <form class="calc-in" data-form>
    {_num("rent", "Total monthly rent", 2400)}
    {_num("utilities", "Shared utilities and internet", 220)}
    <div class="seg" role="group" aria-label="Split method"><button type="button" class="is-on" data-method="equal">Equal</button><button type="button" data-method="size">By room size</button><button type="button" data-method="income">By income</button></div>
    <div class="mates" data-mates></div>
    <button type="button" class="btn btn-ghost" data-add-mate>+ Add roommate</button>
  </form>
  <div class="calc-out">
    <h2 class="out-title">Monthly split</h2>
    <div class="split-bars" data-split></div>
    <p class="calc-note">Utilities are split evenly; rent follows the method you choose. Room size uses square feet (or any consistent unit); income uses each person's take-home pay.</p>
    <button type="button" class="btn" data-copy-result>Copy summary</button>
  </div>
</div>""",

    "rent-increase-calculator": f"""
<div class="calc">
  <form class="calc-in" data-form>
    {_num("current", "Current monthly rent", 1650)}
    {_num("proposed", "Proposed new rent", 1780)}
    {_num("cap", "Legal or lease cap (optional)", "", prefix="", suffix="%", step="0.1", hint="Leave blank if none applies. Many places have no cap.")}
    {_num("months", "Lease length", 12, prefix="", suffix="months")}
  </form>
  <div class="calc-out">
    <div class="big-num"><small>Increase</small><strong data-out="pct">0%</strong><span data-out="cmp"></span></div>
    <div class="result-rows">
      <div><span>Extra per month</span><strong data-out="month"></strong></div>
      <div><span>Extra over the lease</span><strong data-out="lease"></strong></div>
      <div><span>Max rent under your cap</span><strong data-out="capRent"></strong></div>
      <div><span>Income needed at 30% rule</span><strong data-out="income"></strong></div>
    </div>
    <div class="bar-compare" data-bars></div>
    <p class="calc-note">Before you sign: compare listings nearby, ask whether the landlord will match a longer lease at a lower increase, and check your state and city rules on notice periods and caps.</p>
  </div>
</div>""",

    "moving-cost-calculator": f"""
<div class="calc">
  <form class="calc-in" data-form>
    {_num("rent", "Monthly rent at the new place", 1800)}
    <label class="field"><span>Security deposit</span><select name="deposit"><option value="0">None</option><option value="0.5">Half a month</option><option value="1" selected>One month</option><option value="1.5">1.5 months</option><option value="2">Two months</option></select></label>
    <label class="check"><input type="checkbox" name="last"> Last month's rent due up front</label>
    {_num("appfee", "Application fees (all applications)", 100)}
    {_num("broker", "Broker or admin fee", 0)}
    {_num("pet", "Pet deposit or fee", 0)}
    <label class="field"><span>How are you moving?</span><select name="move"><option value="diy">DIY with a rental truck</option><option value="labor">Truck + hired loaders</option><option value="full">Full-service movers</option><option value="none">Friends / car only</option></select></label>
    <label class="field"><span>Home size</span><select name="size"><option value="0">Studio</option><option value="1" selected>1 bedroom</option><option value="2">2 bedrooms</option><option value="3">3+ bedrooms</option></select></label>
    {_num("miles", "Distance", 15, prefix="", suffix="miles")}
    {_num("utilities", "Utility deposits and setup", 150)}
    {_num("supplies", "Boxes, supplies, cleaning", 120)}
  </form>
  <div class="calc-out">
    <div class="big-num"><small>Cash needed to move in</small><strong data-out="total">$0</strong></div>
    <div class="donut-wrap"><svg class="donut" viewBox="0 0 42 42" data-donut aria-hidden="true"></svg><ul class="legend" data-legend></ul></div>
    <p class="calc-note">Moving-labor figures are rough planning ranges, not quotes. Get at least two written estimates and confirm every fee in your lease before you pay.</p>
  </div>
</div>""",

    "rent-vs-buy-calculator": f"""
<div class="calc">
  <form class="calc-in" data-form>
    {_num("rent", "Monthly rent", 1900)}
    {_range("rentGrowth", "Yearly rent increase", 3, 0, 8, 0.5)}
    {_num("price", "Home price", 350000, step="1000")}
    {_range("down", "Down payment", 10, 3, 30, 1)}
    {_range("rate", "Mortgage rate", 6.5, 3, 9, 0.125)}
    {_range("years", "Years you'll stay", 7, 1, 30, 1, "yr")}
    {_range("tax", "Property tax + insurance (yearly, % of price)", 2, 0.5, 4, 0.1)}
    {_range("maint", "Maintenance (yearly, % of price)", 1, 0, 3, 0.25)}
    {_range("appr", "Home value growth", 3, 0, 7, 0.5)}
    {_range("invest", "Investment return on savings", 6, 0, 10, 0.5)}
  </form>
  <div class="calc-out">
    <div class="big-num"><small data-out="verdictLabel">After 7 years</small><strong data-out="verdict"></strong><span data-out="gap"></span></div>
    <div class="line-chart" data-chart></div>
    <div class="result-rows">
      <div><span>Monthly mortgage payment (P&amp;I)</span><strong data-out="pmt"></strong></div>
      <div><span>Upfront cash to buy (down + ~3% closing)</span><strong data-out="upfront"></strong></div>
      <div><span>Renter's net worth at the end</span><strong data-out="rentNW"></strong></div>
      <div><span>Buyer's net worth at the end (after ~6% selling costs)</span><strong data-out="buyNW"></strong></div>
    </div>
    <p class="calc-note">The renter invests the down payment plus any month the rent is cheaper than owning. A simplified model: it ignores tax deductions, PMI and changing rates.</p>
  </div>
</div>""",

    "renters-insurance-calculator": """
<div class="calc">
  <form class="calc-in" data-form>
    <p class="calc-hint">Enter what it would cost to <strong>replace</strong> your things today. Leave a row at 0 if it doesn't apply.</p>
    <div class="inv" data-inventory></div>
    <label class="field"><span>Liability limit you want</span><select name="liability"><option value="100000">$100,000</option><option value="300000" selected>$300,000</option><option value="500000">$500,000</option></select></label>
  </form>
  <div class="calc-out">
    <div class="big-num"><small>Personal property coverage to ask for</small><strong data-out="cover">$0</strong><span data-out="raw"></span></div>
    <div class="room-bars" data-rooms></div>
    <ul class="checklist-out" data-advice></ul>
    <button type="button" class="btn btn-ghost" data-print>Print my inventory</button>
  </div>
</div>""",

    "lease-notice-calculator": f"""
<div class="calc">
  <form class="calc-in" data-form>
    <label class="field"><span>Lease end date</span><input type="date" name="end" required></label>
    {_num("days", "Notice required by your lease", 60, prefix="", suffix="days", hint="Check your lease. 30 or 60 days is common; local law may set a minimum.")}
    <label class="check"><input type="checkbox" name="month"> Notice must be given on the 1st of a month</label>
  </form>
  <div class="calc-out">
    <div class="big-num"><small>Give written notice by</small><strong data-out="deadline">—</strong><span data-out="left"></span></div>
    <div class="timeline" data-timeline></div>
    <div class="btn-row"><button type="button" class="btn" data-ics>Add reminder to calendar</button></div>
    <p class="calc-note">Send notice in the way your lease requires (often in writing), keep a copy, and get proof of delivery.</p>
  </div>
</div>""",

    "fire-safety-checklist": """
<div class="calc">
  <div class="calc-in">
    <div class="checklist" data-checklist></div>
  </div>
  <div class="calc-out sticky">
    <div class="ring" data-ring><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="r-track" cx="60" cy="60" r="52"/><circle class="r-fill" cx="60" cy="60" r="52"/></svg>
      <div class="ring-label"><strong data-out="score">0</strong><small>of 100</small></div></div>
    <p class="ring-grade" data-out="grade"></p>
    <h2 class="out-title">Fix these first</h2>
    <ol class="checklist-out" data-todo></ol>
    <div class="btn-row"><button type="button" class="btn btn-ghost" data-reset>Reset</button><button type="button" class="btn btn-ghost" data-print>Print</button></div>
    <p class="calc-note">Your answers stay in this browser. Based on guidance from the NFPA and the US Fire Administration.</p>
  </div>
</div>""",
}

TOOL_FAQ = {
    "rent-affordability-calculator": [
        ("What is the 30% rule for rent?", "A common guideline that housing costs should take no more than about 30% of your gross (pre-tax) income. Households that spend more than 30% are often described as cost-burdened."),
        ("What is the 40x rent rule?", "Many landlords require gross yearly income of at least 40 times the monthly rent. A $1,500 apartment would require about $60,000 a year. Some accept a guarantor or co-signer if you don't meet it."),
        ("Should I include utilities?", "Yes. Rent plus utilities is what you actually pay to live there, so the calculator subtracts your expected utilities from the housing budget."),
    ],
    "rent-split-calculator": [
        ("What is the fairest way to split rent?", "There is no single answer. Equal splits are simplest; splitting by room size is fair when bedrooms differ; splitting by income can make sense for couples or roommates with very different pay. Agree on the method in writing."),
        ("Should utilities be split by room size too?", "Most households split utilities evenly because usage is shared, which is what this calculator does."),
    ],
    "rent-increase-calculator": [
        ("Is there a limit on how much my rent can go up?", "It depends on where you live. A few states and some cities cap annual increases for some buildings; many places have no cap. Your lease also controls increases during its term. Check your state and city rules."),
        ("How much notice does a landlord have to give?", "Notice rules vary by state and sometimes by the size of the increase. Your lease may also set a notice period."),
    ],
    "moving-cost-calculator": [
        ("How much money do I need to move into an apartment?", "Often first month's rent plus a security deposit, application fees and moving costs, so two to three times the monthly rent is a common ballpark. Use the calculator for your own numbers."),
        ("Are application fees refundable?", "Usually not, though some states limit how much landlords can charge or require a refund if no screening was done. Ask before you apply."),
    ],
    "rent-vs-buy-calculator": [
        ("Is renting throwing money away?", "No. Renting buys housing plus flexibility and avoids the large costs of owning: interest, taxes, insurance, maintenance and the cost of buying and selling. Whether buying wins depends mainly on how long you stay and on prices and rates."),
        ("Why does how long I stay matter so much?", "Buying and selling costs are large one-time hits. The longer you stay, the more time appreciation and principal paydown have to make up for them."),
    ],
    "renters-insurance-calculator": [
        ("What does renters insurance cover?", "Typically your personal belongings, personal liability, and additional living expenses (loss of use) if a covered event like a fire makes your home uninhabitable. Your landlord's policy generally does not cover your belongings. Read our <a href=\"/news/renters-insurance-fire-coverage-loss-of-use/\">renters insurance guide</a>."),
        ("Replacement cost or actual cash value?", "Replacement cost pays to buy new items; actual cash value subtracts depreciation. Replacement cost policies cost a little more but pay out more after a loss."),
    ],
    "lease-notice-calculator": [
        ("What happens if I miss the notice deadline?", "Depending on your lease and state law, you may owe rent for an extra period or your lease could renew automatically. Read your lease carefully."),
        ("Does notice have to be in writing?", "Many leases require written notice. Keep a copy and proof of delivery."),
    ],
    "fire-safety-checklist": [
        ("How often should I test my smoke alarms?", "Fire safety agencies recommend testing smoke alarms monthly and replacing alarms that are 10 years old. Tell your landlord right away if an alarm is missing or does not work."),
        ("What should I do after an apartment fire?", "Read our <a href=\"/news/apartment-fire-first-72-hours-checklist/\">first-72-hours checklist</a> for displaced tenants."),
    ],
}
