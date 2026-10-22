<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// /feed/: RSS 2.0 of the 20 most recently updated guides (WordPress's old feed URL).
header('Content-Type: application/rss+xml; charset=utf-8');
$posts = all_posts();
uasort($posts, fn($a, $b) => [$b['updated'], $b['published']] <=> [$a['updated'], $a['published']]);
$posts = array_slice($posts, 0, 20);
$x = fn($s) => htmlspecialchars((string) $s, ENT_XML1 | ENT_QUOTES, 'UTF-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title><?= $x(SITE_NAME) ?></title>
  <link><?= SITE_URL ?>/</link>
  <atom:link href="<?= SITE_URL ?>/feed/" rel="self" type="application/rss+xml"/>
  <description><?= $x(SITE_TAGLINE) ?></description>
  <language>en-us</language>
  <lastBuildDate><?= date(DATE_RSS, strtotime(reset($posts)['updated'] . ' 08:00:00 UTC')) ?></lastBuildDate>
  <image><url><?= SITE_URL ?>/android-chrome-192x192.png</url><title><?= $x(SITE_NAME) ?></title><link><?= SITE_URL ?>/</link></image>
<?php foreach ($posts as $p): ?>
  <item>
    <title><?= $x($p['h1']) ?></title>
    <link><?= SITE_URL . $p['url'] ?></link>
    <guid isPermaLink="true"><?= SITE_URL . $p['url'] ?></guid>
    <pubDate><?= date(DATE_RSS, strtotime($p['updated'] . ' 08:00:00 UTC')) ?></pubDate>
    <category><?= $x(CATEGORIES[$p['category']][0]) ?></category>
    <description><?= $x($p['description']) ?></description>
  </item>
<?php endforeach; ?>
</channel>
</rss>
