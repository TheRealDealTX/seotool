<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
$path = '/faq/';
$crumbs = [['Home', '/'], ['FAQ', $path]];
$sections = [
    'Hiring a public adjuster' => [
        ['What is a public adjuster?', '<p>A public adjuster is an insurance claims professional licensed by the Texas Department of Insurance to represent policyholders. Unlike the insurance company’s adjuster, a public adjuster works only for you: inspecting the damage, reviewing the policy, preparing the claim and negotiating the settlement.</p>'],
        ['Why hire a Sugar Land public adjuster instead of an out-of-town firm?', '<p>Local knowledge: Houston-area repair pricing, Fort Bend County storm history, and how carriers handle Sugar Land claims. We can also inspect quickly and attend re-inspections in person.</p>'],
        ['How much does a public adjuster in Sugar Land cost?', '<p>No upfront fees. Texas caps public adjuster compensation at 10% of the insurance settlement. See the <a href="/tools/public-adjuster-fee-calculator/">fee calculator</a> and <a href="/how-much-does-a-public-adjuster-cost-in-texas/">our full guide to fees</a>.</p>'],
        ['How do I verify a public adjuster’s license?', '<p>Use the Texas Department of Insurance license lookup. Our firm is ' . e(SITE['firm']) . ', license #' . e(SITE['firm_license']) . '.</p>'],
        ['Will a public adjuster slow my claim down?', '<p>Usually the opposite: a complete, well-documented claim reduces back-and-forth and re-inspections.</p>'],
        ['Is a public adjuster a lawyer?', '<p>No. We prepare and negotiate insurance claims. If your claim needs litigation, we will tell you so you can consult an attorney.</p>'],
    ],
    'Your claim' => [
        ['When should I contact a public adjuster?', '<p>Ideally right after the damage and before the insurer’s inspection—but we can help after a denial, a low offer or even a closed claim.</p>'],
        ['My claim was denied. Can you still help?', '<p>Often, yes. We review the denial reason against your policy and the evidence, document what was missed, and present a supplemented claim or invoke appraisal where it fits. See <a href="/services/denied-underpaid-claims/">denied &amp; underpaid claims</a>.</p>'],
        ['Can a closed claim be reopened?', '<p>Many policies allow supplemental claims when additional damage is found or the original scope was incomplete, usually within a time limit set in the policy.</p>'],
        ['What is recoverable depreciation?', '<p>On a replacement cost policy, the insurer typically holds back depreciation until repairs are complete. That held-back amount is recoverable once you document the work. Try the <a href="/tools/depreciation-calculator/">depreciation calculator</a>.</p>'],
        ['How long does the insurer have to pay in Texas?', '<p>Texas’s Prompt Payment of Claims Act sets deadlines for acknowledging, deciding and paying claims. Map yours with the <a href="/tools/claim-deadline-calculator/">claim deadline calculator</a>.</p>'],
        ['Should I give the insurer a recorded statement?', '<p>You must cooperate with your insurer, but you can prepare first. Stick to facts, don’t guess about causes or amounts, and consider talking to a public adjuster beforehand.</p>'],
    ],
    'Storms & coverage in Sugar Land' => [
        ['Is hurricane damage covered by my homeowners policy?', '<p>Wind damage generally is—Fort Bend County is outside the TWIA coastal area, so wind coverage comes from your regular policy, often with a percentage wind/hail or named-storm deductible. Rising water requires separate flood insurance.</p>'],
        ['Is a burst pipe covered?', '<p>Sudden and accidental water discharge is generally covered; long-term leaks and seepage often are not. See <a href="/services/water-damage-claims/">water damage claims</a>.</p>'],
        ['Does homeowners insurance cover flooding from the Brazos River?', '<p>No. River and surface flooding is excluded from standard homeowners policies and covered only by NFIP or private flood insurance. See <a href="/services/flood-damage-claims/">flood claims</a>.</p>'],
        ['Where can I check the weather and alerts for Sugar Land?', '<p>Our <a href="/sugar-land-weather/">live storm center</a> shows current conditions, NWS alerts, radar, the tropical outlook and the Brazos River gauge.</p>'],
    ],
];
$all = [];
foreach ($sections as $qs) { $all = array_merge($all, $qs); }
page_start([
    'title' => 'Public Adjuster FAQ | Sugar Land Public Adjuster',
    'description' => 'Answers from a Sugar Land public adjuster: fees, licensing, denied claims, depreciation, hurricane and flood coverage, and Texas claim deadlines.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
    'schema' => [faq_schema($all, $path)],
]);
page_hero('Frequently Asked Questions', 'Straight answers about public adjusters, insurance claims and storm coverage in Sugar Land, Texas.', $crumbs, 'Sugar Land Public Adjuster');
?>
<div class="container content-layout">
  <div class="prose">
<?php foreach ($sections as $title => $qs): ?>
    <h2><?= e($title) ?></h2>
    <?php faq_list($qs); ?>
<?php endforeach; ?>
  </div>
  <?php sidebar_cta(); ?>
</div>
<?php page_end(); ?>
