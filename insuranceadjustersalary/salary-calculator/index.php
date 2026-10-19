<?php
require dirname(__DIR__) . '/inc/config.php';
require SITE_ROOT . '/inc/data.php';

$faqs = [
    ['q' => 'How accurate is this insurance adjuster salary calculator?',
     'a' => 'It gives a realistic range, not a quote. The model starts from the BLS national median for claims adjusters ($76,790, May 2024) and adjusts for role, line of business, experience and a regional wage index. Actual offers vary by employer, caseload and storm activity.'],
    ['q' => 'Why is the range so wide for independent and CAT adjusters?',
     'a' => 'Independent and catastrophe adjusters are paid per claim or per day, so income depends on how many deployments they land. A quiet year can pay half of a staff salary, while a major hurricane season can pay two or three times as much.'],
    ['q' => 'Does location change what independent adjusters earn?',
     'a' => 'Less than it does for staff. IA fee schedules are set nationally by carriers and firms, so where you live matters far less than where storms hit. The calculator applies only part of the state wage index to 1099 roles.'],
    ['q' => 'What is included in total compensation for staff adjusters?',
     'a' => 'Staff roles typically include health insurance, a 401(k) match and paid time off. Field roles often add a company car, gas card, phone and laptop. We value that package at roughly $8,000 to $11,000 a year.'],
];

$page = [
    'title' => 'Insurance Adjuster Salary Calculator: Texas & All States',
    'description' => 'Free insurance adjuster salary calculator for Texas metros and every state. Estimate staff, independent, CAT and public adjuster pay in seconds.',
    'path' => '/salary-calculator/',
    'image' => 'analytics-laptop.webp',
    'scripts' => ['salary-model.js', 'tools.js'],
    'schema' => [tool_schema('Insurance Adjuster Salary Calculator', '/salary-calculator/', 'Estimate insurance adjuster pay by role, line, experience and state.'), faq_schema($faqs)],
];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Free tool', 'Insurance Adjuster Salary Calculator', 'Estimate what you could earn as a staff, independent, catastrophe or public adjuster in Houston, Dallas-Fort Worth, Austin, San Antonio or anywhere else in Texas &mdash; or any other state.', 'analytics-laptop.webp', ['Tools' => '/tools/', 'Salary Calculator' => null]);
?>
<section class="section">
  <div class="container">
    <div class="tool-shell reveal" id="salary-calc">
      <form class="tool-form" onsubmit="return false">
        <div class="field">
          <span class="label">How will you work?</span>
          <div class="seg">
            <input type="radio" name="role" id="r-desk" value="desk" checked><label for="r-desk">Staff desk</label>
            <input type="radio" name="role" id="r-field" value="field"><label for="r-field">Staff field</label>
            <input type="radio" name="role" id="r-ind" value="independent"><label for="r-ind">Independent</label>
            <input type="radio" name="role" id="r-cat" value="cat"><label for="r-cat">CAT</label>
            <input type="radio" name="role" id="r-pub" value="public"><label for="r-pub">Public</label>
          </div>
        </div>
        <div class="two-col">
          <div class="field">
            <label for="c-line">Line of business</label>
            <select id="c-line" name="line">
              <option value="property">Property (homeowners)</option>
              <option value="auto">Auto / material damage</option>
              <option value="wc">Workers compensation</option>
              <option value="casualty">Bodily injury / casualty</option>
              <option value="commercial">Commercial / large loss</option>
            </select>
          </div>
          <div class="field">
            <label for="c-state">Texas metro or state</label>
            <select id="c-state" name="state">
              <optgroup label="Texas">
                <option value="1" selected>Texas (statewide)</option>
<?php foreach (texas_metros() as $m): ?>
                <option value="<?= $m['index'] ?>">Texas - <?= e($m['name']) ?></option>
<?php endforeach; ?>
              </optgroup>
              <optgroup label="Other states">
<?php foreach (states() as $s): if ($s['code'] === 'TX') continue; ?>
                <option value="<?= $s['index'] ?>"><?= e($s['name']) ?></option>
<?php endforeach; ?>
              </optgroup>
            </select>
          </div>
        </div>
        <div class="field">
          <label for="c-years">Years of experience <output id="c-years-out">3</output></label>
          <input type="range" id="c-years" name="years" min="0" max="20" value="3">
          <div class="hint">0 = trainee or newly licensed</div>
        </div>
        <div class="field">
          <span class="label">Credentials</span>
          <div class="seg">
            <input type="checkbox" id="c-desig" name="designation"><label for="c-desig">AIC / CPCU</label>
            <input type="checkbox" id="c-bi" name="bilingual"><label for="c-bi">Bilingual</label>
          </div>
        </div>
      </form>
      <div class="tool-result" aria-live="polite">
        <h3>Your estimated salary</h3>
        <div class="result-big" id="c-mid">$0</div>
        <div class="result-sub" id="c-label">-</div>
        <div class="range-viz">
          <div class="track"><span class="band" id="c-band"></span><span class="pin" id="c-pin"></span></div>
          <div class="labels"><span>$30k</span><span>$130k</span><span>$230k</span></div>
        </div>
        <ul class="result-list">
          <li><span>Realistic range</span><b id="c-range">-</b></li>
          <li><span>Hourly equivalent</span><b id="c-hour">-</b></li>
          <li><span>Monthly (gross)</span><b id="c-month">-</b></li>
          <li><span>Benefits &amp; vehicle value</span><b id="c-ben">-</b></li>
          <li class="total"><span>vs. national median ($<?= number_format(BLS_MEDIAN_ANNUAL) ?>)</span><b id="c-vs">-</b></li>
        </ul>
        <p class="tool-disclaimer" id="c-note">Estimates only. Not a job offer.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container narrow prose reveal">
    <h2>How this insurance adjuster salary calculator works</h2>
    <p>Every estimate starts from the Bureau of Labor Statistics median for claims adjusters, appraisers, examiners and investigators: <strong>$<?= number_format(BLS_MEDIAN_ANNUAL) ?> a year</strong> (May 2024). From there the calculator applies four adjustments:</p>
    <ul>
      <li><strong>Role.</strong> Staff desk and field adjusters earn a W-2 salary. Independent, CAT and public adjusters earn per claim, per day or by percentage, so their ranges are much wider.</li>
      <li><strong>Line of business.</strong> Commercial and large-loss claims pay the most; auto material damage pays the least.</li>
      <li><strong>Experience.</strong> Pay climbs quickly over the first five years, then levels off. A ten-year adjuster earns roughly 15% more than a five-year adjuster.</li>
      <li><strong>Location.</strong> Texas metros are built in: Austin, Dallas-Fort Worth and Houston pay about 4&ndash;6% above the national median, while El Paso and McAllen pay less. A regional wage index covers every other state. For 1099 roles, where carriers set national fee schedules, location counts for much less.</li>
    </ul>
    <p>Want the detail behind the numbers? Read <a href="<?= BLOG_BASE ?>how-much-do-insurance-adjusters-make/">how much insurance adjusters make</a>, compare <a href="<?= BLOG_BASE ?>claims-adjuster-salary/">claims adjuster salary</a> by line, or see how <a href="<?= BLOG_BASE ?>independent-adjuster-salary/">independent adjuster pay</a> really works.</p>
    <h2 id="faq">Calculator FAQs</h2>
    <?= faq_html($faqs) ?>
  </div>
</section>
<?= other_tools('/salary-calculator/') ?>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
