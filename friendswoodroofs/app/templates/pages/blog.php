<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
$cats = article_categories();
// Server-side filter so category links work without JavaScript.
$active = isset($_GET['category']) && is_string($_GET['category']) && isset($cats[$_GET['category']]) ? $_GET['category'] : 'all';
partial('page-hero', [
    'eyebrow' => 'Roofing blog',
    'title'   => 'Roofing Guides for Friendswood Homeowners',
    'lead'    => 'Practical articles to help you understand your roof, compare options and prepare for a conversation with a roofer.',
    'actions' => false,
]);
?>
<section class="section">
  <div class="container">
    <div class="filter-bar" data-filter-bar>
      <p class="filter-label" id="filter-label">Filter by category:</p>
      <ul class="filter-list" role="list" aria-labelledby="filter-label">
        <li><a class="filter-btn" href="/blog/" data-filter="all"<?= $active === 'all' ? ' aria-current="true"' : '' ?>>All articles</a></li>
        <?php foreach ($cats as $slug => $name): ?>
        <li><a class="filter-btn" href="/blog/?category=<?= e($slug) ?>" data-filter="<?= e($slug) ?>"<?= $active === $slug ? ' aria-current="true"' : '' ?>><?= e($name) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <p class="filter-status sr-only" aria-live="polite" data-filter-status></p>
    <div class="card-grid article-grid article-grid--index" data-filter-grid>
      <?php foreach (articles() as $a): ?>
        <?php partial('article-card', ['a' => $a, 'headingLevel' => 'h2', 'hidden' => $active !== 'all' && $active !== $a['category_slug']]); ?>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php partial('cta-band', ['title' => 'Have a roofing question we haven\'t covered?', 'text' => 'Call or send a message with what you are seeing. We are happy to explain your options.']); ?>
