<?php defined('WCA') || exit; ?>
<section class="hero">
  <div class="hero-bg" style="background-image:url('/assets/img/photos/ext-1.webp')"></div>
  <div class="wrap hero-inner">
    <p class="eyebrow">West Carrollton Apartments · Ohio 45449</p>
    <h1>West Carrollton Apartments: find your next home in West Carrollton, OH</h1>
    <p class="lead">West Carrollton Apartments lets you compare <?= (int)$stats['count'] ?> apartment, townhome and senior communities in one place, with rents, floor plans, pet policies, amenities and a live map.</p>
    <form class="search-box" action="/apartments/" method="get" role="search">
      <label class="sr" for="hq">Search</label>
      <input id="hq" name="q" type="search" placeholder="Community name, street or amenity (e.g. pool)">
      <select name="beds" aria-label="Bedrooms">
        <option value="">Any beds</option><option value="0">Studio</option><option value="1">1 bed</option><option value="2">2 beds</option><option value="3">3+ beds</option>
      </select>
      <select name="max" aria-label="Max rent">
        <option value="">Any price</option><option value="900">Under $900</option><option value="1000">Under $1,000</option><option value="1200">Under $1,200</option><option value="1500">Under $1,500</option>
      </select>
      <button class="btn" type="submit">Search</button>
    </form>
    <div class="quick-links">
      <a href="/apartments/pet-friendly/">🐾 Pet-friendly</a>
      <a href="/apartments/under-1000/">💲 Under $1,000</a>
      <a href="/apartments/2-bedroom/">🛏️ 2 bedrooms</a>
      <a href="/apartments/townhomes/">🏘️ Townhomes</a>
      <a href="/apartments/senior/">🌿 Senior 55+</a>
    </div>
  </div>
</section>

