<a class="tool-card reveal" data-tool-card data-cat="<?= e($t[1]) ?>" href="/<?= e($s) ?>">
  <span class="tool-ic"><?= icon($t[2]) ?></span>
  <div><h3><?= e($t[0]) ?></h3><p><?= e($t[3]) ?></p></div>
  <?php if ($t[4]): ?><span class="pop">Popular</span><?php endif; ?>
</a>
