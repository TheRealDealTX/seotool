<?php defined('APP') || exit; ?>
<p>You have a new message about <strong>“<?= e($l['title']) ?>”</strong> on The Sublet.</p>
<p><strong>From:</strong> <?= e($name) ?> &lt;<?= e($email) ?>&gt;</p>
<blockquote style="border-left:3px solid #2f6f4f;margin:12px 0;padding:8px 14px;background:#f4f7f5"><?= nl2br(e($msg)) ?></blockquote>
<p>Reply to this email to answer <?= e($name) ?> directly (your reply will show your email address to them).</p>
<p style="font-size:13px;color:#6b7b73">Safety: arrange a tour (in person or live video) and a written sublease before taking any money. Never accept overpayments or “send back the difference” requests. Your listing: <a href="<?= e(base_url(listing_url($l))) ?>"><?= e(base_url(listing_url($l))) ?></a></p>
