/* The Colony Public Adjuster — free claim tools. Everything runs in the browser; nothing is sent to us. */
'use strict';
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const usd = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  const usd2 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 });
  const num = v => { const n = parseFloat(String(v).replace(/[^0-9.\-]/g, '')); return Number.isFinite(n) ? n : 0; };
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
  };
  function bar(el, parts) {
    const total = parts.reduce((a, p) => a + Math.max(0, p.v), 0) || 1;
    el.innerHTML = parts.map(p => '<i style="width:' + (Math.max(0, p.v) / total * 100).toFixed(2) + '%;background:' + p.c + '" title="' + esc(p.l) + '"></i>').join('');
    const legend = el.nextElementSibling;
    if (legend && legend.classList.contains('bar-legend')) legend.innerHTML = parts.map(p => '<span><b style="background:' + p.c + '"></b>' + esc(p.l) + '</span>').join('');
  }
  function downloadCSV(name, rows) {
    const csv = rows.map(r => r.map(c => '"' + String(c == null ? '' : c).replace(/"/g, '""') + '"').join(',')).join('\r\n');
    const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  function seg(root, onChange) {
    $$('.seg button', root).forEach(b => b.addEventListener('click', () => {
      $$('.seg button', root).forEach(x => x.setAttribute('aria-pressed', String(x === b))); onChange(b.dataset.mode);
    }));
  }

  /* 1. Deductible calculator */
  const ded = $('#tool-deductible');
  if (ded) {
    let mode = 'percent';
    const f = ded.querySelector('form');
    const calc = () => {
      const cov = num(f.elements.coverage.value), pct = num(f.elements.rate.value), flat = num(f.elements.flat.value), est = num(f.elements.estimate.value);
      const d = mode === 'percent' ? cov * pct / 100 : flat;
      $('#ded-out').textContent = usd2.format(d);
      $('#ded-desc').textContent = mode === 'percent'
        ? pct + '% of a ' + usd.format(cov) + ' Coverage A (dwelling) limit.'
        : 'A flat deductible of ' + usd.format(flat) + ' per covered loss.';
      const above = Math.max(0, est - d);
      $('#ded-est').textContent = est ? usd.format(est) : '—';
      $('#ded-above').textContent = est ? usd.format(above) : '—';
      $('#ded-verdict').textContent = !est ? 'Add a repair estimate to compare it with your deductible.'
        : est <= d ? 'This estimate is at or below the deductible, so a covered payment for this loss would likely be $0 before any other policy terms.'
        : 'The estimate exceeds the deductible by ' + usd.format(above) + '. Depreciation, limits and other policy terms can still change the payment.';
      if (est) bar($('#ded-bar'), [{ v: Math.min(d, est), c: '#e2c48f', l: 'Deductible (you pay)' }, { v: above, c: '#ffffff', l: 'Above deductible' }]);
      else bar($('#ded-bar'), [{ v: 1, c: '#e2c48f', l: 'Deductible' }]);
      const tbl = $('#ded-table');
      if (tbl) tbl.innerHTML = [1, 2, 3, 4, 5].map(p => '<tr><td>' + p + '%</td><td class="num">' + usd.format(cov * p / 100) + '</td></tr>').join('');
      $('#rate-out').value = pct + '%';
    };
    seg(ded, m => { mode = m; $$('[data-mode-show]', ded).forEach(el => el.hidden = el.dataset.modeShow !== m); calc(); });
    f.addEventListener('input', calc); f.addEventListener('submit', e => { e.preventDefault(); calc(); }); calc();
  }

  /* 2. Claim payment estimator (RCV / ACV) */
  const pay = $('#tool-payment');
  if (pay) {
    const f = pay.querySelector('form');
    let depMode = 'amount';
    seg(pay, m => { depMode = m; $$('[data-mode-show]', pay).forEach(el => el.hidden = el.dataset.modeShow !== m); calc(); });
    const calc = () => {
      const rcv = num(f.elements.rcv.value), dedv = num(f.elements.deductible.value), prior = num(f.elements.prior.value);
      const dep = depMode === 'amount' ? num(f.elements.dep.value) : rcv * num(f.elements.deppct.value) / 100;
      const nonrec = f.elements.policy.value === 'acv';
      const acv = Math.max(0, rcv - dep);
      const first = Math.max(0, acv - dedv - prior);
      const holdback = nonrec ? 0 : Math.min(dep, Math.max(0, rcv - dedv - prior - first));
      const total = first + holdback;
      $('#pay-first').textContent = usd.format(first);
      $('#pay-rcv').textContent = usd.format(rcv);
      $('#pay-dep').textContent = '−' + usd.format(dep);
      $('#pay-acv').textContent = usd.format(acv);
      $('#pay-ded').textContent = '−' + usd.format(dedv);
      $('#pay-prior').textContent = '−' + usd.format(prior);
      $('#pay-hold').textContent = nonrec ? 'Not applicable (ACV policy)' : usd.format(holdback);
      $('#pay-total').textContent = usd.format(total);
      $('#pay-note').textContent = nonrec
        ? 'With actual cash value coverage, depreciation is generally not paid back after repairs.'
        : 'With replacement cost coverage, withheld depreciation is often recoverable once repairs are completed and documented, subject to your policy terms and deadlines.';
      bar($('#pay-bar'), [
        { v: first, c: '#ffffff', l: 'Initial (ACV) payment' },
        { v: holdback, c: '#e2c48f', l: 'Recoverable depreciation' },
        { v: Math.min(dedv, rcv), c: '#b53a62', l: 'Deductible' },
        { v: nonrec ? dep : 0, c: '#6d5f65', l: 'Non-recoverable depreciation' }
      ]);
      $('#dep-out').value = num(f.elements.deppct.value) + '%';
    };
    f.addEventListener('input', calc); f.addEventListener('submit', e => { e.preventDefault(); calc(); }); calc();
  }

  /* 3. Depreciation calculator (multi-item) */
  const depr = $('#tool-depreciation');
  if (depr) {
    const KEY = 'tcpa-depreciation-v2';
    const f = depr.querySelector('form');
    const tbody = $('#depr-rows');
    let items = store.get(KEY, []);
    f.elements.preset.addEventListener('change', () => {
      const o = f.elements.preset.selectedOptions[0];
      if (o && o.dataset.life) { f.elements.life.value = o.dataset.life; if (!f.elements.itemname.value) f.elements.itemname.value = o.textContent.replace(/\s*\(.*\)$/, ''); }
      preview();
    });
    const calcOne = (cost, age, life, cap) => {
      const pct = life > 0 ? Math.min(cap, age / life * 100) : 0;
      return { pct, dep: cost * pct / 100, acv: cost - cost * pct / 100 };
    };
    const preview = () => {
      const r = calcOne(num(f.elements.cost.value), num(f.elements.age.value), num(f.elements.life.value), num(f.elements.cap.value));
      $('#depr-preview').textContent = usd.format(r.acv) + ' ACV · ' + r.pct.toFixed(1) + '% depreciated';
      $('#cap-out').value = num(f.elements.cap.value) + '%';
    };
    const render = () => {
      let tc = 0, td = 0, ta = 0;
      tbody.innerHTML = items.map((it, i) => {
        const r = calcOne(it.cost, it.age, it.life, it.cap); tc += it.cost; td += r.dep; ta += r.acv;
        return '<tr><td>' + esc(it.item) + '</td><td class="num">' + usd.format(it.cost) + '</td><td class="num">' + it.age + ' / ' + it.life + ' yrs</td><td class="num">' + r.pct.toFixed(1) + '%</td><td class="num">' + usd.format(r.acv) + '</td><td><button type="button" data-del="' + i + '" aria-label="Remove ' + esc(it.item) + '">✕</button></td></tr>';
      }).join('') || '<tr><td colspan="6">Add an item to build your depreciation worksheet.</td></tr>';
      $('#depr-rcv').textContent = usd.format(tc); $('#depr-dep').textContent = '−' + usd.format(td); $('#depr-acv').textContent = usd.format(ta);
      $('#depr-count').textContent = items.length + (items.length === 1 ? ' item' : ' items');
      bar($('#depr-bar'), [{ v: ta, c: '#ffffff', l: 'Actual cash value' }, { v: td, c: '#e2c48f', l: 'Depreciation' }]);
      store.set(KEY, items);
    };
    f.addEventListener('input', preview);
    f.addEventListener('submit', e => {
      e.preventDefault();
      if (!f.elements.itemname.value.trim() || num(f.elements.cost.value) <= 0 || num(f.elements.life.value) <= 0) { f.reportValidity(); return; }
      items.push({ item: f.elements.itemname.value.trim().slice(0, 80), cost: num(f.elements.cost.value), age: num(f.elements.age.value), life: num(f.elements.life.value), cap: num(f.elements.cap.value) });
      f.elements.itemname.value = ''; f.elements.cost.value = ''; f.elements.age.value = ''; f.elements.preset.value = ''; render(); preview(); f.elements.itemname.focus();
    });
    tbody.addEventListener('click', e => { const b = e.target.closest('[data-del]'); if (b) { items.splice(+b.dataset.del, 1); render(); } });
    $('#depr-csv').addEventListener('click', () => downloadCSV('depreciation-worksheet.csv', [['Item', 'Replacement cost', 'Age (yrs)', 'Life expectancy (yrs)', 'Depreciation %', 'Actual cash value']].concat(items.map(it => { const r = calcOne(it.cost, it.age, it.life, it.cap); return [it.item, it.cost, it.age, it.life, r.pct.toFixed(1), r.acv.toFixed(2)]; }))));
    $('#depr-clear').addEventListener('click', () => { if (confirm('Remove every item from this worksheet?')) { items = []; render(); } });
    $('#depr-print').addEventListener('click', () => print());
    render(); preview();
  }

  /* 4. Claim checklist */
  const cl = $('#tool-checklist');
  if (cl) {
    const KEY = 'tcpa-checklist-v2';
    const boxes = $$('input[type=checkbox]', cl);
    const saved = store.get(KEY, {});
    boxes.forEach(b => { b.checked = !!saved[b.id]; });
    const update = () => {
      const state = {}; let done = 0;
      boxes.forEach(b => { state[b.id] = b.checked; if (b.checked) done++; b.closest('.check-item').classList.toggle('done', b.checked); });
      $$('.checklist-stage', cl).forEach(st => { const bs = $$('input', st); st.querySelector('h3 small').textContent = bs.filter(b => b.checked).length + ' / ' + bs.length; });
      const pct = Math.round(done / boxes.length * 100);
      const ring = $('#check-ring'); ring.style.setProperty('--p', pct); ring.dataset.label = pct + '%';
      $('#check-status').textContent = done + ' of ' + boxes.length + ' steps complete';
      $('#check-next').textContent = (boxes.find(b => !b.checked) || { dataset: {} }).dataset.label || 'Every step is checked. Bring this list to your claim review.';
      store.set(KEY, state);
    };
    boxes.forEach(b => b.addEventListener('change', update));
    $('#check-reset').addEventListener('click', () => { boxes.forEach(b => b.checked = false); update(); });
    $('#check-print').addEventListener('click', () => print());
    update();
  }

  /* 5. Home inventory builder */
  const inv = $('#tool-inventory');
  if (inv) {
    const KEY = 'tcpa-inventory-v1';
    const f = inv.querySelector('form'), tbody = $('#inv-rows');
    let rows = store.get(KEY, []);
    const render = () => {
      const byRoom = {}; let total = 0, count = 0;
      tbody.innerHTML = rows.map((r, i) => {
        const line = r.qty * r.value; total += line; count += r.qty; byRoom[r.room] = (byRoom[r.room] || 0) + line;
        return '<tr><td>' + esc(r.room) + '</td><td>' + esc(r.item) + (r.notes ? '<br><small>' + esc(r.notes) + '</small>' : '') + '</td><td class="num">' + r.qty + '</td><td class="num">' + esc(r.year || '—') + '</td><td class="num">' + usd.format(line) + '</td><td><button type="button" data-del="' + i + '" aria-label="Remove ' + esc(r.item) + '">✕</button></td></tr>';
      }).join('') || '<tr><td colspan="6">No items yet. Start with one room.</td></tr>';
      $('#inv-total').textContent = usd.format(total);
      $('#inv-count').textContent = count + (count === 1 ? ' item' : ' items') + ' · ' + Object.keys(byRoom).length + ' rooms';
      $('#inv-rooms').innerHTML = Object.entries(byRoom).sort((a, b) => b[1] - a[1]).map(([k, v]) => '<div><span>' + esc(k) + '</span><strong>' + usd.format(v) + '</strong></div>').join('') || '<div><span>No rooms yet</span><strong>—</strong></div>';
      store.set(KEY, rows);
    };
    f.addEventListener('submit', e => {
      e.preventDefault();
      if (!f.elements.itemname.value.trim()) { f.reportValidity(); return; }
      rows.push({ room: f.elements.room.value.trim().slice(0, 40) || 'Unassigned', item: f.elements.itemname.value.trim().slice(0, 100), qty: Math.max(1, Math.round(num(f.elements.qty.value)) || 1), year: f.elements.year.value.trim().slice(0, 4), value: num(f.elements.value.value), notes: f.elements.notes.value.trim().slice(0, 140) });
      const room = f.elements.room.value; f.reset(); f.elements.room.value = room; f.elements.qty.value = 1; render(); f.elements.itemname.focus();
    });
    tbody.addEventListener('click', e => { const b = e.target.closest('[data-del]'); if (b) { rows.splice(+b.dataset.del, 1); render(); } });
    $('#inv-csv').addEventListener('click', () => downloadCSV('home-inventory.csv', [['Room', 'Item', 'Quantity', 'Purchase year', 'Estimated unit value', 'Line total', 'Notes / serial']].concat(rows.map(r => [r.room, r.item, r.qty, r.year, r.value, (r.qty * r.value).toFixed(2), r.notes]))));
    $('#inv-print').addEventListener('click', () => print());
    $('#inv-clear').addEventListener('click', () => { if (confirm('Delete the entire inventory saved in this browser?')) { rows = []; render(); } });
    render();
  }

  /* 6. Claim communication diary */
  const diary = $('#tool-diary');
  if (diary) {
    const KEY = 'tcpa-diary-v1';
    const f = diary.querySelector('form'), list = $('#diary-rows');
    let rows = store.get(KEY, []);
    f.elements.date.valueAsDate = new Date();
    const render = () => {
      rows.sort((a, b) => b.date.localeCompare(a.date));
      const today = new Date().toISOString().slice(0, 10);
      list.innerHTML = rows.map((r, i) => '<tr><td>' + esc(r.date) + '</td><td>' + esc(r.type) + '</td><td>' + esc(r.who) + '</td><td>' + esc(r.summary) + '</td><td>' + (r.follow ? '<span class="cat"' + (r.follow < today ? ' style="background:#fbeaea;color:#9b1c1c"' : '') + '>' + esc(r.follow) + '</span>' : '—') + '</td><td><button type="button" data-del="' + i + '" aria-label="Remove entry">✕</button></td></tr>').join('') || '<tr><td colspan="6">No entries yet. Log your first call, email or inspection.</td></tr>';
      const open = rows.filter(r => r.follow && r.follow >= today).sort((a, b) => a.follow.localeCompare(b.follow));
      const overdue = rows.filter(r => r.follow && r.follow < today).length;
      $('#diary-count').textContent = rows.length;
      $('#diary-next').textContent = open.length ? open[0].follow + ' — ' + open[0].who : 'None scheduled';
      $('#diary-overdue').textContent = overdue;
      store.set(KEY, rows);
    };
    f.addEventListener('submit', e => {
      e.preventDefault();
      if (!f.elements.summary.value.trim()) { f.reportValidity(); return; }
      rows.push({ date: f.elements.date.value, type: f.elements.type.value, who: f.elements.who.value.trim().slice(0, 80), summary: f.elements.summary.value.trim().slice(0, 600), follow: f.elements.follow.value });
      f.elements.who.value = ''; f.elements.summary.value = ''; f.elements.follow.value = ''; render();
    });
    list.addEventListener('click', e => { const b = e.target.closest('[data-del]'); if (b) { rows.splice(+b.dataset.del, 1); render(); } });
    $('#diary-csv').addEventListener('click', () => downloadCSV('claim-diary.csv', [['Date', 'Type', 'Spoke with / from', 'Summary', 'Follow-up date']].concat(rows.map(r => [r.date, r.type, r.who, r.summary, r.follow]))));
    $('#diary-print').addEventListener('click', () => print());
    $('#diary-clear').addEventListener('click', () => { if (confirm('Delete every diary entry saved in this browser?')) { rows = []; render(); } });
    render();
  }

  /* 7. Texas prompt-payment timeline (Tex. Ins. Code ch. 542, subchapter B) */
  const tl = $('#tool-timeline');
  if (tl) {
    const f = tl.querySelector('form');
    const nth = (y, m, wd, n) => { const d = new Date(y, m, 1); const off = (wd - d.getDay() + 7) % 7; return new Date(y, m, 1 + off + (n - 1) * 7); };
    const last = (y, m, wd) => { const d = new Date(y, m + 1, 0); return new Date(y, m, d.getDate() - ((d.getDay() - wd + 7) % 7)); };
    const obs = d => { const w = d.getDay(); return w === 6 ? new Date(d.getFullYear(), d.getMonth(), d.getDate() - 1) : w === 0 ? new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1) : d; };
    const hcache = {};
    const holidays = y => hcache[y] || (hcache[y] = new Set([
      obs(new Date(y, 0, 1)), nth(y, 0, 1, 3), nth(y, 1, 1, 3), last(y, 4, 1), obs(new Date(y, 5, 19)), obs(new Date(y, 6, 4)),
      nth(y, 8, 1, 1), nth(y, 9, 1, 2), obs(new Date(y, 10, 11)), nth(y, 10, 4, 4), obs(new Date(y, 11, 25))
    ].map(d => d.toDateString())));
    const isBiz = d => d.getDay() !== 0 && d.getDay() !== 6 && !holidays(d.getFullYear()).has(d.toDateString());
    const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
    const addBiz = (d, n) => { let x = new Date(d); let c = 0; while (c < n) { x = addDays(x, 1); if (isBiz(x)) c++; } return x; };
    const parse = v => { if (!v) return null; const [y, m, d] = v.split('-').map(Number); return new Date(y, m - 1, d); };
    const show = d => d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
    f.elements.notice.valueAsDate = f.elements.notice.valueAsDate || new Date();
    const calc = () => {
      const notice = parse(f.elements.notice.value), items = parse(f.elements.items.value), accepted = parse(f.elements.accepted.value);
      const cat = f.elements.cat.checked, surplus = f.elements.surplus.checked, extra = cat ? 15 : 0;
      const out = [];
      if (notice) {
        const ack = surplus ? addBiz(notice, 30 + extra) : addDays(notice, 15 + extra);
        out.push({ d: ack, t: 'Acknowledge, start investigating and request items', p: (surplus ? '30 business days' : '15 days') + ' after the insurer receives notice of the claim' + (cat ? ', plus 15 days for a declared weather catastrophe' : '') + ' (§542.055).' });
      }
      const base = items || null;
      if (base) {
        const dec = addBiz(base, 15 + extra);
        out.push({ d: dec, t: 'Written decision to accept or reject the claim', p: '15 business days after the insurer receives every item it requested' + (cat ? ' plus 15 days' : '') + ' (§542.056).' });
        out.push({ d: addDays(base, 45 + extra), t: 'Outer limit if the insurer says it needs more time', p: 'If the insurer notifies you that it needs more time and explains why, it may take up to 45 days' + (cat ? ' plus 15 days' : '') + ' from receiving the items (§542.056(d)).' });
      }
      if (accepted) {
        out.push({ d: addBiz(accepted, 5), t: 'Payment due after acceptance', p: '5 business days after notice that the claim (or part of it) will be paid (§542.057).' });
      }
      $('#tl-list').innerHTML = out.length ? out.sort((a, b) => a.d - b.d).map(o => '<li><span class="date">' + show(o.d) + '</span><div><strong>' + o.t + '</strong><p>' + o.p + '</p></div></li>').join('')
        : '<li><span class="date">—</span><div><strong>Enter a date to begin</strong><p>Start with the date you reported the claim.</p></div></li>';
    };
    f.addEventListener('input', calc); f.addEventListener('change', calc); f.addEventListener('submit', e => { e.preventDefault(); calc(); }); calc();
    const ics = $('#tl-print'); ics && ics.addEventListener('click', () => print());
  }
})();
