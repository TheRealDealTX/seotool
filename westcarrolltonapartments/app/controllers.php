<?php defined('WCA') || exit;

function site_schema(): array
{
    return [
        '@context' => 'https://schema.org',
        '@type' => 'WebSite',
        'name' => cfg('site_name'),
        'url' => url('/'),
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => url('/apartments/?q={search_term_string}'),
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

function page_home(): void
{
    $all = listings_published();
    $featured = array_slice($all, 0, 6);
    $posts = array_slice(posts_all(), 0, 3);
    $stats = [
        'count' => count($all),
        'min' => min(array_filter(array_column($all, 'rent_min')) ?: [0]),
        'pets' => count(array_filter($all, 'is_pet_friendly')),
    ];
    render('pages/home', compact('all', 'featured', 'posts', 'stats'), [
        'title' => 'West Carrollton, OH Apartments for Rent | Local Apartment Directory',
        'description' => 'Compare ' . count($all) . ' apartment and townhome communities in West Carrollton, Ohio. Rents, floor plans, pet policies, amenities, maps and free renter tools.',
        'canonical' => '/',
        'schema' => [site_schema(), [
            '@context' => 'https://schema.org', '@type' => 'Organization', 'name' => cfg('site_name'), 'url' => url('/'),
            'logo' => url('/assets/img/logo.svg'), 'email' => 'info@westcarrolltonapartments.com',
            'areaServed' => ['@type' => 'City', 'name' => 'West Carrollton', 'containedInPlace' => ['@type' => 'State', 'name' => 'Ohio']],
        ]],
        'body_class' => 'home',
    ]);
}

function directory_schema(array $items, string $name): array
{
    $list = [];
    foreach (array_values($items) as $i => $l) {
        $list[] = ['@type' => 'ListItem', 'position' => $i + 1, 'url' => url($l['url']), 'name' => $l['name']];
    }
    return ['@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => $name, 'numberOfItems' => count($list), 'itemListElement' => $list];
}

function page_directory(): void
{
    $all = listings_published();
    render('pages/directory', [
        'listings' => $all,
        'h1' => 'Apartments for Rent in West Carrollton, OH',
        'intro' => 'Every apartment, townhome and senior community we know of in West Carrollton and nearby Moraine, Miamisburg, Miami Township and Kettering, in one searchable list. Filter by price, bedrooms and pets, see them on the map, save favorites and compare up to three side by side.',
        'landing' => null,
    ], [
        'title' => 'Apartments for Rent in West Carrollton, OH (' . count($all) . ' Communities)',
        'description' => 'Search all ' . count($all) . ' apartment communities in West Carrollton, Ohio. Filter by rent, bedrooms and pet policy, view them on a map and compare side by side.',
        'canonical' => '/apartments/',
        'schema' => [directory_schema($all, 'Apartments in West Carrollton, OH'), breadcrumb_schema([['Home', '/'], ['Apartments', '/apartments/']])],
        'breadcrumbs' => [['Home', '/'], ['Apartments', null]],
        'leaflet' => true,
    ]);
}

function page_landing(string $key): void
{
    $lp = landing_pages()[$key];
    $items = array_values(array_filter(listings_published(), $lp['filter']));
    render('pages/directory', ['listings' => $items, 'h1' => $lp['h1'], 'intro' => $lp['intro'], 'landing' => $key], [
        'title' => $lp['title'],
        'description' => $lp['desc'],
        'canonical' => "/apartments/$key/",
        'schema' => [directory_schema($items, $lp['h1']), breadcrumb_schema([['Home', '/'], ['Apartments', '/apartments/'], [$lp['h1'], "/apartments/$key/"]])],
        'breadcrumbs' => [['Home', '/'], ['Apartments', '/apartments/'], [$lp['h1'], null]],
        'leaflet' => true,
    ]);
}

function page_listing(string $slug): void
{
    $l = listing_by_slug($slug);
    if (!$l || $l['status'] !== 'published') {
        // allow owners/admin to preview
        if (!$l || !(is_admin() || (current_user() && (int)$l['owner_id'] === (int)current_user()['id']))) not_found();
    }
    db()->prepare('UPDATE listings SET views = views + 1 WHERE id = ?')->execute([$l['id']]);

    $similar = array_values(array_filter(listings_published(), fn($o) => $o['id'] !== $l['id']));
    usort($similar, function ($a, $b) use ($l) {
        $d = fn($o) => ($o['lat'] && $l['lat']) ? (($o['lat'] - $l['lat']) ** 2 + ($o['lng'] - $l['lng']) ** 2) : 99;
        return $d($a) <=> $d($b);
    });
    $similar = array_slice($similar, 0, 3);
    $products = amazon_products_for_listing($l);

    $schema = [
        '@context' => 'https://schema.org',
        '@type' => $l['type'] === 'townhome' ? 'ApartmentComplex' : 'ApartmentComplex',
        'name' => $l['name'],
        'url' => url($l['url']),
        'description' => mb_substr($l['description'], 0, 300),
        'image' => array_map(fn($p) => url(photo_url($p)), array_slice($l['photos'], 0, 4)),
        'address' => ['@type' => 'PostalAddress', 'streetAddress' => $l['address'], 'addressLocality' => $l['city'], 'addressRegion' => $l['state'], 'postalCode' => $l['zip'], 'addressCountry' => 'US'],
        'petsAllowed' => is_pet_friendly($l),
    ];
    if ($l['lat']) $schema['geo'] = ['@type' => 'GeoCoordinates', 'latitude' => (float)$l['lat'], 'longitude' => (float)$l['lng']];
    if ($l['units']) $schema['numberOfAccommodationUnits'] = (int)$l['units'];
    if ($l['amenities']) $schema['amenityFeature'] = array_map(fn($a) => ['@type' => 'LocationFeatureSpecification', 'name' => $a, 'value' => true], array_slice($l['amenities'], 0, 20));
    if ($l['show_contact'] && $l['phone']) $schema['telephone'] = $l['phone'];

    $bedsTxt = beds_label($l);
    render('pages/listing', compact('l', 'similar', 'products'), [
        'title' => $l['name'] . ' – ' . $bedsTxt . ' in ' . $l['city'] . ', OH',
        'description' => mb_substr($l['name'] . ' at ' . $l['address'] . ', ' . $l['city'] . ', OH. ' . $bedsTxt . ', ' . rent_label($l) . '. ' . pets_label($l) . '. See photos, amenities, map and details.', 0, 158),
        'canonical' => $l['url'],
        'image' => photo_url($l['photos'][0]),
        'schema' => [$schema, breadcrumb_schema([['Home', '/'], ['Apartments', '/apartments/'], [$l['name'], $l['url']]])],
        'breadcrumbs' => [['Home', '/'], ['Apartments', '/apartments/'], [$l['name'], null]],
        'robots' => $l['status'] === 'published' ? null : 'noindex, nofollow',
        'leaflet' => true,
    ]);
}

function page_compare(): void
{
    $ids = array_slice(array_filter(array_map('intval', explode(',', $_GET['ids'] ?? ''))), 0, 3);
    $items = array_values(array_filter(listings_published(), fn($l) => in_array((int)$l['id'], $ids, true)));
    render('pages/compare', ['items' => $items, 'all' => listings_published()], [
        'title' => 'Compare West Carrollton Apartments Side by Side',
        'description' => 'Compare up to three West Carrollton, OH apartment communities side by side: rent, bedrooms, square footage, pets and amenities.',
        'canonical' => '/compare/',
        'robots' => $ids ? 'noindex, follow' : null,
        'breadcrumbs' => [['Home', '/'], ['Compare', null]],
    ]);
}

/* ---------- Claim + submit ---------- */

function page_claim(string $slug): void
{
    $l = listing_by_slug($slug);
    if (!$l || $l['status'] !== 'published') not_found();
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        $name = mb_substr(post('name'), 0, 120);
        $email = strtolower(post('email'));
        if (!spam_check()) $errors[] = 'Submission blocked.';
        if (mb_strlen($name) < 2) $errors[] = 'Please enter your name.';
        if (!valid_email($email)) $errors[] = 'Please enter a valid email address.';
        if (!post('confirm')) $errors[] = 'Please confirm you are authorized to manage this property.';
        if ($l['claimed']) $errors[] = 'This listing has already been claimed. Contact us if you believe this is a mistake.';
        if (!stripe_ready()) $errors[] = 'Online payments are being set up. Please email info@westcarrolltonapartments.com to claim this listing today.';
        if (!$errors) {
            try {
                redirect(start_checkout('claim', (int)$l['id'], $name, $email, $l['name']), 303);
            } catch (Throwable $e) {
                error_log('[claim] ' . $e->getMessage());
                $errors[] = 'We could not start the payment. Please try again or contact us.';
            }
        }
    }
    render('pages/claim', compact('l', 'errors'), [
        'title' => 'Claim ' . $l['name'] . ' | Owner & Manager Access',
        'description' => 'Are you the owner or manager of ' . $l['name'] . '? Claim the listing to show your contact details and edit photos, rents and amenities.',
        'canonical' => '/claim/' . $l['slug'] . '/',
        'robots' => 'noindex, follow',
        'nocache' => true,
        'breadcrumbs' => [['Home', '/'], ['Apartments', '/apartments/'], [$l['name'], $l['url']], ['Claim', null]],
    ]);
}

function page_submit(): void
{
    $errors = [];
    $old = $_POST;
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        [$d, $errors] = listing_from_post();
        $plan = post('plan') === 'paid' ? 'paid' : 'free';
        $sname = mb_substr(post('submitter_name'), 0, 120);
        $semail = strtolower(post('submitter_email'));
        if (!spam_check()) $errors[] = 'Submission blocked.';
        if (mb_strlen($sname) < 2) $errors[] = 'Please enter your name.';
        if (!valid_email($semail)) $errors[] = 'Please enter a valid email address for yourself.';
        if ($plan === 'paid' && !stripe_ready()) $errors[] = 'Paid listings are temporarily unavailable while payments are set up. Choose the free option or contact us.';

        if (!$errors) {
            $pdo = db();
            $d['slug'] = $d['name'];
            $d['status'] = $plan === 'paid' ? 'awaiting_payment' : 'pending';
            $d['source'] = $plan;
            $d['submitter_name'] = $sname;
            $d['submitter_email'] = $semail;
            $d['contact_visible'] = 0;
            $photos = [];
            foreach (normalize_files($_FILES['photos'] ?? []) as $f) {
                if (count($photos) >= 8) break;
                if ($p = save_uploaded_photo($f)) $photos[] = $p;
            }
            if ($photos) $d['photos'] = $photos;
            if ($geo = geocode($d['address'] . ', ' . $d['city'] . ', OH ' . $d['zip'])) [$d['lat'], $d['lng']] = $geo;
            $id = listing_insert($pdo, $d);

            if ($plan === 'paid') {
                try {
                    redirect(start_checkout('submit', $id, $sname, $semail, $d['name']), 303);
                } catch (Throwable $e) {
                    error_log('[submit] ' . $e->getMessage());
                    $pdo->prepare("UPDATE listings SET status = 'pending', source = 'free' WHERE id = ?")->execute([$id]);
                    flash('error', 'We could not start the payment, so your listing was saved as a free submission for review instead.');
                }
            }
            send_mail($semail, 'We received your listing: ' . $d['name'],
                '<p>Hi ' . e($sname) . ',</p><p>Thanks for submitting <strong>' . e($d['name']) . '</strong> to West Carrollton Apartments. Our team will review it, usually within 2 business days, and email you when it is live.</p>'
                . '<p>Free listings are published with contact details hidden. Want your phone, email and website shown, plus an owner account to edit the listing any time? You can upgrade for a one-time $' . (listing_price_cents() / 100) . ' once it is approved.</p>');
            notify_admin('New free listing submission: ' . $d['name'],
                '<p>' . e($sname) . ' (' . e($semail) . ') submitted <strong>' . e($d['name']) . '</strong>, ' . e($d['address']) . '.</p><p><a href="' . e(url('/admin/listings/?status=pending')) . '">Review pending listings</a></p>', $semail);
            redirect('/list-your-property/thanks/', 303);
        }
    }
    render('pages/submit', compact('errors', 'old'), [
        'title' => 'List Your Property in West Carrollton, OH | Free or $' . (listing_price_cents() / 100) . ' Owner Listing',
        'description' => 'Add your apartment, townhome or rental community to the West Carrollton, Ohio apartment directory. Free reviewed listings or an instant $' . (listing_price_cents() / 100) . ' owner listing with contact details.',
        'canonical' => '/list-your-property/',
        'nocache' => true,
        'breadcrumbs' => [['Home', '/'], ['List Your Property', null]],
    ]);
}

function normalize_files(array $f): array
{
    if (empty($f['name'])) return [];
    if (!is_array($f['name'])) return [$f];
    $out = [];
    foreach ($f['name'] as $i => $n) {
        if ($n === '') continue;
        $out[] = ['name' => $n, 'type' => $f['type'][$i], 'tmp_name' => $f['tmp_name'][$i], 'error' => $f['error'][$i], 'size' => $f['size'][$i]];
    }
    return $out;
}

function page_submit_thanks(): void
{
    render('pages/message', [
        'heading' => 'Thanks! Your listing was submitted.',
        'body' => '<p>We emailed you a confirmation. Our team reviews free submissions, usually within 2 business days, and we will email you when your listing goes live.</p><p>Free listings show with contact details hidden. After approval you can upgrade for a one-time $' . (listing_price_cents() / 100) . ' to display your phone, email and website and get an owner account to manage the listing.</p><p><a class="btn" href="/apartments/">Browse the directory</a></p>',
    ], ['title' => 'Listing Submitted', 'robots' => 'noindex', 'nocache' => true]);
}

function page_checkout_success(): void
{
    $sid = $_GET['session_id'] ?? '';
    $p = null;
    if ($sid && stripe_ready()) {
        try {
            $p = fulfill_session(stripe_request('GET', 'checkout/sessions/' . rawurlencode($sid)));
        } catch (Throwable $e) {
            error_log('[success] ' . $e->getMessage());
        }
    }
    if (!$p) {
        render('pages/message', ['heading' => 'We are confirming your payment', 'body' => '<p>Your payment is being confirmed. You will receive an email shortly. If you do not get one within 15 minutes, contact <a href="mailto:info@westcarrolltonapartments.com">info@westcarrolltonapartments.com</a>.</p>'],
            ['title' => 'Payment Processing', 'robots' => 'noindex', 'nocache' => true]);
    }
    $l = listing_by_id((int)$p['listing_id']);
    $u = user_by_email($p['email']);
    $verified = $u && $u['verified_at'];
    render('pages/message', [
        'heading' => 'Payment received. Thank you!',
        'body' => '<p><strong>' . e($l['name'] ?? 'Your listing') . '</strong> is live and your contact details are now shown to renters.</p>'
            . ($verified
                ? '<p>The listing has been added to your owner account.</p><p><a class="btn" href="/account/">Go to my account</a></p>'
                : '<p><strong>One more step:</strong> we sent a verification link to <strong>' . e($p['email']) . '</strong>. Click it to activate your owner account and start editing your listing.</p>')
            . '<p><a href="' . e($l['url'] ?? '/apartments/') . '">View the listing</a></p>',
    ], ['title' => 'Payment Received', 'robots' => 'noindex', 'nocache' => true]);
}

function page_checkout_cancel(): void
{
    $pid = (int)($_GET['p'] ?? 0);
    $st = db()->prepare("SELECT * FROM payments WHERE id = ? AND status = 'pending'");
    $st->execute([$pid]);
    $p = $st->fetch();
    $l = $p ? listing_by_id((int)$p['listing_id']) : null;
    $body = '<p>Your payment was cancelled and you were not charged.</p>';
    if ($p && $p['purpose'] === 'submit' && $l && $l['status'] === 'awaiting_payment') {
        // keep their work: convert to a free submission for review
        db()->prepare("UPDATE listings SET status = 'pending', source = 'free' WHERE id = ?")->execute([$l['id']]);
        db()->prepare("UPDATE payments SET status = 'cancelled' WHERE id = ?")->execute([$pid]);
        $body .= '<p>We saved <strong>' . e($l['name']) . '</strong> as a <strong>free submission</strong>. Our team will review it and email you when it is live (contact details hidden). You can upgrade later.</p>';
        notify_admin('New free listing submission: ' . $l['name'], '<p>Paid checkout was cancelled, saved as a free submission. <a href="' . e(url('/admin/listings/?status=pending')) . '">Review</a></p>');
    } elseif ($l) {
        $body .= '<p><a class="btn" href="/claim/' . e($l['slug']) . '/">Try again</a> &nbsp; <a href="' . e($l['url']) . '">Back to the listing</a></p>';
    }
    render('pages/message', ['heading' => 'Payment cancelled', 'body' => $body], ['title' => 'Payment Cancelled', 'robots' => 'noindex', 'nocache' => true]);
}

function stripe_webhook(): void
{
    $payload = file_get_contents('php://input');
    $secret = (string)setting('stripe_webhook_secret', '');
    if (!$secret || !stripe_verify_webhook($payload, $_SERVER['HTTP_STRIPE_SIGNATURE'] ?? '', $secret)) {
        http_response_code(400);
        exit('invalid signature');
    }
    $event = json_decode($payload, true);
    if (in_array($event['type'] ?? '', ['checkout.session.completed', 'checkout.session.async_payment_succeeded'], true)) {
        fulfill_session($event['data']['object']);
    }
    header('Content-Type: application/json');
    echo '{"received":true}';
}

/* ---------- Blog ---------- */

function page_blog(): void
{
    render('pages/blog', ['posts' => posts_all(), 'cat' => null], [
        'title' => 'West Carrollton Renter Blog: Apartment Tips, Moving & Budgeting',
        'description' => 'Practical renter advice for West Carrollton and the Dayton area: lease checklists, Ohio tenant rights, budgeting, moving and small-space decorating.',
        'canonical' => '/blog/',
        'breadcrumbs' => [['Home', '/'], ['Blog', null]],
    ]);
}

function page_blog_category(string $slug): void
{
    $cats = post_categories();
    if (!isset($cats[$slug])) not_found();
    $posts = array_filter(posts_all(), fn($p) => $p['category'] === $cats[$slug]);
    render('pages/blog', ['posts' => $posts, 'cat' => $cats[$slug]], [
        'title' => $cats[$slug] . ' for Renters | West Carrollton Apartments Blog',
        'description' => $cats[$slug] . ' articles for apartment renters in West Carrollton, Ohio and the Dayton area.',
        'canonical' => "/blog/category/$slug/",
        'breadcrumbs' => [['Home', '/'], ['Blog', '/blog/'], [$cats[$slug], null]],
    ]);
}

function page_post(string $slug): void
{
    $p = post_by_slug($slug);
    if (!$p) not_found();
    $related = array_slice(array_filter(posts_all(), fn($o) => $o['slug'] !== $slug && $o['category'] === $p['category']), 0, 3);
    if (count($related) < 3) $related = array_slice(array_filter(posts_all(), fn($o) => $o['slug'] !== $slug), 0, 3);
    $schema = [[
        '@context' => 'https://schema.org', '@type' => 'BlogPosting',
        'headline' => $p['title'], 'description' => $p['description'],
        'image' => url(photo_url($p['image'])), 'datePublished' => $p['date'], 'dateModified' => $p['updated'] ?? $p['date'],
        'mainEntityOfPage' => url("/blog/$slug/"),
        'author' => ['@type' => 'Organization', 'name' => cfg('site_name'), 'url' => url('/about/')],
        'publisher' => ['@type' => 'Organization', 'name' => cfg('site_name'), 'logo' => ['@type' => 'ImageObject', 'url' => url('/assets/img/logo.svg')]],
    ], breadcrumb_schema([['Home', '/'], ['Blog', '/blog/'], [$p['title'], "/blog/$slug/"]])];
    if (!empty($p['faq'])) {
        $schema[] = ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']]], $p['faq'])];
    }
    render('pages/post', compact('p', 'related'), [
        'title' => $p['meta_title'] ?? $p['title'],
        'description' => $p['description'],
        'canonical' => "/blog/$slug/",
        'image' => photo_url($p['image']),
        'og_type' => 'article',
        'schema' => $schema,
        'breadcrumbs' => [['Home', '/'], ['Blog', '/blog/'], [$p['title'], null]],
    ]);
}

/* ---------- Tools ---------- */

function tools_list(): array
{
    return [
        'rent-affordability-calculator' => ['Rent Affordability Calculator', 'How much rent can you afford on your income in West Carrollton?', '🧮'],
        'apartment-match-quiz' => ['Apartment Match Quiz', 'Answer 6 quick questions and we will match you with West Carrollton communities.', '🎯'],
        'roommate-rent-splitter' => ['Roommate Rent Splitter', 'Split rent fairly by room size, private bath and parking.', '🤝'],
        'moving-cost-estimator' => ['Moving Cost Estimator', 'Estimate the real cost of moving, from deposits to pizza for helpers.', '🚚'],
        'moving-checklist' => ['Interactive Moving Checklist', 'A week-by-week checklist that saves your progress.', '✅'],
        'room-planner' => ['Room Layout Planner', 'Drag furniture around a floor plan to see what fits before you sign.', '🛋️'],
    ];
}

function page_tools(): void
{
    render('pages/tools', ['tools' => tools_list()], [
        'title' => 'Free Renter Tools: Rent Calculator, Apartment Quiz & Room Planner',
        'description' => 'Free interactive tools for West Carrollton renters: rent affordability calculator, apartment match quiz, roommate rent splitter, moving cost estimator and room planner.',
        'canonical' => '/tools/',
        'breadcrumbs' => [['Home', '/'], ['Renter Tools', null]],
    ]);
}

function page_tool(string $slug): void
{
    $tools = tools_list();
    if (!isset($tools[$slug])) not_found();
    [$name, $desc] = $tools[$slug];
    render('tools/' . $slug, ['tool' => $tools[$slug], 'tools' => $tools, 'slug' => $slug, 'all' => listings_published()], [
        'title' => $name . ' | West Carrollton Apartments',
        'description' => $desc . ' Free and private: everything runs in your browser.',
        'canonical' => "/tools/$slug/",
        'schema' => [['@context' => 'https://schema.org', '@type' => 'WebApplication', 'name' => $name, 'url' => url("/tools/$slug/"), 'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD']],
            breadcrumb_schema([['Home', '/'], ['Renter Tools', '/tools/'], [$name, "/tools/$slug/"]])],
        'breadcrumbs' => [['Home', '/'], ['Renter Tools', '/tools/'], [$name, null]],
        'tools_js' => true,
    ]);
}

