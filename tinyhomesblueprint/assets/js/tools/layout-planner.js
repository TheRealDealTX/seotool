// Tiny Homes Blueprint - drag-and-drop tiny house layout planner.
// SVG user units are feet: x runs along the length, y across the width.
(function () {
  var root = document.getElementById('lp');
  if (!root) return;
  var svg = document.getElementById('lp-svg');
  var NS = 'http://www.w3.org/2000/svg';
  var STORE = 'thb-layout-v1';
  var SNAP = 0.5;

  // key: [label, short label, width (x), depth (y), kind]
  var CAT = {
    queen:   ['Queen bed', 'Queen', 5, 6.7, 'sleep'],
    full:    ['Full bed', 'Full', 4.5, 6.3, 'sleep'],
    twin:    ['Twin bed', 'Twin', 3.2, 6.3, 'sleep'],
    sofa:    ['Sofa', 'Sofa', 7, 3, 'living'],
    love:    ['Loveseat', 'Loveseat', 5, 3, 'living'],
    table:   ['Dining table', 'Table', 2.5, 4, 'living'],
    desk:    ['Desk', 'Desk', 4, 2, 'living'],
    counter: ['Galley counter', 'Counter', 8, 2, 'kitchen'],
    fridge:  ['Fridge', 'Fridge', 2.5, 2.5, 'kitchen'],
    range:   ['Range', 'Range', 2.5, 2, 'kitchen'],
    sink:    ['Sink base', 'Sink', 2.5, 2, 'kitchen'],
    shower:  ['Shower', 'Shower', 3, 3, 'bath'],
    toilet:  ['Toilet zone', 'WC', 2.5, 4, 'bath'],
    wd:      ['Washer/dryer stack', 'W/D', 2.5, 2.5, 'util'],
    closet:  ['Closet', 'Closet', 4, 2, 'util'],
    stairs:  ['Storage stairs', 'Stairs', 8, 2.5, 'circ'],
    ladder:  ['Loft ladder', 'Ladder', 1.5, 1.5, 'circ'],
    stove:   ['Wood stove + clearance', 'Stove', 3.5, 3.5, 'heat'],
    wall:    ['Interior wall', 'Wall', 6, 0.35, 'wall'],
    door:    ['Door (32 in)', 'Door', 2.67, 2.67, 'door'],
    window:  ['Window', 'Window', 3, 0.4, 'window']
  };
  var COLORS = { sleep: '#8fd0c3', living: '#c6b4e6', kitchen: '#f2c58d', bath: '#8ec3ea', util: '#d4dadb', circ: '#e6d38f', heat: '#f39b7c', wall: '#ffffff', door: '#9fe0dc', window: '#9fe0dc' };
  var OPENING = { door: 1, window: 1 };

  var state = { fw: 8.5, fl: 24, items: [] };
  var sel = null, drag = null, nextId = 1;
  var $ = function (id) { return document.getElementById(id); };

  function snap(v) { return Math.round(v / SNAP) * SNAP; }
  function round2(v) { return Math.round(v * 100) / 100; }
  function fmt(v) { return (Math.round(v * 10) / 10).toString(); }
  function dims(it) {
    var c = CAT[it.t], bw = it.bw || c[2], bh = c[3];
    return it.r % 2 ? { w: bh, h: bw, bw: bw, bh: bh } : { w: bw, h: bh, bw: bw, bh: bh };
  }
  function byId(id) { for (var i = 0; i < state.items.length; i++) if (state.items[i].id === id) return state.items[i]; return null; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function clampItem(it) {
    var d = dims(it);
    it.x = round2(Math.max(0, Math.min(state.fl - d.w, it.x)));
    it.y = round2(Math.max(0, Math.min(state.fw - d.h, it.y)));
  }
  function fits(it) { var d = dims(it); return d.w <= state.fl + 1e-6 && d.h <= state.fw + 1e-6; }
  function overlaps(a, b) {
    var da = dims(a), db = dims(b), e = 0.01;
    return a.x < b.x + db.w - e && b.x < a.x + da.w - e && a.y < b.y + db.h - e && b.y < a.y + da.h - e;
  }
  function conflictSet() {
    var bad = {}, solid = state.items.filter(function (i) { return !OPENING[CAT[i.t][4]]; });
    for (var i = 0; i < solid.length; i++) {
      if (!fits(solid[i])) bad[solid[i].id] = 1;
      for (var j = i + 1; j < solid.length; j++) if (overlaps(solid[i], solid[j])) { bad[solid[i].id] = 1; bad[solid[j].id] = 1; }
    }
    state.items.forEach(function (i) { if (OPENING[CAT[i.t][4]] && !fits(i)) bad[i.id] = 1; });
    return bad;
  }

  // Item artwork drawn in the base (unrotated) box bw x bh, rotated by the caller.
  function art(t, bw, bh, col) {
    var s = 'stroke="' + col + '" stroke-width="0.05" fill="none"';
    switch (t) {
      case 'queen': case 'full': case 'twin':
        var pw = t === 'twin' ? bw - 0.6 : (bw - 0.9) / 2;
        var p = '<rect x="0.3" y="0.3" width="' + pw + '" height="0.9" rx="0.2" ' + s + '/>';
        if (t !== 'twin') p += '<rect x="' + (0.6 + pw) + '" y="0.3" width="' + pw + '" height="0.9" rx="0.2" ' + s + '/>';
        return p + '<path d="M0 1.7H' + bw + '" ' + s + '/>';
      case 'sofa': case 'love':
        return '<rect x="0.15" y="0.15" width="' + (bw - 0.3) + '" height="0.7" rx="0.2" ' + s + '/><path d="M0.15 0.85V' + (bh - 0.15) + 'M' + (bw - 0.15) + ' 0.85V' + (bh - 0.15) + '" ' + s + '/>';
      case 'table':
        return '<circle cx="-0.35" cy="1.2" r="0.3" ' + s + '/><circle cx="-0.35" cy="2.8" r="0.3" ' + s + '/><circle cx="' + (bw + 0.35) + '" cy="1.2" r="0.3" ' + s + '/><circle cx="' + (bw + 0.35) + '" cy="2.8" r="0.3" ' + s + '/>';
      case 'counter':
        return '<rect x="2.6" y="0.35" width="1.6" height="1.2" rx="0.15" ' + s + '/><circle cx="5.9" cy="0.65" r="0.3" ' + s + '/><circle cx="6.9" cy="0.65" r="0.3" ' + s + '/><circle cx="5.9" cy="1.4" r="0.3" ' + s + '/><circle cx="6.9" cy="1.4" r="0.3" ' + s + '/>';
      case 'range':
        return '<circle cx="0.75" cy="0.6" r="0.3" ' + s + '/><circle cx="1.75" cy="0.6" r="0.3" ' + s + '/><circle cx="0.75" cy="1.4" r="0.3" ' + s + '/><circle cx="1.75" cy="1.4" r="0.3" ' + s + '/>';
      case 'sink':
        return '<rect x="0.4" y="0.35" width="1.7" height="1.2" rx="0.2" ' + s + '/>';
      case 'fridge':
        return '<path d="M0.2 0.4H' + (bw - 0.2) + '" ' + s + '/>';
      case 'shower':
        return '<path d="M0 0L' + bw + ' ' + bh + 'M' + bw + ' 0L0 ' + bh + '" ' + s + '/><circle cx="' + bw / 2 + '" cy="' + bh / 2 + '" r="0.18" ' + s + '/>';
      case 'toilet':
        return '<rect x="0.75" y="0.1" width="1" height="0.45" rx="0.1" ' + s + '/><ellipse cx="1.25" cy="1.05" rx="0.42" ry="0.55" ' + s + '/>';
      case 'wd':
        return '<circle cx="' + bw / 2 + '" cy="' + bh / 2 + '" r="0.8" ' + s + '/>';
      case 'closet':
        return '<path d="M0.2 1H' + (bw - 0.2) + '" ' + s + '/>';
      case 'stairs':
        var st = ''; for (var i = 1; i < 8; i++) st += 'M' + i + ' 0V' + bh;
        return '<path d="' + st + '" ' + s + '/><path d="M0.4 ' + bh / 2 + 'H' + (bw - 0.6) + 'l-0.35 -0.3m0.35 0.3l-0.35 0.3" ' + s + '/>';
      case 'ladder':
        return '<path d="M0.3 0.1V1.4M1.2 0.1V1.4M0.3 0.4H1.2M0.3 0.75H1.2M0.3 1.1H1.2" ' + s + '/>';
      case 'stove':
        return '<rect x="1" y="1" width="1.5" height="1.5" rx="0.15" fill="' + col + '" fill-opacity="0.55" stroke="' + col + '" stroke-width="0.05"/>';
      case 'door':
        return '<path d="M0 ' + bh + 'V0" stroke="' + col + '" stroke-width="0.09"/><path d="M0 0A' + bw + ' ' + bw + ' 0 0 1 ' + bw + ' ' + bh + '" ' + s + ' stroke-dasharray="0.15 0.1"/>';
      default: return '';
    }
  }
  function rotTransform(r, bw, bh) {
    return ['', 'translate(' + bh + ' 0) rotate(90)', 'translate(' + bw + ' ' + bh + ') rotate(180)', 'translate(0 ' + bw + ') rotate(270)'][r];
  }

  function itemMarkup(it, bad, exporting) {
    var c = CAT[it.t], d = dims(it), kind = c[4], col = COLORS[kind];
    var isSel = !exporting && sel === it.id;
    var body;
    if (kind === 'wall') {
      body = '<rect class="hit" width="' + d.w + '" height="' + d.h + '" fill="#e8f2f2"/>';
    } else if (kind === 'window') {
      body = '<rect class="hit" width="' + d.w + '" height="' + d.h + '" fill="#0d3c48" stroke="' + col + '" stroke-width="0.06"/>' +
        (it.r % 2 ? '<path d="M' + d.w / 2 + ' 0V' + d.h + '" stroke="' + col + '" stroke-width="0.05"/>' : '<path d="M0 ' + d.h / 2 + 'H' + d.w + '" stroke="' + col + '" stroke-width="0.05"/>');
    } else if (kind === 'door') {
      body = '<rect class="hit" width="' + d.w + '" height="' + d.h + '" fill="' + col + '" fill-opacity="0.06"/>';
    } else {
      body = '<rect class="hit" width="' + d.w + '" height="' + d.h + '" rx="0.12" fill="' + col + '" fill-opacity="0.26" stroke="' + col + '" stroke-width="0.06"/>';
    }
    var a = art(it.t, d.bw, d.bh, col);
    if (a) body += '<g transform="' + rotTransform(it.r, d.bw, d.bh) + '" opacity="0.85">' + a + '</g>';
    if (kind !== 'wall' && kind !== 'window' && kind !== 'door') {
      var fs = Math.max(0.32, Math.min(0.5, Math.min(d.w, d.h) * 0.24));
      var label = c[0].length * fs * 0.56 < d.w - 0.3 ? c[0] : c[1];
      body += '<text x="' + d.w / 2 + '" y="' + d.h / 2 + '" font-size="' + fs + '" font-family="Inter, Arial, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle" dominant-baseline="central" pointer-events="none">' + esc(label) + '</text>';
    }
    if (bad[it.id]) body += '<rect width="' + d.w + '" height="' + d.h + '" fill="#ff5a4f" fill-opacity="0.42" stroke="#ff6b5f" stroke-width="0.08" pointer-events="none"/>';
    if (isSel) body += '<rect x="-0.12" y="-0.12" width="' + (d.w + 0.24) + '" height="' + (d.h + 0.24) + '" fill="none" stroke="#f2c58d" stroke-width="0.09" stroke-dasharray="0.3 0.18" pointer-events="none"/>';
    var aria = exporting ? '' : ' tabindex="0" role="button" aria-label="' + esc(c[0] + ', ' + fmt(d.w) + ' by ' + fmt(d.h) + ' ft, at ' + fmt(it.x) + ' ft, ' + fmt(it.y) + ' ft' + (bad[it.id] ? ', overlapping' : '')) + '" aria-pressed="' + (isSel ? 'true' : 'false') + '"';
    return '<g class="item" data-id="' + it.id + '" transform="translate(' + it.x + ' ' + it.y + ')"' + aria + '>' + body + '</g>';
  }

  function markup(exporting) {
    var fl = state.fl, fw = state.fw, out = '';
    out += '<rect x="0" y="0" width="' + fl + '" height="' + fw + '" fill="#0f4654"/>';
    var g = '';
    for (var x = 1; x < fl; x++) g += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="' + fw + '" stroke="#ffffff" stroke-opacity="' + (x % 4 ? 0.09 : 0.22) + '" stroke-width="0.03"/>';
    for (var y = 1; y < fw; y++) g += '<line x1="0" y1="' + y + '" x2="' + fl + '" y2="' + y + '" stroke="#ffffff" stroke-opacity="' + (y % 4 ? 0.09 : 0.22) + '" stroke-width="0.03"/>';
    out += '<g pointer-events="none">' + g + '</g>';
    out += '<rect x="-0.15" y="-0.15" width="' + (fl + 0.3) + '" height="' + (fw + 0.3) + '" fill="none" stroke="#e8f2f2" stroke-width="0.3" pointer-events="none"/>';
    // Dimension lines.
    var dim = 'stroke="#f2c58d" stroke-width="0.04"';
    out += '<g pointer-events="none"><path d="M0 -0.9H' + fl + 'M0 -1.15V-0.65M' + fl + ' -1.15V-0.65" ' + dim + '/>' +
      '<text x="' + fl / 2 + '" y="-1.1" font-size="0.55" font-family="Inter, Arial, sans-serif" font-weight="700" fill="#f2c58d" text-anchor="middle">' + fmt(fl) + ' ft</text>' +
      '<path d="M-0.9 0V' + fw + 'M-1.15 0H-0.65M-1.15 ' + fw + 'H-0.65" ' + dim + '/>' +
      '<text x="-1.1" y="' + fw / 2 + '" font-size="0.55" font-family="Inter, Arial, sans-serif" font-weight="700" fill="#f2c58d" text-anchor="middle" transform="rotate(-90 -1.1 ' + fw / 2 + ')">' + fmt(fw) + ' ft</text></g>';
    var bad = conflictSet();
    // Openings on top so doors and windows stay visible over furniture edges.
    var items = state.items.slice().sort(function (a, b) { return (OPENING[CAT[a.t][4]] ? 1 : 0) - (OPENING[CAT[b.t][4]] ? 1 : 0); });
    out += '<g id="lp-items">' + items.map(function (it) { return itemMarkup(it, bad, exporting); }).join('') + '</g>';
    return { svg: out, bad: bad };
  }

  function viewBox() { return [-1.7, -1.7, state.fl + 2.3, state.fw + 2.3]; }

  function stats(bad) {
    var area = state.fw * state.fl, step = 0.25, occ = 0;
    var solid = state.items.filter(function (i) { return !OPENING[CAT[i.t][4]]; }).map(function (i) { var d = dims(i); return [i.x, i.y, i.x + d.w, i.y + d.h]; });
    for (var x = step / 2; x < state.fl; x += step) {
      for (var y = step / 2; y < state.fw; y += step) {
        for (var k = 0; k < solid.length; k++) { var r = solid[k]; if (x > r[0] && x < r[2] && y > r[1] && y < r[3]) { occ++; break; } }
      }
    }
    var occArea = Math.min(area, occ * step * step);
    var nBad = Object.keys(bad).length;
    $('lp-area').textContent = fmt(area);
    $('lp-occ').textContent = Math.round(occArea / area * 100) + '%';
    $('lp-open').textContent = Math.round(area - occArea);
    $('lp-ov').textContent = nBad;
    $('lp-ov-box').className = nBad ? 'warn' : '';
  }

  function render(keepFocus) {
    var vb = viewBox();
    svg.setAttribute('viewBox', vb.join(' '));
    var m = markup(false);
    svg.innerHTML = m.svg;
    stats(m.bad);
    var it = sel ? byId(sel) : null;
    var has = !!it;
    $('lp-rotate').disabled = !has; $('lp-del').disabled = !has; $('lp-dup').disabled = !has;
    var wrap = $('lp-wall-wrap');
    if (has) {
      var d = dims(it);
      $('lp-sel').innerHTML = esc(CAT[it.t][0]) + ' <small>' + fmt(d.w) + ' &times; ' + fmt(d.h) + ' ft</small>';
      wrap.classList.toggle('on', it.t === 'wall');
      if (it.t === 'wall' && document.activeElement !== $('lp-wall-len')) $('lp-wall-len').value = it.bw || CAT.wall[2];
    } else {
      $('lp-sel').textContent = 'Nothing selected';
      wrap.classList.remove('on');
    }
    if (keepFocus && has) {
      var g = svg.querySelector('g.item[data-id="' + sel + '"]');
      if (g) g.focus({ preventScroll: true });
    }
  }

  function msg(text, warn) { var el = $('lp-msg'); el.textContent = text || ''; el.className = 'planner-msg' + (warn ? ' warn' : ''); }

  function save() {
    try {
      localStorage.setItem(STORE, JSON.stringify({ fw: state.fw, fl: state.fl, items: state.items.map(function (i) { return { t: i.t, x: i.x, y: i.y, r: i.r, bw: i.bw }; }) }));
    } catch (e) { /* storage blocked: the planner still works for this visit */ }
  }
  function load() {
    try {
      var raw = localStorage.getItem(STORE);
      if (!raw) return false;
      var d = JSON.parse(raw);
      if (!d || !Array.isArray(d.items) || !(d.fw > 0) || !(d.fl > 0)) return false;
      state.fw = d.fw; state.fl = d.fl;
      state.items = d.items.filter(function (i) { return CAT[i.t]; }).map(function (i) { return { id: nextId++, t: i.t, x: +i.x || 0, y: +i.y || 0, r: (+i.r || 0) % 4, bw: i.bw ? +i.bw : undefined }; });
      return true;
    } catch (e) { return false; }
  }

  function sample() {
    state.fw = 8.5; state.fl = 24; nextId = 1;
    var s = [
      ['shower', 0, 0, 0], ['sink', 3.5, 0, 0], ['toilet', 0, 4.5, 0], ['wd', 3.5, 6, 0],
      ['wall', 6, 0, 1, 5.5], ['counter', 6.5, 0, 0], ['fridge', 14.5, 0, 0], ['table', 11, 4.5, 0],
      ['sofa', 17, 0, 0], ['stairs', 16, 6, 0], ['door', 7, 5.83, 0],
      ['window', 8.5, 0, 0], ['window', 19.5, 0, 0], ['window', 13.5, 8.1, 0]
    ];
    state.items = s.map(function (a) { return { id: nextId++, t: a[0], x: a[1], y: a[2], r: a[3], bw: a[4] }; });
    sel = null;
  }

  function syncFootInputs() {
    $('lp-w').value = state.fw; $('lp-l').value = state.fl;
    var key = state.fw + 'x' + state.fl, opt = $('lp-preset').querySelector('option[value="' + key + '"]');
    $('lp-preset').value = opt ? key : 'custom';
  }

  function setFootprint(w, l) {
    w = Math.max(6, Math.min(30, snap(+w || 8.5)));
    l = Math.max(8, Math.min(60, snap(+l || 24)));
    state.fw = w; state.fl = l;
    state.items.forEach(clampItem);
    var bad = state.items.filter(function (i) { return !fits(i); }).length;
    msg(bad ? bad + ' item' + (bad > 1 ? 's are' : ' is') + ' too big for this footprint. Rotate or remove ' + (bad > 1 ? 'them' : 'it') + '.' : '', !!bad);
    render(); save();
  }

  function findSpot(it) {
    var solid = state.items.filter(function (i) { return !OPENING[CAT[i.t][4]]; });
    if (OPENING[CAT[it.t][4]]) { it.x = 0; it.y = 0; clampItem(it); return; }
    var d = dims(it);
    for (var y = 0; y <= state.fw - d.h + 1e-6; y += SNAP) {
      for (var x = 0; x <= state.fl - d.w + 1e-6; x += SNAP) {
        it.x = x; it.y = y;
        if (!solid.some(function (o) { return overlaps(it, o); })) return true;
      }
    }
    it.x = (state.fl - d.w) / 2; it.y = (state.fw - d.h) / 2; clampItem(it); it.x = snap(it.x); it.y = snap(it.y); clampItem(it);
    return false;
  }

  function add(t) {
    var it = { id: nextId++, t: t, x: 0, y: 0, r: 0 };
    if (!fits(it)) { it.r = 1; if (!fits(it)) { msg(CAT[t][0] + ' does not fit in a ' + fmt(state.fw) + ' x ' + fmt(state.fl) + ' ft footprint.', true); return; } }
    var free = findSpot(it);
    state.items.push(it); sel = it.id;
    msg(free ? CAT[t][0] + ' added. Drag it into place.' : 'No free space left, so the ' + CAT[t][0].toLowerCase() + ' was placed in the middle. Move things around to make room.', !free);
    render(true); save();
  }

  function rotate() {
    var it = byId(sel); if (!it) return;
    var d0 = dims(it), cx = it.x + d0.w / 2, cy = it.y + d0.h / 2;
    var old = it.r;
    it.r = (it.r + 1) % 4;
    if (!fits(it)) { it.r = (it.r + 1) % 4; }
    if (!fits(it)) { it.r = old; msg('There is not enough room to rotate that item here.', true); return; }
    var d = dims(it);
    it.x = snap(cx - d.w / 2); it.y = snap(cy - d.h / 2); clampItem(it);
    msg('');
    render(true); save();
  }
  function remove() {
    if (!sel) return;
    state.items = state.items.filter(function (i) { return i.id !== sel; });
    sel = null; msg('Item removed.'); render(); save();
  }
  function duplicate() {
    var it = byId(sel); if (!it) return;
    var c = { id: nextId++, t: it.t, x: it.x, y: it.y, r: it.r, bw: it.bw };
    var free = findSpot(c);
    state.items.push(c); sel = c.id;
    msg(free ? 'Copy added.' : 'Copy placed, but there is no free space for it.', !free);
    render(true); save();
  }
  function nudge(dx, dy) {
    var it = byId(sel); if (!it) return;
    it.x = snap(it.x + dx); it.y = snap(it.y + dy); clampItem(it);
    render(true); save();
  }

  // Pointer dragging (mouse, touch and pen).
  function svgPoint(e) {
    var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    var m = svg.getScreenCTM();
    return m ? pt.matrixTransform(m.inverse()) : { x: 0, y: 0 };
  }
  svg.addEventListener('pointerdown', function (e) {
    var g = e.target.closest && e.target.closest('g.item');
    if (!g) { if (sel) { sel = null; render(); } return; }
    e.preventDefault();
    var it = byId(+g.dataset.id); if (!it) return;
    sel = it.id;
    var p = svgPoint(e);
    drag = { id: it.id, pid: e.pointerId, dx: p.x - it.x, dy: p.y - it.y, moved: false };
    try { svg.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ }
    render();
  });
  svg.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.pid) return;
    var it = byId(drag.id); if (!it) return;
    var p = svgPoint(e);
    var nx = snap(p.x - drag.dx), ny = snap(p.y - drag.dy);
    if (nx === it.x && ny === it.y) return;
    it.x = nx; it.y = ny; clampItem(it); drag.moved = true;
    render();
  });
  function endDrag(e) {
    if (!drag || e.pointerId !== drag.pid) return;
    try { svg.releasePointerCapture(e.pointerId); } catch (err) { /* ignore */ }
    var moved = drag.moved; drag = null;
    if (moved) { save(); var b = conflictSet(); msg(Object.keys(b).length ? 'Some items overlap (shown in red).' : '', !!Object.keys(b).length); }
  }
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);

  svg.addEventListener('focusin', function (e) {
    var g = e.target.closest && e.target.closest('g.item');
    if (g && sel !== +g.dataset.id && !drag) { sel = +g.dataset.id; render(true); }
  });

  document.addEventListener('keydown', function (e) {
    if (!sel) return;
    var t = e.target, tag = t && t.tagName;
    if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA' || (t && t.isContentEditable)) return;
    // Only react when focus is in the planner or nowhere in particular.
    if (t !== document.body && !root.contains(t)) return;
    var step = e.shiftKey ? 1 : SNAP, k = e.key;
    if (k === 'ArrowLeft') nudge(-step, 0);
    else if (k === 'ArrowRight') nudge(step, 0);
    else if (k === 'ArrowUp') nudge(0, -step);
    else if (k === 'ArrowDown') nudge(0, step);
    else if (k === 'r' || k === 'R') rotate();
    else if (k === 'Delete' || k === 'Backspace') remove();
    else if (k === 'Escape') { sel = null; render(); }
    else return;
    e.preventDefault();
  });

  // Palette.
  var pal = $('lp-palette');
  pal.innerHTML = Object.keys(CAT).map(function (k) {
    var c = CAT[k];
    var size = k === 'wall' ? 'resizable' : fmt(c[2]) + ' &times; ' + fmt(c[3]) + ' ft';
    return '<button type="button" data-add="' + k + '" aria-label="Add ' + esc(c[0]) + '">' + esc(c[0]) + '<small>' + size + '</small></button>';
  }).join('');
  pal.addEventListener('click', function (e) { var b = e.target.closest('button[data-add]'); if (b) add(b.dataset.add); });

  // Toolbar and footprint controls.
  $('lp-rotate').addEventListener('click', rotate);
  $('lp-del').addEventListener('click', remove);
  $('lp-dup').addEventListener('click', duplicate);
  $('lp-clear').addEventListener('click', function () { state.items = []; sel = null; msg('Layout cleared. Add items from the list.'); render(); save(); });
  $('lp-sample').addEventListener('click', function () { sample(); syncFootInputs(); msg('Sample 8.5 x 24 ft layout loaded.'); render(); save(); });
  $('lp-preset').addEventListener('change', function () {
    var v = this.value; if (v === 'custom') { $('lp-w').focus(); return; }
    var p = v.split('x'); $('lp-w').value = p[0]; $('lp-l').value = p[1];
    setFootprint(p[0], p[1]);
  });
  function onDims() { setFootprint($('lp-w').value, $('lp-l').value); syncFootInputs(); }
  $('lp-w').addEventListener('change', onDims);
  $('lp-l').addEventListener('change', onDims);
  $('lp-wall-len').addEventListener('input', function () {
    var it = byId(sel); if (!it || it.t !== 'wall') return;
    var v = snap(+this.value); if (!(v >= 1)) return;
    var max = it.r % 2 ? state.fw : state.fl;
    it.bw = Math.min(v, max); clampItem(it); render(); save();
  });

  // PNG export: serialize a standalone SVG and draw it to a canvas.
  $('lp-png').addEventListener('click', function () {
    var vb = viewBox(), scale = Math.min(48, 2400 / vb[2]);
    var head = 1.6; // title band in feet
    var W = Math.round(vb[2] * scale), H = Math.round((vb[3] + head) * scale);
    var m = markup(true);
    var title = 'Tiny house layout: ' + fmt(state.fw) + ' x ' + fmt(state.fl) + ' ft (' + fmt(state.fw * state.fl) + ' sq ft)';
    var xml = '<svg xmlns="' + NS + '" width="' + W + '" height="' + H + '" viewBox="' + vb[0] + ' ' + (vb[1] - head) + ' ' + vb[2] + ' ' + (vb[3] + head) + '">' +
      '<rect x="' + vb[0] + '" y="' + (vb[1] - head) + '" width="' + vb[2] + '" height="' + (vb[3] + head) + '" fill="#0d3c48"/>' +
      '<text x="' + (vb[0] + 0.4) + '" y="' + (vb[1] - head + 0.95) + '" font-size="0.6" font-family="Inter, Arial, sans-serif" font-weight="700" fill="#ffffff">' + esc(title) + '</text>' +
      '<text x="' + (vb[0] + vb[2] - 0.4) + '" y="' + (vb[1] - head + 0.95) + '" font-size="0.42" font-family="Inter, Arial, sans-serif" fill="#9fe0dc" text-anchor="end">tinyhomesblueprint.com</text>' +
      m.svg + '</svg>';
    var img = new Image();
    img.onload = function () {
      var cv = document.createElement('canvas'); cv.width = W; cv.height = H;
      var ctx = cv.getContext('2d'); ctx.drawImage(img, 0, 0, W, H);
      var name = 'tiny-house-layout-' + fmt(state.fw) + 'x' + fmt(state.fl) + '.png';
      function dl(href) { var a = document.createElement('a'); a.href = href; a.download = name; document.body.appendChild(a); a.click(); document.body.removeChild(a); }
      if (cv.toBlob) cv.toBlob(function (b) { if (!b) { dl(cv.toDataURL('image/png')); return; } var u = URL.createObjectURL(b); dl(u); setTimeout(function () { URL.revokeObjectURL(u); }, 4000); }, 'image/png');
      else dl(cv.toDataURL('image/png'));
      msg('PNG downloaded.');
    };
    img.onerror = function () { msg('Sorry, this browser could not create the image.', true); };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
  });

  if (!load()) sample();
  syncFootInputs();
  render();
})();
