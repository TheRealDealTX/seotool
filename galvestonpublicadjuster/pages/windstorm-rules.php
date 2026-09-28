<?php
$meta['title'] = 'Texas Windstorm Rules: TWIA, WPI-8 & Claim Deadlines';
$meta['description'] = 'Texas windstorm insurance rules for Galveston owners: TWIA eligibility, WPI-8 certificates, TWIA claim deadlines, appraisal, public adjuster rules and 2025–2026 changes.';
$meta['crumb'] = 'Texas Windstorm Rules';
$meta['schema'][] = ['@type' => 'Article', 'headline' => 'Texas Windstorm Rules for Galveston Property Owners', 'author' => ['@type' => 'Person', 'name' => AUTHOR],
    'publisher' => ['@id' => SITE_URL . '/#business'], 'dateModified' => '2026-09-28'];
echo page_hero(icon('scale', 18) . ' Texas windstorm rules', 'Texas Windstorm Rules Every Galveston Owner Should Know',
    'TWIA eligibility, windstorm certificates, claim deadlines and your rights when a claim goes wrong — in plain English, with the statute behind each rule.');
?>
<section class="section">
  <div class="wrap layout-side">
    <article class="prose">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#twia">TWIA: who it covers</a></li><li><a href="#wpi8">WPI-8 windstorm certificates</a></li><li><a href="#deadlines">TWIA claim deadlines</a></li>
        <li><a href="#disputes">Disputes: appraisal and denials</a></li><li><a href="#private">Private insurers: Prompt Payment Act</a></li>
        <li><a href="#pa">Texas public adjuster rules</a></li><li><a href="#changes">2025–2026 changes</a></li></ol></nav>

      <h2 id="twia">TWIA: who it covers</h2>
      <p>The Texas Windstorm Insurance Association is the state's wind and hail insurer of last resort, created under <strong>Texas Insurance Code chapter 2210</strong>. It writes wind and hail coverage in the 14 first-tier coastal counties — Aransas, Brazoria, Calhoun, Cameron, Chambers, <strong>Galveston</strong>, Jefferson, Kenedy, Kleberg, Matagorda, Nueces, Refugio, San Patricio and Willacy — plus the part of Harris County east of Highway 146.</p>
      <p>A typical Galveston homeowner carries three policies: a homeowners policy that excludes wind and hail, a TWIA windstorm policy, and a separate flood policy (NFIP or private). Knowing which policy pays for which damage is the heart of most coastal claims.</p>

      <h2 id="wpi8">WPI-8 windstorm certificates</h2>
      <p>Any structure built, altered or repaired on or after <strong>January 1, 1988</strong> generally needs a Certificate of Compliance to be eligible for TWIA coverage. That includes most roof replacements.</p>
      <div class="table-wrap"><table class="data"><thead><tr><th>Form</th><th>What it is</th></tr></thead><tbody>
        <tr><td><strong>WPI-1</strong></td><td>Notice filed with TDI <em>before</em> work begins, by the appointed engineer or inspector.</td></tr>
        <tr><td><strong>WPI-8</strong></td><td>Certificate of Compliance issued by the Texas Department of Insurance after inspections during construction.</td></tr>
        <tr><td><strong>WPI-8-E</strong></td><td>Certificate issued by TDI for completed work certified by a Texas-licensed professional engineer (Ins. Code §2210.2515).</td></tr>
        <tr><td><strong>WPI-8-C</strong></td><td>Legacy certificate TWIA issued for completed work submitted roughly 2017–2020.</td></tr>
      </tbody></table></div>
      <div class="callout"><?= icon('building', 24) ?><div><strong>Code in effect:</strong> For WPI-1 applications on or after <strong>April 1, 2026</strong>, TDI requires work to be certified to the <strong>2024 IRC or 2024 IBC</strong> with TDI revisions. Projects started earlier may use the prior code. That matters for your claim: code-required windstorm upgrades are part of the cost to repair. See <a href="/galveston-local-code/">Galveston local code</a>.</div></div>

      <h2 id="deadlines">TWIA claim deadlines</h2>
      <ol class="timeline" style="margin-top:28px">
        <li><span class="yr ts">1 yr</span><div class="card"><h3>File your claim</h3><p>Within one year of the date of damage. The Commissioner may extend by up to 180 days for good cause. <span class="tag">§2210.573(a), §2210.205</span></p></div></li>
        <li><span class="yr">30 d</span><div class="card"><h3>TWIA requests information</h3><p>TWIA may ask in writing for what it needs within 30 days after the claim is filed. <span class="tag">§2210.573(b)</span></p></div></li>
        <li><span class="yr c2">60 d</span><div class="card"><h3>TWIA decides</h3><p>Accept in full, accept in part / deny in part, or deny — in writing — within 60 days of receiving the claim or the requested information, whichever is later. Catastrophe extensions may not exceed 120 days total. <span class="tag">§2210.573(d), §2210.581</span></p></div></li>
        <li><span class="yr c1">10 d</span><div class="card"><h3>TWIA pays</h3><p>Within 10 days after it notifies you it accepted the claim (or after you perform any required condition). <span class="tag">§2210.5731</span></p></div></li>
      </ol>

      <h2 id="disputes">Disputes: appraisal and denials</h2>
      <h3>Disagree with the amount? Appraisal.</h3>
      <p>You may demand appraisal within <strong>60 days</strong> of TWIA's decision notice; TWIA may grant 30 more days if you ask in writing, with good cause, within 15 days after the 60 days end (§2210.574). Appraisal costs are split, and the award is binding. For claims after January 1, 2024, TDI rules set timelines for naming an umpire and completing residential (90 + 60 days) and commercial (120 + 90 days) appraisals.</p>
      <h3>Coverage denied? Notice of intent to sue.</h3>
      <p>For a denial of coverage, you must give TWIA a <strong>notice of intent to sue</strong> before the limitations period expires or the right to contest is waived (§2210.575). TWIA may require mediation or a moderated settlement conference. Any suit must be filed within <strong>two years</strong> of receiving the denial — a statute of repose (§2210.577). A public adjuster cannot file suit; we'll tell you early if your claim needs an attorney.</p>
      <?= banner('Up against a TWIA deadline? Call for an expert consultation.', 'We review your letters and map every date that applies to your claim.') ?>

      <h2 id="private">Private insurers: the Prompt Payment of Claims Act</h2>
      <p>Homeowners, flood-excluded and commercial policies from private carriers follow <strong>Insurance Code chapter 542</strong> instead:</p>
      <ul class="checks">
        <li><strong>15 days</strong> after notice to acknowledge, start investigating and request items (§542.055)</li>
        <li><strong>15 business days</strong> after receiving everything to accept or reject — up to 45 more days if they notify you they need it (§542.056)</li>
        <li><strong>5 business days</strong> to pay after accepting (§542.057)</li>
        <li><strong>+15 days</strong> on every deadline after a declared weather catastrophe (§542.059)</li>
        <li>Late payment can carry statutory interest and attorney's fees (§542.060)</li>
      </ul>

      <h2 id="pa">Texas public adjuster rules</h2>
      <ul class="checks">
        <li>Public adjusters must be licensed by the Texas Department of Insurance (§4102.051).</li>
        <li>Contracts must be on a TDI-approved form and say <strong>"WE REPRESENT THE INSURED ONLY"</strong> (§4102.103).</li>
        <li>You can rescind the contract in writing within <strong>72 hours</strong> of signing.</li>
        <li>Fees are capped at <strong>10%</strong> of the settlement; no percentage fee if the insurer pays or commits to pay policy limits within 72 hours of the loss report (§4102.104).</li>
        <li>You must be named on claim checks. Public adjusters cannot perform or profit from repairs (§4102.158, §4102.163).</li>
      </ul>

      <h2 id="changes">2025–2026 changes</h2>
      <ul>
        <li><strong>HB 3689 (effective Sept. 1, 2025)</strong> changed how TWIA is funded after a catastrophe, including state financing repaid by a statewide surcharge.</li>
        <li><strong>SB 458 (2025)</strong>: residential and auto policies issued or renewed after January 1, 2026 must include an appraisal clause.</li>
        <li><strong>HB 2067 (2025)</strong>: insurers must give written reasons for declines, cancellations and nonrenewals.</li>
        <li><strong>April 1, 2026</strong>: TDI's windstorm program moved to the 2024 IRC/IBC with Texas revisions.</li>
      </ul>
      <p class="small muted">This page is general information, current as of September 2026, and is not legal advice. Statute text: <a href="https://tcss.legis.texas.gov/resources/in/htm/in.2210.htm" rel="nofollow noopener" target="_blank">Ins. Code ch. 2210</a>, <a href="https://tcss.legis.texas.gov/resources/in/htm/in.542.htm" rel="nofollow noopener" target="_blank">ch. 542</a>, <a href="https://tcss.legis.texas.gov/resources/in/htm/in.4102.htm" rel="nofollow noopener" target="_blank">ch. 4102</a>; <a href="https://www.tdi.texas.gov/wind/adopted-codes.html" rel="nofollow noopener" target="_blank">TDI adopted codes</a>; <a href="https://www.twia.org/claims/" rel="nofollow noopener" target="_blank">TWIA claims</a>.</p>
    </article>
    <aside class="sidebar">
      <div class="side-card dark"><h3>TWIA claims help</h3><p>Talk to a TWIA expert about your deadlines.</p><?= phone_link('btn btn-cta btn-block', icon('phone', 18) . ' ' . PHONE) ?><p class="small" style="margin-top:12px"><a href="/twia-claims-expert/" style="color:#fff">TWIA claims expert →</a></p></div>
      <div class="side-card"><h3>Free claim review</h3><?= lead_form('windstorm-rules', true) ?></div>
    </aside>
  </div>
</section>
