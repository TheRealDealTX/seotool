<?php
require dirname(__DIR__) . '/inc/tools.php';
$crumbs = [['Home', '/'], ['Claim Tools', '/tools/']];
page_start([
    'title' => 'Free Insurance Claim Calculators & Tools | Houston Public Adjusters',
    'desc' => 'Free insurance claim calculators from Houston Public Adjusters: settlement, public adjuster fee, hurricane deductible, depreciation, ALE, Texas claim deadlines and a contents inventory builder.',
    'path' => '/tools/',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'ItemList', 'name' => 'Insurance claim tools', 'itemListElement' => array_map(fn($s, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => SITE_URL . '/tools/' . $s . '/', 'name' => TOOLS[$s][0]], array_keys(TOOLS), array_keys(array_keys(TOOLS)))]],
]);
echo page_hero('Free Insurance Claim Tools &amp; Calculators', 'Run the numbers on your own claim before you talk to anyone. Built by licensed Houston public adjusters, every tool runs in your browser &mdash; nothing you enter is saved or sent.', $crumbs);
?>
<section class="section">
  <div class="wrap">
    <div class="card-grid">
<?php foreach (TOOLS as $slug => [$name, $icon, $blurb]): ?>
      <a class="card tool-card" href="/tools/<?= $slug ?>/"><span class="ic" aria-hidden="true"><?= $icon ?></span><h3><?= e($name) ?></h3><p><?= e($blurb) ?></p><span class="go">Open tool &rarr;</span></a>
<?php endforeach; ?>
      <a class="card tool-card" href="/houston-weather/"><span class="ic" aria-hidden="true">&#9928;</span><h3>Live Houston Weather Tracker</h3><p>Current conditions, NWS alerts, radar and hurricane outlook for Houston-area cities.</p><span class="go">Open tracker &rarr;</span></a>
      <a class="card tool-card" href="/hurricane-preparedness-checklist/"><span class="ic" aria-hidden="true">&#9989;</span><h3>Hurricane Preparedness Checklist</h3><p>An interactive, insurance-focused checklist that saves your progress.</p><span class="go">Open checklist &rarr;</span></a>
      <a class="card tool-card" href="/insurance-claim-glossary/"><span class="ic" aria-hidden="true">&#128214;</span><h3>Insurance Claim Glossary</h3><p>Plain-English definitions of ACV, RCV, O&amp;P, appraisal and more.</p><span class="go">Open glossary &rarr;</span></a>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap two-col">
    <div class="prose">
      <h2>Calculators are a starting point, not a settlement</h2>
      <p>These tools show how a claim is built: replacement cost, depreciation, deductibles, coverage limits and deadlines. The hard part is the input. If the insurance company&rsquo;s estimate is missing line items or uses the wrong pricing, every number downstream is wrong too.</p>
      <p>That is what Houston public adjusters do: inspect the property, build an independent estimate and negotiate the difference. If a calculator shows a gap between what you were offered and what repairs will cost, call us for a free review.</p>
    </div>
    <div class="side-card"><?= lead_form('lead-tools', 'Free claim review', '', true) ?></div>
  </div>
</section>
<?php
page_end();
