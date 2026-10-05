<?php
header('Content-Type: application/rss+xml; charset=UTF-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title><?= e(cfg('name')) ?></title>
<link><?= e(abs_url('/')) ?></link>
<atom:link href="<?= e(abs_url('/feed/')) ?>" rel="self" type="application/rss+xml"/>
<description><?= e(cfg('tagline')) ?></description>
<language>en-US</language>
<?php foreach (posts() as $p): ?>
<item>
<title><?= e($p['title']) ?></title>
<link><?= e(abs_url('/' . $p['slug'] . '/')) ?></link>
<guid isPermaLink="true"><?= e(abs_url('/' . $p['slug'] . '/')) ?></guid>
<pubDate><?= date(DATE_RSS, strtotime($p['date'])) ?></pubDate>
<description><?= e($p['excerpt']) ?></description>
</item>
<?php endforeach; ?>
</channel>
</rss>
