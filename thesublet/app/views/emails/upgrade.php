<?php defined('APP') || exit; ?>
<p>Hi <?= e($l['contact_name'] ?: 'there') ?>,</p>
<p>You asked to add photos to <strong>“<?= e($l['title']) ?>”</strong>. Photo uploads, editing and renewals come with a verified listing on The Sublet (<?= e(price_label()) ?> one-time), which also shows your contact details and adds a Verified host badge.</p>
<?= email_button(upgrade_link($l), 'Upgrade & add photos') ?>
<p>After paying you’ll get a sign-in link to your dashboard, where you can upload photos.</p>
