<?php
// Shared sidebar for the city pages. Included by pages/areas/<city>.php.
$here = $GLOBALS['path'];
?>
<aside class="sidebar">
  <div class="side-box side-box--cta">
    <h2>Free Design Consult</h2>
    <p>Tell Cowboy Tiny Homes your address, budget and what you want to build. We will check what your lot allows and map out next steps.</p>
    <a class="btn btn--gold" href="/contact-us/">Start My Project</a>
    <a class="btn btn--ghost" href="<?= PHONE_HREF ?>">Call <?= PHONE ?></a>
  </div>
  <div class="side-box">
    <h2>Other Texas Service Areas</h2>
    <ul>
<?php foreach (SERVICE_CITIES as $slug => $city):
        $p = '/tiny-home-builders-' . $slug . '/';
        if ($p === $here) continue; ?>
      <li><a href="<?= $p ?>">Tiny Home Builders <?= $city ?></a></li>
<?php endforeach; ?>
      <li><a href="/service-areas/">All Service Areas</a></li>
    </ul>
  </div>
  <div class="side-box">
    <h2>What We Build</h2>
    <ul>
      <li><a href="/custom-tiny-homes-texas/">Custom Tiny Homes</a></li>
      <li><a href="/adu-builders-texas/">ADUs, Casitas &amp; Granny Flats</a></li>
      <li><a href="/tiny-homes-on-wheels-texas/">Tiny Homes on Wheels</a></li>
      <li><a href="/park-model-homes-texas/">Park Model Homes</a></li>
      <li><a href="/tiny-house-design-services/">Design Services</a></li>
    </ul>
  </div>
  <div class="side-box">
    <h2>Plan Ahead</h2>
    <ul>
      <li><a href="/tools/tiny-home-cost-calculator/">Tiny Home Cost Calculator</a></li>
      <li><a href="/tools/adu-rental-income-calculator/">ADU Rental Income Calculator</a></li>
      <li><a href="/guides/tiny-house-laws-texas/">Texas Tiny House Laws</a></li>
    </ul>
  </div>
</aside>
