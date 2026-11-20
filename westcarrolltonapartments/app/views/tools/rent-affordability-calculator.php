<?php defined('WCA') || exit; partial('partials/tool_head', ['tool' => $tool]); ?>
<div class="wrap tool" data-tool="afford">
  <div class="tool-grid-2">
    <form class="card form" onsubmit="return false">
      <label>Income type
        <select data-i="period"><option value="year">Annual gross (before taxes)</option><option value="hour">Hourly wage</option><option value="month">Monthly gross</option></select></label>
      <label><span data-i-label>Annual gross income ($)</span><input type="number" data-i="income" value="45000" min="0" step="500"></label>
      <label data-hours hidden>Hours per week<input type="number" data-i="hours" value="40" min="1" max="80"></label>
      <label>Monthly debt payments (car, cards, loans) ($)<input type="number" data-i="debt" value="250" min="0" step="10"></label>
      <label>Household members sharing rent<input type="range" data-i="people" min="1" max="4" value="1"><output data-out-people>1</output></label>
    </form>
    <div class="card result-card">
      <p class="muted small">Comfortable rent budget</p>
      <p class="big" data-r="main">$0</p>
      <div class="bars">
        <div><span>30% rule</span><div class="bar"><i data-bar="r30"></i></div><b data-r="r30"></b></div>
        <div><span>50/30/20 needs (housing ~70%)</span><div class="bar"><i data-bar="r5030"></i></div><b data-r="r5030"></b></div>
        <div><span>Landlord 3× income test</span><div class="bar"><i data-bar="r3x"></i></div><b data-r="r3x"></b></div>
      </div>
      <p class="small muted" data-r="note"></p>
    </div>
  </div>
  <div class="section-tight">
    <h2>West Carrollton communities in your budget</h2>
    <div class="card-grid" data-matches></div>
  </div>
</div>
<?php partial('partials/tool_foot', compact('tools', 'slug', 'all') + ['products' => [
  ['name' => 'Budget planner notebook', 'query' => 'monthly budget planner', 'icon' => '📒', 'why' => 'Track rent and bills by hand.'],
  ['name' => 'Smart thermostat-friendly window film', 'query' => 'window insulation film kit', 'icon' => '🪟', 'why' => 'Cut winter heating bills.'],
  ['name' => 'LED bulb multipack', 'query' => 'led light bulbs 60w equivalent pack', 'icon' => '💡', 'why' => 'Lower your electric bill.'],
  ['name' => 'Smart power strip', 'query' => 'smart power strip', 'icon' => '🔌', 'why' => 'Stop phantom power drain.'],
]]); ?>
