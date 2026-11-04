<?php
defined('SCC') || (http_response_code(404) && exit);

$faq = [
    ['What is a solar CCTV camera?', 'A solar CCTV camera is a security camera powered by a small photovoltaic panel and a rechargeable battery instead of mains power. The panel charges the battery in daylight, the battery runs the camera at night, and footage goes to a microSD card, a hub or the cloud over Wi‑Fi or 4G. Most consumer models record motion events rather than 24/7.'],
    ['Do solar CCTV cameras work at night and in winter?', 'Yes. The camera runs on its battery after dark and switches to infrared or spotlight night vision. Winter is the real test: short days and low sun can cut solar input to a third of summer levels, so tilt the panel steeper, keep it out of shade and choose a battery that covers several sunless days. Our <a href="/tools/solar-camera-battery-calculator/">battery calculator</a> shows how many.'],
    ['How much sun does a solar security camera need?', 'Most solar security cameras with a 3–6 W panel stay charged with about 2–4 hours of direct sun a day at moderate activity. Busy driveways, 4G models, 4K video and color night vision need more. Check your mounting spot with the <a href="/tools/solar-camera-site-check/">Solar Site Check</a>.'],
    ['Do I need Wi‑Fi for a solar CCTV camera?', 'No. Wi‑Fi models are cheapest, but 4G LTE solar cameras with a SIM card work anywhere with cell coverage, and some cameras can record to a microSD card with no internet at all (you just lose live alerts). See <a href="/guides/do-solar-cameras-need-wifi/">do solar cameras need Wi‑Fi</a>.'],
    ['How long do solar camera batteries last?', 'Two different answers: on a full charge with zero sun, a typical camera runs for roughly one to four weeks depending on activity. As for lifespan, lithium batteries usually keep useful capacity for about 2–4 years before runtime drops noticeably. Heat shortens it; mild temperatures extend it.'],
    ['Are solar CCTV cameras worth it?', 'They are worth it when running a cable is expensive or impossible: outbuildings, gates, farms, rentals, vacation homes and construction sites. If you need continuous 24/7 recording at a house that already has power, wired PoE cameras are usually the better buy. Compare both with our <a href="/tools/solar-vs-wired-cost-calculator/">cost calculator</a>.'],
];

$picks = articles('pillar');
$recent = articles();
uasort($recent, fn($a, $b) => strcmp($b['updated'] . $b['published'], $a['updated'] . $a['published']));

page_head([
    'title' => 'Solar CCTV Camera: Solar Security Camera Guides & Tools',
    'description' => 'Solar CCTV Camera helps you choose, size and install solar security cameras: 2026 buying guide, panel angle and battery calculators, and setup guides.',
    'path' => '/',
    'body_class' => 'is-home',
    'schema' => [
        breadcrumb_schema([['Home', '/']]),
        ['@type' => 'WebPage', '@id' => SITE_ORIGIN . '/#webpage', 'url' => SITE_ORIGIN . '/', 'name' => 'Solar CCTV Camera', 'isPartOf' => ['@id' => SITE_ORIGIN . '/#website'], 'about' => ['@type' => 'Thing', 'name' => 'Solar-powered security cameras'], 'dateModified' => BUILD_DATE . 'T08:00:00+00:00'],
        ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f[1], '<a>')]], $faq)],
    ],
]);
?>
<section class="home-hero" aria-label="Introduction">
  <div class="stage">
    <div class="sky" aria-hidden="true"><i class="dawn"></i><i class="noon"></i><i class="dusk"></i><i class="night"></i><div class="stars"></div></div>
    <div class="sun-arc" aria-hidden="true"><span class="orb"></span><span class="moon-orb"></span></div>
    <div class="horizon" aria-hidden="true">
      <svg viewBox="0 0 1440 260" preserveAspectRatio="none"><path class="hill-1" d="M0 150 C 240 80 420 120 640 140 S 1060 70 1440 120 V260 H0Z"/><path class="hill-2" d="M0 200 C 300 150 520 210 820 190 S 1240 150 1440 185 V260 H0Z"/></svg>
    </div>
    <div class="wrap hero-content">
      <div class="hero-copy">
        <span class="eyebrow"><?= icon('sun', 16) ?> Updated November 2026</span>
        <h1>Solar CCTV Camera: <span class="grad">security that runs on sunlight</span></h1>
        <p class="lede">Solar CCTV Camera is the independent guide to solar-powered security cameras. Find the best solar security camera for your property, size the panel and battery for your climate, and install it right the first time, with free calculators that do the math for you.</p>
        <div class="hero-ctas">
          <a class="btn btn-sun btn-lg" href="/best-solar-security-cameras/"><?= icon('star', 20) ?> Best solar cameras 2026</a>
          <a class="btn btn-ghost btn-lg" href="/tools/"><?= icon('calc', 20) ?> Free tools</a>
        </div>
        <div class="hero-clock" aria-hidden="true">
          <span><?= icon('clock', 18) ?> <b data-clock>6:00 AM</b></span>
          <span><?= icon('zap', 18) ?> <span data-state>Charging from sun</span></span>
        </div>
      </div>
      <div class="rig" aria-hidden="true">
        <svg viewBox="0 0 420 420">
          <defs>
            <linearGradient id="body" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe5ee"/></linearGradient>
            <linearGradient id="beamG" x1="0" x2="1"><stop offset="0" stop-color="#ffdd88" stop-opacity=".55"/><stop offset="1" stop-color="#ffdd88" stop-opacity="0"/></linearGradient>
          </defs>
          <!-- pole -->
          <rect x="190" y="150" width="16" height="270" rx="4" fill="#5b6475"/>
          <!-- solar panel -->
          <g transform="translate(58 30) rotate(-18 140 65)">
            <rect x="0" y="0" width="280" height="130" rx="8" fill="#0f2350"/>
            <g>
