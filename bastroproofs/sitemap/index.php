<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$list = fn(array $items) => '<ul>' . implode('', array_map(fn($i) => '<li><a href="' . $i[1] . '">' . e($i[0]) . '</a></li>', $items)) . '</ul>';
$html = '<h2>Main Pages</h2>' . $list([['Bastrop Roofing — Home', '/'], ['About', '/about/'], ['Contact', '/contact/'], ['FAQ', '/faq/']])
      . '<h2>Roofing Services</h2>' . $list(array_merge([['All services', '/services/']], array_map(fn($s, $k) => [$s['name'] . ' in Bastrop, TX', "/services/$k/"], $SERVICES, array_keys($SERVICES))))
      . '<h2>Service Areas</h2>' . $list(array_merge([['All service areas', '/service-areas/']], array_map(fn($a, $k) => ['Roofing ' . $a['name'] . ', TX', "/service-areas/$k/"], $AREAS, array_keys($AREAS))))
      . '<h2>Roofing Tools</h2>' . $list(array_merge([['All roofing tools', '/roofing-tools/']], array_map(fn($t, $k) => [$t['name'], "/roofing-tools/$k/"], $TOOLS, array_keys($TOOLS))))
      . '<h2>Blog</h2>' . $list(array_merge([['All articles', '/blog/']], array_map(fn($p, $k) => [$p['h1'], "/blog/$k/"], $POSTS, array_keys($POSTS))))
      . '<h2>Legal</h2>' . $list([['Privacy Policy', '/privacy-policy/'], ['Terms of Use', '/terms-of-use/']]);
$legal = [
    'title'       => 'Sitemap | All Pages on bastroproofs.com | Bastrop Roofing',
    'description' => 'Every page on the Bastrop Roofing website: roofing services, Bastrop County service areas, free roofing tools, blog articles and company pages.',
    'path'        => '/sitemap/',
    'h1'          => 'Sitemap',
    'lead'        => 'Every page on bastroproofs.com in one place.',
    'html'        => $html,
];
require dirname(__DIR__) . '/includes/templates/legal.php';
