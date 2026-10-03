<?php
/**
 * Lead forms: rendering, CSRF tokens, spam protection, validation and
 * delivery. The recipient address and SMTP settings are read from the
 * private mail configuration on the server only — they are never sent to
 * the browser.
 */
defined('TR_ROOT') || exit;

/* ---------- Private configuration ---------- */

/**
 * Private mail config, searched in this order:
 *  1. path in the TR_PRIVATE_CONFIG environment variable
 *  2. ../templeroofs-private/mail-config.php (outside public_html — recommended)
 *  3. includes/private/mail-config.php (inside the site, blocked from the web)
 */
function private_config(): array
{
    static $c = null;
    if ($c !== null) {
        return $c;
    }
    $candidates = array_filter([
        getenv('TR_PRIVATE_CONFIG') ?: ($_SERVER['TR_PRIVATE_CONFIG'] ?? null),
        dirname(TR_ROOT) . '/templeroofs-private/mail-config.php',
        TR_INC . '/private/mail-config.php',
    ]);
    foreach ($candidates as $file) {
        if (@is_file($file) && @is_readable($file)) {
            $data = require $file;
            if (is_array($data)) {
                return $c = $data;
            }
        }
    }
    return $c = [];
}

/** Secret used to sign form tokens and hash IPs. Generated on first use if not configured. */
function app_secret(): string
{
    $s = (string) (private_config()['app_secret'] ?? '');
    if (strlen($s) >= 32) {
        return $s;
    }
    $file = TR_STORAGE . '/secret.php';
    if (is_file($file)) {
        $s = (string) require $file;
        if (strlen($s) >= 32) {
            return $s;
        }
    }
    $s = bin2hex(random_bytes(32));
    storage_write($file, "<?php\nreturn '" . $s . "';\n");
    return $s;
}

/* ---------- CSRF / timing token ---------- */

/** Stateless signed token: issue-time.nonce.signature */
function form_token(): string
{
    $payload = time() . '.' . bin2hex(random_bytes(8));
    return $payload . '.' . hash_hmac('sha256', $payload, app_secret());
}

/** Returns '' if valid, or an error code. */
function check_form_token(string $token): string
{
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return 'token';
    }
    [$ts, $nonce, $sig] = $parts;
    if (!ctype_digit($ts) || !hash_equals(hash_hmac('sha256', $ts . '.' . $nonce, app_secret()), $sig)) {
        return 'token';
    }
    $age = time() - (int) $ts;
    if ($age < 3) {
        return 'too_fast';
    }
    if ($age > 6 * 3600) {
        return 'expired';
    }
    return '';
}

/* ---------- Flash data for no-JavaScript submissions ---------- */

function flash_session_start(): void
{
    if (session_status() === PHP_SESSION_NONE) {
        session_name('tr_flash');
        session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off', 'httponly' => true, 'samesite' => 'Lax']);
        @session_start();
    }
}

function take_flash(string $formId): array
{
    if (empty($_COOKIE['tr_flash'])) {
        return [];
    }
    flash_session_start();
    $f = $_SESSION['flash'][$formId] ?? [];
    unset($_SESSION['flash'][$formId]);
    return $f;
}

/* ---------- Rendering ---------- */

/**
 * Options: variant (full|compact|short), id, source (path), title, concern (preselect), button.
 */
