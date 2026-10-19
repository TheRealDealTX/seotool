<?php
require dirname(__DIR__) . '/inc/config.php';

$faqs = [
    ['q' => 'How do public adjusters get paid?',
     'a' => 'Public adjusters work for the policyholder on a contingency fee, a percentage of the insurance settlement they help recover. Typical fees run 10% to 20%, and the adjuster is paid only when the claim pays.'],
    ['q' => 'Is there a cap on public adjuster fees?',
     'a' => 'Many states cap them. Texas limits public adjuster fees to 10% of the settlement. Florida generally caps fees at 20%, and at 10% for claims tied to a declared state of emergency during the year after the declaration. Always check your state\'s current rules.'],
    ['q' => 'How much does a public adjuster make a year?',
     'a' => 'Commonly $50,000 to $100,000. Established public adjusters with steady referral flow and commercial or large-loss claims can earn $150,000 or more, especially if they own the firm rather than splitting fees with one.'],
    ['q' => 'Is hiring a public adjuster worth it for a homeowner?',
     'a' => 'It can be on large, complex or disputed claims where a skilled adjuster recovers substantially more than the insurer first offered. On small, straightforward claims the fee can outweigh the gain, which is why this calculator compares the net to the initial offer.'],
];

$page = [
    'title' => 'Public Adjuster Fee Calculator: Fees, Caps & PA Income',
    'description' => 'Calculate public adjuster fees on any settlement, with Texas and Florida fee caps built in. See the homeowner net and what a public adjuster earns per year.',
    'path' => '/public-adjuster-fee-calculator/',
    'image' => 'signing-documents.webp',
    'scripts' => ['tools.js'],
    'schema' => [tool_schema('Public Adjuster Fee Calculator', '/public-adjuster-fee-calculator/', 'Calculate public adjuster contingency fees, state caps and annual public adjuster income.'), faq_schema($faqs)],
];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Free tool', 'Public Adjuster Fee Calculator', 'See exactly how a public adjuster gets paid on a claim &mdash; and what the policyholder keeps. Then model a public adjuster\'s annual income.', 'signing-documents.webp', ['Tools' => '/tools/', 'Public Adjuster Fee Calculator' => null]);
?>
<section class="section">
  <div class="container">
    <div class="tool-shell reveal" id="pa-calc">
      <form class="tool-form" onsubmit="return false">
        <div class="field">
          <span class="label">State rules</span>
          <div class="seg">
            <input type="radio" name="cap" id="p-other" value="none" checked><label for="p-other">Other state</label>
            <input type="radio" name="cap" id="p-tx" value="tx"><label for="p-tx">Texas (10% cap)</label>
            <input type="radio" name="cap" id="p-fl" value="fl"><label for="p-fl">Florida (20% cap)</label>
            <input type="radio" name="cap" id="p-fle" value="fle"><label for="p-fle">FL emergency (10%)</label>
          </div>
        </div>
        <div class="two-col">
          <div class="field">
            <label for="p-offer">Insurer's initial offer ($)</label>
            <input type="number" id="p-offer" min="0" step="500" value="40000">
          </div>
          <div class="field">
            <label for="p-settle">Final settlement ($)</label>
            <input type="number" id="p-settle" min="0" step="500" value="85000">
          </div>
        </div>
        <div class="field">
          <label for="p-fee">Public adjuster fee <output id="p-fee-out">15%</output></label>
          <input type="range" id="p-fee" min="5" max="25" step="0.5" value="15">
          <div class="hint" id="p-cap-hint">Fees above the state cap are reduced automatically.</div>
        </div>
        <hr style="border:0;border-top:1px dashed var(--line);margin:26px 0">
        <span class="eyebrow" style="margin-bottom:6px">PA annual income</span>
        <div class="two-col">
          <div class="field">
            <label for="p-count">Claims settled per year <output id="p-count-out">30</output></label>
            <input type="range" id="p-count" min="5" max="120" value="30">
          </div>
          <div class="field">
            <label for="p-split">Your share of the fee <output id="p-split-out">50%</output></label>
            <input type="range" id="p-split" min="30" max="100" step="5" value="50">
            <div class="hint">100% if you own the firm</div>
          </div>
        </div>
      </form>
      <div class="tool-result" aria-live="polite">
        <h3>Public adjuster fee</h3>
        <div class="result-big" id="p-feeamt">$0</div>
        <div class="result-sub" id="p-rate">-</div>
        <ul class="result-list">
          <li><span>Policyholder keeps</span><b id="p-net">-</b></li>
          <li><span>Gain vs. initial offer (after fee)</span><b id="p-gain">-</b></li>
          <li><span>Break-even settlement</span><b id="p-break">-</b></li>
        </ul>
        <h3 style="margin-top:28px">Estimated PA income / year</h3>
        <div class="result-big" style="font-size:2.6rem" id="p-annual">$0</div>
        <p class="tool-disclaimer">Assumes every claim settles near the amount above. Fee caps shown are general rules; confirm current law and contract terms in your state.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container narrow prose reveal">
    <h2>How public adjusters get paid</h2>
    <p>A public adjuster is the only kind of adjuster who works for the policyholder instead of the insurance company. There is no salary: the public adjuster earns a <strong>contingency fee</strong>, a percentage of what the claim pays. If the claim pays nothing, neither does the adjuster.</p>
    <p>That makes public adjuster salary a function of three things &mdash; average claim size, the fee percentage the state allows, and how many claims you settle. A residential-only public adjuster in a capped state needs volume; one who handles commercial fires and hurricane losses can earn more from a handful of files.</p>
    <p>Learn more in our full <a href="<?= BLOG_BASE ?>public-adjuster-salary/">public adjuster salary guide</a>, or see how every adjuster type is paid in <a href="<?= BLOG_BASE ?>how-do-insurance-adjusters-get-paid/">how do insurance adjusters get paid</a>.</p>
    <h2 id="faq">Public adjuster fee FAQs</h2>
    <?= faq_html($faqs) ?>
  </div>
</section>
<?= other_tools('/public-adjuster-fee-calculator/') ?>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
