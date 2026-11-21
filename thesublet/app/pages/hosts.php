<?php defined('APP') || exit;

cache_public();
$crumbs = [['The Sublet', '/'], ['For hosts', '/hosts/']];
$dirCount = (int)val("SELECT COUNT(*) FROM listings WHERE source = 'directory' AND status = 'active'");
$bg = photo_url('site.owners');
$faqs = [
    ['q' => 'What does it cost to host on The Sublet?', 'a' => 'Listing is free. A free listing is reviewed by our team and renters reach you through our private message relay. A one-time ' . price_label() . ' verified listing goes live instantly, shows your contact details, adds a Verified host badge and top placement, and unlocks the dashboard.'],
    ['q' => 'Who rents on The Sublet?', 'a' => 'People who need furnished housing for one to twelve months: summer interns, travel nurses and other healthcare travelers, students and visiting researchers, and professionals relocating for work.'],
    ['q' => 'My building or extended-stay property is already listed. How do I take it over?', 'a' => 'Open the listing and choose “Claim this listing”. Verify instantly with a card payment, or submit a free claim — an email address at your property’s website domain speeds up review. Once approved you can add photos, rates, availability and a direct contact form.'],
    ['q' => 'Can I sublet my apartment legally?', 'a' => 'It depends on your lease and local law. Many leases require the landlord’s written consent, and some cities regulate stays under 30 days. Read our guide to subletting legally and check your city’s rules before you list.'],
    ['q' => 'How long does a listing stay live?', 'a' => 'Until your “available until” date or 60 days, whichever comes first. We email a one-click renew link before it expires.'],
];
ob_start(); ?>
<section class="page-hero"<?= $bg ? ' style="--hero:url(\'' . e($bg) . '\')"' : '' ?>>
  <div class="page-hero-bg" aria-hidden="true"></div>
  <div class="wrap page-hero-inner">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="pill-eyebrow reveal"><span class="dot"></span> For hosts, landlords &amp; property managers</p>
    <h1 class="reveal">Turn empty months into <span class="grad-text">booked months</span></h1>
    <p class="lead reveal">The Sublet connects furnished rooms, apartments and buildings with renters who need one to twelve months — not one night, not a full year.</p>
    <p class="reveal"><a class="btn btn-lg btn-glow" href="/post-a-sublet/">List your place</a> <a class="btn btn-lg btn-outline-light" href="#claim">Claim your property</a></p>
  </div>
</section>

<section class="wrap section">
  <div class="feature-grid">
    <div class="feature reveal"><span class="f-ico">🎯</span><h3>The right renters</h3><p>Interns, travel nurses, students and relocating professionals looking specifically for furnished, flexible stays.</p></div>
    <div class="feature reveal" style="--d:70ms"><span class="f-ico">⚡</span><h3>Live in minutes</h3><p>Verified listings publish the moment payment completes. Free listings are reviewed by a person, usually within a day or two.</p></div>
    <div class="feature reveal" style="--d:140ms"><span class="f-ico">🔒</span><h3>Private by default</h3><p>Renters message you through our relay, so your email isn’t published on free listings. Report tools and scam warnings protect both sides.</p></div>
    <div class="feature reveal"><span class="f-ico">📸</span><h3>Photos that sell</h3><p>Upload up to 12 photos; we convert them to fast WebP and strip location metadata automatically.</p></div>
    <div class="feature reveal" style="--d:70ms"><span class="f-ico">🗺️</span><h3>Local SEO pages</h3><p>Your listing appears on city pages with neighborhood guides, maps and filters for furnished, pet-friendly, summer and budget searches.</p></div>
    <div class="feature reveal" style="--d:140ms"><span class="f-ico">🔁</span><h3>Easy renewals</h3><p>Mark it rented, re-activate it next season, or renew with one click from the reminder email.</p></div>
  </div>
</section>

