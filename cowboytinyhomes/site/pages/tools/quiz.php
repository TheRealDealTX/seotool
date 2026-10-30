<?php
$GLOBALS['scripts'][] = 'tools.js';
hero([
    'eyebrow' => 'Free Tool',
    'h1'      => 'Which Tiny Home Is Right for Me?',
    'lead'    => 'Answer six quick questions about your land, lifestyle and budget. In about 60 seconds you will see how well a tiny home on wheels, park model, ADU or custom foundation home fits you.',
    'image'   => 'Tiny-Homes-On-Wheels.webp',
    'cta'     => false,
]);
// Each option: [label, hint, score string "type:points,..."]
$questions = [
    ['Where will your tiny home go?', [
        ['In the backyard of a house I own', 'A city or suburban lot with an existing home', 'adu:3,custom:1'],
        ['On my own rural or ranch land', 'Acreage, likely outside city limits', 'custom:3,park:2,thow:1'],
        ['In an RV park or tiny home community', 'Renting a lot with hookups', 'thow:3,park:3'],
        ['I do not have land yet', 'Still shopping or keeping options open', 'thow:3,park:1,custom:1'],
    ]],
    ['How important is being able to move the home?', [
        ['Very — I may relocate in the next few years', 'Moving with work, family or the seasons', 'thow:4'],
        ['Nice to have, but not often', 'Maybe once, with a professional hauler', 'park:3,thow:1'],
        ['Not important — it is staying put', 'Permanent home or backyard unit', 'adu:3,custom:3'],
    ]],
    ['How will you mainly use it?', [
        ['My full-time, primary home', 'Living in it year-round', 'custom:3,thow:1,adu:1'],
        ['A guest house or space for family', 'Parents, adult kids or visitors', 'adu:4'],
        ['Rental income', 'Long-term tenants or short-term guests', 'adu:3,park:2'],
        ['A weekend, hunting or lake getaway', 'Part-time use', 'park:3,thow:2'],
    ]],
    ['What is your rough budget for the home (not land)?', [
        ['Under $70,000', 'Keep it simple and efficient', 'thow:3,park:3'],
        ['$70,000 – $150,000', 'Room for good finishes or a foundation', 'park:1,thow:2,adu:2,custom:1'],
        ['$150,000 – $300,000', 'A roomy ADU or small custom home', 'adu:3,custom:3'],
        ['$300,000 or more', 'Larger custom home with premium details', 'custom:4,adu:1'],
    ]],
    ['How many people will live or stay there?', [
        ['Just me', 'A studio or sleeping loft works', 'thow:3,park:2,adu:1'],
        ['Two of us', 'One bedroom or a bedroom plus loft', 'park:2,adu:2,thow:2,custom:1'],
        ['Three or four, or I need 2+ bedrooms', 'Real bedrooms and storage', 'custom:3,adu:2'],
    ]],
    ['How do you plan to pay for it?', [
        ['Cash or savings', 'No lender involved', 'thow:2,park:2,adu:1,custom:1'],
        ['RV or personal loan', 'Shorter-term financing', 'thow:3,park:3'],
        ['Home equity (HELOC or cash-out refi)', 'Borrowing against my current home', 'adu:4'],
        ['A mortgage or construction loan', 'Traditional long-term financing', 'custom:4,adu:2'],
    ]],
];
?>
<section class="section">
  <div class="wrap">
    <div class="quiz tool-panel" data-tool="quiz">
      <div class="quiz-progress" aria-hidden="true"><i></i></div>
<?php foreach ($questions as $i => [$q, $opts]): ?>
      <div class="quiz-q" role="group" aria-labelledby="quiz-q<?= $i ?>">
        <p class="eyebrow" style="color:var(--gold-dark)">Question <?= $i + 1 ?> of <?= count($questions) ?></p>
        <h2 id="quiz-q<?= $i ?>"><?= e($q) ?></h2>
        <div class="quiz-opts">
<?php foreach ($opts as [$label, $hint, $score]): ?>
          <button type="button" class="quiz-opt" data-score="<?= $score ?>"><?= e($label) ?><small><?= e($hint) ?></small></button>
<?php endforeach; ?>
        </div>
      </div>