<?php for ($r = 0; $r < 3; $r++) for ($c = 0; $c < 6; $c++): ?>
              <rect class="cell" x="<?= 8 + $c * 45 ?>" y="<?= 8 + $r * 39 ?>" width="41" height="35" rx="3"/>
<?php endfor; ?>
            </g>
            <path class="glint" d="M20 8 L70 8 L30 122 L-0 122Z" fill="#ffffff" opacity=".2"/>
          </g>
          <rect x="186" y="150" width="24" height="26" rx="5" fill="#475066"/>
          <!-- cable with energy flow -->
          <path d="M206 176 C 240 190 250 220 240 248" fill="none" stroke="#20283a" stroke-width="5"/>
          <path class="flow" d="M206 176 C 240 190 250 220 240 248" fill="none" stroke="#fbbf24" stroke-width="3"/>
          <!-- bracket -->
          <rect x="200" y="250" width="40" height="12" rx="4" fill="#5b6475"/>
          <!-- night beam -->
          <path class="beam" d="M236 268 L420 210 L420 340 Z" fill="url(#beamG)"/>
          <!-- camera -->
          <g>
            <rect x="160" y="246" width="110" height="56" rx="26" fill="url(#body)" stroke="#c6cfdc"/>
            <circle cx="236" cy="274" r="20" fill="#0b1324"/>
            <circle cx="236" cy="274" r="11" fill="#1e3a8a"/>
            <circle cx="232" cy="270" r="4" fill="#93c5fd"/>
            <circle class="ir" cx="208" cy="266" r="3"/><circle class="ir" cx="208" cy="282" r="3"/><circle class="ir" cx="198" cy="274" r="3"/>
            <rect x="172" y="232" width="6" height="22" rx="3" fill="#c6cfdc"/>
          </g>
        </svg>
        <div class="battery-hud"><div class="state"><span>Battery</span><b data-batt>58%</b></div><div class="bar"><i></i></div></div>
      </div>
    </div>
    <div class="scroll-hint" aria-hidden="true"><i></i>Scroll through a solar day</div>
  </div>
</section>

