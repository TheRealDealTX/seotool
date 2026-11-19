<?php defined('M1S') || exit; $here = strtok($_SERVER['REQUEST_URI'] ?? '', '?'); ?>
<nav class="admin-nav sort-tabs" aria-label="Admin">
  <?php foreach (['/admin/' => 'Dashboard', '/admin/reports/' => 'Reports', '/admin/users/' => 'Users', '/admin/articles/' => 'Articles', '/admin/communities/' => 'Communities', '/admin/topics/' => 'Topics', '/admin/products/' => 'Products'] as $u => $l): ?>
    <?php if (in_array($u, ['/admin/articles/', '/admin/communities/', '/admin/topics/', '/admin/products/'], true) && !is_admin()) continue; ?>
    <a href="<?= $u ?>"<?= $here === $u ? ' aria-current="true"' : '' ?>><?= $l ?></a>
  <?php endforeach; ?>
</nav>
