<?php defined('BO') || exit; ?>
<div class="tool-wrap" data-tool="arrow-speed">
  <div class="panel reveal">
    <h2>Your setup</h2>
    <div class="field">
      <label for="as-preset">Start from a bow we&rsquo;ve reviewed (optional)</label>
      <select id="as-preset">
        <option value="">Custom bow</option>
        <option value="348">Mathews Lift 29.5 (348 fps IBO)</option>
        <option value="340">Bear Persist (340 fps IBO)</option>
        <option value="339">Bear Whitetail Maxx RTH (339 fps IBO)</option>
        <option value="335">Bear Alaskan XT RTH (335 fps IBO)</option>
        <option value="335">PSE Evolve 28 (335 fps IBO)</option>
        <option value="346">Mathews Prima (346 fps IBO spec)</option>
      </select>
    </div>
    <div class="field">
      <label for="as-ibo">Bow IBO / ATA speed rating <output id="as-ibo-out">335 fps</output></label>
      <input type="range" id="as-ibo" min="250" max="370" step="1" value="335">
    </div>
    <div class="field">
      <label for="as-dl">Your draw length <output id="as-dl-out">28 in</output></label>
      <input type="range" id="as-dl" min="22" max="32" step="0.5" value="28">
    </div>
    <div class="field">
      <label for="as-dw">Your peak draw weight <output id="as-dw-out">65 lb</output></label>
      <input type="range" id="as-dw" min="30" max="80" step="1" value="65">
    </div>
    <div class="field">
      <label for="as-aw">Total arrow weight <output id="as-aw-out">425 gr</output></label>
      <input type="range" id="as-aw" min="300" max="700" step="5" value="425">
      <p class="hint">Shaft + insert + point + nock + fletching. Most hunting arrows weigh 400–500 grains.</p>
    </div>
    <div class="field">
      <label for="as-sw">Weight added to the string <output id="as-sw-out">10 gr</output></label>
      <input type="range" id="as-sw" min="0" max="40" step="1" value="10">
      <p class="hint">Peep, D-loop, nock set and silencers. A peep plus D-loop is typically around 10 grains.</p>
    </div>
  </div>
  <div class="result reveal reveal-d2" aria-live="polite">
    <p style="margin:0">Estimated real-world arrow speed</p>
    <div class="big-num"><span id="as-result">286</span><small>fps</small></div>
    <p id="as-note">About <b id="as-loss">49</b> fps below the IBO rating.</p>
    <div class="result-grid">
      <div><b id="as-ke">77</b><span>Kinetic energy (ft-lbs)</span></div>
      <div><b id="as-mo">0.54</b><span>Momentum (slug-ft/s)</span></div>
      <div><b id="as-t20">0.21</b><span>Seconds to 20 yards</span></div>
      <div><b id="as-t40">0.42</b><span>Seconds to 40 yards</span></div>
    </div>
    <h3 style="font-size:1.05rem;margin-top:22px">Where your speed is lost</h3>
    <ul class="game-list" id="as-breakdown"></ul>
  </div>
</div>

<div class="tool-content prose">
  <h2 id="ibo-vs-real">IBO Speed vs. Real-World Speed</h2>
  <p>Every compound bow is sold with an IBO or ATA speed rating. That number is measured at a standard setup: a 30-inch draw length, 70-pound draw weight and a 350-grain arrow, with nothing on the string. Very few hunters shoot that setup, which is why your chronograph almost always reads lower. This Better Outdoors calculator works backward from the IBO rating using common rules of thumb:</p>
  <?= data_table(['Change from IBO setup', 'Typical effect on speed'], [
      ['Each inch of draw length under 30"', 'About −10 fps'],
      ['Each pound of draw weight under 70 lb', 'About −2 fps'],
      ['Each 3 grains of arrow weight over 350 gr', 'About −1 fps'],
      ['Each 3 grains added to the string', 'About −1 fps'],
  ], 'Arrow speed rules of thumb') ?>
  <?= callout('note', 'An estimate, not a chronograph', 'Cam design, let-off and string material change how closely a bow follows these rules. For exact numbers, shoot through a chronograph. For sight tapes, always use measured speed.') ?>
  <h2 id="does-speed-matter">Does Arrow Speed Matter for Hunting?</h2>
  <p>Speed flattens trajectory, which makes misjudged yardage less costly. But speed is not everything: a heavier arrow carries more momentum, penetrates better and is quieter. Most whitetail hunters do well anywhere from 260 to 300 fps with a 400–475 grain arrow. Check what your setup delivers in our <a href="/tools/kinetic-energy-calculator/">kinetic energy calculator</a>, and see how draw length shifts speed in our <?= post_link('2016-pse-draw-length-adjustment', 'draw length adjustment guide') ?>.</p>
  <?= product_grid([
      ['name' => 'Archery Chronograph', 'q' => 'archery chronograph arrow speed', 'icon' => 'fa-gauge-high', 'blurb' => 'Measure true arrow speed to build accurate sight tapes.'],
      ['name' => 'Grain Scale', 'q' => 'grain scale arrow weight', 'icon' => 'fa-scale-balanced', 'blurb' => 'Weigh arrows and broadheads to the grain for consistent flight.'],
      ['name' => 'Hunting Arrows', 'q' => 'carbon hunting arrows 400 spine', 'icon' => 'fa-arrow-right-long', 'blurb' => 'Match spine to your draw weight and length for best flight.'],
  ], 'Measure and tune your speed') ?>
  <?= faq_block([
      'How do I calculate arrow speed from IBO?' => 'Start with the IBO rating, subtract about 10 fps per inch of draw length under 30 inches, about 2 fps per pound under 70 pounds, and about 1 fps for every 3 grains of arrow weight over 350 grains and every 3 grains added to the string.',
      'Why is my arrow slower than the advertised speed?' => 'IBO speed uses a 30-inch draw, 70-pound weight and a light 350-grain arrow with a bare string. Shorter draw lengths, lower weights, heavier arrows and string accessories all reduce speed.',
      'What is a good arrow speed for deer hunting?' => 'Most hunters are well served between about 260 and 300 fps with a 400 to 475 grain arrow. Accuracy and shot placement matter far more than a few extra fps.',
      'Does a heavier arrow lose speed but gain energy?' => 'A heavier arrow is slower, but it usually keeps slightly more kinetic energy and noticeably more momentum, which helps penetration.',
  ], 'faq') ?>
</div>
