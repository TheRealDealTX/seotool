<?php defined('SNW') || (http_response_code(404) && exit);
/* Static pages. View file name = page slug. */
$pages = [
    'buy-a-home-in-seattle' => ['Buy a Home in Seattle | Local Buyer\'s Agents | Seattle Northwest Homes',
        'Ready to buy a home in Seattle? Tell us what you are looking for and get a curated list of homes, neighborhood advice and expert help from offer to closing.', 'Buy a Home'],
    'sell-your-home-seattle' => ['Sell Your Home in Seattle | Free Home Value Review',
        'Thinking of selling your Seattle home? Get a free pricing review, a prep and marketing plan, and expert negotiation from a local team that knows your neighborhood.', 'Sell Your Home'],
    'about-seattle-northwest-homes' => ['About Us | Seattle Real Estate Team | Seattle Northwest Homes',
        'Meet Seattle Northwest Homes — a local Seattle real estate team built on personalized service, honest advice and deep knowledge of Seattle neighborhoods.', 'About Us'],
    'contact-seattle-real-estate-agents' => ['Contact Our Seattle Real Estate Agents | Seattle Northwest Homes',
        'Contact Seattle Northwest Homes to buy, sell or ask about a listing. Send us a message and a local Seattle real estate agent will get back to you promptly.', 'Contact Us'],
    'privacy-policy' => ['Privacy Policy | Seattle Northwest Homes', 'How Seattle Northwest Homes collects, uses and protects the information you share through this website.', 'Privacy Policy'],
    'terms-of-use' => ['Terms of Use | Seattle Northwest Homes', 'Terms governing your use of the Seattle Northwest Homes website, listing information and content.', 'Terms of Use'],
    'thank-you' => ['Thank You | Seattle Northwest Homes', 'Thanks for reaching out to Seattle Northwest Homes.', 'Thank You'],
];
[$t, $d, $crumb] = $pages[$p];
$schema = [schema_breadcrumbs([[$crumb, '/' . $p . '/']])];
if ($p === 'contact-seattle-real-estate-agents') $schema[] = ['@type' => 'ContactPage', 'url' => abs_url('/' . $p . '/'), 'about' => ['@id' => abs_url('/#organization')]];
if ($p === 'about-seattle-northwest-homes') $schema[] = ['@type' => 'AboutPage', 'url' => abs_url('/' . $p . '/'), 'about' => ['@id' => abs_url('/#organization')]];
render('pages/' . $p, [], [
    'title' => $t, 'description' => $d, 'canonical' => '/' . $p . '/',
    'noindex' => $p === 'thank-you', 'schema' => $schema,
]);
