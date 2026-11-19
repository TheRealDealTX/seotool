<?php defined('M1S') || exit;
$editing = (bool)$thread;
$action = $editing ? thread_url($thread) . 'edit/' : '/submit/';
?>
<div class="narrow">
  <h1><?= $editing ? 'Edit your post' : 'Create a post' ?></h1>
  <form class="form card-pad" method="post" action="<?= e($action) ?>" enctype="multipart/form-data">
    <?= member_csrf_field() ?>
    <?php if (!current_user()): ?>
      <div class="notice">Posting as a guest: just add your name and email. <a href="/login/?next=/submit/" rel="nofollow">Log in</a> or <a href="/register/" rel="nofollow">join</a> to vote, upload images and get a profile.</div>
    <?php endif; ?>
    <?php if (!$editing): ?>
    <label for="community">Community</label>
    <select id="community" name="community" required>
      <option value="">Choose a community…</option>
      <?php foreach ($communities as $c): ?>
        <option value="<?= e($c['slug']) ?>"<?= $selected === $c['slug'] ? ' selected' : '' ?>><?= e($c['name']) ?></option>
      <?php endforeach; ?>
    </select>
    <?php else: ?>
      <p class="muted">Posting in <?= community_chip($thread) ?></p>
    <?php endif; ?>

    <label for="title">Title</label>
    <input id="title" name="title" type="text" required minlength="8" maxlength="300" value="<?= e($editing ? $thread['title'] : old('title')) ?>" placeholder="Ask a clear question or sum up your tip">
    <p class="hint">Good titles get better answers: “Landlord kept my deposit for normal wear. What are my options in Texas?”</p>

    <label for="body">Text <span class="muted">(optional)</span></label>
    <textarea id="body" name="body" rows="10" maxlength="40000" placeholder="Add details, what you've tried, and where you are."><?= e($editing ? $thread['body'] : old('body')) ?></textarea>
    <p class="hint">Markdown works: **bold**, *italic*, [link text](https://…), - bullet lists, &gt; quotes, ## headings.</p>

    <label for="link_url">Link <span class="muted">(optional)</span></label>
    <input id="link_url" name="link_url" type="url" maxlength="1000" value="<?= e($editing ? (string)$thread['link_url'] : old('link_url')) ?>" placeholder="https://">

    <?php if (!current_user()): ?>
      <?= guest_fields() ?>
    <?php endif; ?>
    <?php if (!$editing && current_user()): ?>
      <label for="image">Image <span class="muted">(optional, JPG/PNG/WebP/GIF up to 8 MB)</span></label>
      <input id="image" name="image" type="file" accept="image/jpeg,image/png,image/webp,image/gif">
    <?php elseif ($editing && $thread['image']): ?>
      <label class="check"><input type="checkbox" name="remove_image" value="1"> Remove the image</label>
    <?php endif; ?>

    <div class="form-row">
      <a class="btn btn-ghost" href="<?= e($editing ? thread_url($thread) : '/forum/') ?>">Cancel</a>
      <button class="btn btn-accent" type="submit"><?= $editing ? 'Save changes' : 'Post' ?></button>
    </div>
  </form>
  <aside class="card-pad tips">
    <h2>Posting tips</h2>
    <ul>
      <li>Search first: your question may already have great answers.</li>
      <li>Never post addresses, phone numbers, policy or claim numbers.</li>
      <li>Promotional posts and affiliate links are removed.</li>
      <li>Read the <a href="/community-guidelines/">community guidelines</a>.</li>
    </ul>
  </aside>
</div>
