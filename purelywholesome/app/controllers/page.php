<?php
/** @var array $parts */
$slug = $parts[0];
$crumbs = [['Home', '/']];
switch ($slug) {
    case 'about-us':
        $crumbs[] = ['About Us', '/about-us/'];
        render('about', ['crumbs' => $crumbs], ['title' => 'About Us | ' . SITE_NAME,
            'desc' => 'Meet Purely Wholesome Farm: a farm kitchen and homestead journal sharing tested recipes, livestock know-how and free tools to help you grow better and live simpler.',
            'path' => '/about-us/', 'schema' => [breadcrumb_schema($crumbs), ['@type' => 'AboutPage', 'url' => canonical('/about-us/'), 'about' => ['@id' => SITE_ORIGIN . '/#organization']]]]);
        break;
    case 'editorial-policy':
        $crumbs[] = ['Editorial Policy', '/editorial-policy/'];
        render('editorial', ['crumbs' => $crumbs], ['title' => 'Editorial Policy | ' . SITE_NAME,
            'desc' => 'How Purely Wholesome Farm writes, tests, fact-checks and updates its recipes and homestead guides, and how we handle sponsored content.',
            'path' => '/editorial-policy/', 'schema' => [breadcrumb_schema($crumbs)]]);
        break;
    case 'contact-us':
        $crumbs[] = ['Contact', '/contact-us/'];
        $sent = null;
        $errors = [];
        $old = ['name' => '', 'email' => '', 'topic' => 'question', 'message' => ''];
        if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
            require ROOT . '/app/mailer.php';
            $old = array_merge($old, array_map(fn($v) => trim((string)$v), array_intersect_key($_POST, $old)));
            $errors = handle_contact($old);
            $sent = !$errors;
            if ($sent) {
                $old = ['name' => '', 'email' => '', 'topic' => 'question', 'message' => ''];
            }
        }
        render('contact', compact('crumbs', 'sent', 'errors', 'old'), ['title' => 'Contact | ' . SITE_NAME,
            'desc' => 'Get in touch with Purely Wholesome Farm with questions about a recipe, livestock care or the farm tools. We read every message.',
            'path' => '/contact-us/', 'schema' => [breadcrumb_schema($crumbs), ['@type' => 'ContactPage', 'url' => canonical('/contact-us/')]]]);
        break;
    default: // privacy-policy, terms-of-use
        $doc = require ROOT . '/content/pages/' . $slug . '.php';
        $crumbs[] = [$doc['title'], '/' . $slug . '/'];
        render('legal', ['doc' => $doc, 'crumbs' => $crumbs], ['title' => $doc['title'] . ' | ' . SITE_NAME,
            'desc' => $doc['desc'] ?: $doc['title'] . ' for purelywholesome.com.', 'path' => '/' . $slug . '/', 'schema' => [breadcrumb_schema($crumbs)]]);
}
