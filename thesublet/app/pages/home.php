<?php defined('APP') || exit;

cache_public();
$latest = listing_card_data(listing_search([], 8)['items']);
$all = known_cities();
$featured = ['ny/new-york', 'ca/los-angeles', 'il/chicago', 'ma/boston', 'dc/washington', 'ca/san-francisco', 'wa/seattle', 'tx/austin',
    'tx/houston', 'pa/philadelphia', 'co/denver', 'ga/atlanta', 'fl/miami', 'tn/nashville', 'mn/rochester', 'mi/ann-arbor'];
$featured = array_values(array_filter($featured, fn($k) => isset($all[$k])));
$colleges = array_filter($all, fn($c) => ($c['type'] ?? '') === 'college');
$posts = array_slice(blog_posts(), 0, 3);

$faqs = [
    ['q' => 'What is The Sublet?', 'a' => 'The Sublet (thesublet.com) is a nationwide directory of furnished rooms, apartments and homes available for roughly one to twelve months — summer sublets, travel-nurse housing, intern housing, student sublets and temporary housing for people relocating.'],
    ['q' => 'Is it free to list a sublet on The Sublet?', 'a' => 'Yes. Free listings are reviewed by a person before they go live, and renters contact you through a relay form so your email stays private. A one-time ' . price_label() . ' verified listing is published instantly, shows your contact details, adds a Verified host badge and gives you a dashboard to edit, renew or mark the place rented.'],
    ['q' => 'How do renters contact hosts?', 'a' => 'Every listing has a Contact form. The Sublet relays the message from our mailbox to the host, so the host’s email address is never published on free listings. Verified listings can also show the host’s contact details.'],
    ['q' => 'Does “Verified host” mean the host was background-checked?', 'a' => 'No. It means the host paid for the listing by card and confirmed their email address. Always tour (in person or by live video), confirm the person has the right to sublet, and never wire money or pay with gift cards or crypto.'],
    ['q' => 'How long do listings stay up?', 'a' => 'Listings expire automatically after their “available to” date or after 60 days, whichever comes first. Hosts get an email reminder before expiry with a one-click renew link.'],
];

ob_start(); ?>
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow">Furnished sublets · 1–12 months · nationwide</p>
      <h1>Find a sublet that fits your next chapter</h1>
      <p class="lead">The Sublet is where hosts and renters meet for short-term rentals across the US — furnished rooms, apartments and houses for summer internships, travel-nurse contracts, semesters and moves.</p>
      <form class="hero-search" action="/sublets/" method="get" role="search">
        <label><span>Where?</span><input type="search" name="q" list="city-list" placeholder="City, e.g. Boston" autocomplete="off" required></label>
        <label><span>Move in</span><input type="date" name="from"></label>
        <label><span>Max rent</span><select name="max"><option value="">Any</option><option value="1000">$1,000</option><option value="1500">$1,500</option><option value="2000">$2,000</option><option value="3000">$3,000</option></select></label>
        <button class="btn btn-lg" type="submit">Search</button>
        <datalist id="city-list"><?php foreach ($all as $c): ?><option value="<?= e($c['name'] . ', ' . $c['state']) ?>"><?php endforeach; ?></datalist>
      </form>
      <p class="hero-sub small">Hosting? <a href="/post-a-sublet/">List your place free</a> or get verified for <?= e(price_label()) ?>.</p>
    </div>
    <div class="hero-art" aria-hidden="true">
      <img src="/assets/img/hero.svg" alt="" width="640" height="520" fetchpriority="high">
    </div>
  </div>
</section>

<section class="wrap section who">
  <h2>Who uses The Sublet</h2>
  <div class="grid five">
    <a class="who-card" href="/sublets/?summer=1"><span class="who-ico">☀️</span><h3>Summer sublets</h3><p>Students leaving town and interns arriving — May to August.</p></a>
    <a class="who-card" href="/blog/travel-nurse-housing-guide/"><span class="who-ico">🩺</span><h3>Travel nurses</h3><p>Furnished places near hospitals that match a 13-week contract.</p></a>
    <a class="who-card" href="/blog/intern-housing-guide-by-city/"><span class="who-ico">💼</span><h3>Interns</h3><p>Short, furnished stays in the cities where internships happen.</p></a>
    <a class="who-card" href="/blog/student-sublets-semester-abroad/"><span class="who-ico">🎓</span><h3>Students</h3><p>Semester sublets, study-abroad swaps and college-town rooms.</p></a>
    <a class="who-card" href="/blog/relocating-for-work-temporary-housing/"><span class="who-ico">📦</span><h3>Relocations</h3><p>A month or three to learn a city before signing a long lease.</p></a>
  </div>
</section>

<section class="wrap section">
  <div class="section-head"><h2>Newest sublets on The Sublet</h2><a href="/sublets/">See all →</a></div>
  <?php if ($latest): ?>
    <div class="grid cards"><?php foreach ($latest as $c) echo listing_card_html($c); ?></div>
  <?php else: ?>
    <div class="first-cta">
      <?= placeholder_svg('', true) ?>
      <div>
        <h3>Be one of the first hosts on the new The Sublet</h3>
        <p>We just relaunched thesublet.com as a nationwide directory, and every listing here is posted by a real host — we never pad the site with fake listings. If you have a furnished room or apartment free for a month or more, list it now and it will be among the first renters see.</p>
        <p><a class="btn" href="/post-a-sublet/">List your place</a> <a class="btn btn-ghost" href="/pricing/">Free vs. verified</a></p>
      </div>
    </div>
  <?php endif; ?>
