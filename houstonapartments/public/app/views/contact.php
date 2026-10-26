<?php defined('HA_ROOT') || exit; ?>
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true"><img src="/assets/img/Houston-Skyline.webp" alt="" width="1600" height="700"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><span aria-current="page">Contact</span></nav>
    <h1 class="fade-up">Contact Houston Apartments</h1>
    <p class="hero-sub fade-up d1">Get up to $<?= SITE['cashback'] ?> when you lease! Fill out the form and a locator will send personalized listings.</p>
  </div>
</section>
<section class="section">
  <div class="wrap split contact-split">
    <div class="split-copy reveal">
      <h2>Talk to a Houston apartment locator</h2>
      <p>Call or text <a href="tel:<?= SITE['phone_raw'] ?>"><?= SITE['phone'] ?></a>, or send the form. We usually reply within one business day with a short list that matches your budget, move-in date and must-haves.</p>
      <ul class="ticks">
        <li>100% free for renters</li>
        <li>Current specials and real availability</li>
        <li>Tours scheduled around your calendar</li>
        <li>Up to $<?= SITE['cashback'] ?> back when you lease</li>
      </ul>
      <p><a href="https://www.instagram.com/riseapartmentshtx/" target="_blank" rel="noopener">Follow us on Instagram @riseapartmentshtx</a></p>
    </div>
    <div class="form-card reveal d1">
      <form class="lead-form" novalidate>
        <input type="hidden" name="page" value="/contact-houston-apartments/">
        <label class="hp">Website <input name="website" tabindex="-1" autocomplete="off"></label>
        <div class="grid2">
          <label>Name<input name="name" required autocomplete="name"></label>
          <label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
        </div>
        <label>Email<input name="email" type="email" autocomplete="email"></label>
        <div class="grid3">
          <label>Move-in<select name="move_in"><option value="">Any time</option><option>ASAP</option><option>Within 30 days</option><option>1–2 months</option><option>2+ months</option></select></label>
          <label>Bedrooms<select name="beds"><option value="">Any</option><option>Studio</option><option>1</option><option>2</option><option>3+</option></select></label>
          <label>Budget<select name="budget"><option value="">Any</option><option>Under $1,200</option><option>$1,200–$1,600</option><option>$1,600–$2,200</option><option>$2,200+</option></select></label>
        </div>
        <label>Neighborhoods &amp; must-haves<textarea name="message" rows="4"></textarea></label>
        <button class="btn btn-grad btn-block btn-lg" type="submit">Send my request</button>
        <p class="form-msg" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
</section>
