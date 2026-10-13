<?php
/** Page renderers for the hubs and one-off pages. */

function loss_type_options(): string
{
    $opts = ['Roof / hail', 'Wind / hurricane', 'Water / plumbing', 'Fire / smoke', 'Flood', 'Commercial property', 'Other'];
    $out = '<option value="">Type of damage</option>';
    foreach ($opts as $o) {
        $out .= '<option>' . h($o) . '</option>';
    }
    return $out;
}

function quick_form(string $source = 'home-hero'): string
{
    return '<form class="qform" action="/contact-submit/" method="post" data-ajax-form>
  <input type="hidden" name="token" value="' . h(form_token()) . '">
  <input type="hidden" name="source" value="' . h($source) . '">
  <div class="hp" aria-hidden="true"><label>Leave empty <input name="website" tabindex="-1" autocomplete="off"></label></div>
  <label class="field"><span>Your name</span><input name="name" required autocomplete="name" placeholder="Full name"></label>
  <label class="field"><span>Phone</span><input name="phone" type="tel" required autocomplete="tel" placeholder="(555) 555-5555"></label>
  <label class="field"><span>Damage</span><select name="loss_type" required>' . loss_type_options() . '</select></label>
  <label class="field"><span>City</span><input name="city" autocomplete="address-level2" placeholder="City, TX"></label>
  <button class="btn btn--primary btn--block btn--lg" type="submit">Get my free claim review ' . icon('arrow') . '</button>
  <p class="qform__note">No cost, no obligation. Joseph will call you back, usually the same business day.</p>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>';
}