<?php endforeach; ?>
      <button type="button" class="btn btn--outline btn--sm" data-quiz-back hidden>← Back</button>
      <div class="quiz-result" aria-live="polite">
        <p class="eyebrow" style="color:var(--gold-dark)">Your best match</p>
        <h2 data-out="top">—</h2>
        <p data-out="why"></p>
        <div data-out="bars"></div>
        <div class="btn-row">
          <a class="btn btn--ink" data-out="top-link" href="/">Learn About This Home</a>
          <a class="btn btn--gold" data-out="quote" href="/contact-us/">Talk to a Designer</a>
          <button type="button" class="btn btn--outline" data-quiz-restart>Retake the Quiz</button>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--narrow prose">
    <h2>How the Tiny Home Quiz Works</h2>
    <p>"Which tiny home is right for me?" is the first question almost every caller asks Cowboy Tiny Homes, and the honest answer is: it depends on a handful of practical factors. This quiz scores your answers against the four main ways to build small in Texas, then ranks them by how well they fit. Each answer gives points to the home types it suits — for example, "I may relocate" strongly favors a tiny home on wheels, while "borrowing against my current home" points toward a backyard ADU.</p>
    <p>Your match percentage compares each type's score to the highest possible score, so two types can both rank well. That is common, and it usually means you have a real choice to make based on design preferences or local rules.</p>

    <h2>The Four Tiny Home Types</h2>
    <h3>Tiny home on wheels (THOW)</h3>
    <p>Built on a bumper-pull or gooseneck trailer, usually 8.5 feet wide so it can be towed without special permits, and typically 120 to 400 square feet including lofts. In much of Texas a THOW is treated as a recreational vehicle, which can make it easier to place in RV parks or on rural land — and harder to place in a city neighborhood. See <a href="/tiny-homes-on-wheels-texas/">tiny homes on wheels in Texas</a>.</p>
    <h3>Park model home</h3>
    <p>A cabin-style unit on a chassis, generally kept under 400 square feet. Park models are wider than a towable tiny house, feel more like a small cottage inside, and are usually moved only once to an RV park, ranch or lake lot. See <a href="/park-model-homes-texas/">park model homes in Texas</a>.</p>
    <h3>ADU, casita or granny flat</h3>
    <p>A permanent accessory dwelling unit built on a foundation behind or beside a main house. ADUs are ideal for multigenerational living, guests or rental income, and they add lasting property value. Local zoning controls size, setbacks and whether you can rent it. See <a href="/adu-builders-texas/">ADU builders in Texas</a>.</p>
    <h3>Custom tiny or small home on a foundation</h3>
    <p>A stand-alone house on its own lot, built to the International Residential Code. This is the most straightforward path to full-time living, conventional mortgages and resale. See <a href="/custom-tiny-homes-texas/">custom tiny homes in Texas</a>.</p>

    <h2>What to Do With Your Result</h2>
    <p>Treat the quiz as a starting point. Before you commit, confirm that your land and city allow the home type you chose — our guide to <a href="/guides/tiny-house-laws-texas/">tiny house laws in Texas</a> explains permits, zoning and HOA rules — and price it with the <a href="/tools/tiny-home-cost-calculator/">tiny home cost calculator</a>. For a deeper side-by-side, read <a href="/guides/adu-vs-park-model-vs-tiny-house-on-wheels/">ADU vs park model vs tiny house on wheels</a>.</p>
    <p>Still between two options? That is exactly what the free Cowboy Tiny Homes consultation is for. Share your result and we will look at your property, budget and goals together.</p>
  </div>
</section>

<?php faq_section([
    ['Is a tiny home on wheels or a foundation tiny home better?',
     '<p>Neither is better for everyone. Wheels give you flexibility and often fewer permitting hurdles outside cities; a foundation gives you easier financing, stronger resale and a clearer path to full-time legal living inside city limits.</p>'],
    ['Can I live full-time in a park model home in Texas?',
     '<p>Many people do, typically in RV parks or on rural land that allows it. Park models are designed as recreational dwellings, so check the park rules, county requirements and any deed restrictions before planning full-time use.</p>'],
    ['What is the best tiny home for rental income?',
     '<p>A permanent ADU on a property you already own is usually the strongest rental option because it can be financed with home equity and rented long-term or short-term where local rules allow. Run your numbers with our <a href="/tools/adu-rental-income-calculator/">ADU rental income calculator</a>.</p>'],
    ['What if the quiz gives me two close matches?',
     '<p>That is normal. Close scores mean both options could work, and the deciding factors are usually local zoning, financing and personal taste. A Cowboy Tiny Homes designer can help you weigh them for your specific property.</p>'],
], 'Tiny Home Quiz FAQs'); ?>

<?php related([
    '/guides/adu-vs-park-model-vs-tiny-house-on-wheels/',
    '/tools/tiny-home-cost-calculator/',
    '/tools/tiny-house-size-planner/',
    '/guides/tiny-house-laws-texas/',
], 'Next Steps After the Quiz'); ?>

<?php cta_band('Found Your Match? Let’s Design It.'); ?>
