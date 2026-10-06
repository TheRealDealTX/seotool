<?php defined('SLT') || exit;
page_hero(['title' => 'Areas We Serve', 'eyebrow' => 'Local landscape lighting', 'sub' => 'Spring Landscape Lighting designs and installs outdoor lighting for homes across Spring and the North Houston suburbs.', 'cta' => true, 'crumbs' => [['Home', '/'], ['Service Areas', null]]]);
$blurbs = [
 'spring-tx' => 'From Old Town Spring to newer subdivisions, homes of every style and lot size.',
 'klein-tx' => 'Established neighborhoods with mature trees and older systems ready for LED.',
 'champion-forest' => 'Wooded lots and big canopy trees that reward thoughtful tree lighting.',
 'gleannloch-farms' => 'Master-planned living, HOA guidelines, and long driveways done right.',
 'augusta-pines' => 'Golf-course views, backyard living and careful glare control.',
 'the-woodlands-tx' => 'Forest settings where restraint and covenant-friendly design matter.',
];
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap split">
    <div>
      <h2 data-split>Rooted in Spring. Lighting North Houston.</h2>
      <p style="color:#cfdcd3" data-reveal>Every community here has its own character: tree cover, lot sizes, home styles and HOA rules. We design for those details. If you are near any of these areas and do not see your neighborhood, just ask.</p>
      <div class="grid-2" style="margin-top:26px">
        <?php $i = 0; foreach (AREAS as $k => $a): ?>
        <a class="tcard" href="/service-areas/<?= $k ?>/" data-reveal data-delay="<?= $i++ % 2 ?>"><span class="tcard__icon"><?= icon('map-pin') ?></span><div><h3><?= e($a['name']) ?></h3><p><?= e($blurbs[$k]) ?></p></div><span class="tcard__go"><?= icon('arrow-up-right') ?></span></a>
        <?php endforeach; ?>
      </div>
    </div>
    <div class="areamap" data-reveal="zoom" aria-hidden="true">
      <span class="areamap__ring" style="--i:6%"></span><span class="areamap__ring" style="--i:22%;animation-direction:reverse"></span><span class="areamap__ring" style="--i:38%"></span>
      <span class="areamap__pin areamap__pin--main" style="--x:50%;--y:50%"><i></i>Spring</span>
      <span class="areamap__pin" style="--x:58%;--y:16%;--d:.4s"><i></i>The Woodlands</span>
      <span class="areamap__pin" style="--x:22%;--y:30%;--d:.8s"><i></i>Gleannloch Farms</span>
      <span class="areamap__pin" style="--x:34%;--y:72%;--d:1.2s"><i></i>Champion Forest</span>
      <span class="areamap__pin" style="--x:66%;--y:78%;--d:1.6s"><i></i>Klein</span>
      <span class="areamap__pin" style="--x:80%;--y:42%;--d:2s"><i></i>Augusta Pines</span>
    </div>
  </div>
</section>
<section class="sec sec--forest"><div class="wrap"><?php section_head('Available everywhere we work', 'Our landscape lighting services'); ?><div class="grid-3"><?php $i = 0; foreach (SERVICES as $k => $s) echo service_card($k, $s, $i++); ?></div></div></section>
<?php cta_band(); ?>
