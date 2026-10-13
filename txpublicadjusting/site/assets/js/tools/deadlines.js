/* Texas Chapter 542 / TWIA claim deadline calculator */
(function () {
  'use strict';
  var root = document.querySelector('[data-dl]');
  if (!root) return;
  var ins = 'std';
  var DAY = 86400000;

  function parse(v) { if (!v) return null; var p = v.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function fmt(d) { return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); }
  function ymd(d) { return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); }

  // Texas state holidays (non-optional), with weekend observance.
  function nthDow(y, m, dow, n) { var d = new Date(y, m, 1); var off = (dow - d.getDay() + 7) % 7; return new Date(y, m, 1 + off + (n - 1) * 7); }
  function lastDow(y, m, dow) { var d = new Date(y, m + 1, 0); var off = (d.getDay() - dow + 7) % 7; return new Date(y, m + 1, -off); }
  var holCache = {};
  function holidays(y) {
    if (holCache[y]) return holCache[y];
    var thx = nthDow(y, 10, 4, 4);
    var list = [new Date(y, 0, 1), nthDow(y, 0, 1, 3), nthDow(y, 1, 1, 3), lastDow(y, 4, 1), new Date(y, 5, 19), new Date(y, 6, 4),
      nthDow(y, 8, 1, 1), new Date(y, 10, 11), thx, addDays(thx, 1), new Date(y, 11, 24), new Date(y, 11, 25), new Date(y, 11, 26)];
    var set = {};
    list.forEach(function (d) { set[ymd(d)] = 1; });
    return (holCache[y] = set);
  }
  function isBiz(d) { var w = d.getDay(); return w !== 0 && w !== 6 && !holidays(d.getFullYear())[ymd(d)]; }
  function addBiz(d, n) { var x = new Date(d); while (n > 0) { x = addDays(x, 1); if (isBiz(x)) n--; } return x; }

  root.querySelector('[data-seg="ins"]').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    this.querySelectorAll('button').forEach(function (x) { x.classList.toggle('is-on', x === b); });
    ins = b.getAttribute('data-v'); run();
  });

  var items = [];
  function v(k) { var el = root.querySelector('[data-in="' + k + '"]'); return el.type === 'checkbox' ? el.checked : el.value; }

  function run() {
    root.querySelector('[data-more]').hidden = !v('more');
    var loss = parse(v('loss')), notice = parse(v('notice')), all = parse(v('items')), acc = parse(v('accept')), more = v('more') ? parse(v('moredate')) : null;
    var cat = v('cat') ? 15 : 0, arson = v('arson');
    items = [];
    var today = new Date(); today.setHours(0, 0, 0, 0);

    if (ins === 'twia') {
      if (loss) items.push({ d: addDays(new Date(loss.getFullYear() + 1, loss.getMonth(), loss.getDate()), 0), t: 'Last day to file the claim with TWIA', law: '§2210.573(a); the commissioner may extend up to 180 days for good cause (§2210.205(b))', deadline: true });
      if (notice) {
        items.push({ d: addDays(notice, 30), t: 'TWIA\'s deadline to request any additional information it needs', law: '§2210.573(b)' });
        var base = all && all > notice ? all : notice;
        items.push({ d: addDays(base, 60), t: 'TWIA must notify you in writing whether it accepts or denies the claim (60 days after the claim, or after receiving the information it requested)', law: '§2210.573(d), unless extended by the commissioner', deadline: true });
      }
    } else {
      if (loss) items.push({ d: new Date(loss.getFullYear() + 1, loss.getMonth(), loss.getDate()), t: 'Common one-year reporting window for wind and hail on many private policies. Verify in your policy', law: 'Policy condition, not a statute', soft: true });
      if (notice) {
        var ack = ins === 'sl' ? addBiz(notice, 30) : addDays(notice, 15);
        items.push({ d: addDays(ack, cat), t: 'Insurer must acknowledge the claim, begin investigating and request the items it needs', law: ins === 'sl' ? '§542.055 (30 business days, surplus lines)' : '§542.055 (15 days)', deadline: true });
      }
      if (all) {
        var dec = arson ? addDays(all, 30) : addBiz(all, 15);
        items.push({ d: addDays(dec, cat), t: 'Insurer must accept or reject the claim in writing' + (arson ? ' (arson suspected)' : '') + ', or explain why it needs more time', law: arson ? '§542.056(b) (30 days)' : '§542.056(a) (15 business days)', deadline: true });
        if (more) items.push({ d: addDays(addDays(more, 45), cat), t: 'Extended decision deadline after the insurer\'s "need more time" notice', law: '§542.056(d) (45 days)', deadline: true });
        items.push({ d: addDays(all, 60), t: 'If an owed claim is still unpaid 60 days after the insurer has everything it needs, statutory interest can apply', law: '§542.058, §542.060', soft: true });
      }
      if (acc) {
        var pay = ins === 'sl' ? addBiz(acc, 20) : addBiz(acc, 5);
        items.push({ d: addDays(pay, cat), t: 'Insurer must pay the accepted claim (or the accepted part)', law: ins === 'sl' ? '§542.057(c) (20 business days)' : '§542.057(a) (5 business days)', deadline: true });
      }
    }
    items.sort(function (a, b) { return a.d - b.d; });

    var list = root.querySelector('[data-out="list"]');
    root.querySelector('[data-out="today"]').textContent = 'Today: ' + today.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    if (!items.length) { list.innerHTML = '<li><p class="vt__what">Enter the date you reported the claim to see the timeline.</p></li>'; return; }
    var nextSet = false;
    list.innerHTML = items.map(function (it) {
      var days = Math.round((it.d - today) / DAY), cls = '', badge = '';
      if (days < 0) { cls = it.deadline && !it.soft ? 'is-late' : 'is-past'; badge = '<span class="badge ' + (it.soft ? 'badge--warn' : 'badge--bad') + '">' + (-days) + ' days ago</span>'; }
      else if (!nextSet) { cls = 'is-next'; nextSet = true; badge = '<span class="badge badge--ok">' + (days === 0 ? 'today' : 'in ' + days + ' days') + '</span>'; }
      else badge = '<span class="badge badge--info">in ' + days + ' days</span>';
      return '<li class="' + cls + '"><div class="vt__date">' + fmt(it.d) + badge + '</div><div class="vt__what">' + it.t + '</div><div class="vt__law">' + it.law + (cat && it.deadline && ins !== 'twia' ? ' + 15 days (catastrophe)' : '') + '</div></li>';
    }).join('');
  }

  function summary() {
    return items.map(function (it) { return fmt(it.d) + ': ' + it.t + ' [' + it.law + ']'; }).join('\n');
  }

  root.addEventListener('input', run);
  root.addEventListener('change', run);
  root.addEventListener('click', function (e) {
    var a = e.target.closest('[data-act]'); if (!a) return;
    var act = a.getAttribute('data-act');
    if (act === 'print') window.print();
    if (act === 'copy' && items.length) {
      (navigator.clipboard ? navigator.clipboard.writeText(summary()) : Promise.reject()).then(function () { a.textContent = 'Copied'; setTimeout(function () { a.textContent = 'Copy summary'; }, 1600); }, function () { window.prompt('Copy:', summary()); });
    }
    if (act === 'ics' && items.length) {
      var esc = function (s) { return s.replace(/[\\,;]/g, function (c) { return '\\' + c; }); };
      var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//TX Public Adjusting//Claim deadlines//EN'];
      items.forEach(function (it, i) {
        lines.push('BEGIN:VEVENT', 'UID:txpa-' + ymd(it.d) + '-' + i + '@txpublicadjusting.com', 'DTSTAMP:' + ymd(new Date()) + 'T000000Z',
          'DTSTART;VALUE=DATE:' + ymd(it.d), 'DTEND;VALUE=DATE:' + ymd(addDays(it.d, 1)), 'SUMMARY:' + esc('Claim deadline: ' + it.t.slice(0, 70)),
          'DESCRIPTION:' + esc(it.t + ' (' + it.law + '). Calculated at txpublicadjusting.com'), 'END:VEVENT');
      });
      lines.push('END:VCALENDAR');
      var blob = new Blob([lines.join('\r\n')], { type: 'text/calendar' });
      var link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = 'claim-deadlines.ics';
      document.body.appendChild(link); link.click(); link.remove();
    }
  });
  run();
})();
