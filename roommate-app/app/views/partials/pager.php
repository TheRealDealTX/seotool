<?php if ($pages > 1): ?>
<nav class="pager" aria-label="Pages">
  <?php if ($page > 1): ?><a class="btn btn-outline btn-sm" href="<?= e(page_link($page - 1)) ?>">Previous</a><?php endif; ?>
  <span class="muted small">Page <?= $page ?> of <?= $pages ?></span>
  <?php if ($page < $pages): ?><a class="btn btn-outline btn-sm" href="<?= e(page_link($page + 1)) ?>">Next</a><?php endif; ?>
</nav>
<?php endif; ?>