<div class="wrap">
  <div class="stats">
    <div class="stat reveal"><b data-count="7">0</b><span>free calculators for solar camera owners</span></div>
    <div class="stat reveal"><b><span data-count="28">0</span></b><span>in-depth guides, updated for 2026</span></div>
    <div class="stat reveal"><b><span data-count="2">0</span>–<span data-count="4">0</span><small> h</small></b><span>direct sun most cameras need daily</span></div>
    <div class="stat reveal"><b>$<span data-count="0">0</span></b><span>paid placements: we pick on merit</span></div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="overline">Best solar security cameras 2026</span>
      <h2>Our Solar CCTV Camera picks by situation</h2>
      <p>There is no single best solar CCTV camera, only the best one for your sun, your signal and your property. We weigh the spec sheet against the energy math: panel watts, battery watt-hours, radio type and how the camera behaves in winter.</p>
    </div>
    <div class="picks">
      <div class="pick top reveal"><span class="badge">Best overall</span><h3>Wi‑Fi solar kit</h3><p class="for">Homes with Wi‑Fi reaching the yard</p><ul><li>2K–4K camera + detachable 3–6 W panel</li><li>Local microSD storage, optional cloud</li><li>Person / vehicle detection cuts false alerts</li></ul><a class="btn btn-sun btn-sm" href="/best-solar-security-cameras/#best-overall">See the pick</a></div>
      <div class="pick reveal"><span class="badge">No Wi‑Fi</span><h3>4G LTE solar camera</h3><p class="for">Farms, gates, cabins, job sites</p><ul><li>Works anywhere with cell coverage</li><li>Needs a SIM data plan (1–10 GB/mo)</li><li>Pair with a 5–10 W panel</li></ul><a class="btn btn-line btn-sm" href="/reviews/solar-cctv-camera-with-sim-card/">4G buying guide</a></div>
      <div class="pick reveal"><span class="badge">No subscription</span><h3>Built-in panel camera</h3><p class="for">Renters and simple installs</p><ul><li>Panel on the camera: one-piece mount</li><li>On-board or hub storage, no monthly fee</li><li>Best in sunny, open spots</li></ul><a class="btn btn-line btn-sm" href="/guides/rental-property-outdoor-camera-no-subscription/">No-fee options</a></div>
    </div>
  </div>
</section>

<section class="section section-dark cycle">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="overline">How it works</span>
      <h2>24 hours in the life of a Solar CCTV Camera</h2>
      <p>A solar camera is an energy budget. The panel banks energy while the sun is up; the battery spends it on standby, motion clips, live view and night vision. Keep income above spending and it never needs a charge.</p>
    </div>
    <div class="cycle-chart reveal">
      <svg viewBox="0 0 720 260" role="img" aria-label="Chart: solar input peaks at midday while the battery charges from about 60 to 100 percent, then drains slowly overnight as motion events are recorded">
        <defs><linearGradient id="sunGrad" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fbbf24" stop-opacity=".85"/><stop offset="1" stop-color="#f97316" stop-opacity=".08"/></linearGradient></defs>
        <g class="grid"><line x1="40" x2="700" y1="30" y2="30"/><line x1="40" x2="700" y1="90" y2="90"/><line x1="40" x2="700" y1="150" y2="150"/><line x1="40" x2="700" y1="210" y2="210"/></g>
        <text class="lbl" x="34" y="34" text-anchor="end">100%</text><text class="lbl" x="34" y="124" text-anchor="end">50%</text><text class="lbl" x="34" y="214" text-anchor="end">0%</text>
        <path class="sunfill" d="M178 210 C 260 210 290 60 370 60 C 450 60 480 210 562 210 Z"/>
        <path class="batt" d="M40 102 L150 106 C 200 106 230 95 300 70 C 360 48 420 36 470 32 L560 32 C 600 34 640 40 700 46"/>
        <g class="events"><circle cx="95" cy="104" r="4"/><circle cx="250" cy="90" r="4"/><circle cx="330" cy="60" r="4"/><circle cx="520" cy="32" r="4"/><circle cx="610" cy="37" r="4"/><circle cx="665" cy="43" r="4"/></g>
        <text class="lbl" x="40" y="240">Midnight</text><text class="lbl" x="178" y="240">6 AM</text><text class="lbl" x="355" y="240">Noon</text><text class="lbl" x="540" y="240">6 PM</text><text class="lbl" x="660" y="240">Midnight</text>
      </svg>
      <div class="cycle-legend"><span><i style="background:#fbbf24"></i>Solar input</span><span><i style="background:#4ade80"></i>Battery level</span><span><i style="background:#fbbf24;width:8px;height:8px;border-radius:50%"></i>Motion events recorded</span></div>
    </div>
    <div class="cycle-steps">
      <div class="reveal"><b><?= icon('panel', 18) ?> Harvest</b><p>A 5 W panel in 3 peak sun hours delivers ~10 Wh after losses.</p></div>
      <div class="reveal"><b><?= icon('battery', 18) ?> Store</b><p>A 10,000 mAh battery holds ~33 Wh: weeks of standby.</p></div>
      <div class="reveal"><b><?= icon('eye', 18) ?> Sleep &amp; wake</b><p>PIR or radar wakes the camera in under a second when something moves.</p></div>
      <div class="reveal"><b><?= icon('moon', 18) ?> Night</b><p>Infrared LEDs or a spotlight run off the battery until sunrise.</p></div>
    </div>
    <p style="margin-top:26px" class="reveal"><a class="btn btn-sun" href="/how-solar-cameras-work/">How solar cameras work <?= icon('arrow', 18) ?></a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="overline">Free tools</span>
      <h2>Size your Solar CCTV Camera before you buy</h2>
      <p>Most solar camera problems are sizing problems: panel too small, aimed wrong, battery too small for winter, or a 4G plan that runs out. These calculators answer those questions for your exact location and use.</p>
    </div>
    <div class="tool-grid">
