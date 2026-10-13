<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/tool.php';
$faqs = [
    ['Why do I need a home inventory for an insurance claim?', '<p>Contents (personal property) claims are paid item by item. After a fire, flood or hurricane, most people can remember only a fraction of what they owned. An inventory made before a loss—or rebuilt carefully after one—directly increases what you can document and recover.</p>'],
    ['Is my inventory saved?', '<p>Your list is stored only in this browser on this device. Nothing is sent to us unless you choose to share it. Export a CSV regularly and keep a copy in cloud storage or email it to yourself.</p>'],
    ['What should I include?', '<p>Item, room, quantity, approximate age, what it would cost to replace today, and brand/model where you know it. Photos or video of each room are the best supporting evidence.</p>'],
];
tool_start('home-inventory-checklist', 'Home Inventory Builder',
    'Home Inventory Checklist & Builder for Insurance Claims | Sugar Land Public Adjuster',
    'Build a room-by-room home inventory for your insurance claim and export it to a spreadsheet. Free, private tool from a Sugar Land public adjuster.',
    'Home Inventory Builder for Insurance Claims',
    'List your belongings room by room, total the replacement cost, and export a spreadsheet you can send with your contents claim. Everything stays in your browser.', $faqs);
?>
<form class="tool" id="inventory" onsubmit="return false">
  <h2>Add items</h2>
  <div class="tool-grid">
    <label>Room
      <select name="room">
        <option>Living room</option><option>Kitchen</option><option>Dining room</option><option>Primary bedroom</option><option>Bedroom 2</option><option>Bedroom 3</option><option>Bathrooms</option><option>Home office</option><option>Laundry</option><option>Garage</option><option>Patio / outdoor</option><option>Closets</option><option>Attic / storage</option>
      </select>
    </label>
    <label>Item<input type="text" name="item" maxlength="120" placeholder="e.g. 65&quot; Samsung TV" list="inv-suggest"></label>
    <label>Quantity<input type="number" name="qty" min="1" step="1" value="1" inputmode="numeric"></label>
    <label>Age (years)<input type="number" name="age" min="0" step="0.5" value="" inputmode="decimal"></label>
    <label>Replacement cost (each) <span class="money"><input type="number" name="cost" min="0" step="10" inputmode="decimal"></span></label>
    <label>Brand / model / notes<input type="text" name="notes" maxlength="160"></label>
  </div>
  <datalist id="inv-suggest"></datalist>
  <div class="tool-actions">
    <button type="button" class="btn btn-primary" data-add>Add item</button>
    <button type="button" class="btn btn-outline" data-suggest>Show common items for this room</button>
  </div>
  <p class="small muted" data-suggest-list></p>
  <div class="tool-results" aria-live="polite">
    <div class="result-grid">
      <div class="result"><span>Items</span><strong data-out="count">0</strong></div>
      <div class="result hl"><span>Total replacement cost</span><strong data-out="total">$0</strong></div>
      <div class="result"><span>Rooms covered</span><strong data-out="rooms">0</strong></div>
    </div>
  </div>
  <div class="table-wrap mt-2">
    <table class="inv-table">
      <thead><tr><th>Room</th><th>Item</th><th>Qty</th><th>Age</th><th>Each</th><th>Total</th><th>Notes</th><th></th></tr></thead>
      <tbody data-list><tr><td colspan="8" class="muted">No items yet.</td></tr></tbody>
    </table>
  </div>
  <div class="tool-actions">
    <button type="button" class="btn btn-primary" data-csv>Download CSV / Excel</button>
    <button type="button" class="btn btn-outline" onclick="window.print()">Print</button>
    <button type="button" class="btn btn-outline" data-clear>Clear list</button>
  </div>
</form>
<section class="prose mt-2">
  <h2>Tips for a stronger contents claim</h2>
  <ul class="checklist">
    <li>Walk every room with your phone recording video—open closets, drawers and cabinets.</li>
    <li>Photograph serial numbers on electronics and appliances.</li>
    <li>Search your email and card statements for purchase receipts.</li>
    <li>Don’t forget the garage, attic, outdoor furniture, tools, food and cleaning supplies.</li>
    <li>Keep damaged items until the insurer (or your public adjuster) has documented them.</li>
  </ul>
  <p>Contents claims after a <a href="/services/fire-smoke-damage-claims/">fire</a> or <a href="/services/flood-damage-claims/">flood</a> often run to hundreds of line items. A public adjuster in Sugar Land can build and price the full inventory for you.</p>
</section>
<?php tool_end($faqs); ?>
