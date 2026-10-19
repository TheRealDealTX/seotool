/* Texas Landscape Lights — interactive planning tools */
(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const money = (v, dec = 2) => '$' + (isFinite(v) ? v : 0).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const num = (v, dec = 0) => (isFinite(v) ? v : 0).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const RATE = 0.15;
  const TX_SIZES = [150, 200, 300, 600, 900, 1200];
  const txFor = w => { const need = w / 0.8; const s = TX_SIZES.find(x => x >= need); return s ? s + ' W' : Math.ceil(need / 1200) + ' × 1200 W'; };

  /** Kelvin → RGB (Tanner Helland approximation). */
  function kelvin(k) {
    const t = k / 100;
    const r = t <= 66 ? 255 : 329.698727446 * Math.pow(t - 60, -0.1332047592);
    const g = t <= 66 ? 99.4708025861 * Math.log(t) - 161.1195681661 : 288.1221695283 * Math.pow(t - 60, -0.0755148492);
    const b = t >= 66 ? 255 : t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307;
    const c = v => Math.round(Math.min(255, Math.max(0, v)));
    return `rgb(${c(r)},${c(g)},${c(b)})`;
  }
  const kInfo = k => k < 2500 ? ['Amber / candlelight', 'Very warm, intimate, vintage', 'Best for string lights, historic homes and old Chicago brick. Can muddy greens and blues.']
    : k < 2900 ? ['Warm white', 'Cozy, residential, flattering', 'The go-to for most Texas homes: red brick, Austin stone, cedar and entries. Inviting without looking yellow.']
    : k < 3500 ? ['Soft white', 'Crisp but still warm', 'Great on white limestone, light stucco, live oaks and full-property designs.']
    : k < 4500 ? ['Neutral / cool white', 'Clean, modern, moonlike', 'Use selectively: moonlighting, silver foliage like Texas sage, agave and contemporary architecture.']
    : ['Daylight', 'Stark, commercial', 'Rarely flattering on homes. Reserve for signage, special effects or water features.'];
  const fill = r => r.style.setProperty('--fill', ((r.value - r.min) / (r.max - r.min) * 100) + '%');
  const bind = (root, fn) => {
    const run = () => {
      $$('input[type=range]', root).forEach(r => { fill(r); const o = $(`output[data-out="${r.dataset.in}"]`, root); if (o) o.textContent = r.value; });
      fn();
    };
    root.addEventListener('input', run); root.addEventListener('change', run); run();
  };
  const val = (root, k) => { const el = $(`[data-in="${k}"]`, root); return el.type === 'checkbox' ? el.checked : (isNaN(parseFloat(el.value)) ? el.value : parseFloat(el.value)); };
  const out = (root, k, v) => { const el = $(`[data-out="${k}"]`, root); if (el) el.textContent = v; return el; };

  /* ---------- Visualizer ---------- */
  $$('[data-tool="visualizer"]').forEach(root => {
    const stage = $('.scene', root);
    const LAYERS = { arch: { fx: 6, w: 6 }, path: { fx: 6, w: 3 }, tree: { fx: 5, w: 9 }, patio: { fx: 10, w: 1.5 } };
    const PRESETS = {
      subtle: { arch: true, path: true, tree: false, patio: false, k: 2700, int: 55 },
      balanced: { arch: true, path: true, tree: true, patio: true, k: 2700, int: 100 },
      showcase: { arch: true, path: true, tree: true, patio: true, k: 3000, int: 100 },
      welcome: { arch: false, path: true, tree: false, patio: false, k: 2700, int: 80 },
    };
    $$('[data-layer]', root).forEach(i => i.dataset.in = 'layer-' + i.dataset.layer);
    const update = () => {
      const k = val(root, 'k'), int = val(root, 'int') / 100, col = kelvin(k);
      stage.style.setProperty('--lc', col); stage.style.setProperty('--int', .35 + int * .65);
      let fx = 0, w = 0;
      Object.keys(LAYERS).forEach(l => {
        const on = val(root, 'layer-' + l);
        $$('.lt-' + l, stage).forEach(g => g.style.opacity = on ? 1 : 0);
        if (on) { fx += LAYERS[l].fx; w += LAYERS[l].fx * LAYERS[l].w * (0.4 + int * .6); }
      });
      out(root, 'k', k + 'K'); out(root, 'int', Math.round(int * 100) + '%'); out(root, 'kname', kInfo(k)[0]);
      out(root, 'fx', fx); out(root, 'w', Math.round(w) + ' W');
      out(root, 'mo', money(w * 6 * 30 / 1000 * RATE)); out(root, 'tx', w ? txFor(w) : '—');
    };
    $$('[data-preset]', root).forEach(b => b.addEventListener('click', () => {
      const p = PRESETS[b.dataset.preset];
      Object.keys(LAYERS).forEach(l => $(`[data-layer="${l}"]`, root).checked = p[l]);
      $('[data-in="k"]', root).value = p.k; $('[data-in="int"]', root).value = p.int;
      $$('[data-preset]', root).forEach(x => x.classList.toggle('is-on', x === b));
      root.dispatchEvent(new Event('input'));
    }));
    stage.classList.add('win-on');
    bind(root, update);
  });

  /* ---------- Energy cost ---------- */
  $$('[data-tool="energy"]').forEach(root => {
    $$('[data-set]', root).forEach(b => b.addEventListener('click', () => {
      Object.entries(JSON.parse(b.dataset.set)).forEach(([k, v]) => $(`[data-in="${k}"]`, root).value = v);
      root.dispatchEvent(new Event('input'));
    }));
    bind(root, () => {
      const n = val(root, 'n'), w = val(root, 'w'), h = val(root, 'h'), r = val(root, 'r') / 100;
      const tw = n * w, kn = tw * h / 1000, km = kn * 30.4, ky = kn * 365;
      out(root, 'tw', num(tw, tw % 1 ? 1 : 0) + ' W'); out(root, 'kn', num(kn, 2) + ' kWh'); out(root, 'km', num(km, 1) + ' kWh'); out(root, 'ky', num(ky, 0) + ' kWh');
      out(root, 'mo', money(km * r)); out(root, 'cn', money(kn * r)); out(root, 'cy', money(ky * r, 0)); out(root, 'rv', (r * 100).toFixed(1) + '¢');
      const m = out(root, 'msg', km * r < 5 ? 'A low operating cost for a full outdoor lighting system. LED makes a big difference here.' : km * r < 15 ? 'A moderate operating cost. Zoning and a shorter late-night schedule can trim it further.' : 'On the higher side. Check for halogen lamps, oversized wattages or all-night schedules: an LED upgrade or a smarter timer could cut this substantially.');
      m.classList.toggle('is-warn', km * r >= 15);
    });
  });

  /* ---------- Fixture estimator ---------- */
  $$('[data-tool="estimator"]').forEach(root => bind(root, () => {
    const s = val(root, 'style');
    const rows = [
      ['Facade uplights / washes', Math.ceil(val(root, 'facade') / 10 * s), 6],
      ['Columns, gables & entry accents', Math.round(val(root, 'cols') * s), 4],
      ['Walkway path lights', Math.ceil(val(root, 'walk') / 9 * s), 3],
      ['Driveway markers', Math.ceil(val(root, 'drive') / 16 * s), 3],
      ['Large tree uplights (live oak, pecan)', Math.round(val(root, 'big') * 2.5 * s), 9],
      ['Small tree / palm / yucca accents', Math.round(val(root, 'small') * 1.2 * s), 5],
      ['Patio / outdoor living', Math.ceil(val(root, 'patio') / 80 * s), 3],
      ['Step & wall lights', Math.round(val(root, 'steps') * s), 2],
    ].filter(r => r[1] > 0);
    let total = 0, watts = 0;
    $('[data-out="rows"]', root).innerHTML = rows.map(([a, n, w]) => { total += n; watts += n * w; return `<tr><td>${a}</td><td>${n}</td><td>${n * w} W</td></tr>`; }).join('') || '<tr><td colspan="3">Add some areas to light.</td></tr>';
    out(root, 'total', total); out(root, 'watts', Math.round(watts) + ' W'); out(root, 'tx', watts ? txFor(watts) : '—');
    out(root, 'sum', `≈ ${Math.round(watts)} W of LED · about ${money(watts * 6 * 30 / 1000 * RATE)} a month to run*`);
  }));

  /* ---------- Transformer + voltage drop ---------- */
  $$('[data-tool="transformer"]').forEach(root => bind(root, () => {
    const total = val(root, 'n') * val(root, 'w');
    out(root, 'tx', txFor(total)); out(root, 'txs', `${num(total, total % 1 ? 1 : 0)} W load ÷ 0.8 = ${num(total / .8, 0)} W minimum`);
    const load = val(root, 'load'), len = val(root, 'len'), ohm = val(root, 'g'), tap = val(root, 'tap');
    const amps = load / 12, vd = amps * (2 * len * ohm / 1000), vend = tap - vd;
    out(root, 'amps', num(amps, 1) + ' A'); out(root, 'vd', num(vd, 2) + ' V'); out(root, 'vend', num(vend, 1) + ' V');
    out(root, 'best', ([12, 13, 14, 15].find(t => t - vd >= 10.8) || 15) + ' V');
    let msg = vend >= 10.5 && vend <= 12.5 ? 'Within a typical 10.5–12.5 V target at the fixtures.' : vend > 12.5 ? 'Voltage at the end is high. Use a lower tap or confirm your fixtures accept it.' : 'Too much drop. Try a higher tap, heavier wire, a shorter run or splitting the load (hub or T-method wiring).';
    if (amps > 20) msg = 'Over 20 A on one run is not recommended: split this load across more home runs.';
    out(root, 'msg', msg).classList.toggle('is-warn', !(vend >= 10.5 && vend <= 12.5) || amps > 20);
  }));

  /* ---------- LED savings ---------- */
  $$('[data-tool="led"]').forEach(root => bind(root, () => {
    const n = val(root, 'n'), hw = val(root, 'hw'), lw = val(root, 'lw'), h = val(root, 'h'), r = val(root, 'r') / 100, lamp = val(root, 'lamp'), cost = val(root, 'cost');
    const hrs = h * 365, kh = n * hw * hrs / 1000, kl = n * lw * hrs / 1000, ch = kh * r, cl = kl * r;
    const lamps = n * hrs / 3000, lampc = lamps * lamp, save = ch - cl + lampc;
    out(root, 'save', money(save, 0)); out(root, 'pct', `${Math.round((1 - lw / hw) * 100)}% less energy, plus far fewer lamp changes`);
    out(root, 'ch', money(ch, 0)); out(root, 'cl', money(cl, 0));
    $('[data-out="bh"]', root).style.width = '100%'; $('[data-out="bl"]', root).style.width = Math.max(2, cl / ch * 100) + '%';
    out(root, 'kwh', num(kh - kl)); out(root, 'lamps', num(lamps)); out(root, 'lampc', money(lampc, 0));
    out(root, 'pay', cost > 0 && save > 0 ? num(cost * n / save, 1) + ' yrs' : '—');
  }));

  /* ---------- Color temperature ---------- */
  $$('[data-tool="kelvin"]').forEach(root => {
    $$('[data-k]', root).forEach(b => b.addEventListener('click', () => { $('[data-in="k"]', root).value = b.dataset.k; root.dispatchEvent(new Event('input')); }));
    bind(root, () => {
      const k = val(root, 'k'), col = kelvin(k), [name, feel, best] = kInfo(k);
      const t = $('[data-out="tint"]', root); t.style.background = col; t.style.color = col;
      $$('.swatch__s', root).forEach(s => s.style.setProperty('--lc', col));
      out(root, 'k', k + 'K'); out(root, 'kbig', k + 'K'); out(root, 'kname', name); out(root, 'kfeel', feel); out(root, 'kbest', best);
      out(root, 'kdesc', k <= 3000 ? 'Warm light makes reds, browns and golds glow and feels like home. Most residential landscape lighting in Texas is designed between 2700K and 3000K.' : 'Cooler light renders greens and blues crisply and reads like moonlight, but it can make brick, cedar and warm stone look flat or gray.');
      $$('[data-k]', root).forEach(b => b.classList.toggle('is-on', +b.dataset.k === k));
    });
  });

  /* ---------- Sunset planner (solar position, any Texas city) ---------- */
  function sunTimes(date, LAT, LON) {
    const rad = Math.PI / 180, day = Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
    const n = Math.ceil(day / 864e5 + 2440587.5 - 2451545 + .0008);
    const J = n - LON / 360, M = (357.5291 + .98560028 * J) % 360;
    const C = 1.9148 * Math.sin(M * rad) + .02 * Math.sin(2 * M * rad) + .0003 * Math.sin(3 * M * rad);
    const L = (M + C + 180 + 102.9372) % 360;
    const Jt = 2451545 + J + .0053 * Math.sin(M * rad) - .0069 * Math.sin(2 * L * rad);
    const dec = Math.asin(Math.sin(L * rad) * Math.sin(23.4397 * rad));
    const w = Math.acos((Math.sin(-.833 * rad) - Math.sin(LAT * rad) * Math.sin(dec)) / (Math.cos(LAT * rad) * Math.cos(dec))) / rad;
    const toDate = jd => new Date((jd - 2440587.5) * 864e5);
    return { rise: toDate(Jt - w / 360), set: toDate(Jt + w / 360) };
  }
  $$('[data-tool="sunset"]').forEach(root => {
    const cities = JSON.parse(root.dataset.cities);
    bind(root, () => {
      const c = cities[val(root, 'city')], tz = c.tz || 'America/Chicago';
      const ct = d => d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: tz });
      const ctH = d => { const p = new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: 'numeric', hourCycle: 'h23', timeZone: tz }).formatToParts(d); return +p.find(x => x.type === 'hour').value + p.find(x => x.type === 'minute').value / 60; };
      const on = +val(root, 'on'), off = val(root, 'off'), w = val(root, 'w'), y = new Date().getFullYear();
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], cur = new Date().getMonth();
      let year = 0, rows = '';
      months.forEach((m, i) => {
        const t = sunTimes(new Date(y, i, 15), c.la, c.lo), sOn = ctH(t.set) + on / 60;
        const sOff = off === 'dawn' ? ctH(t.rise) + 24 : +off;
        const hrs = Math.max(0, sOff - sOn), days = new Date(y, i + 1, 0).getDate();
        year += hrs * days;
        rows += `<tr${i === cur ? ' class="is-now"' : ''}><td>${m}</td><td>${ct(t.set)}</td><td>${ct(t.rise)}</td><td>${ct(new Date(t.set.getTime() + on * 6e4))}</td><td>${num(hrs, 1)} h</td></tr>`;
      });
      $('[data-out="rows"]', root).innerHTML = rows;
      out(root, 'cname', c.n); out(root, 'today', ct(sunTimes(new Date(), c.la, c.lo).set));
      out(root, 'hrs', num(year)); out(root, 'kwh', num(year * w / 1000)); out(root, 'cost', money(year * w / 1000 * RATE, 0));
    });
  });
})();