<?php foreach (tools_meta() as $t) echo tool_card($t); ?>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap split">
    <div class="split-media reveal">
      <?= img('solar-panel-angle', 'Solar CCTV camera panel tilted toward the sun on a clear day', ['sizes' => '(max-width: 860px) 100vw, 560px']) ?>
      <span class="float-badge"><?= icon('angle', 18) ?> Rule of thumb: tilt ≈ latitude + 10° for winter</span>
    </div>
    <div class="reveal">
      <span class="overline">Most-read guide</span>
      <h2>Aim the panel right and the camera looks after itself</h2>
      <p>The single biggest factor in whether a Solar CCTV Camera keeps charging is the panel: where it points, how steeply it tilts and whether anything shades it in December. A panel facing true south (true north below the equator) at roughly your latitude collects close to the maximum year-round.</p>
      <ul class="checks">
        <li>Face true south, not magnetic south: compass readings can be off by 10–20° in parts of the US.</li>
        <li>Steeper in winter: the sun is low, and a steep panel sheds snow.</li>
        <li>Shade costs far more than angle: one shaded corner can halve output.</li>
      </ul>
      <a class="btn btn-sun" href="/guides/solar-camera-panel-angle/">Best panel angle guide</a>
      <a class="btn btn-line" href="/tools/solar-panel-angle-calculator/">Calculate my angle</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="overline">Use cases</span>
      <h2>Where a solar security camera beats a wired one</h2>
      <p>Anywhere a power cable is expensive, impossible or temporary, a Solar CCTV Camera earns its keep.</p>
    </div>
    <div class="uses">
      <a class="use reveal" href="/use-cases/solar-cameras-for-farms/"><?= img('barn-solar-camera', 'Solar camera on a barn post at sunset', ['sizes' => '(max-width: 560px) 100vw, 380px']) ?><span><strong><?= icon('barn', 20) ?> Farms &amp; ranches</strong><em>Barns, fuel tanks, gates, calving pens</em></span></a>
      <a class="use reveal" href="/guides/solar-gate-camera/"><?= img('solar-gate-camera', 'Solar camera watching a driveway gate', ['sizes' => '(max-width: 560px) 100vw, 380px']) ?><span><strong><?= icon('gate', 20) ?> Gates &amp; driveways</strong><em>Alerts the moment a vehicle arrives</em></span></a>
      <a class="use reveal" href="/use-cases/solar-cameras-rural-property/"><?= img('off-grid-camera', 'Off-grid solar security camera on rural land', ['sizes' => '(max-width: 560px) 100vw, 380px']) ?><span><strong><?= icon('tree', 20) ?> Rural &amp; vacant land</strong><em>Off-grid, often no Wi‑Fi</em></span></a>
      <a class="use reveal" href="/use-cases/solar-cameras-for-rvs/"><?= img('rv-solar-camera', 'Solar camera mounted on an RV', ['sizes' => '(max-width: 560px) 100vw, 380px']) ?><span><strong><?= icon('rv', 20) ?> RVs &amp; campers</strong><em>On the road and in storage</em></span></a>
      <a class="use reveal" href="/use-cases/solar-cameras-for-construction-sites/"><?= img('construction-solar-camera', 'Solar CCTV on a construction site', ['sizes' => '(max-width: 560px) 100vw, 380px']) ?><span><strong><?= icon('building', 20) ?> Construction sites</strong><em>Temporary, movable, 4G</em></span></a>
      <a class="use reveal" href="/guides/remote-cabin-solar-camera/"><?= img('remote-cabin', 'Solar camera at a remote cabin', ['sizes' => '(max-width: 560px) 100vw, 380px']) ?><span><strong><?= icon('home', 20) ?> Cabins &amp; vacation homes</strong><em>Watch it while you are away</em></span></a>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap split rev">
    <div class="split-media reveal">
      <?= img('solar-vs-wired', 'Solar security camera compared with a wired camera', ['sizes' => '(max-width: 860px) 100vw, 560px']) ?>
    </div>
    <div class="reveal">
      <span class="overline">Solar vs wired</span>
      <h2>Is a Solar CCTV Camera right for you?</h2>
      <p>Solar wins on installation: no trenching, no electrician, mount it in an afternoon and move it whenever you like. Wired PoE wins on continuous recording and never thinking about batteries. Many properties end up with both: wired cameras on the house, solar ones on the gate, shed and fence line.</p>
      <ul class="checks">
        <li>Choose solar for outbuildings, gates, rentals, farms and anywhere power is 50+ ft away.</li>
        <li>Choose wired for 24/7 recording, busy commercial frontages and deep-shade walls.</li>
        <li>Price both honestly, including trenching and labor, with the cost calculator.</li>
      </ul>
      <a class="btn btn-sun" href="/compare/solar-vs-wired/">Read the comparison</a>
      <a class="btn btn-line" href="/guides/are-solar-cameras-worth-it/">Are they worth it?</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="overline">Latest guides</span>
      <h2>Fresh from the Solar CCTV Camera guide library</h2>
    </div>
    <div class="card-grid">
