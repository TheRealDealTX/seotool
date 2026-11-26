<?php
// Email templates. Each returns [subject, plain text, html]; mhr_mail() sends
// both parts as multipart/alternative from the site mailbox.

// Sent to the submitter when an admin approves a free submission.
function mhr_email_approved($name, $title, $slug) {
    $live = abs_url('/properties/' . $slug . '/');
    $claim = abs_url('/claim/' . $slug . '/');
    $price = mhr_price_label();
    $site = cfg('name');
    $hi = $name !== '' ? $name : 'there';
    $subject = 'Your listing is live: ' . $title;

    $text = "Hi $hi,\n\n"
        . "Good news: your property \"$title\" has been approved and is now live on $site:\n$live\n\n"
        . "Right now your listing is on our free plan, so your phone, email and website are hidden from visitors.\n\n"
        . "UPGRADE FOR $price (ONE-TIME) TO GET MORE RENTERS TO CONTACT YOU\n"
        . "- Featured listing: shown first in search results and in the Featured section\n"
        . "- Your contact info made public: phone, email and website on your listing\n"
        . "- Verified owner badge so military families know it's legitimate\n"
        . "- Owner dashboard to update details and photos any time\n\n"
        . "Upgrade here: $claim\n\n"
        . "Questions? Just reply to this email.\n\n"
        . "Thanks for helping military families find a home,\nThe $site team\n\n"
        . "--\n$site · " . abs_url('/') . " · " . cfg('phone') . "\nYou're receiving this because you submitted a property at " . parse_url(abs_url('/'), PHP_URL_HOST) . ".";

    $E = fn($s) => htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $check = fn($strong, $rest) => '<tr><td valign="top" style="padding:3px 8px 3px 0;color:#1f9d6b;font-weight:bold;">&#10003;</td><td style="padding:3px 0;"><strong>' . $E($strong) . '</strong>' . $E($rest) . '</td></tr>';
    $btn = fn($href, $label, $bg, $fg) => '<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background:' . $bg . ';border-radius:8px;"><a href="' . $E($href) . '" style="display:inline-block;padding:12px 22px;color:' . $fg . ';font-weight:bold;text-decoration:none;font-size:15px;">' . $E($label) . '</a></td></tr></table>';
    $logo = abs_url('/assets/img/email-logo.png');
    $host = parse_url(abs_url('/'), PHP_URL_HOST);

    $html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' . $E($subject) . '</title></head>'
        . '<body style="margin:0;padding:0;background:#f6f8fb;font-family:Arial,Helvetica,sans-serif;color:#0f1b2d;">'
        . '<div style="display:none;max-height:0;overflow:hidden;">' . $E($title) . ' is now published on ' . $E($site) . '.</div>'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f8fb;padding:24px 12px;"><tr><td align="center">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border:1px solid #dfe5ee;border-radius:12px;">'
        . '<tr><td style="background:#0b1f3a;padding:20px 28px;border-radius:12px 12px 0 0;"><img src="' . $E($logo) . '" width="130" height="61" alt="' . $E($site) . '" style="display:block;border:0;"></td></tr>'
        . '<tr><td style="padding:28px;">'
        . '<p style="margin:0 0 16px;font-size:16px;">Hi ' . $E($hi) . ',</p>'
        . '<p style="margin:0 0 16px;font-size:16px;line-height:1.5;">Good news: your property <strong>' . $E($title) . '</strong> has been approved and is now live on ' . $E($site) . '.</p>'
        . '<div style="margin:0 0 12px;">' . $btn($live, 'View your live listing', '#1d5bd8', '#ffffff') . '</div>'
        . '<p style="margin:0 0 24px;font-size:13px;color:#56637a;word-break:break-all;"><a href="' . $E($live) . '" style="color:#56637a;">' . $E($live) . '</a></p>'
        . '<p style="margin:0 0 16px;font-size:15px;line-height:1.5;">Right now your listing is on our <strong>free plan</strong>, so your phone, email and website are hidden from visitors.</p>'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#fff8ec;border:1px solid #f2d39b;border-radius:10px;"><tr><td style="padding:20px 22px;">'
        . '<p style="margin:0 0 4px;font-size:13px;font-weight:bold;letter-spacing:.06em;text-transform:uppercase;color:#8a5a00;">Upgrade for ' . $E($price) . ', one-time</p>'
        . '<p style="margin:0 0 12px;font-size:18px;font-weight:bold;">Get more renters to contact you</p>'
        . '<table role="presentation" cellpadding="0" cellspacing="0" style="font-size:15px;line-height:1.5;">'
        . $check('Featured listing', ': shown first in search results and in the Featured section')
        . $check('Your contact info made public', ': phone, email and website on your listing')
        . $check('Verified owner badge', " so military families know it's legitimate")
        . $check('Owner dashboard', ' to update details and photos any time')
        . '</table><div style="margin:16px 0 0;">' . $btn($claim, 'Upgrade my listing for ' . $price, '#f2a93b', '#0b1f3a') . '</div>'
        . '</td></tr></table>'
        . '<p style="margin:24px 0 0;font-size:15px;line-height:1.5;">Questions? Just reply to this email.</p>'
        . '<p style="margin:16px 0 0;font-size:15px;line-height:1.5;">Thanks for helping military families find a home,<br>The ' . $E($site) . ' team</p>'
        . '</td></tr>'
        . '<tr><td style="padding:16px 28px;border-top:1px solid #dfe5ee;font-size:12px;line-height:1.5;color:#56637a;">'
        . $E($site) . ' &middot; <a href="' . $E(abs_url('/')) . '" style="color:#56637a;">' . $E($host) . '</a> &middot; ' . $E(cfg('phone')) . '<br>'
        . "You're receiving this because you submitted a property at " . $E($host) . '.</td></tr>'
        . '</table></td></tr></table></body></html>';

    return [$subject, $text, $html];
}
