<?php
return [
    'title'       => 'Contents Inventory Builder for Insurance Claims',
    'description' => 'Free room-by-room personal property inventory for fire, water and storm claims. Add items, ages and prices, estimate depreciation and export to CSV.',
    'h1'          => 'Contents inventory builder',
    'lead'        => 'After a fire or major water loss, you, not the insurer, have to list what was damaged. Build the list room by room here, then export it as a spreadsheet for your claim. It saves automatically in this browser.',
    'updated'     => '2026-10-13',
    'script'      => '/assets/js/tools/inventory.js',
    'app'         => <<<'HTML'
<div data-inv>
  <div class="cl-head" style="justify-content:space-between">
    <div>
      <p class="tlabel" style="margin-bottom:.4rem">Add a room</p>
      <div class="chips" style="margin:0" data-rooms>
        <button type="button" class="chip">Living room</button><button type="button" class="chip">Kitchen</button><button type="button" class="chip">Primary bedroom</button><button type="button" class="chip">Bedroom 2</button><button type="button" class="chip">Bathroom</button><button type="button" class="chip">Garage</button><button type="button" class="chip">Office</button><button type="button" class="chip">Closets</button>
      </div>
    </div>
  </div>
  <div class="table-wrap">
    <table class="inv-table">
      <thead><tr><th>Room</th><th>Item</th><th>Brand / model / notes</th><th>Category</th><th>Qty</th><th>Age (yrs)</th><th>Replacement cost (each)</th><th></th></tr></thead>
      <tbody data-rows></tbody>
    </table>
  </div>
  <div class="tbtns">
    <button type="button" class="btn btn--ghost btn--sm" data-act="add">+ Add item</button>
    <button type="button" class="btn btn--primary btn--sm" data-act="csv">Export CSV</button>
    <button type="button" class="btn btn--ghost btn--sm" data-act="print">Print</button>
    <button type="button" class="btn btn--ghost btn--sm" data-act="clear">Clear all</button>
  </div>
  <div class="inv-totals">
    <div><span data-out="count">0</span><p>items</p></div>
    <div><span data-out="rcv">$0</span><p>replacement cost</p></div>
    <div><span data-out="acv">$0</span><p>rough depreciated value (ACV)</p></div>
    <div><span data-out="rooms">0</span><p>rooms</p></div>
  </div>
  <p class="muted" style="margin-top:1rem">Depreciation uses rough useful-life assumptions by category (electronics 5 years, clothing 4, furniture 12, appliances 12, tools 15, decor 15, other 10) with a 20% floor. Insurers use their own tables. On a replacement cost policy, withheld depreciation is usually recoverable once items are replaced.</p>
</div>
HTML,
    'body'        => <<<'HTML'
<h2>How to build a contents list insurers accept</h2>
<p>Contents (personal property) claims are where fire and water claims lose the most money, because the burden is on you to list each item. Insurers rarely accept "living room furniture: $8,000." They want each item, its age and its replacement cost.</p>
<ol class="steps">
  <li><strong>Go room by room, then wall by wall.</strong> Start at the door and work clockwise: walls, then furniture, then drawers and closets. Don't forget the garage, attic and outdoor items.</li>
  <li><strong>Use your phone's photo history.</strong> Old photos, videos and social media posts show what was in each room. Online order histories and bank statements prove purchases and prices.</li>
  <li><strong>Price at today's replacement cost.</strong> Use a current listing for a like-kind item, not what you paid years ago. Note the link or store in the notes column.</li>
  <li><strong>Be realistic about age.</strong> Age drives depreciation, and honest ages make the whole list more credible.</li>
  <li><strong>Export and send it in batches.</strong> Large losses can run to thousands of lines. Send the inventory in batches so payments can start before you finish.</li>
</ol>
<div class="callout callout--tip"><p><strong>Tip:</strong> photograph damaged items and keep them until the insurer confirms it doesn't need to inspect them. Serial numbers on electronics and appliances are especially useful.</p></div>
<p>Facing a large fire loss? See our guides on <a href="/post/fire-damage-insurance/">fire damage insurance</a> and <a href="/post/house-fire-debris-removal-cost/">debris removal costs</a>, or <a href="/services/fire-smoke-damage-claims/">how we handle fire and smoke claims</a>.</p>
HTML,
    'faqs' => [
        ['q' => 'Is my inventory saved or sent anywhere?', 'a' => 'It saves automatically in this browser only. Nothing is uploaded. Export a CSV regularly as a backup, because clearing your browser data deletes the list.'],
        ['q' => 'Can I open the export in Excel or Google Sheets?', 'a' => 'Yes. The CSV opens in Excel, Google Sheets and Numbers, and most insurers accept spreadsheet inventories.'],
        ['q' => 'What if I cannot remember everything?', 'a' => 'Almost nobody can at first. Start with large and expensive items, then add more as photos and memories surface. You can keep adding items to a contents claim as you go.'],
    ],
    'related' => ['/post/fire-damage-insurance/', '/services/fire-smoke-damage-claims/', '/tools/claim-documentation-checklist/'],
];