/* ---------- Static pages ---------- */

function page_guide(): void
{
    render('pages/guide', ['all' => listings_published()], [
        'title' => 'Living in West Carrollton, Ohio: Neighborhood Guide for Renters',
        'description' => 'What it is like to rent in West Carrollton, OH: parks, the Great Miami River Trail, schools, commute times to Dayton, shopping and apartment communities.',
        'canonical' => '/west-carrollton-living-guide/',
        'image' => photo_url('ext-1'),
        'breadcrumbs' => [['Home', '/'], ['Living Guide', null]],
        'leaflet' => true,
    ]);
}

function page_about(): void
{
    render('pages/about', [], [
        'title' => 'About West Carrollton Apartments',
        'description' => 'West Carrollton Apartments is an independent directory of apartment communities in West Carrollton, Ohio, built to help renters compare options.',
        'canonical' => '/about/',
        'breadcrumbs' => [['Home', '/'], ['About', null]],
    ]);
}

function page_contact(): void
{
    $errors = [];
    $sent = false;
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        $name = mb_substr(post('name'), 0, 120);
        $email = post('email');
        $subject = mb_substr(post('subject'), 0, 190);
        $body = mb_substr(post('message'), 0, 5000);
        if (!spam_check()) $errors[] = 'Message blocked.';
        if (mb_strlen($name) < 2) $errors[] = 'Please enter your name.';
        if (!valid_email($email)) $errors[] = 'Please enter a valid email.';
        if (mb_strlen($body) < 10) $errors[] = 'Please enter a message.';
        if (!$errors) {
            db()->prepare('INSERT INTO messages (name, email, subject, body, created_at) VALUES (?,?,?,?,?)')->execute([$name, $email, $subject, $body, now()]);
            notify_admin('Contact form: ' . ($subject ?: 'New message'), '<p><strong>' . e($name) . '</strong> (' . e($email) . ') wrote:</p><p>' . nl2br(e($body)) . '</p>', $email);
            $sent = true;
        }
    }
    render('pages/contact', compact('errors', 'sent'), [
        'title' => 'Contact West Carrollton Apartments',
        'description' => 'Questions about a listing, corrections or advertising? Contact the West Carrollton Apartments directory team.',
        'canonical' => '/contact/',
        'nocache' => true,
        'breadcrumbs' => [['Home', '/'], ['Contact', null]],
    ]);
}

