<?php
return [
    'title'       => 'Insurance Claim Documentation Checklist (Printable)',
    'description' => 'Interactive checklist of what to photograph, save and request for a Texas hail, wind, water, fire or hurricane claim. Saves your progress and prints cleanly.',
    'h1'          => 'Claim documentation checklist',
    'lead'        => 'The claims that get paid fairly are the well-documented ones. Pick your type of loss and work through the list. Your progress saves in this browser, and the list prints cleanly for your claim file.',
    'updated'     => '2026-10-13',
    'script'      => '/assets/js/tools/checklist.js',
    'app'         => <<<'HTML'
<div data-cl>
  <div class="cl-head">
    <div class="ring" data-ring style="--v:0"><span data-out="pct">0%</span></div>
    <div>
      <p class="tlabel" style="margin-bottom:.4rem">What kind of damage?</p>
      <div class="seg" data-seg="loss" style="margin:0">
        <button type="button" class="is-on" data-v="roof">Hail &amp; wind</button>
        <button type="button" data-v="water">Water</button>
        <button type="button" data-v="fire">Fire &amp; smoke</button>
        <button type="button" data-v="storm">Hurricane &amp; flood</button>
      </div>
    </div>
  </div>
  <div data-out="sections"></div>
  <div class="tbtns">
    <button type="button" class="btn btn--primary btn--sm" data-act="print">Print checklist</button>
    <button type="button" class="btn btn--ghost btn--sm" data-act="reset">Reset this list</button>
  </div>
</div>
HTML,
    'body'        => <<<'HTML'
<h2>Why documentation decides claims</h2>
<p>An insurance adjuster can only pay for what is documented and tied to a covered cause of loss. When a claim comes back short, it's usually because something wasn't recorded before it was cleaned up, thrown away or repaired, or because there's no evidence linking the damage to a specific storm date. This checklist covers both.</p>
<h2>Three habits that matter more than any single photo</h2>
<ol class="steps">
  <li><strong>Document before you change anything.</strong> Photograph and video every room and roof slope before mitigation, tear-out or debris removal. Emergency repairs to prevent more damage are expected, but record the condition first.</li>
  <li><strong>Put everything in writing.</strong> Follow every phone call with an email summary. Written requests also start the Texas prompt payment clocks; see the <a href="/tools/texas-claim-deadline-calculator/">deadline calculator</a>.</li>
  <li><strong>Keep one claim file.</strong> One folder (paper or cloud) for the policy, the estimate, letters, receipts and photos, organized by date. Our guide to <a href="/post/how-to-document-damage-for-your-claim/">documenting damage</a> walks through the method.</li>
</ol>
[[tool:contents-inventory-builder]]
HTML,
    'faqs' => [
        ['q' => 'Where is my progress saved?', 'a' => 'Only in this browser, using local storage. Nothing is sent to us. Clearing your browser data or switching devices starts a fresh list.'],
        ['q' => 'Should I throw away damaged items after I photograph them?', 'a' => 'Not until the insurer says it doesn\'t need to inspect them. Keep samples of damaged flooring, carpet and roofing where you can, and photograph serial numbers and labels.'],
        ['q' => 'Do I need receipts for everything?', 'a' => 'No. Receipts help, but photos, bank statements, manuals and online order histories also prove ownership and value. Start with the high-value items.'],
    ],
    'related' => ['/post/how-to-document-damage-for-your-claim/', '/tools/contents-inventory-builder/', '/post/common-property-insurance-claims-mistakes/'],
];
