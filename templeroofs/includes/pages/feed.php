<?php
defined('TR_ROOT') || exit;
header('Content-Type: application/rss+xml; charset=utf-8');
header('Cache-Control: public, max-age=1800');
$x = fn ($s) => htmlspecialchars((string) $s, ENT_XML1 | ENT_QUOTES, 'UTF-8');
$list = array_slice(posts(), 0, 20);
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Temple Roofers Blog</title>
  <link><?= $x(abs_url('/blog/')) ?></link>
  <atom:link href="<?= $x(abs_url('/blog/feed/')) ?>" rel="self" type="application/rss+xml"/>
  <description>Roofing guides for homeowners in Temple and Bell County, Texas.</description>
  <language>en-us</language>
<?php if ($list): ?>
  <lastBuildDate><?= $x(reset($list)['date']->format(DATE_RSS)) ?></lastBuildDate>
<?php endif; ?>
<?php foreach ($list as $p): ?>
  <item>
    <title><?= $x($p['title']) ?></title>
    <link><?= $x(abs_url($p['url'])) ?></link>
    <guid isPermaLink="true"><?= $x(abs_url($p['url'])) ?></guid>
    <pubDate><?= $x($p['date']->format(DATE_RSS)) ?></pubDate>
    <category><?= $x(category_name($p['category'])) ?></category>
    <description><?= $x($p['excerpt']) ?></description>
  </item>
<?php endforeach; ?>
</channel>
</rss>
<?php exit;
