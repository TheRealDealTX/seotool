<?php defined('M1S') || exit; ?>
<div class="narrow">
  <h1>Report <?= $type === 'thread' ? 'post' : 'comment' ?></h1>
  <blockquote class="quote-preview"><?= e(excerpt($type === 'thread' ? $row['title'] . ' ' . $row['body'] : $row['body'], 300)) ?></blockquote>
  <form class="form card-pad" method="post" action="/report/">
    <?= csrf_field() ?>
    <input type="hidden" name="type" value="<?= e($type) ?>"><input type="hidden" name="id" value="<?= (int)$id ?>">
    <fieldset>
      <legend>What's wrong with it?</legend>
      <?php foreach (['Spam or advertising', 'Harassment or hate', 'Personal information', 'Misinformation that could cause harm', 'Off-topic', 'Something else'] as $r): ?>
        <label class="check"><input type="radio" name="reason" value="<?= e($r) ?>" required> <?= e($r) ?></label>
      <?php endforeach; ?>
    </fieldset>
    <label for="detail">Details <span class="muted">(optional)</span></label>
    <textarea id="detail" name="detail" rows="3" maxlength="400"></textarea>
    <div class="form-row"><button class="btn btn-accent" type="submit">Send report</button></div>
  </form>
</div>
