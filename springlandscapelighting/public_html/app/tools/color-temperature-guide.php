<?php defined('SLT') || exit; ?>
<div class="tool" data-tool="kelvin">
  <div class="tool__in">
    <div class="ktint"><img src="/assets/img/Spring-Landscape-Lighting-BG-1-960.webp" alt="Grasses and trees lit at night" loading="lazy" data-out="photo"><div data-out="tint" style="position:absolute;inset:0;mix-blend-mode:color;opacity:.55;background:#ffc27a"></div></div>
    <label class="rng" style="margin-top:20px"><span class="rng__top">Color temperature <output data-out="k">2700K</output></span><input class="kelvin" type="range" min="2200" max="5000" step="100" value="2700" data-in="k"></label>
    <div class="presets"><button type="button" class="chip" data-k="2200">2200K</button><button type="button" class="chip is-on" data-k="2700">2700K</button><button type="button" class="chip" data-k="3000">3000K</button><button type="button" class="chip" data-k="4000">4000K</button><button type="button" class="chip" data-k="5000">5000K</button></div>
  </div>
  <div class="tool__out">
    <div class="tool__hero"><small data-out="kname">Warm white</small><strong data-out="kbig">2700K</strong><span data-out="kfeel">Cozy, residential, flattering</span></div>
    <p data-out="kdesc" style="color:#cfdcd3;font-size:.95rem"></p>
    <div class="swatches">
      <div class="swatch"><div class="swatch__s" style="background:#7a3b2a"></div><span>Red brick</span></div>
      <div class="swatch"><div class="swatch__s" style="background:#b9a988"></div><span>Limestone</span></div>
      <div class="swatch"><div class="swatch__s" style="background:#2f5a35"></div><span>Foliage</span></div>
      <div class="swatch"><div class="swatch__s" style="background:#2f5f73"></div><span>Water</span></div>
    </div>
    <p class="tool__note" data-out="kbest"></p>
  </div>
</div>
