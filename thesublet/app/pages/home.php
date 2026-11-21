<?php defined('APP') || exit;

cache_public();
$hostCards = listing_card_data(listing_search(['source' => 'host'], 8)['items']);
$dirCards = listing_card_data(listing_search(['source' => 'directory'], 8)['items']);
$all = known_cities();
$guides = city_content();
$featured = ['ny/new-york', 'ca/los-angeles', 'il/chicago', 'ma/boston', 'dc/washington', 'ca/san-francisco', 'wa/seattle', 'tx/austin',
    'tx/houston', 'pa/philadelphia', 'co/denver', 'ga/atlanta', 'fl/miami', 'tn/nashville', 'mn/rochester', 'mi/ann-arbor'];
$featured = array_values(array_filter($featured, fn($k) => isset($all[$k])));
$colleges = array_filter($all, fn($c) => ($c['type'] ?? '') === 'college');
$posts = array_slice(blog_posts(), 0, 3);
$liveCount = (int)val("SELECT COUNT(*) FROM listings WHERE status = 'active'");
$stateCount = count(array_unique(array_map(fn($k) => explode('/', $k)[0], array_keys($all))));
$heroBg = photo_url('site.hero');

$faqs = [
    ['q' => 'What is The Sublet?', 'a' => 'The Sublet (thesublet.com) is a nationwide directory of furnished rooms, apartments and homes available for roughly one to twelve months — summer sublets, travel-nurse housing, intern housing, student sublets and temporary housing for people relocating.'],
    ['q' => 'Is it free to list a sublet on The Sublet?', 'a' => 'Yes. Free listings are reviewed by a person before they go live, and renters contact you through a relay form so your email stays private. A one-time ' . price_label() . ' verified listing is published instantly, shows your contact details, adds a Verified host badge and gives you a dashboard to edit, renew or mark the place rented.'],
    ['q' => 'I manage a furnished building or extended-stay property. Is it already listed?', 'a' => 'Possibly. The Sublet includes a directory of furnished apartment buildings, corporate-housing operators, extended-stay properties and student housing built from public business information. Search your city, open your property and use “Claim this listing” to add photos, rates and availability.'],
    ['q' => 'How do renters contact hosts?', 'a' => 'Every host listing has a Contact form. The Sublet relays the message from our mailbox to the host, so the host’s email address is never published on free listings. Verified listings can also show the host’s contact details.'],
    ['q' => 'Does “Verified host” mean the host was background-checked?', 'a' => 'No. It means the host paid for the listing by card and confirmed their email address. Always tour (in person or by live video), confirm the person has the right to sublet, and never wire money or pay with gift cards or crypto.'],
];
$who = [
    ['site.summer', '☀️', 'Summer sublets', 'Students leaving town and interns arriving — May to August.', '/sublets/?summer=1'],
    ['site.nurses', '🩺', 'Travel nurses', 'Furnished places near hospitals that match a 13-week contract.', '/blog/travel-nurse-housing-guide/'],
    ['site.interns', '💼', 'Interns', 'Short, furnished stays in the cities where internships happen.', '/blog/intern-housing-guide-by-city/'],
    ['site.students', '🎓', 'Students', 'Semester sublets, study-abroad swaps and college-town rooms.', '/blog/student-sublets-semester-abroad/'],
    ['site.relocation', '📦', 'Relocations', 'A month or three to learn a city before signing a long lease.', '/blog/relocating-for-work-temporary-housing/'],
];

ob_start(); ?>
<section class="hero-x"<?= $heroBg ? ' style="--hero:url(\'' . e($heroBg) . '\')"' : '' ?>>
  <div class="hero-x-bg" aria-hidden="true"></div>
  <div class="blob blob-1" aria-hidden="true"></div><div class="blob blob-2" aria-hidden="true"></div>
  <div class="wrap hero-x-inner">
    <div class="hero-x-copy">
      <p class="pill-eyebrow reveal"><span class="dot"></span> Furnished stays · 1–12 months · all 50 states</p>
      <h1 class="reveal">Find a place that fits your <span class="grad-text">next chapter</span></h1>
      <p class="lead reveal">The Sublet is where hosts and renters meet for flexible, furnished housing across the US — rooms, apartments, houses and corporate suites for internships, travel-nurse contracts, semesters and moves.</p>
      <form class="hero-search glass reveal" action="/sublets/" method="get" role="search">
        <label class="hs-where"><span>Where?</span><input type="search" name="q" list="city-list" placeholder="City, e.g. Boston" autocomplete="off" required></label>
        <label><span>Move in</span><input type="date" name="from"></label>
        <label><span>Max rent</span><select name="max"><option value="">Any</option><option value="1000">$1,000</option><option value="1500">$1,500</option><option value="2000">$2,000</option><option value="3000">$3,000</option></select></label>
        <button class="btn btn-lg btn-glow" type="submit">Search</button>
        <datalist id="city-list"><?php foreach ($all as $c): ?><option value="<?= e($c['name'] . ', ' . $c['state']) ?>"><?php endforeach; ?></datalist>
      </form>
      <p class="hero-trust reveal"><span>✔ Real hosts, human-reviewed</span><span>🔒 Private message relay</span><span>🏢 Claimable property directory</span></p>
    </div>
    <div class="hero-x-float" aria-hidden="true">
      <div class="float-card fc-1 glass"><span class="fc-ico">✔</span><div><strong>Verified host</strong><small>Email &amp; card confirmed</small></div></div>
      <div class="float-card fc-2 glass"><span class="fc-ico">📅</span><div><strong>Jun 1 → Aug 31</strong><small>Summer sublet</small></div></div>
      <div class="float-card fc-3 glass"><span class="fc-ico">🛋️</span><div><strong>Furnished · Wi-Fi</strong><small>Utilities included</small></div></div>
    </div>
  </div>
