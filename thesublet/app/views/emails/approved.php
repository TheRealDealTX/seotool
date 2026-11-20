<?php defined('APP') || exit; ?>
<p>Hi <?= e($l['contact_name'] ?: 'there') ?>,</p>
<p>Good news — your listing <strong>“<?= e($l['title']) ?>”</strong> is now live on The Sublet:</p>
<?= email_button(base_url(listing_url($l)), 'View my listing') ?>
<p>Renters will contact you through our relay; their messages arrive in this inbox and you can reply directly. Your listing runs until <?= e(fmt_date($l['expires_at'])) ?> and we’ll remind you before it expires.</p>
<p><strong>Get more replies:</strong> upgrade to a verified listing for <?= e(price_label()) ?> to show your contact details, add a Verified host badge and photos, and manage everything from a dashboard. <a href="<?= e(upgrade_link($l)) ?>">Upgrade now</a>.</p>
