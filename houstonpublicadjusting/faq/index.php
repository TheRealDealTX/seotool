<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['FAQ', '/faq/']];
$groups = [
    'Hiring a public adjuster in Houston' => [
        ['What is a public adjuster?', 'A public adjuster is a licensed insurance professional who represents the policyholder in a property insurance claim. We inspect the damage, interpret the policy, prepare and document the claim, and negotiate with the insurance company. <a href="/understanding-what-is-public-adjuster/">Read the full guide</a>.'],
        ['Why hire Houston public adjusters instead of handling the claim myself?', 'The insurance company has trained adjusters, estimators and engineers on its side. Houston public adjusters give you the same expertise: a complete estimate, policy knowledge and a negotiator who does this every day. Many policyholders also simply don’t have the time to manage a large claim.'],
        ['How much does a public adjuster cost in Texas?', 'Nothing upfront. Public adjusters are paid a percentage of the settlement, and Texas law caps that fee at 10%. If nothing is recovered, nothing is owed. Try our <a href="/tools/public-adjuster-fee-calculator/">fee calculator</a>.'],
        ['Is a public adjuster in Houston, TX licensed?', 'Every public adjuster in Texas must be licensed by the Texas Department of Insurance. Houston Public Adjusters works under Rise Public Adjusting LLC, license #3356839.'],
        ['Will hiring a public adjuster delay my claim?', 'Usually the opposite. A complete, well-documented claim gives the insurer fewer reasons to request more information, re-inspect or delay.'],
        ['Is a public adjuster the same as an attorney?', 'No. Public adjusters handle the claim itself: documentation, estimating and negotiation. We do not give legal advice or file lawsuits. If a dispute needs an attorney, we will tell you.'],
    ],
    'Claims and coverage' => [
        ['My claim was denied. Can you still help?', 'Yes. We review the denial letter, inspect the damage, compare the carrier’s reasons with the policy and Texas law, and advise on the next step: a re-inspection, a supplement, appraisal, or other options.'],
        ['Can a settled claim be reopened?', 'Often. If hidden damage was found during repairs or the original estimate was incomplete, the claim may be supplemented or reopened within the policy’s time limits.'],
        ['Does homeowners insurance cover flood damage in Houston?', 'No. Rising water is excluded from standard homeowners policies and requires separate flood insurance through the NFIP or a private flood carrier. Wind-driven rain and burst pipes are generally covered under the homeowners policy.'],
        ['What is a hurricane deductible?', 'A separate deductible, usually 1%–5% of your dwelling coverage, that applies to named-storm damage. Use our <a href="/tools/hurricane-deductible-calculator/">hurricane deductible calculator</a> to see it in dollars.'],
        ['What is recoverable depreciation?', 'The amount withheld from your first check for the age of damaged items. On a replacement-cost policy it is paid once repairs are completed. See the <a href="/tools/claim-settlement-calculator/">settlement calculator</a>.'],
        ['How long does a Texas insurer have to pay a claim?', 'Generally 5 business days after accepting it; acceptance must come within 15 business days of receiving everything the insurer requested (with a possible 45-day extension). Use the <a href="/tools/claim-deadline-calculator/">deadline calculator</a>.'],
    ],
    'Working with us' => [
        ['What areas do you serve?', 'Houston and the surrounding area, including Katy, Sugar Land, The Woodlands, Cypress, Spring, Pearland, Pasadena, Humble, Kingwood, League City, Baytown and Galveston. <a href="/service-areas/">See all areas</a>.'],
        ['What should I have ready when I call?', 'Whatever you have: photos of the damage, your claim number, the insurer’s estimate or letters, contractor bids and your policy. If you have nothing yet, call anyway — we can start from the beginning.'],
        ['How do I get started?', 'Call or text (832) 503-5866, email jditt@risepublicadjusting.com, or fill out the <a href="/contact/">contact form</a>. The first review is free.'],
    ],
];
$all = array_merge(...array_values($groups));
page_start([
    'title' => 'Public Adjuster FAQ: Houston Insurance Claim Questions Answered',
    'desc' => 'Answers from Houston Public Adjusters on public adjuster fees, licensing, denied claims, hurricane deductibles, flood coverage, depreciation and Texas claim deadlines.',
    'path' => '/faq/',
    'crumbs' => $crumbs,
    'schema' => [faq_schema($all)],
]);
echo page_hero('Public Adjuster FAQ', 'Straight answers to the questions Houston homeowners and business owners ask us most about insurance claims and hiring a public adjuster.', $crumbs);
?>
<div class="wrap layout-sidebar">
  <div class="prose">
<?php foreach ($groups as $title => $faqs): ?>
    <h2><?= e($title) ?></h2>
    <?= faq_html($faqs) ?>
<?php endforeach; ?>
  </div>
  <aside class="sidebar"><div class="side-card sticky"><?= lead_form('lead-faq', 'Still have questions?', 'Ask a licensed Houston public adjuster &mdash; free.', true) ?></div></aside>
</div>
<?php
page_end();
