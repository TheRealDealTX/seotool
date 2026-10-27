<?php
defined('HA_ROOT') || exit;
$title = 'Leads';
$actions = '<a class="btn" href="/admin/leads.csv">⬇ Download spreadsheet (CSV)</a>';
?>
<div class="tabs-row">
  <a href="/admin/leads/"<?= $status === '' ? ' class="on"' : '' ?>>All</a>
  <?php foreach (LEAD_STATUSES as $k => $l): ?><a href="/admin/leads/?status=<?= $k ?>"<?= $status === $k ? ' class="on"' : '' ?>><?= $l ?></a><?php endforeach ?>
</div>
<p class="muted">New requests are emailed to <strong><?= e(config('lead_email') ?: '—') ?></strong>. Change the status as you work each lead; notes save automatically.</p>
<div class="lead-list">
  <?php foreach ($rows as $l): ?>
    <form class="card lead" method="post" action="/admin/leads/<?= $l['id'] ?>/" data-autosave>
      <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
      <div class="lead-main">
        <div class="lead-who"><strong><?= e($l['name']) ?></strong>
          <span><?php if ($l['phone']): ?><a href="tel:<?= e($l['phone']) ?>">📞 <?= e($l['phone']) ?></a><?php endif ?> <?php if ($l['email']): ?><a href="mailto:<?= e($l['email']) ?>">✉ <?= e($l['email']) ?></a><?php endif ?></span>
        </div>
        <div class="lead-meta">
          <?php if ($l['property']): ?><span>🏢 <a href="/apartment/<?= e($l['slug']) ?>/" target="_blank" rel="noopener"><?= e($l['property']) ?></a></span><?php endif ?>
          <?php foreach (['move_in' => 'Move-in', 'beds' => 'Beds', 'budget' => 'Budget'] as $k => $lab): if ($l[$k]): ?><span><?= $lab ?>: <?= e($l[$k]) ?></span><?php endif; endforeach ?>
          <span class="muted"><?= e(date('M j, Y g:ia', strtotime($l['created_at']))) ?></span>
        </div>
        <?php if ($l['message']): ?><p class="lead-msg"><?= nl2br(e($l['message'])) ?></p><?php endif ?>
      </div>
      <div class="lead-side">
        <select name="status" class="s-<?= e($l['status']) ?>"><?php foreach (LEAD_STATUSES as $k => $lab): ?><option value="<?= $k ?>"<?= $l['status'] === $k ? ' selected' : '' ?>><?= $lab ?></option><?php endforeach ?></select>
        <textarea name="notes" rows="2" placeholder="Notes…"><?= e($l['notes'] ?? '') ?></textarea>
        <small class="saved" hidden>Saved ✓</small>
      </div>
    </form>
  <?php endforeach ?>
  <?php if (!$rows): ?><div class="card empty">No leads here yet.</div><?php endif ?>
</div>
