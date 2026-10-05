<?php
header('Content-Type: text/plain; charset=UTF-8');
echo "# " . cfg('name') . ": " . cfg('tagline') . "\n\n";
echo "> A directory of on-base military family housing communities and military-friendly rentals, with guides for PCS moves, BAH and leases.\n\n";
echo "The XML sitemap is at " . abs_url('/sitemap_index.xml') . "\n\n## Pages\n";
foreach (['/' => 'Home', '/properties/' => 'All listings', '/marine-bases/' => 'Military bases', '/blog/' => 'Blog', '/submit-property/' => 'Submit a property', '/contact-us/' => 'Contact us'] as $u => $t) echo "- [$t](" . abs_url($u) . ")\n";
echo "\n## Posts\n";
foreach (posts() as $p) echo "- [{$p['title']}](" . abs_url('/' . $p['slug'] . '/') . ")\n";
echo "\n## Properties\n";
foreach (listings() as $l) echo "- [{$l['title']}](" . abs_url('/properties/' . $l['slug'] . '/') . ")\n";
echo "\n## Military Bases\n";
foreach (bases() as $b) echo "- [{$b['name']}](" . abs_url('/bases/' . $b['slug'] . '/') . ")\n";
