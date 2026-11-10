<div class="layout-3">
  <aside class="side-left">
    <div class="card side-card me-card">
      <a href="/u/<?= e(current_user()['username']) ?>" class="me-link"><?= avatar(current_user(), 'lg') ?><div><strong><?= e(current_user()['name']) ?></strong><small class="muted">@<?= e(current_user()['username']) ?></small></div></a>
      <?php if ($completeness < 100): ?>
      <div class="progress-block">
        <div class="progress-label"><span>Profile <?= $completeness ?>% complete</span><a href="/profile/edit">Finish</a></div>
        <div class="progress"><span style="width:<?= $completeness ?>%"></span></div>
        <small class="muted">Complete profiles get far more friend requests.</small>
      </div>
      <?php endif; ?>
    </div>
    <div class="card side-card">
      <h3 class="side-title">My properties</h3>
      <?php if ($myProps): ?>
        <ul class="side-list"><?php foreach ($myProps as $mp): ?><li><a href="/properties/<?= e($mp['slug']) ?>"><?= icon('building') ?><?= e($mp['name']) ?></a></li><?php endforeach; ?></ul>
      <?php else: ?>
        <p class="muted small">Pick the apartments you're interested in to meet renters who want the same place.</p>
      <?php endif; ?>
      <a class="btn btn-sm btn-outline btn-block" href="/properties"><?= icon('plus') ?> Browse properties</a>
    </div>
  </aside>

  <section class="feed-col">
    <form method="post" action="/post" enctype="multipart/form-data" class="card composer">
      <?= csrf_field() ?>
      <div class="composer-row">
        <?= avatar(current_user(), 'md') ?>
        <textarea name="body" rows="2" maxlength="3000" placeholder="Looking for a roommate? Share an update, <?= e(explode(' ', current_user()['name'])[0]) ?>…" class="autogrow"></textarea>
      </div>
      <div class="composer-preview" hidden><img alt=""><button type="button" class="iconbtn composer-clear" aria-label="Remove image"><?= icon('x') ?></button></div>
      <div class="composer-actions">
        <label class="act" title="Add photo"><?= icon('image') ?> Photo<input type="file" name="image" accept="image/*" hidden class="js-img-input"></label>
        <?php if ($myProps): ?>
        <select name="property_id" class="select-sm" aria-label="Tag a property">
          <option value="">Tag a property (optional)</option>
          <?php foreach ($myProps as $mp): ?><option value="<?= (int)$mp['id'] ?>"><?= e($mp['name']) ?></option><?php endforeach; ?>
        </select>
        <?php endif; ?>
        <button class="btn btn-primary btn-sm" type="submit">Post</button>
      </div>
    </form>

    <nav class="tabs">
      <a href="/home" class="<?= $tab === 'all' ? 'active' : '' ?>">Everyone</a>
      <a href="/home?tab=friends" class="<?= $tab === 'friends' ? 'active' : '' ?>">Friends</a>
      <a href="/home?tab=properties" class="<?= $tab === 'properties' ? 'active' : '' ?>">My properties</a>
    </nav>

    <?php if (!$posts): ?>
      <div class="card empty-state">
        <?= icon('sparkle') ?>
        <h3><?= $page > 1 ? 'No more posts' : 'Nothing here yet' ?></h3>
        <p class="muted"><?= $tab === 'friends' ? 'Add friends to see their updates here.' : ($tab === 'properties' ? 'Posts tagged with your properties will show up here.' : 'Be the first to post!') ?></p>
      </div>
    <?php endif; ?>
    <?php foreach ($posts as $p) partial('partials/post', ['p' => $p]); ?>
    <div class="pager">
      <?php if ($page > 1): ?><a class="btn btn-outline btn-sm" href="?<?= e(http_build_query(['tab' => $tab, 'page' => $page - 1])) ?>">Newer</a><?php endif; ?>
      <?php if (count($posts) === 15): ?><a class="btn btn-outline btn-sm" href="?<?= e(http_build_query(['tab' => $tab, 'page' => $page + 1])) ?>">Older posts</a><?php endif; ?>
    </div>
  </section>

  <aside class="side-right">
    <div class="card side-card">
      <h3 class="side-title">Top matches for you</h3>
      <?php if (!$suggest): ?><p class="muted small">No suggestions yet — check back as more renters join.</p><?php endif; ?>
      <ul class="match-list">
        <?php foreach ($suggest as $s): ?>
        <li>
          <a href="/u/<?= e($s['u']['username']) ?>"><?= avatar($s['u'], 'sm') ?></a>
          <div class="match-id"><a href="/u/<?= e($s['u']['username']) ?>"><?= e($s['u']['name']) ?></a><small class="muted"><?= e($s['m']['reasons'][0] ?? label('looking_for', $s['u']['looking_for'])) ?></small></div>
          <span class="score sm <?= score_class($s['m']['score']) ?>"><?= $s['m']['score'] ?>%</span>
        </li>
        <?php endforeach; ?>
      </ul>
      <a class="btn btn-sm btn-outline btn-block" href="/discover">See all matches</a>
    </div>
    <div class="card side-card small muted">
      <a href="/safety">Safety tips</a> · <a href="/terms">Terms</a> · <a href="/privacy">Privacy</a><br>© <?= date('Y') ?> <?= e(setting('site_name')) ?>
    </div>
  </aside>
</div>
