<div class="profile">
  <section class="card profile-hero">
    <div class="profile-cover" style="--h:<?= crc32($u['username']) % 360 ?>"></div>
    <div class="profile-main">
      <div class="avatar-wrap profile-avatar"><?= avatar($u, 'xl') ?><?php if (is_online($u)): ?><span class="online-dot"></span><?php endif; ?></div>
      <div class="profile-id">
        <h1><?= e($u['name']) ?><?php if ($u['is_verified']): ?> <span class="verified" title="Verified member"><?= icon('check') ?></span><?php endif; ?><?php if (age_of($u)): ?><span class="age">, <?= age_of($u) ?></span><?php endif; ?></h1>
        <p class="muted">@<?= e($u['username']) ?> · <?= e(label('looking_for', $u['looking_for'])) ?><?= $u['city'] ? ' · ' . e($u['city']) : '' ?></p>
        <p class="muted small"><?= $friendCount ?> friend<?= $friendCount === 1 ? '' : 's' ?><?= $mutualCount ? " · $mutualCount mutual" : '' ?> · Joined <?= e(date('M Y', strtotime($u['created_at']))) ?><?= !is_online($u) && $u['last_seen'] ? ' · Active ' . e(time_ago($u['last_seen'])) . ' ago' : '' ?></p>
        <?= quiz_badge($u['quiz_type']) ?>
        <?php if ($isMe && !$u['quiz_type']): ?><a class="type-badge type-badge-cta" href="/quiz">🧩 Take the roommate quiz</a><?php endif; ?>
        <?php if ($u['status'] !== 'active'): ?><span class="tag tag-danger">Suspended</span><?php endif; ?>
      </div>
      <div class="profile-actions">
        <?php if ($isMe): ?>
          <a class="btn btn-primary" href="/profile/edit"><?= icon('edit') ?> Edit profile</a>
        <?php else: ?>
          <?php partial('partials/friend_button', ['u' => $u, 'fstatus' => $fstatus]); ?>
          <?php if ($canMessage): ?><a class="btn btn-primary" href="/messages/<?= e($u['username']) ?>"><?= icon('chat') ?> Message</a><?php endif; ?>
          <details class="menu menu-right">
            <summary class="btn btn-outline btn-icon" aria-label="More"><?= icon('more') ?></summary>
            <div class="menu-pop">
              <?php if ($fstatus === 'friends'): ?><a href="/agreement/<?= e($u['username']) ?>">📝 Roommate agreement</a><?php endif; ?>
              <button type="button" class="js-report" data-type="user" data-id="<?= (int)$u['id'] ?>"><?= icon('flag') ?> Report profile</button>
              <form method="post" action="/block/<?= (int)$u['id'] ?>" data-confirm="Block <?= e($u['name']) ?>? They won't be able to see your profile or message you."><?= csrf_field() ?><button type="submit"><?= icon('ban') ?> Block</button></form>
              <?php if (is_admin()): ?><a href="/admin/users/<?= (int)$u['id'] ?>"><?= icon('shield') ?> Manage in admin</a><?php endif; ?>
            </div>
          </details>
        <?php endif; ?>
      </div>
    </div>
  </section>

  <div class="profile-grid">
    <div class="profile-side">
      <?php if ($match): ?>
      <section class="card match-card">
        <div class="match-ring <?= score_class($match['score']) ?>" style="--p:<?= $match['score'] ?>"><span><?= $match['score'] ?>%</span></div>
        <div><h3>Compatibility</h3>
          <?php if ($match['reasons']): ?><ul class="reasons"><?php foreach ($match['reasons'] as $r): ?><li><?= icon('check') ?><?= e($r) ?></li><?php endforeach; ?></ul>
          <?php else: ?><p class="muted small">Add more to your profile for a better match estimate.</p><?php endif; ?>
        </div>
      </section>
      <?php endif; ?>

      <section class="card">
        <h3 class="card-title">Roommate details</h3>
        <dl class="facts">
          <?php if (budget_label($u)): ?><div><dt><?= icon('dollar') ?>Budget</dt><dd><?= e(budget_label($u)) ?>/mo</dd></div><?php endif; ?>
          <?php if ($u['move_in_date']): ?><div><dt><?= icon('calendar') ?>Move-in</dt><dd><?= e(date('M j, Y', strtotime($u['move_in_date']))) ?></dd></div><?php endif; ?>
          <?php if ($u['lease_months']): ?><div><dt><?= icon('calendar') ?>Lease</dt><dd><?= (int)$u['lease_months'] ?> months</dd></div><?php endif; ?>
          <?php if ($u['occupation']): ?><div><dt><?= icon('briefcase') ?>Work</dt><dd><?= e($u['occupation']) ?><?= $u['work_from_home'] ? ' · WFH' : '' ?></dd></div><?php endif; ?>
          <?php if ($u['gender']): ?><div><dt><?= icon('user') ?>Gender</dt><dd><?= e(label('gender', $u['gender'])) ?></dd></div><?php endif; ?>
          <div><dt><?= icon('users') ?>Prefers</dt><dd><?= e(label('gender_pref', $u['gender_pref'])) ?></dd></div>
        </dl>
        <h4 class="mini-title">Lifestyle</h4>
        <div class="chips">
          <span class="chip"><?= e(label('cleanliness', $u['cleanliness'])) ?></span>
          <span class="chip"><?= e(label('sleep_schedule', $u['sleep_schedule'])) ?></span>
          <span class="chip"><?= e(label('smoking', $u['smoking'])) ?></span>
          <span class="chip"><?= e(label('pets', $u['pets'])) ?></span>
          <span class="chip"><?= e(label('guests', $u['guests'])) ?></span>
        </div>
        <?php if ($u['interests']): ?>
        <h4 class="mini-title">Interests</h4>
        <div class="chips"><?php foreach (explode(',', $u['interests']) as $i): ?><span class="chip chip-soft"><?= e(trim($i)) ?></span><?php endforeach; ?></div>
        <?php endif; ?>
        <?php if ($u['instagram']): ?><p class="small" style="margin-top:12px"><a href="https://instagram.com/<?= e($u['instagram']) ?>" target="_blank" rel="noopener nofollow"><?= icon('link') ?> @<?= e($u['instagram']) ?></a></p><?php endif; ?>
      </section>

      <section class="card">
        <h3 class="card-title">Preferred properties</h3>
        <?php if (!$props): ?><p class="muted small"><?= $isMe ? 'You haven’t picked any properties yet. <a href="/properties">Browse properties</a>' : 'No properties selected yet.' ?></p><?php endif; ?>
        <ul class="prop-mini-list">
          <?php foreach ($props as $p): ?>
          <li><a href="/properties/<?= e($p['slug']) ?>"><?= icon('building') ?><span><?= e($p['name']) ?><small class="muted"><?= e($p['city']) ?></small></span></a><?php if (!$isMe && $p['shared']): ?><span class="tag tag-ok">You too</span><?php endif; ?></li>
          <?php endforeach; ?>
        </ul>
      </section>

      <?php if ($mutualUsers): ?>
      <section class="card">
        <h3 class="card-title">Mutual friends</h3>
        <div class="avatar-row"><?php foreach ($mutualUsers as $m): ?><a href="/u/<?= e($m['username']) ?>" title="<?= e($m['name']) ?>"><?= avatar($m, 'sm') ?></a><?php endforeach; ?></div>
      </section>
      <?php endif; ?>
    </div>

    <div class="profile-content">
      <section class="card">
        <h3 class="card-title">About <?= e(explode(' ', $u['name'])[0]) ?></h3>
        <?php if ($u['bio']): ?><div class="prose"><?= linkify($u['bio']) ?></div>
        <?php else: ?><p class="muted"><?= $isMe ? 'Tell potential roommates about yourself. <a href="/profile/edit">Add a bio</a>' : 'No bio yet.' ?></p><?php endif; ?>
      </section>
      <h3 class="section-sub">Posts</h3>
      <?php if (!$posts): ?><div class="card empty-state small"><p class="muted">No posts yet.</p></div><?php endif; ?>
      <?php foreach ($posts as $p) partial('partials/post', ['p' => $p]); ?>
    </div>
  </div>
</div>
