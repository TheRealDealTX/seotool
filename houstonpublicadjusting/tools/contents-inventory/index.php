<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'contents-inventory',
    'title' => 'Home Contents Inventory Builder for Insurance Claims (Free)',
    'desc' => 'Build a room-by-room personal property inventory for your insurance claim. Totals automatically, saves in your browser, prints or exports to CSV. Free from Houston Public Adjusters.',
    'h1' => 'Contents Inventory Builder',
    'lede' => 'Contents are the most under-claimed part of most property claims. List damaged belongings room by room &mdash; the list saves in your browser so you can come back to it.',
    'form' => '
<div class="table-wrap"><table class="inv-table" id="inventory">
  <thead><tr><th>Room</th><th>Item &amp; description</th><th>Qty</th><th>Age (yrs)</th><th>Cost each ($)</th><th>Total</th><th></th></tr></thead>
  <tbody></tbody>
  <tfoot><tr><th colspan="5" style="text-align:right">Inventory total</th><th id="inv-total">$0</th><th></th></tr></tfoot>
</table></div>
<div class="inv-actions no-print">
  <button class="btn btn-dark" type="button" id="inv-add">+ Add item</button>
  <button class="btn btn-outline" type="button" id="inv-csv">Download CSV</button>
  <button class="btn btn-outline" type="button" id="inv-print">Print</button>
  <button class="btn btn-outline" type="button" id="inv-clear">Clear all</button>
</div>',
    'prose' => '
<h2>How to build a contents inventory insurers accept</h2>
<p>Your insurer needs to know what was damaged, how many, how old and what it costs to replace today. Go room by room, including closets, the garage, the attic and outdoor items. Brand, model and size matter: a 65-inch OLED TV and a 32-inch LCD are not the same line item.</p>
<ul class="checklist">
  <li>Start with photos and video of every room, then fill in the list from them</li>
  <li>Use current replacement prices from major retailers, not what you originally paid</li>
  <li>Include small items in bulk (&ldquo;kitchen utensils &ndash; 40 pieces&rdquo;) &mdash; they add up</li>
  <li>Don&rsquo;t throw away damaged items until the adjuster has documented them</li>
  <li>Group by room so the adjuster can match the list to the photos</li>
</ul>
<p>For large losses such as fire or flood, a full contents inventory can run to thousands of lines. Houston Public Adjusters handle that work for our clients.</p>',
    'faqs' => [
        ['Is my inventory saved?', 'Yes, in this browser only. Nothing is uploaded. Download the CSV to keep a copy or share it with your adjuster.'],
        ['Do I need receipts for every item?', 'No. Receipts help, but photos, bank and card statements, manuals, and online order history are all accepted ways to prove ownership.'],
    ],
]);
