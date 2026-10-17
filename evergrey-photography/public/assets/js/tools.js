/* Evergrey Photography — planning tools: sun maths, golden hour calculator,
   wedding timeline planner, elopement location finder, pricing estimator. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var TZ = 'America/Vancouver';

  /* ---------- sun position (after NOAA / suncalc formulas) ---------- */
  var PI = Math.PI, sin = Math.sin, cos = Math.cos, tan = Math.tan, asin = Math.asin, acos = Math.acos, atan2 = Math.atan2;
  var rad = PI / 180, dayMs = 864e5, J1970 = 2440588, J2000 = 2451545, J0 = 0.0009, e = rad * 23.4397;
  function toDays(d) { return d.valueOf() / dayMs - 0.5 + J1970 - J2000; }
  function fromJulian(j) { return new Date((j + 0.5 - J1970) * dayMs); }
  function declination(l) { return asin(sin(e) * sin(l)); }
  function rightAscension(l) { return atan2(sin(l) * cos(e), cos(l)); }
  function meanAnomaly(d) { return rad * (357.5291 + 0.98560028 * d); }
  function eclLong(M) { var C = rad * (1.9148 * sin(M) + 0.02 * sin(2 * M) + 0.0003 * sin(3 * M)); return M + C + rad * 102.9372 + PI; }
  function transit(ds, M, L) { return J2000 + ds + 0.0053 * sin(M) - 0.0069 * sin(2 * L); }

  function sunTimes(date, lat, lng) {
    var lw = rad * -lng, phi = rad * lat, d = toDays(date);
    var n = Math.round(d - J0 - lw / (2 * PI));
    var ds = J0 + lw / (2 * PI) + n;
    var M = meanAnomaly(ds), L = eclLong(M), dec = declination(L), Jnoon = transit(ds, M, L);
    function pair(h) {
      var x = (sin(h * rad) - sin(phi) * sin(dec)) / (cos(phi) * cos(dec));
      if (x < -1 || x > 1) return [null, null];
      var w = acos(x), Jset = transit(J0 + (w + lw) / (2 * PI) + n, M, L);
      return [fromJulian(Jnoon - (Jset - Jnoon)), fromJulian(Jset)];
    }
    var rs = pair(-0.833), g = pair(6), b = pair(-4), c = pair(-6);
    return {
      noon: fromJulian(Jnoon), sunrise: rs[0], sunset: rs[1],
      goldenMorningEnd: g[0], goldenEveningStart: g[1],
      blueMorningEnd: b[0], blueEveningEnd: c[1], blueMorningStart: c[0], blueEveningStart: b[1]
    };
  }
  function altitude(date, lat, lng) {
    var lw = rad * -lng, phi = rad * lat, d = toDays(date);
    var M = meanAnomaly(d), L = eclLong(M), dec = declination(L), ra = rightAscension(L);
    var H = rad * (280.16 + 360.9856235 * d) - lw - ra;
    return asin(sin(phi) * sin(dec) + cos(phi) * cos(dec) * cos(H)) / rad;
  }
  var fmtT = new Intl.DateTimeFormat('en-CA', { timeZone: TZ, hour: 'numeric', minute: '2-digit' });
  function fmt(d) { return d ? fmtT.format(d) : '—'; }
  function localMinutes(d) {
    var p = new Intl.DateTimeFormat('en-GB', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(d);
    var h = 0, m = 0; p.forEach(function (x) { if (x.type === 'hour') h = +x.value; if (x.type === 'minute') m = +x.value; });
    return h * 60 + m;
  }
  // midday (local) instant for a YYYY-MM-DD string; 20:00 UTC is noon PST / 1 pm PDT
  function middayFor(s) { var a = s.split('-'); return new Date(Date.UTC(+a[0], +a[1] - 1, +a[2], 20, 0, 0)); }
  // Date for a local clock time on a given day (handles PDT/PST)
  function atLocal(s, minutes) {
    var base = middayFor(s), off = localMinutes(base) - 12 * 60; // local offset vs noon reference
    var noonUtc = new Date(base.getTime() - off * 60000);
    return new Date(noonUtc.getTime() + (minutes - 720) * 60000);
  }
  function todayStr() {
    var p = new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
    return p.slice(0, 10);
  }
  function addDays(s, n) { var d = middayFor(s); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  function prettyDate(s) { return new Intl.DateTimeFormat('en-CA', { timeZone: 'UTC', weekday: 'short', month: 'short', day: 'numeric' }).format(middayFor(s)); }
  function hm(min) { min = ((Math.round(min) % 1440) + 1440) % 1440; var h = Math.floor(min / 60), m = min % 60, ap = h >= 12 ? 'p.m.' : 'a.m.'; h = h % 12 || 12; return h + ':' + (m < 10 ? '0' : '') + m + ' ' + ap; }
  function dur(ms) { var m = Math.round(ms / 60000); return Math.floor(m / 60) + ' h ' + (m % 60) + ' min'; }

  var LOCS = window.EG_LOCATIONS || [];
  function locByKey(k) { for (var i = 0; i < LOCS.length; i++) if (LOCS[i].key === k) return LOCS[i]; return LOCS[0]; }
  function fillLocSelect(sel, chosen) {
    if (!sel) return;
    sel.innerHTML = LOCS.map(function (l) { return '<option value="' + l.key + '"' + (l.key === chosen ? ' selected' : '') + '>' + l.name + '</option>'; }).join('');
  }

  /* ---------- golden hour calculator ---------- */
  var gh = $('#golden-hour-tool');
  if (gh) {
    var q = new URLSearchParams(location.search);
    var selLoc = $('#gh-loc', gh), inDate = $('#gh-date', gh);
    fillLocSelect(selLoc, q.get('loc') || 'victoria');
    inDate.value = /^\d{4}-\d{2}-\d{2}$/.test(q.get('date') || '') ? q.get('date') : todayStr();
    var render = function () {
      var loc = locByKey(selLoc.value), ds = inDate.value || todayStr();
      var t = sunTimes(middayFor(ds), loc.lat, loc.lng);
      var set = function (id, v) { var el = $('#' + id, gh); if (el) el.textContent = v; };
      set('gh-sunrise', fmt(t.sunrise));
      set('gh-sunset', fmt(t.sunset));
      set('gh-morning', fmt(t.sunrise) + ' – ' + fmt(t.goldenMorningEnd));
      set('gh-evening', fmt(t.goldenEveningStart) + ' – ' + fmt(t.sunset));
      set('gh-blue', fmt(t.blueEveningStart) + ' – ' + fmt(t.blueEveningEnd));
      set('gh-length', t.sunrise && t.sunset ? dur(t.sunset - t.sunrise) : '—');
      var best = t.goldenEveningStart && t.sunset ? hm(localMinutes(t.sunset) - 45) + ' – ' + fmt(t.sunset) : '—';
      set('gh-best', best);
      set('gh-place', loc.name + ' · ' + prettyDate(ds));

      // day bar
      var seg = function (d) { return d ? (localMinutes(d) / 1440 * 100).toFixed(2) : null; };
      var night = '#1f2a33', blue = '#4c6a8c', gold = '#e0a85a', day = '#f3e7cf';
      var a = [seg(t.blueMorningStart), seg(t.blueMorningEnd), seg(t.goldenMorningEnd), seg(t.goldenEveningStart), seg(t.blueEveningStart), seg(t.blueEveningEnd)];
      var bar = $('.daybar', gh);
      if (bar && a.every(function (x) { return x !== null; })) {
        bar.style.background = 'linear-gradient(90deg,' + night + ' 0%,' + night + ' ' + a[0] + '%,' + blue + ' ' + a[0] + '%,' + blue + ' ' + a[1] + '%,' + gold + ' ' + a[1] + '%,' + gold + ' ' + a[2] + '%,' + day + ' ' + a[2] + '%,' + day + ' ' + a[3] + '%,' + gold + ' ' + a[3] + '%,' + gold + ' ' + a[4] + '%,' + blue + ' ' + a[4] + '%,' + blue + ' ' + a[5] + '%,' + night + ' ' + a[5] + '%,' + night + ' 100%)';
      }
      // elevation arc
      var svg = $('.sun-arc svg', gh);
      if (svg) {
        var W = 1000, H = 200, maxAlt = 70, pts = [], start = atLocal(ds, 0).getTime();
        for (var m = 0; m <= 1440; m += 10) {
          var alt = altitude(new Date(start + m * 60000), loc.lat, loc.lng);
          var x = m / 1440 * W, y = H * .78 - (alt / maxAlt) * H * .74;
          pts.push(x.toFixed(1) + ',' + y.toFixed(1));
        }
        var horizon = (H * .78).toFixed(1);
        var gs = t.goldenEveningStart ? localMinutes(t.goldenEveningStart) / 1440 * W : 0;
        var ss = t.sunset ? localMinutes(t.sunset) / 1440 * W : 0;
        var sy = H * .78 - (6 / maxAlt) * H * .74;
        svg.innerHTML =
          '<defs><linearGradient id="skyg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#c4a275" stop-opacity=".35"/><stop offset="1" stop-color="#c4a275" stop-opacity="0"/></linearGradient></defs>' +
          '<rect x="' + gs.toFixed(1) + '" y="0" width="' + Math.max(0, ss - gs).toFixed(1) + '" height="' + horizon + '" fill="url(#skyg)"/>' +
          '<line x1="0" x2="' + W + '" y1="' + horizon + '" y2="' + horizon + '" stroke="currentColor" stroke-opacity=".25" stroke-dasharray="4 6"/>' +
          '<polyline points="' + pts.join(' ') + '" fill="none" stroke="#2d3b33" stroke-width="2.5" stroke-linecap="round" class="arc-line"/>' +
          '<circle cx="' + gs.toFixed(1) + '" cy="' + sy.toFixed(1) + '" r="9" fill="#e0a85a"><animate attributeName="r" values="7;11;7" dur="2.4s" repeatCount="indefinite"/></circle>' +
          '<text x="' + Math.min(W - 150, gs + 14).toFixed(1) + '" y="' + (sy - 14).toFixed(1) + '" font-size="22" fill="#5e6e60" font-family="Manrope, sans-serif">Golden hour</text>';
        var line = svg.querySelector('.arc-line');
        if (line && line.getTotalLength) {
          var L = line.getTotalLength(); line.style.strokeDasharray = L; line.style.strokeDashoffset = L;
          line.getBoundingClientRect(); line.style.transition = 'stroke-dashoffset 1.6s cubic-bezier(.2,.7,.1,1)'; line.style.strokeDashoffset = 0;
        }
      }
      // week table
      var tb = $('#gh-week tbody', gh);
      if (tb) {
        var rows = '';
        for (var i = 0; i < 7; i++) {
          var dd = addDays(ds, i), tt = sunTimes(middayFor(dd), loc.lat, loc.lng);
          rows += '<tr><td>' + prettyDate(dd) + '</td><td>' + fmt(tt.sunrise) + '</td><td>' + fmt(tt.goldenEveningStart) + '</td><td>' + fmt(tt.sunset) + '</td><td>' + fmt(tt.blueEveningEnd) + '</td></tr>';
        }
        tb.innerHTML = rows;
      }
      var link = $('#gh-inquire', gh);
      if (link) link.href = '/contact?date=' + encodeURIComponent(ds) + '&location=' + encodeURIComponent(loc.name);
      if (history.replaceState) history.replaceState(null, '', '?loc=' + loc.key + '&date=' + ds);
    };
    selLoc.addEventListener('change', render);
    inDate.addEventListener('change', render);
    $$('[data-jump]', gh).forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-jump'), y = (inDate.value || todayStr()).slice(0, 4);
        inDate.value = v === 'today' ? todayStr() : y + '-' + v; render();
      });
    });
    render();
  }

  /* ---------- wedding timeline planner ---------- */
  var tp = $('#timeline-tool');
  if (tp) {
    var f = $('form', tp);
    fillLocSelect($('[name="loc"]', f), 'victoria');
    $('[name="date"]', f).value = addDays(todayStr(), 240);
    var out = $('#tl-out', tp);
    var build = function () {
      var v = function (n) { return f.elements[n]; };
      var ds = v('date').value || todayStr();
      var loc = locByKey(v('loc').value);
      var cs = v('ceremony').value.split(':'); var C = (+cs[0]) * 60 + (+cs[1] || 0);
      var firstLook = v('firstlook').checked, prep = v('prep').checked;
      var cLen = +v('clen').value, groups = +v('groups').value, travel = +v('travel').value;
      var cocktail = +v('cocktail').value, party = +v('party').value;
      var t = sunTimes(middayFor(ds), loc.lat, loc.lng);
      var sunset = t.sunset ? localMinutes(t.sunset) : 20 * 60;
      var ev = [];
      var add = function (time, title, note, cls) { ev.push({ t: time, title: title, note: note || '', cls: cls || '' }); };
      var start;
      if (firstLook) {
        start = prep ? C - 210 : C - 150;
        if (prep) { add(C - 210, 'Photographer arrives · details', 'Rings, invitation suite, florals, shoes — flat lays in window light.'); add(C - 180, 'Getting ready', 'Final touches, letters, the dress or suit going on.'); }
        add(C - 150, 'First look', 'A private moment before the day speeds up.', 'gold');
        add(C - 135, 'Couple portraits', 'Unhurried portraits while everyone is fresh.');
        add(C - 95, 'Wedding party photos', 'Group shots plus a few candid ones.');
        add(C - 60, 'Tuck away & rest', 'Water, snacks, touch-ups. Guests start arriving.');
      } else {
        start = prep ? C - 150 : C - 45;
        if (prep) { add(C - 150, 'Photographer arrives · details', 'Rings, stationery, florals and the space itself.'); add(C - 120, 'Getting ready', 'Hair and makeup finishing, getting dressed, quiet moments.'); add(C - 60, 'Portraits of each partner', 'Solo portraits and immediate family before the ceremony.'); }
        add(C - 45, 'Guests arrive · ceremony details', 'Venue, seating, and arrival moments.');
      }
      add(C, 'Ceremony', cLen + ' minutes — we stay quiet and out of your guests\' sightlines.', 'gold');
      var x = C + cLen;
      add(x, 'Hugs, confetti & receiving line', 'Plan 10–15 minutes before anyone gets herded anywhere.'); x += 15;
      var fam = Math.max(10, groups * 3 + 5);
      add(x, 'Family formals', groups + ' groupings — about ' + fam + ' minutes with a shot list.'); x += fam;
      if (!firstLook) { add(x, 'Wedding party photos', 'About 20 minutes.'); x += 20; add(x, 'Couple portraits', 'About 30 minutes while guests enjoy cocktails.'); x += 30; }
      else { add(x, 'Quick couple portraits', 'Ceremony attire touch-ups and a few frames at the ceremony site.'); x += 15; }
      add(C + cLen, 'Cocktail hour begins', cocktail + ' minutes for guests.', '');
      var R = Math.max(x + travel, C + cLen + cocktail + travel);
      if (travel > 0) add(Math.max(x, C + cLen + cocktail), 'Travel to reception', travel + ' minutes.');
      add(R, 'Grand entrance', 'Reception begins.');
      add(R + 10, 'Dinner service', 'We take a break to eat while you do.');
      add(R + 70, 'Speeches & toasts', 'Reactions from both sides of the room.');
      add(R + 95, 'Cake cutting', '');
      add(R + 105, 'First dance & parent dances', '');
      var golden = sunset - 40;
      add(golden, 'Golden hour portraits', '15–20 minutes of glowing light. Sunset is ' + hm(sunset) + ' on ' + prettyDate(ds) + ' at ' + loc.name + '.', 'gold');
      var end = R + 125 + party * 60;
      if (party > 0) add(R + 125, 'Open dance floor', party + ' hour' + (party > 1 ? 's' : '') + ' of party coverage.');
      add(end, 'Photography wraps', 'Optional sparkler or faux exit before we leave.');
      ev.sort(function (a, b) { return a.t - b.t; });
      var hours = (end - start) / 60;
      out.innerHTML = '<ol class="tl">' + ev.map(function (e, i) {
        return '<li class="' + e.cls + '" style="animation-delay:' + (i * 40) + 'ms"><time>' + hm(e.t) + '</time><div><b>' + e.title + '</b>' + (e.note ? '<small>' + e.note + '</small>' : '') + '</div></li>';
      }).join('') + '</ol>';
      var sum = $('#tl-summary', tp);
      var goldWarn = (golden < R) ? ' Sunset falls before the reception starts, so we\'ll fold golden-hour portraits into the cocktail-hour session.' : (golden > end ? ' Sunset is after coverage ends — consider adding an hour or shifting the ceremony later.' : '');
      sum.innerHTML = 'Suggested coverage: <strong>' + (Math.round(hours * 2) / 2) + ' hours</strong> (' + hm(start) + ' – ' + hm(end) + '). Sunset: <strong>' + hm(sunset) + '</strong>.' + goldWarn;
      var pr = $('#tl-pricing', tp); if (pr) pr.href = '/pricing?hours=' + Math.min(12, Math.max(4, Math.ceil(hours)));
    };
    f.addEventListener('input', build); f.addEventListener('change', build);
    f.addEventListener('submit', function (e) { e.preventDefault(); build(); });
    var pb = $('#tl-print', tp); if (pb) pb.addEventListener('click', function () { window.print(); });
    build();
  }

  /* ---------- elopement location finder ---------- */
  var lf = $('#finder-tool');
  if (lf) {
    var spots = window.EG_SPOTS || [];
    var answers = {}, qs = $$('.quiz-q', lf), step = 0;
    var bar = $('.quiz-progress span', lf);
    var showQ = function (i) {
      qs.forEach(function (q, k) { q.classList.toggle('active', k === i); });
      bar.style.width = (i / qs.length * 100) + '%';
      $('#finder-results', lf).hidden = true;
      var back = $('#quiz-back', lf); back.hidden = i === 0;
    };
    var results = function () {
      bar.style.width = '100%';
      qs.forEach(function (q) { q.classList.remove('active'); });
      var scored = spots.map(function (s) {
        var sc = 0;
        if (s.scene.indexOf(answers.scene) > -1) sc += 40; else if (answers.scene === 'any') sc += 25;
        var wl = { easy: 0, moderate: 1, hike: 2 };
        var diff = wl[s.walk] - wl[answers.walk]; sc += diff <= 0 ? 22 - (Math.abs(diff) * 4) : (diff === 1 ? 6 : 0);
        var pl = { low: 0, med: 1, high: 2 };
        sc += 20 - Math.abs(pl[s.privacy] - pl[answers.privacy]) * 9;
        var dr = s.drive <= 25 ? 0 : (s.drive <= 70 ? 1 : 2), want = { near: 0, hour: 1, trip: 2 }[answers.drive];
        sc += dr <= want ? 18 : (dr - want === 1 ? 6 : 0);
        return { s: s, score: Math.max(0, Math.min(99, Math.round(sc))) };
      }).sort(function (a, b) { return b.score - a.score; }).slice(0, 4);
      var box = $('#finder-results', lf);
      $('#finder-list', lf).innerHTML = scored.map(function (r, i) {
        var s = r.s;
        return '<div class="loc-result" style="animation-delay:' + (i * 90) + 'ms"><div class="score">' + r.score + '%</div><div><h3>' + s.name + '</h3>' +
          '<div class="tags"><span>' + s.scene.join(' · ') + '</span><span>' + ({ easy: 'Easy access', moderate: 'Short trail', hike: 'Real hike' })[s.walk] + '</span><span>' + ({ low: 'Busy spot', med: 'Some privacy', high: 'Secluded' })[s.privacy] + '</span><span>~' + (s.drive < 60 ? s.drive + ' min' : (Math.round(s.drive / 6) / 10) + ' h') + ' from Victoria</span></div>' +
          '<p>' + s.blurb + '</p><a class="text-link" href="/tools/golden-hour-calculator?loc=' + s.loc + '">Check golden hour here</a></div></div>';
      }).join('');
      box.hidden = false;
      $('#quiz-back', lf).hidden = false;
    };
    $$('.quiz-opt', lf).forEach(function (b) {
      b.addEventListener('click', function () {
        answers[b.getAttribute('data-q')] = b.getAttribute('data-v');
        step++; if (step < qs.length) showQ(step); else results();
      });
    });
    $('#quiz-back', lf).addEventListener('click', function () { step = Math.max(0, step - 1); showQ(step); });
    $('#quiz-restart', lf).addEventListener('click', function () { answers = {}; step = 0; showQ(0); });
    showQ(0);
  }

  /* ---------- pricing estimator ---------- */
  var pe = $('#estimator');
  if (pe) {
    var P = window.EG_PRICING;
    var hours = $('#est-hours', pe), hoursVal = $('#est-hours-val', pe), mode = 'wedding';
    var qh = new URLSearchParams(location.search).get('hours');
    if (qh && +qh >= 4 && +qh <= 12) hours.value = qh;
    var money = function (n) { return '$' + Math.round(n).toLocaleString('en-CA'); };
    var shown = 0;
    var animateTo = function (el, target) {
      var from = shown, t0 = null; shown = target;
      var tick = function (t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 600); var v = from + (target - from) * (1 - Math.pow(1 - k, 3)); el.textContent = money(v); if (k < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick);
    };
    var calc = function () {
      var lines = [], sub = 0;
      if (mode === 'wedding') {
        var h = +hours.value; hoursVal.textContent = h + ' h';
        var base = P.weddingBase + P.weddingHour * h; lines.push([h + '-hour wedding coverage', base]); sub += base;
      } else {
        var opt = $('[name="elope"]:checked', pe); var ep = P.elopement[opt.value];
        lines.push([ep.label, ep.price]); sub += ep.price;
      }
      $$('[data-addon]', pe).forEach(function (c) {
        if (!c.checked || c.closest('[hidden]')) return;
        var a = P.addons[c.getAttribute('data-addon')];
        var amt = a.perHour ? a.price * (mode === 'wedding' ? +hours.value : 3) : a.price;
        lines.push([a.label, amt]); sub += amt;
      });
      var tz = $('#est-travel', pe), tr = P.travel[tz.value];
      if (tr.price) { lines.push(['Travel: ' + tr.label, tr.price]); sub += tr.price; }
      var gst = sub * 0.05;
      $('#est-lines', pe).innerHTML = lines.map(function (l) { return '<li><span>' + l[0] + '</span><span>' + money(l[1]) + '</span></li>'; }).join('') +
        '<li><span>GST (5%)</span><span>' + money(gst) + '</span></li>';
      animateTo($('#est-total', pe), sub + gst);
      var cta = $('#est-cta', pe);
      if (cta) cta.href = '/contact?type=' + mode + '&estimate=' + encodeURIComponent(money(sub + gst) + ' incl. GST — ' + lines.map(function (l) { return l[0]; }).join(', '));
    };
    $$('.seg button', pe).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.seg button', pe).forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-pressed', 'false'); });
        b.classList.add('active'); b.setAttribute('aria-pressed', 'true'); mode = b.getAttribute('data-mode');
        $('#est-wedding', pe).hidden = mode !== 'wedding'; $('#est-elope', pe).hidden = mode !== 'elopement';
        $$('[data-only]', pe).forEach(function (el) { el.hidden = el.getAttribute('data-only') !== mode; });
        calc();
      });
    });
    pe.addEventListener('input', calc); pe.addEventListener('change', calc);
    calc();
  }
})();
