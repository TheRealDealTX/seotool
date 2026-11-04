"""Homepage. Primary keyword / brand: "Enforce Interest" (used 14+ times in body copy)."""
import lib
from lib import (FLOAT_RATE_S, JUDG_RATE_S, RATE_MONTH, FLOAT_RATE, btn, cite, icon, sec_head, faq_block,
                 cta_band, disclaim, money, interest, FIRM, LICENSE, esc)
from content import art, products

TITLE = "Enforce Interest | Texas 60-Day Rule & 18% Late Claim Interest"
DESC = ("Enforce Interest helps Texas policyholders recover statutory interest when an insurer pays a property claim "
        "late: 18% a year under §542.060, or the floating weather-claim rate. Free claim review.")


def build(ctx, post_pages):
    s50_18 = interest(50000, 18, 90)
    s50_fl = interest(50000, FLOAT_RATE, 90)
    hin = interest(100000, 18, 548)

    ticker_items = [
        ("§542.055", "15 days to acknowledge, investigate &amp; request items"),
        ("§542.056", "15 business days to accept or reject"),
        ("§542.057", "5 business days to pay once accepted"),
        ("§542.058", "60 days to pay after receiving what it asked for"),
        ("§542.060(a)", "18% a year, plus attorney&rsquo;s fees"),
        ("§542.060(c)", f"{FLOAT_RATE_S} for weather claims ({RATE_MONTH})"),
        ("Hinojos (Tex. 2021)", "appraisal payment doesn&rsquo;t erase the delay"),
        ("§542A.003", "61-day pre-suit notice on weather claims"),
        ("§4102.104", "public adjuster fees capped at 10%"),
    ]
    tick = "".join(f"<span><b>{a}</b>{b}</span>" for a, b in ticker_items)

    faqs = [
        ("What is Enforce Interest?",
         f"<p>Enforce Interest is a {FIRM} service built around one part of Texas law: the prompt-payment rules in "
         "Chapter 542 of the Texas Insurance Code. When a carrier pays a covered property claim late, §542.060 adds "
         "statutory interest as damages. We rebuild the claim timeline, calculate that interest and present it to the "
         "carrier on the policyholder&rsquo;s behalf.</p>"),
        ("What is the Texas 60-day rule?",
         "<p>Under Tex. Ins. Code §542.058, once an insurer has received all the items, statements and forms it "
         "reasonably requested, it generally has 60 days to pay a covered claim (unless another statute sets a different "
         "period). If it delays longer, it owes the damages in §542.060: interest on the claim amount plus reasonable "
         "and necessary attorney&rsquo;s fees.</p>"),
        ("How much interest does a Texas insurer owe for paying late?",
         f"<p>For most claims, 18% a year, simple interest, on the amount that was paid late. For weather-related property "
         f"claims made on or after September 1, 2017 (in an action governed by Chapter 542A), the rate is the Finance Code "
         f"§304.003 judgment rate plus 5%. The {RATE_MONTH} judgment rate is {JUDG_RATE_S}, which makes the weather rate "
         f"{FLOAT_RATE_S}. In a lawsuit, that rate is fixed on the date of judgment.</p>"),
        ("Does paying an appraisal award end the insurer&rsquo;s liability for interest?",
         "<p>No, not automatically. In <em>Barbara Technologies Corp. v. State Farm Lloyds</em> (Tex. 2019) and "
         "<em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651 (Tex. 2021), the Texas Supreme Court held that paying an "
         "appraisal award does not, by itself, protect an insurer from prompt-payment damages. If money was owed and "
         "unpaid when the statutory deadline passed, interest can be owed on it even though the award was later paid.</p>"),
        ("Do I need a lawyer to recover prompt-payment interest?",
         "<p>Not always. Many carriers resolve the issue once the dates and the math are documented and presented. If a "
         "carrier refuses and a lawsuit is needed, that is work for a licensed Texas attorney; Enforce Interest is not a "
         "law firm and does not give legal advice.</p>"),
        ("What does it cost?",
         "<p>The first claim review is free. If we take the engagement, the fee is a contingency percentage of what is "
         "recovered, and Texas law caps public adjuster compensation at 10% of the insurance settlement on the claim "
         "(§4102.104). If nothing is recovered, you owe nothing.</p>"),
    ]
    faq_html, faq_ld = faq_block(faqs)

    latest = sorted(post_pages, key=lambda p: p["published"], reverse=True)[:3]

    def body():
        pic = ctx["pic"]
        cards_blog = "".join(
            f'<a class="card post-card" href="{p["path"]}"><div class="pc-img">{pic(p["og"], p["h1_plain"])}</div>'
            f'<div class="pc-body"><span class="tag wine">{p["section"]}</span><h3 style="margin-top:12px">{p["h1"]}</h3>'
            f'<p>{esc(p["desc"])}</p><span class="meta">{p["read"]} min read</span></div></a>' for p in latest)
        return f'''
<section class="hero-home dark">
  <div class="hero-sect" aria-hidden="true" data-parallax="0.25">§</div>
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Texas Insurance Code &middot; Chapter 542</span>
      <h1><span class="line">Paid late?</span><span class="line"><em class="underline-draw">Enforce Interest</em></span><span class="line">on every day of delay.</span></h1>
      <p class="lede">Texas gives insurers a deadline to pay covered property claims. When they miss it, §542.060 adds
      statutory interest &mdash; 18% a year on most claims. Enforce Interest rebuilds your claim timeline, calculates what
      the delay is worth and presents it to the carrier. Most policyholders never hear the word.</p>
      <div class="btn-row">{btn("/statutory-damages-calculator/", "Calculate what you&rsquo;re owed", "gold")}{btn("/contact/", "Free claim review", "ghost", arrow=False)}</div>
      <div class="hero-meta">
        <div><b>18%</b>a year, §542.060(a)</div>
        <div><b>{FLOAT_RATE_S}</b>weather rate, {RATE_MONTH}</div>
        <div><b>60 days</b>to pay, §542.058</div>
      </div>
      {disclaim()}
    </div>
    <div data-reveal="right">
      <div class="accrual" id="accrual" data-amount="50000" data-days="90">
        <div class="accrual-top"><span class="live">Interest accruing</span><span class="cite">§542.060</span></div>
        <div class="ring-wrap">
          <div class="ring">
            <svg viewBox="0 0 150 150" aria-hidden="true"><defs><linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c9a24f"/><stop offset="1" stop-color="#e2c27a"/></linearGradient></defs>
              <circle class="track" cx="75" cy="75" r="64" fill="none" stroke-width="10"/>
              <circle class="fill" cx="75" cy="75" r="64" fill="none" stroke-width="10" stroke-dasharray="402.1" stroke-dashoffset="402.1"/>
              <circle class="over" cx="75" cy="75" r="52" fill="none" stroke-width="5" stroke-dasharray="326.7" stroke-dashoffset="326.7"/></svg>
            <div class="ring-label"><b data-ring-day>0</b><span>days late</span></div>
          </div>
          <div>
            <div class="accrual-amt" data-acc-amt>$0<small>.00</small></div>
            <div class="accrual-sub">owed on top of a <b data-acc-claim>$50,000</b> claim</div>
          </div>
        </div>
        <div class="accrual-rows">
          <div><span>Penalty rate</span><b data-acc-rate>18.00% / yr</b></div>
          <div><span>Per-day accrual</span><b data-acc-day>$24.66</b></div>
          <div><span>Days past the deadline</span><b><input type="range" min="0" max="730" value="90" data-acc-slider aria-label="Days past the payment deadline" style="width:120px;accent-color:#c9a24f;vertical-align:middle"></b></div>
        </div>
        <div class="accrual-ctrl" role="group" aria-label="Rate">
          <button type="button" data-rate="18" aria-pressed="true">18% standard</button>
          <button type="button" data-rate="{FLOAT_RATE:.2f}" aria-pressed="false">{FLOAT_RATE_S} weather</button>
        </div>
        <div class="accrual-ctrl" role="group" aria-label="Claim amount">
          <button type="button" data-amt="25000" aria-pressed="false">$25k</button>
          <button type="button" data-amt="50000" aria-pressed="true">$50k</button>
          <button type="button" data-amt="100000" aria-pressed="false">$100k</button>
          <button type="button" data-amt="250000" aria-pressed="false">$250k</button>
        </div>
        <div class="accrual-foot">Simple interest &middot; amount &times; rate &divide; 365 &times; days late &middot; illustration only</div>
      </div>
    </div>
  </div>
</section>
<div class="ticker" aria-label="Key Texas prompt-payment deadlines"><div class="ticker-track">{tick}{tick}</div></div>

<section class="section">
  <div class="wrap split">
    <div data-reveal="left">
      <span class="eyebrow"><span class="numeral">I.</span>What we do</span>
      <h2>Enforce Interest turns a slow claim into a <em>documented</em> one.</h2>
      <p class="lede">Insurance claims rarely fail all at once. They stall: an inspection that takes a month, a desk review
      that cuts the estimate, a document request for something already in the file, a supplement that sits for a season.</p>
      <p>Texas lawmakers anticipated that. Since 1991 the state has had a prompt-payment statute &mdash; first Article 21.55,
      now Chapter 542, Subchapter B of the Insurance Code &mdash; that puts insurers on a clock and charges them for
      running past it. Enforce Interest exists because that clock is almost never raised by the people it protects. We
      read the claim file the way the statute does: what was requested, when it arrived, when payment was due and when it
      actually came.</p>
      <p>The result is a dated, sourced timeline and an interest figure the carrier can check line by line. That is what
      Enforce Interest presents &mdash; not a feeling that the claim took too long, but the statutory math of how long,
      on how much, at what rate.</p>
      <div class="btn-row" style="margin-top:22px">{btn("/texas-prompt-payment-act/", "Read the Prompt Payment Act guide", "primary")}</div>
    </div>
    <div data-reveal="right">
      <div class="stats" style="grid-template-columns:1fr 1fr">
        <div><b data-count="18" data-suffix="%">18%</b><span>Standard penalty rate a year, §542.060(a)</span></div>
        <div><b data-count="60">60</b><span>Days to pay after receiving requested items, §542.058</span></div>
        <div><b data-count="10" data-suffix="%">10%</b><span>Texas cap on public adjuster fees, §4102.104</span></div>
        <div><b>$0</b><span>Cost of a claim review with Enforce Interest</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section clock-sec" id="clock">
  <div class="wrap clock-grid">
    <div class="clock-sticky">
      {sec_head('<span class="numeral">II.</span>The clock', "Texas built a payment clock into every property policy.",
                "Scroll the statute. Each step is a separate deadline in Chapter 542 &mdash; and a missed one is what Enforce Interest documents.")}
      <div class="clock-face" aria-hidden="true">
        <div class="clock-day"><small>Statutory clock</small><span data-clock-day>Day 0</span></div>
        <div class="clock-bar"><i data-clock-bar></i></div>
        <div class="clock-legend"><span>Notice</span><span>Day 60</span><span>Paid</span></div>
        <p class="clock-status" data-clock-status>The claim is reported. Nothing is late yet.</p>
      </div>
    </div>
    <div class="steps-v">
      <div class="prog" data-steps-prog></div>
      <div class="step-v" data-step data-day="0" data-status="The claim is reported. Nothing is late yet.">
        <span class="when">Day 0 &middot; Notice of claim</span>
        <h3>You give the insurer written notice.</h3>
        <p>&ldquo;Notice of claim&rdquo; means any written notice that reasonably tells the insurer the facts of the claim
        (§542.051). Keep the date and a copy &mdash; every later deadline is measured from a document like this one.</p>
      </div>
      <div class="step-v" data-step data-day="15" data-status="By day 15 the insurer must <b>acknowledge, start investigating and request items</b>.">
        <span class="when">By day 15 &middot; §542.055</span>
        <h3>Acknowledge, investigate, ask for what it needs.</h3>
        <p>Within 15 days (30 business days for an eligible surplus lines insurer) the carrier must acknowledge the claim,
        begin its investigation and request every item, statement and form it reasonably believes it will need. It can
        ask for more later only if the investigation makes that necessary.</p>
      </div>
      <div class="step-v" data-step data-day="36" data-status="15 business days after the last requested item arrives, the insurer must <b>accept or reject in writing</b>.">
        <span class="when">15 business days after items arrive &middot; §542.056</span>
        <h3>Accept or reject &mdash; in writing.</h3>
        <p>Once it has the items it requested, the insurer has 15 business days to accept or reject the claim in writing
        (30 days if it reasonably suspects arson). If it needs more time it must say why within that window, and then
        decide within 45 more days. A rejection must state its reasons.</p>
      </div>
      <div class="step-v" data-step data-day="43" data-status="Accepted? Payment is due within <b>5 business days</b>.">
        <span class="when">5 business days after acceptance &middot; §542.057</span>
        <h3>Accepted means paid &mdash; within five business days.</h3>
        <p>After notifying you that it will pay all or part of the claim, the insurer must pay within 5 business days
        (20 business days for an eligible surplus lines insurer), or within 5 business days after you perform any act the
        payment was conditioned on.</p>
      </div>
      <div class="step-v" data-step data-day="60" data-status="<b>Day 60</b> after the requested items arrive: the general payment deadline in §542.058.">
        <span class="when">60 days after items arrive &middot; §542.058</span>
        <h3>The 60-day backstop.</h3>
        <p>Whatever happens with acceptance, an insurer that delays payment for more than 60 days after receiving all the
        items it reasonably requested is liable under §542.060. The exception: if arbitration or litigation finds the
        claim invalid. In a declared weather catastrophe the claim-handling deadlines extend by 15 days (§542.059(b)).</p>
      </div>
      <div class="step-v" data-step data-day="80" data-status="Past the deadline: <b>interest accrues daily</b> on the unpaid amount until it is paid.">
        <span class="when">Every day after &middot; §542.060</span>
        <h3>Interest runs until the money is paid.</h3>
        <p>From the date the claim was required to be paid, the insurer owes interest on the late amount as damages
        &mdash; 18% a year, or the floating rate for qualifying weather claims &mdash; plus reasonable and necessary
        attorney&rsquo;s fees. Partial payments shrink the balance the interest runs on; they don&rsquo;t stop it.</p>
        <a class="link-arrow" href="/tools/claim-deadline-calculator/">Calculate your own deadlines</a>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="rates">
  <div class="wrap">
    {sec_head('<span class="numeral">III.</span>Two rates', "Standard 18% or the weather floating rate.",
              "Since 2017, Texas has applied two different interest rates depending on the claim. Picking the right one is the first thing Enforce Interest checks.", center=True)}
    <div class="rate-cards" data-reveal>
      <div class="rate-card std">
        {cite("§542.060(a) &middot; standard")}
        <div class="rate-big">18<sup>%</sup></div>
        <p><strong>Fixed by statute. Simple interest, per year.</strong></p>
        <div class="bar"><i style="--w:1"></i></div>
        <ul><li>Fire, smoke, water, plumbing, theft, vandalism and other non-weather losses</li>
        <li>Weather claims <em>made</em> before September 1, 2017</li>
        <li>Plus reasonable and necessary attorney&rsquo;s fees</li></ul>
        <a class="link-arrow" href="/blog/18-standard-rate-explained/">How the 18% rate works</a>
      </div>
      <div class="rate-card flt">
        {cite("§542.060(c) &middot; Chapter 542A")}
        <div class="rate-big">{FLOAT_RATE_S.replace("%", "")}<sup>%</sup></div>
        <p><strong>§304.003 judgment rate ({JUDG_RATE_S}) + 5%, {RATE_MONTH}.</strong></p>
        <div class="bar"><i style="--w:{FLOAT_RATE / 18:.3f}"></i></div>
        <ul><li>Claims for damage caused wholly or partly by forces of nature &mdash; hail, wind, hurricane, tornado,
        flood, lightning, wildfire, snowstorm, rainstorm, earthquake</li>
        <li>Claims made on or after September 1, 2017, in an action governed by Chapter 542A</li>
        <li>In court the rate is set on the date of judgment; it can range from 10% to 20%</li></ul>
        <a class="link-arrow" href="/blog/act-of-god-floating-rate/">How the floating rate works</a>
      </div>
    </div>
    <p class="center muted" style="margin-top:26px;font-size:.92rem">On a {money(50000, False)} claim paid 90 days late:
    <strong>{money(s50_18)}</strong> at 18% versus <strong>{money(s50_fl)}</strong> at {FLOAT_RATE_S}.
    <a href="/texas-judgment-interest-rate/">See every monthly §304.003 rate since 2005</a>.</p>
  </div>
</section>

<section class="section" id="claims">
  <div class="wrap">
    {sec_head('<span class="numeral">IV.</span>Claim types', "Where Texas claims get stalled.",
              "Every first-party property loss is covered by the same deadlines. What changes is the rate, the evidence and the tactics.")}
    <div class="grid g4" data-stagger>
      <a class="card claim-card" href="/hail-wind-claims/"><div class="cc-top">{art.hail()}<span class="rate">{FLOAT_RATE_S} &middot; 542A</span></div>
        <div class="cc-body"><h3>Hail &amp; wind</h3><p>Roof claims, &ldquo;wear and tear&rdquo; denials, cut estimates and the 61-day pre-suit notice.</p><span class="more">Storm claims</span></div></a>
      <a class="card claim-card" href="/hurricane-claims/"><div class="cc-top">{art.hurricane()}<span class="rate">{FLOAT_RATE_S} &middot; 542A</span></div>
        <div class="cc-body"><h3>Hurricane</h3><p>Named-storm deductibles, wind-versus-flood disputes, TWIA and catastrophe extensions.</p><span class="more">Hurricane claims</span></div></a>
      <a class="card claim-card" href="/fire-smoke-damage/"><div class="cc-top">{art.fire()}<span class="rate">18% &middot; 542.060(a)</span></div>
        <div class="cc-body"><h3>Fire &amp; smoke</h3><p>Smoke and soot scope, contents inventories, ALE and code upgrades &mdash; at the full 18%.</p><span class="more">Fire claims</span></div></a>
      <a class="card claim-card" href="/water-plumbing-damage/"><div class="cc-top">{art.water()}<span class="rate">18% &middot; 542.060(a)</span></div>
        <div class="cc-body"><h3>Water &amp; plumbing</h3><p>Sudden discharge versus seepage, mold, hidden damage and freeze losses.</p><span class="more">Water claims</span></div></a>
    </div>
  </div>
</section>

<section class="section dark" id="appraisal">
  <div class="wrap">
    {sec_head('<span class="numeral">V.</span>Appraisal &amp; late payment', "The appraisal award came in higher. The interest may still be owed.",
              "For years carriers treated paying an appraisal award as the end of the claim. The Texas Supreme Court disagreed.")}
    <div data-reveal>
      <div class="toggle-pill" role="tablist" aria-label="Before and after Hinojos">
        <button type="button" role="tab" aria-selected="true" aria-controls="ba-before" id="tab-before">Before 2019&ndash;2021</button>
        <button type="button" role="tab" aria-selected="false" aria-controls="ba-after" id="tab-after">After Barbara Technologies &amp; Hinojos</button>
      </div>
      <div class="ba-panel" id="ba-before" role="tabpanel" aria-labelledby="tab-before">
        <div class="ba-flow">
          <div class="ba-step"><b>Step 1</b><p>Claim stalls; carrier pays a low figure.</p></div>
          <div class="ba-step"><b>Step 2</b><p>Policyholder invokes appraisal.</p></div>
          <div class="ba-step"><b>Step 3</b><p>Panel awards more; carrier pays the award.</p></div>
          <div class="ba-step bad"><b>Result</b><p>Carrier argues the claim is closed and no prompt-payment damages are owed.</p></div>
        </div>
      </div>
      <div class="ba-panel" id="ba-after" role="tabpanel" aria-labelledby="tab-after" hidden>
        <div class="ba-flow">
          <div class="ba-step"><b>2019</b><p><em>Barbara Technologies</em>: paying an award is not an acknowledgment of liability and doesn&rsquo;t bar prompt-payment claims.</p></div>
          <div class="ba-step"><b>2020</b><p><em>Alvarez</em>: same rule applied to an award paid on a disputed claim.</p></div>
          <div class="ba-step"><b>2021</b><p><em>Hinojos</em>: a reasonable, timely partial payment doesn&rsquo;t shield the unpaid balance.</p></div>
          <div class="ba-step good"><b>Result</b><p>Interest can run on whatever was owed but unpaid at the deadline, through the date the award is paid.</p></div>
        </div>
      </div>
      <p style="margin-top:26px;max-width:72ch">On a {money(100000, False)} underpayment paid eighteen months (548 days) late at 18%,
      the interest alone is <strong>{money(hin)}</strong>. Enforce Interest calculates it from the original deadline to the
      award payment date &mdash; and checks whether any interest the carrier did pay used the right rate and dates.</p>
      <div class="btn-row" style="margin-top:22px">{btn("/post-appraisal-interest-recovery/", "Post-appraisal interest guide", "gold")}{btn("/tools/appraisal-interest-calculator/", "Appraisal interest calculator", "ghost", arrow=False)}</div>
    </div>
  </div>
</section>

<section class="section" id="qualify">
  <div class="wrap">
    {sec_head('<span class="numeral">VI.</span>Does your claim qualify?', "Most Texas first-party property claims can.",
              "Whether interest is owed depends on coverage, what the insurer requested and when, and why the payment was late. Here is the quick version.")}
    <div class="grid g2" data-stagger>
      <div class="card"><h3>Likely worth a review</h3><ul class="check">
        <li>The carrier accepted the claim but paid part of it later, or paid it all late.</li>
        <li>No decision arrived within the statutory windows after you sent what was requested.</li>
        <li>A supplement for additional damage sat unpaid for months.</li>
        <li>Appraisal produced an award higher than what the carrier had paid.</li>
        <li>The claim was denied, then paid after you pushed back.</li></ul></div>
      <div class="card"><h3>Probably not</h3><ul class="cross">
        <li>The claim was paid in full within the deadlines.</li>
        <li>The claim was denied and the denial was never reversed or found wrong.</li>
        <li>The delay was caused by the policyholder &mdash; no access, no documents, no response.</li>
        <li>Workers&rsquo; comp, title, mortgage guaranty, fidelity/surety bonds or marine insurance (excluded by §542.053).</li></ul></div>
    </div>
    <div class="btn-row" style="margin-top:28px;justify-content:center">{btn("/does-my-claim-qualify/", "Take the 2-minute qualification check", "primary")}</div>
  </div>
</section>

<section class="section alt" id="tools">
  <div class="wrap">
    {sec_head('<span class="numeral">VII.</span>Free tools', "Calculators built on the actual statutes.",
              "Every Enforce Interest tool runs in your browser, cites its authority and lets you print or copy the result. No sign-up.", center=True)}
    <div class="grid g3" data-stagger>
      {"".join(f'<a class="card" href="{t["path"]}"><div class="ico">{icon(t["icon"])}</div><h3>{t["short"]}</h3><p>{t["blurb"]}</p><span class="more">Open tool</span></a>' for t in ctx_tools()[:6])}
    </div>
    <div class="btn-row" style="margin-top:28px;justify-content:center">{btn("/tools/", "See all tools", "ghost", arrow=True)}</div>
  </div>
</section>

<section class="section" id="process">
  <div class="wrap">
    {sec_head('<span class="numeral">VIII.</span>How recovery works', "Four steps. No upfront cost.",
              "Enforce Interest is a contingency-based public adjusting service: if nothing is recovered, there is no fee.")}
    <div class="steps-h" data-stagger>
      <div class="step-h"><h3>Free claim review</h3><p>Send the policy, claim letters, payment history and correspondence. We tell you whether the timeline supports a prompt-payment issue.</p></div>
      <div class="step-h"><h3>Timeline forensics</h3><p>Every notice, request, response, inspection and payment gets a date and a source. We identify when each payment was due.</p></div>
      <div class="step-h"><h3>Claim presentation</h3><p>The carrier receives a written presentation of unpaid amounts, deadlines and calculated statutory interest for its review.</p></div>
      <div class="step-h"><h3>You get paid</h3><p>Payments are made to you; Texas requires the insured on every check. Our fee is contingent and capped by law at 10%.</p></div>
    </div>
  </div>
</section>

<section class="section dark" id="about">
  <div class="wrap split">
    <div data-reveal="left">
      <span class="eyebrow"><span class="numeral">IX.</span>Who we are</span>
      <h2>A Texas-licensed public adjusting firm built around <em>§542</em>.</h2>
      <p>Enforce Interest is a service of {FIRM}, a public adjusting firm licensed by the Texas Department of Insurance
      (license #{LICENSE}) and based in Austin. We handle residential and commercial property claims across Texas, with a
      focus on files that were disputed, underpaid or slow-paid.</p>
      <p>We started Enforce Interest after seeing the same pattern again and again: claims paid months &mdash; sometimes
      years &mdash; after the statute said they were due, and no one ever raised the interest. The review is free and the
      math is the math. If you waited more than two months for a Texas property claim to be paid, Enforce Interest wants
      to look at your file.</p>
      <div class="btn-row" style="margin-top:24px">{btn("/about-us/", "About Enforce Interest", "gold")}{btn("/contact/", "Contact us", "ghost", arrow=False)}</div>
    </div>
    <div data-reveal="right">
      <div class="card dark-card" style="padding:32px">
        <h3>What we will and won&rsquo;t do</h3>
        <ul class="check" style="color:rgba(255,255,255,.85)">
          <li>Adjust and document your property claim as a licensed public adjuster.</li>
          <li>Build the claim timeline and calculate statutory interest.</li>
          <li>Present unpaid amounts and interest to the carrier in writing.</li></ul>
        <ul class="cross" style="color:rgba(255,255,255,.85);margin-top:8px">
          <li>Give legal advice or file lawsuits &mdash; we are not a law firm.</li>
          <li>Refer you to an attorney for a fee (prohibited by §4102.158).</li>
          <li>Charge more than the 10% Texas cap, or take any fee if nothing is recovered.</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="toolkit">
  <div class="wrap">
    {sec_head("Documentation toolkit", "Gear that makes a claim easier to prove.",
              "Moisture readings, thermal images and organized records get the carrier what it needs, and make the Enforce Interest timeline easier to prove.")}
    <div class="grid g3" data-stagger>{"".join(products.card(k) for k in ["moisture-pin", "thermal", "scanner"])}</div>
    <p class="aff-note">{products.DISCLOSURE}</p>
    <div class="btn-row" style="margin-top:18px">{btn("/claim-documentation-toolkit/", "See the full toolkit", "ghost")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head("From the blog", "Guides to Texas claim interest.",
              "Plain-English explanations of the statutes and cases behind Enforce Interest.")}
    <div class="grid g3" data-stagger>{cards_blog}</div>
    <div class="btn-row" style="margin-top:28px">{btn("/blog/", "All articles", "ghost")}</div>
  </div>
</section>

<section class="section alt" id="faq">
  <div class="wrap-narrow">
    {sec_head('<span class="numeral">X.</span>FAQ', "Questions policyholders ask Enforce Interest.", center=True)}
    <div data-reveal>{faq_html}</div>
    <p class="center" style="margin-top:26px"><a class="link-arrow" href="/faq/">More answers in the full FAQ</a></p>
  </div>
</section>
{cta_band("Already paid &mdash; but late? Let Enforce Interest run the numbers.")}
'''

    return {
        "path": "/", "title": TITLE, "desc": DESC, "body": body, "priority": "1.0", "freq": "weekly",
        "schema": [faq_ld, {
            "@context": "https://schema.org", "@type": "WebPage", "@id": lib.SITE + "/#webpage",
            "url": lib.SITE + "/", "name": TITLE, "description": DESC, "isPartOf": {"@id": lib.SITE + "/#website"},
            "about": {"@id": lib.SITE + "/#org"}, "dateModified": lib.BUILD_DATE}],
        "h1_plain": "Paid late? Enforce Interest on every day of delay.",
        "body_class": "home",
    }


def ctx_tools():
    from content import tools
    return tools.TOOL_LIST
