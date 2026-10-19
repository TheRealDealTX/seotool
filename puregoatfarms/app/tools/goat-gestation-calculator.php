<?php
defined('PGF') || exit;
ob_start(); ?>
<div class="tool__fields tool__fields--row">
  <div class="field"><label for="ge-date">Breeding date</label><input id="ge-date" type="date"></div>
  <div class="field"><label for="ge-breed">Breed type</label>
    <select id="ge-breed"><option value="150" selected>Standard dairy or meat (≈150 days)</option><option value="145">Nigerian Dwarf / Pygmy (≈145 days)</option></select></div>
  <div class="field"><label for="ge-name">Doe's name <span class="opt">(optional)</span></label><input id="ge-name" type="text" maxlength="40" placeholder="e.g. Clover"></div>
</div>
<div class="due-card" aria-live="polite">
  <div><p class="out-label">Estimated kidding date</p><p class="out-big" id="ge-due">—</p><p class="out-sub" id="ge-window"></p></div>
  <div class="due-card__count"><strong id="ge-count">—</strong><span id="ge-count-l">days to go</span></div>
</div>
<div class="gest-bar" aria-hidden="true"><span class="gest-bar__fill" id="ge-progress"></span><span class="gest-bar__today" id="ge-today"></span></div>
<ol class="timeline-list" id="ge-timeline"></ol>
<p class="center"><button type="button" class="btn btn--ghost btn--sm" id="ge-ics"><?= icon('calendar') ?> Add these dates to my calendar (.ics)</button></p>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Goat Gestation Calculator — Kidding Date & Timeline | Pure Goat Farms',
    'desc'  => 'Free goat gestation calculator: enter a breeding date to get the kidding due date (about 150 days), the due-date window, dry-off, CDT booster and kidding-prep timeline.',
    'intro' => 'Enter the date your doe was bred and get her kidding date, the normal 145–155 day window, and a timeline of everything to do before the kids arrive — dry-off, booster, feed changes and kidding kit.',
    'widget' => $widget,
    'how' => '<h2>How long is a goat pregnant?</h2>
<p>Goat gestation averages about <strong>150 days</strong> — roughly five months — with a normal range of 145 to 155 days. Smaller breeds such as Nigerian Dwarfs and Pygmies often kid a few days earlier, around 145 days.</p>
<h2>What the timeline includes</h2>
<ul>
<li><strong>Heat check (days 18–24):</strong> if she comes back into heat, she probably did not settle.</li>
<li><strong>Pregnancy test (day 30+):</strong> a blood test can confirm pregnancy from about 30 days after breeding; ultrasound from about 45 days.</li>
<li><strong>Dry off (≈60 days before kidding):</strong> stop milking so the udder can rest and rebuild. See <a href="/do-goats-produce-milk-without-being-pregnant/">why goats need a dry period</a>.</li>
<li><strong>Increase nutrition (last 6–8 weeks):</strong> most fetal growth happens late in pregnancy.</li>
<li><strong>CDT booster (≈30 days before):</strong> boosts antibodies passed to kids through colostrum. Follow your vet\'s protocol.</li>
<li><strong>Kidding kit and pen (≈10 days before):</strong> clean, dry kidding pen and supplies ready.</li>
</ul>',
    'faq' => [
        ['How long is a goat pregnant?', 'About 150 days on average, with 145 to 155 days considered normal. Nigerian Dwarf and Pygmy goats often kid closer to 145 days.'],
        ['When should I dry off a pregnant doe?', 'Most keepers stop milking about 60 days (two months) before the expected kidding date, so the udder can rest and prepare for the next lactation.'],
        ['What are signs a goat will kid soon?', 'Common signs include a full, tight udder ("strutted" teats), loosened tail ligaments, a sunken look around the tail head, restlessness, pawing at bedding and talking to her belly.'],
    ],
    'posts' => ['do-goats-produce-milk-without-being-pregnant', 'how-often-do-you-milk-a-goat'],
];
