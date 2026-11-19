<?php defined('SNW') || (http_response_code(404) && exit);
header('Content-Type: application/rss+xml; charset=utf-8');
$items = array_slice(posts(), 0, 20);
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title><?= e(cfg('name')) ?> — Seattle Real Estate Blog</title>
  <link><?= e(abs_url('/blog/')) ?></link>
  <atom:link href="<?= e(abs_url('/feed/')) ?>" rel="self" type="application/rss+xml"/>
  <description>Buying, selling and living in Seattle.</description>
  <language>en-us</language>
<?php foreach ($items as $p): ?>
  <item>
    <title><?= e($p['title']) ?></title>
    <link><?= e(abs_url('/blog/' . $p['slug'] . '/')) ?></link>
    <guid isPermaLink="true"><?= e(abs_url('/blog/' . $p['slug'] . '/')) ?></guid>
    <pubDate><?= date(DATE_RSS, strtotime($p['date'] . ' 09:00:00')) ?></pubDate>
    <description><?= e($p['description']) ?></description>
  </item>
<?php endforeach ?>
</channel>
</rss>
