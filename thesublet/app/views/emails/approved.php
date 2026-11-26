<?php defined('APP') || exit;
/** @var array $l  Approved free listing (sent when an admin approves & publishes it). */
$url = base_url(listing_url($l));
$dates = $l['available_from'] ? fmt_date($l['available_from']) . ($l['available_to'] ? ' – ' . fmt_date($l['available_to']) : ' onward') : 'Flexible';
$where = ($l['neighborhood'] ? $l['neighborhood'] . ', ' : '') . $l['city'] . ', ' . $l['state'];
$row = fn($k, $v) => '<tr><td style="padding:6px 0;color:#6b7b73;font-size:13px;width:110px;vertical-align:top">' . $k . '</td><td style="padding:6px 0;font-size:14px;color:#1d2a24">' . $v . '</td></tr>';
?>
<p>Hi <?= e($l['contact_name'] ?: 'there') ?>,</p>
<p>Good news: we reviewed and approved your listing, and it’s now <strong>live on The Sublet</strong>.</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #dfe9e3;border-radius:10px;margin:18px 0"><tr><td style="padding:16px 18px">
  <p style="margin:0 0 8px;font-size:16px;font-weight:bold;color:#1d2a24"><?= e($l['title']) ?></p>
  <table role="presentation" cellpadding="0" cellspacing="0">
    <?= $row('Location', e($where)) ?>
    <?= $row('Rent', e(money($l['rent'])) . '/month') ?>
    <?= $row('Available', e($dates)) ?>
    <?= $row('Listed until', e(fmt_date($l['expires_at']))) ?>
  </table>
</td></tr></table>

<?= email_button($url, 'View your live listing') ?>
<p style="font-size:13px;color:#6b7b73;margin-top:-8px">Or copy this link to share it: <a href="<?= e($url) ?>" style="color:#2f6f4f;word-break:break-all"><?= e($url) ?></a></p>

<p><strong>How renters reach you:</strong> they use the contact form on your listing. Their messages are forwarded to this inbox, and you can reply directly. Your email address stays private.</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f3f8f5;border:1px solid #cfe3d8;border-radius:10px;margin:24px 0 8px"><tr><td style="padding:20px 20px 6px">
  <p style="margin:0 0 4px;font-size:12px;font-weight:bold;letter-spacing:.06em;text-transform:uppercase;color:#e46f4c">Optional upgrade</p>
  <p style="margin:0 0 10px;font-size:18px;font-weight:bold;color:#1d2a24">Get featured for <?= e(price_label()) ?> (one-time)</p>
  <table role="presentation" cellpadding="0" cellspacing="0" style="font-size:14px;line-height:1.5">
    <tr><td style="padding:3px 8px 3px 0;vertical-align:top;color:#2f6f4f">✔</td><td style="padding:3px 0"><strong>★ Featured badge and top placement</strong>: shown above free listings in search results and on city pages</td></tr>
    <tr><td style="padding:3px 8px 3px 0;vertical-align:top;color:#2f6f4f">✔</td><td style="padding:3px 0"><strong>Your contact info shown publicly</strong>, so renters can call or email you directly</td></tr>
    <tr><td style="padding:3px 8px 3px 0;vertical-align:top;color:#2f6f4f">✔</td><td style="padding:3px 0"><strong>Verified host badge</strong> on your listing</td></tr>
    <tr><td style="padding:3px 8px 3px 0;vertical-align:top;color:#2f6f4f">✔</td><td style="padding:3px 0"><strong>Your own dashboard</strong> to edit, renew, add photos and mark it rented</td></tr>
  </table>
  <?= email_button(upgrade_link($l), 'Feature my listing for ' . price_label()) ?>
  <p style="margin:-10px 0 14px;font-size:12px;color:#6b7b73">Same listing and link, upgraded right after checkout. You’ll get a sign-in link by email; once you open it, your contact details go live.</p>
</td></tr></table>

<p style="font-size:14px">Need to change something or take the listing down? Just reply to this email.</p>
<p style="font-size:14px">Thanks for listing on The Sublet!<br>The Sublet team</p>
