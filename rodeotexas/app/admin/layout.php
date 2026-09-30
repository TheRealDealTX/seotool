<?php
/**
 * Admin layout and small form helpers. Output is always escaped with e().
 * The admin runs under a strict Content-Security-Policy (no inline scripts or
 * inline style attributes), so behaviour lives in /assets/js/admin.js.
 */
declare(strict_types=1);

use RT\Auth;
use RT\Db;

function admin_url(string $page, array $q = []): string
{
    return '/admin/?' . http_build_query(array_merge(['page' => $page], $q));
}

function flash(string $msg, string $type = 'success'): void
{
    $_SESSION['flash'][] = [$type, $msg];
}

function admin_header(string $title): void
{
    $u = Auth::user();
    $open = $u ? (int) Db::val("SELECT COUNT(*) FROM review_items WHERE status = 'open'") : 0;
    $nav = [
        'dashboard' => 'Dashboard', 'events' => 'Events', 'review' => 'Review queue' . ($open ? " ({$open})" : ''),
        'sources' => 'Sources', 'imports' => 'Import history', 'venues' => 'Venues', 'articles' => 'Articles',
        'links' => 'Links & missing info', 'redirects' => 'Redirects', 'associations' => 'Associations', 'account' => 'Account',
    ];
    $cur = (string) ($_GET['page'] ?? 'dashboard');
    ?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<?php /* Hostinger's server replaces the CSP response header, so the policy is repeated here (frame-ancestors is covered by X-Frame-Options: DENY). */ ?>
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: https:; style-src 'self'; script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; object-src 'none'">
<title><?= e($title) ?> · Rodeo Texas admin</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="<?= e(asset('assets/css/admin.css')) ?>">
</head>
<body>
<?php if ($u): ?>
<header class="a-top">
  <a class="a-brand" href="/admin/">Rodeo Texas · Admin</a>
  <nav class="a-nav" aria-label="Admin"><?php foreach ($nav as $k => $label): ?><a href="<?= e(admin_url($k)) ?>"<?= $cur === $k || rtrim($cur, 's') === rtrim($k, 's') ? ' aria-current="page"' : '' ?>><?= e($label) ?></a><?php endforeach; ?></nav>
  <div class="a-user"><a href="/" target="_blank" rel="noopener">View site</a> · <?= e($u['email']) ?> ·
    <form method="post" action="<?= e(admin_url('logout')) ?>" class="inline"><?= Auth::csrfField() ?><button class="linkbtn" type="submit">Log out</button></form></div>
</header>
<?php endif; ?>
<main class="a-main">
<?php foreach ($_SESSION['flash'] ?? [] as [$t, $m]): ?><div class="alert alert--<?= e($t) ?>" role="status"><?= e($m) ?></div><?php endforeach; unset($_SESSION['flash']); ?>
<h1><?= e($title) ?></h1>
<?php
}

function admin_footer(): void
{
    echo '</main><script src="' . e(asset('assets/js/admin.js')) . '" defer></script></body></html>';
}

/** Text input row. */
function f_text(string $name, string $label, $value, array $o = []): string
{
    $type = $o['type'] ?? 'text';
    $id = 'f_' . $name;
    return '<div class="field"><label for="' . e($id) . '">' . e($label) . (!empty($o['required']) ? ' *' : '') . '</label>'
        . '<input id="' . e($id) . '" type="' . e($type) . '" name="' . e($name) . '" value="' . e($value) . '"'
        . (!empty($o['required']) ? ' required' : '') . (isset($o['placeholder']) ? ' placeholder="' . e($o['placeholder']) . '"' : '')
        . (isset($o['maxlength']) ? ' maxlength="' . (int) $o['maxlength'] . '"' : '') . '>'
        . (isset($o['help']) ? '<small>' . e($o['help']) . '</small>' : '') . '</div>';
}

function f_area(string $name, string $label, $value, array $o = []): string
{
    $id = 'f_' . $name;
    return '<div class="field"><label for="' . e($id) . '">' . e($label) . '</label><textarea id="' . e($id) . '" name="' . e($name) . '" rows="' . (int) ($o['rows'] ?? 4) . '"'
        . (!empty($o['mono']) ? ' class="mono"' : '') . '>' . e($value) . '</textarea>' . (isset($o['help']) ? '<small>' . e($o['help']) . '</small>' : '') . '</div>';
}

/** @param array<string|int,string> $options value => label */
function f_select(string $name, string $label, $value, array $options, bool $blank = true): string
{
    $id = 'f_' . $name;
    $h = '<div class="field"><label for="' . e($id) . '">' . e($label) . '</label><select id="' . e($id) . '" name="' . e($name) . '">';
    if ($blank) {
        $h .= '<option value="">—</option>';
    }
    foreach ($options as $v => $l) {
        $h .= '<option value="' . e($v) . '"' . ((string) $v === (string) $value ? ' selected' : '') . '>' . e($l) . '</option>';
    }
    return $h . '</select></div>';
}

function f_check(string $name, string $label, bool $checked, ?string $help = null): string
{
    return '<div class="check"><input type="checkbox" id="f_' . e($name) . '" name="' . e($name) . '" value="1"' . ($checked ? ' checked' : '') . '>'
        . '<label for="f_' . e($name) . '">' . e($label) . '</label>' . ($help ? '<small>' . e($help) . '</small>' : '') . '</div>';
}

function post_str(string $k, int $max = 255): ?string
{
    return clean_str(is_string($_POST[$k] ?? null) ? $_POST[$k] : null, $max);
}

function post_int(string $k): ?int
{
    $v = $_POST[$k] ?? '';
    return (is_string($v) && ctype_digit($v)) ? (int) $v : null;
}

function fmt_dt(?string $utc, string $fmt = 'M j, Y g:i A'): string
{
    if (!$utc) {
        return '—';
    }
    return (new DateTimeImmutable($utc . ' UTC'))->setTimezone(new DateTimeZone('America/Chicago'))->format($fmt . ' T');
}

function status_pill(string $s): string
{
    return '<span class="pill pill--' . e($s) . '">' . e(str_replace('_', ' ', $s)) . '</span>';
}

function options_from(string $sql): array
{
    $o = [];
    foreach (Db::all($sql) as $r) {
        $o[$r['id']] = $r['label'];
    }
    return $o;
}
