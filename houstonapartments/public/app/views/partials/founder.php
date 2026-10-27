<?php
// Founder profile. $founderVariant: 'full' (About page) or 'compact' (homepage).
defined('HA_ROOT') || exit;
$full = ($founderVariant ?? 'full') === 'full';
?>
<section class="founder <?= $full ? 'founder-full' : 'founder-compact' ?>" id="joseph-dittman" itemscope itemtype="https://schema.org/Person">
  <figure class="founder-photo reveal">
    <img src="<?= e(FOUNDER['photo']) ?>" alt="Joseph Dittman, founder of Houston Apartments" width="560" height="700" loading="lazy" itemprop="image">
    <figcaption><span class="ico ico-pin" aria-hidden="true"></span> Houston, TX · Locating since <?= SITE['founded'] ?></figcaption>
  </figure>
  <div class="founder-copy reveal d1">
    <span class="pill">Meet your locator</span>
    <h2><span itemprop="name"><?= e(FOUNDER['name']) ?></span></h2>
    <p class="founder-title" itemprop="jobTitle"><?= e(FOUNDER['title']) ?></p>
    <?php if ($full): ?>
      <p>Joseph started Houston Apartments in <?= SITE['founded'] ?> with a simple goal: make apartment hunting in a city this big feel personal again. He has spent years helping renters across Houston and the rest of Texas – Dallas, Fort Worth and San Antonio included – and he still answers calls, books tours and walks properties himself.</p>
      <h3>Why renters work with Joseph</h3>
      <ul class="ticks">
        <li><strong>He sees the buildings first.</strong> A background in videography means Joseph films communities so you can judge the layout, light and amenities before you ever drive over.</li>
        <li><strong>He knows where the deals are.</strong> Move-in specials change weekly. Joseph tracks them, along with which properties are flexible on credit, pets or lease terms.</li>
        <li><strong>He builds better tools.</strong> The draw-on-map search on this site came from his push to make finding a home faster and simpler – no endless scrolling through listings that don’t fit.</li>
        <li><strong>He keeps you in the loop.</strong> Clear updates, honest opinions and no pressure – just a short list that actually matches your budget and move date.</li>
      </ul>
      <h3>Outside of work</h3>
      <p>When he isn’t touring apartments, Joseph is usually on a hiking trail or out on a lake or river. He makes a point of visiting a couple of new countries and around twenty states every year, and says those trips shape how he listens to people moving to Houston from somewhere new.</p>
      <h3>What drives him</h3>
      <p>Joseph’s ambition is to be the best apartment locator anywhere – measured by how well his clients are served, not by volume. His faith is central to how he does business: every recommendation is meant to be honest, caring and genuinely in your interest.</p>
    <?php else: ?>
      <p><?= e(FOUNDER['short']) ?> When you reach out, you’re talking to someone who has actually seen the places on your list.</p>
      <ul class="ticks">
        <li>Films and tours properties so you can see them first</li>
        <li>Tracks weekly move-in specials across Houston</li>
        <li>Built the draw-on-map search on this site</li>
      </ul>
    <?php endif ?>
    <div class="hero-actions">
      <button class="btn btn-grad" type="button" data-lead data-lead-name="Request for Joseph Dittman">Work with Joseph</button>
      <?php if ($full): ?><a class="btn btn-outline" href="tel:<?= SITE['phone_raw'] ?>">Call <?= SITE['phone'] ?></a><?php else: ?><a class="btn btn-outline" href="/about-houston-apartments/#joseph-dittman">More about Joseph</a><?php endif ?>
    </div>
  </div>
</section>
