<?php defined('WCA') || exit;

function admin_meta(string $t): array
{
    return ['title' => $t . ' | Admin', 'robots' => 'noindex, nofollow', 'nocache' => true, 'body_class' => 'admin'];
}

function admin_login(): void
{
    if (is_admin()) redirect('/admin/');
    $error = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        $pdo = db();
        $ip = client_ip();
        $pdo->prepare('DELETE FROM login_attempts WHERE created_at < ?')->execute([date('Y-m-d H:i:s', time() - 900)]);
        $st = $pdo->prepare('SELECT COUNT(*) FROM login_attempts WHERE ip = ?');
        $st->execute([$ip]);
        if ((int)$st->fetchColumn() >= 8) {
            $error = 'Too many attempts. Please wait 15 minutes.';
        } elseif (hash_equals((string)cfg('admin_user'), post('username')) && cfg('admin_password_hash') && password_verify(post('password'), (string)cfg('admin_password_hash'))) {
            session_start_once();
            session_regenerate_id(true);
            $_SESSION['admin'] = true;
            redirect('/admin/');
        } else {
            $pdo->prepare('INSERT INTO login_attempts (ip, created_at) VALUES (?, ?)')->execute([$ip, now()]);
            usleep(400000);
            $error = 'Invalid username or password.';
        }
    }
    render('admin/login', compact('error'), admin_meta('Sign In'));
}

function admin_logout(): void
{
    session_start_once();
    unset($_SESSION['admin']);
    redirect('/admin/login/');
}

function admin_dashboard(): void
{
    require_admin();
    $pdo = db();
    $c = fn($sql) => (int)$pdo->query($sql)->fetchColumn();
    $stats = [
        'published' => $c("SELECT COUNT(*) FROM listings WHERE status='published'"),
        'pending' => $c("SELECT COUNT(*) FROM listings WHERE status='pending'"),
        'claimed' => $c('SELECT COUNT(*) FROM listings WHERE owner_id IS NOT NULL'),
        'users' => $c('SELECT COUNT(*) FROM users'),
        'revenue' => $c("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='paid'") / 100,
        'messages' => $c('SELECT COUNT(*) FROM messages WHERE is_read = 0'),
    ];
    $pending = array_map('listing_hydrate', $pdo->query("SELECT * FROM listings WHERE status='pending' ORDER BY id DESC LIMIT 10")->fetchAll());
    $payments = $pdo->query("SELECT p.*, l.name AS listing_name FROM payments p LEFT JOIN listings l ON l.id=p.listing_id ORDER BY p.id DESC LIMIT 8")->fetchAll();
    $top = $pdo->query("SELECT id, name, slug, views FROM listings WHERE status='published' ORDER BY views DESC LIMIT 5")->fetchAll();
    render('admin/dashboard', compact('stats', 'pending', 'payments', 'top'), admin_meta('Dashboard'));
}

function admin_listings(): void
{
    require_admin();
    $status = $_GET['status'] ?? '';
    $q = trim($_GET['q'] ?? '');
    $sql = 'SELECT l.*, u.email AS owner_email FROM listings l LEFT JOIN users u ON u.id = l.owner_id WHERE 1=1';
    $args = [];
    if ($status !== '') { $sql .= ' AND l.status = ?'; $args[] = $status; }
    if ($q !== '') { $sql .= ' AND (l.name LIKE ? OR l.address LIKE ?)'; $args[] = "%$q%"; $args[] = "%$q%"; }
    $sql .= ' ORDER BY l.id DESC';
    $st = db()->prepare($sql);
    $st->execute($args);
    $rows = array_map('listing_hydrate', $st->fetchAll());
    render('admin/listings', compact('rows', 'status', 'q'), admin_meta('Listings'));
}

