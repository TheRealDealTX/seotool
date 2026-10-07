<?php
defined('GAP') || exit;
/** @var array $p */
$trail = cat_trail($p['category']);
$trail[] = [$p['name'], $p['path']];
$cat = category($p['category']);
$brand = $p['brand_path'] ? $CAT['brands'][$p['brand_path']] : null;

// Related: same category first, then the parent category, never itself.
$related = pick($cat['products'], 8, [$p['path']]);
if (count($related) < 4 && $cat['parent']) $related = array_merge($related, pick(category($cat['parent'])['products'], 8 - count($related), array_merge([$p['path']], array_column($related, 'path'))));
// A tool that fits this product.
$tool = null;
foreach (TOOLS as $slug => $t) if (in_array($p['kind'], $t[3], true)) { $tool = [$slug, $t]; break; }

$ld = [
    '@type' => 'Product', 'name' => $p['name'], 'description' => $p['summary'],
    'image' => abs_url($p['photo']['src'] ?? kind_img($p['kind'])), 'url' => abs_url($p['path']), 'category' => $cat['name'],
];
if ($p['brand_name'] ?? '') $ld['brand'] = ['@type' => 'Brand', 'name' => $p['brand_name']];
$meta = [
    'title' => $p['title'], 'desc' => $p['meta'], 'canonical' => $p['path'], 'og_type' => 'product',
    'jsonld' => array_filter([$ld, crumbs_ld($trail), faq_ld($p['faq'] ?? [])]),
    'body_class' => 'is-product',
];
$data = card_data($p);
$ph = $p['photo'] ?? null;
?>
<div class="wrap"><?= crumbs($trail) ?></div>

<section class="pdp wrap" data-product="<?= $data ?>">
  <div class="pdp-stage reveal">
<?php if ($ph): ?>
    <figure class="stage stage-photo tilt-deep">
      <?= photo_img($ph, $p['kind'], 'Representative photo for ' . $p['name'], '(max-width: 900px) 100vw, 600px', 'eager') ?>
      <span class="stage-badge"><?= e($cat['name']) ?></span>
    </figure>
    <p class="stage-note">Representative photo. Check the retailer listing for the exact model, color and size.<br><span class="credit"><?= photo_credit($ph) ?></span></p>
<?php else: ?>
    <div class="stage tilt-deep" data-kind="<?= e($p['kind']) ?>">
      <svg class="stage-rings" viewBox="0 0 400 400" aria-hidden="true"><?php for ($i = 1; $i <= 8; $i++): ?><circle cx="200" cy="200" r="<?= 24 + $i * 21 ?>" style="--i:<?= $i ?>"/><?php endfor; ?></svg>
      <img src="<?= kind_img($p['kind']) ?>" alt="<?= e($p['name']) ?> illustration" width="320" height="320">
      <span class="stage-badge"><?= e($cat['name']) ?></span>
    </div>
<?php endif; ?>
  </div>

  <div class="pdp-info">
    <?php if ($brand): ?><a class="pdp-brand" href="<?= e($brand['path']) ?>"><?= e($p['brand_name']) ?></a><?php elseif ($p['brand_name'] ?? ''): ?><span class="pdp-brand"><?= e($p['brand_name']) ?></span><?php endif; ?>
    <h1><?= e($p['h1']) ?></h1>
    <p class="pdp-tagline"><?= e($p['tagline']) ?></p>
    <div class="pdp-price">
      <span class="price-big"><?= money((int)$p['price']) ?></span>
      <span class="price-note">Typical price. Retail prices change, so check today's price before you buy.</span>
    </div>
    <div class="buy-row">
      <div class="qty" data-qty><button type="button" aria-label="Less" data-step="-1">−</button><input type="number" min="1" max="99" value="1" aria-label="Quantity"><button type="button" aria-label="More" data-step="1">+</button></div>
      <button class="btn btn-lg btn-chain" type="button" data-add>Add to cart</button>
      <button class="icon-btn heart heart-lg" type="button" data-save aria-label="Save for later"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8 3.2 4 7 4c2.1 0 3.6 1.2 5 3 1.4-1.8 2.9-3 5-3 3.8 0 6.1 4 4.6 7.7C19.5 16.4 12 21 12 21z"/></svg></button>
    </div>
    <a class="btn btn-lg btn-outline full" href="/go/?p=<?= rawurlencode($p['path']) ?>" target="_blank" rel="sponsored nofollow noopener">Check price at retailer ↗</a>
    <label class="compare-tog pdp-compare"><input type="checkbox" data-compare> <span>Add to compare</span></label>
    <ul class="highlights">
