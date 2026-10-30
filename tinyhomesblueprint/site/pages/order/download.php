<?php
// GET /order/download/?o=THB-XXXXXXXX&t=<token> - stream a purchased plan set.
require_once __DIR__ . '/../../inc/store.php';
$o = find_order((string)($_GET['o'] ?? ''));
$t = (string)($_GET['t'] ?? '');
$problem = null;
if (!$o || $t === '' || !hash_equals($o['token'], $t)) $problem = 'This download link is not valid.';
elseif (!empty($o['revoked'])) $problem = 'This order was refunded, so its download link has been turned off.';
elseif (time() > $o['expires']) $problem = 'This download link has expired.';
elseif ($o['downloads'] >= DOWNLOAD_MAX) $problem = 'This link has reached its download limit.';
elseif (!is_file(plan_file($o['plan']))) $problem = 'The plan files are being updated right now.';

if ($problem === null) {
    $o['downloads']++;
    $o['last_download'] = time();
    save_order($o);
    $file = plan_file($o['plan']);
    $name = preg_replace('/[^A-Za-z0-9-]/', '-', $PLANS[$o['plan']]['name']) . '-Complete-Plan-Set.zip';
    while (ob_get_level()) ob_end_clean();
    header('Content-Type: application/zip');
    header('Content-Length: ' . filesize($file));
    header('Content-Disposition: attachment; filename="' . $name . '"');
    header('Cache-Control: private, no-store');
    header('X-Robots-Tag: noindex');
    $fp = fopen($file, 'rb');
    while (!feof($fp)) { echo fread($fp, 1 << 16); flush(); }
    fclose($fp);
    exit;
}
// Unknown order or wrong token: 404, so the response does not confirm an order exists.
http_response_code(!$o || $t === '' || !hash_equals($o['token'], $t) ? 404 : 410);
page_start(['robots' => 'noindex,nofollow']);
?>
<section class="section"><div class="narrow panel">
  <h1 style="font-size:2rem">Download unavailable</h1>
  <p><?= e($problem) ?></p>
  <p>Get a fresh link at <a href="/order/lookup/">Find my plan download</a> with the email you used at checkout, or contact us at <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a> / <a href="tel:<?= SITE_TEL ?>"><?= SITE_PHONE ?></a> and include your order number.</p>
</div></section>
<?php page_end(); ?>