function admin_edit_listing(): void
{
    require_admin();
    $id = (int)($_GET['id'] ?? 0);
    $l = $id ? listing_by_id($id) : null;
    if ($id && !$l) not_found();
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        [$d, $errors] = listing_from_post(true);
        $d['status'] = in_array(post('status'), ['published', 'pending', 'rejected', 'draft', 'awaiting_payment'], true) ? post('status') : 'draft';
        $d['featured'] = post('featured') ? 1 : 0;
        $d['contact_visible'] = post('contact_visible') ? 1 : 0;
        $d['lat'] = is_numeric(post('lat')) ? (float)post('lat') : null;
        $d['lng'] = is_numeric(post('lng')) ? (float)post('lng') : null;
        $ownerEmail = strtolower(post('owner_email'));
        if ($ownerEmail === '') {
            $d['owner_id'] = null;
        } elseif ($ou = user_by_email($ownerEmail)) {
            $d['owner_id'] = (int)$ou['id'];
        } else {
            $errors[] = 'No owner account exists with that email.';
        }
        $slug = slugify(post('slug') ?: $d['name']);
        $photos = $l ? array_values(array_filter(
            json_decode(db()->query('SELECT photos FROM listings WHERE id = ' . (int)$id)->fetchColumn() ?: '[]', true) ?: [],
            fn($p) => !in_array($p, (array)($_POST['remove_photos'] ?? []), true))) : [];
        foreach (normalize_files($_FILES['photos'] ?? []) as $f) {
            if ($p = save_uploaded_photo($f)) $photos[] = $p;
        }
        foreach (array_slice(array_filter(array_map('trim', preg_split('/\s+/', post('photo_urls')))), 0, 15) as $pu) {
            if ($p = import_photo_url($pu)) $photos[] = $p; else $errors[] = 'Could not import photo: ' . $pu;
        }
        $stock = array_values(array_filter(array_map('trim', explode(',', post('stock_photos')))));
        if ($stock && !$photos) $photos = $stock;
        $d['photos'] = $photos;
        if (!$d['lat'] && ($geo = geocode($d['address'] . ', ' . $d['city'] . ', OH ' . $d['zip']))) [$d['lat'], $d['lng']] = $geo;
        if (!$errors) {
            $wasPending = $l && $l['status'] === 'pending';
            if ($l) {
                $d['slug'] = unique_slug(db(), $slug, $id);
                listing_update($id, $d);
            } else {
                $d['slug'] = $slug;
                $d['source'] = 'seed';
                $id = listing_insert(db(), $d);
            }
            if ($wasPending && $d['status'] === 'published') listing_approved_email(listing_by_id($id));
            flash('success', 'Listing saved.');
            redirect('/admin/listings/edit/?id=' . $id);
        }
        $l = array_merge($l ?? [], $d);
    }
    $owner = null;
    if (!empty($l['owner_id'])) {
        $st = db()->prepare('SELECT * FROM users WHERE id = ?');
        $st->execute([$l['owner_id']]);
        $owner = $st->fetch();
    }
    render('admin/edit', compact('l', 'errors', 'owner'), admin_meta($l ? 'Edit ' . $l['name'] : 'New Listing'));
}

function listing_approved_email(?array $l): void
{
    if (!$l || !$l['submitter_email']) return;
    send_mail($l['submitter_email'], 'Your listing is live: ' . $l['name'], listing_approved_email_html($l));
}

