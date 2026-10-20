<?php
// RSS 2.0 feed of the 20 newest indexable posts (replaces WordPress /feed/).
header('Content-Type: application/rss+xml; charset=utf-8');
$items = array_slice(live_posts(), 0, 20);
echo '<?xml version="1.0" encoding="UTF-8"?>', "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title><?= e(SITE_NAME) ?></title>
<link><?= SITE_ORIGIN ?>/</link>
<atom:link href="<?= SITE_ORIGIN ?>/feed/" rel="self" type="application/rss+xml"/>
<description>Farm kitchen recipes, homestead guides and free tools from Purely Wholesome Farm.</description>
<language>en-US</language>
<?php foreach ($items as $p): ?>
<item>
  <title><?= e($p['h1'] ?: $p['title']) ?></title>
  <link><?= e(canonical(post_url($p['slug']))) ?></link>
  <guid isPermaLink="true"><?= e(canonical(post_url($p['slug']))) ?></guid>
  <pubDate><?= date(DATE_RSS, strtotime($p['published'] . ' 12:00:00')) ?></pubDate>
  <description><?= e($p['desc']) ?></description>
</item>
<?php endforeach ?>
</channel>
</rss>
