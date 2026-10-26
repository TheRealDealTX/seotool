<?php defined('BO') || exit;
// /category/tips/ - kept from WordPress; lists every guide grouped by topic.
$crumbs = [['Home', '/'], ['Tips', '/category/tips/']];
$groups = [];
foreach ($POSTS as $s => $p) $groups[$p['cat']][$s] = $p;
page_head([
    'title' => 'Archery Tips & Bowhunting Guides | Better Outdoors',
    'desc'  => 'Archery tips from Better Outdoors: draw length adjustment, bow grip and torque, choosing a bow package, plus Mathews, Bear and PSE bow reviews.',
    'path'  => '/category/tips/',
    'schema' => [breadcrumb_schema($crumbs), ['@type' => 'CollectionPage', 'name' => 'Archery Tips', 'url' => SITE_URL . '/category/tips/']],
]);
?>
<section class="page-hero mist-after">
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Archery Tips &amp; Bowhunting Guides</h1>
    <p>Practical, field-tested tips to help you set up, tune and choose the right bow. Every Better Outdoors tip is written to work in real hunting conditions, not just on paper.</p>
  </div>
</section>
<section class="section-mist" style="padding:10px 0 90px">
  <div class="wrap">
<?php $heads = ['Bow Tuning' => 'Bow Tuning Tips', 'Hunting Tips' => 'Bowhunting Tips', 'Outdoor Tips' => 'Outdoor & Camping Tips', 'Bow Guides' => 'Buying Guides', 'Bow Reviews' => 'Compound Bow Reviews'];
foreach ($heads as $g => $head): if (empty($groups[$g])) continue; ?>
    <h2 class="reveal" style="margin:30px 0 24px"><?= e($head) ?></h2>
    <div class="post-grid" style="margin-bottom:30px">
<?php foreach ($groups[$g] as $s => $p) echo post_card($s, $p); ?>
    </div>
<?php endforeach; ?>
    <div class="prose" style="max-width:860px;margin:40px auto 0">
      <h2 id="quick-tips">Five Quick Archery Tips That Help Every Hunter</h2>
      <ol class="steps">
        <li><strong>Get your draw length right first.</strong> It affects anchor, peep alignment and accuracy more than any accessory. Use our <a href="/tools/draw-length-calculator/">draw length calculator</a>.</li>
        <li><strong>Relax your bow hand.</strong> A tight grip torques the riser. Read our <a href="/bear-archery-bear-paw-grip/">bow grip guide</a>.</li>
        <li><strong>Shoot broadheads before the season.</strong> Field points and broadheads don&rsquo;t always hit together.</li>
        <li><strong>Practice from elevation.</strong> If you hunt from a treestand, practice from one, bending at the waist.</li>
        <li><strong>Know your real arrow speed.</strong> Use the <a href="/tools/arrow-speed-calculator/">arrow speed calculator</a> or a chronograph to set accurate sight pins.</li>
      </ol>
    </div>
  </div>
</section>
<?php page_foot(); ?>
