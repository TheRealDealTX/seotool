/* Mid-Century Room Designer — Vintique Flea mini game */
(function () {
  'use strict';

  var SLUG = 'room-designer';
  var SAVE_KEY = 'vf_game_room_layout';
  var RATIO = 1.6; // canvas width / height (16:10)
  var MAX_PIECES = 40;

  /* ---------- shared helpers ---------- */
  function amazon(q) {
    try { if (window.VF && typeof window.VF.amazon === 'function') return window.VF.amazon(q); } catch (e) {}
    return 'https://www.amazon.com/s?k=' + encodeURIComponent(q) + '&tag=josephrayditt-20';
  }
  function shopUrl(s) {
    try { if (window.VF && typeof window.VF.shopUrl === 'function') return window.VF.shopUrl(s); } catch (e) {}
    return '/shop/' + s + '/';
  }
  function store(key, val) {
    try {
      if (arguments.length > 1) {
        if (val === undefined) window.localStorage.removeItem(key);
        else window.localStorage.setItem(key, JSON.stringify(val));
        return true;
      }
      var raw = window.localStorage.getItem(key);
      return raw == null ? null : JSON.parse(raw);
    } catch (e) { return null; }
  }
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v == null || v === false) return;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k === 'html') el.innerHTML = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : v);
    });
    (kids || []).forEach(function (c) { if (c != null) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function linkItem(href, ico, label, sub, amz) {
    var a = h('a', { class: 'g-link', href: href }, [
      h('span', { class: 'g-link__ico', 'aria-hidden': 'true', html: ico }),
      h('span', null, [label, sub ? h('small', { text: sub }) : null])
    ]);
    if (amz) { a.target = '_blank'; a.rel = 'sponsored nofollow noopener'; }
    return h('li', null, [a]);
  }

  /* ---------- palette & drawings ---------- */
  var C = { teak: '#a0612f', teakL: '#bf7a43', teakD: '#6e3d1c', rust: '#c2552d', mustard: '#d9a21b', teal: '#1f6f6b', tealL: '#2d8a85', olive: '#6b7a3a', ink: '#2b2420', cream: '#fffaf1', brass: '#c99a3b', chrome: '#9aa3a8', leaf: '#4f7a3a', leaf2: '#3e6b4f' };

  function rays(cx, cy, n, r1, r2, r3, color, width, dots) {
    var s = '';
    for (var i = 0; i < n; i++) {
      var a = (i / n) * Math.PI * 2;
      var r = i % 2 ? r3 : r2;
      var x1 = cx + Math.cos(a) * r1, y1 = cy + Math.sin(a) * r1, x2 = cx + Math.cos(a) * r, y2 = cy + Math.sin(a) * r;
      s += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" stroke="' + color + '" stroke-width="' + width + '" stroke-linecap="round"/>';
      if (dots) s += '<circle cx="' + x2.toFixed(1) + '" cy="' + y2.toFixed(1) + '" r="' + (i % 2 ? 2.2 : 3) + '" fill="' + color + '"/>';
    }
    return s;
  }
  function leg(x1, y1, x2, y2, w) {
    return '<path d="M' + (x1 - w) + ' ' + y1 + ' L' + (x1 + w) + ' ' + y1 + ' L' + (x2 + w / 3) + ' ' + y2 + ' L' + (x2 - w / 3) + ' ' + y2 + 'Z" fill="' + C.teakD + '"/>';
  }

  var PIECES = {
    sofa: { label: 'Sofa', vb: [200, 100], w: 34, zone: 'floor', q: 'sofa', svg: function () {
      return '<rect x="12" y="26" width="176" height="40" rx="12" fill="' + C.teal + '"/>' +
        '<circle cx="50" cy="44" r="2.5" fill="' + C.ink + '" opacity=".4"/><circle cx="100" cy="44" r="2.5" fill="' + C.ink + '" opacity=".4"/><circle cx="150" cy="44" r="2.5" fill="' + C.ink + '" opacity=".4"/>' +
        '<rect x="20" y="54" width="79" height="24" rx="7" fill="' + C.tealL + '"/><rect x="101" y="54" width="79" height="24" rx="7" fill="' + C.tealL + '"/>' +
        '<rect x="4" y="46" width="22" height="34" rx="9" fill="' + C.teal + '"/><rect x="174" y="46" width="22" height="34" rx="9" fill="' + C.teal + '"/>' +
        '<rect x="8" y="78" width="184" height="7" rx="2" fill="' + C.teak + '"/>' +
        leg(22, 85, 16, 99, 3.5) + leg(178, 85, 184, 99, 3.5) + leg(100, 85, 100, 97, 3);
    } },
    lounge: { label: 'Lounge chair', vb: [110, 100], w: 16, zone: 'floor', q: 'lounge chair and ottoman', svg: function () {
      return '<path d="M26 6 Q16 8 18 26 L26 58 L60 52 L54 12 Q50 2 26 6Z" fill="' + C.teak + '"/>' +
        '<path d="M28 12 Q22 14 24 28 L30 52 L54 47 L49 16 Q46 9 28 12Z" fill="' + C.ink + '"/>' +
        '<path d="M20 58 Q16 70 30 70 L72 66 Q82 64 80 54 L66 50 L28 56Z" fill="' + C.teak + '"/>' +
        '<path d="M26 60 Q24 66 32 66 L70 62 Q76 60 74 55 L64 53 L30 58Z" fill="' + C.ink + '"/>' +
        '<rect x="47" y="68" width="5" height="16" fill="' + C.ink + '"/>' +
        '<path d="M49 84 L28 96 M49 84 L72 96 M49 84 L50 98" stroke="' + C.ink + '" stroke-width="3.5" stroke-linecap="round"/>' +
        '<path d="M80 72 Q78 64 88 64 L104 64 Q110 64 108 72 L106 78 L82 78Z" fill="' + C.teak + '"/>' +
        '<rect x="84" y="66" width="20" height="8" rx="3" fill="' + C.ink + '"/>' +
        '<path d="M94 78 L86 96 M94 78 L102 96" stroke="' + C.ink + '" stroke-width="3" stroke-linecap="round"/>';
    } },
    credenza: { label: 'Credenza', vb: [200, 90], w: 32, zone: 'floor', q: 'credenza sideboard', svg: function () {
      var doors = '';
      for (var i = 0; i < 4; i++) {
        var x = 14 + i * 44;
        doors += '<rect x="' + x + '" y="18" width="40" height="40" rx="2" fill="' + (i % 2 ? C.teakL : C.teak) + '" stroke="' + C.teakD + '" stroke-width="1.5"/>';
        for (var j = 0; j < 5; j++) doors += '<line x1="' + (x + 6 + j * 7) + '" y1="22" x2="' + (x + 6 + j * 7) + '" y2="54" stroke="' + C.teakD + '" stroke-width=".8" opacity=".35"/>';
        doors += '<rect x="' + (x + (i % 2 ? 4 : 32)) + '" y="34" width="4" height="10" rx="2" fill="' + C.brass + '"/>';
      }
      return '<rect x="6" y="10" width="188" height="56" rx="4" fill="' + C.teak + '" stroke="' + C.teakD + '" stroke-width="2"/>' + doors +
        '<rect x="10" y="64" width="180" height="5" fill="' + C.teakD + '"/>' + leg(22, 69, 16, 88, 3.5) + leg(178, 69, 184, 88, 3.5);
    } },
    mirror: { label: 'Sunburst mirror', vb: [100, 100], w: 13, zone: 'wall', q: 'sunburst mirror', svg: function () {
      return rays(50, 50, 24, 22, 47, 38, C.brass, 2.6, true) +
        '<circle cx="50" cy="50" r="21" fill="#cfe3e1" stroke="' + C.brass + '" stroke-width="4"/>' +
        '<path d="M38 42 Q44 34 54 34" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>';
    } },
    arclamp: { label: 'Arc floor lamp', vb: [130, 200], w: 18, zone: 'floor', q: 'arc floor lamp', svg: function () {
      return '<path d="M26 190 L26 118 Q26 26 104 36" stroke="' + C.chrome + '" stroke-width="4.5" fill="none" stroke-linecap="round"/>' +
        '<path d="M80 64 Q80 30 104 30 Q128 30 128 64Z" fill="' + C.mustard + '" stroke="' + C.ink + '" stroke-width="1.5"/>' +
        '<ellipse cx="104" cy="66" rx="14" ry="4" fill="#fff6c8"/>' +
        '<rect x="8" y="184" width="36" height="14" rx="4" fill="#efe9df" stroke="' + C.ink + '" stroke-width="1.5"/>';
    } },
    plant: { label: 'Potted plant', vb: [70, 120], w: 9, zone: 'floor', q: 'planter with stand', svg: function () {
      return '<ellipse cx="22" cy="44" rx="9" ry="22" transform="rotate(-25 22 44)" fill="' + C.leaf + '"/>' +
        '<ellipse cx="48" cy="40" rx="9" ry="24" transform="rotate(22 48 40)" fill="' + C.leaf2 + '"/>' +
        '<ellipse cx="35" cy="28" rx="9" ry="26" fill="' + C.olive + '"/>' +
        '<ellipse cx="16" cy="64" rx="7" ry="16" transform="rotate(-50 16 64)" fill="' + C.leaf2 + '"/>' +
        '<ellipse cx="54" cy="62" rx="7" ry="16" transform="rotate(50 54 62)" fill="' + C.leaf + '"/>' +
        '<path d="M35 30 L35 76 M35 58 L22 46 M35 52 L48 42" stroke="' + C.leaf2 + '" stroke-width="2" fill="none"/>' +
        '<path d="M16 74 L54 74 L49 100 L21 100Z" fill="' + C.rust + '"/><rect x="14" y="72" width="42" height="5" rx="2" fill="#a9461f"/>' +
        leg(24, 100, 18, 119, 2) + leg(46, 100, 52, 119, 2);
    } },
    rug: { label: 'Area rug', vb: [240, 50], w: 46, zone: 'rug', q: 'geometric area rug', svg: function () {
      var d = '';
      for (var i = 0; i < 7; i++) {
        var cx = 42 + i * 26;
        d += '<path d="M' + cx + ' 13 L' + (cx + 9) + ' 25 L' + cx + ' 37 L' + (cx - 9) + ' 25Z" fill="' + (i % 2 ? C.teal : C.rust) + '"/>';
      }
      return '<path d="M24 4 L216 4 L238 46 L2 46Z" fill="' + C.mustard + '"/>' +
        '<path d="M32 9 L208 9 L226 41 L14 41Z" fill="none" stroke="' + C.cream + '" stroke-width="2"/>' + d;
    } },
    record: { label: 'Record player console', vb: [120, 100], w: 16, zone: 'floor', q: 'record player console turntable', svg: function () {
      return '<rect x="8" y="38" width="104" height="40" rx="3" fill="' + C.teak + '" stroke="' + C.teakD + '" stroke-width="2"/>' +
        '<rect x="66" y="44" width="40" height="28" rx="2" fill="#d8c9b0"/>' +
        '<path d="M70 48 H102 M70 53 H102 M70 58 H102 M70 63 H102 M70 68 H102" stroke="' + C.teakD + '" stroke-width="1" opacity=".5"/>' +
        '<rect x="14" y="46" width="44" height="26" rx="2" fill="' + C.teakL + '"/><circle cx="24" cy="59" r="3" fill="' + C.brass + '"/><circle cx="36" cy="59" r="3" fill="' + C.brass + '"/>' +
        '<ellipse cx="42" cy="34" rx="26" ry="6" fill="' + C.ink + '"/><ellipse cx="42" cy="33" rx="7" ry="1.8" fill="' + C.rust + '"/>' +
        '<path d="M84 28 L84 32 L62 36" stroke="' + C.chrome + '" stroke-width="2" fill="none" stroke-linecap="round"/>' +
        '<rect x="6" y="36" width="108" height="4" fill="' + C.teakD + '"/>' +
        leg(18, 78, 12, 98, 3) + leg(102, 78, 108, 98, 3);
    } },
    sidetable: { label: 'Side table', vb: [70, 72], w: 9, zone: 'floor', q: 'side table', svg: function () {
      return '<path d="M35 22 Q30 6 38 4 Q42 12 35 22Z" fill="' + C.teal + '"/><rect x="31" y="10" width="8" height="12" rx="3" fill="' + C.mustard + '"/>' +
        '<ellipse cx="35" cy="26" rx="32" ry="7" fill="' + C.teak + '" stroke="' + C.teakD + '" stroke-width="1.5"/>' +
        leg(14, 30, 6, 70, 2.5) + leg(56, 30, 64, 70, 2.5) + leg(35, 32, 35, 66, 2) +
        '<ellipse cx="35" cy="52" rx="22" ry="4" fill="' + C.teakL + '"/>';
    } },
    shelving: { label: 'Wall shelving', vb: [130, 150], w: 18, zone: 'wall', q: 'wall shelving unit', svg: function () {
      var books = '', colors = [C.rust, C.mustard, C.teal, C.olive, C.cream, C.rust];
      for (var i = 0; i < 6; i++) books += '<rect x="' + (14 + i * 7) + '" y="' + (18 - (i % 3) * 2) + '" width="6" height="' + (22 + (i % 3) * 2) + '" fill="' + colors[i] + '" stroke="' + C.ink + '" stroke-width=".6"/>';
      return '<path d="M8 2 V148 M122 2 V148" stroke="' + C.ink + '" stroke-width="2.5"/>' +
        '<path d="M8 10 H122 M8 30 H122 M8 50 H122 M8 70 H122 M8 90 H122 M8 110 H122 M8 130 H122" stroke="' + C.ink + '" stroke-width=".8" opacity=".5"/>' +
        '<rect x="4" y="40" width="122" height="6" rx="1" fill="' + C.teak + '"/>' +
        '<rect x="4" y="86" width="122" height="6" rx="1" fill="' + C.teak + '"/>' +
        '<rect x="4" y="132" width="122" height="6" rx="1" fill="' + C.teak + '"/>' + books +
        '<path d="M86 40 Q80 24 92 20 Q104 24 98 40Z" fill="' + C.teal + '"/>' +
        '<rect x="20" y="64" width="34" height="22" rx="2" fill="' + C.cream + '" stroke="' + C.ink + '"/><circle cx="37" cy="75" r="6" fill="' + C.rust + '"/>' +
        '<ellipse cx="94" cy="80" rx="14" ry="6" fill="' + C.leaf + '"/><path d="M84 80 L104 80 L100 86 L88 86Z" fill="' + C.mustard + '"/>' +
        '<path d="M30 132 Q22 112 36 108 Q50 112 42 132Z" fill="' + C.mustard + '"/><rect x="70" y="112" width="40" height="20" fill="' + C.ink + '"/><circle cx="90" cy="122" r="7" fill="' + C.rust + '"/>';
    } },
    painting: { label: 'Abstract painting', vb: [110, 86], w: 16, zone: 'wall', q: 'abstract wall art print', svg: function () {
      return '<rect x="2" y="2" width="106" height="82" rx="2" fill="' + C.teakD + '"/>' +
        '<rect x="8" y="8" width="94" height="70" fill="' + C.cream + '"/>' +
        '<circle cx="36" cy="38" r="17" fill="' + C.mustard + '"/>' +
        '<rect x="54" y="20" width="30" height="40" fill="' + C.rust + '" transform="rotate(12 69 40)"/>' +
        '<path d="M14 70 Q40 46 70 70" stroke="' + C.teal + '" stroke-width="7" fill="none"/>' +
        '<path d="M20 18 L96 66" stroke="' + C.ink + '" stroke-width="1.5"/><circle cx="86" cy="22" r="5" fill="' + C.ink + '"/>';
    } },
    clock: { label: 'Starburst clock', vb: [100, 100], w: 10, zone: 'wall', q: 'starburst wall clock', svg: function () {
      var tips = '';
      for (var i = 0; i < 12; i++) {
        var a = i / 12 * Math.PI * 2, x = 50 + Math.cos(a) * 42, y = 50 + Math.sin(a) * 42;
        tips += '<rect x="' + (x - 3.5).toFixed(1) + '" y="' + (y - 3.5).toFixed(1) + '" width="7" height="7" transform="rotate(45 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')" fill="' + (i % 3 ? C.brass : C.teak) + '"/>';
      }
      return rays(50, 50, 12, 14, 40, 40, C.brass, 2.4, false) + tips +
        '<circle cx="50" cy="50" r="15" fill="' + C.teak + '" stroke="' + C.brass + '" stroke-width="2"/>' +
        '<path d="M50 50 L50 40 M50 50 L57 54" stroke="' + C.cream + '" stroke-width="2.2" stroke-linecap="round"/><circle cx="50" cy="50" r="2" fill="' + C.cream + '"/>';
    } }
  };
  var ORDER = ['sofa', 'lounge', 'credenza', 'sidetable', 'arclamp', 'plant', 'rug', 'record', 'shelving', 'painting', 'mirror', 'clock'];

  var WALLS = [
    { id: 'cream', name: 'Cream', c: '#f3e6cc' },
    { id: 'mustard', name: 'Mustard', c: '#e3b448' },
    { id: 'teal', name: 'Teal', c: '#4f938e' },
    { id: 'olive', name: 'Avocado', c: '#9aa660' },
    { id: 'terracotta', name: 'Terracotta', c: '#d77d58' },
    { id: 'charcoal', name: 'Charcoal', c: '#4a433e' }
  ];
  var FLOORS = [
    { id: 'walnut', name: 'Walnut planks', bg: 'repeating-linear-gradient(90deg,#7a4a26 0 38px,#6a3f20 38px 40px), #7a4a26' },
    { id: 'oak', name: 'Light oak', bg: 'repeating-linear-gradient(90deg,#c99a63 0 46px,#b5864f 46px 48px), #c99a63' },
    { id: 'terrazzo', name: 'Terrazzo', bg: 'radial-gradient(circle at 20% 30%,#c2552d 0 2px,transparent 3px) 0 0/34px 26px, radial-gradient(circle at 70% 60%,#1f6f6b 0 2px,transparent 3px) 0 0/28px 30px, radial-gradient(circle at 40% 80%,#d9a21b 0 1.5px,transparent 2.5px) 0 0/22px 18px, #e9e1d3' },
    { id: 'checker', name: 'Checker tile', bg: 'conic-gradient(#2b2420 25%,#f3e6cc 0 50%,#2b2420 0 75%,#f3e6cc 0) 0 0/32px 32px' },
    { id: 'shag', name: 'Green shag', bg: 'repeating-radial-gradient(circle at 30% 40%,#6b7a3a 0 2px,#5d6b31 2px 4px), #6b7a3a' }
  ];

  /* ---------- state ---------- */
  var root, stage, live, canvas, wallEl, floorEl, emptyEl, toolsBox, shopList, paletteBox;
  var room = { pieces: [], wall: 'cream', floor: 'walnut' };
  var selected = null, nextId = 1, drag = null;

  function piece(id) { for (var i = 0; i < room.pieces.length; i++) if (room.pieces[i].id === id) return room.pieces[i]; return null; }
  function dims(p) {
    var d = PIECES[p.type];
    var w = d.w * p.s;
    return { w: w, h: w * (d.vb[1] / d.vb[0]) * RATIO };
  }
  function clampPos(p) {
    var d = dims(p);
    p.x = clamp(p.x, 0, Math.max(0, 100 - d.w));
    p.y = clamp(p.y, 0, Math.max(0, 100 - d.h));
  }

  function svgFor(type, flip) {
    var d = PIECES[type];
    return '<svg viewBox="0 0 ' + d.vb[0] + ' ' + d.vb[1] + '" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMid meet"' +
      (flip ? ' style="transform:scaleX(-1)"' : '') + '>' + d.svg() + '</svg>';
  }

  function announce(t) { live.textContent = ''; window.setTimeout(function () { live.textContent = t; }, 30); }

  /* ---------- canvas rendering ---------- */
  function applyPos(el, p) {
    var d = dims(p);
    el.style.left = p.x + '%';
    el.style.top = p.y + '%';
    el.style.width = d.w + '%';
    el.style.height = d.h + '%';
  }

  function renderCanvas(focusId) {
    var wall = WALLS.filter(function (w) { return w.id === room.wall; })[0] || WALLS[0];
    var floor = FLOORS.filter(function (f) { return f.id === room.floor; })[0] || FLOORS[0];
    wallEl.style.background = wall.c;
    floorEl.style.background = floor.bg;
    Array.prototype.slice.call(canvas.querySelectorAll('.g-room__piece')).forEach(function (n) { n.remove(); });
    room.pieces.forEach(function (p, i) {
      var d = PIECES[p.type];
      var el = h('button', {
        type: 'button',
        class: 'g-room__piece' + (p.id === selected ? ' is-selected' : ''),
        'data-id': String(p.id),
        'aria-label': d.label + (p.id === selected ? ' (selected)' : ''),
        'aria-describedby': 'g-room-keys',
        html: svgFor(p.type, p.f)
      });
      el.style.zIndex = String(i + 1);
      applyPos(el, p);
      el.addEventListener('pointerdown', onDown);
      el.addEventListener('keydown', onKey);
      el.addEventListener('click', function () { if (!el._dragged) select(p.id); el._dragged = false; });
      canvas.appendChild(el);
    });
    emptyEl.hidden = room.pieces.length > 0;
    if (focusId != null) {
      var f = canvas.querySelector('[data-id="' + focusId + '"]');
      if (f) f.focus({ preventScroll: true });
    }
    renderTools();
    renderShop();
    renderSwatches();
  }

  function select(id) {
    selected = id;
    Array.prototype.forEach.call(canvas.querySelectorAll('.g-room__piece'), function (el) {
      var on = Number(el.getAttribute('data-id')) === id;
      el.classList.toggle('is-selected', on);
      var p = piece(Number(el.getAttribute('data-id')));
      if (p) el.setAttribute('aria-label', PIECES[p.type].label + (on ? ' (selected)' : ''));
    });
    renderTools();
  }

  /* ---------- pointer dragging ---------- */
  function onDown(e) {
    if (e.button != null && e.button !== 0) return;
    var el = e.currentTarget;
    var id = Number(el.getAttribute('data-id'));
    var p = piece(id);
    if (!p) return;
    e.preventDefault();
    el.focus({ preventScroll: true });
    if (selected !== id) select(id);
    var rect = canvas.getBoundingClientRect();
    drag = { el: el, p: p, sx: e.clientX, sy: e.clientY, ox: p.x, oy: p.y, rect: rect, moved: false, pid: e.pointerId };
    try { el.setPointerCapture(e.pointerId); } catch (err) {}
    el.classList.add('is-dragging');
    el.addEventListener('pointermove', onMove);
    el.addEventListener('pointerup', onUp);
    el.addEventListener('pointercancel', onUp);
  }
  function onMove(e) {
    if (!drag || e.pointerId !== drag.pid) return;
    var dx = (e.clientX - drag.sx) / drag.rect.width * 100;
    var dy = (e.clientY - drag.sy) / drag.rect.height * 100;
    if (Math.abs(dx) + Math.abs(dy) > 0.5) drag.moved = true;
    drag.p.x = drag.ox + dx;
    drag.p.y = drag.oy + dy;
    clampPos(drag.p);
    applyPos(drag.el, drag.p);
  }
  function onUp(e) {
    if (!drag || e.pointerId !== drag.pid) return;
    var el = drag.el;
    try { el.releasePointerCapture(e.pointerId); } catch (err) {}
    el.classList.remove('is-dragging');
    el.removeEventListener('pointermove', onMove);
    el.removeEventListener('pointerup', onUp);
    el.removeEventListener('pointercancel', onUp);
    el._dragged = drag.moved;
    drag = null;
  }

  /* ---------- keyboard ---------- */
  function onKey(e) {
    var id = Number(e.currentTarget.getAttribute('data-id'));
    var p = piece(id);
    if (!p) return;
    var step = e.shiftKey ? 5 : 1;
    var moved = true;
    switch (e.key) {
      case 'ArrowLeft': p.x -= step; break;
      case 'ArrowRight': p.x += step; break;
      case 'ArrowUp': p.y -= step * RATIO; break;
      case 'ArrowDown': p.y += step * RATIO; break;
      case 'Delete': case 'Backspace': e.preventDefault(); select(id); act('delete'); return;
      case 'f': case 'F': select(id); act('flip'); return;
      case '+': case '=': select(id); act('bigger'); return;
      case '-': case '_': select(id); act('smaller'); return;
      case ']': select(id); act('forward'); return;
      case '[': select(id); act('back'); return;
      case 'Escape': select(null); return;
      default: moved = false;
    }
    if (moved) {
      e.preventDefault();
      if (selected !== id) select(id);
      clampPos(p);
      applyPos(e.currentTarget, p);
    }
  }

  /* ---------- actions ---------- */
  function addPiece(type) {
    if (room.pieces.length >= MAX_PIECES) { announce('That\'s a full room! Remove something first.'); return; }
    var d = PIECES[type];
    var p = { id: nextId++, type: type, x: 0, y: 0, s: 1, f: false };
    var dm = dims(p);
    var jitter = (Math.random() - 0.5) * 30;
    p.x = 50 - dm.w / 2 + jitter;
    if (d.zone === 'wall') p.y = 10 + Math.random() * 8;
    else if (d.zone === 'rug') p.y = 97 - dm.h;
    else p.y = 92 - dm.h;
    clampPos(p);
    if (d.zone === 'rug') room.pieces.unshift(p); else room.pieces.push(p);
    selected = p.id;
    renderCanvas(p.id);
    announce(d.label + ' added. Use arrow keys to move it.');
  }

  function act(kind) {
    var p = piece(selected);
    if (!p) return;
    var label = PIECES[p.type].label, idx = room.pieces.indexOf(p), msg = '';
    if (kind === 'delete') {
      room.pieces.splice(idx, 1);
      selected = null;
      renderCanvas();
      var next = canvas.querySelector('.g-room__piece');
      (next || paletteBox.querySelector('button')).focus({ preventScroll: true });
      return announce(label + ' removed.');
    }
    if (kind === 'flip') { p.f = !p.f; msg = label + ' flipped.'; }
    if (kind === 'bigger') { p.s = Math.min(2, Math.round((p.s + 0.15) * 100) / 100); msg = label + ' size ' + Math.round(p.s * 100) + '%.'; }
    if (kind === 'smaller') { p.s = Math.max(0.5, Math.round((p.s - 0.15) * 100) / 100); msg = label + ' size ' + Math.round(p.s * 100) + '%.'; }
    if (kind === 'forward' && idx < room.pieces.length - 1) { room.pieces.splice(idx, 1); room.pieces.splice(idx + 1, 0, p); msg = label + ' brought forward.'; }
    if (kind === 'back' && idx > 0) { room.pieces.splice(idx, 1); room.pieces.splice(idx - 1, 0, p); msg = label + ' sent back.'; }
    if (kind === 'forward' && !msg) msg = label + ' is already in front.';
    if (kind === 'back' && !msg) msg = label + ' is already at the back.';
    clampPos(p);
    var hadFocus = document.activeElement && document.activeElement.classList && document.activeElement.classList.contains('g-room__piece');
    renderCanvas(hadFocus ? p.id : null);
    announce(msg);
  }

  function renderTools() {
    var p = piece(selected);
    toolsBox.innerHTML = '';
    var mk = function (kind, text, title) {
      return h('button', { type: 'button', class: 'g-btn g-btn--sm', disabled: !p, title: title, onclick: function () { act(kind); } }, [text]);
    };
    toolsBox.appendChild(h('span', { class: 'g-sub', style: 'align-self:center;margin:0 4px 0 0;font-size:.85rem', text: p ? 'Selected: ' + PIECES[p.type].label : 'Tap a piece to select it' }));
    toolsBox.appendChild(mk('forward', '⬆ Forward', 'Bring forward (])'));
    toolsBox.appendChild(mk('back', '⬇ Back', 'Send back ([)'));
    toolsBox.appendChild(mk('flip', '⇋ Flip', 'Flip (F)'));
    toolsBox.appendChild(mk('bigger', '＋ Bigger', 'Bigger (+)'));
    toolsBox.appendChild(mk('smaller', '－ Smaller', 'Smaller (-)'));
    var del = mk('delete', '✕ Delete', 'Delete (Del)');
    del.classList.add('g-btn--rust');
    toolsBox.appendChild(del);
  }

  var swatchWrap;
  function renderSwatches() {
    swatchWrap.innerHTML = '';
    var wallSet = h('fieldset', { class: 'g-room__swgroup' }, [h('legend', { text: 'Wall color' })]);
    WALLS.forEach(function (w) {
      wallSet.appendChild(h('button', { type: 'button', class: 'g-room__sw', style: 'background:' + w.c, 'aria-label': w.name + ' wall', title: w.name, 'aria-pressed': room.wall === w.id ? 'true' : 'false',
        onclick: function () { room.wall = w.id; wallEl.style.background = w.c; updatePressed(wallSet, this); announce('Wall painted ' + w.name + '.'); } }));
    });
    var floorSet = h('fieldset', { class: 'g-room__swgroup' }, [h('legend', { text: 'Floor' })]);
    FLOORS.forEach(function (f) {
      floorSet.appendChild(h('button', { type: 'button', class: 'g-room__sw', style: 'background:' + f.bg, 'aria-label': f.name + ' floor', title: f.name, 'aria-pressed': room.floor === f.id ? 'true' : 'false',
        onclick: function () { room.floor = f.id; floorEl.style.background = f.bg; updatePressed(floorSet, this); announce(f.name + ' floor.'); } }));
    });
    swatchWrap.appendChild(wallSet);
    swatchWrap.appendChild(floorSet);
  }
  function updatePressed(set, btn) {
    Array.prototype.forEach.call(set.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
  }

  function placedTypes() {
    var seen = {}, out = [];
    room.pieces.forEach(function (p) { if (!seen[p.type]) { seen[p.type] = 1; out.push(p.type); } });
    return out;
  }

  function shopLinks(types) {
    return types.map(function (t) {
      var d = PIECES[t];
      return linkItem(amazon('mid century modern ' + d.q), '<svg viewBox="0 0 ' + d.vb[0] + ' ' + d.vb[1] + '" width="32" height="28" aria-hidden="true" focusable="false">' + d.svg() + '</svg>', d.label, 'Mid-century style on Amazon', true);
    });
  }

  function renderShop() {
    shopList.innerHTML = '';
    var types = placedTypes();
    if (!types.length) { shopList.appendChild(h('li', { class: 'g-sub', text: 'Add pieces to build your shopping list.' })); return; }
    shopLinks(types).forEach(function (li) { shopList.appendChild(li); });
  }

  function save() {
    var ok = store(SAVE_KEY, { pieces: room.pieces, wall: room.wall, floor: room.floor, v: 1 });
    announce(ok ? 'Room saved on this device.' : 'Sorry, saving isn\'t available in this browser.');
    flash(ok ? 'Saved! ✓' : 'Couldn\'t save');
  }
  function validPiece(p) {
    return p && PIECES[p.type] && isFinite(p.x) && isFinite(p.y) && isFinite(p.s);
  }
  function load(silent) {
    var data = store(SAVE_KEY);
    if (!data || !Array.isArray(data.pieces)) { if (!silent) { announce('No saved room yet.'); flash('Nothing saved yet'); } return false; }
    room.pieces = data.pieces.filter(validPiece).slice(0, MAX_PIECES).map(function (p) {
      var q = { id: nextId++, type: p.type, x: Number(p.x), y: Number(p.y), s: clamp(Number(p.s), 0.5, 2), f: !!p.f };
      clampPos(q);
      return q;
    });
    room.wall = WALLS.some(function (w) { return w.id === data.wall; }) ? data.wall : 'cream';
    room.floor = FLOORS.some(function (f) { return f.id === data.floor; }) ? data.floor : 'walnut';
    selected = null;
    renderCanvas();
    if (!silent) { announce('Saved room loaded.'); flash('Loaded ✓'); }
    return true;
  }
  function clearRoom() {
    if (room.pieces.length && !window.confirm('Clear every piece from the room?')) return;
    room.pieces = [];
    selected = null;
    renderCanvas();
    announce('Room cleared.');
  }

  var statusEl;
  function flash(t) {
    statusEl.textContent = t;
    window.clearTimeout(flash._t);
    flash._t = window.setTimeout(function () { statusEl.textContent = ''; }, 2200);
  }

  /* ---------- results ---------- */
  function rate() {
    var types = placedTypes();
    var has = function (t) { return types.indexOf(t) >= 0; };
    var score = Math.min(types.length, 8) * 8;
    if (has('rug')) score += 8;
    if (has('arclamp')) score += 6;
    if (has('plant')) score += 6;
    if (has('painting') || has('mirror') || has('clock')) score += 8;
    if (has('sofa') || has('lounge')) score += 8;
    if (room.pieces.length > 14) score -= (room.pieces.length - 14) * 3;
    score = clamp(score, 0, 100);
    var tips = [];
    if (!has('rug')) tips.push('a geometric rug to anchor the seating');
    if (!has('plant')) tips.push('a leafy plant on tapered legs');
    if (!has('arclamp')) tips.push('an arc lamp for that sweeping silhouette');
    if (!(has('painting') || has('mirror') || has('clock'))) tips.push('a sunburst or abstract art on the wall');
    var title = score >= 85 ? ['🍸', 'Mad Men Approved'] : score >= 60 ? ['🛋️', 'Atomic Ranch Ready'] : score >= 35 ? ['🪴', 'Mod in Progress'] : ['📐', 'Blank Canvas Energy'];
    return { score: score, title: title, tips: tips.slice(0, 2), types: types };
  }

  function showResults() {
    var r = rate();
    stage.hidden = true;
    var panel = h('section', { class: 'g-card g-results g-pop', 'aria-labelledby': 'g-room-res' });
    var again = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: function () {
      room.pieces = []; selected = null; panel.remove(); stage.hidden = false; renderCanvas(); paletteBox.querySelector('button').focus({ preventScroll: true }); announce('Fresh room. Start decorating!');
    } }, ['↻ Design a new room']);
    var keep = h('button', { type: 'button', class: 'g-btn g-btn--ghost', onclick: function () { panel.remove(); stage.hidden = false; finishBtn.focus({ preventScroll: true }); } }, ['✎ Keep editing']);
    var links = [linkItem(shopUrl('mid-century-modern'), '🏷️', 'Shop Mid-Century Modern', 'Authentic pieces from Vintique Flea dealers')]
      .concat(r.types.length ? [] : [linkItem(shopUrl('rustic-home-decor'), '🪵', 'Shop Rustic Home Decor', 'More looks to mix in')]);
    panel.appendChild(h('div', { class: 'g-results__badge', 'aria-hidden': 'true', text: r.title[0] }));
    panel.appendChild(h('h2', { class: 'g-title', id: 'g-room-res', text: r.title[1] }));
    panel.appendChild(h('p', { class: 'g-results__big', text: r.score + '/100' }));
    panel.appendChild(h('p', { text: room.pieces.length + ' piece' + (room.pieces.length === 1 ? '' : 's') + ' placed across ' + r.types.length + ' styles of furniture.' + (r.tips.length ? ' To push it further, try ' + r.tips.join(' and ') + '.' : ' A beautifully balanced mid-century room!') }));
    panel.appendChild(h('div', { class: 'g-row g-row--center g-mt' }, [again, keep]));
    panel.appendChild(h('ul', { class: 'g-links' }, links));
    if (r.types.length) {
      panel.appendChild(h('h3', { class: 'g-sub', style: 'font-weight:700;margin-top:18px', text: 'Shop this look' }));
      panel.appendChild(h('ul', { class: 'g-links' }, shopLinks(r.types)));
    }
    panel.appendChild(h('p', { class: 'g-disclose', text: 'Amazon links are affiliate links; we may earn a small commission.' }));
    root.insertBefore(panel, live);
    announce(r.title[1] + '. Style score ' + r.score + ' out of 100.');
    again.focus({ preventScroll: true });
  }

  /* ---------- build UI ---------- */
  var finishBtn;
  function build() {
    stage.innerHTML = '';
    paletteBox = h('div', { class: 'g-room__palette', role: 'group', 'aria-label': 'Add furniture' });
    ORDER.forEach(function (t) {
      var d = PIECES[t];
      paletteBox.appendChild(h('button', { type: 'button', class: 'g-room__add', 'aria-label': 'Add ' + d.label, onclick: function () { addPiece(t); },
        html: '<svg viewBox="0 0 ' + d.vb[0] + ' ' + d.vb[1] + '" aria-hidden="true" focusable="false">' + d.svg() + '</svg><span>' + d.label + '</span>' }));
    });
    wallEl = h('div', { class: 'g-room__wall' });
    floorEl = h('div', { class: 'g-room__floor' });
    emptyEl = h('div', { class: 'g-room__empty', text: 'Your empty room awaits. Pick a piece to get started!' });
    canvas = h('div', { class: 'g-room__canvas', role: 'group', 'aria-label': 'Room canvas. Pieces are buttons; select one and use arrow keys to move it.' }, [wallEl, floorEl, emptyEl]);
    canvas.addEventListener('pointerdown', function (e) { if (e.target === canvas || e.target === wallEl || e.target === floorEl) select(null); });
    toolsBox = h('div', { class: 'g-room__tools', role: 'toolbar', 'aria-label': 'Selected piece tools' });
    swatchWrap = h('div', { class: 'g-room__swatches' });
    shopList = h('ul', { class: 'g-room__shop' });
    statusEl = h('span', { class: 'g-sub', style: 'font-weight:600', 'aria-hidden': 'true' });
    finishBtn = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: showResults }, ['✓ I\'m done — rate my room']);

    stage.appendChild(h('section', { class: 'g-card', 'aria-labelledby': 'g-room-title' }, [
      h('div', { class: 'g-head' }, [
        h('div', null, [
          h('h2', { class: 'g-title', id: 'g-room-title', text: 'Mid-Century Room Designer' }),
          h('p', { class: 'g-sub', text: 'Add pieces, drag them into place, and paint the walls.' })
        ])
      ]),
      h('div', { class: 'g-room__layout' }, [
        paletteBox,
        h('div', { class: 'g-room__stagewrap' }, [
          canvas,
          toolsBox,
          h('p', { class: 'g-room__hint', id: 'g-room-keys', text: 'Drag pieces with mouse or touch. Keyboard: arrows move (Shift = bigger steps), F flips, + / − resize, [ ] change layer, Delete removes.' }),
          swatchWrap,
          h('div', { class: 'g-row g-mt' }, [
            h('button', { type: 'button', class: 'g-btn g-btn--teal', onclick: save }, ['💾 Save']),
            h('button', { type: 'button', class: 'g-btn', onclick: function () { load(false); } }, ['📂 Load']),
            h('button', { type: 'button', class: 'g-btn', onclick: clearRoom }, ['🧹 Clear']),
            statusEl
          ]),
          h('div', { class: 'g-row g-mt' }, [finishBtn])
        ])
      ])
    ]));
    stage.appendChild(h('section', { class: 'g-card', 'aria-labelledby': 'g-room-shop' }, [
      h('h3', { class: 'g-title', id: 'g-room-shop', style: 'font-size:1.25rem', text: 'Shop this look' }),
      h('p', { class: 'g-sub', text: 'Every piece in your room, ready to hunt down. Or find the real vintage deal at Vintique Flea.' }),
      shopList,
      h('p', { class: 'g-disclose', text: 'Amazon links are affiliate links; we may earn a small commission.' })
    ]));
  }

  function init() {
    root = document.querySelector('.game[data-game="' + SLUG + '"]') || document.getElementById('game-root');
    if (!root) return;
    root.innerHTML = '';
    stage = h('div', { class: 'g-stage' });
    live = h('p', { class: 'g-sr', 'aria-live': 'polite', role: 'status' });
    root.appendChild(stage);
    root.appendChild(live);
    build();
    if (!load(true)) renderCanvas();
    else announce('Welcome back — your saved room is loaded.');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