<?php foreach (array_slice($recent, 0, 6) as $a) echo article_card($a); ?>
    </div>
    <p style="margin-top:28px;text-align:center"><a class="btn btn-line" href="/solar-camera-guides/">Browse all guides <?= icon('arrow', 18) ?></a></p>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap split">
    <div class="reveal">
      <span class="overline">Why trust us</span>
      <h2>Why Solar CCTV Camera is different</h2>
      <p>Solar CCTV Camera covers one thing only: solar-powered security cameras. That focus lets us go deeper than general tech sites on the parts that decide whether a solar camera works for you: sun hours, panel sizing, cold-weather charging, cellular data and real-world battery life.</p>
      <ul class="checks">
        <li>Research-based: manufacturer specs, solar irradiance data, installer documentation and owner reports, cross-checked.</li>
        <li>No paid placements. Affiliate commissions never decide a pick, and we label every affiliate link.</li>
        <li>Math you can check: every calculator shows its assumptions.</li>
      </ul>
      <a class="btn btn-sun" href="/about-us/">About Solar CCTV Camera</a>
    </div>
    <div class="reveal">
      <div class="faq">
<?php foreach ($faq as [$q, $a]): ?>
        <details><summary><?= e($q) ?></summary><div><p><?= $a ?></p></div></details>
<?php endforeach; ?>
      </div>
    </div>
  </div>
</section>

<?php cta_band_home(); page_foot();

function cta_band_home(): void
{ ?>
<section class="cta-band" style="padding-top:80px">
  <div class="wrap cta-inner reveal">
    <div>
      <h2>Not sure solar will work at your spot?</h2>
      <p>Answer seven quick questions and the Solar CCTV Camera Site Check tells you whether a standard panel will keep up, and what to change if it won’t.</p>
    </div>
    <a class="btn btn-sun btn-lg" href="/tools/solar-camera-site-check/"><?= icon('compass', 20) ?> Run the site check</a>
  </div>
</section>
<?php }
