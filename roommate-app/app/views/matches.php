<div class="narrow-lg">
  <div class="page-head"><div><h1>Your matches</h1><p class="muted">People who liked you back. You're automatically friends — say hi!</p></div><a class="btn btn-primary" href="/match"><?= icon('heart') ?> Keep swiping</a></div>
  <?php if (!$matches): ?><div class="card empty-state"><?= icon('heart') ?><h3>No matches yet</h3><p class="muted">Like people on Roommate Match — when they like you back, they'll show up here.</p></div><?php endif; ?>
  <div class="grid grid-3"><?php foreach ($matches as $u) partial('partials/user_card', ['u' => $u, 'match' => $u['_m']]); ?></div>
  <?php if ($likedMe): ?>
  <h2 class="section-sub" style="margin-top:28px">Liked you <span class="count hot"><?= count($likedMe) ?></span></h2>
  <p class="muted small">Like them back on Roommate Match (or here) to match.</p>
  <div class="grid grid-3"><?php foreach ($likedMe as $u): ?>
    <div class="card user-card">
      <?php partial('partials/user_card_top', ['u' => $u, 'match' => $u['_m']]); ?>
      <form method="post" action="/api/swipe" class="js-likeback"><?= csrf_field() ?><input type="hidden" name="target" value="<?= (int)$u['id'] ?>"><input type="hidden" name="liked" value="1"><button class="btn btn-primary btn-block"><?= icon('heart') ?> Like back</button></form>
    </div>
  <?php endforeach; ?></div>
  <?php endif; ?>
</div>