function page_privacy(): void
{
    render('pages/privacy', [], ['title' => 'Privacy Policy | West Carrollton Apartments', 'description' => 'How West Carrollton Apartments collects, uses and protects your information.', 'canonical' => '/privacy-policy/', 'breadcrumbs' => [['Home', '/'], ['Privacy Policy', null]]]);
}

function page_terms(): void
{
    render('pages/terms', [], ['title' => 'Terms of Use | West Carrollton Apartments', 'description' => 'Terms of use for the West Carrollton Apartments directory, owner listings and payments.', 'canonical' => '/terms-of-use/', 'breadcrumbs' => [['Home', '/'], ['Terms of Use', null]]]);
}

function page_disclosure(): void
{
    render('pages/disclosure', [], ['title' => 'Affiliate Disclosure | West Carrollton Apartments', 'description' => 'West Carrollton Apartments participates in the Amazon Services LLC Associates Program.', 'canonical' => '/affiliate-disclosure/', 'breadcrumbs' => [['Home', '/'], ['Affiliate Disclosure', null]]]);
}

/* ---------- XML / robots ---------- */

function sitemap_xml(): void
{
    header('Content-Type: application/xml; charset=UTF-8');
    $u = [['/', 'daily', '1.0'], ['/apartments/', 'daily', '0.9']];
    foreach (array_keys(landing_pages()) as $k) {
        $f = landing_pages()[$k]['filter'];
        if (array_filter(listings_published(), $f)) $u[] = ["/apartments/$k/", 'weekly', '0.8'];
    }
    foreach (listings_published() as $l) $u[] = [$l['url'], 'weekly', '0.8', substr($l['updated_at'], 0, 10)];
    $u[] = ['/west-carrollton-living-guide/', 'monthly', '0.7'];
    $u[] = ['/list-your-property/', 'monthly', '0.6'];
    $u[] = ['/tools/', 'monthly', '0.6'];
    foreach (array_keys(tools_list()) as $t) $u[] = ["/tools/$t/", 'monthly', '0.6'];
    $u[] = ['/blog/', 'weekly', '0.7'];
    foreach (array_keys(post_categories()) as $c) $u[] = ["/blog/category/$c/", 'weekly', '0.4'];
    foreach (posts_all() as $p) $u[] = ['/blog/' . $p['slug'] . '/', 'monthly', '0.6', $p['updated'] ?? $p['date']];
    foreach (['/about/', '/contact/', '/privacy-policy/', '/terms-of-use/', '/affiliate-disclosure/'] as $s) $u[] = [$s, 'yearly', '0.3'];
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($u as $r) {
        echo '  <url><loc>' . e(url($r[0])) . '</loc>' . (isset($r[3]) ? '<lastmod>' . e($r[3]) . '</lastmod>' : '') . '<changefreq>' . $r[1] . '</changefreq><priority>' . $r[2] . "</priority></url>\n";
    }
    echo '</urlset>';
}

function robots_txt(): void
{
    header('Content-Type: text/plain; charset=UTF-8');
    echo "User-agent: *\nDisallow: /admin/\nDisallow: /account/\nDisallow: /claim/\nDisallow: /checkout/\nDisallow: /compare/?\nDisallow: /app/\n\nSitemap: " . url('/sitemap.xml') . "\n";
}
