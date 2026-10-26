<?php defined('BO') || exit; ?>
<div class="tool-wrap" data-tool="draw-length">
  <div class="panel reveal">
    <h2>Measure yourself</h2>
    <div class="seg" role="tablist" aria-label="Measurement method">
      <button type="button" class="on" data-mode="wingspan" role="tab" aria-selected="true">Wingspan</button>
      <button type="button" data-mode="height" role="tab" aria-selected="false">Height</button>
    </div>
    <div class="field">
      <label for="dl-unit">Units</label>
      <select id="dl-unit"><option value="in">Inches</option><option value="cm">Centimeters</option></select>
    </div>
    <div class="field" id="dl-ws-field">
      <label for="dl-ws">Wingspan (fingertip to fingertip) <output id="dl-ws-out">70 in</output></label>
      <input type="range" id="dl-ws" min="48" max="84" step="0.5" value="70">
      <p class="hint">Stand against a wall, arms straight out, palms forward. Don&rsquo;t stretch.</p>
    </div>
    <div class="field" id="dl-h-field" hidden>
      <label for="dl-h">Height (barefoot) <output id="dl-h-out">5 ft 10 in</output></label>
      <input type="range" id="dl-h" min="48" max="84" step="0.5" value="70">
      <p class="hint">Height is a rougher estimate because arm length varies. Use wingspan if you can.</p>
    </div>
    <div class="field">
      <label for="dl-release">Release type</label>
      <select id="dl-release">
        <option value="0">Wrist-strap index release</option>
        <option value="0.5">Handheld (thumb / hinge) release</option>
        <option value="0">Fingers (traditional)</option>
      </select>
      <p class="hint">Handheld releases anchor further back, so many archers add about &frac12; inch.</p>
    </div>
  </div>
  <div class="result reveal reveal-d2" aria-live="polite">
    <p style="margin:0">Your estimated draw length</p>
    <div class="big-num"><span id="dl-result">28</span><small>inches</small></div>
    <p id="dl-range">Try 27.5&Prime; to 28.5&Prime; and confirm by shooting.</p>
    <svg class="archer" viewBox="0 0 300 140" aria-hidden="true">
      <line x1="20" y1="120" x2="280" y2="120" stroke="rgba(255,255,255,.2)" stroke-width="2"/>
      <path id="dl-bow" d="M230 20 Q265 70 230 120" fill="none" stroke="#FF6930" stroke-width="5" stroke-linecap="round"/>
      <path id="dl-string" d="M230 20 L140 70 L230 120" fill="none" stroke="#fff" stroke-width="1.5"/>
      <line id="dl-arrow" x1="140" y1="70" x2="262" y2="70" stroke="#cfe3e4" stroke-width="2.5"/>
      <text id="dl-label" x="185" y="62" fill="#fff" font-size="12" text-anchor="middle" font-family="Roboto">28"</text>
    </svg>
    <h3 style="font-size:1.05rem;margin-top:10px">Bows we&rsquo;ve reviewed that fit</h3>
    <div id="dl-bows"></div>
  </div>
</div>

<div class="tool-content prose">
  <h2 id="how-it-works">How the Draw Length Calculator Works</h2>
  <p>This Better Outdoors draw length calculator uses the method most archery pro shops start with: measure your wingspan in inches and divide by 2.5. If you can&rsquo;t measure wingspan, height works as a stand-in because most adults have a wingspan within an inch or two of their height. The result is rounded to the nearest half inch, because that is how most modern compound bow cams adjust.</p>
  <?= data_table(['Wingspan', 'Estimated draw length'], [
      ['60"', '24"'], ['63"', '25" (25.2")'], ['65"', '26"'], ['68"', '27" (27.2")'], ['70"', '28"'], ['73"', '29" (29.2")'], ['75"', '30"'], ['78"', '31" (31.2")'],
  ], 'Quick draw length chart (wingspan ÷ 2.5)') ?>
  <h2 id="confirm">Confirm Your Number at Full Draw</h2>
  <p>A calculator gets you close. Your body gets the final vote. At full draw with your real release, check that:</p>
  <ul class="checks">
    <li>The string lightly touches the tip of your nose and the corner of your mouth</li>
    <li>Your bow arm has a soft bend, not a locked elbow</li>
    <li>Your front shoulder stays down and relaxed</li>
    <li>Your release hand sits behind your jaw at a repeatable anchor</li>
  </ul>
  <p>If you are stretched, go ½ inch shorter. If your anchor is crowded and your elbow is bent sharply, go ½ inch longer. Our <?= post_link('2016-pse-draw-length-adjustment', '2016 PSE draw length adjustment guide') ?> walks through moving cam modules step by step, and the same logic applies to most brands.</p>
  <?= callout('tip', 'Pro shop tip', 'Shoot 30 or more arrows at a new setting before judging it. Fatigue and new muscle memory make the first dozen shots misleading.') ?>
  <?= product_grid([
      ['name' => 'Draw Check Arrow', 'q' => 'archery draw length arrow measuring', 'icon' => 'fa-ruler', 'blurb' => 'A marked arrow that shows your real draw length at full draw.'],
      ['name' => 'Wrist-Strap Release', 'q' => 'index finger bow release aid', 'icon' => 'fa-hand-pointer', 'blurb' => 'Adjustable strap length lets you fine-tune fit by small amounts.'],
      ['name' => 'Bow Draw Weight Scale', 'q' => 'bow draw weight scale digital', 'icon' => 'fa-weight-hanging', 'blurb' => 'Re-check peak weight after any draw length change.'],
  ], 'Helpful gear for checking fit') ?>
  <?= faq_block([
      'How do I calculate my draw length?' => 'Measure your wingspan from fingertip to fingertip in inches with your arms straight out, then divide by 2.5. A 70-inch wingspan gives a 28-inch draw length. Confirm the result by shooting.',
      'Is draw length the same as arm length?' => 'No. Draw length is measured from the nocking point to the pivot point of the grip plus 1.75 inches, at full draw. It depends on arm length, shoulder width and anchor style.',
      'Can I use my height to find draw length?' => 'Yes, as a rough estimate. Height divided by 2.5 works for many adults because wingspan is usually close to height, but measuring wingspan is more accurate.',
      'What happens if my draw length is too long?' => 'You will feel stretched, your bow arm locks, the string may slap your forearm and your groups open up. Shortening by ½ inch usually helps.',
      'Should a draw length be different for a release aid and fingers?' => 'Often slightly. Handheld releases anchor further back than wrist-strap releases, so many archers run about ½ inch more draw with a handheld release.',
  ], 'faq') ?>
</div>