function render_home(): void
{
    $posts = array_slice(posts_sorted(), 0, 3);
    $services = load_all('services');
    $order = ['roof-hail-damage-claims', 'water-damage-claims', 'fire-smoke-damage-claims', 'hurricane-windstorm-claims', 'denied-underpaid-claims'];
    $faqs = [
        ['q' => 'What does a public adjuster do?', 'a' => 'A public adjuster is a licensed professional who represents you, the policyholder, on a property insurance claim. We inspect and document the damage, read the policy, write a detailed estimate, and negotiate with your insurance company. The insurer\'s adjuster works for the insurer. <a href="/post/what-is-a-public-adjuster-a-complete-guide-for-property-owners/">Read the full guide</a>.'],
        ['q' => 'How much does a Texas public adjuster cost?', 'a' => 'We work on contingency: a percentage of what the insurer pays on the claim, agreed in writing up front. There\'s no upfront fee, and Texas law caps public adjuster fees at 10% of the settlement. <a href="/post/the-truth-about-public-adjuster-fees/">How fees work</a>.'],
        ['q' => 'Is it too late if I already filed my claim or got a payment?', 'a' => 'Usually not. Many people call us after a low estimate, a partial payment or a denial. What matters is your policy\'s deadlines and the claim\'s status. <a href="/post/when-is-it-too-late-to-hire-a-public-adjuster/">When it is (and isn\'t) too late</a>.'],
        ['q' => 'Do you only work in one city?', 'a' => 'No. We\'re based in Belton and handle residential and commercial claims statewide, from El Paso to Beaumont and Amarillo to the Rio Grande Valley.'],
        ['q' => 'Can my roofer handle the insurance claim instead?', 'a' => 'Not legally. Texas Insurance Code §4102.163 bars contractors from acting as public adjusters on property they may repair. We can work alongside the contractor you choose. <a href="/post/can-a-public-adjuster-work-for-a-contractor/">Why the law separates the two</a>.'],
        ['q' => 'Can I cancel if I change my mind?', 'a' => 'Yes. Every Texas public adjuster contract must let you rescind in writing within 72 hours of signing (§4102.103).'],
    ];
    $schema = schema_graph([schema_faq($faqs), ['@type' => 'WebPage', '@id' => CANONICAL_ORIGIN . '/#webpage', 'url' => CANONICAL_ORIGIN . '/', 'name' => 'Texas Public Adjuster', 'about' => ['@id' => CANONICAL_ORIGIN . '/#org'], 'isPartOf' => ['@id' => CANONICAL_ORIGIN . '/#website']]]);

    render_page([
        'title_full'  => 'Texas Public Adjuster | TX Public Adjusting · Free Claim Review',
        'title'       => 'Texas Public Adjuster',
        'description' => 'Licensed Texas public adjuster for roof, hail, water, fire and storm claims. We document your loss and negotiate with your insurer. Free review, no upfront fee.',
        'path'        => '/',
        'schema'      => $schema,
        'body_class'  => 'page-home',
    ], function () use ($posts, $services, $order, $faqs) {
        ?>
<section class="hero hero--home">
  <div class="hero__bg" aria-hidden="true">
    <span class="blob blob--1"></span><span class="blob blob--2"></span><span class="blob blob--3"></span>
    <span class="grid-lines"></span>
    <?= texas_map([], false, false, 'hero__map') ?>
  </div>
  <div class="wrap hero__in hero__in--split">
    <div class="hero__copy">
      <p class="eyebrow eyebrow--pill"><span class="dot"></span> We represent policyholders, never insurers</p>
      <h1>Texas public adjuster for <span class="grad-text">homeowners and businesses</span></h1>
      <p class="hero__lead">When your insurer's estimate doesn't cover the real damage, we document the full loss, build a line-by-line estimate and negotiate the claim for you. No upfront fees.</p>
      <div class="hero__btns">
        <a class="btn btn--primary btn--lg" href="/contact-us/">Get a free claim review <?= icon('arrow') ?></a>
        <a class="btn btn--light btn--lg" href="<?= tel_link() ?>"><?= icon('phone') ?> <?= h(BIZ['phone_display']) ?></a>
      </div>
      <ul class="trust">
        <li><?= icon('license') ?> TDI license #<?= h(BIZ['license']) ?></li>
        <li><?= icon('dollar') ?> Fees capped at 10% by law</li>
        <li><?= icon('pin') ?> Statewide service</li>
      </ul>
    </div>
    <div class="hero__card glass" data-reveal>
      <p class="hero__card-title"><?= icon('shield') ?> Free claim review</p>
      <p class="hero__card-sub">Tell us what happened. We'll tell you whether your estimate, denial or payment deserves a second look.</p>
      <?= quick_form('home-hero') ?>
    </div>
  </div>
</section>

<section class="ticker" aria-label="Claims we handle">
  <div class="ticker__track">
    <?php for ($i = 0; $i < 2; $i++): foreach (['Hail damage', 'Wind & hurricane', 'Burst pipes', 'Roof leaks', 'House fires', 'Smoke & soot', 'Tornado damage', 'Denied claims', 'Underpaid claims', 'Commercial roofs', 'Appraisal', 'Supplements'] as $t): ?>
      <span><?= icon('check') ?> <?= h($t) ?></span>
    <?php endforeach; endfor; ?>
  </div>
</section>

<section class="section wrap">
  <div class="section-head" data-reveal>
    <p class="eyebrow">Claims we handle</p>
    <h2 class="section-title">Residential and commercial property claims, start to finish</h2>
    <p class="section-sub">Whether the claim is new, stalled, underpaid or denied, we take over the documentation and the negotiation.</p>
  </div>
  <div class="grid grid--3 svc-grid">
    <?php foreach ($order as $slug): if (!isset($services[$slug])) continue; $s = $services[$slug]; ?>
    <a class="svc" href="/services/<?= h($slug) ?>/" data-reveal>
      <span class="svc__icon"><?= icon($s['icon'] ?? 'shield') ?></span>
      <span class="svc__title"><?= h($s['h1']) ?></span>
      <span class="svc__desc"><?= h($s['description']) ?></span>
      <span class="svc__more">Learn more <?= icon('arrow') ?></span>
    </a>
    <?php endforeach; ?>
    <a class="svc svc--dark" href="/commercial-claims/" data-reveal>
      <span class="svc__icon"><?= icon('building') ?></span>
      <span class="svc__title">Commercial property claims</span>
      <span class="svc__desc">Offices, warehouses, apartments, churches, hotels and retail: multi-building scopes, business income and coinsurance issues.</span>
      <span class="svc__more">Commercial claims <?= icon('arrow') ?></span>
    </a>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap split">
    <div data-reveal>
      <p class="eyebrow">Why it matters</p>
      <h2 class="section-title">The adjuster your insurer sends works for the insurer</h2>
      <p>That isn't a conspiracy; it's the job. The carrier's adjuster scopes the loss for the company that pays it. A public adjuster is the only adjuster legally hired by, and working for, you.</p>
      <p>Most underpaid claims aren't denied outright. They're short: a missing roof slope, no code items, drywall patched instead of replaced, or contents depreciated to nothing. We find those gaps and prove them.</p>
      <a class="link-arrow" href="/post/public-adjuster-vs-independent-adjuster/">Public vs. company vs. independent adjusters <?= icon('arrow') ?></a>
    </div>
    <div class="vs" data-reveal>
      <div class="vs__col">
        <p class="vs__title">Insurance company adjuster</p>
        <ul>
          <li>Hired and paid by the insurer</li>
          <li>Often handling dozens of claims after a storm</li>
          <li>Scope limited to what they see on one visit</li>
          <li>Settles under the carrier's guidelines</li>
        </ul>
      </div>
      <div class="vs__col vs__col--us">
        <p class="vs__title"><?= icon('shield') ?> Your public adjuster</p>
        <ul>
          <li>Hired by you, legally required to represent only you</li>
          <li>Room-by-room, slope-by-slope documentation</li>
          <li>Independent Xactimate estimate and policy review</li>
          <li>Negotiates, re-inspects, supplements and, if needed, goes to appraisal</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="section-head" data-reveal>
    <p class="eyebrow">How it works</p>
    <h2 class="section-title">A clear process from first call to final check</h2>
  </div>
  <ol class="timeline" data-timeline>
    <li data-reveal><span class="timeline__n">1</span><h3>Free claim review</h3><p>Send the estimate, denial letter or photos. We tell you honestly whether there's money left on the table.</p></li>
    <li data-reveal><span class="timeline__n">2</span><h3>Inspection &amp; documentation</h3><p>Roof-level photos, measurements, moisture readings and Matterport 3D scans where they help.</p></li>
    <li data-reveal><span class="timeline__n">3</span><h3>Policy review</h3><p>Declarations, endorsements, deductibles and exclusions, so we claim everything the policy actually covers.</p></li>
    <li data-reveal><span class="timeline__n">4</span><h3>Detailed estimate</h3><p>A line-item Xactimate estimate, including the items carriers routinely leave out.</p></li>
    <li data-reveal><span class="timeline__n">5</span><h3>Negotiation</h3><p>We handle the carrier: re-inspections, supplements and, when the numbers won't move, appraisal.</p></li>
    <li data-reveal><span class="timeline__n">6</span><h3>Settlement</h3><p>The insurer pays with you named on every check. Our fee is the agreed percentage, never more than 10%.</p></li>
  </ol>
  <div class="center" data-reveal><a class="btn btn--primary btn--lg" href="/contact-us/">Start with a free review <?= icon('arrow') ?></a></div>
</section>

<section class="section section--navy">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap meet">
    <div class="meet__photo" data-reveal>
      <img src="/assets/img/Joseph-Dittman-TX-Public-Adjusting.webp" width="360" height="360" alt="Joseph Dittman, licensed Texas public adjuster" loading="lazy">
      <span class="meet__badge"><?= icon('license') ?> License #<?= h(BIZ['license']) ?></span>
    </div>
    <div data-reveal>
      <p class="eyebrow">Meet your adjuster</p>
      <h2 class="section-title">Joseph Dittman, licensed Texas public adjuster</h2>
      <p>Joseph leads <?= h(BIZ['name']) ?>, the public adjusting practice of <?= h(BIZ['legal_name']) ?>. When you hire us, you work with him directly, not a call center.</p>
      <ul class="checklist checklist--light">
        <li>Licensed by the Texas Department of Insurance (#<?= h(BIZ['license']) ?>)</li>
        <li>Xactimate estimates, the same software insurers use</li>
        <li>Matterport 3D scans and roof-level photo documentation</li>
        <li>Based in Belton, inspecting properties across Texas</li>
      </ul>
      <div class="hero__btns">
        <a class="btn btn--primary" href="/about-us/">About Joseph <?= icon('arrow') ?></a>
        <a class="btn btn--light" href="<?= h(BIZ['license_url']) ?>" target="_blank" rel="noopener">Verify a TDI license <?= icon('external') ?></a>
      </div>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="section-head" data-reveal>
    <p class="eyebrow">Free claim tools</p>
    <h2 class="section-title">Check your claim yourself, before you call anyone</h2>
    <p class="section-sub">Built for Texas policyholders. No sign-up, and nothing you enter leaves your browser.</p>
  </div>
  <div class="grid grid--3">
    <?php foreach (array_keys(tools_registry()) as $slug) echo tool_card($slug, 'tool-card--tile'); ?>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap split split--map">
    <div data-reveal>
      <p class="eyebrow">Service areas</p>
      <h2 class="section-title">One licensed adjuster, all 254 Texas counties</h2>
      <p>We're based in Belton, in Bell County, and travel to inspect properties statewide. Claims play out differently by region: hurricanes and TWIA on the coast, hail in the Panhandle and North Texas, freezes and burst pipes everywhere. Our regional pages cover what matters in each.</p>
      <div class="chips">
        <?php foreach (load_all('areas') as $slug => $a): ?>
          <a class="chip" href="/areas/<?= h($slug) ?>/"><?= h($a['city'] ?? $slug) ?></a>
        <?php endforeach; ?>
      </div>
      <a class="link-arrow" href="/areas/">All service areas <?= icon('arrow') ?></a>
    </div>
    <div class="map-card" data-reveal><?= texas_map([], true, true) ?></div>
  </div>
</section>

<section class="section wrap">
  <div class="section-head" data-reveal>
    <p class="eyebrow">Know your rights</p>
    <h2 class="section-title">Texas law puts your insurer on a clock</h2>
    <p class="section-sub">The Texas prompt payment of claims rules (Insurance Code Chapter 542) set hard deadlines. Most policyholders never hear about them.</p>
  </div>
  <div class="keyfacts keyfacts--big">
    <div data-reveal><span data-count="15">15</span><p>days to acknowledge your claim and start investigating</p></div>
    <div data-reveal><span data-count="15">15</span><p>business days to accept or reject once they have everything they asked for</p></div>
    <div data-reveal><span data-count="5">5</span><p>business days to pay after accepting the claim</p></div>
    <div data-reveal><span data-count="10" data-suffix="%">10%</span><p>maximum public adjuster fee under Texas law</p></div>
  </div>
  <div class="center" data-reveal><a class="link-arrow" href="/tools/texas-claim-deadline-calculator/">Calculate your insurer's deadlines <?= icon('arrow') ?></a></div>
</section>

<?php if ($posts): ?>
<section class="section section--tint">
  <div class="wrap">
    <div class="section-head section-head--row" data-reveal>
      <div><p class="eyebrow">Claim guides</p><h2 class="section-title">Plain-English answers from a licensed adjuster</h2></div>
      <a class="btn btn--ghost" href="/blog/">All guides <?= icon('arrow') ?></a>
    </div>
    <div class="grid grid--3">
      <?php foreach ($posts as $p) echo card_for($p); ?>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="section wrap narrow">
  <?= faq_html($faqs, 'Questions Texas property owners ask') ?>
</section>
<?php
    });
}

function render_about(): void
{
    $p = load_content('pages', 'about-us');
    [$body, $toc] = add_heading_ids(normalize_body(process_shortcodes($p['body'])));
    $crumbs = [['Home', '/'], ['About', '/about-us/']];
    render_page([
        'title'       => $p['title'],
        'description' => $p['description'],
        'path'        => '/about-us/',
        'schema'      => schema_graph([schema_breadcrumbs($crumbs), ['@type' => 'ProfilePage', 'url' => canonical('/about-us/'), 'mainEntity' => ['@id' => CANONICAL_ORIGIN . '/about-us/#joseph-dittman']], schema_faq($p['faqs'] ?? [])]),
        'body_class'  => 'page-about',
    ], function () use ($p, $body, $crumbs) {
        ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in hero__in--split">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow"><?= h($p['eyebrow']) ?></p>
      <h1><?= h($p['h1']) ?></h1>
      <p class="hero__lead"><?= h($p['lead']) ?></p>
      <dl class="creds">
        <div><dt>Licensed adjuster</dt><dd><?= h(BIZ['adjuster']) ?></dd></div>
        <div><dt>TDI license</dt><dd>#<?= h(BIZ['license']) ?></dd></div>
        <div><dt>Company</dt><dd><?= h(BIZ['legal_name']) ?></dd></div>
        <div><dt>Based in</dt><dd><?= h(BIZ['city']) ?>, Texas</dd></div>
      </dl>
    </div>
    <div class="profile" data-reveal>
      <img src="/assets/img/Joseph-Dittman-TX-Public-Adjusting.webp" width="420" height="420" alt="Joseph Dittman, licensed Texas public adjuster" fetchpriority="high">
    </div>
  </div>
</section>
<div class="wrap article-layout">
  <article class="prose"><?= $body ?><?= faq_html($p['faqs'] ?? []) ?></article>
  <aside class="article-aside"><div class="sticky"><?= aside_contact() ?></div></aside>
</div>
<?php
    });
}

function render_contact(): void
{
    $crumbs = [['Home', '/'], ['Contact', '/contact-us/']];
    $sent = isset($_GET['sent']);
    render_page([
        'title'       => 'Contact a Texas Public Adjuster: Free Claim Review',
        'description' => 'Call, text or send your claim details to licensed Texas public adjuster Joseph Dittman. Free review of your estimate, denial or policy. No upfront fees.',
        'path'        => '/contact-us/',
        'schema'      => schema_graph([schema_breadcrumbs($crumbs), ['@type' => 'ContactPage', 'url' => canonical('/contact-us/'), 'about' => ['@id' => CANONICAL_ORIGIN . '/#org']]]),
        'body_class'  => 'page-contact',
    ], function () use ($crumbs, $sent) {
        ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow">Free claim review</p>
      <h1>Talk to a licensed public adjuster</h1>
      <p class="hero__lead">Call or text <?= h(BIZ['phone_display']) ?>, or send the details below. Joseph reviews every request personally and will tell you plainly whether your claim needs help.</p>
    </div>
  </div>
</section>
<div class="wrap contact">
  <div class="contact__form card-panel" data-reveal>
    <?php if ($sent): ?><div class="notice notice--ok"><?= icon('check') ?> Thanks, we received your request and will be in touch shortly.</div><?php endif; ?>
    <h2>Tell us about your claim</h2>
    <form action="/contact-submit/" method="post" data-ajax-form class="form">
      <input type="hidden" name="token" value="<?= h(form_token()) ?>">
      <input type="hidden" name="source" value="contact-page">
      <div class="hp" aria-hidden="true"><label>Leave empty <input name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="form__row">
        <label class="field"><span>Name *</span><input name="name" required autocomplete="name"></label>
        <label class="field"><span>Phone *</span><input name="phone" type="tel" required autocomplete="tel"></label>
      </div>
      <div class="form__row">
        <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email"></label>
        <label class="field"><span>Property city</span><input name="city" autocomplete="address-level2" placeholder="City, TX"></label>
      </div>
      <div class="form__row">
        <label class="field"><span>Type of damage *</span><select name="loss_type" required><?= loss_type_options() ?></select></label>
        <label class="field"><span>Where is the claim?</span>
          <select name="stage">
            <option value="">Choose one</option>
            <option>Haven't filed yet</option>
            <option>Filed, waiting on inspection</option>
            <option>Received an estimate or payment</option>
            <option>Claim denied</option>
            <option>In dispute or appraisal</option>
          </select>
        </label>
      </div>
      <div class="form__row">
        <label class="field"><span>Property type</span>
          <select name="property"><option>Home</option><option>Rental / investment</option><option>Commercial</option><option>Church / nonprofit</option><option>HOA / multifamily</option></select>
        </label>
        <label class="field"><span>Approximate date of loss</span><input name="loss_date" type="date"></label>
      </div>
      <label class="field"><span>What happened?</span><textarea name="message" rows="5" placeholder="Briefly describe the damage and what the insurer has said or paid so far."></textarea></label>
      <button class="btn btn--primary btn--lg" type="submit">Send my request <?= icon('arrow') ?></button>
      <p class="form__fine">By sending this form you agree we may contact you about your claim. We never sell your information. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      <div class="form-status" role="status" aria-live="polite"></div>
    </form>
  </div>
  <aside class="contact__side">
    <div class="card-panel contact__direct" data-reveal>
      <h2>Prefer to talk now?</h2>
      <a class="contact__big" href="<?= tel_link() ?>"><?= icon('phone') ?> <?= h(BIZ['phone_display']) ?></a>
      <div class="contact__btns">
        <a class="btn btn--primary btn--block" href="<?= tel_link() ?>">Call</a>
        <a class="btn btn--ghost btn--block" href="<?= sms_link() ?>"><?= icon('message') ?> Text photos</a>
      </div>
      <p class="muted"><?= icon('pin') ?> Based in <?= h(BIZ['city']) ?>, TX · serving all of Texas</p>
    </div>
    <div class="card-panel" data-reveal>
      <h3>Helpful to have ready</h3>
      <ul class="checklist">
        <li>Your policy declarations page</li>
        <li>Claim number and the insurer's adjuster name</li>
        <li>The insurer's estimate or denial letter</li>
        <li>Photos or video of the damage</li>
        <li>Any repair, mitigation or tarp invoices</li>
      </ul>
      <p class="muted">Don't have everything? Reach out anyway. We can help you get it.</p>
    </div>
    <div class="card-panel" data-reveal>
      <h3>What happens next</h3>
      <ol class="mini-steps">
        <li>We review what you send, at no cost.</li>
        <li>We call to talk through the claim and your options.</li>
        <li>If we can help, we explain the fee in writing. You can cancel within 72 hours of signing.</li>
      </ol>
    </div>
  </aside>
</div>
<?php
    });
}

function render_simple_page(string $slug, string $crumb): void
{
    $p = load_content('pages', $slug);
    if (!$p) {
        render_404();
        return;
    }
    render_article($p, "/$slug/", [['Home', '/'], [$crumb, "/$slug/"]]);
}

function render_hub(string $type, string $crumb): void
{
    $p = load_content($type, 'index');
    if (!$p) {
        render_404();
        return;
    }
    $path = $type === 'services' ? '/services/' : '/commercial-claims/';
    $items = load_all($type);
    $cards = '';
    foreach ($items as $it) {
        $cards .= card_for($it);
    }
    $grid = '<section class="section wrap"><h2 class="section-title">' . ($type === 'services' ? 'Claims we handle' : 'Property types we handle') . '</h2><div class="grid grid--3">' . $cards . '</div></section>';
    render_article($p, $path, [['Home', '/'], [$crumb, $path]], ['before' => $grid]);
}

function render_blog(): void
{
    $posts = posts_sorted();
    $crumbs = [['Home', '/'], ['Guides', '/blog/']];
    render_page([
        'title'       => 'Texas Insurance Claim Guides',
        'description' => 'Practical guides to Texas property insurance claims: hail and roof claims, denials, underpayments, fire and water losses, deadlines and public adjuster fees.',
        'path'        => '/blog/',
        'schema'      => schema_graph([schema_breadcrumbs($crumbs), ['@type' => 'Blog', 'url' => canonical('/blog/'), 'name' => 'TX Public Adjusting claim guides', 'publisher' => ['@id' => CANONICAL_ORIGIN . '/#org']]]),
        'body_class'  => 'page-blog',
    ], function () use ($posts, $crumbs) {
        $first = array_shift($posts);
        ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow">Claim guides</p>
      <h1>Texas insurance claim guides</h1>
      <p class="hero__lead">Written by licensed public adjuster Joseph Dittman. No fluff, just what to do, what the law says and what the insurer will look for.</p>
    </div>
  </div>
</section>
<section class="section wrap">
  <div class="filters" role="tablist" data-filters>
    <button class="chip is-on" data-filter="all" type="button">All guides</button>
    <?php foreach (CATEGORIES as $name => $slug): ?>
    <button class="chip" data-filter="<?= h($slug) ?>" type="button"><?= h($name) ?></button>
    <?php endforeach; ?>
  </div>
  <?php if ($first): ?>
  <a class="feature" href="/post/<?= h($first['_slug']) ?>/" data-reveal data-cat="<?= h(CATEGORIES[$first['category']] ?? '') ?>">
    <span class="feature__img"><img src="/assets/img/blog/<?= h($first['_slug']) ?>.webp" alt="" width="1200" height="800"></span>
    <span class="feature__body">
      <span class="card__kicker"><?= h($first['category'] ?? '') ?> · Latest</span>
      <span class="feature__title"><?= h($first['h1']) ?></span>
      <span class="card__desc"><?= h($first['description']) ?></span>
      <span class="card__more">Read the guide <?= icon('arrow') ?></span>
    </span>
  </a>
  <?php endif; ?>
  <div class="grid grid--3" data-filter-grid>
    <?php foreach ($posts as $p): ?>
      <div data-cat="<?= h(CATEGORIES[$p['category'] ?? ''] ?? '') ?>"><?= card_for($p) ?></div>
    <?php endforeach; ?>
  </div>
</section>
<?php
    });
}

function render_areas_hub(): void
{
    $p = load_content('pages', 'areas');
    $areas = load_all('areas');
    $crumbs = [['Home', '/'], ['Service areas', '/areas/']];
    [$body] = add_heading_ids(normalize_body(process_shortcodes($p['body'] ?? '')));
    $byRegion = [];
    foreach ($areas as $slug => $a) {
        $byRegion[$a['region'] ?? 'Texas'][] = $a;
    }
    ksort($byRegion);
    render_page([
        'title'       => $p['title'],
        'description' => $p['description'],
        'path'        => '/areas/',
        'schema'      => schema_graph([schema_breadcrumbs($crumbs), schema_faq($p['faqs'] ?? [])]),
        'body_class'  => 'page-areas',
    ], function () use ($p, $areas, $crumbs, $body, $byRegion) {
        ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in hero__in--split">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow"><?= h($p['eyebrow']) ?></p>
      <h1><?= h($p['h1']) ?></h1>
      <p class="hero__lead"><?= h($p['lead']) ?></p>
      <div class="hero__btns"><a class="btn btn--primary" href="/contact-us/">Free claim review <?= icon('arrow') ?></a></div>
    </div>
    <div class="map-card map-card--hero" data-reveal><?= texas_map([], true, true) ?></div>
  </div>
</section>
<section class="section wrap">
  <h2 class="section-title">Regional claim guides</h2>
  <div class="grid grid--3">
    <?php foreach ($byRegion as $region => $list): foreach ($list as $a): ?>
    <a class="area-card" href="/areas/<?= h($a['_slug']) ?>/" data-reveal>
      <span class="area-card__region"><?= h($region) ?></span>
      <span class="area-card__city"><?= icon('pin') ?> <?= h($a['city']) ?></span>
      <span class="area-card__risks"><?php foreach (array_slice($a['risks'] ?? [], 0, 3) as $r) echo '<span>' . h($r['title']) . '</span>'; ?></span>
      <span class="area-card__near">Also covers <?= h(implode(', ', array_slice($a['nearby'] ?? [], 0, 4))) ?></span>
    </a>
    <?php endforeach; endforeach; ?>
  </div>
</section>
<div class="wrap article-layout">
  <article class="prose"><?= $body ?><?= faq_html($p['faqs'] ?? []) ?></article>
  <aside class="article-aside"><div class="sticky"><?= aside_contact() ?></div></aside>
</div>
<?php
    });
}

function render_area(array $p, string $path, array $crumbs): void
{
    [$body, $toc] = add_heading_ids(normalize_body(process_shortcodes($p['body'] ?? '')));
    $slug = preg_replace('/^public-insurance-adjuster-/', '', $p['_slug']);
    render_page([
        'title'       => $p['title'],
        'description' => $p['description'],
        'path'        => $path,
        'schema'      => schema_graph([schema_breadcrumbs($crumbs), schema_service($p, $path), schema_faq($p['faqs'] ?? [])]),
        'body_class'  => 'page-area',
    ], function () use ($p, $path, $crumbs, $body, $toc, $slug) {
        ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in hero__in--split">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow"><?= h($p['eyebrow'] ?? $p['region'] ?? '') ?></p>
      <h1><?= h($p['h1']) ?></h1>
      <p class="hero__lead"><?= h($p['lead']) ?></p>
      <div class="hero__btns">
        <a class="btn btn--primary" href="/contact-us/">Free claim review <?= icon('arrow') ?></a>
        <a class="btn btn--light" href="<?= tel_link() ?>"><?= icon('phone') ?> <?= h(BIZ['phone_display']) ?></a>
      </div>
      <?php if (!empty($p['counties'])): ?><p class="hero__meta"><?= icon('pin') ?> <?= h(implode(' · ', $p['counties'])) ?> <?= count($p['counties']) > 1 ? 'counties' : 'County' ?></p><?php endif; ?>
    </div>
    <div class="map-card map-card--hero" data-reveal><?= texas_map([$slug]) ?></div>
  </div>
</section>
<?php if (!empty($p['risks'])): ?>
<section class="section wrap">
  <h2 class="section-title">What drives claims in <?= h($p['city']) ?></h2>
  <div class="grid grid--<?= count($p['risks']) >= 4 ? 4 : 3 ?> risks">
    <?php foreach ($p['risks'] as $i => $r): ?>
    <div class="risk" data-reveal><span class="risk__n">0<?= $i + 1 ?></span><h3><?= h($r['title']) ?></h3><p><?= h($r['text']) ?></p></div>
    <?php endforeach; ?>
  </div>
</section>
<?php endif; ?>
<div class="wrap article-layout">
  <article class="prose">
    <?= $body ?>
    <?php if (!empty($p['case_notes'])): ?>
    <h2 id="recent-claims">Recent claims in this area</h2>
    <div class="cases">
      <?php foreach ($p['case_notes'] as $c): ?>
      <div class="case"><p class="case__title"><?= h($c['title'] ?? '') ?></p><p><?= h($c['text'] ?? '') ?></p></div>
      <?php endforeach; ?>
    </div>
    <?php endif; ?>
    <?php if (!empty($p['nearby'])): ?>
    <h2 id="communities">Communities covered from this page</h2>
    <div class="chips chips--plain"><?php foreach ($p['nearby'] as $n) echo '<span class="chip">' . h($n) . '</span>'; ?></div>
    <p class="muted">Don't see your town? We serve every Texas county. <a href="/contact-us/">Ask us about your property</a>.</p>
    <?php endif; ?>
    <?= faq_html($p['faqs'] ?? []) ?>
  </article>
  <aside class="article-aside"><div class="sticky"><?= toc_html($toc) ?><?= aside_contact() ?></div></aside>
</div>
<section class="section wrap">
  <h2 class="section-title">Other regions we serve</h2>
  <div class="chips">
    <?php foreach (load_all('areas') as $s => $a): if ($s === $p['_slug']) continue; ?>
    <a class="chip" href="/areas/<?= h($s) ?>/"><?= h($a['city']) ?></a>
    <?php endforeach; ?>
  </div>
</section>
<?= related_html($p['related'] ?? [], 'Guides for ' . ($p['city'] ?? 'this area') . ' property owners') ?>
<?php
    });
}

function render_tools_hub(): void
{
    $crumbs = [['Home', '/'], ['Free tools', '/tools/']];
    render_page([
        'title'       => 'Free Texas Insurance Claim Tools & Calculators',
        'description' => 'Free tools for Texas policyholders: settlement calculator, Chapter 542 deadline calculator, documentation checklist, contents inventory and storm lookup.',
        'path'        => '/tools/',
        'schema'      => schema_graph([schema_breadcrumbs($crumbs)]),
        'body_class'  => 'page-tools',
    ], function () use ($crumbs) {
        ?>
<section class="hero hero--page">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <p class="eyebrow">Free claim tools</p>
      <h1>Free tools for Texas insurance claims</h1>
      <p class="hero__lead">Work out what your claim should pay, when your insurer has to respond, and what to document. Everything runs in your browser, with no sign-up, and nothing is sent to us unless you choose to.</p>
    </div>
  </div>
</section>
<section class="section wrap">
  <div class="grid grid--2">
    <?php foreach (array_keys(tools_registry()) as $slug) echo tool_card($slug, 'tool-card--big'); ?>
  </div>
  <p class="muted center">These tools give general estimates for planning. Your policy wording and the facts of your loss control the actual outcome.</p>
</section>
<?php
    });
}

function render_tool(array $p, string $path, array $crumbs): void
{
    [$body, $toc] = add_heading_ids(normalize_body(process_shortcodes($p['body'] ?? '')));
    $reg = tools_registry()[$p['_slug']] ?? [$p['h1'], '', 'calc'];
    render_page([
        'title'       => $p['title'],
        'description' => $p['description'],
        'path'        => $path,
        'schema'      => schema_graph([schema_breadcrumbs($crumbs), schema_faq($p['faqs'] ?? []), [
            '@type' => 'WebApplication', 'name' => $p['h1'], 'url' => canonical($path), 'applicationCategory' => 'FinanceApplication',
            'operatingSystem' => 'Any', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
            'provider' => ['@id' => CANONICAL_ORIGIN . '/#org'],
        ]]),
        'body_class'  => 'page-tool',
    ], function () use ($p, $crumbs, $body, $reg) {
        ?>
<section class="hero hero--page hero--tool">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="grid-lines"></span></div>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <?= breadcrumbs_html($crumbs) ?>
      <span class="hero__icon"><?= icon($reg[2]) ?></span>
      <p class="eyebrow">Free tool</p>
      <h1><?= h($p['h1']) ?></h1>
      <p class="hero__lead"><?= h($p['lead']) ?></p>
    </div>
  </div>
</section>
<section class="wrap tool-wrap">
  <div class="tool-app" id="tool"><?= $p['app'] ?></div>
  <p class="tool-disclaimer"><?= icon('shield') ?> For general planning only. This isn't legal advice, and it doesn't replace your policy's wording.</p>
</section>
<div class="wrap article-layout">
  <article class="prose"><?= $body ?><?= faq_html($p['faqs'] ?? []) ?></article>
  <aside class="article-aside"><div class="sticky"><?= aside_contact() ?></div></aside>
</div>
<?= related_html($p['related'] ?? [], 'Related guides') ?>
<?php if (!empty($p['script'])): ?><script src="<?= asset($p['script']) ?>" defer></script><?php endif; ?>
<?php
    });
}

function handle_contact(string $method): void
{
    $wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
    $respond = function (bool $ok, string $msg, int $code = 200) use ($wantsJson) {
        if ($wantsJson) {
            http_response_code($code);
            header('Content-Type: application/json');
            echo json_encode(['ok' => $ok, 'message' => $msg]);
        } else {
            redirect($ok ? '/contact-us/?sent=1' : '/contact-us/?error=1', 303);
        }
    };
    if ($method !== 'POST') {
        redirect('/contact-us/', 302);
    }
    $f = fn($k, $max = 200) => trim(mb_substr(str_replace(["\r", "\n"], ' ', (string) ($_POST[$k] ?? '')), 0, $max));
    if ($f('website') !== '' || !form_token_valid((string) ($_POST['token'] ?? ''))) {
        $respond(false, 'Your session expired. Please reload the page and try again.', 400);
        return;
    }
    $data = [
        'time'      => date('c'),
        'source'    => $f('source', 40),
        'name'      => $f('name', 120),
        'phone'     => $f('phone', 40),
        'email'     => $f('email', 160),
        'city'      => $f('city', 120),
        'loss_type' => $f('loss_type', 60),
        'stage'     => $f('stage', 80),
        'property'  => $f('property', 60),
        'loss_date' => $f('loss_date', 20),
        'message'   => trim(mb_substr((string) ($_POST['message'] ?? ''), 0, 4000)),
        'ip'        => $_SERVER['REMOTE_ADDR'] ?? '',
    ];
    if ($data['name'] === '' || !preg_match('/\d{3}.*\d{4}/', $data['phone'])) {
        $respond(false, 'Please include your name and a phone number we can reach you at.', 422);
        return;
    }
    if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        $data['email'] = '';
    }

    $csv = leads_file();
    $new = !is_file($csv);
    if ($fh = @fopen($csv, 'a')) {
        if ($new) {
            fputcsv($fh, array_keys($data));
        }
        fputcsv($fh, array_map(fn($v) => preg_match('/^[=+\-@]/', $v) ? "'" . $v : $v, $data));
        fclose($fh);
    }

    global $LEAD_EMAIL, $LEAD_FROM;
    if ($LEAD_EMAIL) {
        $lines = [];
        foreach ($data as $k => $v) {
            if ($v !== '') {
                $lines[] = str_pad(ucfirst(str_replace('_', ' ', $k)) . ':', 12) . ' ' . $v;
            }
        }
        $headers = "From: " . BIZ['name'] . " <$LEAD_FROM>\r\nContent-Type: text/plain; charset=UTF-8";
        if ($data['email']) {
            $headers .= "\r\nReply-To: " . $data['email'];
        }
        @mail($LEAD_EMAIL, 'New claim review request: ' . $data['name'] . ' (' . ($data['loss_type'] ?: 'claim') . ')', implode("\n", $lines), $headers);
    }
    $respond(true, 'Thanks, we received your request. Joseph will reach out shortly, usually the same business day.');
}
