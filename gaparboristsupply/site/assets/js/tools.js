/* Gap Arborist Supply — interactive tools. Each tool reads products embedded in #tool-products. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const app = $('[data-tool]'); if (!app) return;
  const G = window.Gap, money = n => '$' + Math.round(n).toLocaleString('en-US');
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const img = k => '/assets/img/kinds/' + k + '.svg';
  const PRODUCTS = JSON.parse($('#tool-products').textContent || '[]');
  const fmt = (n, d = 1) => (+n).toLocaleString('en-US', { maximumFractionDigits: d });

  function recs(list) {
    const box = $('[data-tool-recs]'); if (!box) return;
    box.innerHTML = list.slice(0, 4).map(p => `<article class="card" data-product='${esc(JSON.stringify({ p: p.p, n: p.n, pr: p.pr, k: p.k }))}'>
      <a class="card-media" href="${esc(p.p)}" tabindex="-1" aria-hidden="true"><span class="rings"></span><img src="${img(p.k)}" alt="" loading="lazy"></a>
      <div class="card-body"><p class="card-brand">${esc(p.bn)}</p><h3 class="card-title"><a href="${esc(p.p)}">${esc(p.n)}</a></h3>
      <div class="card-foot"><span class="price"><small>Typical</small> ${money(p.pr)}</span><button class="btn btn-sm btn-cart" type="button" data-add>Add</button></div></div></article>`).join('');
  }
  const pickBy = (fn, n = 4) => PRODUCTS.filter(fn).sort((a, b) => (b.l === 'pro') - (a.l === 'pro')).slice(0, n);

  const tools = {
    // ------------------------------------------------------------------ kit builder
    'climbing-kit-builder'() {
      const form = $('[data-kit-form]'), slotsEl = $('[data-kit-slots]');
      const has = (p, ...parts) => parts.some(x => p.c.includes(x));
      const SLOTS = {
        saddle:   { role: 'Saddle', why: 'Your work-positioning harness: comfort here pays off all day.', f: p => p.k === 'saddle' && has(p, 'saddles-and-harnesses') && !has(p, 'saddle-parts') },
        rope:     { role: 'Climbing rope', why: 'Life-support line. Match its diameter to your hitch or device.', f: p => p.k === 'rope' && has(p, '/rope/climbing-rope/') },
        mrs:      { role: 'Friction device', why: 'Moving-rope device or hitch system for ascending and descending.', f: p => (p.k === 'friction-device' && has(p, 'devices-for-mrs', 'mechanical-friction')) || has(p, 'eye-and-eye-prusiks') },
        pulley:   { role: 'Hitch-tending pulley', why: 'Keeps your hitch tended so you take in slack smoothly.', f: p => has(p, 'micro-pulleys') },
        srs:      { role: 'SRS device', why: 'Rope wrench or mechanical device for stationary-rope climbing.', f: p => has(p, 'devices-for-srs') },
        ascender: { role: 'Ascender', why: 'Foot or hand ascender to climb a stationary line efficiently.', f: p => p.k === 'ascender' && has(p, 'ascent-and-descent') },
        lanyard:  { role: 'Lanyard', why: 'Your second point of attachment while you work and cut.', f: p => p.k === 'lanyard' && has(p, 'fliplines-and-lanyards') && !has(p, 'wire-core') },
        flipline: { role: 'Steel-core flipline', why: 'Cut-resistant flipline for spur removals.', f: p => p.k === 'lanyard' && has(p, 'fliplines-and-lanyards') },
        spurs:    { role: 'Climbing spurs', why: 'For removals only. Never spike a tree you are keeping.', f: p => p.k === 'spur' && has(p, '/climbing/spurs/') && !has(p, 'climber-pads', 'replacement-gaffs') },
        biners:   { role: 'Locking carabiners ×3', why: 'Auto-locking connectors for bridge, device and lanyard.', qty: 3, f: p => p.k === 'carabiner' && has(p, 'auto-locking-carabiners') },
        helmet:   { role: 'Helmet', why: 'Climbing-rated helmet with a chin strap.', f: p => p.k === 'helmet' && has(p, '/climbing/helmets/') },
        throw:    { role: 'Throw line & weight', why: 'Sets your line in the canopy without climbing to install it.', f: p => p.k === 'throw-line' },
        saw:      { role: 'Hand saw', why: 'Pruning saw with a scabbard for the saddle.', f: p => p.k === 'hand-saw' },
        bag:      { role: 'Gear bag', why: 'Keeps rope and hardware clean and organized.', f: p => p.k === 'case-bag' },
      };
      const SYSTEMS = { mrs: ['saddle', 'rope', 'mrs', 'pulley', 'lanyard', 'biners', 'helmet'], srs: ['saddle', 'rope', 'srs', 'ascender', 'lanyard', 'biners', 'helmet'], spurs: ['saddle', 'spurs', 'flipline', 'lanyard', 'rope', 'biners', 'helmet'] };
      const options = {}; for (const k in SLOTS) options[k] = PRODUCTS.filter(SLOTS[k].f).sort((a, b) => a.pr - b.pr);
      let choice = {}; // slot -> index into options
      const slotsFor = () => {
        const sys = form.sys.value, extras = $$('.checks input:checked', form).map(i => i.value);
        return SYSTEMS[sys].concat(extras).filter(s => options[s] && options[s].length);
      };
      const qty = s => SLOTS[s].qty || 1;
      const total = slots => slots.reduce((a, s) => a + options[s][choice[s]].pr * qty(s), 0);
      // Start every slot at its best option, then step down whichever slot saves the most until it fits the budget.
      const fit = () => {
        const budget = +$('[data-budget]').value, slots = slotsFor();
        choice = {}; slots.forEach(s => choice[s] = options[s].length - 1);
        let guard = 200;
        while (total(slots) > budget && guard--) {
          let best = null, save = 0;
          for (const s of slots) if (choice[s] > 0) { const d = (options[s][choice[s]].pr - options[s][choice[s] - 1].pr) * qty(s); if (d > save) { save = d; best = s; } }
          if (!best) break; choice[best]--;
        }
        draw();
      };
      const draw = () => {
        const slots = slotsFor(), budget = +$('[data-budget]').value, t = total(slots);
        $('[data-budget-out]').textContent = money(budget);
        slotsEl.innerHTML = slots.map((s, i) => {
          const p = options[s][choice[s]], n = options[s].length;
          return `<li class="kit-slot" style="animation-delay:${i * 40}ms"><img src="${img(p.k)}" alt="" width="56" height="56">
            <div><span class="role">${SLOTS[s].role}</span><a href="${esc(p.p)}">${esc(p.n)}</a><span class="why">${SLOTS[s].why}</span></div>
            <div class="slot-right"><span class="slot-price">${money(p.pr * qty(s))}</span>${n > 1 ? `<button class="swap" type="button" data-swap="${s}">Swap (${choice[s] + 1}/${n})</button>` : ''}</div></li>`;
        }).join('');
        $('[data-kit-total]').textContent = money(t);
        const ring = $('[data-ring]'), frac = Math.min(1, t / budget);
        ring.style.strokeDashoffset = 326.7 * (1 - frac); ring.classList.toggle('over', t > budget);
        $('[data-kit-status]').textContent = t > budget ? `${money(t - budget)} over budget, the cheapest option in each slot` : `${money(budget - t)} left in your budget`;
      };
      slotsEl.addEventListener('click', e => {
        const b = e.target.closest('[data-swap]'); if (!b) return;
        const s = b.dataset.swap; choice[s] = (choice[s] + 1) % options[s].length; draw();
      });
      form.addEventListener('input', fit); form.addEventListener('change', fit);
      $('[data-kit-add]').addEventListener('click', e => {
        const slots = slotsFor(), c = G.cart();
        slots.forEach(s => { const p = options[s][choice[s]], hit = c.find(i => i.p === p.p); if (hit) hit.q += qty(s); else c.push({ p: p.p, n: p.n, pr: p.pr, k: p.k, q: qty(s) }); });
        G.setCart(c); G.toast(`Added ${slots.length} kit items · <a href="/cart/">View cart</a>`);
        e.target.textContent = 'Kit added ✓'; setTimeout(() => e.target.textContent = 'Add whole kit to cart', 1600);
      });
      fit();
    },

    // ------------------------------------------------------------------ rigging
    'rigging-load-calculator'() {
      // Typical green (freshly cut) weights, lb per cubic foot.
      const SPECIES = [['Red oak', 63], ['White oak', 62], ['Live oak', 76], ['Pin / water oak', 64], ['Hickory / pecan', 63], ['Sugar maple', 56], ['Red maple', 50], ['Silver maple', 45], ['White ash', 48], ['American elm', 54], ['Hackberry', 50], ['Sycamore', 52], ['Sweetgum', 55], ['Black walnut', 58], ['Black cherry', 45], ['Cottonwood', 49], ['Tulip poplar', 38], ['Willow', 50], ['Loblolly / southern pine', 53], ['Ponderosa pine', 46], ['Eastern white pine', 36], ['Douglas fir', 38], ['Eastern hemlock', 50], ['Spruce', 34]];
      // Typical double-braid polyester rigging rope, average breaking strength (lb).
      const ROPES = [['3/8 in (≈ 5,000 lb)', 5000], ['1/2 in (≈ 9,000 lb)', 9000], ['9/16 in (≈ 11,000 lb)', 11000], ['5/8 in (≈ 14,000 lb)', 14000], ['3/4 in (≈ 20,000 lb)', 20000], ['7/8 in (≈ 26,000 lb)', 26000]];
      const sp = $('[data-species]'), rp = $('[data-rope]');
      sp.innerHTML = SPECIES.map(([n, w], i) => `<option value="${i}">${n} · ${w} lb/ft³</option>`).join('');
      rp.innerHTML = ROPES.map(([n], i) => `<option value="${i}"${i === 1 ? ' selected' : ''}>${n}</option>`).join('');
      const scene = $('.rig-scene');
      const calc = (animate) => {
        const dia = +$('[data-dia]').value, len = +$('[data-len]').value, drop = +$('[data-drop]').value, L = +$('[data-ropelen]').value;
        const [sName, dens] = SPECIES[sp.value], [rName, mbs] = ROPES[rp.value];
        $('[data-dia-out]').textContent = dia + ' in'; $('[data-len-out]').textContent = len + ' ft'; $('[data-drop-out]').textContent = drop + ' ft'; $('[data-rope-out]').textContent = L + ' ft';
        const r = dia / 24, vol = Math.PI * r * r * len, W = vol * dens;
        // Elastic rope: stiffness modelled as MBS / 0.15 (about 15% stretch at break). F = W(1 + sqrt(1 + 2·FF·M/W)).
        const M = mbs / 0.15, FF = drop / L, peak = drop > 0 ? W * (1 + Math.sqrt(1 + 2 * FF * M / W)) : W;
        const pct = peak / mbs * 100;
        $('[data-weight]').textContent = fmt(W, 0) + ' lb'; $('[data-weight-note]').textContent = `${fmt(vol, 1)} ft³ of ${sName.toLowerCase()}`;
        $('[data-peak]').textContent = fmt(peak, 0) + ' lb'; $('[data-peak-note]').textContent = `${fmt(peak / W, 1)}× the log weight · ${fmt(pct, 0)}% of the rope's strength`;
        $('[data-mbs]').textContent = fmt(W * 10, 0) + ' lb';
        $('[data-gauge]').style.setProperty('--g', Math.min(100, pct) + '%');
        $('[data-gauge-label]').textContent = fmt(pct, 0) + '% of breaking strength';
        const v = $('[data-verdict]');
        if (W * 10 > mbs) { v.className = 'verdict bad'; v.textContent = `Even hanging still, this piece is past a 10:1 working load for ${rName.split(' (')[0]} rope. Go bigger on rope and hardware or cut it smaller.`; }
        else if (pct > 20) { v.className = 'verdict warn'; v.textContent = `A ${drop} ft drop pushes the peak load past a fifth of the rope's strength. Shorten the drop, let the rope run on the lowering device, or take a smaller piece.`; }
        else { v.className = 'verdict'; v.textContent = `Within a sensible margin for ${rName.split(' (')[0]} rope, assuming the rigging point and hardware are rated for it.`; }
        // scene
        const w = Math.min(130, 30 + len * 6), h = Math.min(48, 10 + dia * 1.1);
        const shape = $('[data-rig-logshape]'); shape.setAttribute('x', -w / 2); shape.setAttribute('width', w); shape.setAttribute('y', -h / 2); shape.setAttribute('height', h); shape.setAttribute('rx', h / 2);
        const end = $('.rig-end'); end.setAttribute('cx', w / 2); end.setAttribute('ry', h / 2);
        if (animate && drop > 0) { scene.classList.remove('drop'); void scene.getBBox; requestAnimationFrame(() => scene.classList.add('drop')); }
        recs(pickBy(p => p.k === 'rigging-device' || p.k === 'sling' || (p.k === 'rope' && p.c.includes('rigging'))));
      };
      $('[data-rig-form]').addEventListener('input', e => calc(e.target.matches('[data-drop]')));
      $('[data-rig-form]').addEventListener('change', () => calc(false));
      calc(false);
    },

    // ------------------------------------------------------------------ tree height & rope length
    'rope-length-calculator'() {
      const STOCK = [120, 150, 200, 250, 300];
      const calc = () => {
        const d = +$('[data-d]').value, a = +$('[data-a]').value, eye = +$('[data-eye]').value, tie = +$('[data-tie]').value / 100;
        const sys = $('input[name=rs]:checked').value;
        $('[data-d-out]').textContent = d + ' ft'; $('[data-a-out]').textContent = a + '°'; $('[data-eye-out]').textContent = eye + ' ft'; $('[data-tie-out]').textContent = Math.round(tie * 100) + '%';
        const H = d * Math.tan(a * Math.PI / 180) + eye, T = H * tie;
        const need = sys === 'mrs' ? 2 * T + 15 : T + 15;
        const stock = STOCK.find(s => s >= need);
        $('[data-h]').textContent = fmt(H, 0) + ' ft'; $('[data-tie-h]').textContent = fmt(T, 0) + ' ft';
        $('[data-rope]').textContent = fmt(Math.ceil(need / 5) * 5, 0) + ' ft';
        $('[data-rope-note]').textContent = sys === 'mrs' ? 'Doubled line to the tie-in plus a 15 ft tail' : 'Single line to the anchor plus a 15 ft tail';
        $('[data-rope-verdict]').textContent = stock ? `A ${stock} ft rope covers this climb with room to spare.` : `That's a big tree: you'll want a custom length over 300 ft, or climb it in stages.`;
        // scene: scale the tree to fit
        const sc = Math.min(1, 200 / H), top = 270 - H * sc, tieY = 270 - T * sc, angle = Math.atan2(236 - top, 250);
        $('[data-hs-trunk]').setAttribute('d', `M290 270 V${top + 30}`);
        const crown = $('[data-hs-crown]'); crown.setAttribute('cy', top + 34); crown.setAttribute('r', Math.max(18, 46 * sc));
        $('[data-hs-sight]').setAttribute('d', `M40 236 L290 ${top}`);
        $('[data-hs-tie]').setAttribute('cy', tieY);
        $('[data-hs-arc]').setAttribute('d', `M80 236 A40 40 0 0 0 ${40 + 40 * Math.cos(angle)} ${236 - 40 * Math.sin(angle)}`);
        $('[data-hs-dist]').textContent = d + ' ft';
        recs(pickBy(p => p.k === 'rope' || p.k === 'throw-line'));
      };
      app.addEventListener('input', calc); app.addEventListener('change', calc); calc();
    },

    // ------------------------------------------------------------------ fuel mix
    'fuel-mix-calculator'() {
      const amt = $('[data-amt]');
      const calc = () => {
        const unit = $('input[name=u]:checked').value, r = +$('input[name=r]:checked').value;
        if (unit === 'l') { amt.min = 1; amt.max = 20; amt.step = .5; } else { amt.min = .25; amt.max = 5; amt.step = .25; }
        const v = Math.min(+amt.value, +amt.max);
        const gal = unit === 'gal' ? v : v / 3.78541, ml = gal * 3785.41 / r, oz = ml / 29.5735;
        $('[data-amt-out]').textContent = unit === 'gal' ? fmt(v, 2) + ' gal' : fmt(v, 1) + ' L';
        $('[data-oz]').textContent = fmt(oz, 1) + ' fl oz'; $('[data-ml]').textContent = fmt(ml, 0) + ' ml';
        $('[data-mix]').textContent = `${unit === 'gal' ? fmt(v, 2) + ' gal' : fmt(v, 1) + ' L'} at ${r}:1`;
        const fill = Math.min(1, gal / (unit === 'gal' ? 5 : 5.3)), top = 230 - 150 * fill, oilH = Math.max(3, 150 * fill / r * 6);
        const gas = $('[data-gas]'), oil = $('[data-oil]');
        gas.setAttribute('y', top); gas.setAttribute('height', 240 - top); oil.setAttribute('y', top); oil.setAttribute('height', oilH);
        $('[data-mix-table]').innerHTML = [1, 2, 2.5, 5].map(g => `<tr class="${unit === 'gal' && Math.abs(g - v) < .01 ? 'on' : ''}"><td>${g} gal</td>${[50, 40, 32].map(x => `<td>${fmt(g * 128 / x, 1)}</td>`).join('')}</tr>`).join('');
      };
      app.addEventListener('input', calc); app.addEventListener('change', calc); calc();
      recs(pickBy(p => p.k === 'fluid').concat(pickBy(p => p.k === 'chainsaw' || p.k === 'top-handle', 2)));
    },

    // ------------------------------------------------------------------ spark plug decoder
    'spark-plug-decoder'() {
      const THREAD = { A: '18 mm thread', B: '14 mm thread', C: '10 mm thread', D: '12 mm thread', E: '8 mm thread' };
      const MID = { P: 'Projected insulator tip: the firing tip sits further into the chamber for better self-cleaning', M: 'Compact (short) shell, common on small 2-stroke engines', R: 'Resistor type: suppresses radio-frequency interference', Z: 'Special construction variant' };
      const REACH = { E: '19 mm thread reach', H: '12.7 mm thread reach', L: '11.2 mm thread reach' };
      const input = $('[data-plug-in]'), chips = $('[data-plug-chips]'), parts = $('[data-plug-parts]');
      const decode = () => {
        const code = input.value.toUpperCase().replace(/[^A-Z0-9-]/g, ''); input.value = code;
        const out = []; let i = 0;
        if (THREAD[code[i]]) { out.push([code[i], THREAD[code[i]]]); i++; }
        while (i < code.length && /[A-Z]/.test(code[i]) && !/\d/.test(code[i])) {
          out.push([code[i], MID[code[i]] || 'Design code: check NGK’s chart for this letter']); i++;
        }
        const heat = code.slice(i).match(/^\d+/);
        if (heat) { out.push([heat[0], `Heat range ${heat[0]}. On NGK plugs a lower number is a hotter plug, a higher number is colder`]); i += heat[0].length; }
        for (; i < code.length; i++) {
          const ch = code[i];
          out.push([ch, REACH[ch] || (ch === '-' ? 'Separator before gap or special-feature codes' : 'Special design or electrode variant: check NGK’s chart')]);
        }
        chips.innerHTML = out.map(([c, , ], n) => `<span data-i="${n}" class="${/check NGK/.test(out[n][1]) ? 'unk' : ''}">${esc(c)}</span>`).join('');
        parts.innerHTML = out.map(([c, t], n) => `<li data-i="${n}"><b>${esc(c)}</b> — ${esc(t)}</li>`).join('') + '<li>Use the exact plug number listed in your saw’s operator’s manual. Check and set the gap to the manual’s figure.</li>';
      };
      chips.addEventListener('pointerover', e => { const s = e.target.closest('[data-i]'); $$('li', parts).forEach(l => l.classList.toggle('on', s && l.dataset.i === s.dataset.i)); $$('span', chips).forEach(c => c.classList.toggle('on', c === s)); });
      input.addEventListener('input', decode);
      $$('[data-plug]').forEach(b => b.addEventListener('click', () => { input.value = b.dataset.plug; decode(); }));
      decode();
      const TIPS = [
        ['#c9a36b', 'Tan / light gray', 'Running right', 'A light tan or gray insulator with clean electrodes means the mixture, heat range and tune are where they should be. Re-gap and reuse, or replace if the electrode is rounded.'],
        ['#2b2b2b', 'Dry black soot', 'Running rich', 'Dry, fluffy carbon usually means too much fuel or too little air: check the air filter first, then the choke and carburetor adjustment. Long idling can do it too.'],
        ['#4a3a22', 'Wet and oily', 'Oil fouled or flooded', 'Wet deposits point to too much oil in the mix, a flooded engine or worn rings. Check your fuel mix ratio, dry the plug and try again. Repeated oil fouling needs a closer look.'],
        ['#f2f0ea', 'White / blistered', 'Running lean and hot', 'A chalky white or blistered tip means the engine is running too hot or too lean. Stop and check for air leaks, a clogged fuel filter or a lean carburetor setting before the saw seizes.'],
        ['#a35d2a', 'Rusty brown deposits', 'Fuel additives or old fuel', 'Reddish or brown ash often comes from fuel additives or stale fuel. Drain old fuel, run fresh mix and replace the plug.'],
      ];
      const sw = $('[data-swatches]'), diag = $('[data-diagnosis]');
      sw.innerHTML = TIPS.map((t, i) => `<button type="button" class="swatch" role="radio" aria-checked="false" style="background:radial-gradient(circle at 40% 35%, #fff6 0 18%, ${t[0]} 40%)" data-t="${i}" aria-label="${t[1]}"><span>${t[1]}</span></button>`).join('');
      sw.addEventListener('click', e => {
        const b = e.target.closest('[data-t]'); if (!b) return;
        $$('.swatch', sw).forEach(x => x.setAttribute('aria-checked', x === b));
        const t = TIPS[b.dataset.t]; diag.innerHTML = `<h3>${t[2]}</h3><p>${t[3]}</p>`;
      });
      sw.querySelector('[data-t]').click();
      recs(pickBy(p => p.k === 'spark-plug').concat(pickBy(p => p.k === 'parts', 2)));
    },

    // ------------------------------------------------------------------ chain & file
    'chain-file-finder'() {
      const PITCH = { '1/4': [.25, '5/32"', '4.0 mm'], '3/8LP': [.375, '5/32"', '4.0 mm'], '.325': [.325, '3/16"', '4.8 mm'], '3/8': [.375, '7/32"', '5.5 mm'], '.404': [.404, '7/32"', '5.5 mm'] };
      // Typical drive links by bar length (in), varies by bar maker.
      const BARS = { '3/8LP': { 12: 45, 14: 52, 16: 56, 18: 62 }, '.325': { 13: 56, 16: 66, 18: 72, 20: 78 }, '3/8': { 16: 60, 18: 66, 20: 72, 24: 84, 28: 93, 32: 105, 36: 114 }, '.404': { 20: 64, 24: 72, 28: 84, 32: 91, 36: 104 }, '1/4': { 10: 60, 12: 70 } };
      const track = $('[data-chain-track]');
      const calc = () => {
        const p = $('input[name=pitch]:checked').value, g = $('input[name=gauge]:checked').value, dl = +$('[data-dl]').value;
        $('[data-dl-out]').textContent = dl;
        const [pv, file, mm] = PITCH[p];
        $('[data-file]').textContent = file; $('[data-file-mm]').textContent = mm;
        $('[data-code]').textContent = `${p.replace('LP', '" LP')}${p.includes('LP') ? '' : '"'} ${g}" ${dl}DL`;
        $('[data-loop]').textContent = fmt(dl * pv * 2, 1) + ' in';
        const table = BARS[p] || {}; let best = null, diff = 1e9;
        for (const [len, n] of Object.entries(table)) if (Math.abs(n - dl) < diff) { diff = Math.abs(n - dl); best = len; }
        $('[data-bar]').textContent = best ? best + ' in' : '—';
        $('[data-bar-note]').textContent = best ? (diff === 0 ? 'Common match' : `Closest common size is ${table[best]} DL`) : '';
        track.style.strokeDasharray = `${6 + pv * 8} ${3 + pv * 4}`;
      };
      app.addEventListener('input', calc); app.addEventListener('change', calc); calc();
      recs(pickBy(p => p.k === 'chain-bar').concat(pickBy(p => p.k === 'wrench-file', 2)));
    },
  };
  tools[app.dataset.tool]?.();
})();
