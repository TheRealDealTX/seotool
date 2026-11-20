(function () {
  'use strict';
  var W = window.WCA, $ = W.$, $$ = W.$$, money = W.money, store = W.store, esc = W.esc;
  var LISTINGS = window.WCA_LISTINGS || [];
  var tool = $('[data-tool]'); if (!tool) return;
  var kind = tool.dataset.tool;

  /* ---------- Affordability ---------- */
  if (kind === 'afford') {
    var g = function (k) { return $('[data-i="' + k + '"]', tool); };
    var run = function () {
      var p = g('period').value, inc = +g('income').value || 0, hrs = +g('hours').value || 40;
      $('[data-hours]', tool).hidden = p !== 'hour';
      $('[data-i-label]', tool).textContent = p === 'hour' ? 'Hourly wage ($)' : p === 'month' ? 'Monthly gross income ($)' : 'Annual gross income ($)';
      var people = +g('people').value; $('[data-out-people]', tool).textContent = people;
      var monthly = p === 'year' ? inc / 12 : p === 'month' ? inc : inc * hrs * 52 / 12;
      monthly *= people;
      var debt = +g('debt').value || 0;
      var r30 = monthly * 0.30;
      var r5030 = Math.max(0, monthly * 0.78 * 0.5 * 0.7); // take-home ≈78%, needs 50%, housing ~70% of needs
      var r3x = monthly / 3;
      var dti = Math.max(0, monthly * 0.36 - debt); // 36% total debt-to-income
      var main = Math.max(0, Math.min(r30, dti + 0));
      var set = function (k, v) { $('[data-r="' + k + '"]', tool).textContent = money(v); };
      set('main', main); set('r30', r30); set('r5030', r5030); set('r3x', r3x);
      var mx = Math.max(r30, r5030, r3x, 1);
      ['r30', 'r5030', 'r3x'].forEach(function (k) { $('[data-bar="' + k + '"]', tool).style.width = ({ r30: r30, r5030: r5030, r3x: r3x }[k] / mx * 100) + '%'; });
      $('[data-r="note"]', tool).textContent = 'Based on ' + money(monthly) + '/mo gross household income. ' + (debt ? 'Your debt payments lower the comfortable budget (36% total debt-to-income guideline). ' : '') + 'Many landlords require gross income of about 3× the rent.';
      var m = LISTINGS.filter(function (l) { return l.rmin && l.rmin <= main; }).sort(function (a, b) { return b.rmin - a.rmin; });
      $('[data-matches]', tool).innerHTML = m.length ? m.slice(0, 6).map(function (l) { return W.cardHTML(l); }).join('') :
        '<p class="muted">No listings advertise rents that low right now. Look at <a href="/apartments/income-based/">income-based housing</a> or consider a <a href="/tools/roommate-rent-splitter/">roommate</a>.</p>';
    };
    tool.addEventListener('input', run); run();
  }

  /* ---------- Quiz ---------- */
  if (kind === 'quiz') {
    var Q = [
      { k: 'budget', q: 'What is your monthly rent budget?', o: [['💵', 'Under $900', 900], ['💳', '$900 – $1,200', 1200], ['🏦', '$1,200 – $1,600', 1600], ['💎', '$1,600+', 9999]] },
      { k: 'beds', q: 'How many bedrooms do you need?', o: [['🛋️', 'Studio is fine', 0], ['🛏️', '1 bedroom', 1], ['🛏️🛏️', '2 bedrooms', 2], ['🏠', '3 or more', 3]] },
      { k: 'pets', q: 'Are you bringing a pet?', o: [['🐶', 'Yes, a dog', 'dog'], ['🐱', 'Yes, a cat', 'cat'], ['🚫', 'No pets', 'none']] },
      { k: 'style', q: 'Which sounds most like home?', o: [['🏘️', 'Townhome with my own entry', 'townhome'], ['🏢', 'Classic apartment community', 'apartment'], ['🌿', 'Quiet 55+ / senior living', 'senior'], ['🤷', 'No preference', 'any']] },
      { k: 'perk', q: 'Pick your must-have perk', o: [['🏊', 'Pool', 'pool'], ['🏋️', 'Fitness center', 'fitness'], ['🧺', 'Washer/dryer', 'washer|laundry'], ['🌳', 'Near parks & trails', 'park|trail|arboretum']] },
      { k: 'income', q: 'Interested in income-based housing?', o: [['✅', 'Yes, I may qualify', 'yes'], ['➖', 'No / not sure', 'no']] }
    ];
    var step = 0, ans = {};
    var stage = $('[data-q-stage]', tool), back = $('[data-q-back]', tool), prog = $('[data-q-progress]', tool);
    var show = function () {
      prog.style.width = (step / Q.length * 100) + '%';
      back.hidden = step === 0;
      var q = Q[step];
      stage.innerHTML = '<p class="eyebrow">Question ' + (step + 1) + ' of ' + Q.length + '</p><h2>' + q.q + '</h2><div class="quiz-options">' +
        q.o.map(function (o, i) { return '<button type="button" data-i="' + i + '"><span>' + o[0] + '</span>' + o[1] + '</button>'; }).join('') + '</div>';
    };
    stage.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      ans[Q[step].k] = Q[step].o[+b.dataset.i][2];
      step++;
      if (step >= Q.length) results(); else show();
    });
    back.addEventListener('click', function () { if (step > 0) { step--; show(); } });
    $('[data-q-restart]', tool).addEventListener('click', function () { step = 0; ans = {}; $('[data-q-results]', tool).hidden = true; tool.querySelector('.quiz').hidden = false; show(); });
    var results = function () {
      prog.style.width = '100%';
      var scored = LISTINGS.map(function (l) {
        var s = 50, am = l.amen.join(' ');
        if (l.rmin) s += l.rmin <= ans.budget ? 20 : (l.rmin <= ans.budget * 1.12 ? 5 : -25);
        if (l.bmin != null) s += (ans.beds === 3 ? l.bmax >= 3 : (l.bmin <= ans.beds && l.bmax >= ans.beds)) ? 15 : -15;
        if (ans.pets === 'dog') s += l.dogs ? 12 : (l.dogs === false ? -40 : -5);
        if (ans.pets === 'cat') s += l.cats ? 12 : (l.cats === false ? -40 : -5);
        if (ans.style !== 'any') s += l.type === ans.style ? 12 : (ans.style === 'senior' ? -30 : 0);
        if (ans.style !== 'senior' && l.age) s -= 40;
        if (new RegExp(ans.perk, 'i').test(am)) s += 10;
        if (ans.income === 'yes' && l.income) s += 10;
        if (ans.income === 'no' && l.income) s -= 3;
        if (l.claimed) s += 2;
        return { l: l, s: Math.max(1, Math.min(99, s)) };
      }).sort(function (a, b) { return b.s - a.s; }).slice(0, 3);
      tool.querySelector('.quiz').hidden = true;
      $('[data-q-results]', tool).hidden = false;
      $('[data-q-cards]', tool).innerHTML = scored.map(function (x) { return W.cardHTML(x.l, '<span class="match-score">' + x.s + '% match</span>'); }).join('');
      store.set('wca_quiz', ans);
    };
    show();
  }

  /* ---------- Rent splitter ---------- */
  if (kind === 'split') {
    var rows = $('[data-s-rows]', tool);
    var people = store.get('wca_split', [{ n: 'You', sq: 150, bath: true, park: true }, { n: 'Roommate', sq: 120, bath: false, park: false }]);
    var draw = function () {
      rows.innerHTML = people.map(function (p, i) {
        return '<tr data-r="' + i + '"><td><input value="' + esc(p.n) + '" data-k="n"></td><td><input type="number" min="40" value="' + p.sq + '" data-k="sq"></td>' +
          '<td><input type="checkbox" data-k="bath" ' + (p.bath ? 'checked' : '') + '></td><td><input type="checkbox" data-k="park" ' + (p.park ? 'checked' : '') + '></td>' +
          '<td data-o="rent"></td><td data-o="util"></td><td><strong data-o="total"></strong>' + (people.length > 2 ? ' <button type="button" class="linklike small" data-del="' + i + '">remove</button>' : '') + '</td></tr>';
      }).join('');
      calc();
    };
    var calc = function () {
      var rent = +$('[data-s="rent"]', tool).value || 0, util = +$('[data-s="util"]', tool).value || 0, method = $('[data-s="method"]', tool).value;
      var n = people.length, totSq = people.reduce(function (a, p) { return a + (+p.sq || 0); }, 0) || 1;
      var w = people.map(function (p) {
        if (method === 'equal') return 1;
        if (method === 'size') return (+p.sq || 0) / totSq;
        var x = 0.6 * ((+p.sq || 0) / totSq) + 0.4 / n;
        if (p.bath) x *= 1.10;
        return x;
      });
      var parkCount = method === 'fair' ? people.filter(function (p) { return p.park; }).length : 0;
      var base = rent - parkCount * 25, ws = w.reduce(function (a, b) { return a + b; }, 0);
      $$('tr', rows).forEach(function (tr, i) {
        var share = base * w[i] / ws + (method === 'fair' && people[i].park ? 25 : 0), u = util / n;
        tr.querySelector('[data-o="rent"]').textContent = money(share);
        tr.querySelector('[data-o="util"]').textContent = money(u);
        tr.querySelector('[data-o="total"]').textContent = money(share + u);
      });
      store.set('wca_split', people);
    };
    rows.addEventListener('input', function (e) {
      var tr = e.target.closest('tr'), k = e.target.dataset.k; if (!tr || !k) return;
      people[+tr.dataset.r][k] = e.target.type === 'checkbox' ? e.target.checked : e.target.value; calc();
    });
    rows.addEventListener('click', function (e) { var d = e.target.closest('[data-del]'); if (d) { people.splice(+d.dataset.del, 1); draw(); } });
    $('[data-s-add]', tool).addEventListener('click', function () { if (people.length < 6) { people.push({ n: 'Roommate ' + people.length, sq: 110, bath: false, park: false }); draw(); } });
    tool.addEventListener('input', function (e) { if (e.target.matches('[data-s]')) calc(); });
    tool.addEventListener('change', function (e) { if (e.target.matches('[data-s]')) calc(); });
    draw();
  }

  /* ---------- Moving cost ---------- */
  if (kind === 'moving') {
    var mv = function () {
      var g = function (k) { var el = $('[data-m="' + k + '"]', tool); return el.type === 'checkbox' ? el.checked : (+el.value || 0); };
      var rent = g('rent'), size = g('size'), how = $('[data-m="how"]', tool).value, miles = g('miles');
      var items = [];
      items.push(['First month\'s rent', rent]);
      if (g('dep')) items.push(['Security deposit', rent * g('dep')]);
      items.push(['Application fees', g('app') * g('adults')]);
      var truck = [60, 80, 110, 140][size] + miles * 1.1 + 25;
      var pro = [350, 550, 850, 1250][size] + miles * 4;
      if (how === 'diy') items.push(['Truck rental, mileage & fuel', truck]);
      if (how === 'pro') items.push(['Local movers (est.)', pro]);
      if (how === 'friends') items.push(['Pizza & drinks for helpers', 60]);
      items.push(['Boxes & packing supplies', [40, 70, 110, 150][size]]);
      items.push(['Utility & internet setup fees', 75]);
      items.push(['Cleaning supplies & move-out clean', 40]);
      if (g('pet')) items.push(['Pet deposit / fee', 300]);
      if (g('overlap')) items.push(['Overlapping rent (half month)', rent / 2]);
      items.push(['Cushion for surprises (5%)', 0]);
      var sub = items.reduce(function (a, x) { return a + x[1]; }, 0);
      items[items.length - 1][1] = sub * 0.05;
      $('[data-m-total]', tool).textContent = money(sub * 1.05);
      $('[data-m-list]', tool).innerHTML = items.map(function (x) { return '<li><span>' + x[0] + '</span><b>' + money(x[1]) + '</b></li>'; }).join('');
    };
    tool.addEventListener('input', mv); tool.addEventListener('change', mv); mv();
  }

  /* ---------- Checklist ---------- */
  if (kind === 'checklist') {
    var groups = [
      ['6–8 weeks before', ['Set a moving budget with the moving cost estimator', 'Tour apartments and compare up to 3 side by side', 'Give notice to your current landlord (check your lease for the required notice period)', 'Start decluttering: sell, donate or toss what you won\'t move', 'Book movers or reserve a rental truck']],
      ['4 weeks before', ['Sign the lease and get move-in date & key pickup details in writing', 'Gather boxes, tape, markers and packing paper', 'Buy or update renters insurance for the new address', 'Schedule electric, gas and internet start dates', 'Ask about elevator/parking rules for moving day']],
      ['2 weeks before', ['Submit USPS change of address', 'Update address with your bank, employer and subscriptions', 'Pack non-essentials room by room and label each box', 'Confirm movers/truck and helpers', 'Plan pet and child care for moving day']],
      ['Moving week', ['Pack an essentials box: chargers, meds, toiletries, sheets, tools', 'Defrost and clean the fridge', 'Photograph your old unit after cleaning (deposit evidence)', 'Return old keys and give a forwarding address in writing', 'Confirm move-in time with the new leasing office']],
      ['Move-in day & first week', ['Do a move-in inspection and photograph every room', 'Test smoke detectors, locks, faucets and appliances', 'Report any damage or repairs in writing', 'Update your driver\'s license and vehicle registration with the Ohio BMV', 'Register to vote at your new address', 'Explore your new neighborhood: parks, groceries, the Great Miami River Trail']]
    ];
    var done = store.get('wca_cl', {});
    var list = $('[data-cl-list]', tool), total = 0;
    list.innerHTML = groups.map(function (g, gi) {
      return '<div class="cl-group"><h3>' + g[0] + '</h3>' + g[1].map(function (t, ti) {
        total++; var id = gi + '-' + ti;
        return '<label class="cl-item ' + (done[id] ? 'done' : '') + '"><input type="checkbox" data-id="' + id + '" ' + (done[id] ? 'checked' : '') + '><span>' + t + '</span></label>';
      }).join('') + '</div>';
    }).join('');
    $('[data-cl-total]', tool).textContent = total;
    var paint = function () {
      var n = Object.keys(done).filter(function (k) { return done[k]; }).length;
      $('[data-cl-count]', tool).textContent = n;
      $('[data-cl-progress]', tool).style.width = (n / total * 100) + '%';
    };
    list.addEventListener('change', function (e) {
      var id = e.target.dataset.id; done[id] = e.target.checked; e.target.closest('.cl-item').classList.toggle('done', e.target.checked);
      store.set('wca_cl', done); paint();
    });
    $('[data-cl-reset]', tool).addEventListener('click', function () { done = {}; store.set('wca_cl', done); $$('input', list).forEach(function (x) { x.checked = false; x.closest('.cl-item').classList.remove('done'); }); paint(); });
    paint();
  }

  /* ---------- Room planner ---------- */
  if (kind === 'planner') {
    var FURN = [['Queen bed', 5, 6.7], ['Full bed', 4.5, 6.3], ['Twin bed', 3.3, 6.3], ['Sofa', 7, 3], ['Loveseat', 5, 3], ['Armchair', 3, 3], ['Coffee table', 4, 2], ['TV stand', 5, 1.5], ['Dining table', 5, 3], ['Desk', 4, 2], ['Dresser', 5, 1.7], ['Nightstand', 1.7, 1.5], ['Bookshelf', 3, 1], ['Rug 5×8', 8, 5]];
    var room = $('[data-p-room]', tool), pal = $('[data-p-palette]', tool);
    var st = store.get('wca_room', { w: 12, h: 14, items: [] });
    $('[data-p="w"]', tool).value = st.w; $('[data-p="h"]', tool).value = st.h;
    var scale = 30, sel = null;
    pal.innerHTML = FURN.map(function (f, i) { return '<button type="button" data-add="' + i + '">' + f[0] + '</button>'; }).join('');
    var save = function () { store.set('wca_room', st); };
    var layout = function () {
      var avail = Math.min(room.parentNode.clientWidth - 40, 760);
      scale = Math.max(14, Math.min(40, Math.floor(avail / st.w)));
      room.style.width = st.w * scale + 'px'; room.style.height = st.h * scale + 'px';
      room.style.backgroundSize = scale + 'px ' + scale + 'px';
      draw();
    };
    var overlap = function (a, b) {
      var aw = a.r ? a.d : a.wd, ad = a.r ? a.wd : a.d, bw = b.r ? b.d : b.wd, bd = b.r ? b.wd : b.d;
      return a.x < b.x + bw && a.x + aw > b.x && a.y < b.y + bd && a.y + ad > b.y;
    };
    var draw = function () {
      room.innerHTML = '';
      st.items.forEach(function (it, i) {
        var w = it.r ? it.d : it.wd, d = it.r ? it.wd : it.d;
        var el = document.createElement('div');
        var clash = it.name.indexOf('Rug') < 0 && st.items.some(function (o, j) { return j !== i && o.name.indexOf('Rug') < 0 && overlap(it, o); });
        var out = it.x < 0 || it.y < 0 || it.x + w > st.w + 0.01 || it.y + d > st.h + 0.01;
        el.className = 'furn' + (i === sel ? ' sel' : '') + (clash || out ? ' clash' : '');
        el.style.cssText = 'left:' + it.x * scale + 'px;top:' + it.y * scale + 'px;width:' + w * scale + 'px;height:' + d * scale + 'px;' + (it.name.indexOf('Rug') > -1 ? 'background:rgba(251,139,36,.12);border-style:dashed;z-index:0' : 'z-index:1');
        el.textContent = it.name; el.dataset.i = i; el.title = it.name + ' (' + it.wd + '×' + it.d + ' ft) double-click to rotate';
        room.appendChild(el);
      });
    };
    pal.addEventListener('click', function (e) {
      var b = e.target.closest('[data-add]'); if (!b) return;
      var f = FURN[+b.dataset.add];
      var off = (st.items.length % 6) * 0.75; st.items.push({ name: f[0], wd: f[1], d: f[2], x: 0.5 + off, y: 0.5 + off, r: false }); sel = st.items.length - 1; save(); draw();
    });
    var drag = null;
    room.addEventListener('pointerdown', function (e) {
      var el = e.target.closest('.furn'); if (!el) { sel = null; draw(); return; }
      sel = +el.dataset.i; var it = st.items[sel], r = room.getBoundingClientRect();
      drag = { dx: (e.clientX - r.left) / scale - it.x, dy: (e.clientY - r.top) / scale - it.y };
      room.setPointerCapture(e.pointerId); draw();
    });
    room.addEventListener('pointermove', function (e) {
      if (!drag || sel == null) return;
      var r = room.getBoundingClientRect(), it = st.items[sel];
      it.x = Math.round(((e.clientX - r.left) / scale - drag.dx) * 4) / 4;
      it.y = Math.round(((e.clientY - r.top) / scale - drag.dy) * 4) / 4;
      draw();
    });
    room.addEventListener('pointerup', function () { if (drag) { drag = null; save(); } });
    var lastTap = 0;
    room.addEventListener('dblclick', function (e) { var el = e.target.closest('.furn'); if (el) { var it = st.items[+el.dataset.i]; it.r = !it.r; save(); draw(); } });
    room.addEventListener('touchend', function (e) { var now = Date.now(); if (now - lastTap < 300) { var el = e.target.closest('.furn'); if (el) { var it = st.items[+el.dataset.i]; it.r = !it.r; save(); draw(); } } lastTap = now; });
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Delete' || e.key === 'Backspace') && sel != null && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { st.items.splice(sel, 1); sel = null; save(); draw(); e.preventDefault(); }
    });
    tool.addEventListener('input', function (e) {
      if (e.target.dataset.p) { st[e.target.dataset.p] = Math.max(6, Math.min(40, +e.target.value || 12)); save(); layout(); }
    });
    $('[data-p-clear]', tool).addEventListener('click', function () { st.items = []; sel = null; save(); draw(); });
    $('[data-p-del]', tool).addEventListener('click', function () { if (sel != null) { st.items.splice(sel, 1); sel = null; save(); draw(); } });
    $('[data-p-rot]', tool).addEventListener('click', function () { if (sel != null) { st.items[sel].r = !st.items[sel].r; save(); draw(); } });
    window.addEventListener('resize', layout);
    layout();
  }
})();