</section>

<section class="stats-strip">
  <div class="wrap stats-grid">
    <div class="stat-x reveal"><strong data-count="<?= $liveCount ?>"><?= number_format($liveCount) ?></strong><span>live listings &amp; properties</span></div>
    <div class="stat-x reveal"><strong data-count="<?= count($guides) ?>"><?= count($guides) ?></strong><span>local city guides</span></div>
    <div class="stat-x reveal"><strong data-count="<?= $stateCount ?>"><?= $stateCount ?></strong><span>states &amp; DC covered</span></div>
    <div class="stat-x reveal"><strong data-count="<?= count(blog_posts()) ?>"><?= count(blog_posts()) ?></strong><span>renter &amp; host guides</span></div>
  </div>
</section>

<div class="marquee" aria-label="Popular cities">
  <div class="marquee-track">
    <?php for ($r = 0; $r < 2; $r++): foreach ($all as $k => $c): if (empty($c['guide'])) continue; [$st, $slug] = explode('/', $k); ?>
      <a href="<?= e(city_url($st, $slug)) ?>"<?= $r ? ' aria-hidden="true" tabindex="-1"' : '' ?>><?= e($c['name']) ?> <span><?= e($c['state']) ?></span></a>
    <?php endforeach; endfor; ?>
  </div>
</div>

<section class="wrap section who">
  <div class="section-head reveal"><div><p class="eyebrow">Made for the in-between</p><h2>Who uses The Sublet</h2></div></div>
  <div class="who-grid">
    <?php foreach ($who as $i => [$pk, $ico, $t, $d, $u]): $img = photo_img($pk, 'who-img'); ?>
      <a class="who-x reveal" style="--d:<?= $i * 70 ?>ms" href="<?= e($u) ?>">
        <?= $img ?: '<span class="who-img who-img-ph"></span>' ?>
        <span class="who-x-body"><span class="who-ico"><?= $ico ?></span><strong><?= e($t) ?></strong><span><?= e($d) ?></span></span>
      </a>
    <?php endforeach; ?>
  </div>
</section>

<section class="wrap section">
  <div class="section-head reveal"><div><p class="eyebrow">Fresh from hosts</p><h2>Newest sublets on The Sublet</h2></div><a class="link-arrow" href="/sublets/">See all →</a></div>
  <?php if ($hostCards): ?>
    <div class="grid cards"><?php foreach ($hostCards as $c) echo listing_card_html($c); ?></div>
  <?php else: ?>
    <div class="first-cta reveal">
      <?= photo_img('site.cta', 'first-cta-img') ?: placeholder_svg('', true) ?>
      <div>
        <h3>Be one of the first hosts on the new The Sublet</h3>
        <p>We just relaunched thesublet.com, and every host listing is posted by a real person — we never pad the site with fake sublets. Have a furnished room or apartment free for a month or more? List it now and it’ll be among the first renters see.</p>
        <p><a class="btn btn-glow" href="/post-a-sublet/">List your place</a> <a class="btn btn-ghost" href="/hosts/">Why host here</a></p>
      </div>
    </div>
  <?php endif; ?>
</section>

<?php if ($dirCards): ?>
<section class="wrap section-sm">
  <div class="section-head reveal"><div><p class="eyebrow">Furnished &amp; corporate housing</p><h2>Properties for monthly stays</h2></div><a class="link-arrow" href="/sublets/?type=furnished_community">Browse properties →</a></div>
  <p class="muted reveal">Furnished apartment buildings, corporate-housing operators and extended-stay suites from our property directory. Managers can claim their listing to add photos, rates and availability.</p>
  <div class="grid cards"><?php foreach ($dirCards as $c) echo listing_card_html($c); ?></div>
