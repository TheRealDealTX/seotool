<div class="narrow">
  <a class="backlink" href="/tools"><?= icon('back') ?> Tools</a>
  <h1>Roommate agreements</h1>
  <p class="muted">Put the important stuff in writing — rent, bills, chores, guests and quiet hours. Both of you can edit, and both sign when you're happy.</p>
  <?php if ($rows): ?>
  <ul class="card people-list big">
    <?php foreach ($rows as $r): $both = $r['signed_a'] && $r['signed_b']; ?>
    <li><?= avatar($r, 'md') ?><div class="grow"><a class="strong" href="/agreement/<?= e($r['username']) ?>">With <?= e($r['name']) ?></a><small class="muted">Updated <?= e(time_ago($r['updated_at'])) ?></small></div>
      <span class="tag <?= $both ? 'tag-ok' : 'tag-warn' ?>"><?= $both ? 'Signed by both' : (($r['signed_a'] || $r['signed_b']) ? '1 of 2 signed' : 'Draft') ?></span></li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>
  <h2 class="section-sub">Start a new agreement</h2>
  <?php if (!$friends): ?><div class="card empty-state small"><p class="muted">Agreements are between friends. <a href="/discover">Find a roommate</a> first.</p></div><?php endif; ?>
  <div class="avatar-pick">
    <?php foreach ($friends as $f): ?><a class="card" href="/agreement/<?= e($f['username']) ?>"><?= avatar($f, 'lg') ?><span><?= e($f['name']) ?></span></a><?php endforeach; ?>
  </div>
</div>
