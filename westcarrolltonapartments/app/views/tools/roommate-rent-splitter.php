<?php defined('WCA') || exit; partial('partials/tool_head', ['tool' => $tool]); ?>
<div class="wrap tool" data-tool="split">
  <div class="card form">
    <div class="grid-3">
      <label>Total monthly rent ($)<input type="number" data-s="rent" value="1400" min="0" step="10"></label>
      <label>Shared utilities ($/mo)<input type="number" data-s="util" value="180" min="0" step="5"></label>
      <label>Split method
        <select data-s="method"><option value="fair">Fair (room size + perks)</option><option value="size">By room size only</option><option value="equal">Equal</option></select></label>
    </div>
    <div class="table-scroll">
    <table class="split-table">
      <thead><tr><th>Roommate</th><th>Bedroom sq ft</th><th>Private bath</th><th>Parking spot</th><th>Rent share</th><th>+ Utilities</th><th>Total</th></tr></thead>
      <tbody data-s-rows></tbody>
    </table>
    </div>
    <p><button type="button" class="btn btn-ghost btn-sm" data-s-add>+ Add roommate</button></p>
    <p class="small muted">"Fair" weights 60% by bedroom size (shared space split equally), adds a 10% premium for a private bath and a flat $25 for parking, then normalizes to the total rent.</p>
  </div>
</div>
<?php partial('partials/tool_foot', compact('tools', 'slug', 'all') + ['products' => [
  ['name' => 'Label maker', 'query' => 'label maker', 'icon' => '🏷️', 'why' => 'Keep shared shelves sorted.'],
  ['name' => 'Fridge organizer bins', 'query' => 'fridge organizer bins', 'icon' => '🧊', 'why' => 'Everyone gets their own shelf.'],
  ['name' => 'Chore chart whiteboard', 'query' => 'magnetic chore chart whiteboard', 'icon' => '📋', 'why' => 'Fewer arguments about dishes.'],
  ['name' => 'Door draft stopper', 'query' => 'door draft stopper', 'icon' => '🚪', 'why' => 'Privacy and quieter rooms.'],
]]); ?>