function lead_form(array $o = []): void
{
    $variant = $o['variant'] ?? 'full';
    $id = preg_replace('/[^a-z0-9-]/', '', $o['id'] ?? $variant);
    $source = $o['source'] ?? (parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
    $flash = take_flash($id);
    $old = $flash['old'] ?? [];
    $errors = $flash['errors'] ?? [];
    $concern = $old['concern'] ?? ($o['concern'] ?? ($_GET['concern'] ?? 'inspection'));
    if (!isset(catalog('concerns')[$concern])) {
        $concern = 'inspection';
    }
    $v = fn ($k) => e($old[$k] ?? '');
    $err = function ($k) use ($errors, $id) {
        return isset($errors[$k]) ? '<p class="field__error" id="' . $id . '-' . $k . '-err">' . e($errors[$k]) . '</p>' : '<p class="field__error" id="' . $id . '-' . $k . '-err" hidden></p>';
    };
    $inv = fn ($k) => isset($errors[$k]) ? ' aria-invalid="true"' : '';
    $full = $variant === 'full';
    ?>
<form class="lead-form lead-form--<?= e($variant) ?>" id="lead-form-<?= e($id) ?>" action="/api/lead/" method="post" novalidate data-lead-form>
  <?php if (!empty($o['title'])): ?><p class="lead-form__title"><?= e($o['title']) ?></p><?php endif; ?>
  <?php if (!empty($o['subtitle'])): ?><p class="lead-form__sub"><?= e($o['subtitle']) ?></p><?php endif; ?>
  <div class="form-alert form-alert--error" role="alert" tabindex="-1" <?= isset($errors['_form']) ? '' : 'hidden' ?> data-form-alert><?= e($errors['_form'] ?? '') ?></div>
  <input type="hidden" name="token" value="<?= e(form_token()) ?>">
  <input type="hidden" name="source" value="<?= e($source) ?>">
  <input type="hidden" name="form_id" value="<?= e($id) ?>">
  <div class="hp-field" aria-hidden="true">
    <label for="<?= e($id) ?>-website">Leave this field empty</label>
    <input type="text" id="<?= e($id) ?>-website" name="website" tabindex="-1" autocomplete="off">
  </div>
  <div class="form-grid">
    <div class="field">
      <label for="<?= e($id) ?>-name">Full name <span class="req" aria-hidden="true">*</span></label>
      <input type="text" id="<?= e($id) ?>-name" name="name" required maxlength="100" autocomplete="name" value="<?= $v('name') ?>" aria-describedby="<?= e($id) ?>-name-err"<?= $inv('name') ?>>
      <?= $err('name') ?>
    </div>
    <div class="field">
      <label for="<?= e($id) ?>-phone">Phone number <span class="req" aria-hidden="true">*</span></label>
      <input type="tel" id="<?= e($id) ?>-phone" name="phone" required maxlength="30" autocomplete="tel" inputmode="tel" value="<?= $v('phone') ?>" aria-describedby="<?= e($id) ?>-phone-err"<?= $inv('phone') ?>>
      <?= $err('phone') ?>
    </div>
    <?php if ($variant !== 'compact'): ?>
    <div class="field">
      <label for="<?= e($id) ?>-email">Email address <span class="opt">(optional)</span></label>
      <input type="email" id="<?= e($id) ?>-email" name="email" maxlength="150" autocomplete="email" value="<?= $v('email') ?>" aria-describedby="<?= e($id) ?>-email-err"<?= $inv('email') ?>>
      <?= $err('email') ?>
    </div>
    <?php endif; ?>
    <div class="field">
      <label for="<?= e($id) ?>-address"><?= $variant === 'compact' ? 'Address or ZIP' : 'Property address or ZIP' ?> <span class="opt">(optional)</span></label>
      <input type="text" id="<?= e($id) ?>-address" name="address" maxlength="200" autocomplete="street-address" value="<?= $v('address') ?>" aria-describedby="<?= e($id) ?>-address-err"<?= $inv('address') ?>>
      <?= $err('address') ?>
    </div>
    <div class="field<?= $variant === 'short' ? ' field--wide' : '' ?>">
      <label for="<?= e($id) ?>-concern">Type of roofing concern</label>
      <select id="<?= e($id) ?>-concern" name="concern">
        <?php foreach (catalog('concerns') as $k => $label): ?>
        <option value="<?= e($k) ?>"<?= $k === $concern ? ' selected' : '' ?>><?= e($label) ?></option>
        <?php endforeach; ?>
      </select>
    </div>
    <?php if ($full): ?>
    <div class="field">
      <label for="<?= e($id) ?>-contact_method">Preferred contact method</label>
      <select id="<?= e($id) ?>-contact_method" name="contact_method">
        <?php foreach (['phone' => 'Phone call', 'text' => 'Text message', 'email' => 'Email'] as $k => $label): ?>
        <option value="<?= e($k) ?>"<?= ($old['contact_method'] ?? 'phone') === $k ? ' selected' : '' ?>><?= e($label) ?></option>
        <?php endforeach; ?>
      </select>
    </div>
    <div class="field field--wide">
      <label for="<?= e($id) ?>-preferred_time">Preferred inspection date or time <span class="opt">(optional)</span></label>
      <input type="text" id="<?= e($id) ?>-preferred_time" name="preferred_time" maxlength="120" placeholder="e.g. Weekday mornings, or Friday after 2 pm" value="<?= $v('preferred_time') ?>">
    </div>
    <?php endif; ?>
    <?php if ($variant !== 'compact'): ?>
    <div class="field field--wide">
      <label for="<?= e($id) ?>-details"><?= $full ? 'Additional details' : 'What is going on with your roof?' ?> <span class="opt">(optional)</span></label>
      <textarea id="<?= e($id) ?>-details" name="details" rows="<?= $full ? 5 : 3 ?>" maxlength="3000" aria-describedby="<?= e($id) ?>-details-err"<?= $inv('details') ?>><?= $v('details') ?></textarea>
      <?= $err('details') ?>
    </div>
    <?php endif; ?>
    <div class="field field--wide field--check">
      <input type="checkbox" id="<?= e($id) ?>-consent" name="consent" value="yes" required aria-describedby="<?= e($id) ?>-consent-err"<?= $inv('consent') ?><?= !empty($old['consent']) ? ' checked' : '' ?>>
      <label for="<?= e($id) ?>-consent">I agree that Temple Roofers may contact me about this request by my chosen method. See our <a href="/privacy-policy/">Privacy Policy</a>. <span class="req" aria-hidden="true">*</span></label>
      <?= $err('consent') ?>
    </div>
  </div>
  <button class="btn btn--gold btn--block lead-form__submit" type="submit" data-submit>
    <span data-submit-label><?= e($o['button'] ?? 'Request My Free Inspection') ?></span>
  </button>
  <p class="lead-form__note"><?= icon('lock') ?> Free and no obligation. We never sell your information. Prefer to call? <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_display')) ?></a></p>
</form>
<?php
}

/* ---------- Processing ---------- */

/** Strip control characters (incl. CR/LF, which prevents header injection). */
function clean_line(string $s, int $max): string
{
    $s = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $s) ?? '';
    return mb_substr(trim(preg_replace('/\s+/u', ' ', $s)), 0, $max);
}

