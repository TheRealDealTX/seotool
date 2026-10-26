<?php
/** Roofing tool page template. Expects $slug and optional $toolBody (extra prose HTML). */
require_once dirname(__DIR__) . '/bootstrap.php';
$t = $TOOLS[$slug];
$path = "/roofing-tools/$slug/";
$crumbs = [['Home', '/'], ['Roof Tools', '/roofing-tools/'], [$t['name'], $path]];

page_start([
    'title'       => $t['title'],
    'description' => $t['description'],
    'path'        => $path,
    'body'        => 'page-tool',
    'schema'      => [
        [
            '@type'               => 'WebApplication',
            'name'                => $t['name'],
            'description'         => $t['description'],
            'url'                 => abs_url($path),
            'applicationCategory' => 'UtilitiesApplication',
            'operatingSystem'     => 'Any',
            'offers'              => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
            'provider'            => ['@id' => abs_url('/#business')],
        ],
        breadcrumb_schema($crumbs),
        faq_schema($toolFaqs),
    ],
]);
page_hero('Free Bastrop Roofing tool', $t['h1'], $t['lead'], $crumbs, null, [['All roof tools', '/roofing-tools/']]);
?>
<section class="section section-tool">
  <div class="container">
    <?php include dirname(__DIR__) . "/tools/$slug.php"; ?>
  </div>
</section>
<section class="section">
  <div class="container narrow prose">
    <?= $toolBody ?>
  </div>
</section>
<?php faq_block($toolFaqs, 'About This Tool'); ?>
<section class="section section-tint">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">More free tools</span><h2 class="section-title small">Other Roofing Tools</h2></div>
    <div class="tool-grid"><?php tool_cards([$slug]); ?></div>
  </div>
</section>
<?php
cta_band();
page_end();