function listing_approved_email_html(array $l): string
{
    $price = '$' . rtrim(rtrim(number_format(listing_price_cents() / 100, 2), '0'), '.');
    $live = url($l['url']);
    $claim = url('/claim/' . $l['slug'] . '/');
    $first = trim(explode(' ', trim((string)$l['submitter_name']))[0]) ?: 'there';
    $li = fn($t) => '<tr><td style="padding:4px 10px 4px 0;vertical-align:top;color:#1b7f4b;font-weight:bold">&#10003;</td><td style="padding:4px 0">' . $t . '</td></tr>';
    return '<p style="margin:0 0 14px">Hi ' . e($first) . ',</p>'
        . '<p style="margin:0 0 14px">Good news! Your listing <strong>' . e($l['name']) . '</strong> has been reviewed and is now <strong>live</strong> on West Carrollton Apartments.</p>'
        . email_button($live, 'View your live listing')
        . '<p style="margin:0 0 6px"><strong>Your listing includes:</strong></p>'
        . '<table cellpadding="0" cellspacing="0" style="margin:0 0 18px;font-size:15px">'
        . $li('Photos, rent, floor plans and amenities shown to renters')
        . $li('A spot in our West Carrollton directory, map and category pages')
        . '<tr><td style="padding:4px 10px 4px 0;vertical-align:top;color:#b42318;font-weight:bold">&#128274;</td><td style="padding:4px 0">Your phone, email and website are <strong>hidden</strong> on free listings</td></tr>'
        . '</table>'
        . '<table cellpadding="0" cellspacing="0" width="100%" style="background:#fff8f1;border:1px solid #fde3c8;border-radius:10px;margin:0 0 18px"><tr><td style="padding:20px">'
        . '<p style="margin:0 0 4px;font-size:12px;font-weight:bold;letter-spacing:.08em;text-transform:uppercase;color:#e36414">Upgrade for a one-time ' . $price . '</p>'
        . '<p style="margin:0 0 10px;font-size:18px;font-weight:bold;color:#0a3540">Get more renters calling you</p>'
        . '<table cellpadding="0" cellspacing="0" style="font-size:15px">'
        . $li('<strong>Featured placement:</strong> your listing is prioritized at the top of search results and category pages')
        . $li('<strong>Contact info made public:</strong> your phone, email and website shown on your listing')
        . $li('<strong>Verified owner badge</strong> that builds trust with renters')
        . $li('<strong>Owner account</strong> to update rents, specials, photos and amenities any time')
        . '</table>'
        . email_button($claim, 'Feature my listing for ' . $price)
        . '<p style="margin:0;font-size:13px;color:#6b7280">One-time payment, no subscription. Secure checkout by Stripe; promo codes accepted.</p>'
        . '</td></tr></table>'
        . '<p style="margin:0 0 14px">Need to change something on your listing? Just reply to this email and we\'ll take care of it.</p>'
        . '<p style="margin:0">Thanks for listing with us,<br><strong>The West Carrollton Apartments team</strong><br><a href="mailto:info@westcarrolltonapartments.com" style="color:#0f4c5c">info@westcarrolltonapartments.com</a></p>';
}

function admin_listing_action(): void
{
    require_admin();
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') redirect('/admin/listings/');
    csrf_check();
    $id = (int)post('id');
    $l = listing_by_id($id);
    if (!$l) not_found();
    switch (post('action')) {
        case 'approve':
            listing_update($id, ['status' => 'published']);
            listing_approved_email(listing_by_id($id));
            flash('success', 'Approved and published: ' . $l['name']);
            break;
        case 'reject':
            listing_update($id, ['status' => 'rejected']);
            flash('success', 'Rejected: ' . $l['name']);
            break;
        case 'unpublish':
            listing_update($id, ['status' => 'draft']);
            flash('success', 'Unpublished: ' . $l['name']);
            break;
        case 'delete':
            db()->prepare('DELETE FROM listings WHERE id = ?')->execute([$id]);
            flash('success', 'Deleted: ' . $l['name']);
            redirect('/admin/listings/');
        case 'revoke':
            db()->prepare('UPDATE listings SET owner_id = NULL, contact_visible = 0 WHERE id = ?')->execute([$id]);
            flash('success', 'Owner access removed for ' . $l['name']);
            break;
    }
    redirect($_SERVER['HTTP_REFERER'] ?? '/admin/listings/');
}

