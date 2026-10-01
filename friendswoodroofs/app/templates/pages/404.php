<section class="page-hero page-hero--center">
  <div class="container narrow page-hero-inner">
    <p class="eyebrow eyebrow--light">Error 404</p>
    <h1>We couldn't find that page</h1>
    <p class="lead">The page may have moved, or the address may have a typo. These links should help you find what you need.</p>
    <div class="hero-actions">
      <a class="btn btn-accent btn-lg" href="/">Go to the homepage</a>
      <a class="btn btn-light btn-lg" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call <?= e(phone_display()) ?></span></a>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="related-grid">
      <div>
        <h2 class="h3">Roofing services</h2>
        <ul class="link-list">
          <?php foreach (services() as $slug => $s): ?>
          <li><a href="/services/<?= e($slug) ?>/"><?= e($s['name']) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
      <div>
        <h2 class="h3">Helpful pages</h2>
        <ul class="link-list">
          <li><a href="/contact/">Request an estimate</a></li>
          <li><a href="/roofing-project-planner/">Roofing Project Planner</a></li>
          <li><a href="/faqs/">Roofing FAQs</a></li>
          <li><a href="/service-area/">Service area</a></li>
          <li><a href="/about/">About us</a></li>
        </ul>
      </div>
      <div>
        <h2 class="h3">Latest articles</h2>
        <ul class="link-list">
          <?php foreach (array_slice(articles(), 0, 3) as $a): ?>
          <li><a href="<?= e($a['url']) ?>"><?= e($a['title']) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
    </div>
  </div>
</section>
