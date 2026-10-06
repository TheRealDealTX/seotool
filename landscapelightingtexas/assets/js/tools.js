/* Landscape Lighting Texas — interactive tools.
   Each widget is a [data-tool] element; markup comes from inc/widgets.php. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, isFinite(v) ? v : a)); };
  var usd = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  var usd2 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var num = function (v, d) { return Number(v).toLocaleString('en-US', { maximumFractionDigits: d || 0, minimumFractionDigits: d || 0 }); };
  function R(root, k, v) { var el = $('[data-r="' + k + '"]', root); if (el) el.textContent = v; return el; }

  // Shared: quantity steppers, slider fill + outputs.
  function wireCommon(root, onChange) {
    $$('.qty-ctrl', root).forEach(function (q) {
      var inp = $('input', q);
      $$('button', q).forEach(function (b) {
        b.addEventListener('click', function () { inp.value = clamp((parseInt(inp.value, 10) || 0) + parseInt(b.getAttribute('data-step'), 10), 0, 100); onChange(); });
      });
    });
    $$('input[type=range].slider', root).forEach(function (s) {
      var paint = function () {
        s.style.setProperty('--fill', ((s.value - s.min) / (s.max - s.min) * 100) + '%');
        var out = $('[data-out="' + s.getAttribute('data-in') + '"]', root);
        if (out) out.textContent = Number(s.value).toLocaleString('en-US');
      };
      s.addEventListener('input', paint); paint();
    });
    root.addEventListener('input', onChange);
    root.addEventListener('change', onChange);
  }
  var val = function (root, sel) { var el = $(sel, root); return el ? parseFloat(el.value) : 0; };

  // Kelvin -> RGB (Tanner Helland approximation).
  function kelvinRGB(k) {
    var t = k / 100, r, g, b;
    r = t <= 66 ? 255 : clamp(329.7 * Math.pow(t - 60, -0.1332), 0, 255);
    g = t <= 66 ? clamp(99.47 * Math.log(t) - 161.12, 0, 255) : clamp(288.12 * Math.pow(t - 60, -0.0755), 0, 255);
    b = t >= 66 ? 255 : (t <= 19 ? 0 : clamp(138.52 * Math.log(t - 10) - 305.04, 0, 255));
    return [Math.round(r), Math.round(g), Math.round(b)];
  }

  /* ================= Cost calculator ================= */
  function cost(root) {
    var F = { uplights: [165, 115, 6], path: [145, 105, 4], garden: [175, 125, 7], step: [130, 120, 3], pool: [260, 190, 10], security: [185, 135, 15] };
    var tiers = [[0, 0], [10, 650], [20, 950], [35, 1350], [50, 1850], [Infinity, 2500]];
    var sizes = [75, 100, 150, 200, 300, 600, 900, 1200];
    var opts = { smart: 900, zone: 425, removal: 600, hardscape: 850 };
    var presets = { front: [6, 6, 2, 0, 0, 0], back: [4, 4, 4, 2, 0, 1], both: [6, 6, 4, 0, 0, 0], full: [10, 10, 8, 4, 0, 2], pool: [2, 2, 4, 4, 3, 0], drive: [4, 10, 0, 0, 0, 0], comm: [12, 12, 4, 0, 0, 6] };
    var keys = Object.keys(F);
    var area = $('[data-f="area"]', root);
    area.addEventListener('change', function () {
      var p = presets[area.value]; keys.forEach(function (k, i) { $('[data-qty="' + k + '"]', root).value = p[i]; }); calc();
    });
    $('[data-reset]', root).addEventListener('click', function () { area.value = 'both'; area.dispatchEvent(new Event('change')); });
    function calc() {
      var mType = val(root, '[data-f="type"]'), mQ = val(root, '[data-f="quality"]'), mD = val(root, '[data-f="diff"]');
      var n = 0, eq = 0, lab = 0, w = 0;
      keys.forEach(function (k) {
        var inp = $('[data-qty="' + k + '"]', root), q = clamp(parseInt(inp.value, 10) || 0, 0, 100);
        n += q; eq += q * F[k][0] * mQ; lab += q * F[k][1] * mD; w += q * F[k][2];
      });
      eq *= mType; lab *= mType;
      var infra = 0; for (var i = 0; i < tiers.length; i++) if (n <= tiers[i][0]) { infra = tiers[i][1]; break; }
      var o = 0; Object.keys(opts).forEach(function (k) { var c = $('[data-opt="' + k + '"]', root); if (c && c.checked) o += opts[k]; });
      var sub = eq + lab + infra + o;
      var lo = Math.round(sub * 0.9 / 50) * 50, hi = Math.round(sub * 1.12 / 50) * 50;
      R(root, 'range', n ? usd.format(lo) + ' – ' + usd.format(hi) : 'Add fixtures');
      R(root, 'count', n); R(root, 'equip', usd.format(eq)); R(root, 'labor', usd.format(lab)); R(root, 'infra', usd.format(infra)); R(root, 'opts', usd.format(o));
      var need = w / 0.8 * ($('[data-opt="expansion"]', root).checked ? 1.2 : 1), size = null;
      for (var j = 0; j < sizes.length; j++) if (need <= sizes[j]) { size = sizes[j]; break; }
      R(root, 'xfmr', !w ? '—' : (size ? size + ' W' : 'Multiple transformers'));
      var load = size ? w / size * 100 : 100;
      var bar = R(root, 'loadbar', ''); bar.style.width = clamp(load, 0, 100) + '%';
      R(root, 'loadtext', w ? Math.round(load) + '% loaded — we size for 80% or less so lamps run cool and you can add fixtures later.' : '');
      var hrs = val(root, '[data-in="hours"]'), rate = clamp(val(root, '[data-f="rate"]'), 0.01, 1);
      var monthly = w / 1000 * hrs * 30 * rate;
      R(root, 'watts', num(w) + ' W'); R(root, 'monthly', usd2.format(monthly)); R(root, 'yearly', usd.format(monthly * 12));
      var scope = n < 12 ? 'a starter system' : n < 25 ? 'a typical front-and-back design' : n < 45 ? 'a whole-property design' : 'an estate-scale design';
      R(root, 'summary', n ? n + ' fixtures is ' + scope + '. Most Texas homes land between $2,500 and $12,000.' : '');
    }
    wireCommon(root, calc); calc();
  }

  /* ================= Simulator ================= */
  function simulator(root) {
    var zones = {
      facade: { mask: 'radial-gradient(22% 30% at 30% 42%, #000 35%, transparent 72%), radial-gradient(22% 30% at 62% 40%, #000 35%, transparent 72%), radial-gradient(14% 26% at 82% 46%, #000 35%, transparent 72%)', fx: 6, w: 5 },
      trees:  { mask: 'radial-gradient(18% 45% at 6% 30%, #000 30%, transparent 75%), radial-gradient(18% 45% at 96% 26%, #000 30%, transparent 75%), radial-gradient(9% 30% at 18% 40%, #000 30%, transparent 75%)', fx: 4, w: 7 },
      path:   { mask: 'radial-gradient(60% 22% at 62% 88%, #000 30%, transparent 75%), radial-gradient(30% 16% at 20% 80%, #000 30%, transparent 75%)', fx: 8, w: 3 },
      entry:  { mask: 'radial-gradient(10% 18% at 54% 50%, #000 35%, transparent 75%), radial-gradient(12% 14% at 36% 48%, #000 30%, transparent 75%), radial-gradient(10% 14% at 72% 50%, #000 30%, transparent 75%)', fx: 2, w: 4 },
      accent: { mask: 'radial-gradient(40% 16% at 45% 68%, #000 30%, transparent 75%), radial-gradient(18% 14% at 90% 66%, #000 30%, transparent 75%)', fx: 5, w: 4 }
    };
    var scenes = {
      welcome: ['facade', 'path', 'entry'], party: ['facade', 'trees', 'path', 'entry', 'accent'],
      security: ['path', 'entry', 'facade'], late: ['path'], all: Object.keys(zones), off: []
    };
    var state = {};
    Object.keys(zones).forEach(function (k) {
      state[k] = false;
      var layer = $('[data-zone-layer="' + k + '"]', root);
      layer.style.webkitMaskImage = layer.style.maskImage = zones[k].mask;
    });
    function render() {
      var dim = val(root, '[data-in="dim"]') / 100, k = val(root, '[data-in="kelvin"]');
      var on = 0, fx = 0, w = 0;
      Object.keys(zones).forEach(function (z) {
        var layer = $('[data-zone-layer="' + z + '"]', root);
        layer.style.opacity = state[z] ? (0.35 + dim * 0.65).toFixed(2) : 0;
        layer.style.filter = 'brightness(' + (0.7 + dim * 0.5).toFixed(2) + ')';
        $('[data-zone="' + z + '"]', root).setAttribute('aria-pressed', state[z]);
        if (state[z]) { on++; fx += zones[z].fx; w += zones[z].fx * zones[z].w * dim; }
      });
      var rgb = kelvinRGB(k), tint = $('[data-tint]', root);
      tint.style.background = 'rgb(' + rgb.join(',') + ')';
      tint.style.opacity = on ? (0.12 + Math.abs(k - 2700) / 2300 * 0.4).toFixed(2) : 0;
      root.classList.toggle('sim-dark', on === 0);
      R(root, 'zones', on); R(root, 'fx', fx); R(root, 'w', Math.round(w) + ' W');
      R(root, 'cost', usd2.format(w / 1000 * 6 * 30 * 0.15));
    }
    $$('[data-zone]', root).forEach(function (b) {
      b.addEventListener('click', function () { state[b.getAttribute('data-zone')] = !state[b.getAttribute('data-zone')]; $$('[data-scene]', root).forEach(function (s) { s.classList.remove('is-on'); }); render(); });
    });
    $$('[data-scene]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        var s = b.getAttribute('data-scene');
        Object.keys(state).forEach(function (z) { state[z] = scenes[s].indexOf(z) > -1; });
        var dims = { late: 35, security: 100, welcome: 80, party: 90, all: 100 };
        if (dims[s]) { var d = $('[data-in="dim"]', root); d.value = dims[s]; d.dispatchEvent(new Event('input', { bubbles: true })); }
        $$('[data-scene]', root).forEach(function (x) { x.classList.toggle('is-on', x === b); });
        render();
      });
    });
    wireCommon(root, render);
    render();
    // Turn zones on one by one when the simulator first scrolls into view.
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return; io.disconnect();
        ['path', 'accent', 'facade', 'trees', 'entry'].forEach(function (z, i) {
          setTimeout(function () { state[z] = true; render(); }, 500 + i * 550);
        });
      }, { threshold: 0.45 });
      io.observe(root);
    }
  }

  /* ================= Kelvin visualizer ================= */
  function kelvin(root) {
    var info = [
      [2200, 'Candlelight amber', 'Very warm and intimate, close to firelight. Makes stone look honey-toned but can muddy greens.', 'Patios, fire features, historic homes and dark-sky-sensitive properties.'],
      [2600, 'Warm white', 'The classic landscape lighting look: inviting and residential, flattering on limestone, brick and wood.', 'Facades, entries, paths and most Texas homes. Our default for architecture.'],
      [3100, 'Soft white', 'Slightly crisper while still warm. Greens read more natural and white stone looks cleaner.', 'Trees and foliage, modern homes, mixed architecture and planting designs.'],
      [3700, 'Neutral white', 'Clean and bright. Starts to feel commercial on homes, but renders foliage vividly.', 'Specimen plants, silver foliage, contemporary commercial exteriors.'],
      [4500, 'Cool white', 'Moonlight-like and crisp. Can feel stark or clinical against warm materials.', 'Moonlighting effects in large trees, water features and security zones.'],
      [5100, 'Daylight', 'Blue-white and harsh at night; draws more insects and reads as a parking lot.', 'Rarely recommended for residential landscapes. Utility and security only.']
    ];
    var img = $('[data-k-img]', root);
    $$('[data-img]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        img.src = '/assets/img/' + b.getAttribute('data-img') + '-1600.webp';
        $$('[data-img]', root).forEach(function (x) { x.classList.toggle('is-on', x === b); });
      });
    });
    function render() {
      var k = val(root, '[data-in="kelvin"]'), rgb = kelvinRGB(k), row = info[info.length - 1];
      for (var i = 0; i < info.length; i++) if (k < info[i][0]) { row = info[i]; break; }
      var t = $('[data-tint]', root), t2 = $('[data-tint2]', root);
      t.style.background = 'rgb(' + rgb.join(',') + ')';
      t.style.opacity = (0.25 + Math.abs(k - 2700) / 2300 * 0.45).toFixed(2);
      t2.style.background = k > 3500 ? 'rgba(170,200,255,' + ((k - 3500) / 1500 * 0.5).toFixed(2) + ')' : 'rgba(255,170,80,' + ((3500 - k) / 1300 * 0.35).toFixed(2) + ')';
      R(root, 'k', num(k) + 'K'); R(root, 'name', row[1]); R(root, 'desc', row[2]); R(root, 'best', row[3]);
    }
    wireCommon(root, render); render();
  }

  /* ================= Transformer ================= */
  function transformer(root) {
    var W = { a: 5, b: 3, c: 7, d: 10 };
    var ohms = { 16: 4.016, 14: 2.525, 12: 1.588, 10: 0.999, 8: 0.628 }; // per 1,000 ft, one conductor
    var sizes = [60, 75, 100, 150, 200, 300, 600, 900, 1200];
    function calc() {
      var w = 0; Object.keys(W).forEach(function (k) { w += (parseInt($('[data-qty="' + k + '"]', root).value, 10) || 0) * W[k]; });
      var len = val(root, '[data-in="len"]'), awg = $('[data-f="awg"]', root).value, method = val(root, '[data-f="method"]'), vmin = val(root, '[data-f="min"]');
      var need = w / 0.8, size = null;
      for (var i = 0; i < sizes.length; i++) if (need <= sizes[i]) { size = sizes[i]; break; }
      var amps = w / 12;
      var drop = 2 * len * amps * ohms[awg] / 1000 * method;
      var taps = [12, 13, 14, 15], tap = null;
      for (var j = 0; j < taps.length; j++) if (taps[j] - drop >= 10.8 && taps[j] - drop <= 12.6) { tap = taps[j]; break; }
      if (!tap) tap = drop < 0.6 ? 12 : 15;
      var vf = tap - drop;
      R(root, 'xfmr', !w ? '—' : (size ? size + ' W' : 'Split into 2+ transformers'));
      var load = size ? w / size * 100 : 100;
      var bar = R(root, 'bar', ''); bar.style.width = clamp(load, 0, 100) + '%';
      bar.parentElement.classList.toggle('warn', load > 80);
      R(root, 'bartext', w ? Math.round(load) + '% of transformer capacity (aim for 80% or less)' : '');
      R(root, 'watts', num(w) + ' W'); R(root, 'amps', num(amps, 1) + ' A'); R(root, 'drop', num(drop, 2) + ' V');
      R(root, 'tap', tap + ' V tap'); R(root, 'vfix', num(vf, 1) + ' V');
      var adv;
      if (!w) adv = 'Add fixtures to size the run.';
      else if (amps > 25) adv = 'Over 25 A on one run is too much for landscape cable. Split this load across two or more runs from the transformer.';
      else if (vf < vmin || drop > 3) adv = 'Voltage drop is high. Use heavier wire (' + (awg > 10 ? (awg - 2) : 8) + ' AWG), shorten the run, or split the load with hub wiring.';
      else if (drop < 0.6) adv = 'Drop is minimal — the 12 V tap is fine and every fixture will see close to full voltage.';
      else adv = 'Use the ' + tap + ' V tap so fixtures at the end of the run receive about ' + num(vf, 1) + ' V. Verify with a meter at the farthest fixture.';
      R(root, 'advice', adv);
    }
    wireCommon(root, calc); calc();
  }

  /* ================= Beam spread ================= */
  function beam(root) {
    var angle = 36;
    $$('[data-angle]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        angle = +b.getAttribute('data-angle');
        $$('[data-angle]', root).forEach(function (x) { x.classList.toggle('is-on', x === b); }); calc();
      });
    });
    function calc() {
      var d = val(root, '[data-in="dist"]'), lm = val(root, '[data-in="lumens"]'), target = val(root, '[data-f="target"]');
      var spread = 2 * d * Math.tan(angle / 2 * Math.PI / 180);
      var areaFt = Math.PI * Math.pow(spread / 2, 2);
      var fc = lm * 0.7 / areaFt; // ~70% of lumens inside the beam
      // Diagram: fixture at bottom, distance maps to 220px height.
      var half = clamp(Math.tan(angle / 2 * Math.PI / 180) * 220, 4, 190);
      $('[data-beam]', root).setAttribute('points', '200,240 ' + (200 - half) + ',20 ' + (200 + half) + ',20');
      var sp = $('[data-spread]', root); sp.setAttribute('x1', 200 - half); sp.setAttribute('x2', 200 + half);
      $('[data-label]', root).textContent = num(spread, 1) + ' ft wide at ' + d + ' ft';
      R(root, 'spread', num(spread, 1) + ' ft');
      R(root, 'area', num(areaFt) + ' sq ft');
      R(root, 'fc', num(fc, 1) + ' fc');
      var need = 2 * Math.atan(target / 2 / d) * 180 / Math.PI;
      var opts = [10, 15, 25, 36, 45, 60], rec = 60;
      for (var i = 0; i < opts.length; i++) if (opts[i] >= need * 0.85) { rec = opts[i]; break; }
      R(root, 'rec', rec + '°' + (need > 60 ? ' (use 2+ fixtures)' : ''));
      R(root, 'advice', fc < 1 ? 'Under 1 footcandle reads as a soft glow — use a narrower beam, more lumens, or a second fixture.'
        : fc > 15 ? 'That is very bright for landscape lighting. Dim it, widen the beam or step down the lumen package to avoid hot spots.'
        : 'A comfortable accent level for most landscape features. Cross-light from a second angle for depth.');
    }
    wireCommon(root, calc); calc();
  }

  /* ================= Dusk timer (NOAA solar position) ================= */
  function sunTimes(date, lat, lon, zenith) {
    var rad = Math.PI / 180;
    var start = Date.UTC(date.getFullYear(), 0, 0), doy = Math.floor((Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) - start) / 864e5);
    function calcT(rising) {
      var lngHour = lon / 15, t = doy + ((rising ? 6 : 18) - lngHour) / 24;
      var M = 0.9856 * t - 3.289;
      var L = (M + 1.916 * Math.sin(M * rad) + 0.020 * Math.sin(2 * M * rad) + 282.634 + 360) % 360;
      var RA = (Math.atan(0.91764 * Math.tan(L * rad)) / rad + 360) % 360;
      RA = (RA + (Math.floor(L / 90) * 90 - Math.floor(RA / 90) * 90)) / 15;
      var sinDec = 0.39782 * Math.sin(L * rad), cosDec = Math.cos(Math.asin(sinDec));
      var cosH = (Math.cos(zenith * rad) - sinDec * Math.sin(lat * rad)) / (cosDec * Math.cos(lat * rad));
      var H = rising ? 360 - Math.acos(cosH) / rad : Math.acos(cosH) / rad;
      var T = H / 15 + RA - 0.06571 * t - 6.622;
      var UT = ((T - lngHour) % 24 + 24) % 24;
      return new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) + UT * 36e5);
    }
    return { rise: calcT(true), set: calcT(false) };
  }
  function dusk(root) {
    var dateEl = $('[data-f="date"]', root), now = new Date();
    dateEl.value = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
    function fmt(d, tz) { return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: tz }); }
    function calc() {
      var c = $('[data-f="city"]', root).value.split(','), lat = +c[0], lon = +c[1], tz = c[2];
      var parts = (dateEl.value || '').split('-'), date = parts.length === 3 ? new Date(+parts[0], +parts[1] - 1, +parts[2]) : new Date();
      var s = sunTimes(date, lat, lon, 90.833), cd = sunTimes(date, lat, lon, 96);
      var on = new Date(s.set.getTime() + 15 * 6e4);
      R(root, 'sunset', fmt(s.set, tz)); R(root, 'dusk', fmt(cd.set, tz)); R(root, 'on', fmt(on, tz)); R(root, 'sunrise', fmt(s.rise, tz));
      var off = $('[data-f="off"]', root).value, hours;
      var next = sunTimes(new Date(date.getTime() + 864e5), lat, lon, 90.833);
      if (off === 'dawn') hours = (next.rise - on) / 36e5;
      else {
        var localSet = new Date(on.toLocaleString('en-US', { timeZone: tz })), offH = +off;
        var offD = new Date(localSet); offD.setHours(offH, 0, 0, 0); if (offH < 12) offD.setDate(offD.getDate() + 1);
        hours = (offD - localSet) / 36e5;
      }
      R(root, 'hours', num(Math.max(0, hours), 1) + ' h');
      R(root, 'advice', 'Astronomical timers and smart transformers follow these times automatically. With a plain photocell, keep it shaded from your own fixtures; with a basic clock timer, update it monthly — especially around the daylight saving changes in March and November.');
      var rows = '', months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      for (var m = 0; m < 12; m++) {
        var d = new Date(date.getFullYear(), m, 15), st = sunTimes(d, lat, lon, 90.833).set;
        var rounded = new Date(Math.ceil((st.getTime() + 15 * 6e4) / 9e5) * 9e5);
        rows += '<tr' + (m === date.getMonth() ? ' class="is-now"' : '') + '><td>' + months[m] + '</td><td>' + fmt(st, tz) + '</td><td>' + fmt(rounded, tz) + '</td></tr>';
      }
      $('[data-r="months"]', root).innerHTML = rows;
    }
    wireCommon(root, calc); calc();
  }

  /* ================= Energy ================= */
  function energy(root) {
    function calc() {
      var n = val(root, '[data-in="n"]'), hw = val(root, '[data-in="hw"]'), lw = val(root, '[data-in="lw"]'), h = val(root, '[data-in="h"]');
      var rate = clamp(val(root, '[data-f="rate"]'), 0.01, 1), cost = clamp(val(root, '[data-f="cost"]'), 0, 5000);
      var hal = n * hw * h * 365 / 1000 * rate, led = n * lw * h * 365 / 1000 * rate, save = hal - led;
      var hoursYear = h * 365, lampsAvoided = Math.max(0, Math.floor(hoursYear * 10 / 3000) - Math.floor(hoursYear * 10 / 40000)) * n;
      R(root, 'save', usd.format(save)); R(root, 'hal', usd.format(hal) + '/yr'); R(root, 'led', usd.format(led) + '/yr');
      $('[data-r="halbar"]', root).style.width = '100%';
      $('[data-r="ledbar"]', root).style.width = (hal ? led / hal * 100 : 0) + '%';
      R(root, 'kwh', num(n * (hw - lw) * h * 365 / 1000) + ' kWh');
      R(root, 'payback', save > 0 ? num(cost * n / save, 1) + ' years' : '—');
      R(root, 'lamps', num(lampsAvoided));
      R(root, 'ten', usd.format(save * 10 + lampsAvoided * 8));
    }
    wireCommon(root, calc); calc();
  }

  /* ================= Quiz ================= */
  function quiz(root) {
    var Q = [
      ['What style is your home?', [['Traditional / Texas stone', 'Limestone, brick, gables', 'arch'], ['Modern / contemporary', 'Clean lines, stucco, glass', 'modern'], ['Hill Country / ranch', 'Big lot, native landscape', 'ranch'], ['Mediterranean / Spanish', 'Stucco, tile, courtyards', 'garden']]],
      ['What is the star of your yard?', [['Mature trees', 'Live oaks, pecans, elms', 'trees'], ['The house itself', 'Facade, columns, stonework', 'arch'], ['Pool or patio', 'Where you entertain', 'living'], ['Gardens and beds', 'Plants, sculpture, texture', 'garden']]],
      ['What matters most at night?', [['Curb appeal', 'Wow from the street', 'arch'], ['Safety', 'Steps, paths, driveway', 'safety'], ['Entertaining', 'Evenings outside', 'living'], ['Security', 'No dark corners', 'safety']]],
      ['How do you want it to feel?', [['Warm and welcoming', '', 'arch'], ['Dramatic and moody', '', 'trees'], ['Bright and resort-like', '', 'living'], ['Natural, like moonlight', '', 'ranch']]],
      ['How hands-on do you want controls?', [['Set it and forget it', 'Astronomical timer', 'simple'], ['App and scenes', 'Dim, zone, schedule', 'smart'], ['Full smart-home integration', 'Voice, automations', 'smart']]],
      ['Rough budget?', [['Starter: $2,500–$5,000', '', 'starter'], ['Signature: $5,000–$12,000', '', 'signature'], ['Estate: $12,000+', '', 'estate'], ['Not sure yet', '', 'signature']]]
    ];
    var styles = {
      arch: ['The Architectural Statement', 'Your home is the hero. Grazed stone, lit columns and a balanced facade, framed by softly lit paths.', '/services/architectural-uplighting/', 'architectural-uplighting'],
      trees: ['The Moonlit Canopy', 'Big trees, big drama. Uplit trunks and moonlighting from the canopy create dappled light across the lawn.', '/services/garden-tree-lighting/', 'oak-tree-uplighting'],
      living: ['The Backyard Resort', 'Layered pool, patio and string lighting that turns long Texas evenings into the best part of the day.', '/services/pool-water-feature-lighting/', 'pool-lighting'],
      garden: ['The Garden Gallery', 'Texture and depth: accent lights on specimen plants, beds and sculpture with warm path light between.', '/services/garden-tree-lighting/', 'garden-pathway-lighting'],
      safety: ['The Safe Arrival', 'Even, glare-free light on every path, step and drive, with shielded security lighting on the corners.', '/services/pathway-driveway-lighting/', 'driveway-lighting'],
      ranch: ['The Hill Country Night', 'Subtle, dark-sky-friendly lighting that lets the stars stay bright while trees and paths glow softly.', '/services/garden-tree-lighting/', 'oak-tree-uplighting']
    };
    var i = 0, score = {}, extra = {};
    var stage = $('[data-r="stage"]', root), prog = $('[data-r="progress"]', root);
    function show() {
      prog.style.width = (i / Q.length * 100) + '%';
      if (i >= Q.length) return result();
      var q = Q[i];
      stage.innerHTML = '<div class="quiz-q"><p class="result-label">Question ' + (i + 1) + ' of ' + Q.length + '</p><h3>' + q[0] + '</h3><div class="quiz-opts">' +
        q[1].map(function (o, k) { return '<button type="button" class="quiz-opt" data-k="' + k + '">' + o[0] + (o[1] ? '<small>' + o[1] + '</small>' : '') + '</button>'; }).join('') + '</div></div>';
      $$('.quiz-opt', stage).forEach(function (b) {
        b.addEventListener('click', function () {
          var tag = q[1][+b.getAttribute('data-k')][2];
          if (styles[tag]) score[tag] = (score[tag] || 0) + 1; else extra[i] = tag;
          i++; show();
        });
      });
    }
    function result() {
      var best = 'arch', max = -1;
      Object.keys(score).forEach(function (k) { if (score[k] > max) { max = score[k]; best = k; } });
      var s = styles[best], smart = extra[4] === 'smart', budget = extra[5] || 'signature';
      var budgets = { starter: '8–14 fixtures · $2,500–$5,000', signature: '15–30 fixtures · $5,000–$12,000', estate: '30+ fixtures · $12,000–$20,000+' };
      stage.innerHTML = '<div class="quiz-result grid-2" style="align-items:center"><img src="/assets/img/' + s[3] + '-800.webp" alt="" style="border-radius:16px;aspect-ratio:3/2;object-fit:cover" width="800" height="533">' +
        '<div><p class="result-label">Your lighting style</p><h3 style="font-size:2rem">' + s[0] + '</h3><p style="color:var(--muted)">' + s[1] + '</p>' +
        '<dl class="kv"><div><dt>Suggested scope</dt><dd>' + budgets[budget] + '</dd></div><div><dt>Controls</dt><dd>' + (smart ? 'Smart app + scenes' : 'Astronomical timer') + '</dd></div><div><dt>Color temperature</dt><dd>' + (best === 'ranch' ? '2700K, shielded' : best === 'trees' ? '2700K–3000K' : '2700K') + '</dd></div></dl>' +
        '<div class="hero-actions" style="margin-top:10px"><a class="btn btn-gold" href="/quote/">Get this plan quoted</a><a class="btn btn-ghost" href="' + s[2] + '">See the service</a></div>' +
        '<p style="margin-top:14px"><button type="button" class="link-arrow" style="background:none;border:0;cursor:pointer" data-restart>Retake the quiz</button></p></div></div>';
      $('[data-restart]', stage).addEventListener('click', function () { i = 0; score = {}; extra = {}; show(); });
    }
    show();
  }

  var tools = { cost: cost, simulator: simulator, kelvin: kelvin, transformer: transformer, beam: beam, dusk: dusk, energy: energy, quiz: quiz };
  $$('[data-tool]').forEach(function (el) {
    var fn = tools[el.getAttribute('data-tool')];
    if (fn) try { fn(el); } catch (e) { if (window.console) console.error(e); }
  });
})();
