<?php defined('NHS') || exit;

/* ---------------- Home ---------------- */

function view_home(): never {
    $latest = array_slice(posts_in('building-tips'), 0, 6);
    $pillars = [
        ['how-to-be-your-own-general-contractor', 'Be your own general contractor', 'tool'],
        ['how-much-does-it-cost-to-build-a-house-in-texas', 'What it costs to build in Texas', 'chart'],
        ['new-home-construction-timeline', 'The construction timeline', 'clip'],
        ['new-construction-inspection-checklist', 'Inspection checklist', 'check'],
        ['how-to-finance-building-a-house', 'How to finance your build', 'house'],
        ['navigating-texas-building-codes-what-you-need-to-know', 'Texas building codes', 'shield'],
    ];
    ob_start(); ?>
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Training &amp; resources for new home builders</p>
      <h1>Design and build the home of your dreams — without overpaying for it</h1>
      <p class="lead">New Home Investing Knowledge is an online platform that gives new home builders the training, resources and guidance to build their dream home. Whether you're hiring a general contractor, acting as your own, or starting a home-building business, we'll show you how to do it right.</p>
      <div class="hero-actions">
        <a class="btn btn-lg" href="/free-training/">Get the free owner-builder course</a>
        <a class="btn btn-ghost btn-lg" href="/build-a-home-yourself/">How owner-building works</a>
      </div>
      <ul class="hero-points">
        <li><?= icon('check') ?> Make sure your contractor builds it correctly</li>
        <li><?= icon('check') ?> Build without a general contractor — no experience required</li>
        <li><?= icon('check') ?> Launch your own home construction business</li>
      </ul>
    </div>
    <figure class="hero-photo">
      <img src="/assets/img/photos/home-hero.webp" alt="White farmhouse-style new home with a wraparound front porch and green lawn" width="1024" height="576" fetchpriority="high">
      <figcaption><?= icon('house') ?> Your dream home, built right</figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How we help</p>
      <h2 class="section-title">Three ways to build smarter</h2>
    </div>
    <div class="feature-grid">
      <div class="feature"><span class="feature-icon"><?= icon('shield') ?></span><h3>Hiring a builder?</h3><p>Learn what to put in the contract, what to inspect at each phase, and how to catch problems before the drywall goes up.</p><a class="text-link" href="/new-construction-inspection-checklist/">Inspection checklist &rarr;</a></div>
      <div class="feature"><span class="feature-icon"><?= icon('tool') ?></span><h3>Building it yourself?</h3><p>An owner-builder manages the subs instead of paying a general contractor's margin. We teach the scheduling, bidding and permitting.</p><a class="text-link" href="/how-to-be-your-own-general-contractor/">Owner-builder guide &rarr;</a></div>
      <div class="feature"><span class="feature-icon"><?= icon('chart') ?></span><h3>Building a business?</h3><p>Use what you learn on your own home to build homes for others or invest in new construction rentals.</p><a class="text-link" href="/why-new-homes-are-a-great-starting-point-for-real-estate-investors/">New homes for investors &rarr;</a></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Your dream is our passion</p>
      <h2 class="section-title">The secret of the owner-builder</h2>
      <p>Most people hire a general contractor because it looks like the simple, safe option. But a general contractor doesn't swing the hammer — they schedule, supervise and inspect the subcontractors who do. And nobody knows what you want better than you.</p>
      <p>Becoming an owner-builder means taking on that management role yourself. You don't need a construction degree. You need a plan, a budget, good subs and the right checklists — which is exactly what we teach.</p>
      <a class="btn" href="/free-training/">Learn the 6 keys in our free course</a>
    </div>
    <div>
    <img class="rounded-photo" src="/assets/img/photos/home-owner-builder.webp" alt="New wood-frame house under construction with sheathing and roof trusses in place" width="1024" height="576" loading="lazy">
    <ol class="steps">
      <li><strong>Plan &amp; design</strong> — pick a lot, a floor plan and a budget you can live with.</li>
      <li><strong>Finance &amp; permit</strong> — line up a construction loan and get your plans approved.</li>
      <li><strong>Bid &amp; schedule</strong> — hire subs, collect insurance certificates and set the sequence.</li>
      <li><strong>Build &amp; inspect</strong> — manage each phase and pass every inspection.</li>
      <li><strong>Move in</strong> — complete the punch list and protect your investment.</li>
    </ol>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Start here</p>
      <h2 class="section-title">Essential guides for new home builders</h2>
    </div>
    <div class="pillar-grid">
    <?php foreach ($pillars as [$slug, $label, $ic]): if (!get_post($slug)) continue; ?>
      <a class="pillar" href="/<?= e($slug) ?>/"><span class="feature-icon"><?= icon($ic) ?></span><span><?= e($label) ?></span><?= icon('arrow') ?></a>
    <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Recommended resources</p>
      <h2 class="section-title">Tools &amp; books we point every owner-builder to</h2>
      <p>We don't sell our own courses or gear. Instead we recommend the best resources already out there, so you can spend your money on the house.</p>
    </div>
    <?= product_grid(['books_heldmann', 'books_contracting_guide', 'laser_measure', 'moisture_meter', 'books_code_check', 'smart_thermostat']) ?>
    <p class="center"><a class="btn btn-ghost" href="/our-products/">See all recommendations</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head row">
      <div><p class="eyebrow">From the blog</p><h2 class="section-title">Latest building tips</h2></div>
      <a class="text-link" href="/blog/">All articles &rarr;</a>
    </div>
    <div class="card-grid">
      <?php foreach ($latest as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?php
    $h = ob_get_clean() . cta_band();
    render_page([
        'title' => 'Build Your Dream Home: Owner-Builder Training & Resources',
        'description' => 'Free owner-builder training, guides and tools to help you design and build your dream home in Texas, with or without a general contractor.',
        'path' => '/',
        'image' => '/assets/img/photos/home-hero.webp',
        'body' => $h,
        'schema' => [['@type' => 'WebPage', '@id' => url('/#webpage'), 'url' => url('/'), 'name' => SITE['name'], 'isPartOf' => ['@id' => url('/#website')], 'about' => ['@id' => url('/#organization')]]],
    ]);
}

/* ---------------- Free training (lead form) ---------------- */

const LESSONS = [
    ['Why should you build a new house?', 'building-a-new-home-why-its-a-decision-worth-considering'],
    ['How to build a house for less than anyone else', 'how-to-be-your-own-general-contractor'],
    ['The construction process', 'new-home-construction-timeline'],
    ['How to choose a timeless look', 'the-art-of-home-design-where-passion-meets-comfort'],
    ['The 6 keys to a great home', 'crafting-comfort-and-joy-the-6-keys-to-a-great-home'],
    ['How to get started', 'budgeting-for-your-texas-home-build-tips-for-staying-on-track'],
];

function form_token(): string {
    $t = time();
    return $t . '.' . hash_hmac('sha256', (string) $t, form_secret());
}

function form_secret(): string {
    $f = APP_ROOT . '/storage/secret.php';
    if (!is_file($f)) {
        @file_put_contents($f, "<?php exit; ?>\n" . bin2hex(random_bytes(32)));
    }
    $raw = @file_get_contents($f);
    return $raw ? trim(substr($raw, strpos($raw, "\n") + 1)) : 'fallback-' . __FILE__;
}

function handle_signup(): array {
    $errors = [];
    $name = trim((string) ($_POST['name'] ?? ''));
    $email = trim((string) ($_POST['email'] ?? ''));
    $phone = trim((string) ($_POST['phone'] ?? ''));
    $stage = trim((string) ($_POST['stage'] ?? ''));
    // Spam checks: honeypot, signed timestamp, minimum fill time.
    if (($_POST['website'] ?? '') !== '') return ['ok' => true];
    [$t, $sig] = array_pad(explode('.', (string) ($_POST['token'] ?? ''), 2), 2, '');
    if (!hash_equals(hash_hmac('sha256', $t, form_secret()), $sig) || time() - (int) $t < 3 || time() - (int) $t > 86400) {
        $errors[] = 'Your session expired. Please try again.';
    }
    if ($name === '' || mb_strlen($name) > 100) $errors[] = 'Please enter your name.';
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
    if (mb_strlen($phone) > 30) $errors[] = 'Please check your phone number.';
    if ($errors) return ['ok' => false, 'errors' => $errors, 'old' => compact('name', 'email', 'phone', 'stage')];

    $clean = fn($s) => str_replace(["\r", "\n", ','], ' ', $s);
    $row = implode(',', [date('c'), $clean($name), $clean($email), $clean($phone), $clean($stage), $clean($_SERVER['REMOTE_ADDR'] ?? '')]) . "\n";
    $file = APP_ROOT . '/storage/leads.php';
    if (!is_file($file)) @file_put_contents($file, "<?php exit; ?>\ndate,name,email,phone,stage,ip\n");
    @file_put_contents($file, $row, FILE_APPEND | LOCK_EX);

    $msg = "New free-training sign-up on newhomestudent2019.com\n\nName: $name\nEmail: $email\nPhone: $phone\nStage: $stage\nTime: " . date('r') . "\n";
    send_mail(SITE['lead_to'], 'New owner-builder training sign-up: ' . $clean($name), $msg, $email);
    return ['ok' => true];
}

function view_free_training(): never {
    $state = null;
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $state = handle_signup();
        if ($state['ok']) redirect('/free-training/?joined=1#lessons', 303);
    }
    $joined = isset($_GET['joined']);
    $old = $state['old'] ?? ['name' => '', 'email' => '', 'phone' => '', 'stage' => ''];
    ob_start(); ?>
<section class="page-hero hero-training"><div class="wrap training-grid">
  <div>
    <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Free Training</li></ol></nav>
    <p class="eyebrow">Free owner-builder training</p>
    <h1>Build your perfect home for a lower price than everyone else</h1>
    <p class="lead">Our free mini-course walks you through the six keys to designing and building your own home — even if you've never managed a construction project.</p>
    <ul class="hero-points">
      <?php foreach (LESSONS as $i => [$t]): ?><li><?= icon('check') ?> Lesson <?= $i + 1 ?>: <?= e($t) ?></li><?php endforeach; ?>
    </ul>
  </div>
  <div class="form-card" id="signup">
    <?php if ($joined): ?>
      <h2>You're in! 🎉</h2>
      <p>Thanks for signing up. Your six lessons are below — start with Lesson 1. Jonathon may also reach out personally to answer questions about your build.</p>
      <a class="btn" href="#lessons">Go to the lessons</a>
    <?php else: ?>
      <h2>Get instant access</h2>
      <p>Free. No spam. Unsubscribe anytime.</p>
      <?php if (!empty($state['errors'])): ?><div class="form-errors" role="alert"><?php foreach ($state['errors'] as $er) echo '<p>' . e($er) . '</p>'; ?></div><?php endif; ?>
      <form method="post" action="/free-training/#signup" novalidate>
        <input type="hidden" name="token" value="<?= e(form_token()) ?>">
        <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <label>Name <input type="text" name="name" required maxlength="100" autocomplete="name" value="<?= e($old['name']) ?>"></label>
        <label>Email <input type="email" name="email" required maxlength="150" autocomplete="email" value="<?= e($old['email']) ?>"></label>
        <label>Phone <span class="optional">(optional)</span> <input type="tel" name="phone" maxlength="30" autocomplete="tel" value="<?= e($old['phone']) ?>"></label>
        <label>Where are you in the process?
          <select name="stage">
            <?php foreach (['Just researching', 'Looking for land', 'Designing / choosing a plan', 'Getting financing', 'Ready to build', 'Already building', 'Want to start a home-building business'] as $opt): ?>
              <option<?= $old['stage'] === $opt ? ' selected' : '' ?>><?= e($opt) ?></option>
            <?php endforeach; ?>
          </select>
        </label>
        <button class="btn btn-lg btn-block" type="submit">Yes! Reserve my free training</button>
        <p class="fine">By signing up you agree to our <a href="/privacy-policy/">privacy policy</a>. Questions? Call <a href="tel:<?= e(SITE['phone_href']) ?>"><?= e(SITE['phone']) ?></a>.</p>
      </form>
    <?php endif; ?>
  </div>
</div></section>

<div class="wrap post-layout"><div class="prose">
  <figure class="post-figure"><img src="/assets/img/photos/free-training.webp" alt="House construction plans held up inside a newly framed home" width="1024" height="576" loading="lazy"></figure>
  <h2>The secret of the owner-builder</h2>
  <p>The majority of people hire a general contractor to build their home. It looks like the simple, "safe" option — but ask anyone who's been through it. Too many people end up with a house that doesn't have the look they wanted, came in over budget and finished late.</p>
  <p>Hiring a general contractor isn't the only option, and it doesn't take a degree or years of construction experience to do it differently. <strong>"Owner-builder"</strong> simply means acting as your own general contractor.</p>
  <h2>What does a general contractor actually do?</h2>
  <p>To decide whether you could be your own owner-builder, you first need to understand the job. A general contractor <strong>supervises, manages and inspects</strong>. They rarely do the work themselves — they subcontract each trade (foundation, framing, plumbing, electrical, HVAC, roofing, drywall, finishes) and make sure people show up and do the work to standard.</p>
  <p>And who knows your expectations better than you? Even the best general contractor will never fully understand your vision the way you do. That's the opportunity — get exactly the home you want while keeping the margin a builder would charge.</p>
  <div class="callout"><p><strong>Is it right for you?</strong> Owner-building takes time, organization and a willingness to make decisions quickly. It isn't for everyone — the course helps you figure out honestly whether it's a fit, and what to do if it isn't (including how to manage a builder well).</p></div>
  <h2 id="lessons">The six lessons</h2>
  <ol class="lesson-list">
  <?php foreach (LESSONS as $i => [$t, $slug]): $p = get_post($slug); if (!$p) continue; ?>
    <li><a href="<?= e($p['url']) ?>"><span class="lesson-num"><?= $i + 1 ?></span><span><strong><?= e($t) ?></strong><small><?= e($p['excerpt']) ?></small></span></a></li>
  <?php endforeach; ?>
  </ol>
  <h2>Recommended reading to go with the course</h2>
  <?= product_grid(['books_heldmann', 'books_contracting_guide', 'books_dummies']) ?>
</div><aside class="sidebar"><?= sidebar_widgets() ?></aside></div>
<?php
    $h = ob_get_clean();
    $crumbs = [['Home', '/'], ['Free Training', '/free-training/']];
    render_page([
        'title' => 'Free Owner-Builder Training: Build Your Own Home for Less',
        'description' => 'Free mini-course: the 6 keys to designing and building your own home as an owner-builder and saving the general contractor markup.',
        'path' => '/free-training/',
        'image' => '/assets/img/photos/free-training.webp',
        'body' => $h,
        'schema' => [breadcrumb_schema($crumbs), [
            '@type' => 'Course', 'name' => 'How Can Anyone Design & Develop Their Own Home?',
            'description' => 'A free six-lesson owner-builder mini-course covering why to build new, building for less, the construction process, timeless design, the 6 keys to a great home, and getting started.',
            'provider' => ['@id' => url('/#organization')], 'isAccessibleForFree' => true,
            'hasCourseInstance' => ['@type' => 'CourseInstance', 'courseMode' => 'online', 'courseWorkload' => 'PT2H'],
            'offers' => ['@type' => 'Offer', 'price' => 0, 'priceCurrency' => 'USD', 'category' => 'Free'],
        ]],
    ]);
}

