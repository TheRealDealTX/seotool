<?php
header('Content-Type: text/plain; charset=utf-8');
if (!is_production()) {
    // Staging / temporary domain: keep it out of search engines.
    echo "User-agent: *\nDisallow: /\n";
    return;
}
echo "User-agent: *\nAllow: /\nDisallow: /contact-submit/\nDisallow: /thank-you/\n\nSitemap: " . SITE['origin'] . "/sitemap.xml\n";