function clean_text(string $s, int $max): string
{
    $s = str_replace(["\r\n", "\r"], "\n", $s);
    $s = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/u', '', $s) ?? '';
    return mb_substr(trim($s), 0, $max);
}

/** Validate submitted fields. Returns [clean data, errors]. */
function validate_lead(array $in): array
{
    $concerns = catalog('concerns');
    $d = [
        'name'           => clean_line((string) ($in['name'] ?? ''), 100),
        'phone'          => clean_line((string) ($in['phone'] ?? ''), 30),
        'email'          => clean_line((string) ($in['email'] ?? ''), 150),
        'address'        => clean_line((string) ($in['address'] ?? ''), 200),
        'concern'        => (string) ($in['concern'] ?? 'inspection'),
        'contact_method' => (string) ($in['contact_method'] ?? 'phone'),
        'preferred_time' => clean_line((string) ($in['preferred_time'] ?? ''), 120),
        'details'        => clean_text((string) ($in['details'] ?? ''), 3000),
        'consent'        => ($in['consent'] ?? '') === 'yes',
    ];
    $errors = [];
    if (mb_strlen($d['name']) < 2) {
        $errors['name'] = 'Please enter your name.';
    } elseif (preg_match('/https?:|www\.|[<>]/i', $d['name'])) {
        $errors['name'] = 'Please enter your name without links or symbols.';
    }
    $digits = preg_replace('/\D/', '', $d['phone']);
    if (strlen($digits) === 11 && $digits[0] === '1') {
        $digits = substr($digits, 1);
    }
    if (strlen($digits) !== 10) {
        $errors['phone'] = 'Please enter a 10-digit phone number, e.g. (254) 555-0123.';
    } else {
        $d['phone'] = sprintf('(%s) %s-%s', substr($digits, 0, 3), substr($digits, 3, 3), substr($digits, 6));
    }
    if ($d['email'] !== '' && !filter_var($d['email'], FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Please enter a valid email address, or leave it blank.';
    }
    if (!isset($concerns[$d['concern']])) {
        $d['concern'] = 'other';
    }
    if (!in_array($d['contact_method'], ['phone', 'text', 'email'], true)) {
        $d['contact_method'] = 'phone';
    }
    if ($d['contact_method'] === 'email' && $d['email'] === '' && !isset($errors['email'])) {
        $errors['email'] = 'Please add your email address so we can reply by email.';
    }
    if (preg_match_all('~https?://|www\.~i', $d['details']) > 2) {
        $errors['details'] = 'Please remove the links from your message.';
    }
    if (!$d['consent']) {
        $errors['consent'] = 'Please confirm we may contact you about this request.';
    }
    return [$d, $errors];
}

/** File-based rate limit keyed by a salted IP hash (no raw IPs stored). */
function rate_limited(): bool
{
    $max = (int) cfg('rate_limit_max', 5);
    $window = (int) cfg('rate_limit_window', 900);
    $key = hash_hmac('sha256', client_ip(), app_secret());
    $file = TR_STORAGE . '/ratelimit/' . substr($key, 0, 40) . '.json';
    $now = time();
    $hits = is_file($file) ? (json_decode((string) @file_get_contents($file), true) ?: []) : [];
    $hits = array_values(array_filter($hits, fn ($t) => is_int($t) && $t > $now - $window));
    if (count($hits) >= $max) {
        return true;
    }
    $hits[] = $now;
    storage_write($file, json_encode($hits));
    // Occasionally clean up old rate-limit files.
    if (random_int(1, 50) === 1) {
        foreach (glob(TR_STORAGE . '/ratelimit/*.json') ?: [] as $f) {
            if (@filemtime($f) < $now - $window) {
                @unlink($f);
            }
        }
    }
    return false;
}

function safe_source(string $s): string
{
    return preg_match('~^/[a-z0-9/_-]{0,150}$~i', $s) && !str_contains($s, '//') ? $s : '/';
}

/** Build the notification email (plain text + HTML). */
function lead_email(array $d, string $source): array
{
    $concerns = catalog('concerns');
    $when = tr_now()->format('l, F j, Y \a\t g:i A T');
    $rows = [
        'Name'                     => $d['name'],
        'Phone'                    => $d['phone'],
        'Email'                    => $d['email'] ?: '(not provided)',
        'Property address / ZIP'   => $d['address'] ?: '(not provided)',
        'Roofing concern'          => $concerns[$d['concern']] ?? $d['concern'],
        'Preferred contact method' => ['phone' => 'Phone call', 'text' => 'Text message', 'email' => 'Email'][$d['contact_method']],
        'Preferred date / time'    => $d['preferred_time'] ?: '(not provided)',
        'Submitted'                => $when,
        'Source page'              => abs_url($source),
    ];
    $text = "New lead from the Temple Roofers website\n\n";
    $html = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#0B1F3A">'
        . '<h2 style="margin:0 0 12px;color:#0B1F3A">New Temple Roofers Lead — Free Roof Inspection Request</h2>'
        . '<table cellpadding="8" cellspacing="0" style="border-collapse:collapse;border:1px solid #e2e8f0">';
    foreach ($rows as $label => $value) {
        $text .= str_pad($label . ':', 27) . $value . "\n";
        $html .= '<tr><th align="left" style="background:#F8F9FC;border:1px solid #e2e8f0;white-space:nowrap">' . e($label) . '</th>'
            . '<td style="border:1px solid #e2e8f0">' . e($value) . '</td></tr>';
    }
    $details = $d['details'] ?: '(none)';
    $text .= "\nRoofing request details:\n" . $details . "\n";
    $html .= '</table><h3 style="margin:18px 0 6px">Roofing request details</h3>'
        . '<p style="white-space:pre-wrap;background:#F8F9FC;padding:12px;border-radius:6px">' . e($details) . '</p>'
        . '<p style="color:#475569;font-size:13px">Reply to this email to answer the visitor directly when they provided an email address.</p></div>';
    return [$text, $html];
}

/** Send via PHPMailer: authenticated SMTP when configured, otherwise PHP mail(). */
function send_lead_email(array $d, string $source): array
{
    $pc = private_config();
    $to = (string) ($pc['recipient'] ?? '');
    if (!filter_var($to, FILTER_VALIDATE_EMAIL)) {
        return [false, 'Recipient address is not configured.'];
    }
    require_once TR_ROOT . '/vendor/phpmailer/Exception.php';
    require_once TR_ROOT . '/vendor/phpmailer/PHPMailer.php';
    require_once TR_ROOT . '/vendor/phpmailer/SMTP.php';

    [$text, $html] = lead_email($d, $source);
    $mail = new PHPMailer\PHPMailer\PHPMailer(true);
    try {
        $mail->CharSet = 'UTF-8';
        $smtp = $pc['smtp'] ?? [];
        if (!empty($smtp['host']) && !empty($smtp['username']) && !empty($smtp['password'])) {
            $mail->isSMTP();
            $mail->Host = $smtp['host'];
            $mail->Port = (int) ($smtp['port'] ?? 465);
            $mail->SMTPAuth = true;
            $mail->Username = $smtp['username'];
            $mail->Password = $smtp['password'];
            $secure = $smtp['secure'] ?? 'ssl';
            if ($secure === 'none') {          // local testing only
                $mail->SMTPSecure = '';
                $mail->SMTPAutoTLS = false;
            } else {
                $mail->SMTPSecure = $secure === 'tls'
                    ? PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS
                    : PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS;
            }
            $mail->Timeout = 15;
            $from = $pc['from_email'] ?? $smtp['username'];
        } else {
            $mail->isMail();
            $from = $pc['from_email'] ?? ('no-reply@' . parse_url(cfg('base_url'), PHP_URL_HOST));
        }
        $mail->setFrom($from, $pc['from_name'] ?? 'Temple Roofers Website');
        $mail->addAddress($to);
        if ($d['email'] !== '' && PHPMailer\PHPMailer\PHPMailer::validateAddress($d['email'])) {
            $mail->addReplyTo($d['email'], $d['name']);
        }
        $mail->Subject = 'New Temple Roofers Lead — Free Roof Inspection Request';
        $mail->isHTML(true);
        $mail->Body = $html;
        $mail->AltBody = $text;
        $mail->send();
        return [true, ''];
    } catch (Throwable $ex) {
        // Log the transport error only — never the visitor's details or credentials.
        return [false, preg_replace('/[\r\n]+/', ' ', $mail->ErrorInfo ?: $ex->getMessage())];
    }
}

/**
 * If delivery fails, keep the lead in private storage so it is not lost.
 * Stored outside public_html when the private folder exists.
 */
function store_undelivered_lead(array $d, string $source): void
{
    $dir = is_dir(dirname(TR_ROOT) . '/templeroofs-private') && is_writable(dirname(TR_ROOT) . '/templeroofs-private')
        ? dirname(TR_ROOT) . '/templeroofs-private/undelivered-leads'
        : TR_STORAGE . '/undelivered-leads';
    $file = $dir . '/' . tr_now()->format('Y-m-d_His') . '-' . bin2hex(random_bytes(3)) . '.json';
    storage_write($file, json_encode($d + ['source' => $source, 'submitted' => tr_now()->format('c')], JSON_PRETTY_PRINT));
}

function log_event(string $msg): void
{
    $line = tr_now()->format('c') . ' ' . preg_replace('/[\r\n]+/', ' ', $msg) . "\n";
    @file_put_contents(TR_STORAGE . '/logs/forms.log', $line, FILE_APPEND | LOCK_EX);
}

/** POST /api/lead/ */
function handle_lead_post(): void
{
    $wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
    $source = safe_source((string) ($_POST['source'] ?? '/'));
    $formId = preg_replace('/[^a-z0-9-]/', '', (string) ($_POST['form_id'] ?? 'full')) ?: 'full';

    $fail = function (array $errors, int $status, array $old = []) use ($wantsJson, $source, $formId) {
        if ($wantsJson) {
            json_out(['ok' => false, 'errors' => $errors], $status);
        }
        flash_session_start();
        $_SESSION['flash'][$formId] = ['errors' => $errors, 'old' => $old];
        header('Location: ' . $source . '#lead-form-' . $formId, true, 303);
        exit;
    };

    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        header('Allow: POST');
        json_out(['ok' => false, 'errors' => ['_form' => 'Method not allowed.']], 405);
    }
    // Same-origin check (CSRF defence in depth alongside the signed token).
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    $originHost = (string) parse_url($origin, PHP_URL_HOST) . (parse_url($origin, PHP_URL_PORT) ? ':' . parse_url($origin, PHP_URL_PORT) : '');
    if ($origin !== '' && strcasecmp($originHost, (string) ($_SERVER['HTTP_HOST'] ?? '')) !== 0) {
        $fail(['_form' => 'Your request could not be verified. Please refresh the page and try again.'], 403);
    }
    // Honeypot: bots fill hidden fields. Respond like a success without sending.
    if (trim((string) ($_POST['website'] ?? '')) !== '') {
        log_event('honeypot rejected');
        $wantsJson ? json_out(['ok' => true, 'redirect' => '/thank-you/']) : header('Location: /thank-you/', true, 303);
        exit;
    }
    $tokenErr = check_form_token((string) ($_POST['token'] ?? ''));
    [$data, $errors] = validate_lead($_POST);
    $old = $data;
    if ($tokenErr === 'too_fast') {
        $fail(['_form' => 'That was quicker than we expected. Please wait a few seconds and press submit again.'], 429, $old);
    } elseif ($tokenErr !== '') {
        $fail(['_form' => 'This form has expired. Please refresh the page and submit it again.'], 403, $old);
    }
    if ($errors) {
        $errors['_form'] = 'Please correct the highlighted fields and try again.';
        $fail($errors, 422, $old);
    }
    if (rate_limited()) {
        $fail(['_form' => 'We have received several requests from your connection in a short time. Please call us at ' . cfg('phone_display') . ' or try again in a few minutes.'], 429, $old);
    }

    [$sent, $error] = send_lead_email($data, $source);
    if (!$sent) {
        store_undelivered_lead($data, $source);
        log_event('delivery failed: ' . $error);
        $fail(['_form' => 'Sorry — we could not send your request just now. Your details were saved for our team, but please call us at ' . cfg('phone_display') . ' so we can help right away.'], 500, $old);
    }
    log_event('lead delivered (' . $data['concern'] . ', ' . $source . ')');
    if ($wantsJson) {
        json_out(['ok' => true, 'redirect' => '/thank-you/']);
    }
    header('Location: /thank-you/', true, 303);
    exit;
}