/* ---------------- Recommended products hub (/our-products/) ---------------- */

function view_products_hub(): never {
    $byGroup = [];
    foreach (products() as $p) $byGroup[$p['group']][] = $p;
    $order = ['books', 'tools', 'office', 'safety', 'smart-home', 'energy', 'investing', 'home', 'outdoor', 'moving', 'pets'];
    $crumbs = [['Home', '/'], ['Recommended Tools & Books', '/our-products/']];
    $h = page_hero('Recommended tools, books & gear for new home builders',
        'We don\'t sell our own products. These are the books, tools and gadgets we recommend to owner-builders, new homeowners and renters saving for a home — all available on Amazon.', $crumbs);
    $h .= '<section class="section"><div class="wrap">';
    $h .= '<p class="disclosure">As an Amazon Associate we earn from qualifying purchases. Prices and availability change, so we link straight to Amazon for current details. <a href="/affiliate-disclosure/">How we choose products</a>.</p>';
    $h .= '<nav class="chips" aria-label="Jump to category">';
    foreach ($order as $g) if (!empty($byGroup[$g])) $h .= '<a class="chip" href="#' . e($g) . '">' . e(PRODUCT_GROUPS[$g][0]) . '</a>';
    $h .= '</nav>';
    $items = [];
    foreach ($order as $g) {
        if (empty($byGroup[$g])) continue;
        $h .= '<section class="product-section" id="' . e($g) . '"><h2>' . icon(PRODUCT_GROUPS[$g][1]) . ' ' . e(PRODUCT_GROUPS[$g][0]) . '</h2><div class="product-grid">';
        foreach ($byGroup[$g] as $p) { $h .= product_card($p); $items[] = $p; }
        $h .= '</div></section>';
    }
    $h .= '</div></section>' . cta_band();
    $list = ['@type' => 'ItemList', 'name' => 'Recommended resources for new home builders',
        'itemListElement' => array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $p['name'], 'url' => $p['url']], $items, array_keys($items))];
    render_page([
        'title' => 'Best Tools & Books for Owner-Builders and New Homeowners',
        'description' => 'Recommended books, inspection tools, smart-home gear and moving essentials for building a new home, hand-picked and available on Amazon.',
        'path' => '/our-products/',
        'body' => $h,
        'schema' => [breadcrumb_schema($crumbs), $list],
    ]);
}
