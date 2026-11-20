<?php defined('WCA') || exit; partial('partials/tool_head', ['tool' => $tool]); ?>
<div class="wrap tool narrow" data-tool="checklist">
  <div class="card">
    <div class="progress big-progress"><i data-cl-progress></i></div>
    <p><strong data-cl-count>0</strong> of <span data-cl-total>0</span> done · <button type="button" class="linklike" data-cl-reset>Reset</button> · <button type="button" class="linklike" onclick="window.print()">Print</button></p>
    <div data-cl-list></div>
  </div>
</div>
<?php partial('partials/tool_foot', compact('tools', 'slug', 'all') + ['products' => [
  ['name' => 'Moving boxes kit', 'query' => 'moving boxes kit with packing supplies', 'icon' => '📦', 'why' => 'Start packing early.'],
  ['name' => 'Packing paper', 'query' => 'packing paper sheets', 'icon' => '📰', 'why' => 'Protect dishes and frames.'],
  ['name' => 'Color-coded moving labels', 'query' => 'color coded moving labels', 'icon' => '🏷️', 'why' => 'Unpack room by room.'],
  ['name' => 'Cleaning caddy kit', 'query' => 'cleaning supplies caddy kit', 'icon' => '🧽', 'why' => 'Move-out clean = deposit back.'],
]]); ?>
