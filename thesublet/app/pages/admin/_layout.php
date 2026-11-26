<?php defined('APP') || exit;

function admin_page(string $title, string $body): void
{
    $nav = [
        '/admin/' => 'Dashboard', '/admin/listings/?status=pending' => 'Review queue', '/admin/listings/' => 'Listings',
        '/admin/owners/' => 'Owners', '/admin/payments/' => 'Payments', '/admin/messages/' => 'Messages',
        '/admin/claims/' => 'Claims', '/admin/reports/' => 'Reports', '/admin/settings/' => 'Settings',
    ];
    $pending = (int)val("SELECT COUNT(*) FROM listings WHERE status = 'pending'");
    $openReports = (int)val('SELECT COUNT(*) FROM reports WHERE resolved = 0');
    $openClaims = (int)val("SELECT COUNT(*) FROM claims WHERE status = 'pending'");
    $h = '<div class="admin wrap"><nav class="admin-nav">';
    foreach ($nav as $u => $l) {
        $badge = ($l === 'Review queue' && $pending) ? ' <span class="pill">' . $pending . '</span>' : (($l === 'Reports' && $openReports) ? ' <span class="pill">' . $openReports . '</span>' : (($l === 'Claims' && $openClaims) ? ' <span class="pill">' . $openClaims . '</span>' : ''));
        $h .= '<a href="' . e($u) . '">' . e($l) . $badge . '</a>';
    }
    $h .= '<a href="/admin/logout/">Log out</a></nav>' . flashes() . '<h1>' . e($title) . '</h1>' . $body . '</div>';
    page(['title' => $title . ' · Admin · The Sublet', 'robots' => 'noindex, nofollow', 'body' => $h, 'body_class' => 'is-admin', 'h_extra' => leaflet_head()]);
}

function admin_guard_post(): void
{
    if ($g = form_guard()) { flash($g, 'err'); redirect($_SERVER['REQUEST_URI'] ?? '/admin/'); }
}

function admin_listing_action(int $id, string $do, string $reason): void
{
    $l = listing_get($id);
    if (!$l) return;
    switch ($do) {
        case 'approve':
            publish_listing($id);
            $l = listing_get($id);
            if ($l['tier'] === 'free') send_mail($l['contact_email'], 'Your listing is live: ' . mb_strimwidth($l['title'], 0, 70, '…', 'UTF-8'), view('emails/approved', ['l' => $l]));
            break;
        case 'reject':
            update('listings', ['status' => 'rejected', 'reject_reason' => mb_substr($reason, 0, 500), 'updated_at' => now()], 'id = ?', [$id]);
            send_mail($l['contact_email'], 'About your listing on The Sublet', view('emails/rejected', ['l' => listing_get($id)]));
            break;
        case 'expire':
            update('listings', ['status' => 'expired', 'updated_at' => now()], 'id = ?', [$id]);
            break;
        case 'rented':
            update('listings', ['status' => 'rented', 'updated_at' => now()], 'id = ?', [$id]);
            break;
        case 'delete':
            q('DELETE FROM photos WHERE listing_id = ?', [$id]);
            q('DELETE FROM reports WHERE listing_id = ?', [$id]);
            q('DELETE FROM listings WHERE id = ?', [$id]);
            break;
    }
}
