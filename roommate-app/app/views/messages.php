<div class="chat card">
  <aside class="chat-list">
    <div class="chat-list-head"><h1>Messages</h1></div>
    <?php if (!$convos): ?><div class="empty-state small"><p class="muted">No conversations yet. Find someone on <a href="/discover">Discover</a> and say hi!</p></div><?php endif; ?>
    <ul>
      <?php foreach ($convos as $c): ?>
      <li><a href="/messages/<?= e($c['username']) ?>" class="<?= $other && (int)$other['id'] === (int)$c['uid'] ? 'active' : '' ?> <?= $c['unread'] ? 'unread' : '' ?>">
        <div class="avatar-wrap"><?= avatar($c, 'md') ?><?php if (is_online($c)): ?><span class="online-dot"></span><?php endif; ?></div>
        <div class="chat-li-body"><div class="chat-li-top"><strong><?= e($c['name']) ?></strong><small class="muted"><?= e(time_ago($c['last_message_at'])) ?></small></div>
          <div class="chat-li-last"><?= (int)$c['last_sender'] === uid() ? 'You: ' : '' ?><?= e(mb_strimwidth((string)$c['last_body'], 0, 60, '…')) ?></div></div>
        <?php if ($c['unread']): ?><span class="badge"><?= (int)$c['unread'] ?></span><?php endif; ?>
      </a></li>
      <?php endforeach; ?>
    </ul>
  </aside>
  <section class="chat-main">
    <?php if (!$other): ?>
      <div class="chat-empty"><?= icon('chat') ?><h2>Your messages</h2><p class="muted">Pick a conversation, or message someone from their profile.</p></div>
    <?php else: ?>
      <header class="chat-head">
        <a class="iconbtn chat-back" href="/messages" aria-label="Back"><?= icon('back') ?></a>
        <a href="/u/<?= e($other['username']) ?>" class="chat-who"><?= avatar($other, 'sm') ?><div><strong><?= e($other['name']) ?></strong><small class="muted"><?= is_online($other) ? 'Online now' : ($other['last_seen'] ? 'Active ' . e(time_ago($other['last_seen'])) . ' ago' : '') ?></small></div></a>
        <?php if ($fstatus === 'friends'): ?><a class="btn btn-ghost btn-sm hide-sm" href="/agreement/<?= e($other['username']) ?>" title="Roommate agreement">📝 Agreement</a><?php endif; ?>
        <a class="btn btn-outline btn-sm" href="/u/<?= e($other['username']) ?>">Profile</a>
      </header>
      <div class="chat-msgs" id="chat-msgs" data-other="<?= (int)$other['id'] ?>" data-initial='<?= e(json_encode($msgs, JSON_UNESCAPED_UNICODE)) ?>'>
        <div class="chat-hello muted"<?= $msgs ? ' hidden' : '' ?>><?= avatar($other, 'lg') ?><p>Say hi to <?= e(explode(' ', $other['name'])[0]) ?>! Introduce yourself and mention which property you're interested in.</p></div>
      </div>
      <div class="typing" id="typing" hidden><span></span><span></span><span></span> <?= e(explode(' ', $other['name'])[0]) ?> is typing</div>
      <?php if ($canMessage): ?>
      <div class="reply-bar" id="reply-bar" hidden><div><small>Replying to <b class="rb-who"></b></small><span class="rb-text"></span></div><button type="button" class="iconbtn rb-x" aria-label="Cancel reply"><?= icon('x') ?></button></div>
      <div class="reply-bar edit-bar" id="edit-bar" hidden><div><small><b>Editing message</b></small><span class="rb-text"></span></div><button type="button" class="iconbtn rb-x" aria-label="Cancel edit"><?= icon('x') ?></button></div>
      <form class="chat-form" id="chat-form" data-other="<?= (int)$other['id'] ?>" data-other-name="<?= e(explode(' ', $other['name'])[0]) ?>">
        <button type="button" class="tool-btn js-emoji" data-target="#chat-input" aria-label="Emoji">😊</button>
        <button type="button" class="tool-btn js-gif" data-mode="chat" aria-label="GIF">GIF</button>
        <textarea name="body" id="chat-input" rows="1" maxlength="4000" placeholder="Write a message…"><?= e(mb_substr((string)($_GET['draft'] ?? ''), 0, 2000)) ?></textarea>
        <button class="btn btn-primary chat-send" type="submit" aria-label="Send"><?= icon('send') ?></button>
      </form>
      <?php else: ?>
      <div class="chat-locked muted small"><?= setting('messaging_friends_only') === '1' && $fstatus !== 'friends' ? 'You need to be friends to message. ' . ($fstatus === 'none' ? '<a href="/u/' . e($other['username']) . '">Send a friend request</a>.' : '') : 'You can’t reply to this conversation.' ?></div>
      <?php endif; ?>
    <?php endif; ?>
  </section>
</div>
