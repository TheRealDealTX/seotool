<?php
// RSS feed of published blog posts.
header('Content-Type: application/rss+xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>', "\n";
?>
<rss version="2.0"><channel>
<title><?= SITE_NAME ?> Blog</title><link><?= SITE_URL ?>/blog/</link>
<description>Claim guides for Galveston homeowners and businesses by <?= AUTHOR ?>.</description>
<?php foreach (array_slice(blog_posts(), 0, 20) as $p): ?>
<item><title><?= e($p['title']) ?></title><link><?= SITE_URL ?>/blog/<?= e($p['slug']) ?>/</link><guid><?= SITE_URL ?>/blog/<?= e($p['slug']) ?>/</guid><pubDate><?= date(DATE_RSS, strtotime($p['date'])) ?></pubDate><author><?= LEAD_EMAIL ?> (<?= AUTHOR ?>)</author><description><?= e($p['description']) ?></description></item>
<?php endforeach ?>
</channel></rss>
