<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// /llms.txt: a plain-text map of the site for AI assistants (replaces Yoast's static file).
header('Content-Type: text/plain; charset=utf-8');
echo '# ' . SITE_NAME . "\n\n> " . SITE_TAGLINE . ". Independent, reader-supported reviews, comparisons and free tools for people who sit for work.\n\n";
echo "## Pages\n";
foreach ([['Home', '/'], ['All guides', '/blog/'], ['Free tools', '/tools/'], ['About us', '/about-us/'], ['Affiliate disclosure', '/affiliate-disclosure/']] as [$n, $u]) {
    echo "- [$n](" . SITE_URL . "$u)\n";
}
echo "\n## Tools\n";
foreach (TOOLS as $s => $t) {
    echo "- [{$t['h1']}](" . SITE_URL . "/tools/$s/): {$t['description']}\n";
}
foreach (CATEGORIES as $cs => [$cn]) {
    $in = array_filter(all_posts(), fn($p) => $p['category'] === $cs);
    if (!$in) {
        continue;
    }
    echo "\n## $cn\n";
    foreach ($in as $p) {
        echo "- [{$p['h1']}](" . SITE_URL . "{$p['url']}): {$p['description']}\n";
    }
}
