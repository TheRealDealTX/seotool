<?php
require dirname(__DIR__) . '/inc/config.php';

$faqs = [
    ['q' => 'How much does a CAT adjuster make per deployment?',
     'a' => 'Most catastrophe deployments pay an experienced independent adjuster somewhere between $15,000 and $60,000 before expenses and taxes, depending on length, claim complexity, daily closures and the fee split with the IA firm.'],
    ['q' => 'What fee split do IA firms usually offer?',
     'a' => 'Splits commonly run from 65/35 to 75/25 in the adjuster\'s favor. Newer adjusters may start lower, while proven adjusters with strong file quality can negotiate higher splits or daily rates.'],
    ['q' => 'What expenses should I plan for on a deployment?',
     'a' => 'Lodging, food, fuel, vehicle wear, a ladder and safety gear, estimating software such as Xactimate, phone and data. Many adjusters budget $120 to $250 a day, plus travel to and from the storm.'],
    ['q' => 'How many claims can a CAT adjuster close per day?',
     'a' => 'On straightforward hail or wind claims, two to five inspections a day is typical once the deployment is in full swing. Large or complex losses can take several days each but pay much higher fees.'],
];

$page = [
    'title' => 'CAT Adjuster Pay Calculator: Texas Storm Deployment Earnings',
    'description' => 'Estimate CAT adjuster pay for a catastrophe deployment. Enter days, claims per day, fees and split to see gross billing, expenses, taxes and net earnings.',
    'path' => '/cat-deployment-calculator/',
    'image' => 'tornado-storm.webp',
    'scripts' => ['tools.js'],
    'schema' => [tool_schema('CAT Deployment Earnings Calculator', '/cat-deployment-calculator/', 'Estimate catastrophe adjuster deployment earnings after fee splits, expenses and taxes.'), faq_schema($faqs)],
];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Free tool', 'CAT Deployment Earnings Calculator', 'What will that Texas hail or Gulf Coast hurricane deployment really put in your pocket? Model fee-bill income, your split, daily expenses and taxes for any catastrophe assignment.', 'tornado-storm.webp', ['Tools' => '/tools/', 'CAT Calculator' => null]);
?>
<section class="section">
  <div class="container">
    <div class="tool-shell reveal" id="cat-calc">
      <form class="tool-form" onsubmit="return false">
        <div class="field">
          <span class="label">Storm / claim type</span>
          <div class="seg">
            <input type="radio" name="fee" id="f-hail" value="550" data-days="45" data-cpd="3" checked><label for="f-hail">TX hail / wind</label>
            <input type="radio" name="fee" id="f-hur" value="900" data-days="60" data-cpd="2" ><label for="f-hur">Gulf hurricane</label>
            <input type="radio" name="fee" id="f-freeze" value="700" data-days="30" data-cpd="2.5"><label for="f-freeze">TX winter freeze</label>
            <input type="radio" name="fee" id="f-com" value="2500" data-days="60" data-cpd="0.5"><label for="f-com">Commercial</label>
          </div>
          <div class="hint">Texas presets set a typical fee, length and pace. Fine-tune them below.</div>
        </div>
        <div class="field">
          <label for="k-fee">Average fee per claim <output id="k-fee-out">$550</output></label>
          <input type="range" id="k-fee" min="250" max="5000" step="50" value="550">
        </div>
        <div class="two-col">
          <div class="field">
            <label for="k-days">Deployment length <output id="k-days-out">45 days</output></label>
            <input type="range" id="k-days" min="7" max="180" value="45">
          </div>
          <div class="field">
            <label for="k-cpd">Claims closed per day <output id="k-cpd-out">2.5</output></label>
            <input type="range" id="k-cpd" min="0.5" max="6" step="0.5" value="2.5">
          </div>
        </div>
        <div class="two-col">
          <div class="field">
            <label for="k-split">Your fee split <output id="k-split-out">70%</output></label>
            <input type="range" id="k-split" min="50" max="90" step="5" value="70">
          </div>
          <div class="field">
            <label for="k-exp">Daily expenses <output id="k-exp-out">$175</output></label>
            <input type="range" id="k-exp" min="0" max="400" step="5" value="175">
          </div>
        </div>
        <div class="two-col">
          <div class="field">
            <label for="k-travel">Travel to &amp; from storm ($)</label>
            <input type="number" id="k-travel" min="0" step="50" value="800">
          </div>
          <div class="field">
            <label for="k-tax">Tax set-aside <output id="k-tax-out">28%</output></label>
            <input type="range" id="k-tax" min="0" max="45" value="28">
          </div>
        </div>
      </form>
      <div class="tool-result" aria-live="polite">
        <h3>Estimated net earnings</h3>
        <div class="result-big" id="k-net">$0</div>
        <div class="result-sub" id="k-perday">-</div>
        <ul class="result-list">
          <li><span>Claims closed</span><b id="k-claims">-</b></li>
          <li><span>Gross fees billed</span><b id="k-gross">-</b></li>
          <li><span>Your share (split)</span><b id="k-share">-</b></li>
          <li><span>Expenses &amp; travel</span><b id="k-costs">-</b></li>
          <li><span>Tax set-aside</span><b id="k-taxes">-</b></li>
          <li class="total"><span>Take-home</span><b id="k-net2">-</b></li>
        </ul>
        <div class="range-viz" aria-hidden="true">
          <div class="track" id="k-stack" style="display:flex;overflow:hidden;background:rgba(255,255,255,.1)"></div>
          <div class="labels"><span><b style="color:#be9967">&#9632;</b> Take-home</span><span><b style="color:#8f6c3f">&#9632;</b> Taxes</span><span><b style="color:#5d5d62">&#9632;</b> Expenses</span><span><b style="color:#2d2d31;-webkit-text-stroke:1px #555">&#9632;</b> Firm</span></div>
        </div>
        <p class="tool-disclaimer">Illustrative only. Fee schedules, splits and payment timing vary by carrier and IA firm.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container narrow prose reveal">
    <h2>How CAT adjusters get paid</h2>
    <p>Catastrophe adjusters are almost always independent contractors. The carrier pays the IA firm a fee for every claim based on a <strong>fee schedule</strong> tied to the gross loss &mdash; a $6,000 Dallas hail claim might bill $500, while a $60,000 Houston hurricane claim can bill $1,500 or more. The firm keeps its share (often 25&ndash;35%) and pays the rest to you, usually a few weeks after each file is approved.</p>
    <p>Because you pay your own lodging, meals, fuel and software, the number that matters is net take-home per day worked. That is what this calculator shows. A long, busy deployment with simple claims often beats a short one with big losses &mdash; and a slow-starting storm can cut the math in half.</p>
    <p>For the full picture, read our guide to <a href="<?= BLOG_BASE ?>cat-adjuster-salary/">CAT adjuster salary</a>, see the sample fee schedule in <a href="<?= BLOG_BASE ?>insurance-adjuster-pay-rate/">insurance adjuster pay rates</a>, or compare against a staff role with the <a href="/salary-calculator/">insurance adjuster salary calculator</a>.</p>
    <h2 id="faq">CAT deployment FAQs</h2>
    <?= faq_html($faqs) ?>
  </div>
</section>
<?= other_tools('/cat-deployment-calculator/') ?>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
