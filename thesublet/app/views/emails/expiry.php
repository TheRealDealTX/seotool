<?php defined('APP') || exit; ?>
<p>Hi <?= e($l['contact_name'] ?: 'there') ?>,</p>
<p>Your listing <strong>“<?= e($l['title']) ?>”</strong> on The Sublet expires on <strong><?= e(fmt_date($l['expires_at'])) ?></strong>.</p>
<p>Still available? Renew it with one click:</p>
<?= email_button(renew_link($l), 'Renew my listing') ?>
<p>Already rented? You don’t need to do anything — it will come down automatically.</p>
<?php if ($l['tier'] !== 'paid'): ?><p>Want your contact details shown and a Verified host badge? <a href="<?= e(upgrade_link($l)) ?>">Upgrade for <?= e(price_label()) ?></a>.</p><?php endif; ?>