function admin_users(): void
{
    require_admin();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        $id = (int)post('id');
        if (post('action') === 'verify') db()->prepare('UPDATE users SET verified_at = ?, verify_token = NULL WHERE id = ?')->execute([now(), $id]);
        if (post('action') === 'resend') {
            $st = db()->prepare('SELECT * FROM users WHERE id = ?'); $st->execute([$id]);
            if (($u = $st->fetch()) && $u['verify_token']) send_mail($u['email'], 'Verify your email', '<p>Hi ' . e($u['name']) . ',</p><p>Please verify your email to activate your owner account:</p>' . email_button(url('/account/verify/?token=' . $u['verify_token']), 'Verify my email'));
        }
        if (post('action') === 'create') {
            $email = strtolower(post('email'));
            if (valid_email($email) && post('name') !== '') {
                $u = user_find_or_create(post('name'), $email);
                send_mail($u['email'], 'Your owner account', '<p>Hi ' . e($u['name']) . ',</p><p>An owner account was created for you on West Carrollton Apartments. Verify your email to activate it:</p>' . email_button(url('/account/verify/?token=' . $u['verify_token']), 'Verify my email'));
            }
        }
        flash('success', 'Done.');
        redirect('/admin/users/');
    }
    $users = db()->query('SELECT u.*, (SELECT COUNT(*) FROM listings l WHERE l.owner_id = u.id) AS listings FROM users u ORDER BY u.id DESC')->fetchAll();
    render('admin/users', compact('users'), admin_meta('Owners'));
}

function admin_payments(): void
{
    require_admin();
    $payments = db()->query('SELECT p.*, l.name AS listing_name, l.slug FROM payments p LEFT JOIN listings l ON l.id = p.listing_id ORDER BY p.id DESC LIMIT 500')->fetchAll();
    render('admin/payments', compact('payments'), admin_meta('Payments'));
}

function admin_messages(): void
{
    require_admin();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        if (post('action') === 'delete') db()->prepare('DELETE FROM messages WHERE id = ?')->execute([(int)post('id')]);
        redirect('/admin/messages/');
    }
    $messages = db()->query('SELECT * FROM messages ORDER BY id DESC LIMIT 300')->fetchAll();
    db()->exec('UPDATE messages SET is_read = 1');
    render('admin/messages', compact('messages'), admin_meta('Messages'));
}

function admin_settings(): void
{
    require_admin();
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        if (post('action') === 'save') {
            foreach (['stripe_secret_key', 'stripe_webhook_secret'] as $k) {
                if (post($k) !== '') setting_save($k, post($k));
            }
            if (post('clear_stripe')) { setting_save('stripe_secret_key', ''); setting_save('stripe_webhook_secret', ''); }
            $price = (int)round((float)post('price') * 100);
            if ($price >= 50) setting_save('listing_price_cents', (string)$price);
            flash('success', 'Settings saved.');
        } elseif (post('action') === 'test_email') {
            $ok = send_mail((string)cfg('admin_email'), 'Test email from West Carrollton Apartments', '<p>Email delivery is working.</p>');
            flash($ok ? 'success' : 'error', $ok ? 'Test email sent to ' . cfg('admin_email') : 'Email failed. Check SMTP settings in app/config.php.');
        } elseif (post('action') === 'test_stripe') {
            try {
                $b = stripe_request('GET', 'balance');
                flash('success', 'Stripe connected (' . (($b['livemode'] ?? false) ? 'LIVE mode' : 'TEST mode') . ').');
            } catch (Throwable $e) {
                flash('error', $e->getMessage());
            }
        }
        redirect('/admin/settings/');
    }
    $key = (string)setting('stripe_secret_key', '');
    render('admin/settings', [
        'stripe_key_hint' => $key ? substr($key, 0, 8) . '…' . substr($key, -4) : '',
        'webhook_set' => (string)setting('stripe_webhook_secret', '') !== '',
        'price' => listing_price_cents() / 100,
    ], admin_meta('Settings'));
}
