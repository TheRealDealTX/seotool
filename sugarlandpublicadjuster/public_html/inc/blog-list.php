<?php
/** Shared listing for /blog/ and /category/general/ (both URLs existed on the WordPress site). */
require_once __DIR__ . '/layout.php';

function render_post_list(string $path, string $h1, string $title, string $desc, array $crumbs): void
{
    $items = [];
    foreach (POSTS as $i => $p) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'url' => SITE['origin'] . '/' . $p['slug'] . '/', 'name' => $p['title']];
    }
    page_start([
        'title' => $title,
        'description' => $desc,
        'path' => $path,
        'page_type' => 'CollectionPage',
        'breadcrumbs' => $crumbs,
        'schema' => [
            ['@type' => 'Blog', '@id' => SITE['origin'] . '/blog/#blog', 'name' => 'Sugar Land Public Adjuster Blog', 'url' => SITE['origin'] . '/blog/', 'author' => ['@id' => SITE['origin'] . '/#joseph-dittman'], 'publisher' => ['@id' => SITE['origin'] . '/#business']],
            ['@type' => 'ItemList', '@id' => SITE['origin'] . $path . '#list', 'itemListElement' => $items],
        ],
    ]);
    page_hero($h1, 'Insurance claim guides for Sugar Land and Fort Bend County property owners, written by Joseph Dittman, licensed Texas public adjuster.', $crumbs, 'Sugar Land Public Adjuster blog');
    ?>
<section class="section">
  <div class="container">
    <div class="post-grid">
<?php foreach (POSTS as $p) post_card($p); ?>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <div class="team-card">
      <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman, public adjuster" width="240" height="240" loading="lazy">
      <div>
        <p class="eyebrow">About the author</p>
        <h2>Joseph Dittman</h2>
        <p><?= e(AUTHOR['short']) ?></p>
        <a class="btn btn-primary" href="<?= e(AUTHOR['url']) ?>">View author profile</a>
      </div>
    </div>
  </div>
</section>
<?php
    page_end();
}
