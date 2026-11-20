<?php defined('WCA') || exit; partial('partials/tool_head', ['tool' => $tool]); ?>
<div class="wrap tool" data-tool="planner">
  <div class="planner-wrap">
    <div class="card planner-controls form">
      <div class="grid-2">
        <label>Room width (ft)<input type="number" data-p="w" value="12" min="6" max="40"></label>
        <label>Room length (ft)<input type="number" data-p="h" value="14" min="6" max="40"></label>
      </div>
      <p class="small"><strong>Add furniture</strong> (click), then drag. Double-click (or double-tap) to rotate, select + Delete to remove.</p>
      <div class="palette" data-p-palette></div>
      <p><button type="button" class="btn btn-ghost btn-sm" data-p-del>Delete selected</button> <button type="button" class="btn btn-ghost btn-sm" data-p-rot>Rotate selected</button> <button type="button" class="btn btn-ghost btn-sm" data-p-clear>Clear room</button></p>
      <p class="small muted">1 grid square = 1 ft. Your layout is saved in this browser.</p>
    </div>
    <div class="planner-stage card"><div class="room" data-p-room></div></div>
  </div>
</div>
<?php partial('partials/tool_foot', compact('tools', 'slug', 'all') + ['productsHeading' => 'Small-space furniture ideas', 'products' => [
  ['name' => 'Sleeper sofa', 'query' => 'sleeper sofa small space', 'icon' => '🛋️', 'why' => 'A guest bed that hides away.'],
  ['name' => 'Drop-leaf dining table', 'query' => 'drop leaf dining table small', 'icon' => '🍽️', 'why' => 'Folds down when not in use.'],
  ['name' => 'Storage bed frame', 'query' => 'platform bed frame with storage drawers', 'icon' => '🛏️', 'why' => 'Drawers instead of a dresser.'],
  ['name' => 'Wall-mounted desk', 'query' => 'wall mounted folding desk', 'icon' => '🖥️', 'why' => 'A home office in 2 square feet.'],
]]); ?>