</section>
<?php endif; ?>

<section class="band band-mesh">
  <div class="wrap section">
    <div class="section-head reveal"><div><p class="eyebrow">Local know-how</p><h2>Popular cities for sublets</h2></div><a class="link-arrow" href="/sublets/#states">All states →</a></div>
    <div class="city-tiles">
      <?php foreach ($featured as $i => $k): $c = $all[$k]; [$st, $slug] = explode('/', $k); $cp = photo('city.' . $k); ?>
        <a class="city-tile reveal" style="--d:<?= ($i % 4) * 60 ?>ms" href="<?= e(city_url($st, $slug)) ?>">
          <?php if ($cp): ?><img src="<?= e($cp['file']) ?>" alt="<?= e($cp['alt']) ?>" loading="lazy" width="<?= (int)$cp['w'] ?>" height="<?= (int)$cp['h'] ?>"><?php else: ?><span class="city-tile-ph" style="--h:<?= (crc32($k) % 360) ?>"></span><?php endif; ?>
          <span class="city-tile-txt"><strong><?= e($c['name']) ?></strong><span><?= e(state_name($c['state'])) ?><?= $c['n'] ? ' · ' . (int)$c['n'] . ' places' : '' ?></span></span>
        </a>
      <?php endforeach; ?>
    </div>
    <?php if ($colleges): ?>
    <h3 class="mt reveal">College towns</h3>
    <p class="chips reveal"><?php foreach ($colleges as $k => $c): [$st, $slug] = explode('/', $k); ?><a href="<?= e(city_url($st, $slug)) ?>"><?= e($c['name']) ?>, <?= e($c['state']) ?></a><?php endforeach; ?></p>
    <?php endif; ?>
  </div>
</section>

<section class="owner-band">
  <div class="wrap owner-grid">
    <div class="owner-copy">
      <p class="eyebrow eyebrow-light reveal">For hosts &amp; property managers</p>
      <h2 class="reveal">Fill the gap months — without the hassle</h2>
      <p class="reveal">The Sublet is built for medium-term stays: the interns, nurses, researchers and relocating professionals who need a furnished place for one to twelve months. List a single room or a whole building.</p>
      <ul class="owner-list">
        <li class="reveal"><span>⚡</span><div><strong>Live in minutes</strong>Verified listings publish instantly — or list free and we review it by hand.</div></li>
        <li class="reveal"><span>🔒</span><div><strong>Privacy built in</strong>Renter messages arrive through our relay; your email stays private on free listings.</div></li>
        <li class="reveal"><span>📊</span><div><strong>Your own dashboard</strong>Edit details, upload photos, renew, or mark it rented in a click.</div></li>
        <li class="reveal"><span>🏢</span><div><strong>Already in our directory?</strong>Furnished buildings and extended-stay properties can claim their listing.</div></li>
      </ul>
      <p class="reveal"><a class="btn btn-lg btn-glow" href="/post-a-sublet/">List your place</a> <a class="btn btn-lg btn-outline-light" href="/hosts/">See how it works</a></p>
    </div>
    <div class="owner-visual reveal">
      <?= photo_img('site.owners', 'owner-photo') ?>
      <div class="mock-dash glass-dark">
        <div class="md-head"><span class="md-dot"></span><span class="md-dot"></span><span class="md-dot"></span><span class="md-title">Host dashboard</span></div>
        <div class="md-row"><div><strong>Sunny room near the park</strong><small>Live · expires in 54 days</small></div><span class="md-badge">✔ Verified</span></div>
        <div class="md-row"><div><strong>Photos</strong><small>6 uploaded</small></div><span class="md-bar"><i style="--w:100%"></i></span></div>
        <div class="md-row"><div><strong>Renter messages</strong><small>Relayed to your inbox</small></div><span class="md-pill">New</span></div>
        <div class="md-actions"><span>Edit</span><span>Renew</span><span>Mark rented</span></div>
      </div>
    </div>
  </div>
</section>

