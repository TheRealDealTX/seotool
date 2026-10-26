<?php defined('BO') || exit; ?>
<div class="tool-wrap" data-tool="ke">
  <div class="panel reveal">
    <h2>Arrow details</h2>
    <div class="field">
      <label for="ke-speed">Arrow speed <output id="ke-speed-out">285 fps</output></label>
      <input type="range" id="ke-speed" min="150" max="380" step="1" value="285">
      <p class="hint">Don&rsquo;t know it? Estimate it with the <a href="/tools/arrow-speed-calculator/">arrow speed calculator</a>.</p>
    </div>
    <div class="field">
      <label for="ke-weight">Total arrow weight <output id="ke-weight-out">425 gr</output></label>
      <input type="range" id="ke-weight" min="250" max="750" step="5" value="425">
    </div>
    <div class="field">
      <label for="ke-game">What are you hunting?</label>
      <select id="ke-game">
        <option value="small">Small game (turkey, rabbit, coyote)</option>
        <option value="medium" selected>Medium game (whitetail, antelope)</option>
        <option value="large">Large game (elk, black bear, moose)</option>
        <option value="xl">Toughest game (grizzly, cape buffalo)</option>
      </select>
    </div>
  </div>
  <div class="result reveal reveal-d2" aria-live="polite">
    <p style="margin:0">Kinetic energy</p>
    <div class="big-num"><span id="ke-result">76.7</span><small>ft-lbs</small></div>
    <div class="gauge"><div class="gauge-track"><span class="gauge-needle" id="ke-needle"></span></div><div class="gauge-labels"><span>0</span><span>25</span><span>42</span><span>65</span><span>100+</span></div></div>
    <div class="result-grid">
      <div><b id="ke-mo">0.54</b><span>Momentum (slug-ft/s)</span></div>
      <div><b id="ke-verdict">Ready</b><span id="ke-verdict-l">For medium game</span></div>
    </div>
    <ul class="game-list" id="ke-list">
      <li data-min="0" data-mo="0"><i class="fa-solid fa-circle-check"></i> Small game: under 25 ft-lbs</li>
      <li data-min="25" data-mo="0.3"><i class="fa-solid fa-circle-check"></i> Medium game: 25–41 ft-lbs</li>
      <li data-min="42" data-mo="0.45"><i class="fa-solid fa-circle-check"></i> Large game: 42–65 ft-lbs</li>
      <li data-min="65" data-mo="0.6"><i class="fa-solid fa-circle-check"></i> Toughest game: 65+ ft-lbs</li>
    </ul>
  </div>
</div>

<div class="tool-content prose">
  <h2 id="formulas">Kinetic Energy and Momentum Formulas</h2>
  <p>Kinetic energy (KE) tells you how much work an arrow can do. Momentum tells you how hard it is to stop. The Better Outdoors calculator uses the standard archery formulas:</p>
  <ul>
    <li><strong>Kinetic energy (ft-lbs)</strong> = arrow weight (grains) &times; speed (fps)&sup2; &divide; 450,240</li>
    <li><strong>Momentum (slug-ft/s)</strong> = arrow weight (grains) &times; speed (fps) &divide; 225,218</li>
  </ul>
  <?= data_table(['Game class', 'Typical kinetic energy guideline', 'Examples'], [
      ['Small game', 'Under 25 ft-lbs', 'Rabbit, turkey, coyote'],
      ['Medium game', '25–41 ft-lbs', 'Whitetail, antelope'],
      ['Large game', '42–65 ft-lbs', 'Elk, black bear, wild boar'],
      ['Toughest game', '65+ ft-lbs', 'Grizzly, moose, cape buffalo'],
  ], 'Widely used kinetic energy guidelines by game size') ?>
  <?= callout('warn', 'Shot placement first', 'Energy charts are general guidelines. A sharp broadhead, good arrow flight and a broadside double-lung shot matter far more than a few extra ft-lbs. Always follow your state&rsquo;s minimum equipment rules.') ?>
  <h2 id="ke-vs-momentum">Kinetic Energy vs. Momentum: Which Matters More?</h2>
  <p>Light, fast arrows score high on kinetic energy. Heavy arrows score higher on momentum, and momentum tracks penetration more closely, especially through bone on bigger animals. That is why elk and bear hunters often step up to 475–550 grain arrows even though they lose some speed. Reviewing a new bow? Compare real setups in our <?= post_link('bear-archery-alaskan-xt-rth-compound-bow', 'Bear Alaskan XT review') ?> and <?= post_link('mathews-lift-29-5', 'Mathews Lift 29.5 review') ?>.</p>
  <?= product_grid([
      ['name' => 'Fixed-Blade Broadheads', 'q' => 'fixed blade broadheads 100 grain', 'icon' => 'fa-location-arrow', 'blurb' => 'Durable, reliable penetration for whitetail and elk.'],
      ['name' => 'Heavy Hunting Arrows', 'q' => 'heavy hunting arrows elk', 'icon' => 'fa-arrow-right-long', 'blurb' => 'More grains per inch for extra momentum on big game.'],
      ['name' => 'Brass Inserts', 'q' => 'brass arrow inserts weight forward', 'icon' => 'fa-weight-hanging', 'blurb' => 'Add front-of-center weight to boost momentum and stability.'],
  ], 'Build a harder-hitting arrow') ?>
  <?= faq_block([
      'How much kinetic energy do I need to kill a deer with a bow?' => 'A common guideline for whitetail is 25 to 41 ft-lbs of kinetic energy, with most modern compound setups producing well over 50 ft-lbs. Shot placement and a sharp broadhead matter most.',
      'How do you calculate arrow kinetic energy?' => 'Multiply arrow weight in grains by arrow speed in feet per second squared, then divide by 450,240. A 425 grain arrow at 285 fps produces about 76.7 ft-lbs.',
      'What is good arrow momentum for elk?' => 'Many elk hunters aim for roughly 0.5 slug-ft/s or more, typically from a 450 to 550 grain arrow, to improve penetration through heavy muscle and bone.',
      'Is a heavier arrow better for hunting?' => 'For bigger game, usually yes. Heavier arrows are slower but carry more momentum, are quieter and often penetrate deeper. For long-range target shooting, lighter arrows give a flatter trajectory.',
  ], 'faq') ?>
</div>
