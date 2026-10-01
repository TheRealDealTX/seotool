<?php
declare(strict_types=1);

/** Pages that host the estimate form; used to validate the return path. */
const FORM_PAGES = ['/', '/contact/', '/roofing-project-planner/'];

const RATE_LIMIT_MAX    = 5;    // submissions…
const RATE_LIMIT_WINDOW = 3600; // …per hour per visitor
const MIN_FORM_SECONDS  = 3;    // faster than this is almost certainly a bot

/**
 * Validate a submission. Returns [cleanData, errors] where errors maps a
 * field name to a human-readable message.
 */
function validate_estimate(array $in): array
{
    $d = [
        'name'     => clean_line($in['name'] ?? '', 100),
        'phone'    => clean_line($in['phone'] ?? '', 40),
        'email'    => clean_line($in['email'] ?? '', 254),
        'location' => clean_line($in['location'] ?? '', 200),
        'service'  => clean_line($in['service'] ?? '', 40),
        'message'  => clean_text($in['message'] ?? '', 4000),
        'consent'  => !empty($in['consent']),
    ];
    $errors = [];

    if (mb_strlen($d['name']) < 2) {
        $errors['name'] = 'Please enter your name.';
    }

    $digits = preg_replace('/\D/', '', $d['phone']);
    if ($d['phone'] === '') {
        $errors['phone'] = 'Please enter a phone number so we can reach you.';
    } elseif (!preg_match('/^[0-9+().\-\s]+(\s*(x|ext\.?)\s*\d{1,6})?$/i', $d['phone']) || strlen((string) $digits) < 10 || strlen((string) $digits) > 15) {
        $errors['phone'] = 'Please enter a valid phone number, including area code.';
    }

    if ($d['email'] !== '' && !filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'That email address doesn\'t look right. Check it, or leave it blank.';
    }

    if (mb_strlen($d['location']) < 5) {
        $errors['location'] = 'Please enter the property address or ZIP code.';
    }

    if (!array_key_exists($d['service'], service_options())) {
        $errors['service'] = 'Please choose the service you need (or "Not sure / other").';
    }

    if (!$d['consent']) {
        $errors['consent'] = 'Please confirm we may contact you about this request.';
    }

    return [$d, $errors];
}

function wants_json(): bool
{
    return str_contains((string) ($_SERVER['HTTP_ACCEPT'] ?? ''), 'application/json');
}

function safe_return_path(mixed $path): string
{
    return is_string($path) && in_array($path, FORM_PAGES, true) ? $path : '/contact/';
}

/** Handle POST /submit-estimate/ */
function handle_estimate_submission(): void
{
    ensure_session();
    $return = safe_return_path($_POST['return_to'] ?? '');
    $json   = wants_json();

    $respond = function (bool $ok, string $message, array $errors = [], int $status = 200) use ($json, $return): void {
        if ($ok) {
            $_SESSION['estimate_sent'] = true;
            unset($_SESSION['form_old'], $_SESSION['form_errors'], $_SESSION['form_message']);
        } else {
            $_SESSION['form_errors']  = $errors;
            $_SESSION['form_message'] = $message;
            $_SESSION['form_old']     = array_intersect_key($_POST, array_flip(['name', 'phone', 'email', 'location', 'service', 'message', 'consent']));
        }
        if ($json) {
            if (!$ok) {
                // JS shows the errors inline; don't replay them on the next page view.
                unset($_SESSION['form_old'], $_SESSION['form_errors'], $_SESSION['form_message']);
            }
            http_response_code($status);
            header('Content-Type: application/json; charset=utf-8');
            header('Cache-Control: no-store');
            echo json_encode([
                'ok'       => $ok,
                'message'  => $message,
                'errors'   => (object) $errors,
                'redirect' => $ok ? '/thank-you/' : null,
            ], JSON_UNESCAPED_SLASHES);
            return;
        }
        header('Location: ' . ($ok ? '/thank-you/' : $return . '#estimate-form'), true, 303);
    };

    $callUs = 'Please call us at ' . phone_display() . '.';

    if (!csrf_valid($_POST['csrf'] ?? null)) {
        $respond(false, 'Your session expired before the form was sent. Please review the form and submit it again, or ' . lcfirst($callUs), [], 400);
        return;
    }

    // Honeypot: real visitors never see or fill this field. Quietly discard.
    if (trim((string) ($_POST['website'] ?? '')) !== '') {
        app_log('spam', 'Honeypot submission discarded.');
        $respond(true, 'Thank you.');
        return;
    }

    $age = form_age($_POST['ts'] ?? null);
    if ($age === null || $age < MIN_FORM_SECONDS) {
        $respond(false, 'That was very fast. Please check your details and press Send again.', [], 400);
        return;
    }

    [$data, $errors] = validate_estimate($_POST);
    if ($errors) {
        $respond(false, 'Please correct the highlighted fields and try again.', $errors, 422);
        return;
    }

    if (!rate_limit_allow('estimate', RATE_LIMIT_MAX, RATE_LIMIT_WINDOW)) {
        $respond(false, 'We have received several requests from you in a short time. ' . $callUs, [], 429);
        return;
    }

    $data['source'] = abs_url($return);
    if (!send_estimate_email($data)) {
        $respond(false, 'Sorry, your request could not be sent right now and was not delivered. ' . $callUs, [], 503);
        return;
    }

    // New token after a successful submission prevents accidental resubmits.
    $_SESSION['csrf'] = bin2hex(random_bytes(32));
    $respond(true, 'Thank you. Your request was sent.');
}

/** Read and clear flash state for a form render. */
function form_flash(): array
{
    ensure_session();
    $flash = [
        'errors'  => $_SESSION['form_errors'] ?? [],
        'message' => $_SESSION['form_message'] ?? '',
        'old'     => $_SESSION['form_old'] ?? [],
    ];
    unset($_SESSION['form_errors'], $_SESSION['form_message'], $_SESSION['form_old']);
    return $flash;
}
