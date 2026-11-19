<?php
header('Content-Type: application/rss+xml; charset=UTF-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
<title><?= SITE_NAME ?></title>
<atom:link href="<?= SITE_URL ?>/feed/" rel="self" type="application/rss+xml" />
<link><?= SITE_URL ?></link>
<description><?= e(SITE_TAGLINE) ?></description>
<language>en-US</language>
<lastBuildDate><?= date(DATE_RSS, strtotime(posts()[0]['modified'] ?: posts()[0]['published'])) ?></lastBuildDate>
<?php foreach (array_slice(posts(), 0, 20) as $p): ?>
<item>
<title><?= e($p['title']) ?></title>
<link><?= SITE_URL ?>/<?= e($p['slug']) ?>/</link>
<guid isPermaLink="true"><?= SITE_URL ?>/<?= e($p['slug']) ?>/</guid>
<pubDate><?= date(DATE_RSS, strtotime($p['published'])) ?></pubDate>
<?php foreach ($p['categories'] as $c): ?><category><?= e($c) ?></category><?php endforeach; ?>
<description><?= e($p['description']) ?></description>
</item>
<?php endforeach; ?>
</channel>
</rss>