</section>

<section class="band">
  <div class="wrap section">
    <h2>Popular cities for sublets</h2>
    <p class="muted">Local guides with neighborhoods, transit and tips for interns, travel nurses and students.</p>
    <div class="city-grid">
      <?php foreach ($featured as $k): $c = $all[$k]; [$st, $slug] = explode('/', $k); ?>
        <a class="city-chip" href="<?= e(city_url($st, $slug)) ?>"><strong><?= e($c['name']) ?></strong><span><?= e($c['state']) ?><?= $c['n'] ? ' · ' . (int)$c['n'] . ' listed' : '' ?></span></a>
      <?php endforeach; ?>
    </div>
    <?php if ($colleges): ?>
    <h3 class="mt">College towns</h3>
    <p class="chips"><?php foreach ($colleges as $k => $c): [$st, $slug] = explode('/', $k); ?><a href="<?= e(city_url($st, $slug)) ?>"><?= e($c['name']) ?>, <?= e($c['state']) ?></a><?php endforeach; ?></p>
    <?php endif; ?>
    <p><a href="/sublets/#states">Browse all states →</a></p>
  </div>
</section>

<section class="wrap section how">
  <h2>How The Sublet works</h2>
  <div class="grid three">
    <div class="step"><span class="step-n">1</span><h3>Hosts post a place</h3><p>Describe the room or apartment, the dates, rent, deposit and house rules, and add photos. Free listings are checked by a human before they appear on The Sublet.</p></div>
    <div class="step"><span class="step-n">2</span><h3>Renters search &amp; save</h3><p>Filter by price, dates, type, furnished and pets, flip to the map view, save favorites and compare up to four places side by side.</p></div>
    <div class="step"><span class="step-n">3</span><h3>Talk safely</h3><p>Messages go through The Sublet’s relay, so hosts’ emails aren’t published. Tour first, sign a written sublease, and never wire money.</p></div>
  </div>
  <div class="tiers">
    <div class="tier">
      <h3>Free listing</h3>
      <p class="tier-price">$0</p>
      <ul><li>Reviewed before publishing</li><li>Contact details hidden — renters use the relay form</li><li>Upgrade any time</li></ul>
      <a class="btn btn-ghost" href="/post-a-sublet/?tier=free">Post free</a>
    </div>
    <div class="tier tier-hi">
      <h3>Verified listing</h3>
      <p class="tier-price"><?= e(price_label()) ?> <span class="small">one-time</span></p>
      <ul><li>Published instantly</li><li>Your contact details shown</li><li>“Verified host” badge &amp; top placement</li><li>Dashboard to edit, renew &amp; add photos</li></ul>
      <a class="btn" href="/post-a-sublet/?tier=paid">Get verified</a>
    </div>
  </div>
</section>

<section class="band band-warm">
  <div class="wrap section split">
    <div>
      <h2>Sublet smarter with free tools</h2>
      <p>The Sublet’s calculators help you budget before you commit and price fairly before you post.</p>
      <ul class="link-list">
        <li><a href="/tools/cost-calculator/">Sublet cost calculator</a> — rent, deposit and fees, prorated</li>
        <li><a href="/tools/compare/">Sublet vs. short-term lease vs. extended-stay hotel</a></li>
        <li><a href="/tools/proration/">Move-in date proration calculator</a></li>
        <li><a href="/tools/packing-checklist/">Packing checklist</a> that saves on your device</li>
        <li><a href="/tools/room-planner/">Room planner</a> and <a href="/tools/city-quiz/">city match quiz</a></li>
      </ul>
    </div>
    <div class="safety-box">
      <h2>Stay safe</h2>
      <ul class="ticks">
        <li>Never wire money, pay by gift card or crypto, or pay before you’ve toured.</li>
        <li>Confirm the host is allowed to sublet — ask to see the lease or landlord consent.</li>
        <li>Get a written sublease and keep receipts.</li>
        <li>Use the “Report listing” button on anything suspicious and the team at The Sublet will review it.</li>
      </ul>
      <a href="/safety/">Read our scam-awareness tips →</a>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="wrap section">
  <div class="section-head"><h2>Guides from The Sublet</h2><a href="/blog/">All guides →</a></div>
  <div class="grid three"><?php foreach ($posts as $p) echo blog_card($p); ?></div>
</section>
<?php endif; ?>

<section class="wrap section narrow">
  <h2>Why thesublet.com?</h2>
  <p>Most rental sites are built for 12-month leases or for nightly vacation stays. The Sublet focuses on the middle: stays of one to twelve months, usually furnished, usually with flexible dates. That’s the gap a summer intern, a travel nurse on a 13-week contract, a visiting researcher or a family between homes falls into.</p>
  <p>Every listing on thesublet.com is posted by a real host — free listings are reviewed by a person, and paid listings carry a Verified host badge. We never seed the site with placeholder listings, so if your city looks quiet, that’s an honest picture, and a great moment to be the first host there.</p>
  <?= faq_html($faqs) ?>
</section>
<?php
$body = ob_get_clean();
page([
    'title' => 'The Sublet — Furnished Sublets & Short-Term Rentals Across the US',
    'description' => 'The Sublet is a nationwide marketplace for furnished sublets and 1–12 month rentals: summer sublets, travel nurse housing, intern housing and rooms for students.',
    'canonical' => '/',
    'body' => $body,
    'body_class' => 'home',
    'schema' => array_values(array_filter([schema_website(), schema_faq($faqs), schema_itemlist($latest, 'Newest sublets')])),
]);
