<?php $interestedIn = $interestedIn ?? []; $on = in_array((int)$p['id'], $interestedIn, true); ?>
<article class="card prop-card">
  <a class="prop-img" href="/properties/<?= e($p['slug']) ?>" style="<?= property_image($p) ? "background-image:url('" . e(property_image($p)) . "')" : '--h:' . (crc32($p['name']) % 360) ?>">
    <?php if (!property_image($p)): ?><span><?= icon('building') ?></span><?php endif; ?>
    <?php if (!empty($p['is_featured'])): ?><span class="tag tag-feature"><?= icon('star') ?> Featured</span><?php endif; ?>
  </a>
  <div class="prop-body">
    <h3><a href="/properties/<?= e($p['slug']) ?>"><?= e($p['name']) ?></a></h3>
    <p class="muted small"><?= icon('pin') ?> <?= e(trim(($p['city'] ?? '') . (($p['state'] ?? '') ? ', ' . $p['state'] : ''), ', ') ?: 'Location TBD') ?></p>
    <div class="prop-meta">
      <?php if ($p['rent_min'] || $p['rent_max']): ?><span><?= icon('dollar') ?><?= e(money($p['rent_min'])) ?><?= $p['rent_max'] ? '–' . e(money($p['rent_max'])) : '+' ?></span><?php endif; ?>
      <span><?= icon('users') ?><?= (int)($p['interested'] ?? 0) ?> interested</span>
    </div>
    <?php if (empty($guest)): ?>
    <form method="post" action="/property/<?= (int)$p['id'] ?>/toggle" class="js-toggle-prop">
      <?= csrf_field() ?>
      <button class="btn btn-sm btn-block <?= $on ? 'btn-soft is-on' : 'btn-outline' ?>" type="submit"><?= $on ? icon('check') . ' Interested' : icon('plus') . ' I\'m interested' ?></button>
    </form>
    <?php endif; ?>
  </div>
</article>
