<?php
require dirname(__DIR__) . '/includes/layout.php';

$crumbs = [['FAQs', '/faqs/']];
page_start([
    'title' => 'Roofing FAQs | Austin Roofing Answers Your Roof Questions',
    'description' => 'Answers to common roofing questions in Austin, TX: free inspections, repair vs replace, hail damage, insurance claims, roof lifespans, costs and commercial roofing.',
    'path' => '/faqs/',
    'crumbs' => $crumbs,
    'body_class' => 'page-faq faq-page',
]);
page_hero('Austin Roofing FAQs', [
    'crumbs' => $crumbs,
    'eyebrow' => 'Straight answers from Austin roofers',
    'lead' => 'Storm damage, aging materials or a big commercial project — you deserve clear answers, not jargon or surprise costs. Here are the questions Austin Roofing hears most often.',
]);

$groups = [
    'Inspections & Quotes' => [
        ['Do you really offer free roof inspections and quotes?', '<p>Yes. Every inspection and estimate from Austin Roofing is 100% free with no obligation. We believe you should understand your roof’s condition before making any decision.</p>'],
        ['What happens during a roof inspection?', '<p>We check shingles or membrane, flashing, drip edge, gutters, vents, pipe boots and skylights, look for hail, wind and UV damage, and check the attic for moisture and ventilation where accessible. You get a photo report and clear options. <a href="/services/roof-inspection/">More on our inspections</a>.</p>'],
        ['How long does an inspection take?', '<p>Most residential inspections take 30–60 minutes. Large commercial roofs take longer depending on size and access.</p>'],
    ],
    'Repair or Replace' => [
        ['How do I know if my roof needs to be repaired or replaced?', '<p>We evaluate the roof’s age, material condition, storm damage, leaks and structure. Many roofs only need a repair or restoration — we recommend replacement only when it is the most cost-effective option. Try our <a href="/roofing-tools/repair-or-replace-quiz/">repair or replace quiz</a> for a quick read.</p>'],
        ['What are the most common signs of roof damage?', '<p>Missing or curling shingles, leaks and ceiling stains, heavy granule loss in gutters, cracked flashing, sagging areas and visible hail marks on metal vents or gutters. If you are unsure, an inspection will identify the cause and severity.</p>'],
        ['What should I do if I notice a roof leak?', '<p>Move valuables, catch the water and call us right away — even small leaks spread quickly. We will locate the source and stop further damage with a temporary or permanent <a href="/services/roof-repair/">roof repair</a>.</p>'],
        ['How long does a typical roof replacement take?', '<p>Most residential replacements take one to two days. Commercial projects vary with size, structure and weather; we provide a detailed timeline before work begins.</p>'],
    ],
    'Storms, Hail & Insurance' => [
        ['How quickly can you respond after a storm?', '<p>We offer priority scheduling for wind and hail damage and 24/7 emergency service. After major Austin storms our team performs same-day or next-day inspections whenever possible.</p>'],
        ['How can I tell if hail has damaged my roof?', '<p>Hail causes granule loss, soft or bruised spots, cracked shingles, dents in metal and leaks — often invisible from the ground. Check dented gutters, AC fins and vents as clues, or use our <a href="/roofing-tools/hail-damage-checker/">hail damage checker</a>, then schedule a professional inspection.</p>'],
        ['Do you work with insurance claims?', '<p>Yes. We are not adjusters, but we provide documentation, photos and roof reports and can meet your insurance adjuster so they see the actual damage. <a href="/services/roof-insurance-claims/">How our claim help works</a>.</p>'],
        ['Does homeowners insurance cover roof damage in Texas?', '<p>Most policies cover sudden damage from hail and wind, minus your deductible, but not wear and tear. Coverage type (actual cash value vs replacement cost) and wind/hail deductibles vary by policy. Read our guide to <a href="/blog/insurance-coverage-for-storm-damaged-roofs/">insurance coverage for storm-damaged roofs</a>.</p>'],
    ],
    'Materials & Lifespan' => [
        ['What roofing materials do you work with?', '<p>Asphalt and composition shingles (3-tab, architectural and Class 4 impact-resistant), metal roofing including standing seam and stone-coated steel, TPO, EPDM, modified bitumen, built-up roofing and commercial flat-roof systems.</p>'],
        ['How long do roofs last in Austin’s climate?', '<p>Asphalt shingles typically last 15–25 years here, metal roofs 40+ years, and commercial flat roofs 20–30 years with proper maintenance. Heat, storms and UV significantly affect lifespan — estimate yours with our <a href="/roofing-tools/roof-lifespan-calculator/">roof lifespan calculator</a>.</p>'],
        ['Are impact-resistant shingles worth it in Austin?', '<p>For many Austin homes, yes. Class 4 shingles resist hail far better than standard shingles, and some insurers offer premium discounts for them — ask your agent.</p>'],
        ['What is a roofing square?', '<p>A square is 100 square feet of roof surface. Roofers price materials and labor per square. <a href="/blog/what-is-a-square-in-roofing/">Learn how to calculate squares</a>.</p>'],
    ],
    'Commercial & Multi-Family' => [
        ['Do you offer commercial roofing services?', '<p>Absolutely. Our commercial team handles repair, restoration, replacement, coatings and maintenance for retail centers, warehouses, offices, restaurants, industrial buildings and more. <a href="/services/commercial-roofing/">Austin commercial roofing</a>.</p>'],
        ['What are the benefits of a commercial roof coating?', '<p>Coatings can add 10–20 years of service life, reduce cooling costs, stop leaks and avoid a full tear-off. They work best on flat or low-slope roofs that are still structurally sound.</p>'],
        ['Do you roof multi-family properties?', '<p>Yes — apartments, townhomes, condos, duplexes and HOA-managed communities, scheduled to minimize resident disruption with consistent quality across every building.</p>'],
    ],
    'Working With Us' => [
        ['Do you follow building codes and manufacturer guidelines?', '<p>Yes. All installations meet or exceed local building codes, and we use approved methods that keep manufacturer warranties valid.</p>'],
        ['Will you clean up after the job?', '<p>Absolutely. We do a full cleanup including magnetic nail sweeps, debris removal and a final walkthrough of the work area.</p>'],
        ['Which areas do you serve?', '<p>Austin and surrounding Central Texas cities including Round Rock, Pflugerville, Cedar Park, Leander, Georgetown, Hutto, Kyle, San Marcos, Dripping Springs, Lockhart and Bastrop. <a href="/service-areas/">See all service areas</a>.</p>'],
    ],
];
?>
<div class="container layout-sidebar">
  <article class="prose">
    <nav class="toc" aria-label="FAQ topics"><p class="toc__title">Jump to a topic</p><ol>
      <?php foreach (array_keys($groups) as $g): ?><li><a href="#<?= e(strtolower(preg_replace('/[^a-z0-9]+/i', '-', $g))) ?>"><?= e($g) ?></a></li><?php endforeach; ?>
    </ol></nav>
    <?php
    $all = [];
    foreach ($groups as $g => $faqs) {
        $id = strtolower(preg_replace('/[^a-z0-9]+/i', '-', $g));
        echo '<section class="faq" id="' . e($id) . '"><h2>' . e($g) . '</h2><div class="faq__list">';
        foreach ($faqs as [$q, $a]) {
            echo '<details class="faq__item"><summary>' . e($q) . '</summary><div class="faq__a">' . $a . '</div></details>';
            $all[] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(strip_tags($a))]];
        }
        echo '</div></section>';
    }
    add_schema(['@type' => 'FAQPage', '@id' => abs_url('/faqs/#faq'), 'mainEntity' => $all]);
    ?>
    <p style="margin-top:2em"><strong>Still have a question?</strong> <a href="/contact-us/">Contact us today for your free inspection and quote</a> or call <?= phone_link() ?>.</p>
  </article>
  <?php sidebar(['links' => service_links(['roof-repair', 'roof-replacement', 'hail-damage-repair', 'roof-insurance-claims', 'commercial-roofing'])]); ?>
</div>
<?php
cta_band();
page_end();
