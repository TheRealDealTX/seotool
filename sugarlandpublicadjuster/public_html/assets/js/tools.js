/* Sugar Land Public Adjuster — calculators and tools. Each block runs only if its form is on the page. */
(function () {
  'use strict';
  var $ = function (root, sel) { return root.querySelector(sel); };
  var money = function (n) { return (n < 0 ? '-$' : '$') + Math.round(Math.abs(n)).toLocaleString('en-US'); };
  var num = function (el) { var v = parseFloat(el && el.value); return isFinite(v) ? v : 0; };
  var out = function (form, key, html) { var el = $(form, '[data-out="' + key + '"]'); if (el) el.innerHTML = html; return el; };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  function bind(form, fn) { form.addEventListener('input', fn); form.addEventListener('change', fn); fn(); }
  function store() { try { return window.localStorage; } catch (e) { return null; } }

  /* Settlement calculator */
  var s = document.getElementById('settle');
  if (s) bind(s, function () {
    var real = num(s.real), rcv = num(s.rcv), dep = num(s.dep), ded = num(s.ded), nonrec = num(s.nonrec);
    var acvPolicy = s.policy.value === 'acv';
    var acv = Math.max(0, rcv - dep - ded);
    var recov = acvPolicy ? 0 : Math.max(0, dep - nonrec);
    var total = acv + recov;
    var need = Math.max(0, real - ded);
    var gap = Math.max(0, need - total);
    var pct = need > 0 ? Math.min(100, total / need * 100) : 100;
    out(s, 'acv', money(acv)); out(s, 'recov', money(recov)); out(s, 'total', money(total)); out(s, 'gap', money(gap));
    out(s, 'pct', Math.round(pct) + '%');
    $(s, '[data-out="bar"]').style.width = pct + '%';
    out(s, 'msg', gap > 2500
      ? 'The insurer’s payment falls <strong>' + money(gap) + '</strong> short of what the repairs actually cost (after your deductible). Gaps like this usually come from missing scope, pricing or depreciation issues—worth a second look.'
      : 'The insurer’s numbers are close to your real repair cost. Make sure you collect any recoverable depreciation after repairs are complete.');
  });

  /* Depreciation calculator */
  var d = document.getElementById('deprec');
  if (d) {
    var rows = [];
    var calc = function () {
      var cost = num(d.cost), age = num(d.age), life = Math.max(1, num(d.life)), cap = Math.min(100, Math.max(0, num(d.cap)));
      var pct = Math.min(cap, age / life * 100);
      var dep = cost * pct / 100;
      return { cost: cost, age: age, life: life, pct: pct, dep: dep, acv: cost - dep };
    };
    d.preset.addEventListener('change', function () { if (d.preset.value !== 'custom') d.life.value = d.preset.value; else d.life.focus(); });
    bind(d, function () {
      var r = calc();
      out(d, 'dep', money(r.dep) + ' <small>(' + Math.round(r.pct) + '%)</small>');
      out(d, 'acv', money(r.acv)); out(d, 'rec', money(r.dep));
    });
    var draw = function () {
      var tb = $(d, '[data-list]'), t = { cost: 0, dep: 0, acv: 0 };
      tb.innerHTML = rows.map(function (r, i) {
        t.cost += r.cost; t.dep += r.dep; t.acv += r.acv;
        return '<tr><td>' + esc(r.name) + '</td><td>' + money(r.cost) + '</td><td>' + r.age + ' / ' + r.life + ' yr</td><td>' + money(r.dep) + '</td><td>' + money(r.acv) + '</td><td><button type="button" class="del" data-i="' + i + '" aria-label="Remove">×</button></td></tr>';
      }).join('');
      $(d, '[data-t="cost"]').textContent = money(t.cost); $(d, '[data-t="dep"]').textContent = money(t.dep); $(d, '[data-t="acv"]').textContent = money(t.acv);
      $(d, '[data-list-wrap]').hidden = rows.length === 0;
    };
    $(d, '[data-add]').addEventListener('click', function () {
      var r = calc();
      r.name = d.desc.value.trim() || d.preset.options[d.preset.selectedIndex].text.replace(/\s*\(.*\)$/, '');
      rows.push(r); d.desc.value = ''; draw();
    });
    $(d, '[data-list]').addEventListener('click', function (e) {
      if (e.target.matches('.del')) { rows.splice(+e.target.getAttribute('data-i'), 1); draw(); }
    });
  }

  /* Public adjuster fee calculator */
  var f = document.getElementById('fee');
  if (f) bind(f, function () {
    var offer = num(f.offer), settle = num(f.settle), pct = Math.min(10, Math.max(0, num(f.pct)));
    if (num(f.pct) > 10) f.pct.value = 10;
    var base = f.basis.value === 'new' ? Math.max(0, settle - offer) : settle;
    var fee = base * pct / 100, net = settle - fee, diff = net - offer;
    out(f, 'alone', money(offer)); out(f, 'fee', money(fee)); out(f, 'net', money(net));
    out(f, 'diff', (diff >= 0 ? '+' : '') + money(diff));
    var box = $(f, '[data-out-class="diffbox"]'); box.className = 'result ' + (diff >= 0 ? 'good' : 'bad');
    var breakEven = f.basis.value === 'new' ? offer : offer / (1 - pct / 100);
    out(f, 'msg', diff >= 0
      ? 'In this scenario you would keep <strong>' + money(diff) + ' more</strong> after paying the public adjuster. Break-even: the settlement needs to exceed about <strong>' + money(breakEven) + '</strong>.'
      : 'In this scenario the fee would outweigh the increase. The settlement would need to exceed about <strong>' + money(breakEven) + '</strong> for representation to pay for itself.');
  });

  /* Hurricane deductible calculator */
  var h = document.getElementById('hded');
  if (h) bind(h, function () {
    var flat = h.pct.value === 'flat';
    $(h, '[data-flat]').hidden = !flat;
    var ded = flat ? num(h.flat) : num(h.dwell) * parseFloat(h.pct.value);
    var dmg = num(h.damage), aop = num(h.aop);
    var pays = Math.max(0, dmg - ded), you = Math.min(dmg, ded);
    out(h, 'ded', money(ded)); out(h, 'aopdiff', (ded - aop >= 0 ? '+' : '') + money(ded - aop));
    out(h, 'pays', money(pays)); out(h, 'you', money(you));
    $(h, '[data-out="bar"]').style.width = (dmg > 0 ? Math.min(100, pays / dmg * 100) : 0) + '%';
    out(h, 'msg', dmg <= ded
      ? 'This damage estimate is <strong>below your deductible</strong>, so the insurer would pay nothing. Make sure the estimate includes everything—interior water damage, fences, gutters and debris removal often push a claim over the line.'
      : 'Your insurer would cover about <strong>' + Math.round(pays / dmg * 100) + '%</strong> of this storm damage. Your wind deductible is ' + money(ded) + '—' + (ded > aop ? money(ded - aop) + ' more than' : 'no more than') + ' your all-other-perils deductible.');
  });

  /* Texas claim deadline calculator */
  var c = document.getElementById('deadline');
  if (c) {
    var holidays = function (y) {
      var nth = function (m, wd, n) { var dt = new Date(y, m, 1), c2 = 0; while (true) { if (dt.getDay() === wd && ++c2 === n) return dt; dt.setDate(dt.getDate() + 1); } };
      var last = function (m, wd) { var dt = new Date(y, m + 1, 0); while (dt.getDay() !== wd) dt.setDate(dt.getDate() - 1); return dt; };
      var obs = function (dt) { if (dt.getDay() === 6) dt.setDate(dt.getDate() - 1); else if (dt.getDay() === 0) dt.setDate(dt.getDate() + 1); return dt; };
      var tg = nth(10, 4, 4), tg2 = new Date(tg); tg2.setDate(tg.getDate() + 1);
      return [obs(new Date(y, 0, 1)), nth(0, 1, 3), nth(1, 1, 3), last(4, 1), obs(new Date(y, 5, 19)), obs(new Date(y, 6, 4)), nth(8, 1, 1),
        obs(new Date(y, 10, 11)), tg, tg2, obs(new Date(y, 11, 25))].map(function (x) { return x.toDateString(); });
    };
    var isBiz = function (dt) { var w = dt.getDay(); return w !== 0 && w !== 6 && holidays(dt.getFullYear()).indexOf(dt.toDateString()) < 0; };
    var addDays = function (dt, n) { var x = new Date(dt); x.setDate(x.getDate() + n); return x; };
    var addBiz = function (dt, n) { var x = new Date(dt); while (n > 0) { x.setDate(x.getDate() + 1); if (isBiz(x)) n--; } return x; };
    var parse = function (v) { if (!v) return null; var p = v.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); };
    var fmt = function (dt) { return dt.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); };
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var row = function (dt, text, cls) {
      var state = '';
      if (dt) { var days = Math.round((dt - today) / 864e5); state = days < 0 ? ' past' : days <= 7 ? ' soon' : ''; }
      return '<li class="' + (cls || '') + state + '"><strong>' + (dt ? fmt(dt) : '—') + '</strong><span>' + text + (dt && dt < today ? ' <em>(passed)</em>' : '') + '</span></li>';
    };
    bind(c, function () {
      var loss = parse(c.loss.value), notice = parse(c.notice.value), items = parse(c.items.value), accept = parse(c.accept.value);
      var ext = c.cat.checked ? 15 : 0, flood = c.flood.checked, h2 = [];
      if (loss) {
        h2.push(row(loss, 'Date of loss.'));
        if (flood) h2.push(row(addDays(loss, 60), 'NFIP flood: signed proof of loss generally due within 60 days of the loss (unless FEMA extends it).'));
        else h2.push(row(addDays(loss, 365), 'Common policy deadline to report a weather-related claim (one year from loss under many Texas policies—check yours).'));
      }
      if (notice && !flood) {
        h2.push(row(notice, 'Insurer receives notice of the claim.'));
        h2.push(row(addDays(notice, 15 + ext), 'Deadline to acknowledge the claim, begin the investigation and request the information it needs (15 days' + (ext ? ' + 15-day catastrophe extension' : '') + ').'));
        if (items) {
          var dec = addBiz(items, 15); if (ext) dec = addDays(dec, ext);
          h2.push(row(items, 'Insurer receives all items, statements and forms it requested.'));
          h2.push(row(dec, 'Deadline to accept or reject the claim in writing (15 business days' + (ext ? ' + 15 days' : '') + ').'));
          h2.push(row(addDays(dec, 45), 'Latest date if the insurer notified you it needs more time (up to 45 additional days).'));
        } else {
          h2.push('<li><strong>Next</strong><span>Add the date the insurer received the last documents it requested to see the accept/reject deadline.</span></li>');
        }
        if (accept) {
          var pay = addBiz(accept, 5); if (ext) pay = addDays(pay, ext);
          h2.push(row(pay, 'Deadline to pay after notifying you the claim (or part of it) will be paid (5 business days' + (ext ? ' + 15 days' : '') + ').'));
        }
      } else if (!loss) {
        h2.push('<li><strong>—</strong><span>Enter the date of loss and the date the insurer received notice.</span></li>');
      }
      out(c, 'timeline', h2.join(''));
    });
  }

  /* Home inventory builder */
  var inv = document.getElementById('inventory');
  if (inv) {
    var KEY = 'slpa_inventory_v1', ls = store(), items = [];
    try { items = JSON.parse(ls && ls.getItem(KEY) || '[]') || []; } catch (e) { items = []; }
    var save = function () { try { ls && ls.setItem(KEY, JSON.stringify(items)); } catch (e) {} };
    var SUG = {
      'Living room': ['Sofa', 'Coffee table', 'TV', 'TV stand', 'Area rug', 'Lamps', 'Curtains / blinds', 'Bookshelf', 'Wall art', 'Sound bar'],
      'Kitchen': ['Refrigerator', 'Microwave', 'Dishes & glassware', 'Cookware', 'Small appliances', 'Knife set', 'Food & pantry', 'Kitchen table & chairs'],
      'Dining room': ['Dining table', 'Dining chairs', 'China cabinet', 'Chandelier', 'Table linens'],
      'Primary bedroom': ['Bed frame', 'Mattress', 'Dresser', 'Nightstands', 'Bedding', 'Clothing', 'Shoes', 'Jewelry', 'TV'],
      'Bedroom 2': ['Bed & mattress', 'Dresser', 'Desk', 'Clothing', 'Toys', 'Bedding'],
      'Bedroom 3': ['Bed & mattress', 'Dresser', 'Desk', 'Clothing', 'Bedding'],
      'Bathrooms': ['Towels', 'Toiletries', 'Hair dryer / tools', 'Bath mats', 'Shower curtain', 'Medicine & first aid'],
      'Home office': ['Desk', 'Office chair', 'Computer', 'Monitor', 'Printer', 'Files & supplies'],
      'Laundry': ['Washer', 'Dryer', 'Iron & board', 'Laundry supplies'],
      'Garage': ['Power tools', 'Hand tools', 'Lawn mower', 'Bicycles', 'Freezer', 'Shelving', 'Holiday decorations'],
      'Patio / outdoor': ['Patio furniture', 'Grill', 'Outdoor rug', 'Planters', 'Garden tools'],
      'Closets': ['Coats', 'Luggage', 'Linens', 'Vacuum'],
      'Attic / storage': ['Seasonal decor', 'Stored clothing', 'Keepsakes', 'Storage bins']
    };
    var fillSug = function () {
      var list = SUG[inv.room.value] || [];
      document.getElementById('inv-suggest').innerHTML = list.map(function (x) { return '<option value="' + esc(x) + '">'; }).join('');
      return list;
    };
    inv.room.addEventListener('change', fillSug); fillSug();
    var draw2 = function () {
      var tb = $(inv, '[data-list]'), total = 0, rooms = {};
      if (!items.length) tb.innerHTML = '<tr><td colspan="8" class="muted">No items yet.</td></tr>';
      else tb.innerHTML = items.map(function (r, i) {
        var t = r.qty * r.cost; total += t; rooms[r.room] = 1;
        return '<tr><td>' + esc(r.room) + '</td><td>' + esc(r.item) + '</td><td>' + r.qty + '</td><td>' + (r.age === '' ? '' : esc(r.age)) + '</td><td>' + money(r.cost) + '</td><td>' + money(t) + '</td><td>' + esc(r.notes) + '</td><td><button type="button" class="del" data-i="' + i + '" aria-label="Remove">×</button></td></tr>';
      }).join('');
      out(inv, 'count', items.length); out(inv, 'total', money(total)); out(inv, 'rooms', Object.keys(rooms).length);
    };
    $(inv, '[data-add]').addEventListener('click', function () {
      var name = inv.item.value.trim();
      if (!name) { inv.item.focus(); return; }
      items.push({ room: inv.room.value, item: name, qty: Math.max(1, Math.round(num(inv.qty))), age: inv.age.value, cost: num(inv.cost), notes: inv.notes.value.trim() });
      inv.item.value = ''; inv.cost.value = ''; inv.notes.value = ''; inv.age.value = ''; inv.qty.value = 1;
      save(); draw2(); inv.item.focus();
    });
    inv.item.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); $(inv, '[data-add]').click(); } });
    $(inv, '[data-suggest]').addEventListener('click', function () {
      $(inv, '[data-suggest-list]').textContent = 'Common items in the ' + inv.room.value.toLowerCase() + ': ' + fillSug().join(', ') + '.';
    });
    $(inv, '[data-list]').addEventListener('click', function (e) {
      if (e.target.matches('.del')) { items.splice(+e.target.getAttribute('data-i'), 1); save(); draw2(); }
    });
    $(inv, '[data-clear]').addEventListener('click', function () {
      if (items.length && confirm('Remove every item from your inventory?')) { items = []; save(); draw2(); }
    });
    $(inv, '[data-csv]').addEventListener('click', function () {
      var q = function (v) { v = String(v == null ? '' : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
      var lines = [['Room', 'Item', 'Quantity', 'Age (years)', 'Replacement cost each', 'Total', 'Notes'].join(',')];
      items.forEach(function (r) { lines.push([r.room, r.item, r.qty, r.age, r.cost, r.qty * r.cost, r.notes].map(q).join(',')); });
      var blob = new Blob([lines.join('\r\n')], { type: 'text/csv' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'home-inventory.csv';
      document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
    draw2();
  }

  /* Printable / saveable checklists (hurricane preparedness) */
  document.querySelectorAll('[data-checklist]').forEach(function (box) {
    var KEY = 'slpa_check_' + box.getAttribute('data-checklist'), ls = store(), state = {};
    try { state = JSON.parse(ls && ls.getItem(KEY) || '{}') || {}; } catch (e) {}
    var boxes = box.querySelectorAll('input[type="checkbox"]');
    var upd = function () {
      var done = 0; boxes.forEach(function (b) { if (b.checked) done++; });
      var lbl = box.querySelector('[data-progress]'), bar = box.querySelector('[data-progress-bar]');
      if (lbl) lbl.textContent = done + ' of ' + boxes.length + ' done';
      if (bar) bar.style.width = (boxes.length ? done / boxes.length * 100 : 0) + '%';
    };
    boxes.forEach(function (b, i) {
      b.checked = !!state[i];
      b.addEventListener('change', function () { state[i] = b.checked; try { ls && ls.setItem(KEY, JSON.stringify(state)); } catch (e) {} upd(); });
    });
    var reset = box.querySelector('[data-reset]');
    if (reset) reset.addEventListener('click', function () { state = {}; boxes.forEach(function (b) { b.checked = false; }); try { ls && ls.removeItem(KEY); } catch (e) {} upd(); });
    upd();
  });
})();
