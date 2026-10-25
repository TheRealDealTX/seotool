<?php
// RSS 2.0 feed of the blog, built from site_posts().
require __DIR__ . '/../inc/config.php';

header('Content-Type: application/rss+xml; charset=utf-8');

$x = fn(string $s): string => htmlspecialchars($s, ENT_XML1 | ENT_QUOTES, 'UTF-8');
$posts = site_posts();
$latest = max(array_map(fn($p) => strtotime($p[3]), $posts));

echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title><?= $x(SITE_NAME) ?> Blog</title>
  <link><?= SITE_URL ?>/blogs/</link>
  <atom:link href="<?= SITE_URL ?>/feed/" rel="self" type="application/rss+xml"/>
  <description>Influencer marketing guides from <?= $x(SITE_NAME) ?>: brand deals, rates, outreach, affiliate income and Pinterest for creators.</description>
  <language>en-us</language>
  <lastBuildDate><?= date(DATE_RSS, $latest) ?></lastBuildDate>
<?php foreach ($posts as [$url, $title, $cat, $date, $excerpt]): ?>
  <item>
    <title><?= $x($title) ?></title>
    <link><?= SITE_URL . $x($url) ?></link>
    <guid isPermaLink="true"><?= SITE_URL . $x($url) ?></guid>
    <pubDate><?= date(DATE_RSS, strtotime($date . ' 12:00:00 UTC')) ?></pubDate>
    <category><?= $x($cat) ?></category>
    <description><?= $x($excerpt) ?></description>
  </item>
<?php endforeach; ?>
</channel>
</rss>