<section class="wrap section how">
  <div class="section-head reveal"><div><p class="eyebrow">Simple by design</p><h2>How The Sublet works</h2></div></div>
  <div class="steps-x">
    <div class="step-x reveal"><span class="step-n">1</span><h3>Hosts post a place</h3><p>Describe the room or apartment, dates, rent, deposit and house rules, and add photos. Free listings are checked by a human before they appear on The Sublet.</p></div>
    <div class="step-x reveal" style="--d:90ms"><span class="step-n">2</span><h3>Renters search &amp; save</h3><p>Filter by price, dates, type, furnished and pets, flip to the map, save favorites and compare up to four places side by side.</p></div>
    <div class="step-x reveal" style="--d:180ms"><span class="step-n">3</span><h3>Talk safely</h3><p>Messages go through The Sublet’s relay, so hosts’ emails aren’t published. Tour first, sign a written sublease, and never wire money.</p></div>
  </div>
  <div class="tiers">
    <div class="tier reveal">
      <h3>Free listing</h3>
      <p class="tier-price">$0</p>
      <ul><li>Reviewed before publishing</li><li>Contact details hidden — renters use the relay form</li><li>Upgrade any time</li></ul>
      <a class="btn btn-ghost" href="/post-a-sublet/?tier=free">Post free</a>
    </div>
    <div class="tier tier-hi reveal" style="--d:90ms">
      <span class="tier-flag">Most popular</span>
      <h3>Verified listing</h3>
      <p class="tier-price"><?= e(price_label()) ?> <span class="small">one-time</span></p>
      <ul><li>Published instantly</li><li>Your contact details shown</li><li>“Verified host” badge &amp; top placement</li><li>Dashboard to edit, renew &amp; add photos</li></ul>
      <a class="btn btn-glow" href="/post-a-sublet/?tier=paid">Get verified</a>
    </div>
  </div>
</section>

<section class="band band-warm">
  <div class="wrap section split">
    <div class="reveal">
      <p class="eyebrow">Free tools</p>
      <h2>Sublet smarter</h2>
      <p>The Sublet’s calculators help you budget before you commit and price fairly before you post.</p>
      <div class="tool-chips">
        <a href="/tools/cost-calculator/">🧮 Cost calculator</a><a href="/tools/compare/">⚖️ Sublet vs. lease vs. hotel</a><a href="/tools/proration/">📅 Proration</a>
        <a href="/tools/packing-checklist/">🧳 Packing checklist</a><a href="/tools/room-planner/">📐 Room planner</a><a href="/tools/city-quiz/">🗺️ City quiz</a>
      </div>
    </div>
    <div class="safety-box reveal">
      <?= photo_img('site.safety', 'safety-img') ?>
      <h2 class="h3">Stay safe</h2>
      <ul class="ticks">
        <li>Never wire money, pay by gift card or crypto, or pay before you’ve toured.</li>
        <li>Confirm the host is allowed to sublet — ask to see the lease or landlord consent.</li>
        <li>Use “Report listing” on anything suspicious and the team at The Sublet will review it.</li>
      </ul>
      <a class="link-arrow" href="/safety/">Read our scam-awareness tips →</a>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="wrap section">
  <div class="section-head reveal"><div><p class="eyebrow">Guides</p><h2>From The Sublet blog</h2></div><a class="link-arrow" href="/blog/">All guides →</a></div>
  <div class="grid three"><?php foreach ($posts as $p) echo blog_card($p); ?></div>
</section>
<?php endif; ?>

<section class="wrap section narrow">
  <h2 class="reveal">Why thesublet.com?</h2>
  <p class="reveal">Most rental sites are built for 12-month leases or for nightly vacation stays. The Sublet focuses on the middle: stays of one to twelve months, usually furnished, usually with flexible dates. That’s the gap a summer intern, a travel nurse on a 13-week contract, a visiting researcher or a family between homes falls into.</p>
  <p class="reveal">Host listings on thesublet.com are posted by real people — free listings are reviewed by hand and paid listings carry a Verified host badge. Our property directory adds furnished buildings and extended-stay options from public business information, clearly labeled until their managers claim them.</p>
  <?= faq_html($faqs) ?>
</section>

<section class="cta-final">
  <div class="wrap cta-final-inner reveal">
    <h2>Have a furnished place free for a month or more?</h2>
    <p>Join The Sublet and reach renters planning their next move.</p>
    <p><a class="btn btn-lg btn-glow" href="/post-a-sublet/">List your place</a> <a class="btn btn-lg btn-outline-light" href="/sublets/">Find a sublet</a></p>
  </div>
</section>
<?php
$body = ob_get_clean();
page([
    'title' => 'The Sublet — Furnished Sublets & Short-Term Rentals Across the US',
    'description' => 'The Sublet is a nationwide marketplace for furnished sublets and 1–12 month rentals: summer sublets, travel nurse housing, intern housing and rooms for students.',
    'canonical' => '/',
    'body' => $body,
    'body_class' => 'home',
    'h_extra' => $heroBg ? '<link rel="preload" as="image" href="' . e($heroBg) . '">' : '',
    'schema' => array_values(array_filter([schema_website(), schema_faq($faqs), schema_itemlist(array_merge($hostCards, $dirCards), 'Newest sublets and properties')])),
]);
