<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['FAQ', '/faq/']];
$groups = [
    'Repair & Replacement' => [
        ['q' => 'How do I know if my roof needs repair or replacement?', 'a' => 'It depends on the roof\'s age, overall condition and how widespread the problem is. Isolated damage on a younger roof is usually repairable. Recurring leaks, brittle or balding shingles across the roof, or soft decking in several places usually point to replacement. Our repair-or-replace quiz is a good starting point.'],
        ['q' => 'How long does a roof last in Bastrop, TX?', 'a' => 'Architectural shingles typically last around 18 to 25 years in Central Texas heat with good ventilation. Standing seam metal often lasts 40 to 60 years. Hail, poor ventilation and heavy pine debris can shorten any roof\'s life.'],
        ['q' => 'How long does a roof replacement take?', 'a' => 'Most homes in Bastrop are replaced in one to two days once materials arrive. Larger or steeper roofs and most metal roofs take longer. We dry the roof in every evening and never tear off with rain in the forecast.'],
        ['q' => 'What are common signs a roof needs attention?', 'a' => 'Missing or lifted shingles, ceiling stains, recurring leaks, worn flashing, granules collecting near downspouts, cracked pipe boots, sagging areas and visible aging across large sections of the roof.'],
    ],
    'Metal Roofing' => [
        ['q' => 'Is metal roofing worth it in Bastrop?', 'a' => 'For many homeowners, yes. Bastrop metal roofing reflects summer heat, resists wind, sheds pine needles and can carry a Class A fire rating. It costs more up front but often outlasts two shingle roofs, so the lifetime cost can be lower.'],
        ['q' => 'What is the difference between standing seam and R-panel?', 'a' => 'Standing seam uses concealed clips and raised seams with no exposed screws, which means less maintenance and a premium look. R-panel uses exposed fasteners, costs less and installs faster, but the screws need periodic inspection and replacement.'],
        ['q' => 'Does a metal roof attract lightning?', 'a' => 'No. Metal roofs do not make a home more likely to be struck by lightning. If lightning does strike, a metal roof is non-combustible, which is an advantage over many other materials.'],
    ],
    'Storms & Insurance' => [
        ['q' => 'Should I have my roof inspected after hail or strong wind?', 'a' => 'Yes. Hail and wind damage are often invisible from the ground and can take months to cause leaks. A prompt inspection documents damage while it can still be reported under most policies\' timelines.'],
        ['q' => 'Will insurance pay for my new roof?', 'a' => 'Many homeowner policies cover sudden storm damage such as hail and wind, but coverage, deductibles and exclusions vary. We document damage and can meet your adjuster; your insurer decides what is covered.'],
        ['q' => 'What should I do if my roof is leaking during a storm?', 'a' => 'Stay off the roof. Contain water with buckets and towels, move valuables, shut off power near any leak by electrical fixtures, photograph everything and call us at (512) 297-7580 for emergency tarping.'],
    ],
    'Working With Bastrop Roofing' => [
        ['q' => 'What types of projects can I contact Bastrop Roofing about?', 'a' => 'Roof repair, replacement planning, inspections, storm and hail damage, metal roofing, shingle roofing, commercial roofing and general roof maintenance for homes and businesses across Bastrop County.'],
        ['q' => 'Are your estimates free?', 'a' => 'Yes. Inspections and written estimates for repairs, replacements and storm damage are free with no obligation. Detailed reports for real estate transactions may carry a fee, which we will tell you about first.'],
        ['q' => 'How do I contact a Bastrop roofer?', 'a' => 'Call Bastrop Roofing at (512) 297-7580, email info@bastroproofs.com, or use the estimate form on our contact page to describe your property and roofing concern.'],
    ],
];
$all = array_merge(...array_values($groups));
page_start([
    'title'       => 'Roofing FAQ | Bastrop Roofing Questions Answered',
    'description' => 'Answers to common roofing questions from Bastrop, TX homeowners: repair vs. replacement, metal roofing, hail damage, insurance claims and estimates.',
    'path'        => '/faq/',
    'schema'      => [breadcrumb_schema($crumbs), faq_schema($all)],
]);
page_hero('Bastrop Roofing FAQ', 'Roofing Questions, Answered', 'Straightforward answers to the questions Bastrop homeowners ask us most about repairs, metal roofing, storms and insurance.', $crumbs);
?>
<section class="section">
  <div class="container narrow">
<?php foreach ($groups as $title => $faqs): ?>
    <h2 class="faq-group-title reveal"><?= e($title) ?></h2>
    <div class="faq-list">
<?php foreach ($faqs as $f): ?>
      <details class="faq-item reveal">
        <summary><?= e($f['q']) ?><span class="faq-icon" aria-hidden="true"></span></summary>
        <div class="faq-answer"><p><?= e($f['a']) ?></p></div>
      </details>
<?php endforeach; ?>
    </div>
<?php endforeach; ?>
  </div>
</section>
<?php cta_band('Still Have a Roofing Question?', 'Call (512) 297-7580 or email info@bastroproofs.com and tell us what is happening with your roof.'); page_end();
