/* FreeGradeCalculator — calculator engine. Everything runs locally in the browser. */
(function () {
  'use strict';
  var d = document;
  var $ = function (s, c) { return (c || d).querySelector(s); }, $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var FGC = window.FGC = window.FGC || {};

  /* ---------- grade scale ---------- */
  var SCALE = [['A+', 97, 4.0], ['A', 93, 4.0], ['A-', 90, 3.7], ['B+', 87, 3.3], ['B', 83, 3.0], ['B-', 80, 2.7], ['C+', 77, 2.3], ['C', 73, 2.0], ['C-', 70, 1.7], ['D+', 67, 1.3], ['D', 63, 1.0], ['D-', 60, 0.7], ['F', 0, 0]];
  var LETTER_PCT = { 'A+': 98, 'A': 95, 'A-': 91.5, 'B+': 88, 'B': 85, 'B-': 81.5, 'C+': 78, 'C': 75, 'C-': 71.5, 'D+': 68, 'D': 65, 'D-': 61.5, 'F': 50 };
  var GPA_OF = {}; SCALE.forEach(function (r) { GPA_OF[r[0]] = r[2]; });
  function rangeOf(i) { var hi = i === 0 ? '100' : String(SCALE[i - 1][1] - 1) ; return i === SCALE.length - 1 ? 'Below 60' : SCALE[i][1] + '–' + (i === 0 ? '100' : hi); }
  function scaleRow(p) { p = Math.round(p * 100) / 100; for (var i = 0; i < SCALE.length; i++) if (p >= SCALE[i][1]) return i; return SCALE.length - 1; }
  function letterOf(p) { return SCALE[scaleRow(p)][0]; }
  function gcls(l) { return 'g-' + l.charAt(0).toLowerCase(); }

  /* ---------- parsing / formatting ---------- */
  function num(v) { if (v == null) return NaN; v = String(v).replace(/[,%$\s]/g, ''); return v === '' ? NaN : Number(v); }
  function parseGrade(v) {
    var s = String(v || '').trim().toUpperCase().replace(/\s/g, '');
    if (LETTER_PCT.hasOwnProperty(s)) return LETTER_PCT[s];
    return num(s);
  }
  function fmt(n, dp) { if (!isFinite(n)) return '--'; dp = dp == null ? 2 : dp; return String(Number(n.toFixed(dp))); }
  function pct(n, dp) { return fmt(n, dp == null ? 2 : dp) + '%'; }
  function money(n) { return isFinite(n) ? n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 2 }) : '--'; }
  function list(s) { return String(s || '').split(/[\s,;]+/).map(num).filter(function (x) { return isFinite(x); }); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* ---------- output helpers ---------- */
  function ctx(form) {
    return {
      f: form,
      v: function (n) { var el = form.querySelector('[name="' + n + '"]'); return el ? (el.type === 'checkbox' ? el.checked : el.value) : ''; },
      n: function (n) { return num(this.v(n)); },
      out: function (k, html) { $$('[data-out="' + k + '"]', form).forEach(function (el) { el.innerHTML = html; }); },
      ring: function (k, frac, text) {
        var r = form.querySelector('[data-ring="' + k + '"]'); if (!r) return;
        var c = r.querySelector('.ring-fg'), L = 326.73; frac = Math.max(0, Math.min(1, isFinite(frac) ? frac : 0));
        c.style.strokeDashoffset = (L * (1 - frac)).toFixed(1);
        if (text != null) this.out(k, text);
      },
      pill: function (k, letter) { $$('[data-out="' + k + '"]', form).forEach(function (el) { el.textContent = letter; el.className = 'grade-pill ' + gcls(letter); }); },
      show: function () { var r = form.querySelector('[data-result]'); if (r) r.classList.add('show'); },
      hide: function () { var r = form.querySelector('[data-result]'); if (r && !r.hasAttribute('data-keep')) r.classList.remove('show'); },
      rows: function () { return $$('[data-rows] .row', form).map(function (row) { var o = { el: row }; $$('input,select', row).forEach(function (i) { o[i.name] = i.value; }); return o; }); },
      mode: function () { return form.dataset.mode || ''; }
    };
  }
  function err(c, msg) { c.show(); var m = c.f.querySelector('[data-out="msg"]') || c.f.querySelector('[data-out="note"]'); if (m) m.innerHTML = '<span style="color:var(--bad)">' + msg + '</span>'; }
  function celebrate(form, good) { if (good && form._user && FGC.confetti) FGC.confetti(); }

  /* ---------- dynamic rows ---------- */
  function addRow(form, vals) {
    var tpl = form.querySelector('template[data-row]'), box = form.querySelector('[data-rows]');
    var node = tpl.content.firstElementChild.cloneNode(true);
    if (vals) $$('input,select', node).forEach(function (i, k) { if (vals[k] != null) i.value = vals[k]; });
    box.appendChild(node); numberRows(form);
    return node;
  }
  function numberRows(form) { $$('.row-n', form).forEach(function (el, i) { el.textContent = 'Test ' + (i + 1); }); var add = form.querySelector('[data-add][data-max]'); if (add) add.hidden = $$('[data-rows] .row', form).length >= +add.dataset.max; }
  function seedRows(form, data) {
    var box = form.querySelector('[data-rows]'); if (!box) return;
    box.innerHTML = '';
    (data || JSON.parse(box.dataset.seed || '[]')).forEach(function (v) { addRow(form, v); });
    if (!box.children.length) addRow(form);
  }

  /* ---------- persistence ---------- */
  function key(form) { return 'fgc:' + form.dataset.tool; }
  function save(form) {
    try {
      var st = { fields: {}, rows: null, mode: form.dataset.mode || '' };
      $$('input,select,textarea', form).forEach(function (i) { if (i.name && !i.closest('[data-rows]')) st.fields[i.name] = i.type === 'checkbox' ? i.checked : i.value; });
      if (form.querySelector('[data-rows]')) st.rows = $$('[data-rows] .row', form).map(function (r) { return $$('input,select', r).map(function (i) { return i.value; }); });
      localStorage.setItem(key(form), JSON.stringify(st));
    } catch (e) {}
  }
  function restore(form) {
    var st = null; try { st = JSON.parse(localStorage.getItem(key(form)) || 'null'); } catch (e) {}
    if (st && st.fields) Object.keys(st.fields).forEach(function (n) { var i = form.querySelector('[name="' + n + '"]'); if (i && !i.closest('[data-rows]')) { if (i.type === 'checkbox') i.checked = st.fields[n]; else i.value = st.fields[n]; } });
    seedRows(form, st && st.rows && st.rows.length ? st.rows : null);
    if (st && st.mode) setMode(form, st.mode);
  }

  /* ---------- tabs ---------- */
  function setMode(form, m) {
    form.dataset.mode = m;
    $$('.tabs [data-mode]', form).forEach(function (b) { b.setAttribute('aria-selected', b.dataset.mode === m ? 'true' : 'false'); });
    $$('[data-show]', form).forEach(function (el) { el.hidden = el.dataset.show !== m; });
  }

  /* =====================================================================
     Tool implementations: each gets a ctx and returns nothing
     ===================================================================== */
  var T = {};

  T.weighted = function (c) {
    var rows = c.rows(), tw = 0, sum = 0, bars = '';
    rows.forEach(function (r) {
      var w = num(r.w), s = parseGrade(r.s);
      r.el.querySelector('[name="s"]').classList.toggle('invalid', r.s !== '' && !isFinite(s));
      if (isFinite(w) && w > 0 && isFinite(s)) { tw += w; sum += w * s; bars += '<div class="bar"><span>' + esc((r.name || 'Item').slice(0, 5)) + '</span><div class="bar-track"><div class="bar-fill" data-w="' + Math.min(100, s) + '"></div></div><span>' + fmt(s, 1) + '</span></div>'; }
    });
    if (!tw) return err(c, 'Add at least one category with a weight and a score.');
    var p = sum / tw, L = letterOf(p);
    c.ring('pct', p / 100, fmt(p, 1)); c.out('big', pct(p)); c.pill('letter-pill', L); c.out('letter', L); c.out('gpa', fmt(GPA_OF[L], 1)); c.out('tw', fmt(tw, 2) + '%');
    c.out('bars', bars);
    c.out('note', Math.abs(tw - 100) > 0.001 ? 'Your weights add up to ' + fmt(tw) + '%, so the result is scaled by the total weight entered (' + fmt(sum / 100, 2) + ' ÷ ' + fmt(tw / 100, 2) + ').' : 'Weights add up to 100%. Letter grades in your scores were converted using the standard US scale.');
    c.show(); requestAnimationFrame(function () { $$('.bar-fill', c.f).forEach(function (b) { b.style.width = b.dataset.w + '%'; }); });
    celebrate(c.f, p >= 90);
  };

  T.final = function (c) {
    var cur = parseGrade(c.v('cur')), want = parseGrade(c.v('want')), w = c.n('w') / 100;
    if (!isFinite(cur) || !isFinite(want) || !(w > 0 && w <= 1)) return err(c, 'Enter your current grade, the grade you want, and a final weight between 1 and 100%.');
    var need = function (t) { return (t - cur * (1 - w)) / w; }, n = need(want);
    c.ring('need', n / 100, fmt(n, 1)); c.out('big', pct(n));
    var msg = n > 100 ? 'That’s above 100% — ask your teacher about extra credit, or check the table for a reachable target.' : n <= 0 ? 'Good news: you’ll reach ' + fmt(want) + '% even with a zero on the final.' : n >= 90 ? 'Tough but doable — start reviewing early.' : 'Very achievable. Keep up the steady studying!';
    c.out('msg', msg);
    var rows = ''; [['A', 90], ['B', 80], ['C', 70], ['D', 60]].forEach(function (t) { var x = need(t[1]); rows += '<tr><td>' + t[0] + ' (' + t[1] + '%)</td><td>' + (x <= 0 ? 'Already secured' : x > 100 ? fmt(x, 1) + '% (not possible without extra credit)' : pct(x, 1)) + '</td></tr>'; });
    c.out('table', rows); c.show(); celebrate(c.f, n <= 85 && n > 0);
  };

  T.test = function (c) {
    var t = c.n('total'), n = c.n('n'), right = c.mode() === 'right' ? n : t - n;
    if (!(t > 0) || !isFinite(n) || n < 0 || n > t) return err(c, 'Enter the total and a number between 0 and the total.');
    var p = right / t * 100, L = letterOf(p);
    c.ring('pct', p / 100, fmt(p, 1)); c.out('big', pct(p, 1)); c.pill('letter-pill', L);
    var rows = '', wrong = t - right, max = Math.min(Math.floor(t), 200);
    for (var w = 0; w <= max; w++) { var q = (t - w) / t * 100; rows += '<tr' + (Math.abs(w - wrong) < 1e-9 ? ' class="hl"' : '') + '><td>' + w + '</td><td>' + fmt(t - w) + '</td><td>' + pct(q, 1) + '</td><td>' + letterOf(q) + '</td></tr>'; }
    c.out('chart', rows); c.show(); celebrate(c.f, p >= 90);
  };

  T.points = function (c) {
    var e = 0, p = 0; c.rows().forEach(function (r) { var a = num(r.e), b = num(r.p); if (isFinite(a) && b > 0) { e += a; p += b; } });
    if (!p) return err(c, 'Add points earned and points possible.');
    var x = e / p * 100, L = letterOf(x);
    c.ring('pct', x / 100, fmt(x, 1)); c.out('big', pct(x)); c.pill('letter-pill', L); c.out('e', fmt(e)); c.out('p', fmt(p)); c.out('m', fmt(p - e)); c.show(); celebrate(c.f, x >= 90);
  };

  function scaleTable(hiIdx) { return SCALE.map(function (r, i) { return '<tr' + (i === hiIdx ? ' class="hl"' : '') + '><td>' + r[0] + '</td><td>' + rangeOf(i) + '%</td><td>' + r[2].toFixed(1) + '</td></tr>'; }).join(''); }
  T.letter = function (c) {
    var p = c.n('pct'); if (!isFinite(p)) { c.out('scale', scaleTable(-1)); return; }
    var i = scaleRow(p), L = SCALE[i][0];
    c.pill('letter-pill', L); c.out('big', L); c.out('msg', fmt(p) + '% is a <b>' + L + '</b> (' + rangeOf(i) + '%), worth <b>' + SCALE[i][2].toFixed(1) + '</b> GPA points on a 4.0 scale.'); c.out('scale', scaleTable(i));
  };

  T.semester = function (c) {
    var q1 = c.n('q1'), w1 = c.n('q1w'), q2 = c.n('q2'), w2 = c.n('q2w'), fw = c.n('few');
    if (![q1, w1, q2, w2, fw].every(isFinite) || w1 + w2 + fw <= 0) return err(c, 'Fill in all grades and weights.');
    var sw = w1 + w2 + fw;
    if (c.mode() === 'need') {
      var t = c.n('target'); if (!isFinite(t) || !(fw > 0)) return err(c, 'Enter a target and a final exam weight.');
      var n = (t * sw - q1 * w1 - q2 * w2) / fw;
      c.out('label', 'Score needed on the final'); c.ring('pct', n / 100, fmt(n, 1)); c.out('big', pct(n, 1));
      c.out('msg', n > 100 ? 'Not reachable without extra credit — try a lower target.' : n <= 0 ? 'You’ve already secured it.' : 'Score at least ' + pct(n, 1) + ' on the final for a ' + fmt(t) + '% semester grade.');
    } else {
      var fe = c.n('fe'); if (!isFinite(fe)) return err(c, 'Enter your final exam grade.');
      var g = (q1 * w1 + q2 * w2 + fe * fw) / sw, L = letterOf(g);
      c.out('label', 'Semester grade'); c.ring('pct', g / 100, L); c.out('big', pct(g));
      c.out('msg', 'That’s a <b>' + L + '</b>.' + (Math.abs(sw - 100) > .001 ? ' (Weights total ' + fmt(sw) + '%, so the result is scaled to 100.)' : ''));
      celebrate(c.f, g >= 90);
    }
    c.show();
  };

  T.raise = function (c) {
    var e = c.n('e'), p = c.n('p'), r = c.n('r'), t = c.n('t');
    if (!(p > 0) || !(r > 0) || !isFinite(e) || !isFinite(t)) return err(c, 'Enter points so far, points remaining and your target.');
    var cur = e / p * 100, need = (t / 100 * (p + r) - e) / r * 100, mx = (e + r) / (p + r) * 100, mn = e / (p + r) * 100;
    c.ring('need', need / 100, fmt(need, 1)); c.out('big', pct(need, 1)); c.out('cur', pct(cur, 1)); c.out('max', pct(mx, 1)); c.out('min', pct(mn, 1));
    c.out('msg', need > 100 ? 'Even perfect scores top out at ' + pct(mx, 1) + '. Ask about extra credit or aim for a closer target.' : need <= 0 ? 'You’ll hit ' + fmt(t) + '% even with zeros on everything left.' : 'Average ' + pct(need, 1) + ' or better on the remaining ' + fmt(r) + ' points.');
    c.show();
  };

  T.rubric = function (c) {
    var e = c.n('e'), t = c.n('t'); if (!(t > 0) || !isFinite(e)) return err(c, 'Enter points earned and total points.');
    var p = e / t * 100, L = letterOf(p);
    c.ring('pct', p / 100, fmt(p, 1)); c.out('big', pct(p, 1)); c.pill('letter-pill', L);
    var step = t <= 12 ? 0.5 : 1, rows = '';
    for (var s = t; s >= 0 && rows.length < 60000; s -= step) { var q = s / t * 100; rows += '<tr' + (Math.abs(s - e) < 1e-9 ? ' class="hl"' : '') + '><td>' + fmt(s) + ' / ' + fmt(t) + '</td><td>' + pct(q, 1) + '</td><td>' + letterOf(q) + '</td></tr>'; }
    c.out('chart', rows); c.show();
  };

  T.gpa = function (c) {
    var qp = 0, cr = 0; c.rows().forEach(function (r) { var k = num(r.c); if (k > 0) { qp += GPA_OF[r.g] * k; cr += k; } });
    if (!cr) return err(c, 'Add at least one course with credits.');
    var g = qp / cr; c.ring('gpa', g / 4, fmt(g, 2)); c.out('big', g.toFixed(2)); c.out('cr', fmt(cr)); c.out('qp', fmt(qp, 2));
    var pg = c.n('pg'), pc = c.n('pc'), cum = c.f.querySelector('[data-cum]');
    if (isFinite(pg) && pc > 0) { var ng = (pg * pc + qp) / (pc + cr); c.out('cum', ng.toFixed(2)); cum.hidden = false; } else cum.hidden = true;
    c.out('msg', g >= 3.5 ? 'Excellent — that’s Dean’s List territory at many colleges.' : g >= 3.0 ? 'Solid B average or better.' : g >= 2.0 ? 'In good standing at most schools (2.0+).' : 'Below 2.0 — talk to your advisor about a plan.');
    c.show(); celebrate(c.f, g >= 3.7);
  };

  T.hsgpa = function (c) {
    var uq = 0, wq = 0, cr = 0;
    c.rows().forEach(function (r) { var k = num(r.c); if (k > 0) { var b = GPA_OF[r.g]; uq += b * k; wq += (b > 0 ? b + num(r.t) : 0) * k; cr += k; } });
    if (!cr) return err(c, 'Add at least one class with credits.');
    var u = uq / cr, w = wq / cr;
    c.ring('w', w / 5, fmt(w, 2)); c.out('big', w.toFixed(2)); c.out('uw', u.toFixed(2)); c.out('wt', w.toFixed(2)); c.out('cr', fmt(cr));
    c.out('msg', 'Unweighted ' + u.toFixed(2) + ' on a 4.0 scale. Weighted adds +0.5 for Honors and +1.0 for AP/IB — your school’s exact rules may differ.');
    c.show(); celebrate(c.f, u >= 3.7);
  };

  T.cumgpa = function (c) {
    var g0 = c.n('g0'), c0 = c.n('c0'), qp = 0, cr = 0;
    if (isFinite(g0) && c0 > 0) { qp = g0 * c0; cr = c0; }
    c.rows().forEach(function (r) { var g = num(r.g), k = num(r.c); if (isFinite(g) && k > 0) { qp += g * k; cr += k; } });
    if (!cr) return err(c, 'Enter your current GPA and credits, or at least one term.');
    var g = qp / cr; c.ring('gpa', g / 4, fmt(g, 2)); c.out('big', g.toFixed(3)); c.out('cr', fmt(cr)); c.out('qp', fmt(qp, 2));
    var ch = isFinite(g0) && c0 > 0 ? g - g0 : NaN; c.out('chg', isFinite(ch) ? (ch >= 0 ? '+' : '') + ch.toFixed(3) : '--');
    c.out('msg', isFinite(ch) ? (ch >= 0 ? 'Your GPA goes up by ' : 'Your GPA goes down by ') + Math.abs(ch).toFixed(3) + '.' : '');
    c.show(); celebrate(c.f, ch > 0.05);
  };

  T.gpaconv = function (c) {
    var m = c.mode() || 'pct', i;
    if (m === 'pct') { var p = c.n('pct'); if (!isFinite(p)) return; i = scaleRow(p); c.out('label', '4.0 GPA'); c.out('big', SCALE[i][2].toFixed(1)); c.ring('ring', SCALE[i][2] / 4, SCALE[i][0]); c.out('msg', fmt(p) + '% = <b>' + SCALE[i][0] + '</b> = <b>' + SCALE[i][2].toFixed(1) + '</b> GPA.'); }
    else if (m === 'letter') { var L = c.v('lt'); i = SCALE.findIndex(function (r) { return r[0] === L; }); c.out('label', '4.0 GPA'); c.out('big', SCALE[i][2].toFixed(1)); c.ring('ring', SCALE[i][2] / 4, L); c.out('msg', L + ' usually means ' + rangeOf(i) + '% and is worth <b>' + SCALE[i][2].toFixed(1) + '</b> points.'); }
    else { var g = c.n('gpa'); if (!isFinite(g)) return; g = Math.max(0, Math.min(4, g)); i = SCALE.findIndex(function (r) { return r[2] <= g + 1e-9; }); if (g >= 4) i = 1; c.out('label', 'Closest letter'); c.out('big', SCALE[i][0]); c.ring('ring', g / 4, fmt(g, 2)); c.out('msg', 'A ' + fmt(g, 2) + ' GPA is roughly a <b>' + SCALE[i][0] + '</b> average (about ' + rangeOf(i) + '%). Percent equivalents vary by school.'); }
    c.out('scale', scaleTable(i));
  };

  T.cgpa = function (c) {
    var k = c.n('mult'); if (!(k > 0)) return;
    if ((c.mode() || 'c2p') === 'c2p') { var g = c.n('cg'); if (!isFinite(g)) return; var p = g * k; c.out('label', 'Percentage'); c.out('big', pct(p)); c.ring('ring', p / 100, fmt(p, 1)); c.out('msg', g + ' × ' + k + ' = <b>' + pct(p) + '</b>'); }
    else { var q = c.n('pc'); if (!isFinite(q)) return; var cg = q / k; c.out('label', 'CGPA (out of 10)'); c.out('big', fmt(cg, 2)); c.ring('ring', cg / 10, fmt(cg, 2)); c.out('msg', q + ' ÷ ' + k + ' = <b>' + fmt(cg, 2) + '</b> CGPA'); }
  };

  T.target = function (c) {
    var g = c.n('g'), k = c.n('c'), t = c.n('t'), r = c.n('r');
    if (![g, k, t].every(isFinite) || !(r > 0)) return err(c, 'Fill in all four fields.');
    var need = (t * (k + r) - g * k) / r;
    c.ring('need', need / 4, fmt(need, 2)); c.out('big', need.toFixed(2));
    c.out('msg', need > 4 ? 'Above 4.0, so this target isn’t reachable in ' + fmt(r) + ' credits. Max possible: ' + ((g * k + 4 * r) / (k + r)).toFixed(2) + '.' : need <= 0 ? 'You’ll stay above ' + fmt(t) + ' no matter what.' : 'Average a ' + need.toFixed(2) + ' (≈ ' + SCALE[SCALE.findIndex(function (x) { return x[2] <= need + 1e-9; })][0] + ' average) over your next ' + fmt(r) + ' credits.');
    c.show();
  };

  T.ezgrader = function (c) {
    var n = c.n('n'), st = +c.v('step') || 1;
    if (!(n > 0 && n <= 200)) return err(c, 'Enter 1–200 questions.');
    var rows = '';
    for (var w = 0; w <= n + 1e-9; w += st) { var p = (n - w) / n * 100, L = letterOf(p); rows += '<tr><td>' + fmt(w) + '</td><td>' + fmt(n - w) + '</td><td>' + pct(p, 1) + '</td><td><b>' + L + '</b></td></tr>'; }
    c.out('chart', rows); c.show();
  };

  function stats(a) {
    var n = a.length, s = a.reduce(function (x, y) { return x + y; }, 0), m = s / n, sorted = a.slice().sort(function (x, y) { return x - y; });
    var med = n % 2 ? sorted[(n - 1) / 2] : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
    var f = {}, mx = 0; a.forEach(function (x) { f[x] = (f[x] || 0) + 1; mx = Math.max(mx, f[x]); });
    var modes = mx > 1 ? Object.keys(f).filter(function (k) { return f[k] === mx; }).map(Number) : [];
    var sd = Math.sqrt(a.reduce(function (t, x) { return t + (x - m) * (x - m); }, 0) / n);
    return { n: n, sum: s, mean: m, med: med, modes: modes, sd: sd, min: sorted[0], max: sorted[n - 1] };
  }

  T.curve = function (c) {
    var a = list(c.v('scores')); if (!a.length) return err(c, 'Paste at least one score.');
    var st = stats(a), m = c.v('method'), p1 = c.n('p1'), p2 = c.n('p2'), cap = c.v('cap'), f;
    if (m === 'flat') f = function (x) { return x + (100 - st.max); };
    else if (m === 'add') f = function (x) { return x + (isFinite(p1) ? p1 : 0); };
    else if (m === 'sqrt') f = function (x) { return 10 * Math.sqrt(Math.max(0, x)); };
    else if (m === 'mean') f = function (x) { return x + (p1 - st.mean); };
    else f = function (x) { return st.sd ? p1 + (x - st.mean) / st.sd * (isFinite(p2) ? p2 : 10) : p1; };
    var cur = a.map(function (x) { var y = f(x); if (cap) y = Math.min(100, y); return Math.max(0, y); });
    var nm = cur.reduce(function (x, y) { return x + y; }, 0) / cur.length;
    c.out('m0', fmt(st.mean, 1)); c.out('m1', fmt(nm, 1)); c.out('n', a.length);
    c.out('table', a.map(function (x, i) { return '<tr><td>' + (i + 1) + '</td><td>' + fmt(x, 1) + '</td><td><b>' + fmt(cur[i], 1) + '</b></td><td>' + letterOf(cur[i]) + '</td></tr>'; }).join(''));
    c.show();
  };

  function distBars(a) {
    var bands = [['A', 90, 101], ['B', 80, 90], ['C', 70, 80], ['D', 60, 70], ['F', -1e9, 60]], mx = 0, cnt = bands.map(function (b) { var k = a.filter(function (x) { return x >= b[1] && x < b[2]; }).length; mx = Math.max(mx, k); return k; });
    return bands.map(function (b, i) { return '<div class="bar"><span>' + b[0] + '</span><div class="bar-track"><div class="bar-fill" data-w="' + (mx ? cnt[i] / mx * 100 : 0) + '"></div></div><span>' + cnt[i] + '</span></div>'; }).join('');
  }
  T.classavg = function (c) {
    var a = list(c.v('scores')); if (!a.length) return err(c, 'Paste at least one score.');
    var s = stats(a);
    c.out('mean', fmt(s.mean, 2)); c.out('med', fmt(s.med, 2)); c.out('mode', s.modes.length ? s.modes.slice(0, 3).join(', ') : 'None'); c.out('sd', fmt(s.sd, 2)); c.out('range', fmt(s.max - s.min, 2)); c.out('mm', fmt(s.min) + ' / ' + fmt(s.max)); c.out('n', s.n);
    c.out('dist', distBars(a)); c.show();
    requestAnimationFrame(function () { $$('.bar-fill', c.f).forEach(function (b) { b.style.width = b.dataset.w + '%'; }); });
  };

  T.attend = function (c) {
    var h = c.n('h'), a = c.n('a'), r = c.n('req') / 100;
    if (!(h > 0) || !(a >= 0) || a > h || !(r > 0 && r <= 1)) return err(c, 'Attended can’t be more than classes held.');
    var p = a / h; c.ring('pct', p, fmt(p * 100, 1)); c.out('big', pct(p * 100, 2));
    var msg;
    if (p >= r) { var k = Math.floor(a / r - h + 1e-9); msg = k > 0 ? 'You can miss <b>' + k + '</b> more class' + (k === 1 ? '' : 'es') + ' and stay at or above ' + fmt(r * 100) + '%.' : 'You’re right at the line — don’t miss the next class.'; }
    else if (r >= 1) msg = 'A 100% requirement can’t be reached once a class is missed.';
    else { var x = Math.ceil((r * h - a) / (1 - r) - 1e-9); msg = 'Attend the next <b>' + x + '</b> class' + (x === 1 ? '' : 'es') + ' in a row to reach ' + fmt(r * 100) + '%.'; }
    c.out('msg', msg); c.show();
  };

  T.act = function (c) {
    var en = c.n('en'), ma = c.n('ma'), rd = c.n('rd'), sc = c.n('sc'), leg = c.v('legacy'), ok = function (x) { return x >= 1 && x <= 36; };
    if (![en, ma, rd].every(ok) || (leg && !ok(sc))) return err(c, 'Section scores must be between 1 and 36' + (leg ? ' (Science is required in legacy mode).' : '.'));
    var parts = [en, ma, rd]; if (leg) parts.push(sc);
    var avg = parts.reduce(function (x, y) { return x + y; }, 0) / parts.length, comp = Math.floor(avg + 0.5);
    c.ring('comp', comp / 36, comp); c.out('big', comp); c.out('avg', fmt(avg, 2));
    c.out('stem', ok(sc) ? Math.floor((ma + sc) / 2 + 0.5) : '—');
    c.out('msg', (leg ? 'Average of English, Math, Reading and Science' : 'Enhanced ACT: average of English, Math and Reading') + ', rounded to the nearest whole number.');
    c.show(); celebrate(c.f, comp >= 30);
  };

  T.sat = function (c) {
    var bestRW = 0, bestM = 0, single = 0, ok = function (x) { return x >= 200 && x <= 800; };
    c.rows().forEach(function (r) { var a = num(r.rw), b = num(r.m); if (ok(a)) bestRW = Math.max(bestRW, a); if (ok(b)) bestM = Math.max(bestM, b); if (ok(a) && ok(b)) single = Math.max(single, a + b); });
    if (!bestRW || !bestM) return err(c, 'Enter section scores between 200 and 800.');
    var ss = bestRW + bestM; c.ring('ss', (ss - 400) / 1200, ss); c.out('big', ss); c.out('rw', bestRW); c.out('m', bestM); c.out('single', single || '—');
    c.out('msg', ss > single ? 'Superscoring adds <b>' + (ss - single) + '</b> points over your best single test. Check whether each college superscores.' : 'Your best single sitting already equals your superscore.');
    c.show(); celebrate(c.f, ss >= 1400);
  };

  T.percent = function (c) {
    var x = c.n('x'), y = c.n('y'), m = c.mode() || 'of', r;
    var lx = c.f.querySelector('label[for="f-x"]'), ly = c.f.querySelector('label[for="f-y"]');
    if (m === 'of') { lx.textContent = 'Percent (X)'; ly.textContent = 'Of number (Y)'; r = x / 100 * y; c.out('label', fmt(x) + '% of ' + fmt(y) + ' ='); c.out('big', fmt(r, 4)); c.out('msg', fmt(x) + ' ÷ 100 × ' + fmt(y)); }
    else if (m === 'what') { lx.textContent = 'Part (X)'; ly.textContent = 'Whole (Y)'; r = x / y * 100; c.out('label', fmt(x) + ' is what % of ' + fmt(y) + '?'); c.out('big', pct(r, 4)); c.out('msg', fmt(x) + ' ÷ ' + fmt(y) + ' × 100'); }
    else { lx.textContent = 'From (X)'; ly.textContent = 'To (Y)'; r = (y - x) / Math.abs(x) * 100; c.out('label', 'Change from ' + fmt(x) + ' to ' + fmt(y)); c.out('big', (r > 0 ? '+' : '') + pct(r, 4)); c.out('msg', r >= 0 ? 'Increase' : 'Decrease'); }
    if (!isFinite(r)) c.out('big', '--');
  };

  T.average = function (c) {
    var a = list(c.v('nums')); if (!a.length) { ['mean', 'med', 'mode', 'range', 'sum', 'n'].forEach(function (k) { c.out(k, '--'); }); return; }
    var s = stats(a); c.out('mean', fmt(s.mean, 4)); c.out('med', fmt(s.med, 4)); c.out('mode', s.modes.length ? s.modes.slice(0, 4).join(', ') : 'None'); c.out('range', fmt(s.max - s.min, 4)); c.out('sum', fmt(s.sum, 4)); c.out('n', s.n);
  };

  T.wavg = function (c) {
    var sv = 0, sw = 0, plain = [];
    c.rows().forEach(function (r) { var v = num(r.v), w = num(r.w); if (isFinite(v) && w > 0) { sv += v * w; sw += w; plain.push(v); } });
    if (!sw) return err(c, 'Add values with positive weights.');
    c.out('big', fmt(sv / sw, 4)); c.out('sw', fmt(sw, 4)); c.out('sa', fmt(plain.reduce(function (x, y) { return x + y; }, 0) / plain.length, 4)); c.show();
  };

  /* fractions */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = b; b = a % b; a = t; } return a || 1; }
  function frac(s) {
    s = String(s).trim(); var m;
    if ((m = s.match(/^(-?)(\d+)\s+(\d+)\/(\d+)$/))) { var w = +m[2], n = +m[3], dd = +m[4]; return [(m[1] ? -1 : 1) * (w * dd + n), dd]; }
    if ((m = s.match(/^(-?\d+)\/(-?\d+)$/))) return [+m[1], +m[2]];
    if ((m = s.match(/^-?\d*\.?\d+$/))) { var dec = (s.split('.')[1] || '').length, den = Math.pow(10, dec); return [Math.round(+s * den), den]; }
    return null;
  }
  function simp(f) { var g = gcd(f[0], f[1]); var n = f[0] / g, dd = f[1] / g; if (dd < 0) { n = -n; dd = -dd; } return [n, dd]; }
  function fstr(f) { return f[1] === 1 ? String(f[0]) : f[0] + '/' + f[1]; }
  T.fraction = function (c) {
    var a = frac(c.v('a')), b = frac(c.v('b')), op = c.v('op');
    if (!a || !b || !a[1] || !b[1]) return err(c, 'Use formats like 3/4, 1 1/2 or 0.25.');
    var r, steps = ['Write as fractions: ' + fstr(a) + ' and ' + fstr(b)];
    if (op === '+' || op === '-') { var den = a[1] * b[1] / gcd(a[1], b[1]), x = a[0] * den / a[1], y = b[0] * den / b[1]; steps.push('Common denominator ' + den + ': ' + x + '/' + den + ' ' + op + ' ' + y + '/' + den); r = [op === '+' ? x + y : x - y, den]; }
    else if (op === '*') { r = [a[0] * b[0], a[1] * b[1]]; steps.push('Multiply tops and bottoms: (' + a[0] + '×' + b[0] + ')/(' + a[1] + '×' + b[1] + ')'); }
    else { if (!b[0]) return err(c, 'Can’t divide by zero.'); r = [a[0] * b[1], a[1] * b[0]]; steps.push('Flip the second fraction and multiply: ' + fstr(a) + ' × ' + b[1] + '/' + b[0]); }
    steps.push('Unsimplified: ' + fstr(r)); r = simp(r); steps.push('Simplify (divide by the GCD): ' + fstr(r));
    var whole = Math.trunc(r[0] / r[1]), rem = Math.abs(r[0] % r[1]);
    c.out('big', fstr(r)); c.out('mixed', r[1] === 1 || !whole ? fstr(r) : whole + ' ' + rem + '/' + r[1]); c.out('dec', fmt(r[0] / r[1], 6));
    c.out('steps', steps.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('')); c.show();
  };

  T.loan = function (c) {
    var P = c.n('p'), apr = c.n('r'), y = c.n('y');
    if (!(P > 0) || !(apr >= 0) || !(y > 0)) return err(c, 'Enter amount, rate and term.');
    var r = apr / 1200, n = Math.round(y * 12), M = r ? P * r / (1 - Math.pow(1 + r, -n)) : P / n;
    c.out('big', money(M)); c.out('ti', money(M * n - P)); c.out('tp', money(M * n)); c.out('n', n);
    var bal = P, bars = '', yrs = Math.ceil(n / 12);
    for (var k = 1; k <= n; k++) { bal = bal * (1 + r) - M; if (k % 12 === 0 || k === n) { var yr = Math.ceil(k / 12); bars += '<div class="bar"><span>Yr ' + yr + '</span><div class="bar-track"><div class="bar-fill" data-w="' + Math.max(0, bal / P * 100) + '"></div></div><span style="font-size:.72rem">' + (bal > 0 ? '$' + Math.round(bal / 1000) + 'k' : '$0') + '</span></div>'; } }
    c.out('bars', yrs > 30 ? '' : bars); c.show();
    requestAnimationFrame(function () { $$('.bar-fill', c.f).forEach(function (b) { b.style.width = b.dataset.w + '%'; }); });
  };

  /* ---------- live (non-form) tools ---------- */
  var LIVE = { letter: 1, gpaconv: 1, cgpa: 1, percent: 1, average: 1 };

  function words(root) {
    var ta = $('textarea', root), goal = $('[name="goal"]', root), c = ctx(root);
    var STOP = 'the a an and or but of to in on for with is are was were be been it this that as at by from i you he she we they not have has had do does did so if than then there their its my your our his her them me us'.split(' ');
    function run() {
      var t = ta.value, w = (t.match(/[A-Za-z0-9À-ɏ'’-]+/g) || []);
      var n = w.length;
      c.out('w', n.toLocaleString()); c.out('c', t.length.toLocaleString()); c.out('cn', t.replace(/\s/g, '').length.toLocaleString());
      c.out('s', (t.match(/[^.!?]+[.!?]+(\s|$)/g) || (t.trim() ? [1] : [])).length); c.out('p', t.split(/\n\s*\n/).filter(function (x) { return x.trim(); }).length);
      var rt = n / 238, st = n / 130; c.out('rt', rt < 1 ? Math.round(rt * 60) + ' sec' : fmt(rt, 1) + ' min'); c.out('st', st < 1 ? Math.round(st * 60) + ' sec' : fmt(st, 1) + ' min');
      var f = {}; w.forEach(function (x) { x = x.toLowerCase(); if (x.length > 2 && STOP.indexOf(x) < 0) f[x] = (f[x] || 0) + 1; });
      var top = Object.keys(f).sort(function (a, b) { return f[b] - f[a]; }).slice(0, 8);
      c.out('top', top.length ? top.map(function (k) { return '<span class="chip" style="margin:0 6px 6px 0">' + esc(k) + ' · ' + f[k] + '</span>'; }).join('') : '—');
      var g = num(goal.value), bar = $('[data-goalbar]', root); bar.hidden = !(g > 0); if (g > 0) $('[data-out="goalfill"]', root).style.width = Math.min(100, n / g * 100) + '%';
      try { localStorage.setItem('fgc:words', JSON.stringify({ t: t, g: goal.value })); } catch (e) {}
    }
    try { var s = JSON.parse(localStorage.getItem('fgc:words') || 'null'); if (s) { ta.value = s.t; goal.value = s.g; } } catch (e) {}
    ta.addEventListener('input', run); goal.addEventListener('input', run);
    $('[data-clear]', root).addEventListener('click', function () { ta.value = ''; run(); ta.focus(); });
    run();
  }

  function pomo(root) {
    var c = ctx(root), mode = 'focus', running = false, end = 0, left = 0, timer = null, count = 0, focusDone = 0;
    var today = new Date().toDateString();
    try { var s = JSON.parse(localStorage.getItem('fgc:pomo') || 'null'); if (s && s.day === today) count = s.n; } catch (e) {}
    c.out('done', count);
    function mins(m) { return Math.max(1, num($('[name="' + ({ focus: 'fm', short: 'sm', long: 'lm' })[m] + '"]', root).value) || ({ focus: 25, short: 5, long: 15 })[m]) * 60; }
    function draw() {
      var t = Math.max(0, Math.round(left)), mm = Math.floor(t / 60), ss = t % 60, txt = (mm < 10 ? '0' : '') + mm + ':' + (ss < 10 ? '0' : '') + ss;
      c.out('time', txt); c.out('phase', { focus: 'Focus', short: 'Short break', long: 'Long break' }[mode]);
      c.ring('t', left / mins(mode)); if (running) d.title = txt + ' · ' + ({ focus: 'Focus', short: 'Break', long: 'Break' }[mode]);
    }
    function chime() { try { var A = new (window.AudioContext || window.webkitAudioContext)(); [0, .25, .5].forEach(function (o, i) { var os = A.createOscillator(), g = A.createGain(); os.frequency.value = [660, 880, 990][i]; os.connect(g); g.connect(A.destination); g.gain.setValueAtTime(.0001, A.currentTime + o); g.gain.exponentialRampToValueAtTime(.3, A.currentTime + o + .02); g.gain.exponentialRampToValueAtTime(.0001, A.currentTime + o + .4); os.start(A.currentTime + o); os.stop(A.currentTime + o + .45); }); } catch (e) {} }
    function setM(m, keep) { mode = m; running = false; clearInterval(timer); left = mins(m); $$('.tabs [data-mode]', root).forEach(function (b) { b.setAttribute('aria-selected', b.dataset.mode === m ? 'true' : 'false'); }); btn(); draw(); }
    function btn() { $('[data-start] span', root).textContent = running ? 'Pause' : (left < mins(mode) ? 'Resume' : 'Start'); }
    function tick() {
      left = (end - Date.now()) / 1000;
      if (left <= 0) {
        chime(); if (FGC.toast) FGC.toast(mode === 'focus' ? 'Focus session done — take a break!' : 'Break over — back to it!');
        if (mode === 'focus') { count++; focusDone++; try { localStorage.setItem('fgc:pomo', JSON.stringify({ day: today, n: count })); } catch (e) {} c.out('done', count); var ev = Math.max(1, num($('[name="every"]', root).value) || 4); setM(focusDone % ev === 0 ? 'long' : 'short'); }
        else setM('focus');
        start(); return;
      }
      draw();
    }
    function start() { running = true; end = Date.now() + left * 1000; clearInterval(timer); timer = setInterval(tick, 250); btn(); draw(); }
    $('[data-start]', root).addEventListener('click', function () { if (running) { running = false; clearInterval(timer); left = (end - Date.now()) / 1000; btn(); d.title = 'Pomodoro Study Timer'; } else start(); });
    $('[data-reset-timer]', root).addEventListener('click', function () { setM(mode); d.title = 'Pomodoro Study Timer'; });
    $$('.tabs [data-mode]', root).forEach(function (b) { b.addEventListener('click', function () { setM(b.dataset.mode); }); });
    $$('details input', root).forEach(function (i) { i.addEventListener('change', function () { if (!running) setM(mode); }); });
    setM('focus');
  }

  function countdown(root) {
    var c = ctx(root), nm = $('[name="name"]', root), dt = $('[name="dt"]', root), hrs = $('[name="hrs"]', root);
    try { var s = JSON.parse(localStorage.getItem('fgc:countdown') || 'null'); if (s) { nm.value = s.n; dt.value = s.d; hrs.value = s.h; } } catch (e) {}
    if (!dt.value) { var x = new Date(Date.now() + 21 * 864e5); x.setHours(9, 0, 0, 0); dt.value = new Date(x - x.getTimezoneOffset() * 6e4).toISOString().slice(0, 16); }
    function run() {
      var t = new Date(dt.value).getTime() - Date.now();
      c.out('label', 'Time until ' + esc(nm.value || 'your exam'));
      if (!isFinite(t)) return;
      var past = t <= 0; t = Math.max(0, t);
      c.out('d', Math.floor(t / 864e5)); c.out('h', Math.floor(t / 36e5) % 24); c.out('m', Math.floor(t / 6e4) % 60); c.out('s', Math.floor(t / 1e3) % 60);
      var h = num(hrs.value), days = t / 864e5;
      c.out('msg', past ? 'This date has passed — set your next exam!' : h > 0 ? 'Study about <b>' + fmt(h / Math.max(days, 1), 1) + ' hours per day</b> to fit ' + fmt(h) + ' hours in before the exam.' : '');
    }
    [nm, dt, hrs].forEach(function (i) { i.addEventListener('input', function () { run(); try { localStorage.setItem('fgc:countdown', JSON.stringify({ n: nm.value, d: dt.value, h: hrs.value })); } catch (e) {} }); });
    run(); setInterval(run, 1000);
  }

  /* scientific calculator: safe recursive-descent evaluator */
  function sci(root) {
    var c = ctx(root), expr = '', ans = 0, deg = true, second = false, hist = [];
    var PRETTY = { '*': '×', '/': '÷', 'sqrt(': '√(', 'pi': 'π', 'asin(': 'sin⁻¹(', 'acos(': 'cos⁻¹(', 'atan(': 'tan⁻¹(' };
    function pretty(s) { return esc(s.replace(/\*/g, '×').replace(/\//g, '÷').replace(/sqrt\(/g, '√(').replace(/pi/g, 'π').replace(/a(sin|cos|tan)\(/g, '$1⁻¹(').replace(/E/g, '×10^')); }
    function evaluate(src) {
      var s = src.replace(/E/g, '*10^').replace(/\s+/g, ''), i = 0;
      function peek() { return s[i]; }
      function eat(ch) { if (s[i] === ch) { i++; return true; } return false; }
      function expr() { var v = term(); while (true) { if (eat('+')) v += term(); else if (eat('-')) v -= term(); else return v; } }
      function term() { var v = factor(); while (true) { if (eat('*')) v *= factor(); else if (eat('/')) v /= factor(); else if (/[0-9.(a-z]/.test(peek() || '')) v *= factor(); else return v; } }
      function factor() { var b = unary(); if (eat('^')) return Math.pow(b, factor()); return b; }
      function unary() { if (eat('-')) return -unary(); if (eat('+')) return unary(); return postfix(primary()); }
      function postfix(v) { while (true) { if (eat('!')) { if (v < 0 || v > 170 || v % 1) throw 0; var r = 1; for (var k = 2; k <= v; k++) r *= k; v = r; } else if (eat('%')) v /= 100; else return v; } }
      function primary() {
        var m;
        if (eat('(')) { var v = expr(); eat(')'); return v; }
        if ((m = s.slice(i).match(/^\d*\.?\d+/))) { i += m[0].length; return parseFloat(m[0]); }
        if ((m = s.slice(i).match(/^(asin|acos|atan|sin|cos|tan|log|ln|sqrt|pi|e|ans)/))) {
          var f = m[1]; i += f.length;
          if (f === 'pi') return Math.PI; if (f === 'e') return Math.E; if (f === 'ans') return ans;
          eat('('); var x = expr(); eat(')');
          var toR = deg ? Math.PI / 180 : 1;
          switch (f) {
            case 'sin': return round(Math.sin(x * toR)); case 'cos': return round(Math.cos(x * toR)); case 'tan': return round(Math.tan(x * toR));
            case 'asin': return Math.asin(x) / toR; case 'acos': return Math.acos(x) / toR; case 'atan': return Math.atan(x) / toR;
            case 'log': return Math.log10(x); case 'ln': return Math.log(x); case 'sqrt': return Math.sqrt(x);
          }
        }
        throw 0;
      }
      function round(v) { return Math.abs(v) < 1e-12 ? 0 : v; }
      var out = expr(); if (i < s.length) throw 0; return out;
    }
    function show(o) { c.out('expr', pretty(expr)); c.out('out', o != null ? o : (expr ? pretty(expr) : '0')); }
    function fmtN(v) { if (!isFinite(v)) return 'Error'; var a = Math.abs(v); return (a !== 0 && (a >= 1e12 || a < 1e-9)) ? v.toExponential(8).replace(/\.?0+e/, 'e') : String(+v.toPrecision(12)); }
    function press(k) {
      if (k === 'C') { expr = ''; return show(); }
      if (k === 'DEL') { expr = expr.replace(/(asin\(|acos\(|atan\(|sin\(|cos\(|tan\(|log\(|ln\(|sqrt\(|pi|ans|.)$/, ''); return show(); }
      if (k === '2nd') { second = !second; $$('[data-k="sin("],[data-k="cos("],[data-k="tan("],[data-k="asin("],[data-k="acos("],[data-k="atan("]', root).forEach(function (b) { var base = b.dataset.k.replace(/^a/, ''); b.dataset.k = second ? 'a' + base : base; b.textContent = (second ? base.slice(0, 3) + '⁻¹' : base.slice(0, 3)); }); return; }
      if (k === 'ANS') { expr += 'ans'; return show(); }
      if (k === 'NEG') { expr = expr ? '-(' + expr + ')' : '-'; return show(); }
      if (k === '=') {
        if (!expr) return;
        try { var bal = (expr.match(/\(/g) || []).length - (expr.match(/\)/g) || []).length; var e2 = expr + ')'.repeat(Math.max(0, bal)); var v = evaluate(e2); ans = v; var r = fmtN(v); hist.unshift([pretty(e2), r]); hist = hist.slice(0, 8); c.out('hist', hist.map(function (h) { return '<div data-r="' + h[1] + '"><span>' + h[0] + '</span><b>' + h[1] + '</b></div>'; }).join('')); c.out('expr', pretty(e2) + ' ='); c.out('out', r); expr = r === 'Error' ? '' : r.replace('e+', 'E').replace('e', 'E'); }
        catch (x) { c.out('out', 'Error'); }
        return;
      }
      expr += k; show();
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('[data-k]'); if (b) return press(b.dataset.k);
      var a = e.target.closest('[data-ang]'); if (a) { deg = a.dataset.ang === 'deg'; $$('[data-ang]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === a ? 'true' : 'false'); }); }
      var h = e.target.closest('[data-r]'); if (h) { expr += h.dataset.r; show(); }
    });
    d.addEventListener('keydown', function (e) {
      if (e.target.matches('input,textarea,select') || e.metaKey || e.ctrlKey) return;
      var k = e.key, map = { Enter: '=', '=': '=', Backspace: 'DEL', Escape: 'C', x: '*' };
      if (map[k]) { e.preventDefault(); press(map[k]); } else if (/^[0-9.+\-*/()^%!]$/.test(k)) { e.preventDefault(); press(k); }
    });
    show();
  }

  /* ---------- wire up ---------- */
  $$('form.calc[data-tool]').forEach(function (form) {
    var tool = form.dataset.tool, fn = T[tool]; if (!fn) return;
    var first = $('.tabs [data-mode]', form); if (first) setMode(form, first.dataset.mode);
    restore(form);
    function run(user) { form._user = !!user; try { fn(ctx(form)); } catch (e) { if (window.console) console.error(e); } save(form); }
    form.addEventListener('submit', function (e) {
      e.preventDefault(); run(true);
      var r = form.querySelector('[data-result]'); if (r && r.getBoundingClientRect().top > innerHeight - 120) r.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
    var deb; form.addEventListener('input', function () { clearTimeout(deb); deb = setTimeout(function () { if (LIVE[tool] || form.querySelector('[data-result].show')) run(false); else save(form); }, 220); });
    form.addEventListener('change', function () { if (LIVE[tool]) run(false); });
    form.addEventListener('click', function (e) {
      var add = e.target.closest('[data-add]'); if (add) { var r = addRow(form); var i = r.querySelector('input'); i && i.focus(); save(form); }
      var rm = e.target.closest('[data-rm]'); if (rm) { var row = rm.closest('.row'); if ($$('[data-rows] .row', form).length > 1) { row.classList.add('removing'); setTimeout(function () { row.remove(); numberRows(form); if (form.querySelector('[data-result].show')) run(false); else save(form); }, 230); } else { $$('input', row).forEach(function (x) { x.value = ''; }); } }
      var tab = e.target.closest('.tabs [data-mode]'); if (tab) { setMode(form, tab.dataset.mode); run(false); }
      if (e.target.closest('[data-reset]')) { try { localStorage.removeItem(key(form)); } catch (x) {} form.reset(); seedRows(form); if (first) setMode(form, first.dataset.mode); ctx(form).hide(); if (LIVE[tool]) run(false); FGC.toast && FGC.toast('Calculator reset'); }
    });
    if (tool === 'curve') { var ms = $('[name="method"]', form), sync = function () { $$('[data-m]', form).forEach(function (el) { el.hidden = el.dataset.m.split(' ').indexOf(ms.value) < 0; }); var l = form.querySelector('label[for="f-p1"]'); if (l) l.textContent = ms.value === 'add' ? 'Points to add' : 'Target average'; }; ms.addEventListener('change', sync); sync(); }
    run(false);   // show results for the example values immediately
  });
  $$('[data-tool="words"]').forEach(words);
  $$('[data-tool="pomo"]').forEach(pomo);
  $$('[data-tool="countdown"]').forEach(countdown);
  $$('[data-tool="sci"]').forEach(sci);

  /* home: interactive GPA gauge */
  var gp = $('#gauge-range');
  if (gp) {
    var arc = $('#gauge-arc'), L = arc.getTotalLength();
    arc.style.strokeDasharray = L;
    var upd = function () { var p = +gp.value, i = scaleRow(p), g = SCALE[i][2]; gp.style.setProperty('--fill', ((p - 40) / 60 * 100) + '%'); arc.style.strokeDashoffset = L * (1 - (p - 40) / 60); $('#gauge-letter').textContent = SCALE[i][0]; $('#gauge-pct').textContent = p + '%'; $('#gauge-gpa').textContent = g.toFixed(1) + ' GPA'; };
    gp.addEventListener('input', upd); upd();
  }
  FGC.grade = { letterOf: letterOf, parseGrade: parseGrade, SCALE: SCALE };
})();
