<div class="narrow-lg agreement">
  <a class="backlink noprint" href="/agreements"><?= icon('back') ?> Agreements</a>
  <div class="page-head">
    <div><h1>Roommate agreement</h1><p class="muted">Between <strong><?= e(current_user()['name']) ?></strong> and <strong><?= e($other['name']) ?></strong><?= $row ? ' · last edited by ' . e($updatedBy) . ' ' . e(time_ago($row['updated_at'])) . ' ago' : '' ?></p></div>
    <?php if ($row && !$editing): ?><div class="btn-row noprint"><a class="btn btn-outline btn-sm" href="?edit=1"><?= icon('edit') ?> Edit</a><button type="button" class="btn btn-outline btn-sm" onclick="window.print()">Print / PDF</button><a class="btn btn-ghost btn-sm" href="/messages/<?= e($other['username']) ?>"><?= icon('chat') ?> Discuss</a></div><?php endif; ?>
  </div>
  <?php if ($row): ?>
  <div class="sign-status card">
    <div class="sig <?= $signedMe ? 'done' : '' ?>"><?= avatar(current_user(), 'sm') ?><span>You<br><small><?= $signedMe ? 'Signed ' . e(date('M j, Y', strtotime($signedMe))) : 'Not signed yet' ?></small></span></div>
    <div class="sig <?= $signedThem ? 'done' : '' ?>"><?= avatar($other, 'sm') ?><span><?= e(explode(' ', $other['name'])[0]) ?><br><small><?= $signedThem ? 'Signed ' . e(date('M j, Y', strtotime($signedThem))) : 'Not signed yet' ?></small></span></div>
    <?php if (!$signedMe && !$editing): ?>
    <form method="post" class="noprint" data-confirm="Sign this agreement? If anyone edits it later, signatures are cleared."><?= csrf_field() ?><input type="hidden" name="action" value="sign"><button class="btn btn-gold"><?= icon('check') ?> Sign agreement</button></form>
    <?php elseif ($signedMe && $signedThem): ?><span class="tag tag-ok">✓ Fully signed</span><?php endif; ?>
  </div>
  <?php endif; ?>

  <?php if ($editing): ?>
  <form method="post" class="card form form-section">
    <?= csrf_field() ?><input type="hidden" name="action" value="save">
    <?php if (!$row): ?><p class="alert alert-info"><?= icon('info') ?><span>We pre-filled common terms. Change anything — <?= e(explode(' ', $other['name'])[0]) ?> can edit too.</span></p><?php endif; ?>
    <div class="agreement-grid">
    <?php foreach ($labels as $k => [$label, $type]): ?>
      <label class="<?= $type === 'textarea' ? 'span-2' : '' ?>"><?= e($label) ?>
        <?php if ($type === 'textarea'): ?><textarea name="f[<?= $k ?>]" rows="3" class="autogrow"><?= e($data[$k] ?? '') ?></textarea>
        <?php else: ?><input type="<?= $type ?>" name="f[<?= $k ?>]" value="<?= e($data[$k] ?? '') ?>"<?= $type === 'number' ? ' min="0" step="1"' : '' ?>><?php endif; ?>
      </label>
    <?php endforeach; ?>
    </div>
    <div class="form-actions"><?php if ($row): ?><a class="btn btn-ghost" href="/agreement/<?= e($other['username']) ?>">Cancel</a><?php endif; ?><button class="btn btn-primary">Save agreement</button></div>
  </form>
  <?php else: ?>
  <article class="card agreement-doc">
    <dl>
    <?php foreach ($labels as $k => [$label, $type]): if (($data[$k] ?? '') === '') continue;
      $v = $data[$k];
      if ($type === 'date') $v = date('F j, Y', strtotime($v));
      if ($type === 'time') $v = date('g:i A', strtotime($v));
      if ($type === 'number') $v = '$' . number_format((float)$v); ?>
      <div><dt><?= e($label) ?></dt><dd><?= nl2br(e($v)) ?></dd></div>
    <?php endforeach; ?>
    </dl>
    <p class="small muted">This agreement is between roommates and doesn't replace your lease with the property.</p>
  </article>
  <?php endif; ?>
</div>
