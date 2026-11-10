<div class="match-wrap">
  <div class="match-head">
    <div><h1>Roommate Match</h1><p class="muted">Swipe right on people you'd live with. If they like you back, it's a match.</p></div>
    <div class="btn-row">
      <a class="btn btn-outline btn-sm" href="/matches"><?= icon('heart') ?> Matches <span class="count"><?= $matches ?></span></a>
      <?php if ($likedMe): ?><span class="tag tag-feature"><?= $likedMe ?> liked you</span><?php endif; ?>
    </div>
  </div>
  <?php if (!current_user()['quiz_type']): ?>
  <a class="quiz-nudge" href="/quiz"><span>🧩</span><span><strong>Take the 1-minute Roommate Quiz</strong><br><small>Find your roommate type and get sharper matches.</small></span><?= icon('back') ?></a>
  <?php endif; ?>
  <div class="deck" id="deck" data-cards='<?= e(json_encode($deck, JSON_UNESCAPED_UNICODE)) ?>'>
    <div class="deck-empty">
      <div class="deck-empty-icon"><?= icon('sparkle') ?></div>
      <h3>You're all caught up</h3>
      <p class="muted">Check back soon as new renters join, or browse everyone on Discover.</p>
      <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/discover">Discover</a><a class="btn btn-outline" href="/properties">Pick properties</a></div>
    </div>
  </div>
  <div class="deck-actions">
    <button type="button" class="deck-btn undo" data-act="undo" aria-label="Undo" title="Undo (Backspace)"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/></svg></button>
    <button type="button" class="deck-btn pass" data-act="pass" aria-label="Pass" title="Pass (←)"><?= icon('x') ?></button>
    <button type="button" class="deck-btn info" data-act="info" aria-label="View profile" title="Profile (↑)"><?= icon('user') ?></button>
    <button type="button" class="deck-btn like" data-act="like" aria-label="Like" title="Like (→)"><?= icon('heart') ?></button>
  </div>
  <p class="muted small center">Tip: drag cards, or use ← → keys.</p>
</div>
<div class="modal match-modal" id="match-modal" hidden>
  <div class="modal-box center">
    <div class="match-burst">🎉</div>
    <h2>It's a match!</h2>
    <p class="muted" id="match-text"></p>
    <div class="match-avatars"><span id="match-me"><?= avatar(current_user(), 'xl') ?></span><span id="match-them"></span></div>
    <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" id="match-msg" href="#"><?= icon('chat') ?> Send a message</a><button type="button" class="btn btn-ghost js-close-match">Keep swiping</button></div>
  </div>
</div>
