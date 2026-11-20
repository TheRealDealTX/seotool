<?php defined('APP') || exit; ?>
<p>Hi <?= e($l['contact_name'] ?: 'there') ?>,</p>
<p>Thanks for listing <strong>“<?= e($l['title']) ?>”</strong> on The Sublet. Our team reviews free listings by hand, usually within one to two days, and we’ll email you as soon as it’s live.</p>
<p>Want it published right now with your contact details shown and a Verified host badge?</p>
<?= email_button(upgrade_link($l), 'Upgrade for ' . price_label()) ?>
<p>— The Sublet</p>
