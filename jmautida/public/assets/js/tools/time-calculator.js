/* Work hours & logout calculator: logout planner, time zones, countdown, weekly timesheet, decimal converter. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, tabs, tabBar, tabPanel, app } = window.JT;
  const T = window.JMTime;
  const pad = n => String(n).padStart(2, '0');
  const dur = m => `${Math.floor(m / 60)}h ${pad(m % 60)}m`;
  const clock12 = minute => { const h = Math.floor(minute / 60) % 24, m = minute % 60; return `${h % 12 || 12}:${pad(m)} ${h >= 12 ? 'PM' : 'AM'}`; };
  const dayLabel = d => d === 0 ? 'Same day' : d === 1 ? 'Next day' : `${d} days later`;
  const localZone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  const COMMON = ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Phoenix', 'Pacific/Honolulu', 'America/Anchorage', 'America/Toronto', 'Europe/London', 'Europe/Berlin', 'Asia/Manila', 'Asia/Singapore', 'Asia/Kolkata', 'Asia/Dubai', 'Asia/Tokyo', 'Australia/Sydney', 'UTC'];
  let zones = COMMON;
  try { if (Intl.supportedValuesOf) zones = [...new Set([...COMMON, ...Intl.supportedValuesOf('timeZone')])]; } catch { /* older browsers */ }
  const zoneLabel = z => z.replace(/_/g, ' ').replace('America/', 'US · ').replace('Asia/', 'Asia · ').replace('Europe/', 'Europe · ');

  const saved = Object.assign({ start: '19:30', target: '9.3', breaks: [], zone: localZone === 'Asia/Manila' ? 'America/Chicago' : 'Asia/Manila' }, store.get('time:plan', {}));

  app.innerHTML = tabBar('tc', [['logout', 'Logout calculator', 'clock'], ['week', 'Weekly timesheet', 'calendar'], ['decimal', 'Decimal converter', 'hash']]) +
    tabPanel('tc', 'logout', `<div class="time-layout">
      <section class="card time-inputs" style="display:grid;gap:14px;align-content:start">
        <h3 style="margin:0">Plan your shift</h3>
        <div class="form-grid">
          <label class="field">Start time<input class="input" id="start-time" type="time" value="${esc(saved.start)}" required></label>
          <label class="field">Target paid hours<input class="input" id="target-hours" type="number" min="0" max="168" step="any" value="${esc(saved.target)}" inputmode="decimal" required aria-describedby="target-hint"></label>
        </div>
        <p class="muted" id="target-hint" style="margin:-6px 0 0;font-size:13px">Decimal is fine: 9.3 h = 9 h 18 m · 8.25 h = 8 h 15 m</p>
        <div class="chips" id="quick-hours">${[8, 8.5, 9, 9.3, 9.5, 10].map(h => `<button type="button" class="chip" data-hours="${h}">${h} h</button>`).join('')}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:4px"><h3 style="margin:0;font-size:16px">Unpaid breaks</h3>${btn('add-break', 'Add break', { icon: 'plus', ghost: true, size: 'btn-xs' })}</div>
        <div id="breaks" style="display:grid;gap:8px"></div>
        <p class="calc-mode" id="calculation-mode" role="status"></p>
        <label class="field">Show times in<select class="select" id="zone">${zones.map(z => `<option value="${esc(z)}">${esc(zoneLabel(z))}</option>`).join('')}</select></label>
      </section>
      <section class="card time-result">
        <label class="eyebrow" for="logout-time">Logout time — edit to recalculate hours</label>
        <div class="logout-row"><input id="logout-time" class="logout-input" type="time" required aria-describedby="finish-day">
          <select class="select select-sm" id="logout-day" aria-label="Logout day"><option value="auto">Auto</option>${Array.from({ length: 15 }, (_, d) => `<option value="${d}">${dayLabel(d)}</option>`).join('')}</select></div>
        <div class="finish-time" id="finish-time" aria-live="polite"></div>
        <p id="finish-day" class="muted"></p>
        <div class="stat-grid" style="margin:18px 0"><div class="stat"><strong id="paid-duration">—</strong><span>Paid time</span></div><div class="stat"><strong id="break-duration">—</strong><span>Unpaid breaks</span></div><div class="stat"><strong id="elapsed-duration">—</strong><span>Total elapsed</span></div></div>
        <div class="zone-card" id="zone-card"></div>
        <div class="countdown" id="countdown"><div class="countdown-top"><span class="eyebrow" id="cd-label">Live countdown</span><strong id="cd-time">—</strong></div><div class="meter"><i id="cd-bar"></i></div><small class="muted" id="cd-note"></small></div>
        <div class="decimal-explainer"><span class="eyebrow">Decimal hours, made clear</span><h3 id="decimal-equation"></h3><p id="decimal-detail" class="muted"></p></div>
        <div class="btn-row">${btn('copy-plan', 'Copy summary', { icon: 'copy', ghost: true })}${btn('notify', 'Notify me at logout', { icon: 'bell', ghost: true })}</div>
      </section></div>`, true) +
    tabPanel('tc', 'week', `
      <div class="toolbar"><div class="toolbar-group">
        <label class="field" style="grid-auto-flow:column;align-items:center">Overtime after<input class="input input-sm" id="ot-limit" type="number" min="0" max="168" step="any" style="width:80px"> h/week</label>
        <label class="field" style="grid-auto-flow:column;align-items:center">Rate<select class="select select-sm" id="currency" style="width:70px"><option>$</option><option>₱</option><option>€</option><option>£</option><option>A$</option><option>C$</option></select><input class="input input-sm" id="rate" type="number" min="0" step="any" placeholder="0.00" style="width:100px">/h</label>
        <label class="field" style="grid-auto-flow:column;align-items:center">OT ×<input class="input input-sm" id="ot-mult" type="number" min="1" max="5" step="0.25" style="width:80px"></label>
      </div><div class="toolbar-group">${btn('ts-csv', 'CSV', { icon: 'download', ghost: true })}${btn('ts-print', 'Print', { ghost: true })}${btn('ts-clear', 'Clear', { icon: 'trash', ghost: true, cls: 'btn-danger' })}</div></div>
      <div class="table-wrap"><table class="timesheet"><thead><tr><th>Day</th><th>In</th><th>Out</th><th>Break (min)</th><th>Hours</th><th>Decimal</th></tr></thead><tbody id="ts-body"></tbody></table></div>
      <div class="stat-grid" style="margin-top:14px"><div class="stat"><strong id="ts-total">0h 00m</strong><span>Total · <b id="ts-total-dec">0.00</b> h</span></div><div class="stat"><strong id="ts-regular">0h 00m</strong><span>Regular</span></div><div class="stat"><strong id="ts-ot">0h 00m</strong><span>Overtime</span></div><div class="stat"><strong id="ts-pay">—</strong><span>Estimated pay</span></div></div>`) +
    tabPanel('tc', 'decimal', `<div class="grid-2">
      <div class="card" style="display:grid;gap:12px;align-content:start"><h3 style="margin:0">Decimal → hours &amp; minutes</h3><label class="field">Decimal hours<input class="input" id="dec-in" type="number" step="any" min="0" value="7.75" inputmode="decimal"></label><div class="big-result" id="dec-out"></div></div>
      <div class="card" style="display:grid;gap:12px;align-content:start"><h3 style="margin:0">Hours &amp; minutes → decimal</h3><div class="form-grid"><label class="field">Hours<input class="input" id="hm-h" type="number" min="0" step="1" value="7"></label><label class="field">Minutes<input class="input" id="hm-m" type="number" min="0" max="59" step="1" value="45"></label></div><div class="big-result" id="hm-out"></div></div>
    </div>
    <details class="card" style="margin-top:14px"><summary style="cursor:pointer;font-weight:600">Minutes to decimal hours — quick reference</summary><div class="ref-grid">${Array.from({ length: 60 }, (_, i) => `<span><b>${i + 1} min</b>${((i + 1) / 60).toFixed(3).replace(/0+$/, '').replace(/\.$/, '')} h</span>`).join('')}</div></details>`);
  tabs($('#tc'));
  $('#zone').value = zones.includes(saved.zone) ? saved.zone : 'UTC';

  // ---------- Logout calculator ----------
  let sequence = 0, anchor = 'target', current = null, notifyTimer = null;
  const persist = () => store.set('time:plan', { start: $('#start-time').value, target: $('#target-hours').value, breaks: $$('.break-minutes').map(i => i.value), zone: $('#zone').value });

  function shiftWindow(result) {
    const now = new Date(), [h, m] = $('#start-time').value.split(':').map(Number);
    const mk = offset => { const s = new Date(now.getFullYear(), now.getMonth(), now.getDate() + offset, h, m, 0, 0); return { start: s, end: new Date(s.getTime() + result.elapsed * 60000) }; };
    for (const off of [0, -1, -2]) { const w = mk(off); if (now >= w.start && now < w.end) return w; }
    const today = mk(0);
    return now < today.start ? today : mk(1);
  }
  const fmtZone = (date, zone) => new Intl.DateTimeFormat(undefined, { timeZone: zone, weekday: 'short', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }).format(date);

  function update() {
    $('#calculation-mode').innerHTML = anchor === 'target' ? `${icon('lock')} Target hours are fixed — start and break changes move your logout.` : `${icon('lock')} Logout is fixed — start and break changes update paid hours.`;
    try {
      const breaks = $$('.break-minutes').map(i => i.value);
      const result = anchor === 'target' ? T.fromTarget($('#start-time').value, $('#target-hours').value, breaks) : T.fromFinish($('#start-time').value, $('#logout-time').value, $('#logout-day').value, breaks);
      const { paid, unpaid, elapsed, day, minute, hours, rounded } = result;
      current = result;
      if (anchor === 'target') { $('#logout-time').value = `${pad(Math.floor(minute / 60))}:${pad(minute % 60)}`; $('#logout-day').value = String(day); }
      else $('#target-hours').value = String(hours);
      $('#finish-time').textContent = clock12(minute);
      $('#finish-day').textContent = dayLabel(day) + (day ? ' · overnight shift' : '');
      $('#paid-duration').textContent = dur(paid); $('#break-duration').textContent = dur(unpaid); $('#elapsed-duration').textContent = dur(elapsed);
      const frac = Number((hours - Math.floor(hours)).toFixed(6));
      $('#decimal-equation').textContent = `${hours} h = ${dur(paid)}`;
      $('#decimal-detail').textContent = `${frac} × 60 = ${Number((frac * 60).toFixed(2))} minutes. ${rounded ? 'Paid time is rounded to the nearest minute.' : 'The decimal part is a fraction of an hour, not a minute count.'}`;
      const w = shiftWindow(result), zone = $('#zone').value;
      $('#zone-card').innerHTML = `<div><span class="eyebrow">Your time · ${esc(zoneLabel(localZone))}</span><strong>${esc(fmtZone(w.start, localZone))} → ${esc(fmtZone(w.end, localZone))}</strong></div><div><span class="eyebrow">${esc(zoneLabel(zone))}</span><strong>${esc(fmtZone(w.start, zone))} → ${esc(fmtZone(w.end, zone))}</strong></div>`;
      persist(); tick();
      status(anchor === 'target' ? 'Logout updated from your target hours and breaks.' : 'Paid hours updated: elapsed time minus unpaid breaks.');
    } catch (err) {
      current = null;
      ['finish-time', 'paid-duration', 'break-duration', 'elapsed-duration', 'decimal-equation'].forEach(k => { $('#' + k).textContent = '—'; });
      $('#finish-day').textContent = 'Check your inputs.'; $('#decimal-detail').textContent = ''; $('#zone-card').innerHTML = '';
      if (anchor === 'finish') $('#target-hours').value = '';
      status(err.message, 'error'); tick();
    }
  }
  function tick() {
    if (!current) { $('#cd-time').textContent = '—'; $('#cd-note').textContent = ''; $('#cd-bar').style.width = '0'; return; }
    const w = shiftWindow(current), now = Date.now();
    const total = w.end - w.start, left = w.end - now;
    const hms = ms => { const s = Math.max(0, Math.floor(ms / 1000)); return `${Math.floor(s / 3600)}h ${pad(Math.floor(s / 60) % 60)}m ${pad(s % 60)}s`; };
    if (now < w.start) { $('#cd-label').textContent = 'Shift starts in'; $('#cd-time').textContent = hms(w.start - now); $('#cd-bar').style.width = '0'; $('#cd-note').textContent = `Assuming your shift starts ${w.start.toDateString() === new Date().toDateString() ? 'today' : 'tomorrow'} at ${clock12(w.start.getHours() * 60 + w.start.getMinutes())}.`; }
    else { $('#cd-label').textContent = 'Time left until logout'; $('#cd-time').textContent = hms(left); $('#cd-bar').style.width = `${Math.min(100, ((now - w.start) / total) * 100)}%`; $('#cd-note').textContent = `${Math.round(((now - w.start) / total) * 100)}% of your shift done.`; }
  }
  setInterval(tick, 1000);

  $('#target-hours').addEventListener('input', () => { anchor = 'target'; update(); });
  $('#logout-time').addEventListener('input', () => { anchor = 'finish'; update(); });
  $('#logout-day').addEventListener('change', () => { anchor = 'finish'; update(); });
  $('#start-time').addEventListener('input', update);
  $('#zone').addEventListener('change', update);
  $('#quick-hours').addEventListener('click', e => { const b = e.target.closest('[data-hours]'); if (b) { $('#target-hours').value = b.dataset.hours; anchor = 'target'; update(); } });
  function addBreak(value = '30', focus = true) {
    const n = ++sequence, row = document.createElement('div'); row.className = 'break-row';
    row.innerHTML = `<label class="sr-only" for="break-${n}">Break ${n} in minutes</label><input class="input input-sm break-minutes" id="break-${n}" type="number" min="0" max="10080" step="1" value="${esc(value)}" inputmode="numeric"><span class="muted">min</span><div class="chips">${[15, 30, 60].map(v => `<button type="button" class="chip" data-v="${v}">${v}</button>`).join('')}</div><button type="button" class="icon-btn" aria-label="Remove break ${n}">${icon('x')}</button>`;
    const input = row.querySelector('input');
    input.addEventListener('input', update);
    row.querySelectorAll('[data-v]').forEach(b => b.addEventListener('click', () => { input.value = b.dataset.v; update(); }));
    row.querySelector('.icon-btn').addEventListener('click', () => { row.remove(); update(); $('#add-break').focus(); });
    $('#breaks').append(row); if (focus) { update(); input.focus(); }
  }
  $('#add-break').addEventListener('click', () => addBreak());
  saved.breaks.forEach(b => addBreak(b, false));

  $('#copy-plan').addEventListener('click', () => {
    if (!current) return;
    const w = shiftWindow(current), zone = $('#zone').value;
    copy([`Shift plan`, `Start: ${clock12(T.clockMinutes($('#start-time').value))}`, `Logout: ${clock12(current.minute)} (${dayLabel(current.day)})`, `Paid: ${dur(current.paid)} (${current.hours} h) · Breaks: ${dur(current.unpaid)} · Elapsed: ${dur(current.elapsed)}`, `${zoneLabel(zone)}: ${fmtZone(w.start, zone)} → ${fmtZone(w.end, zone)}`].join('\n'), 'Shift summary copied');
  });
  $('#notify').addEventListener('click', async () => {
    if (!current) return;
    const w = shiftWindow(current), ms = w.end - Date.now();
    if (ms <= 0) { toast('That logout time has already passed', 'error'); return; }
    if ('Notification' in window && Notification.permission === 'default') await Notification.requestPermission();
    clearTimeout(notifyTimer);
    notifyTimer = setTimeout(() => {
      const msg = `It’s ${clock12(current.minute)} — time to log out!`;
      if ('Notification' in window && Notification.permission === 'granted') new Notification('Logout time', { body: msg, icon: '/android-chrome-192x192.png' });
      document.title = '⏰ Logout time!'; toast(msg);
    }, Math.min(ms, 2147483000));
    toast(`Reminder set for ${clock12(current.minute)}. Keep this tab open.`);
  });
  update();

  // ---------- Weekly timesheet ----------
  const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const sheet = Object.assign({ rows: DAYS.map(() => ({ in: '', out: '', brk: '' })), limit: 40, rate: '', mult: 1.5, cur: '$' }, store.get('time:week', {}));
  $('#ts-body').innerHTML = DAYS.map((d, i) => `<tr data-i="${i}"><th scope="row">${d}</th><td><input class="input input-sm" type="time" data-k="in" aria-label="${d} in"></td><td><input class="input input-sm" type="time" data-k="out" aria-label="${d} out"></td><td><input class="input input-sm" type="number" min="0" max="1440" step="1" data-k="brk" aria-label="${d} break minutes" placeholder="0"></td><td class="ts-h">—</td><td class="ts-d">—</td></tr>`).join('');
  $$('#ts-body tr').forEach((tr, i) => $$('input', tr).forEach(inp => { inp.value = sheet.rows[i]?.[inp.dataset.k] || ''; }));
  $('#ot-limit').value = sheet.limit; $('#rate').value = sheet.rate; $('#ot-mult').value = sheet.mult; $('#currency').value = sheet.cur;
  function week(silent) {
    const mins = [];
    let error = '';
    $$('#ts-body tr').forEach((tr, i) => {
      const row = Object.fromEntries($$('input', tr).map(inp => [inp.dataset.k, inp.value]));
      sheet.rows[i] = row;
      try { const m = T.shiftMinutes(row.in, row.out, row.brk); mins.push(m); $('.ts-h', tr).textContent = m ? dur(m) : '—'; $('.ts-d', tr).textContent = m ? (m / 60).toFixed(2) : '—'; tr.classList.remove('bad'); }
      catch (err) { mins.push(0); $('.ts-h', tr).textContent = err.message; $('.ts-d', tr).textContent = '—'; tr.classList.add('bad'); error = `${DAYS[i]}: ${err.message}`; }
    });
    Object.assign(sheet, { limit: $('#ot-limit').value, rate: $('#rate').value, mult: $('#ot-mult').value, cur: $('#currency').value });
    const t = T.weekTotals(mins, sheet.limit, sheet.rate, sheet.mult);
    $('#ts-total').textContent = dur(t.total); $('#ts-total-dec').textContent = (t.total / 60).toFixed(2);
    $('#ts-regular').textContent = dur(t.regular); $('#ts-ot').textContent = dur(t.overtime);
    $('#ts-pay').textContent = Number(sheet.rate) > 0 ? `${sheet.cur}${t.pay.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '—';
    store.set('time:week', sheet);
    if (error) status(error, 'error'); else if (silent !== true) status('Timesheet totals updated.');
    return { mins, t };
  }
  $('#tc-panel-week').addEventListener('input', () => week());
  $('#tc-panel-week').addEventListener('change', () => week());
  $('#ts-clear').addEventListener('click', () => { $$('#ts-body input').forEach(i => { i.value = ''; }); week(); toast('Timesheet cleared'); });
  $('#ts-print').addEventListener('click', () => print());
  $('#ts-csv').addEventListener('click', () => {
    const { mins, t } = week();
    const rows = [['Day', 'In', 'Out', 'Break (min)', 'Hours', 'Decimal hours']];
    DAYS.forEach((d, i) => rows.push([d, sheet.rows[i].in, sheet.rows[i].out, sheet.rows[i].brk, mins[i] ? dur(mins[i]) : '', mins[i] ? (mins[i] / 60).toFixed(2) : '']));
    rows.push([], ['Total', '', '', '', dur(t.total), (t.total / 60).toFixed(2)], ['Regular', '', '', '', dur(t.regular), (t.regular / 60).toFixed(2)], ['Overtime', '', '', '', dur(t.overtime), (t.overtime / 60).toFixed(2)]);
    if (Number(sheet.rate) > 0) rows.push(['Estimated pay', '', '', '', '', `${sheet.cur}${t.pay.toFixed(2)}`]);
    download(rows.map(r => r.map(v => `"${String(v ?? '').replace(/"/g, '""')}"`).join(',')).join('\r\n'), 'timesheet.csv', 'text/csv;charset=utf-8');
  });
  week(true);

  // ---------- Decimal converter ----------
  const decOut = () => { try { const r = T.decimalToClock($('#dec-in').value); $('#dec-out').innerHTML = `<strong>${r.h}h ${pad(r.m)}m</strong><span>${r.minutes.toLocaleString()} minutes</span>`; } catch (err) { $('#dec-out').innerHTML = `<span style="color:var(--danger)">${esc(err.message)}</span>`; } };
  const hmOut = () => {
    const h = Number($('#hm-h').value || 0), m = Number($('#hm-m').value || 0);
    if (!Number.isFinite(h) || !Number.isFinite(m) || h < 0 || m < 0) { $('#hm-out').innerHTML = '<span style="color:var(--danger)">Enter positive numbers.</span>'; return; }
    const total = h * 60 + m; $('#hm-out').innerHTML = `<strong>${(total / 60).toFixed(2)} h</strong><span>${Number((total / 60).toFixed(4))} exact · ${total.toLocaleString()} minutes</span>`;
  };
  $('#dec-in').addEventListener('input', decOut); $('#hm-h').addEventListener('input', hmOut); $('#hm-m').addEventListener('input', hmOut);
  decOut(); hmOut();
})();
