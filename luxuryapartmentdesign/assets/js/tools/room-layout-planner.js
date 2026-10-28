(function () {
  'use strict';
  var L = window.LAD, root = document.getElementById('planner');
  if (!root) return;
  var stage = document.getElementById('pl-stage'), warnEl = document.getElementById('pl-warnings');
  var inW = document.getElementById('pl-w'), inL = document.getElementById('pl-l');
  var btnRot = document.getElementById('pl-rotate'), btnDel = document.getElementById('pl-delete');
  var NS = 'http://www.w3.org/2000/svg';

  // [key, label, width in, depth in, fill, shape]
  var CATALOG = [
    ['sofa', 'Sofa', 84, 36, '#cbbfae'], ['loveseat', 'Loveseat', 60, 36, '#cbbfae'], ['sectional', 'Sectional (L)', 108, 84, '#cbbfae', 'L'],
    ['armchair', 'Armchair', 32, 34, '#d8c8ad'], ['coffee', 'Coffee table', 48, 24, '#a98b65'], ['coffee-round', 'Round coffee table', 36, 36, '#a98b65', 'round'],
    ['side', 'Side table', 20, 20, '#a98b65'], ['tv', 'TV console', 60, 18, '#8c7a63'], ['bookcase', 'Bookcase', 36, 14, '#8c7a63'],
    ['queen', 'Queen bed', 60, 80, '#e6ddcd'], ['king', 'King bed', 76, 80, '#e6ddcd'], ['full', 'Full bed', 54, 75, '#e6ddcd'], ['twin', 'Twin bed', 38, 75, '#e6ddcd'],
    ['nightstand', 'Nightstand', 24, 18, '#a98b65'], ['dresser', 'Dresser', 60, 20, '#8c7a63'],
    ['dining', 'Dining table', 60, 36, '#a98b65'], ['dining-round', 'Round dining table', 42, 42, '#a98b65', 'round'], ['chair', 'Dining chair', 18, 20, '#d8c8ad'],
    ['desk', 'Desk', 48, 24, '#a98b65'], ['desk-chair', 'Desk chair', 24, 24, '#d8c8ad', 'round'],
    ['rug58', 'Rug 5×8', 96, 60, '#d4ae5e', 'rug'], ['rug69', 'Rug 6×9', 108, 72, '#d4ae5e', 'rug'], ['rug810', 'Rug 8×10', 120, 96, '#d4ae5e', 'rug'], ['rug912', 'Rug 9×12', 144, 108, '#d4ae5e', 'rug']
  ];
  var BY = {}; CATALOG.forEach(function (c) { BY[c[0]] = c; });
  var KEY = 'lad-planner-v1';
  var state = L.store.get(KEY, null) || {
    w: 14, l: 12, items: [
      { t: 'rug810', x: 24, y: 12, r: 0 }, { t: 'sofa', x: 42, y: 84, r: 0 }, { t: 'coffee', x: 60, y: 44, r: 0 },
      { t: 'armchair', x: 128, y: 40, r: 90 }, { t: 'tv', x: 54, y: 0, r: 0 }, { t: 'side', x: 20, y: 96, r: 0 }
    ]
  };
  var sel = -1, drag = null;
  inW.value = state.w; inL.value = state.l;

  function dims(it) { var c = BY[it.t]; return it.r % 180 ? [c[3], c[2]] : [c[2], c[3]]; }
  function save() { L.store.set(KEY, state); }
  function el(name, attrs) { var e = document.createElementNS(NS, name); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }

  var svg = el('svg', { role: 'img', 'aria-label': 'Scaled floor plan' });
  stage.appendChild(svg);

  function render() {
    var W = state.w * 12, H = state.l * 12, pad = 14;
    svg.setAttribute('viewBox', (-pad) + ' ' + (-pad) + ' ' + (W + pad * 2) + ' ' + (H + pad * 2));
    svg.innerHTML = '';
    var fs = (W + pad * 2) / Math.max(280, stage.clientWidth || 700) * 12;  // ~12px labels at any zoom
    svg.appendChild(el('rect', { x: -pad, y: -pad, width: W + pad * 2, height: H + pad * 2, fill: '#ffffff' }));
    svg.appendChild(el('rect', { x: 0, y: 0, width: W, height: H, fill: '#fbf8f2' }));
    for (var gx = 12; gx < W; gx += 12) svg.appendChild(el('line', { x1: gx, y1: 0, x2: gx, y2: H, stroke: '#eee6d8', 'stroke-width': 0.6 }));
    for (var gy = 12; gy < H; gy += 12) svg.appendChild(el('line', { x1: 0, y1: gy, x2: W, y2: gy, stroke: '#eee6d8', 'stroke-width': 0.6 }));
    svg.appendChild(el('rect', { x: 0, y: 0, width: W, height: H, fill: 'none', stroke: '#1c1a17', 'stroke-width': 3 }));
    var lbl = el('text', { x: W / 2, y: -3, 'text-anchor': 'middle', 'font-size': fs }); lbl.textContent = state.w + ' ft'; svg.appendChild(lbl);
    var lbl2 = el('text', { x: -3, y: H / 2, 'text-anchor': 'middle', 'font-size': fs, transform: 'rotate(-90 -3 ' + H / 2 + ')' }); lbl2.textContent = state.l + ' ft'; svg.appendChild(lbl2);

    var clash = check();
    // rugs first so they sit underneath
    var order = state.items.map(function (_, i) { return i; }).sort(function (a, b) { return (BY[state.items[b].t][5] === 'rug') - (BY[state.items[a].t][5] === 'rug'); });
    order.forEach(function (i) {
      var it = state.items[i], c = BY[it.t], d = dims(it);
      var g = el('g', { class: 'item' + (i === sel ? ' is-selected' : '') + (clash[i] ? ' is-clash' : ''), 'data-i': i, tabindex: 0 });
      var shape = c[5];
      if (shape === 'round') g.appendChild(el('ellipse', { cx: it.x + d[0] / 2, cy: it.y + d[1] / 2, rx: d[0] / 2, ry: d[1] / 2, fill: c[4], stroke: '#6d665b', 'stroke-width': 0.8 }));
      else if (shape === 'L') {
        g.appendChild(el('rect', { x: it.x, y: it.y, width: d[0], height: d[1], fill: 'transparent', stroke: 'none' }));
        var arm = 36;
        var p = it.r % 360 === 0 ? [[it.x, it.y + d[1] - arm, d[0], arm], [it.x, it.y, arm, d[1]]]
          : it.r % 360 === 90 ? [[it.x, it.y, d[0], arm], [it.x, it.y, arm, d[1]]]
          : it.r % 360 === 180 ? [[it.x, it.y, d[0], arm], [it.x + d[0] - arm, it.y, arm, d[1]]]
          : [[it.x, it.y + d[1] - arm, d[0], arm], [it.x + d[0] - arm, it.y, arm, d[1]]];
        p.forEach(function (q) { g.appendChild(el('rect', { x: q[0], y: q[1], width: q[2], height: q[3], rx: 4, fill: c[4], stroke: '#6d665b', 'stroke-width': 0.8 })); });
      } else g.appendChild(el('rect', { x: it.x, y: it.y, width: d[0], height: d[1], rx: shape === 'rug' ? 2 : 4, fill: c[4], 'fill-opacity': shape === 'rug' ? 0.35 : 1, stroke: shape === 'rug' ? '#b88a2e' : '#6d665b', 'stroke-width': 0.8, 'stroke-dasharray': shape === 'rug' ? '5 4' : '' }));
      var t = el('text', { x: it.x + d[0] / 2, y: it.y + d[1] / 2 + fs / 3, 'text-anchor': 'middle', 'font-size': Math.min(fs, d[0] / (c[1].length * 0.55)) }); t.textContent = c[1]; g.appendChild(t);
      svg.appendChild(g);
    });
    btnRot.disabled = btnDel.disabled = sel < 0;
  }

  function box(it) { var d = dims(it); return { x1: it.x, y1: it.y, x2: it.x + d[0], y2: it.y + d[1] }; }
  function gap(a, b) {
    var dx = Math.max(b.x1 - a.x2, a.x1 - b.x2), dy = Math.max(b.y1 - a.y2, a.y1 - b.y2);
    if (dx < 0 && dy < 0) return { overlap: true };
    if (dx >= 0 && dy < 0) return { g: dx };
    if (dy >= 0 && dx < 0) return { g: dy };
    return { g: Math.max(dx, dy), corner: true };
  }
  function name(it) { return BY[it.t][1].toLowerCase(); }
  function check() {
    var W = state.w * 12, H = state.l * 12, warns = [], clash = {};
    var solid = state.items.map(function (it, i) { return [it, i]; }).filter(function (p) { return BY[p[0].t][5] !== 'rug'; });
    var small = { side: 1, nightstand: 1, chair: 1, 'desk-chair': 1 };
    state.items.forEach(function (it, i) {
      var b = box(it);
      if (b.x1 < -0.5 || b.y1 < -0.5 || b.x2 > W + 0.5 || b.y2 > H + 0.5) { clash[i] = 1; warns.push(['bad', 'The ' + name(it) + ' does not fit inside the room.']); }
    });
    for (var a = 0; a < solid.length; a++) for (var b = a + 1; b < solid.length; b++) {
      var A = solid[a][0], B = solid[b][0], r = gap(box(A), box(B)), ta = A.t, tb = B.t;
      var pair = [ta, tb].sort().join('+');
      if (r.overlap) { clash[solid[a][1]] = clash[solid[b][1]] = 1; warns.push(['bad', 'The ' + name(A) + ' and ' + name(B) + ' overlap.']); continue; }
      if (r.corner) continue;
      var isSofa = /sofa|loveseat|sectional|armchair/.test(ta + tb), isCoffee = /coffee/.test(ta + tb);
      if (isSofa && isCoffee && /coffee/.test(pair) && !(/coffee.*coffee/.test(pair))) {
        if (r.g < 14) warns.push(['', 'Only ' + Math.round(r.g) + ' in. between the ' + name(A) + ' and ' + name(B) + '. Aim for 14–18 in. so knees and legs fit.']);
        else if (r.g <= 18) warns.push(['ok', 'Seating to coffee table: ' + Math.round(r.g) + ' in. Perfect reach.']);
        else if (r.g < 30) warns.push(['', Math.round(r.g) + ' in. from the ' + name(A) + ' to the ' + name(B) + ' is a stretch to reach. 14–18 in. is ideal.']);
        continue;
      }
      if (small[ta] || small[tb]) continue;
      if (r.g > 0 && r.g < 30) warns.push(['', 'Only ' + Math.round(r.g) + ' in. between the ' + name(A) + ' and the ' + name(B) + '. Main walkways need 30–36 in.']);
    }
    solid.forEach(function (p) {
      var it = p[0], bx = box(it), sides = [bx.x1, W - bx.x2, bx.y1, H - bx.y2];
      if (/queen|king|full|twin/.test(it.t)) {
        var side = it.r % 180 ? [sides[2], sides[3]] : [sides[0], sides[1]];
        side.forEach(function (g) { if (g > 1 && g < 24) warns.push(['', 'Only ' + Math.round(g) + ' in. beside the ' + name(it) + '. Leave 24–36 in. to walk around and make the bed, or push it against the wall.']); });
      }
      if (/dining/.test(it.t)) {
        sides.forEach(function (g) { if (g < 36) warns.push([g < 24 ? 'bad' : '', Math.round(g) + ' in. from the dining table to a wall. Chairs need 24 in. to pull out and 36 in. for someone to walk behind.']); });
      }
    });
    var seats = solid.filter(function (p) { return /sofa|loveseat|sectional|armchair/.test(p[0].t); });
    for (var s1 = 0; s1 < seats.length; s1++) for (var s2 = s1 + 1; s2 < seats.length; s2++) {
      var c1 = box(seats[s1][0]), c2 = box(seats[s2][0]);
      var dist = Math.hypot((c1.x1 + c1.x2 - c2.x1 - c2.x2) / 2, (c1.y1 + c1.y2 - c2.y1 - c2.y2) / 2);
      if (dist > 120) warns.push(['', 'The ' + name(seats[s1][0]) + ' and ' + name(seats[s2][0]) + ' are ' + L.fmt(dist / 12) + ' ft apart. Conversation areas work best within about 8–10 ft.']);
    }
    if (!warns.length && state.items.length) warns.push(['ok', 'Clearances look good. Every main walkway is at least 30 in.']);
    var seen = {};
    warnEl.innerHTML = warns.filter(function (w) { if (seen[w[1]]) return false; seen[w[1]] = 1; return true; }).slice(0, 8)
      .map(function (w) { return '<li class="' + w[0] + '">' + w[1] + '</li>'; }).join('');
    return clash;
  }

  function pt(e) {
    var p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }
  svg.addEventListener('pointerdown', function (e) {
    var g = e.target.closest('.item');
    if (!g) { sel = -1; render(); return; }
    sel = +g.getAttribute('data-i');
    var p = pt(e), it = state.items[sel];
    drag = { dx: p.x - it.x, dy: p.y - it.y };
    svg.setPointerCapture(e.pointerId);
    render();
  });
  svg.addEventListener('pointermove', function (e) {
    if (!drag || sel < 0) return;
    var p = pt(e), it = state.items[sel], d = dims(it), W = state.w * 12, H = state.l * 12;
    var x = Math.round((p.x - drag.dx) / 2) * 2, y = Math.round((p.y - drag.dy) / 2) * 2;
    it.x = Math.max(0, Math.min(W - d[0], x)); it.y = Math.max(0, Math.min(H - d[1], y));
    render();
  });
  function end() { if (drag) { drag = null; save(); } }
  svg.addEventListener('pointerup', end);
  svg.addEventListener('pointercancel', end);

  function rotate() { if (sel < 0) return; var it = state.items[sel]; it.r = (it.r + 90) % 360; clamp(it); save(); render(); }
  function del() { if (sel < 0) return; state.items.splice(sel, 1); sel = -1; save(); render(); }
  function clamp(it) { var d = dims(it); it.x = Math.max(0, Math.min(state.w * 12 - d[0], it.x)); it.y = Math.max(0, Math.min(state.l * 12 - d[1], it.y)); }
  btnRot.addEventListener('click', rotate);
  btnDel.addEventListener('click', del);
  document.getElementById('pl-clear').addEventListener('click', function () { if (confirm('Remove all furniture from the plan?')) { state.items = []; sel = -1; save(); render(); } });
  document.addEventListener('keydown', function (e) {
    if (sel < 0 || /input|select|textarea/i.test(document.activeElement.tagName)) return;
    var it = state.items[sel], step = e.shiftKey ? 12 : 2, moved = true;
    if (e.key === 'ArrowLeft') it.x -= step; else if (e.key === 'ArrowRight') it.x += step;
    else if (e.key === 'ArrowUp') it.y -= step; else if (e.key === 'ArrowDown') it.y += step;
    else if (e.key === 'r' || e.key === 'R') { rotate(); return; }
    else if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); del(); return; }
    else moved = false;
    if (moved) { e.preventDefault(); clamp(it); save(); render(); }
  });

  var pal = document.getElementById('pl-palette');
  pal.innerHTML = CATALOG.map(function (c) { return '<button type="button" data-t="' + c[0] + '">' + c[1] + '<small>' + c[2] + '×' + c[3] + ' in.</small></button>'; }).join('');
  pal.addEventListener('click', function (e) {
    var b = e.target.closest('[data-t]'); if (!b) return;
    var c = BY[b.getAttribute('data-t')];
    var it = { t: c[0], x: Math.max(0, (state.w * 12 - c[2]) / 2), y: Math.max(0, (state.l * 12 - c[3]) / 2), r: 0 };
    state.items.push(it); sel = state.items.length - 1; clamp(it); save(); render();
    stage.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  });
  function resize() {
    var w = parseFloat(inW.value), l = parseFloat(inL.value);
    if (w >= 5 && w <= 40 && l >= 5 && l <= 40) { state.w = w; state.l = l; state.items.forEach(clamp); save(); render(); }
  }
  inW.addEventListener('input', resize); inL.addEventListener('input', resize);
  window.addEventListener('resize', function () { render(); });

  document.getElementById('pl-download').addEventListener('click', function () {
    var prev = sel; sel = -1; render();
    var vb = svg.viewBox.baseVal, scale = 4;
    var xml = new XMLSerializer().serializeToString(svg).replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg" width="' + vb.width * scale + '" height="' + vb.height * scale + '"');
    xml = xml.replace(/<text /g, '<text font-family="Arial, sans-serif" fill="#3a362f" ');
    var img = new Image();
    img.onload = function () {
      var cv = document.createElement('canvas'); cv.width = vb.width * scale; cv.height = vb.height * scale;
      cv.getContext('2d').drawImage(img, 0, 0);
      var a = document.createElement('a'); a.download = 'room-layout-' + state.w + 'x' + state.l + '.png'; a.href = cv.toDataURL('image/png'); a.click();
      sel = prev; render();
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
  });
  render();
})();
