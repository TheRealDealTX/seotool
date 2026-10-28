(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('pal-form'), out = document.getElementById('pal-result');
  if (!form) return;

  var PRESETS = [
    ['Lavender & Sage', ['#d9d2e6', '#9aa58c', '#6b4f8a', '#f6f3ee', '#4a4540']],
    ['Greige & Brass', ['#d8d0c4', '#8f857a', '#b88a2e', '#f7f3ea', '#3a352f']],
    ['Navy & Cognac', ['#e9e4da', '#23334d', '#a5673f', '#f8f6f0', '#2b2620']],
    ['Blush & Terracotta', ['#f1ddd5', '#c98b6b', '#9c4a32', '#fbf6f1', '#4d3b33']],
    ['Charcoal & Camel', ['#e7e2da', '#3c3d3f', '#c19a6b', '#f7f5f0', '#1f1f20']],
    ['Sage & Oak', ['#dfe3d5', '#a98b65', '#5f6f52', '#f6f4ec', '#3e3a33']]
  ];
  var current = null;

  function hexToHsl(hex) {
    var m = /^#?([0-9a-f]{6})$/i.exec(hex); if (!m) return null;
    var n = parseInt(m[1], 16), r = (n >> 16) / 255, g = (n >> 8 & 255) / 255, b = (n & 255) / 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b), h = 0, s = 0, l = (max + min) / 2;
    if (max !== min) {
      var d = max - min; s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60;
    }
    return [h, s * 100, l * 100];
  }
  function hsl(h, s, l) {
    h = ((h % 360) + 360) % 360; s = Math.max(0, Math.min(100, s)) / 100; l = Math.max(0, Math.min(100, l)) / 100;
    var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l);
    var f = function (n) { return Math.round(255 * (l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))))); };
    return '#' + [f(0), f(8), f(4)].map(function (x) { return x.toString(16).padStart(2, '0'); }).join('');
  }
  function lum(hex) {
    var n = parseInt(hex.slice(1), 16), c = [n >> 16, n >> 8 & 255, n & 255].map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }
  function text(hex) { return lum(hex) > 0.4 ? '#1c1a17' : '#ffffff'; }
  function lrv(hex) { return Math.round(lum(hex) * 100); }

  function generate(base, harmony, role) {
    var b = hexToHsl(base) || [260, 30, 70], h = b[0], s = b[1], l = b[2];
    var warm = (h < 90 || h > 300);
    var hues = { mono: [h, h], analogous: [h + 30, h - 30], complementary: [h + 180, h + 180], split: [h + 150, h + 210], triadic: [h + 120, h + 240], neutral: [35, h] }[harmony];
    var main, second, accent;
    if (role === 'accent') {
      accent = base;
      main = harmony === 'mono' ? hsl(h, Math.min(s, 18), 90) : hsl(harmony === 'neutral' ? 38 : hues[0], 12, 90);
      second = harmony === 'mono' ? hsl(h, Math.min(s, 30), 55) : hsl(hues[1], Math.min(s, 28), 52);
    } else {
      main = base;
      if (harmony === 'mono') { second = hsl(h, s * 0.8, l > 50 ? l - 30 : l + 25); accent = hsl(h, Math.min(100, s * 1.2), l > 50 ? 28 : 80); }
      else if (harmony === 'neutral') { second = hsl(35, 14, 58); accent = hsl(h, Math.min(100, s + 10), Math.max(25, l - 35)); }
      else { second = hsl(hues[0], Math.min(s, 32), 52); accent = hsl(hues[1], Math.min(80, s + 20), 38); }
    }
    var trim = warm || harmony === 'neutral' ? '#f7f2e8' : '#f6f7f5';
    var anchor = hsl(harmony === 'neutral' ? 30 : h, 12, 20);
    return [main, second, accent, trim, anchor];
  }

  function room(p) {
    return '<svg class="diagram" viewBox="0 0 400 230" role="img" aria-label="Room preview using the palette">' +
      '<rect width="400" height="175" fill="' + p[0] + '"/>' +
      '<rect y="168" width="400" height="9" fill="' + p[3] + '"/><rect y="177" width="400" height="53" fill="#b89a74"/><rect y="177" width="400" height="53" fill="' + p[4] + '" fill-opacity=".35"/>' +
      '<rect x="40" y="18" width="98" height="132" fill="' + p[3] + '"/><rect x="47" y="25" width="84" height="118" fill="#dfe9ef"/>' +
      '<rect x="230" y="40" width="70" height="52" fill="' + p[3] + '"/><rect x="235" y="45" width="60" height="42" fill="' + p[2] + '" fill-opacity=".8"/>' +
      '<rect x="165" y="110" width="180" height="50" rx="10" fill="' + p[1] + '"/><rect x="158" y="128" width="194" height="40" rx="10" fill="' + p[1] + '"/><rect x="175" y="102" width="160" height="22" rx="8" fill="' + p[1] + '" style="filter:brightness(.93)"/>' +
      '<rect x="182" y="112" width="34" height="28" rx="6" fill="' + p[2] + '"/><rect x="296" y="112" width="34" height="28" rx="6" fill="' + p[2] + '"/>' +
      '<rect x="168" y="168" width="6" height="14" fill="' + p[4] + '"/><rect x="336" y="168" width="6" height="14" fill="' + p[4] + '"/>' +
      '<rect x="58" y="178" width="70" height="18" rx="3" fill="' + p[4] + '"/><path d="M80 178 q13-28 26 0" fill="' + p[2] + '" fill-opacity=".9"/>' +
      '</svg>';
  }

  function render(p, title) {
    current = p;
    var roles = [['60%', 'Walls & large surfaces'], ['30%', 'Sofa, curtains, rug'], ['10%', 'Cushions, art, accents'], ['Trim', 'Doors, baseboards, ceiling'], ['Anchor', 'Frames, legs, hardware']];
    out.innerHTML = (title ? '<p class="result__label">' + title + '</p>' : '<p class="result__label">Your 60-30-10 palette</p>') +
      '<div class="pal-swatches">' + p.slice(0, 3).map(function (c, i) {
        return '<button type="button" class="pal-sw" data-copy-hex="' + c + '" style="background:' + c + ';color:' + text(c) + '"><b>' + roles[i][0] + '</b>' + c.toUpperCase() + '</button>';
      }).join('') + '</div>' + room(p) +
      '<div class="pal-list">' + p.map(function (c, i) {
        return '<button type="button" class="pal-item" data-copy-hex="' + c + '"><i style="background:' + c + '"></i><span><b>' + c.toUpperCase() + '</b><small>' + roles[i][1] + ' · LRV≈' + lrv(c) + '</small></span></button>';
      }).join('') + '</div>' +
      '<p class="tool-note" style="text-align:left">Click any color to copy its hex code. Screens vary, so match the hex at the paint store and test large samples on two walls at different times of day.</p>' +
      '<div class="tool-actions"><button type="button" class="btn btn--small btn--ghost" data-copy-all>Copy all hex codes</button></div>';
  }

  out.addEventListener('click', function (e) {
    var t = e.target.closest('[data-copy-hex], [data-copy-all]');
    if (!t) return;
    var txt = t.hasAttribute('data-copy-all') ? current.join(', ').toUpperCase() : t.getAttribute('data-copy-hex').toUpperCase();
    if (navigator.clipboard) navigator.clipboard.writeText(txt);
    var old = t.innerHTML; t.innerHTML = '<b>Copied ' + txt.slice(0, 7) + '</b>';
    setTimeout(function () { t.innerHTML = old; }, 1100);
  });

  var pres = document.getElementById('pal-presets');
  pres.innerHTML = PRESETS.map(function (p, i) {
    return '<button type="button" class="preset" data-p="' + i + '"><i>' + p[1].slice(0, 3).map(function (c) { return '<b style="background:' + c + '"></b>'; }).join('') + '</i>' + p[0] + '</button>';
  }).join('');
  pres.addEventListener('click', function (e) {
    var b = e.target.closest('[data-p]'); if (!b) return;
    var p = PRESETS[+b.getAttribute('data-p')];
    form.base.value = p[1][0]; form.hex.value = p[1][0];
    render(p[1], p[0] + ' palette');
  });

  var syncing = false;
  form.hex.addEventListener('input', function () {
    var v = form.hex.value.trim(); if (v[0] !== '#') v = '#' + v;
    if (/^#[0-9a-f]{6}$/i.test(v)) { syncing = true; form.base.value = v.toLowerCase(); }
  });
  form.base.addEventListener('input', function () { if (!syncing) form.hex.value = form.base.value; syncing = false; });

  var q = new URLSearchParams(location.search).get('color');
  if (q && /^[0-9a-f]{6}$/i.test(q)) { form.base.value = '#' + q.toLowerCase(); form.hex.value = form.base.value; }

  L.bind(form, function (v) { render(generate(form.base.value, v.harmony, v.role)); });
})();
