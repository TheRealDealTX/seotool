<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Insurance Claim Glossary', '/insurance-claim-glossary/']];
$terms = [
    ['Actual Cash Value (ACV)', 'Replacement cost minus depreciation. The first payment on most claims, and the total payment on an ACV policy.'],
    ['Additional Living Expense (ALE)', 'Coverage D, or loss of use. Pays the extra cost of living elsewhere while your home is unlivable after a covered loss.'],
    ['Appraisal', 'A policy process for resolving disputes over the amount of loss. Each side picks an appraiser, and an umpire settles disagreements.'],
    ['Coverage A', 'Dwelling coverage: the house and attached structures. Percentage deductibles are calculated from this limit.'],
    ['Coverage B', 'Other structures such as detached garages, fences and sheds, typically 10% of Coverage A.'],
    ['Coverage C', 'Personal property, or contents: furniture, clothing, electronics and other belongings.'],
    ['Declarations Page', 'The summary page of your policy listing coverages, limits, deductibles and endorsements.'],
    ['Depreciation', 'The reduction in value for age and wear. Recoverable depreciation is paid after repairs on a replacement-cost policy.'],
    ['Endorsement', 'An addition to the policy that changes coverage, such as a roof ACV endorsement or water-backup coverage.'],
    ['Exclusion', 'Something the policy does not cover, such as flood, earth movement or wear and tear.'],
    ['Hurricane / Named-Storm Deductible', 'A separate deductible, usually 1%–5% of Coverage A, applied to damage from a named storm.'],
    ['Independent Adjuster', 'An adjuster hired by the insurance company on contract, often brought in after large storms. Works for the insurer.'],
    ['Matching', 'Whether undamaged materials must be replaced so repairs match in color and quality — a frequent roof and flooring dispute.'],
    ['Mitigation', 'Your duty to prevent further damage after a loss, such as tarping a roof or drying a flooded room.'],
    ['NFIP', 'The National Flood Insurance Program, run by FEMA, which writes most U.S. flood insurance policies.'],
    ['Ordinance or Law Coverage', 'Pays the extra cost of rebuilding to current building codes after a covered loss.'],
    ['Overhead and Profit (O&amp;P)', 'A general contractor’s charge (commonly 10% + 10%) for coordinating multi-trade repairs. Often left off carrier estimates.'],
    ['Proof of Loss', 'A sworn statement of the amount you are claiming, sometimes required by a deadline in the policy.'],
    ['Public Adjuster', 'A licensed professional hired by the policyholder to prepare, document and negotiate a property insurance claim.'],
    ['Replacement Cost Value (RCV)', 'What it costs today to repair or replace damaged property with materials of like kind and quality.'],
    ['Reservation of Rights', 'A letter in which the insurer continues investigating while reserving the right to deny coverage later.'],
    ['Scope of Loss', 'The list of damaged items and repairs included in an estimate. An incomplete scope is the most common cause of underpayment.'],
    ['Supplement', 'A request for additional payment for damage or costs not included in the original estimate.'],
    ['TWIA', 'The Texas Windstorm Insurance Association, which provides wind and hail coverage in designated coastal counties, including parts of Harris and Galveston counties.'],
    ['Xactimate', 'The estimating software most insurers and public adjusters use to price repairs line by line by ZIP code.'],
];
$letters = [];
foreach ($terms as $t) $letters[strtoupper($t[0][0])] = true;
page_start([
    'title' => 'Insurance Claim Glossary: Property Claim Terms in Plain English',
    'desc' => 'Plain-English definitions of property insurance claim terms: ACV, RCV, depreciation, O&P, appraisal, TWIA, hurricane deductible and more — from Houston Public Adjusters.',
    'path' => '/insurance-claim-glossary/',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'DefinedTermSet', 'name' => 'Insurance claim glossary', 'hasDefinedTerm' => array_map(fn($t) => ['@type' => 'DefinedTerm', 'name' => html_entity_decode($t[0]), 'description' => $t[1]], $terms)]],
]);
echo page_hero('Insurance Claim Glossary', 'The words in your policy and your adjuster&rsquo;s letters, explained in plain English by Houston public adjusters.', $crumbs);
?>
<div class="wrap layout-sidebar">
  <div class="prose">
    <nav class="az" aria-label="Jump to letter"><?php foreach (array_keys($letters) as $l): ?><a href="#letter-<?= $l ?>"><?= $l ?></a><?php endforeach; ?></nav>
    <dl class="glossary">
<?php $seen = []; foreach ($terms as $t): $l = strtoupper($t[0][0]); ?>
      <dt<?= isset($seen[$l]) ? '' : ' id="letter-' . $l . '"' ?>><?= $t[0] ?></dt><dd><?= $t[1] ?></dd>
<?php $seen[$l] = true; endforeach; ?>
    </dl>
  </div>
  <aside class="sidebar"><div class="side-card sticky"><?= lead_form('lead-glossary', 'Confused by your claim?', 'We&rsquo;ll explain it for free.', true) ?></div></aside>
</div>
<?php
page_end();
