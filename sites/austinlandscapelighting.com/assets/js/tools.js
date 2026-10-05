/* Austin Landscape Lighting - interactive tools.
   Each [data-tool] block is initialised by name. Pure client-side math;
   figures are planning estimates, labelled as such in the markup. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const money = (n) => '$' + Math.round(n).toLocaleString('en-US');
  const range = (lo, hi) => `${money(lo)} – ${money(hi)}`;
  const out = (root, key, html) => { const el = root.querySelector(`[data-out="${key}"]`); if (el) el.innerHTML = html; };
  const val = (form, name) => { const f = form.elements[name]; return f ? (f.type === 'checkbox' ? f.checked : f.value) : ''; };
  const num = (form, name) => parseFloat(val(form, name)) || 0;
  const bars = (root, key, rows) => {
    const max = Math.max(1, ...rows.map((r) => r[1]));
    out(root, key, rows.filter((r) => r[1] > 0).map(([l, v]) => `<li><span>${l}</span><i style="--w:${(v / max * 100).toFixed(1)}%"></i><b>${v}</b></li>`).join(''));
  };
  const transformerFor = (watts) => { const sizes = [150, 300, 600, 900, 1200, 1500]; const need = watts * 1.25; return sizes.find((s) => s >= need) || 'multiple transformers'; };
  const bindRanges = (form) => {
    $$('input[type="range"]', form).forEach((r) => {
      const o = form.querySelector(`output[name="${r.name}_out"]`);
      const upd = () => { if (o) o.value = r.value; r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%'); };
      r.addEventListener('input', upd); upd();
    });
  };

  /* ---------- Fixture calculator ---------- */
  const fixtures = (root) => {
    const form = $('form', root);
    const calc = () => {
      const facade = num(form, 'facade'), stories = num(form, 'stories'), columns = num(form, 'columns');
      const ts = num(form, 'trees_small'), tl = num(form, 'trees_large'), path = num(form, 'path'), steps = num(form, 'steps');
      const patio = num(form, 'patio'), pool = num(form, 'pool'), beds = num(form, 'beds');
      const up = Math.round(facade / 10) + columns + (stories >= 2 ? Math.round(facade / 25) : 0);
      const pathL = Math.ceil(path / 7);
      const treeS = ts * 1, treeL = tl * 2, moon = Math.round(tl * 0.6);
      const stepL = steps * 2;
      const patioL = [0, 3, 5, 8][patio] || 0;
      const poolL = pool ? 4 : 0;
      const bedL = Math.round(beds * 1.5);
      const rows = [['Facade uplights', up], ['Path lights', pathL], ['Tree uplights', treeS + treeL], ['Tree moonlights', moon], ['Step / wall lights', stepL], ['Patio & deck', patioL], ['Pool & water', poolL], ['Garden accents', bedL]];
      const total = rows.reduce((a, r) => a + r[1], 0);
      const watts = up * 5 + pathL * 3 + (treeS + treeL) * 6 + moon * 7 + stepL * 2 + patioL * 4 + poolL * 5 + bedL * 4;
      out(root, 'total', total);
      bars(root, 'bars', rows);
      out(root, 'transformer', typeof transformerFor(watts) === 'number' ? transformerFor(watts) + ' W' : transformerFor(watts));
      out(root, 'watts', `${watts} W (about ${(watts * 6 * 30 / 1000 * 0.14).toFixed(2).replace(/^/, '$')}/mo at 6 h/night)`);
      out(root, 'range', range(total * 275, total * 475));
      out(root, 'time', total <= 14 ? 'Half a day' : total <= 30 ? 'One day' : total <= 45 ? 'One to two days' : 'Two days');
      const scale = total < 10 ? 'A focused entry package. Prioritise the front door, steps and one specimen tree.' : total < 22 ? 'A typical Austin front-yard system: facade, path and one or two feature trees.' : total < 36 ? 'A layered front-and-back design with patio and tree lighting. Plan two zones.' : 'An estate-scale design. We would phase zones and use two transformers for even voltage.';
      out(root, 'note', scale);
    };
    form.addEventListener('input', calc); calc();
  };

  /* ---------- Cost estimator ---------- */
  const cost = (root) => {
    const form = $('form', root);
    bindRanges(form);
    const calc = () => {
      const n = num(form, 'fixtures');
      const grade = { good: [230, 320], better: [290, 420], best: [380, 560] }[val(form, 'grade')];
      const controls = { timer: [120, 220], photocell: [180, 320], smart: [450, 950] }[val(form, 'controls')];
      const zones = num(form, 'zones');
      const terrain = { easy: 1, mixed: 1.12, hard: 1.28 }[val(form, 'terrain')];
      const design = val(form, 'design') === 'plan' ? [350, 750] : [0, 0];
      const watts = n * 5;
      const tx = transformerFor(watts);
      const txCost = typeof tx === 'number' ? [tx * 0.9 + 120, tx * 1.2 + 220] : [900, 1400];
      const lo = (n * grade[0] + controls[0] * zones + txCost[0] * Math.max(1, zones - 1) + design[0]) * terrain;
      const hi = (n * grade[1] + controls[1] * zones + txCost[1] * Math.max(1, zones - 1) + design[1]) * terrain;
      out(root, 'range', range(lo, hi));
      bars(root, 'bars', [['Fixtures & lamps', Math.round(n * (grade[0] + grade[1]) / 2)], ['Wire & connectors', Math.round(n * 28 * terrain)], ['Transformer(s)', Math.round((txCost[0] + txCost[1]) / 2 * Math.max(1, zones - 1))], ['Controls', Math.round((controls[0] + controls[1]) / 2 * zones)], ['Labor & aiming', Math.round(n * 95 * terrain)], ['Design', Math.round((design[0] + design[1]) / 2)]]);
      out(root, 'perfixture', range(lo / n, hi / n));
      out(root, 'transformer', typeof tx === 'number' ? `${tx} W${zones > 1 ? ' × ' + (zones) : ''}` : tx);
      out(root, 'energy', money(watts * 6 * 30 / 1000 * 0.14 * 100) .replace('$', '$') === '' ? '' : '$' + (watts * 6 * 30 / 1000 * 0.14).toFixed(2));
    };
    form.addEventListener('input', calc); calc();
  };

  /* ---------- LED savings ---------- */
  const led = (root) => {
    const form = $('form', root);
    const calc = () => {
      const n = num(form, 'fixtures'), hw = num(form, 'halogen'), lw = num(form, 'led'), h = num(form, 'hours'), rate = num(form, 'rate'), lamp = num(form, 'lamp_cost');
      const kwhH = n * hw * h * 365 / 1000, kwhL = n * lw * h * 365 / 1000;
      const saveKwh = kwhH - kwhL, saveE = saveKwh * rate;
      const lampsPerYear = n * (h * 365) / 2000;
      const lampSave = lampsPerYear * lamp;
      const annual = saveE + lampSave;
      out(root, 'annual', money(annual));
      out(root, 'kwh_h', `${Math.round(kwhH)} kWh`); out(root, 'kwh_l', `${Math.round(kwhL)} kWh`);
      const b = root.querySelector('[data-out="bar_l"]'); if (b) b.style.setProperty('--w', (kwhL / kwhH * 100).toFixed(1) + '%');
      out(root, 'watts', `${n * hw} W → ${n * lw} W (${Math.round((1 - lw / hw) * 100)}% less)`);
      out(root, 'kwh', `${Math.round(saveKwh)} kWh (${money(saveE)} at $${rate.toFixed(2)}/kWh)`);
      out(root, 'lamps', `${Math.round(lampsPerYear * 10)} lamps (${money(lampSave * 10)})`);
      out(root, 'decade', money(annual * 10));
    };
    form.addEventListener('input', calc); calc();
  };

  /* ---------- Transformer ---------- */
  const transformer = (root) => {
    const form = $('form', root);
    const calc = () => {
      const watts = num(form, 'uplights') * 5 + num(form, 'pathlights') * 3 + num(form, 'downlights') * 7 + num(form, 'wall') * 4 + num(form, 'other');
      const head = watts * 1.25;
      const size = transformerFor(watts);
      const run = num(form, 'run'); const gauge = val(form, 'gauge');
      const ohmsPerFt = { 12: 0.00162, 10: 0.00102, 14: 0.00258 }[gauge];
      const amps = watts / 12;
      const drop = amps * ohmsPerFt * run * 2;
      out(root, 'size', typeof size === 'number' ? `${size} W` : 'Split the load');
      out(root, 'watts', `${watts} W (${amps.toFixed(1)} A at 12 V)`);
      out(root, 'headroom', `${Math.round(head)} W`);
      out(root, 'drop', `${drop.toFixed(2)} V (${(drop / 12 * 100).toFixed(1)}%)`);
      const tap = drop < 0.6 ? '12 V' : drop < 1.6 ? '13 V' : drop < 2.6 ? '14 V' : drop < 3.6 ? '15 V' : 'Shorten the run or hub the fixtures';
      out(root, 'tap', tap);
      const pct = typeof size === 'number' ? watts / size * 100 : 100;
      const m = root.querySelector('[data-out="meter"]'); if (m) m.style.setProperty('--w', Math.min(100, pct).toFixed(1) + '%');
      out(root, 'load', `${Math.round(pct)}% loaded`);
      out(root, 'note', pct > 80 ? 'Running above 80 percent leaves no room to add fixtures later. Step up one size.' : pct < 35 ? 'Lightly loaded. Fine for LED, and you have room to grow the system.' : 'Comfortable load with headroom for a few added fixtures.');
    };
    form.addEventListener('input', calc); calc();
  };

  /* ---------- Color temperature ---------- */
  const kelvin = (root) => {
    const form = $('form', root);
    const r = form.elements.kelvin;
    const kToRgb = (k) => {
      const t = k / 100; let rr, g, b;
      rr = t <= 66 ? 255 : 329.7 * Math.pow(t - 60, -0.1332);
      g = t <= 66 ? 99.47 * Math.log(t) - 161.12 : 288.12 * Math.pow(t - 60, -0.0755);
      b = t >= 66 ? 255 : t <= 19 ? 0 : 138.52 * Math.log(t - 10) - 305.04;
      const c = (x) => Math.max(0, Math.min(255, Math.round(x)));
      return `rgb(${c(rr)},${c(g)},${c(b)})`;
    };
    const info = (k) => {
      if (k < 2400) return ['Candlelight', 'Deep amber, like firelight. Flattering on wood, stone and skin, but it can muddy greens and make white trim look yellow.', 'Patios, fire pits, pergolas, wine rooms', 'Facades with white trim, modern stucco, lawns', 'Lovely as an accent zone, rarely for the whole property.'];
      if (k < 2900) return ['Warm white', 'The classic landscape lighting color. Warm enough to feel welcoming, neutral enough to render limestone, brick and foliage honestly.', 'Nearly every Austin home: limestone, brick, live oaks, paths', 'Very cool-toned grey or blue-grey architecture', 'Our default. Austin Landscape Lighting installs 2700K on most projects.'];
      if (k < 3300) return ['Soft white', 'A touch crisper. Greens read true and white trim stays white, with a slightly more contemporary feel.', 'Modern architecture, painted brick, pale stucco, pools', 'Rustic cedar, warm wood decks (can look chalky)', 'Great for modern homes and water. Keep the whole property at one temperature.'];
      if (k < 4300) return ['Neutral white', 'Clean and bright. Reads commercial next to warm interiors and flattens texture on stone.', 'Commercial parking, security zones, sports courts', 'Residential facades and gardens', 'We avoid it on homes; it fights the warm glow from your windows.'];
      return ['Daylight', 'Blue-white light that mimics midday. Harsh on landscapes at night and hard on dark-sky goals.', 'Industrial sites, loading areas', 'Any residential landscape', 'Not for landscape lighting.'];
    };
    const upd = () => {
      const k = parseInt(r.value, 10);
      out(root, 'k', k);
      const tint = root.querySelector('[data-out="tint"]'); if (tint) tint.style.setProperty('--tint', kToRgb(k));
      const [t, d, best, avoid, verdict] = info(k);
      out(root, 'title', `${t} · ${k}K`); out(root, 'desc', d); out(root, 'bestfor', best); out(root, 'avoid', avoid); out(root, 'verdict', verdict);
      $$('.kelvin__chips button', root).forEach((b) => b.classList.toggle('is-active', parseInt(b.dataset.k, 10) === k));
      r.style.setProperty('--p', ((k - r.min) / (r.max - r.min) * 100) + '%');
      const o = form.querySelector('output'); if (o) o.value = k;
    };
    r.addEventListener('input', upd);
    $$('.kelvin__chips button', root).forEach((b) => b.addEventListener('click', () => { r.value = b.dataset.k; upd(); }));
    upd();
  };

  /* ---------- Sunset timer (NOAA solar equations) ---------- */
  const sunset = (root) => {
    const form = $('form', root);
    const lat = 30.2672, lng = -97.7431;
    const rad = Math.PI / 180;
    const dayOfYear = (d) => Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 86400000);
    const solar = (date, event, zenith = 90.833) => {
      // returns minutes after UTC midnight for sunrise ('rise') or sunset ('set')
      const N = dayOfYear(date);
      const lngHour = lng / 15;
      const t = N + ((event === 'rise' ? 6 : 18) - lngHour) / 24;
      const M = (0.9856 * t) - 3.289;
      let L = M + (1.916 * Math.sin(M * rad)) + (0.020 * Math.sin(2 * M * rad)) + 282.634;
      L = ((L % 360) + 360) % 360;
      let RA = Math.atan(0.91764 * Math.tan(L * rad)) / rad;
      RA = ((RA % 360) + 360) % 360;
      RA += (Math.floor(L / 90) * 90 - Math.floor(RA / 90) * 90);
      RA /= 15;
      const sinDec = 0.39782 * Math.sin(L * rad);
      const cosDec = Math.cos(Math.asin(sinDec));
      const cosH = (Math.cos(zenith * rad) - (sinDec * Math.sin(lat * rad))) / (cosDec * Math.cos(lat * rad));
      if (cosH > 1 || cosH < -1) return null;
      let H = event === 'rise' ? 360 - Math.acos(cosH) / rad : Math.acos(cosH) / rad;
      H /= 15;
      const T = H + RA - (0.06571 * t) - 6.622;
      let UT = T - lngHour;
      UT = ((UT % 24) + 24) % 24;
      return UT * 60;
    };
    const toLocal = (date, minutesUTC) => {
      const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), 0, Math.round(minutesUTC)));
      return d;
    };
    const fmt = (d) => d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Chicago' });
    const fmtDate = (d) => d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', timeZone: 'America/Chicago' });
    const minutesLocal = (d) => { const p = new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: 'numeric', hour12: false, timeZone: 'America/Chicago' }).formatToParts(d); const h = parseInt(p.find((x) => x.type === 'hour').value, 10) % 24; const m = parseInt(p.find((x) => x.type === 'minute').value, 10); return h * 60 + m; };
    const calc = () => {
      const today = new Date();
      const setD = toLocal(today, solar(today, 'set'));
      const riseD = toLocal(today, solar(today, 'rise'));
      const duskD = toLocal(today, solar(today, 'set', 96));
      const tomorrowRise = toLocal(new Date(today.getTime() + 86400000), solar(new Date(today.getTime() + 86400000), 'rise'));
      out(root, 'date', fmtDate(today) + ' in Austin');
      out(root, 'sunset', fmt(setD)); out(root, 'dusk', fmt(duskD)); out(root, 'sunrise', fmt(riseD));
      const nightMin = (tomorrowRise - setD) / 60000;
      out(root, 'night', `${Math.floor(nightMin / 60)} h ${Math.round(nightMin % 60)} min`);
      // sun position on arc
      const nowM = minutesLocal(new Date()), riseM = minutesLocal(riseD), setM = minutesLocal(setD);
      const p = Math.max(0, Math.min(1, (nowM - riseM) / (setM - riseM)));
      const ang = Math.PI * (1 - p);
      const sun = root.querySelector('[data-out="sun"]'); if (sun) { sun.setAttribute('cx', (150 + 130 * Math.cos(ang)).toFixed(1)); sun.setAttribute('cy', (150 - 130 * Math.sin(ang)).toFixed(1)); sun.style.opacity = (nowM < riseM || nowM > setM) ? '.25' : '1'; }
      // schedule
      const offset = num(form, 'offset');
      const onD = new Date(setD.getTime() + offset * 60000);
      const offSel = val(form, 'off');
      let offD;
      if (offSel === 'dawn') offD = tomorrowRise;
      else if (offSel === '6h') offD = new Date(duskD.getTime() + 6 * 3600000);
      else { const [hh, mm] = offSel.split(':').map(Number); offD = new Date(onD); const onM = minutesLocal(onD); const target = hh * 60 + mm; const delta = ((target - onM) + 1440) % 1440; offD = new Date(onD.getTime() + delta * 60000); }
      out(root, 'on', fmt(onD)); out(root, 'offtime', fmt(offD));
      const hrs = (offD - onD) / 3600000; out(root, 'hours', `${hrs.toFixed(1)} hours`);
      // table
      const rows = [];
      for (let m = 0; m < 12; m++) {
        const d = new Date(today.getFullYear(), m, 1);
        const s = toLocal(d, solar(d, 'set')), du = toLocal(d, solar(d, 'set', 96)), r = toLocal(d, solar(d, 'rise'));
        const on = new Date(s.getTime() + offset * 60000);
        let off;
        if (offSel === 'dawn') { const nd = new Date(d.getTime() + 86400000); off = toLocal(nd, solar(nd, 'rise')); }
        else if (offSel === '6h') off = new Date(du.getTime() + 6 * 3600000);
        else { const [hh, mm] = offSel.split(':').map(Number); const onM = minutesLocal(on); const delta = ((hh * 60 + mm - onM) + 1440) % 1440; off = new Date(on.getTime() + delta * 60000); }
        rows.push(`<tr class="${m === today.getMonth() ? 'is-now' : ''}"><td>${d.toLocaleDateString('en-US', { month: 'long' })}</td><td>${fmt(s)}</td><td>${fmt(du)}</td><td>${fmt(r)}</td><td>${((off - on) / 3600000).toFixed(1)} h</td></tr>`);
      }
      out(root, 'table', rows.join(''));
    };
    form.addEventListener('input', calc); calc();
  };

  /* ---------- Visualizer ---------- */
  const viz = (root) => {
    const boxes = $$('input[type="checkbox"]', root);
    const scene = $('.scene', root);
    const layers = $$('.lamp, [data-layer="stars"]', scene);
    const upd = () => {
      let count = 0;
      boxes.forEach((b) => {
        count += b.checked ? parseInt(b.dataset.count || '0', 10) : 0;
        layers.filter((l) => l.dataset.layer === b.name).forEach((l) => { l.classList.toggle('is-on', b.checked); l.style.opacity = b.checked ? '1' : '0'; });
      });
      const win = boxes.find((b) => b.name === 'window');
      $$('.scene__win', scene).forEach((w) => { w.style.fill = win && win.checked ? '' : '#2a2f3d'; });
      out(root, 'count', count);
      out(root, 'range', count ? range(count * 275, count * 475) : '$0');
    };
    boxes.forEach((b) => b.addEventListener('change', upd));
    scene.classList.add('is-lit');
    upd();
  };

  /* ---------- Quiz ---------- */
  const quiz = (root) => {
    const steps = $$('.quiz__step', root);
    const back = $('[data-quiz="back"]', root), next = $('[data-quiz="next"]', root);
    const bar = $('[data-out="bar"]', root), result = $('[data-out="result"]', root);
    let i = 0;
    const profiles = {
      modern: ['Modern Minimal', 'You want crisp geometry and bold contrast: narrow-beam uplights grazing clean walls, 3000K light, sculptural plants lit from below and very few visible fixtures. Fewer, better fixtures with premium optics.', ['architectural-uplighting', 'custom-lighting-design', 'smart-lighting-systems'], 'modern-landscape-lighting-austin-1'],
      classic: ['Classic Estate', 'Symmetry and warmth. Even 2700K washes on brick or limestone, a lit entry framed by columns, matched path lights and a specimen tree or two. Brass that patinas for decades on an astronomic timer.', ['architectural-uplighting', 'path-and-walkway-lighting', 'garden-and-tree-lighting'], 'landscape-lighting-design-austin-1'],
      hill: ['Hill Country Natural', 'Light that looks like moonlight. Downlights hidden in live oaks, soft 2400K to 2700K accents on native stone, fully shielded fixtures and plenty of darkness left on purpose so the stars stay visible.', ['garden-and-tree-lighting', 'low-voltage-landscape-lighting', 'custom-lighting-design'], 'austin-landscape-tree-lighting-1'],
      resort: ['Resort Entertainer', 'Your backyard is the destination. Layered scenes for the pool, patio and outdoor kitchen, step and wall lights for safety, and app-controlled zones that shift from dinner mode to party mode.', ['deck-and-patio-lighting', 'pool-and-water-feature-lighting', 'smart-lighting-systems'], 'landscape-lighting-ideas-for-pools-1'],
    };
    const names = { 'architectural-uplighting': 'Architectural Uplighting', 'custom-lighting-design': 'Custom Lighting Design', 'smart-lighting-systems': 'Smart Lighting Systems', 'path-and-walkway-lighting': 'Path & Walkway Lighting', 'garden-and-tree-lighting': 'Garden & Tree Lighting', 'low-voltage-landscape-lighting': 'Low-Voltage Lighting', 'deck-and-patio-lighting': 'Deck & Patio Lighting', 'pool-and-water-feature-lighting': 'Pool & Water Feature Lighting' };
    const show = () => {
      steps.forEach((s, k) => { s.hidden = k !== i; });
      bar.style.width = ((i + 1) / steps.length * 100) + '%';
      back.disabled = i === 0;
      next.disabled = !steps[i].querySelector('input:checked');
      next.innerHTML = i === steps.length - 1 ? 'See my style' : 'Next';
    };
    root.addEventListener('change', () => { next.disabled = !steps[i].querySelector('input:checked'); });
    back.addEventListener('click', () => { if (i > 0) { i--; show(); } });
    next.addEventListener('click', () => {
      if (i < steps.length - 1) { i++; show(); return; }
      const tally = {};
      steps.forEach((s) => { const c = s.querySelector('input:checked'); if (c) tally[c.value] = (tally[c.value] || 0) + 1; });
      const win = Object.keys(tally).sort((a, b) => tally[b] - tally[a])[0] || 'classic';
      const [title, desc, svcs, image] = profiles[win];
      result.innerHTML = `<p class="eyebrow">Your lighting style</p><h3>${title}</h3><img src="/assets/img/${image}.webp" alt="${title} landscape lighting example" loading="lazy" style="border-radius:16px"><p>${desc}</p><p><strong>Start with these services:</strong></p><div class="quiz__services">${svcs.map((s) => `<a class="chip" href="/services/${s}/">${names[s]}</a>`).join('')}</div><a class="btn btn--primary" href="/contact/">Design my ${title} lighting</a>`;
      result.hidden = false; $('.quiz__steps', root).hidden = true; $('.quiz__nav', root).hidden = true; bar.style.width = '100%';
    });
    show();
  };

  const init = { fixtures, cost, led, transformer, kelvin, sunset, viz, quiz };
  $$('[data-tool]').forEach((root) => { const fn = init[root.dataset.tool]; if (fn) { try { fn(root); } catch (e) { console.error(root.dataset.tool, e); } } });
})();
