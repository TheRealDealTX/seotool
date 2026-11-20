<?php defined('WCA') || exit;

function account_meta(string $title): array
{
    return ['title' => $title . ' | West Carrollton Apartments', 'robots' => 'noindex, nofollow', 'nocache' => true];
}

/** Passwordless sign-in: email a one-time link. */
function account_login(): void
{
    if (current_user()) redirect('/account/');
    $sent = false;
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        $email = strtolower(post('email'));
        if (!valid_email($email)) {
            $errors[] = 'Please enter a valid email address.';
        } else {
            $u = user_by_email($email);
            if ($u) {
                if (!$u['verified_at']) {
                    send_mail($u['email'], 'Verify your email', '<p>Hi ' . e($u['name']) . ',</p><p>Please verify your email to activate your owner account:</p>'
                        . email_button(url('/account/verify/?token=' . $u['verify_token']), 'Verify my email'));
                } else {
                    $tok = random_token();
                    db()->prepare('UPDATE users SET login_token = ?, login_expires = ? WHERE id = ?')
                        ->execute([hash('sha256', $tok), date('Y-m-d H:i:s', time() + 1800), $u['id']]);
                    send_mail($u['email'], 'Your sign-in link', '<p>Hi ' . e($u['name']) . ',</p><p>Click below to sign in to your West Carrollton Apartments owner account. This link expires in 30 minutes and can be used once.</p>'
                        . email_button(url('/account/magic/?token=' . $tok), 'Sign in'));
                }
            }
            $sent = true; // same response whether or not the account exists
        }
    }
    render('account/login', compact('sent', 'errors'), account_meta('Owner Sign In'));
}

function account_verify(): void
{
    $tok = (string)($_GET['token'] ?? '');
    $st = db()->prepare('SELECT * FROM users WHERE verify_token = ? AND verify_token IS NOT NULL');
    $st->execute([$tok]);
    $u = $tok ? $st->fetch() : null;
    if (!$u) {
        render('pages/message', ['heading' => 'Link expired', 'body' => '<p>This verification link is invalid or was already used. <a href="/account/login/">Sign in</a> to get a new link.</p>'], account_meta('Verify Email'));
    }
    db()->prepare('UPDATE users SET verified_at = COALESCE(verified_at, ?), verify_token = NULL WHERE id = ?')->execute([now(), $u['id']]);
    login_user((int)$u['id']);
    flash('success', 'Your email is verified and your owner account is active. Welcome!');
    redirect('/account/');
}

function account_magic(): void
{
    $tok = (string)($_GET['token'] ?? '');
    $st = db()->prepare('SELECT * FROM users WHERE login_token = ? AND login_expires > ? AND verified_at IS NOT NULL');
    $st->execute([hash('sha256', $tok), now()]);
    $u = $tok ? $st->fetch() : null;
    if (!$u) {
        render('pages/message', ['heading' => 'Link expired', 'body' => '<p>This sign-in link has expired or was already used. <a href="/account/login/">Request a new one</a>.</p>'], account_meta('Sign In'));
    }
    db()->prepare('UPDATE users SET login_token = NULL, login_expires = NULL WHERE id = ?')->execute([$u['id']]);
    login_user((int)$u['id']);
    redirect('/account/');
}

function account_logout(): void
{
    session_start_once();
    $_SESSION = [];
    session_destroy();
    setcookie(session_name(), '', time() - 3600, '/');
    redirect('/');
}

function account_dashboard(): void
{
    $u = require_user();
    $listings = listings_by_owner((int)$u['id']);
    $st = db()->prepare('SELECT p.*, l.name AS listing_name FROM payments p LEFT JOIN listings l ON l.id = p.listing_id WHERE p.user_id = ? ORDER BY p.id DESC');
    $st->execute([$u['id']]);
    $payments = $st->fetchAll();
    render('account/dashboard', compact('u', 'listings', 'payments'), account_meta('My Account'));
}

function account_edit_listing(): void
{
    $u = require_user();
    $l = listing_by_id((int)($_GET['id'] ?? 0));
    if (!$l || (int)$l['owner_id'] !== (int)$u['id']) not_found();
    $errors = [];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        csrf_check();
        [$d, $errors] = listing_from_post();
        // photos
        $raw = json_decode(db()->query('SELECT photos FROM listings WHERE id = ' . (int)$l['id'])->fetchColumn() ?: '[]', true) ?: [];
        $photos = array_values(array_filter($raw, fn($p) => !in_array($p, (array)($_POST['remove_photos'] ?? []), true)));
        foreach (normalize_files($_FILES['photos'] ?? []) as $f) {
            if (count($photos) >= 12) break;
            if ($p = save_uploaded_photo($f)) $photos[] = $p; else $errors[] = 'One photo could not be used (JPG, PNG or WebP up to 6 MB).';
        }
        if (!$errors) {
            if ($d['address'] !== $l['address'] && ($geo = geocode($d['address'] . ', ' . $d['city'] . ', OH ' . $d['zip']))) [$d['lat'], $d['lng']] = $geo;
            $d['photos'] = $photos;
            listing_update((int)$l['id'], $d);
            flash('success', 'Your listing was updated.');
            redirect('/account/listings/edit/?id=' . $l['id']);
        }
        $l = array_merge($l, $d);
    }
    render('account/edit', compact('u', 'l', 'errors'), account_meta('Edit ' . $l['name']));
}
