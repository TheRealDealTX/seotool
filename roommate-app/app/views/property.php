<div class="property-page">
  <section class="card prop-hero">
    <div class="prop-hero-img" style="<?= property_image($p) ? "background-image:url('" . e(property_image($p)) . "')" : '--h:' . (crc32($p['name']) % 360) ?>"><?php if (!property_image($p)): ?><?= icon('building') ?><?php endif; ?></div>
    <div class="prop-hero-body">
      <?php if ($p['status'] !== 'approved'): ?><span class="tag tag-warn">Awaiting approval</span><?php endif; ?>
      <h1><?= e($p['name']) ?></h1>
      <p class="muted"><?= icon('pin') ?> <?= e(implode(', ', array_filter([$p['address'], $p['city'], trim(($p['state'] ?? '') . ' ' . ($p['zip'] ?? ''))]))) ?></p>
      <div class="prop-meta big">
        <?php if ($p['rent_min'] || $p['rent_max']): ?><span><?= icon('dollar') ?><?= e(money($p['rent_min'])) ?><?= $p['rent_max'] ? '–' . e(money($p['rent_max'])) : '+' ?>/mo</span><?php endif; ?>
        <span><?= icon('users') ?><strong data-interest-count><?= $count ?></strong>&nbsp;renters interested</span>
      </div>
      <?php if ($p['description']): ?><div class="prose"><?= linkify($p['description']) ?></div><?php endif; ?>
      <?php if ($p['amenities']): ?><div class="chips"><?php foreach (explode(',', $p['amenities']) as $a): ?><span class="chip chip-soft"><?= e(trim($a)) ?></span><?php endforeach; ?></div><?php endif; ?>
      <div class="prop-hero-actions">
        <?php if ($p['status'] === 'approved'): ?>
        <form method="post" action="/property/<?= (int)$p['id'] ?>/toggle"><?= csrf_field() ?>
          <button class="btn <?= $interested ? 'btn-soft' : 'btn-primary' ?>" type="submit"><?= $interested ? icon('check') . ' You\'re interested' : icon('plus') . ' I\'m interested in this property' ?></button>
        </form>
        <?php endif; ?>
        <?php if ($p['external_url']): ?><a class="btn btn-outline" href="<?= e($p['external_url']) ?>" target="_blank" rel="noopener"><?= icon('building') ?> Floor plans &amp; pricing on Rise Apartments</a><?php endif; ?>
        <?php if ($p['website']): ?><a class="btn btn-outline" href="<?= e($p['website']) ?>" target="_blank" rel="noopener nofollow"><?= icon('link') ?> Property website</a><?php endif; ?>
        <?php if (is_admin()): ?><a class="btn btn-ghost" href="/admin/properties/<?= (int)$p['id'] ?>"><?= icon('edit') ?> Edit</a><?php endif; ?>
      </div>
    </div>
  </section>

  <div class="layout-2">
    <section>
      <h2 class="section-sub">Renters interested in <?= e($p['name']) ?></h2>
      <?php if (!$list): ?>
        <div class="card empty-state"><?= icon('users') ?><h3>No one yet</h3><p class="muted"><?= $interested ? 'You’re the first! Others will see you when they pick this property.' : 'Be the first — mark yourself as interested.' ?></p></div>
      <?php endif; ?>
      <div class="grid grid-2">
        <?php foreach ($list as $r) partial('partials/user_card', ['u' => $r['u'], 'match' => $r['m']]); ?>
      </div>
    </section>
    <aside>
      <section class="card lounge" id="lounge" data-pid="<?= (int)$p['id'] ?>">
        <div class="lounge-head"><h3><?= icon('chat') ?> Property lounge</h3><span class="muted small" id="lounge-online"></span></div>
        <p class="muted small lounge-sub">Group chat for everyone interested in <?= e($p['name']) ?>.</p>
        <div class="lounge-msgs" id="lounge-msgs"><p class="muted small center">Loading…</p></div>
        <?php if ($interested): ?>
        <form class="lounge-form" id="lounge-form"><button type="button" class="tool-btn js-emoji" data-target="#lounge-input" aria-label="Emoji">😊</button><input type="text" name="body" id="lounge-input" maxlength="1000" placeholder="Say hi to the group…" required autocomplete="off"><button class="btn btn-primary btn-icon" aria-label="Send"><?= icon('send') ?></button></form>
        <?php else: ?><p class="small center lounge-join">Mark yourself as interested to join the conversation.</p><?php endif; ?>
      </section>
      <h2 class="section-sub">Posts about this property</h2>
      <?php if ($interested): ?>
      <form method="post" action="/post" class="card composer">
        <?= csrf_field() ?><input type="hidden" name="property_id" value="<?= (int)$p['id'] ?>">
        <textarea name="body" rows="2" maxlength="3000" required placeholder="Ask about <?= e($p['name']) ?> or say you're looking…" class="autogrow"></textarea>
        <div class="composer-actions"><span class="spacer"></span><button class="btn btn-primary btn-sm" type="submit">Post</button></div>
      </form>
      <?php endif; ?>
      <?php if (!$posts): ?><div class="card empty-state small"><p class="muted">No posts yet.</p></div><?php endif; ?>
      <?php foreach ($posts as $post) partial('partials/post', ['p' => $post]); ?>
    </aside>
  </div>
</div>
