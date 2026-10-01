<?php
/*
 * Live RainViewer radar embed centered on Friendswood, TX.
 * RainViewer's terms allow embedding its live radar maps provided the
 * RainViewer watermark/source is not hidden or distorted. See README.
 */
$geo  = config('geo');
$zoom = (int) config('weather.zoom', 8);
$loc  = sprintf('%.4f,%.4f,%d', $geo['lat'], $geo['lng'], $zoom);
$src  = 'https://www.rainviewer.com/map.html?loc=' . $loc . '&oFa=0&oC=1&oU=0&oCS=1&oF=0&oAP=1&c=3&o=83&lm=1&layer=radar&sm=1&sn=1';
$external = 'https://www.rainviewer.com/weather-radar-map-live.html?loc=' . $loc;
?>
<figure class="weather-map" data-reveal data-weather>
  <div class="weather-frame">
    <p class="weather-placeholder" data-weather-placeholder>
      <?= icon('map') ?>
      <span>Loading the live radar map&hellip; If it doesn't appear, <a href="<?= e($external) ?>" rel="noopener">open the Friendswood radar on RainViewer</a>.</span>
    </p>
    <iframe
      src="<?= e($src) ?>"
      title="Live weather radar map centered on Friendswood, Texas (RainViewer)"
      width="640" height="480"
      loading="lazy"
      referrerpolicy="strict-origin-when-cross-origin"
      allowfullscreen
      data-weather-frame></iframe>
  </div>
  <figcaption>
    <span>Live radar map provided by <a href="<?= e(config('weather.provider_url')) ?>" rel="noopener">RainViewer</a>. Radar imagery may be delayed and is not an official warning source.</span>
    <a class="weather-ext" href="<?= e($external) ?>" rel="noopener">Open full-screen radar <?= icon('external', 'icon icon-sm') ?></a>
  </figcaption>
</figure>