<section class="owner-band">
  <div class="wrap owner-grid">
    <div class="owner-copy">
      <p class="eyebrow eyebrow-light reveal">How it works</p>
      <h2 class="reveal">Three steps to your first inquiry</h2>
      <ol class="timeline">
        <li class="reveal"><strong>Describe your place</strong><span>Dates, monthly rent, deposit, furnishings, house rules and an approximate map pin — your exact address is never shown.</span></li>
        <li class="reveal"><strong>Choose free or verified</strong><span>Go live instantly for <?= e(price_label()) ?> with a Verified host badge, or list free after a quick review.</span></li>
        <li class="reveal"><strong>Answer renters</strong><span>Inquiries land in your inbox. Tour, agree on a written sublease, and mark the place rented from your dashboard.</span></li>
      </ol>
    </div>
    <div class="owner-visual reveal">
      <?= photo_img('site.relocation', 'owner-photo') ?: photo_img('site.cta', 'owner-photo') ?>
      <div class="mock-dash glass-dark">
        <div class="md-head"><span class="md-dot"></span><span class="md-dot"></span><span class="md-dot"></span><span class="md-title">New inquiry</span></div>
        <div class="md-msg"><strong>Travel nurse, 13-week contract</strong><p>“Hi! I start at the hospital on June 3 — is the room available through August? Happy to do a video tour.”</p><small>Relayed by The Sublet · example message</small></div>
      </div>
    </div>
  </div>
</section>

<section class="wrap section" id="claim">
  <div class="claim-band reveal">
    <div>
      <p class="eyebrow">Property managers &amp; corporate housing</p>
      <h2>Your building may already be on The Sublet</h2>
      <p>Our property directory lists <?= number_format($dirCount) ?> furnished apartment buildings, corporate-housing operators, extended-stay properties and student-housing communities across <?= count(city_content()) ?> cities, built from public business information. Claim yours to add photos, monthly rates, availability, and a direct contact form.</p>
      <ol class="claim-steps"><li>Search your city and open your property.</li><li>Click <strong>Claim this listing</strong>.</li><li>Verify instantly for <?= e(price_label()) ?>, or submit a free claim for review.</li></ol>
      <p><a class="btn btn-glow" href="/sublets/?type=furnished_community">Find my property</a> <a class="btn btn-ghost" href="/sublets/?type=extended_stay">Extended-stay properties</a></p>
    </div>
    <form class="claim-search glass" action="/sublets/" method="get">
      <label><span>Search your city</span><input type="search" name="q" placeholder="e.g. Houston" list="claim-cities" required></label>
      <datalist id="claim-cities"><?php foreach (city_content() as $c): ?><option value="<?= e($c['name'] . ', ' . $c['state']) ?>"><?php endforeach; ?></datalist>
      <button class="btn btn-block" type="submit">Find properties</button>
    </form>
  </div>
</section>

<section class="wrap section-sm">
  <div class="tiers">
    <div class="tier reveal"><h3>Free listing</h3><p class="tier-price">$0</p><ul><li>Human-reviewed before publishing</li><li>Private relay — your email stays hidden</li><li>Upgrade any time</li></ul><a class="btn btn-ghost" href="/post-a-sublet/?tier=free">Post free</a></div>
    <div class="tier tier-hi reveal" style="--d:90ms"><span class="tier-flag">Best for results</span><h3>Verified listing</h3><p class="tier-price"><?= e(price_label()) ?> <span class="small">one-time</span></p><ul><li>Published instantly</li><li>Contact details shown</li><li>Verified host badge &amp; top placement</li><li>Dashboard: edit, photos, renew</li></ul><a class="btn btn-glow" href="/post-a-sublet/?tier=paid">Get verified</a></div>
  </div>
</section>

<section class="wrap section narrow">
  <?= faq_html($faqs, 'Host FAQs') ?>
  <p class="small muted">Hosts are responsible for following their lease, HOA or building rules, fair housing laws and local short-term-rental, registration and tax requirements.</p>
</section>
<?php
page([
    'title' => 'Host on The Sublet — List or Claim Your Furnished Rental',
    'description' => 'List your furnished room, apartment or building on The Sublet for 1–12 month renters, or claim your property from our directory. Free or ' . price_label() . ' verified.',
    'canonical' => '/hosts/',
    'body' => ob_get_clean(),
    'body_class' => 'hosts',
    'schema' => array_values(array_filter([schema_breadcrumbs($crumbs), schema_faq($faqs)])),
]);
