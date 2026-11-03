/* Shared helpers for the calculators. Exposes window.SC. */
(function () {
  'use strict';
  if (window.SC) return;
  var SC = {};

  SC.num = function (form, name, def) {
    var el = form.elements[name];
    if (!el) return def;
    var v = el.length && !el.tagName ? (Array.prototype.find.call(el, function (r) { return r.checked; }) || {}).value : el.value;
    var n = parseFloat(v);
    return isFinite(n) ? n : def;
  };
  SC.val = function (form, name, def) {
    var el = form.elements[name];
    if (!el) return def;
    if (el.length && !el.tagName) { var c = Array.prototype.find.call(el, function (r) { return r.checked; }); return c ? c.value : def; }
    if (el.type === 'checkbox') return el.checked;
    return el.value;
  };
  SC.fmt = function (n, dec) {
    if (!isFinite(n)) return '—';
    return Number(n).toLocaleString('en-US', { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });
  };
  SC.money = function (n) { return '$' + SC.fmt(Math.round(n)); };
  SC.clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  SC.esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  /* Keep <output> labels next to range sliders in sync */
  SC.syncOutputs = function (form) {
    form.querySelectorAll('output[data-for]').forEach(function (o) {
      var el = form.elements[o.getAttribute('data-for')];
      if (!el) return;
      var suf = o.getAttribute('data-suffix') || '';
      o.textContent = SC.fmt(parseFloat(el.value), parseInt(o.getAttribute('data-dec') || '0', 10)) + suf;
    });
  };

  /* Prefill from ?query (shareable links) */
  SC.prefill = function (form) {
    var p = new URLSearchParams(location.search);
    p.forEach(function (v, k) {
      var el = form.elements[k];
      if (!el) return;
      if (el.length && !el.tagName) Array.prototype.forEach.call(el, function (r) { r.checked = (r.value === v); });
      else if (el.type === 'checkbox') el.checked = v === '1';
      else el.value = v;
    });
    var zones = p.get('z');
    if (zones !== null) form.querySelectorAll('input[data-zone]').forEach(function (c) { c.checked = zones.split(',').indexOf(c.value) > -1; });
  };
  SC.shareUrl = function (form) {
    var p = new URLSearchParams();
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.hasAttribute('data-zone')) return;
      if (el.type === 'radio') { if (el.checked) p.set(el.name, el.value); }
      else if (el.type === 'checkbox') p.set(el.name, el.checked ? '1' : '0');
      else if (el.tagName !== 'BUTTON') p.set(el.name, el.value);
    });
    var z = Array.prototype.filter.call(form.querySelectorAll('input[data-zone]'), function (c) { return c.checked; }).map(function (c) { return c.value; });
    if (form.querySelector('input[data-zone]')) p.set('z', z.join(','));
    return location.origin + location.pathname + '?' + p.toString() + '#tool';
  };
  SC.copy = function (text, btn) {
    var done = function () { if (btn) { var t = btn.textContent; btn.textContent = 'Copied ✓'; setTimeout(function () { btn.textContent = t; }, 1600); } };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { window.prompt('Copy:', text); });
    else { window.prompt('Copy:', text); }
  };

  /* Wire a tool: compute on every change; share/copy/print buttons */
  SC.init = function (name, compute) {
    document.querySelectorAll('[data-tool="' + name + '"]').forEach(function (box) {
      var form = box.querySelector('form');
      if (!form) return;
      form.addEventListener('submit', function (e) { e.preventDefault(); });
      SC.prefill(form);
      var run = function () { SC.syncOutputs(form); compute(form, box); };
      form.addEventListener('input', run);
      form.addEventListener('change', run);
      box.querySelectorAll('[data-act]').forEach(function (b) {
        b.addEventListener('click', function () {
          var a = b.getAttribute('data-act');
          if (a === 'share') SC.copy(SC.shareUrl(form), b);
          if (a === 'print') window.print();
          if (a === 'copy') { var t = box.querySelector('[data-copy]'); SC.copy(t ? t.innerText : '', b); }
          if (a === 'reset') { form.reset(); form.querySelectorAll('input[type=range]').forEach(function (r) { if (window.scFill) window.scFill(r); }); run(); }
        });
      });
      form.querySelectorAll('input[type=range]').forEach(function (r) { if (window.scFill) window.scFill(r); });
      run();
    });
  };

  /* Minimal SVG line/area chart. series: [{pts:[[x,y],...], color, fill}] */
  SC.lineChart = function (el, o) {
    var W = o.w || 560, H = o.h || 220, P = { l: 38, r: 10, t: 12, b: 28 };
    var xmin = o.xmin, xmax = o.xmax, ymin = o.ymin, ymax = o.ymax;
    var X = function (x) { return P.l + (x - xmin) / (xmax - xmin) * (W - P.l - P.r); };
    var Y = function (y) { return H - P.b - (y - ymin) / (ymax - ymin) * (H - P.t - P.b); };
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + SC.esc(o.label || 'chart') + '">';
    (o.yticks || []).forEach(function (t) {
      s += '<line class="axis" x1="' + P.l + '" x2="' + (W - P.r) + '" y1="' + Y(t) + '" y2="' + Y(t) + '"/>';
      s += '<text x="' + (P.l - 6) + '" y="' + (Y(t) + 3) + '" text-anchor="end">' + t + (o.ysuf || '') + '</text>';
    });
    (o.xticks || []).forEach(function (t) {
      s += '<text x="' + X(t[0]) + '" y="' + (H - 8) + '" text-anchor="middle">' + t[1] + '</text>';
    });
    (o.bands || []).forEach(function (b) {
      s += '<rect x="' + X(b[0]) + '" y="' + P.t + '" width="' + (X(b[1]) - X(b[0])) + '" height="' + (H - P.t - P.b) + '" fill="' + b[2] + '"/>';
    });
    o.series.forEach(function (se) {
      var d = se.pts.map(function (p, i) { return (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1); }).join(' ');
      if (se.fill) s += '<path d="' + d + ' L' + X(se.pts[se.pts.length - 1][0]) + ' ' + Y(ymin) + ' L' + X(se.pts[0][0]) + ' ' + Y(ymin) + 'Z" fill="' + se.fill + '"/>';
      s += '<path d="' + d + '" fill="none" stroke="' + se.color + '" stroke-width="' + (se.width || 2.5) + '" stroke-linejoin="round" stroke-linecap="round"' + (se.dash ? ' stroke-dasharray="' + se.dash + '"' : '') + '/>';
    });
    s += '</svg>';
    el.innerHTML = s;
  };

  window.SC = SC;
})();
