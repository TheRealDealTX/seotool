<?php
// RSS 2.0 feed of the 20 newest articles (replaces the WordPress /feed/).

header('Content-Type: application/rss+xml; charset=utf-8');
$posts = array_slice(all_posts(), 0, 20);
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title><?= e(SITE_NAME) ?></title>
  <link><?= SITE_URL ?>/</link>
  <atom:link href="<?= SITE_URL ?>/feed/" rel="self" type="application/rss+xml"/>
  <description><?= e(SITE_TAGLINE) ?></description>
  <language>en-us</language>
<?php foreach ($posts as $p): ?>
  <item>
    <title><?= e($p['h1']) ?></title>
    <link><?= SITE_URL . $p['url'] ?></link>
    <guid isPermaLink="true"><?= SITE_URL . $p['url'] ?></guid>
    <pubDate><?= date(DATE_RSS, strtotime($p['published'])) ?></pubDate>
    <category><?= e($p['category'] ?? 'Guides') ?></category>
    <description><?= e($p['description']) ?></description>
  </item>
<?php endforeach; ?>
</channel>
</rss>