<?php foreach ($p['highlights'] ?? [] as $h): ?>
      <li><?= e($h) ?></li>
<?php endforeach; ?>
    </ul>
    <?php if (!empty($p['use'])): ?><p class="use-tags"><?php foreach ($p['use'] as $u): ?><span class="tag"><?= e(ucwords(str_replace('-', ' ', $u))) ?></span><?php endforeach; ?><?php if (($p['level'] ?? '') === 'pro'): ?><span class="tag tag-pro">Pro grade</span><?php endif; ?></p><?php endif; ?>
  </div>
</section>

<section class="wrap pdp-detail">
  <div class="tabs" data-tabs>
    <div class="tab-list" role="tablist">
      <button role="tab" aria-selected="true" aria-controls="t-over" id="tb-over">Overview</button>
      <?php if (!empty($p['specs'])): ?><button role="tab" aria-selected="false" aria-controls="t-specs" id="tb-specs">Specs</button><?php endif; ?>
      <?php if (!empty($p['faq'])): ?><button role="tab" aria-selected="false" aria-controls="t-faq" id="tb-faq">Q&amp;A</button><?php endif; ?>
      <span class="tab-ink" aria-hidden="true"></span>
    </div>
    <div class="tab-panel prose" role="tabpanel" id="t-over" aria-labelledby="tb-over">
      <p class="summary"><?= rich($p['summary']) ?></p>
      <?= sections_block($p['body'] ?? []) ?>
    </div>
    <?php if (!empty($p['specs'])): ?>
    <div class="tab-panel" role="tabpanel" id="t-specs" aria-labelledby="tb-specs" hidden>
      <table class="specs"><tbody>
<?php foreach ($p['specs'] as [$k, $v]): ?>
        <tr><th scope="row"><?= e($k) ?></th><td><?= e($v) ?></td></tr>
<?php endforeach; ?>
      </tbody></table>
      <p class="fine">Specs are from the manufacturer's published figures where available. Confirm against the product listing before you buy.</p>
    </div>
    <?php endif; ?>
    <?php if (!empty($p['faq'])): ?>
    <div class="tab-panel" role="tabpanel" id="t-faq" aria-labelledby="tb-faq" hidden>
      <?= faq_block($p['faq'], 'Questions about the ' . $p['name']) ?>
    </div>
    <?php endif; ?>
  </div>
  <aside class="pdp-aside">
<?php if ($tool): ?>
    <a class="aside-tool tilt" href="/tools/<?= $tool[0] ?>/">
      <img src="<?= kind_img($tool[1][2]) ?>" alt="" width="64" height="64">
      <span><small>Free tool</small><b><?= e($tool[1][0]) ?></b><?= e($tool[1][1]) ?></span>
    </a>
<?php endif; ?>
    <div class="aside-box">
      <h2>Shop the category</h2>
      <ul class="aside-links">
<?php foreach (array_reverse(cat_trail($p['category'])) as [$label, $path]): ?>
        <li><a href="<?= e($path) ?>"><?= e($label) ?></a></li>
<?php endforeach; ?>
<?php if ($brand): ?><li><a href="<?= e($brand['path']) ?>">More from <?= e($brand['name']) ?></a></li><?php endif; ?>
      </ul>
    </div>
  </aside>
</section>

<?php if ($related): ?>
<section class="section related">
  <div class="wrap">
    <div class="section-head split reveal"><div><p class="eyebrow dark">Pairs well with</p><h2>More <?= e(strtolower($cat['name'])) ?> &amp; related gear</h2></div></div>
    <div class="shelf" data-shelf><?php foreach ($related as $r) echo product_card($r, 'shelf-item'); ?></div>
  </div>
</section>
<?php endif; ?>

<div class="sticky-buy" data-product="<?= $data ?>" hidden>
  <div class="wrap"><img src="<?= e($ph['sm'] ?? kind_img($p['kind'])) ?>" alt="" width="40" height="40"><span class="sb-name"><?= e($p['name']) ?></span><span class="sb-price"><?= money((int)$p['price']) ?></span><button class="btn btn-sm btn-chain" type="button" data-add>Add to cart</button></div>
</div>
