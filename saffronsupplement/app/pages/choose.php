<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Two saffron supplements with the same "mg" on the front can be completely different products. Use this 7-point checklist to read any label and pick a saffron extract that is likely to work.', 'Guides &middot; Buying');
?>
<div class="wrap layout">
  <article class="prose">
    <?= toc(['checklist' => 'The 7-point checklist', 'red-flags' => 'Red flags', 'form' => 'Capsules vs gummies vs liquids', 'picks' => 'Products that pass', 'faq' => 'FAQ']) ?>

    <h2 id="checklist">The 7-Point Saffron Label Checklist</h2>
    <ol class="steps">
      <li><strong>It says "extract," not just "saffron."</strong> Trials used extracts. "Saffron powder" or "whole herb" is less concentrated and less predictable.</li>
      <li><strong>It names a branded extract or standardization.</strong> Look for affron® (≥3.5% Lepticrosalides®), Satiereal®, or crocin/safranal percentages such as "7.5% crocins, 1% safranal".</li>
      <li><strong>The dose matches your goal.</strong> 28–30 mg for mood, stress and sleep; 20 mg for eyes; 176.5 mg/day of Satiereal® for appetite. Use the <a href="/tools/saffron-dosage-calculator/">dosage calculator</a>.</li>
      <li><strong>It shows evidence of testing.</strong> GMP-certified facility, third-party testing for identity and heavy metals, or a seal such as NSF or USP.</li>
      <li><strong>The country of origin is stated.</strong> Iran, Spain and Greece are the main sources. Reputable extracts trace their raw material.</li>
      <li><strong>The formula is clean.</strong> Minimal fillers, no artificial dyes, and preferably a single ingredient if you want to know what's working.</li>
      <li><strong>The price is realistic.</strong> Saffron is expensive. A very cheap product with a huge "mg" number is a warning sign. Compare with the <a href="/tools/cost-per-dose-calculator/">cost-per-dose calculator</a>.</li>
    </ol>

    <h2 id="red-flags">Red Flags to Avoid</h2>
    <div class="flag flag-red">"Proprietary blend" that hides how much saffron is inside</div>
    <div class="flag flag-red">Huge doses (500 mg+ of "saffron") at a bargain price, often mostly filler or petals</div>
    <div class="flag flag-red">Claims to "cure depression" or "melt fat," which are illegal disease claims for supplements in the US</div>
    <div class="flag flag-red">Fake review patterns: hundreds of five-star reviews posted within days</div>
    <div class="flag flag-amber">Combined with 5-HTP or St John's wort, which is risky if you take antidepressants</div>

    <h2 id="form">Capsules vs Softgels vs Gummies vs Liquids</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Form</th><th>Pros</th><th>Cons</th></tr></thead>
      <tbody>
        <tr><td>Capsule</td><td>Precise dosing; matches trials; few additives</td><td>Some find them hard to swallow</td></tr>
        <tr><td>Softgel</td><td>Easy to swallow</td><td>Usually costs more</td></tr>
        <tr><td>Tablet</td><td>Cheap; easy to split</td><td>Binders and coatings</td></tr>
        <tr><td>Gummy</td><td>Tastes good</td><td>Added sugar; vague dosing; often blends</td></tr>
        <tr><td>Liquid / liposomal</td><td>Flexible dosing</td><td>Hard to measure; little research</td></tr>
      </tbody>
    </table></div>

    <h2 id="picks">Saffron Supplements That Pass the Checklist</h2>
    <?= aff_note() ?>
    <?= compare_table(['nootropics-depot', 'vinatura-affron', 'life-extension', 'now-foods', 'zazzee']) ?>
    <p><a href="/best-saffron-supplements/">See all 12 reviews &rarr;</a></p>

    <?= faq_block([
      ['What should I look for in a saffron supplement?', '<p>A standardized extract (affron®, Satiereal® or stated crocin/safranal percentages), a dose that matches your goal, third-party testing and a clean formula.</p>'],
      ['What is the purest form of saffron supplement?', '<p>A single-ingredient, standardized saffron extract from a manufacturer that publishes third-party test results.</p>'],
      ['Are cheap saffron supplements fake?', '<p>Not always, but very low prices for high doses are a warning sign. Real saffron is expensive, so check for standardization and testing.</p>'],
      ['Is organic saffron extract better?', '<p>Organic certification limits pesticide use but says nothing about potency. Look for standardization first and organic second.</p>'],
    ]) ?>
    <?= med_note() ?>
  </article>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
