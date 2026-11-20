<?php defined('WCA') || exit; partial('partials/tool_head', ['tool' => $tool]); ?>
<div class="wrap tool" data-tool="moving">
  <div class="tool-grid-2">
    <form class="card form" onsubmit="return false">
      <label>New monthly rent ($)<input type="number" data-m="rent" value="1000" min="0" step="10"></label>
      <label>Security deposit<select data-m="dep"><option value="1">1 month's rent</option><option value="0.5">Half month</option><option value="0">None / deposit alternative</option><option value="2">2 months</option></select></label>
      <label>Application fees (per adult)<input type="number" data-m="app" value="45" min="0"></label>
      <label>Adults applying<input type="number" data-m="adults" value="1" min="1" max="6"></label>
      <label>Home size<select data-m="size"><option value="0">Studio</option><option value="1" selected>1 bedroom</option><option value="2">2 bedrooms</option><option value="3">3+ bedrooms</option></select></label>
      <label>How are you moving?<select data-m="how"><option value="diy">DIY rental truck</option><option value="pro">Local movers</option><option value="friends">Friends + my car</option></select></label>
      <label>Distance (miles)<input type="number" data-m="miles" value="10" min="0"></label>
      <label class="check"><input type="checkbox" data-m="pet"> Moving with a pet (deposit/fee)</label>
      <label class="check"><input type="checkbox" data-m="overlap" checked> Pay overlapping rent on old place (half month)</label>
    </form>
    <div class="card result-card">
      <p class="muted small">Estimated cash needed to move</p>
      <p class="big" data-m-total>$0</p>
      <ul class="breakdown" data-m-list></ul>
      <p class="small muted">Rough estimates for the Dayton area; get real quotes before you budget.</p>
    </div>
  </div>
</div>
<?php partial('partials/tool_foot', compact('tools', 'slug', 'all') + ['products' => [
  ['name' => 'Moving boxes kit', 'query' => 'moving boxes kit with packing supplies', 'icon' => '📦', 'why' => 'Boxes, tape and markers in one order.'],
  ['name' => 'Furniture sliders', 'query' => 'furniture sliders for carpet and hardwood', 'icon' => '🛷', 'why' => 'Move heavy pieces without scratches.'],
  ['name' => 'Moving straps', 'query' => 'forearm forklift lifting straps', 'icon' => '💪', 'why' => 'Carry big items safely.'],
  ['name' => 'Mattress bag', 'query' => 'mattress bag for moving', 'icon' => '🛏️', 'why' => 'Keeps your bed clean in the truck.'],
]]); ?>
