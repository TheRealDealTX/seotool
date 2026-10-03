<?php
/** Storm Event Lookup — search reports near a city or ZIP code. */
require_once MPA_ROOT . '/includes/storms.php';
$places = read_json_file(data_path('places.json'), ['places' => [], 'zips' => []]);
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section" aria-labelledby="lookup-h">
  <div class="container" data-storm-app="lookup" data-api="/api/storms.php?set=all">
    <script type="application/json" data-places><?= json_encode($places, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
    <div class="tool-layout">
      <div class="tool-panel">
        <h2 id="lookup-h">Find storm reports near a property</h2>
        <form data-lookup onsubmit="return false" novalidate>
          <div class="form-grid">
            <div class="field field-full"><label for="l-where">City or ZIP code <span class="req" aria-hidden="true">*</span></label>
              <input id="l-where" name="where" type="text" list="l-places" required placeholder="e.g. McAllen or 78504" autocomplete="off">
              <datalist id="l-places"><?php foreach ($places['places'] as $p): ?><option value="<?= e($p['name']) ?>"><?php endforeach; foreach ($places['zips'] as $z): ?><option value="<?= e($z['zip']) ?>"><?php endforeach; ?></datalist>
              <span class="field-hint">Hidalgo County cities and ZIP codes. We do not ask for or store street addresses.</span></div>
            <div class="field"><label for="l-radius">Search radius</label><select id="l-radius" name="radius"><option value="3">3 miles</option><option value="5" selected>5 miles</option><option value="10">10 miles</option><option value="20">20 miles</option></select></div>
            <div class="field"><label for="l-type">Event type</label><select id="l-type" name="fam"><option value="">Hail, wind &amp; more</option><option value="hail">Hail</option><option value="wind">Wind</option><option value="tornado">Tornado</option><option value="flood">Flood &amp; heavy rain</option><option value="tropical">Tropical</option><option value="winter">Freeze &amp; winter</option></select></div>
            <div class="field"><label for="l-date">Approximate date <span class="opt">(optional)</span></label><input id="l-date" name="date" type="date"></div>
            <div class="field"><label for="l-window">Date window</label><select id="l-window" name="window"><option value="3">&plusmn; 3 days</option><option value="7" selected>&plusmn; 7 days</option><option value="30">&plusmn; 30 days</option><option value="365">&plusmn; 1 year</option></select></div>
            <div class="field"><label for="l-from">Or date range: from</label><input id="l-from" name="from" type="date"></div>
            <div class="field"><label for="l-to">to</label><input id="l-to" name="to" type="date"></div>
          </div>
          <button class="btn btn-gold btn-block" type="submit">Search storm reports</button>
          <p class="form-status" data-lookup-status role="status" aria-live="polite"></p>
        </form>
      </div>
      <div class="tool-panel" aria-live="polite">
        <h2>Results</h2>
        <div data-lookup-results><p class="muted">Enter a city or ZIP code to search NOAA and National Weather Service storm reports. Zone- or county-wide events (such as tropical storms and freezes) are included when the date matches.</p></div>
      </div>
    </div>
    <div class="storm-map" data-map style="margin-top:28px" aria-label="Map of matching storm reports"></div>
    <p class="disclaimer-box"><strong>Nearby does not mean damaged.</strong> Results show official reports near the location you entered. They do not show that a storm damaged any particular building, and storms often affect areas where no one filed a report. Distances are measured from the center of the city or ZIP code, not from a specific address. Use these records as supporting documentation together with a professional inspection.</p>
  </div>
</section>
<section class="section section-alt section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php component('cta-storm'); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
