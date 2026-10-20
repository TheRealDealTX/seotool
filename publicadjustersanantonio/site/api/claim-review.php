<?php
/**
 * POST endpoint for every Free Claim Review form on the site.
 * Returns JSON for fetch() requests and an HTML page for no-JavaScript submissions.
 */

declare(strict_types=1);

require_once dirname(__DIR__) . '/includes/bootstrap.php';
require_once dirname(__DIR__) . '/includes/form.php';

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
$success = 'Thank you! Your Free Claim Review request has been received. Our team will contact you.';

function respond(bool $ok, string $message, array $errors = [], int $status = 200): void
{
    global $wantsJson;
    http_response_code($status);
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message, 'errors' => $errors, 'token' => form_token()]);
        exit;
    }
    $page = [
        'path' => '/free-claim-review/', 'title' => $ok ? 'Request Received' : 'Please Check Your Request',
        'description' => '', 'noindex' => true, '_type' => 'page', 'template' => 'form-result',
        'hide_hero_cta' => true, 'hero_compact' => true,
    ];
    render_layout($page, function (array $page) use ($ok, $message, $errors) {
        component('page-hero', ['page' => $page]);
        echo '<section class="section"><div class="container narrow"><div class="notice ' . ($ok ? 'notice-success' : 'notice-error') . '"><p><strong>' . e($message) . '</strong></p>';
        if ($errors) {
            echo '<ul>';
            foreach ($errors as $er) {
                echo '<li>' . e($er) . '</li>';
            }
            echo '</ul>';
        }
        echo '</div><p><a class="btn btn-gold" href="' . ($ok ? '/' : '/free-claim-review/') . '">' . ($ok ? 'Return to the homepage' : 'Go back to the form') . '</a> <a class="btn btn-ghost" href="' . e(tel_link()) . '">Call ' . e(cfg('phone_short')) . '</a></p></div></section>';
    });
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    header('Allow: POST');
    respond(false, 'Please use the Free Claim Review form to send a request.', [], 405);
}

// Same-origin check (blocks cross-site form posts from other domains).
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '') {
    $o = parse_url($origin);
    $originHost = ($o['host'] ?? '') . (isset($o['port']) ? ':' . $o['port'] : '');
    $reqHost = preg_replace('/:(80|443)$/', '', (string) ($_SERVER['HTTP_HOST'] ?? ''));
    if ($originHost !== '' && strcasecmp($originHost, $reqHost) !== 0) {
        respond(false, 'Your request could not be verified. Please reload the page and try again.', [], 403);
    }
}

// Request too large for PHP (post_max_size exceeded): $_POST is empty.
if (empty($_POST) && (int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
    respond(false, 'Your attachments are too large. Please send fewer or smaller files.', [], 413);
}

// Honeypot: pretend success to bots, send nothing.
if (!empty($_POST['website'])) {
    log_line('form', 'Honeypot triggered.');
    respond(true, $success);
}

$tokenErr = verify_form_token((string) ($_POST['csrf_token'] ?? ''));
if ($tokenErr === 'too_fast') {
    respond(false, 'That was very fast! Please wait a few seconds and submit again.', [], 429);
}
if ($tokenErr !== '') {
    respond(false, 'Your session expired. Please reload the page and submit the form again.', [], 400);
}

if (!rate_limit_ok('claim', (int) cfg('rate_limit_max'), (int) cfg('rate_limit_window'))) {
    respond(false, 'Too many requests from this connection. Please call ' . cfg('phone_short') . ' or try again later.', [], 429);
}

[$data, $errors] = validate_claim_form($_POST);
if ($errors) {
    respond(false, 'Please correct the highlighted fields.', $errors, 422);
}

[$files, $fileErr] = validate_uploads();
if ($fileErr) {
    respond(false, $fileErr, ['attachments' => $fileErr], 422);
}

if (!send_claim_email($data, $files)) {
    respond(false, 'Sorry, we could not send your request right now. Please call ' . cfg('phone_display') . ' or email ' . cfg('public_email') . ' so we can help you directly.', [], 502);
}

respond(true, $success);
