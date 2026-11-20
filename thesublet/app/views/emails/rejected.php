<?php defined('APP') || exit; ?>
<p>Hi <?= e($l['contact_name'] ?: 'there') ?>,</p>
<p>Thanks for submitting <strong>“<?= e($l['title']) ?>”</strong> to The Sublet. Unfortunately we couldn’t publish it.</p>
<?php if (!empty($l['reject_reason'])): ?><p><strong>Reason:</strong> <?= nl2br(e($l['reject_reason'])) ?></p><?php endif; ?>
<p>You’re welcome to submit an updated listing at <a href="<?= e(base_url('/post-a-sublet/')) ?>"><?= e(base_url('/post-a-sublet/')) ?></a>. Questions? Just reply to this email.</p>
