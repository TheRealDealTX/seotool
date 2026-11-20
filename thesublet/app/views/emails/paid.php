<?php defined('APP') || exit; ?>
<p>Hi <?= e($o['name'] ?: 'there') ?>,</p>
<p>Thanks for your payment — <strong>“<?= e($l['title']) ?>”</strong> is now live on The Sublet with a Verified host badge.</p>
<?php if (!$o['email_verified_at']): ?>
<p><strong>One more step:</strong> confirm your email to switch on your public contact details and open your host dashboard.</p>
<?= email_button($link, 'Verify email & open dashboard') ?>
<?php else: ?>
<?= email_button($link, 'Open my dashboard') ?>
<?php endif; ?>
<p>From your dashboard you can edit the listing, upload photos, renew it, or mark it rented. This link works once and expires in 60 minutes — you can always get a new one at <a href="<?= e(base_url('/login/')) ?>"><?= e(base_url('/login/')) ?></a>.</p>
<p>Listing: <a href="<?= e(base_url(listing_url($l))) ?>"><?= e(base_url(listing_url($l))) ?></a></p>