<section class="stats-bar">
  <div class="wrap stats">
    <div><strong><?= (int)$stats['count'] ?></strong><span>communities listed</span></div>
    <div><strong><?= $stats['min'] ? money($stats['min']) : '—' ?></strong><span>lowest advertised rent</span></div>
    <div><strong><?= (int)$stats['pets'] ?></strong><span>pet-friendly options</span></div>
    <div><strong>6</strong><span>free renter tools</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Popular West Carrollton apartments</h2>
      <a href="/apartments/">View all <?= (int)$stats['count'] ?> →</a>
    </div>
    <div class="card-grid">
      <?php foreach ($featured as $l) partial('partials/card', ['l' => $l]); ?>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap split">
    <div>
      <h2>See every community on the map</h2>
      <p>West Carrollton sits along the Great Miami River just south of Dayton, with quick access to I-75, Cox Arboretum MetroPark and the Dayton Mall area. The West Carrollton Apartments interactive map shows every listing so you can judge the commute and the neighborhood at a glance.</p>
      <p><a class="btn" href="/apartments/#map">Open the apartment map</a></p>
    </div>
    <a class="map-teaser" href="/apartments/#map" aria-label="Open the apartment map">
      <?php foreach ($all as $l): if (!$l['lat']) continue;
        $x = 50 + ((float)$l['lng'] + 84.245) * 900; $y = 50 - ((float)$l['lat'] - 39.66) * 1100; ?>
        <span class="pin" style="left:<?= max(4, min(96, $x)) ?>%;top:<?= max(6, min(94, $y)) ?>%" title="<?= e($l['name']) ?>"></span>
      <?php endforeach; ?>
      <span class="map-label">Interactive map →</span>
    </a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Free renter tools from West Carrollton Apartments</h2><a href="/tools/">All tools →</a></div>
    <div class="tool-grid">
      <a class="tool-card" href="/tools/apartment-match-quiz/"><span>🎯</span><h3>Apartment Match Quiz</h3><p>Six questions, instant matches from real West Carrollton listings.</p></a>
      <a class="tool-card" href="/tools/rent-affordability-calculator/"><span>🧮</span><h3>Rent Affordability</h3><p>See what rent fits your paycheck using the 30% rule and 50/30/20.</p></a>
      <a class="tool-card" href="/tools/room-planner/"><span>🛋️</span><h3>Room Planner</h3><p>Drag a sofa, bed and desk onto a floor plan to see what fits.</p></a>
      <a class="tool-card" href="/tools/roommate-rent-splitter/"><span>🤝</span><h3>Rent Splitter</h3><p>Split rent fairly by bedroom size, private bath and parking.</p></a>
    </div>
    <div class="mini-calc card">
      <h3>Quick check: how much rent can I afford?</h3>
      <div class="mini-calc-row">
        <label>Monthly take-home pay <input type="range" id="mc-income" min="1500" max="9000" step="100" value="3600"></label>
        <output id="mc-out">$3,600 → about <strong>$1,080/mo</strong> in rent</output>
      </div>
      <p class="small muted" id="mc-match"></p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap owners">
    <div>
      <p class="eyebrow">For owners &amp; property managers</p>
      <h2>Is your community on West Carrollton Apartments? Claim it for $<?= listing_price_cents() / 100 ?>.</h2>
      <p>Every listing starts with contact details hidden. Claim yours with a one-time $<?= listing_price_cents() / 100 ?> payment to show your phone, email and website, upload real photos, and update rents, specials and amenities whenever you like.</p>
      <ul class="checks">
        <li>Your phone, email &amp; website shown to renters</li>
        <li>Owner dashboard to edit details and photos</li>
        <li><strong>★ Featured</strong> placement at the top of search results</li>
        <li>"Verified owner" badge</li>
      </ul>
      <p><a class="btn" href="/apartments/">Find &amp; claim your listing</a> <a class="btn btn-ghost" href="/list-your-property/">Add a new property</a></p>
    </div>
    <div class="owner-steps">
      <div><b>1</b><span>Find your community and click <em>Claim this listing</em></span></div>
      <div><b>2</b><span>Enter your name &amp; email, pay $<?= listing_price_cents() / 100 ?> securely with Stripe</span></div>
      <div><b>3</b><span>Verify your email and manage your listing</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Why renters search West Carrollton Apartments</h2><a href="/west-carrollton-living-guide/">Read the living guide →</a></div>
    <div class="feature-grid">
      <div><h3>🌳 Parks &amp; trails</h3><p>Wilson Park, Weidner Park and direct access to the paved Great Miami River Trail.</p></div>
      <div><h3>🚗 Easy commute</h3><p>Minutes to I-75 for downtown Dayton, Miamisburg, Kettering and Wright-Patterson.</p></div>
      <div><h3>🏫 Local schools</h3><p>Served by the West Carrollton City School District, which also covers parts of Moraine.</p></div>
      <div><h3>💵 Value</h3><p>Many communities advertise starting rents under $1,000, below newer suburbs nearby.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <h2>About West Carrollton Apartments</h2>
    <p>West Carrollton Apartments is a free, independent guide to renting in West Carrollton, Ohio and nearby Moraine, Miamisburg, Miami Township and Kettering. Instead of digging through national rental sites that lump every Dayton suburb together, you can see each local community's rents, floor plans, pet policies and amenities side by side.</p>
    <p>Whether you need a budget-friendly one-bedroom near I-75, a pet-friendly townhome close to Wilson Park, or a quiet 55+ community, West Carrollton Apartments helps you shortlist the right places, compare them and plan your move with our free tools.</p>
  </div>
</section>

<?php if ($posts): ?>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><h2>From the West Carrollton Apartments blog</h2><a href="/blog/">All articles →</a></div>
    <div class="card-grid">
      <?php foreach ($posts as $p): ?>
      <article class="card post-card">
        <a class="card-img" href="/blog/<?= e($p['slug']) ?>/"><img src="<?= e(photo_url($p['image'], true)) ?>" alt="" loading="lazy" width="640" height="427"></a>
        <div class="card-body"><p class="eyebrow"><?= e($p['category']) ?></p><h3><a href="/blog/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></h3><p class="muted"><?= e($p['excerpt']) ?></p></div>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>
<script>window.WCA_LISTINGS = <?= json_encode(array_map('listing_public_json', $all), JSON_HEX_TAG | JSON_UNESCAPED_SLASHES) ?>;</script>
