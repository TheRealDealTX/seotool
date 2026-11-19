<?php
defined('ERE') or exit;
header('Content-Type: application/rss+xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title><?= e(cfg('name')) ?></title>
<link><?= e(abs_url('/')) ?></link>
<atom:link href="<?= e(abs_url('/feed.xml')) ?>" rel="self" type="application/rss+xml"/>
<description><?= e(cfg('description')) ?></description>
<language>en-us</language>
<?php foreach (array_slice(all_posts(), 0, 20) as $p): ?>
<item>
  <title><?= e($p['title']) ?></title>
  <link><?= e(abs_url($p['url'])) ?></link>
  <guid isPermaLink="true"><?= e(abs_url($p['url'])) ?></guid>
  <pubDate><?= date(DATE_RSS, strtotime($p['date'])) ?></pubDate>
  <category><?= e(category($p['category'])['name']) ?></category>
  <description><?= e($p['excerpt']) ?></description>
</item>
<?php endforeach; ?>
</channel>
</rss>
