<?php
$faqs = [
    ['q' => 'Are these jobs in Texas?', 'a' => 'Yes. Best Jobs Pro recruits for employers across Texas. Openings change often, so if you do not see the right fit, apply anyway and choose "Other." A recruiter will contact you when a matching job opens.'],
    ['q' => 'Do I need experience to apply?', 'a' => 'Not always. Roles like packer/stocker, housekeeping, food service and general labor often welcome beginners. Skilled roles such as welding, carpentry, CDL driving and mechanical maintenance require relevant experience or credentials.'],
    ['q' => 'How much does it cost to apply?', 'a' => 'Nothing. Best Jobs Pro does not charge job seekers any employment or processing fees.'],
];
$catIcon = ['office' => 'briefcase', 'labor' => 'package', 'trades' => 'wrench', 'customer' => 'headset', 'driving' => 'truck'];
page_start([
    'title'       => 'Job Postings in Texas | Now Hiring | Best Jobs Pro',
    'description' => 'Browse current Texas job postings from Best Jobs Pro: admin, accounting, warehouse, welding, carpentry, CDL driving and more. Apply free in 5 minutes.',
    'path'        => '/job-postings/',
    'crumbs'      => [['Job Postings', '/job-postings/']],
    'schema'      => [faq_schema($faqs), [
        '@type' => 'ItemList', 'name' => 'Best Jobs Pro job openings in Texas',
        'itemListElement' => array_map(fn($j, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $j[0]], JOBS, array_keys(JOBS)),
    ]],
]);
page_hero('Job Postings in Texas', 'We track Texas employers and keep an up-to-date list of openings, then match each candidate with companies that fit their skills and goals. Search, filter and apply in minutes.', [['Job Postings', '/job-postings/']], '/assets/img/site/job-postings-bg-copy.webp', 'Now hiring');
?>
<section class="section">
  <div class="wrap" data-jobboard>
    <div class="jobbar reveal">
      <label class="jobbar__search"><?= icon('search') ?><input id="job-search" type="search" placeholder="Search jobs, e.g. welder, warehouse, receptionist" aria-label="Search jobs"></label>
      <div class="filters" role="group" aria-label="Filter by category">
        <button type="button" data-filter="all" aria-pressed="true">All</button>
<?php foreach (JOB_CATEGORIES as $k => $label): ?>
        <button type="button" data-filter="<?= $k ?>" aria-pressed="false"><?= e($label) ?></button>
<?php endforeach; ?>
      </div>
    </div>
    <p class="jobs-count" aria-live="polite">Showing <strong data-jobcount><?= count(JOBS) ?></strong> Best Jobs Pro opportunities</p>
    <div class="jobs">
<?php foreach (JOBS as [$name, $cat, $type, $desc]): ?>
      <article class="job-card" data-cat="<?= $cat ?>">
        <div class="job-card__top"><span class="job-card__ico"><?= icon($catIcon[$cat]) ?></span><h2 style="font-size:1.05rem;margin:0"><?= e($name) ?></h2></div>
        <p><?= e($desc) ?></p>
        <div class="job-card__tags"><span class="tag tag--brand"><?= e(JOB_CATEGORIES[$cat]) ?></span><span class="tag"><?= e($type) ?></span><span class="tag">Texas</span></div>
        <a class="more" href="/applications/?job=<?= urlencode($name) ?>#apply-form">Apply for this job <?= icon('arrow') ?></a>
      </article>
<?php endforeach; ?>
    </div>
    <div class="jobs-empty" hidden><p><strong>No openings match that search right now.</strong></p><p>Apply anyway and choose "Other." We will call you when a matching job comes in.</p><a class="btn btn--sm" href="/applications/">Apply now</a></div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Not sure which job to pick?</p>
      <h2>Find your best-fit job in 60 seconds</h2>
      <p>Answer six quick questions about how you like to work. The quiz points you to the job types that suit you and the Best Jobs Pro openings that match.</p>
      <ul class="checks"><li>No sign-up, no email required</li><li>Results instantly</li><li>Apply straight from your results</li></ul>
    </div>
    <div class="reveal"><?= tool_widget('job-quiz', true) ?></div>
  </div>
</section>

<section class="section">
  <div class="wrap"><?= faq_block($faqs, 'Job posting FAQs') ?></div>
</section>
<?= cta_band('Questions about a job posting?', 'Call ' . SITE_PHONE . ' for details on any opening, 24/7. Applying is always free.') ?>
<?php page_end(['/assets/js/tools.js']);
