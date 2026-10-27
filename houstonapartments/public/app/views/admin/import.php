<?php
defined('HA_ROOT') || exit;
$title = 'Import from Rise';
?>
<div class="grid-2">
  <section class="card">
    <h2>Import specific properties</h2>
    <p class="muted">Paste riseapartments.com property links (or their slugs), one per line. Each one takes about 15–20 seconds while photos are copied.</p>
    <textarea id="import-list" rows="6" placeholder="https://riseapartments.com/apartment/camden-heights/&#10;1810-main"></textarea>
    <label class="inline"><input type="checkbox" id="import-force"> Overwrite listings that were edited here</label>
    <button class="btn primary" type="button" data-import-list>Import</button>
  </section>
  <section class="card">
    <h2>Sync new &amp; updated listings</h2>
    <p class="muted">Checks Rise for Houston listings that are new or changed since the last import and brings them in (a few at a time – keep this page open). Listings edited in this admin are skipped.</p>
    <p>Rise listings here: <strong><?= number_format((int) ($counts['total'] ?? 0)) ?></strong> · edited here: <strong><?= number_format((int) ($counts['locked'] ?? 0)) ?></strong><br>
      <small class="muted">Last import: <?= $last ? e(date('M j, Y g:ia', strtotime($last))) : 'never' ?></small></p>
    <button class="btn primary" type="button" data-sync>Start sync</button> <button class="btn ghost" type="button" data-sync-stop hidden>Stop</button>
  </section>
</div>
<section class="card"><h2>Progress</h2><pre class="log" id="import-log">Nothing running.</pre></section>
