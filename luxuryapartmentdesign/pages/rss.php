<?php
header('Content-Type: application/rss+xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title><?= e(SITE_NAME) ?></title>
<link><?= url('/') ?></link>
<atom:link href="<?= url('/rss.xml') ?>" rel="self" type="application/rss+xml"/>
<description><?= e(SITE_TAGLINE) ?></description>
<language>en-us</language>
<?php foreach (array_slice(articles(), 0, 20) as $a): ?>
<item>
  <title><?= e($a['h1']) ?></title>
  <link><?= url('/' . $a['slug'] . '/') ?></link>
  <guid><?= url('/' . $a['slug'] . '/') ?></guid>
  <pubDate><?= date(DATE_RSS, strtotime($a['updated'] ?? $a['published'])) ?></pubDate>
  <description><?= e($a['excerpt'] ?? '') ?></description>
</item>
<?php endforeach; ?>
</channel>
</rss>
