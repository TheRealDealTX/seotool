<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
$geo = config('geo');
$cities = (array) config('service_cities', ['Friendswood']);
partial('page-hero', [
    'eyebrow' => 'Service area',
    'title'   => 'Roofing Service Area: Friendswood, TX',
    'lead'    => 'Friendswood Roofers serves homeowners in Friendswood, Texas. Here is what we keep in mind when working on roofs in this part of the upper Texas Gulf Coast.',
]);
?>
<section class="section">
  <div class="container split">
    <div class="prose" data-reveal>
      <h2>Serving homeowners in Friendswood</h2>
      <p>Our roofing services are offered to homeowners in <?= e(implode(', ', array_map(fn ($c) => $c . ', TX', $cities))) ?>. We work at your property, so there is no office visit needed: call or send an estimate request with your address or ZIP code and we will confirm that your home is within our service area.</p>
      <p>If you are outside Friendswood, you are still welcome to call and ask. We will tell you honestly whether we can help.</p>
      <h2>Local roofing considerations</h2>
      <h3>Heat and humidity</h3>
      <p>Friendswood summers are long and hot, and humidity stays high for much of the year. Heat speeds up the aging of asphalt shingles, and a poorly ventilated attic makes it worse. Humidity also encourages the dark algae streaks often seen on shingle roofs in the region. We pay close attention to attic ventilation and material choice for that reason.</p>
      <h3>Heavy rain and drainage</h3>
      <p>Clear Creek runs through Friendswood, and the area is known for heavy rain events. Intense rainfall tests flashing, valleys and gutters. Making sure water leaves the roof quickly and is carried away from the house is a key part of every repair and replacement.</p>
      <h3>Storms and hurricane season</h3>
      <p>Friendswood is close enough to the Gulf that strong thunderstorms and tropical systems are a regular concern during the Atlantic hurricane season, from June 1 to November 30. Wind resistance, secure edges and protecting an open roof during a project all matter here. See our <a href="/services/storm-damage-roof-repair/">storm damage roof repair</a> page for what to do after severe weather.</p>
      <h3>Two counties, one city</h3>
      <p>Friendswood lies in both Galveston County and Harris County. Homes on the Galveston County side are within the Texas Department of Insurance designated catastrophe area for windstorm insurance. If your home is insured, or might be insured, through the Texas Windstorm Insurance Association (TWIA), roofing work may require a windstorm inspection. Check with your insurer or agent before work begins, and see the <a href="https://www.tdi.texas.gov/wind/index.html" rel="noopener">Texas Department of Insurance windstorm information</a>.</p>
      <h3>Permits and HOAs</h3>
      <p>Permit requirements for roofing work are set locally. Contact the <a href="https://www.ci.friendswood.tx.us/" rel="noopener">City of Friendswood</a> with permit questions. Many Friendswood neighborhoods have homeowners associations, which may have rules about roofing materials and colors, so check yours before choosing a new roof.</p>
    </div>
    <aside class="side-card" data-reveal aria-labelledby="area-card-heading">
      <h2 id="area-card-heading" class="h3">At a glance</h2>
      <dl class="facts">
        <dt>City served</dt><dd><?= e(implode(', ', $cities)) ?>, Texas</dd>
        <dt>Counties</dt><dd>Galveston and Harris</dd>
        <dt>Region</dt><dd>Upper Texas Gulf Coast, southeast of Houston</dd>
        <dt>Official weather source</dt><dd><a href="https://www.weather.gov/hgx/" rel="noopener">NWS Houston/Galveston</a></dd>
      </dl>
      <a class="btn btn-accent btn-block" href="/contact/#estimate-form">Request an Estimate</a>
      <a class="btn btn-outline btn-block" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span><?= e(phone_display()) ?></span></a>
    </aside>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head" data-reveal>
      <h2>Roofing services available in Friendswood</h2>
    </div>
    <?php partial('service-cards'); ?>
  </div>
</section>

<section class="section">
  <div class="container narrow prose" data-reveal>
    <h2>Local roofing guides</h2>
    <ul class="link-list">
      <?php foreach (articles() as $a): ?>
      <li><a href="<?= e($a['url']) ?>"><?= e($a['title']) ?></a></li>
      <?php endforeach; ?>
    </ul>
  </div>
</section>

<?php partial('cta-band', ['title' => 'Live in Friendswood?', 'text' => 'Send your address or ZIP code with an estimate request, or call, and we will take it from there.']); ?>
