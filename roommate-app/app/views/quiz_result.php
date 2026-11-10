<div class="narrow quiz-result">
  <div class="card center result-card">
    <div class="result-emoji"><?= $t['emoji'] ?></div>
    <p class="pill">Your roommate type</p>
    <h1><?= e($t['name']) ?></h1>
    <p class="lead"><?= e($t['desc']) ?></p>
    <p class="small muted">Best with: <?= e(implode(' · ', array_map(fn($k) => QUIZ_TYPES[$k]['emoji'] . ' ' . QUIZ_TYPES[$k]['name'], $t['best']))) ?></p>
    <p class="small muted">We updated your lifestyle preferences from your answers. You can fine-tune them in <a href="/profile/edit">Edit profile</a>.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="/match"><?= icon('heart') ?> Start matching</a>
      <button type="button" class="btn btn-outline js-share-type" data-text="I'm <?= e($t['name']) ?> <?= $t['emoji'] ?> on <?= e(setting('site_name')) ?>! What kind of roommate are you? <?= e(base_url()) ?>/quiz">Share</button>
      <a class="btn btn-ghost" href="/quiz">Retake</a>
    </div>
  </div>
  <?php if ($people): ?>
  <h2 class="section-sub">Renters you'd vibe with</h2>
  <ul class="card people-list big">
    <?php foreach ($people as $p): ?>
    <li><a href="/u/<?= e($p['username']) ?>"><?= avatar($p, 'md') ?></a><div class="grow"><a class="strong" href="/u/<?= e($p['username']) ?>"><?= e($p['name']) ?></a><small class="muted"><?= quiz_badge($p['quiz_type']) ?> <?= e($p['city']) ?></small></div><div class="pl-actions"><a class="btn btn-outline btn-sm" href="/messages/<?= e($p['username']) ?>">Message</a></div></li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>
</div>
