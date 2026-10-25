/* Engagement Rate Calculator */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('er-form')) return;

  var BENCH = { // engagement by followers, % : nano, micro, mid, macro, mega
    instagram: [4, 2.5, 1.6, 1.2, 1.0],
    tiktok: [9, 6.5, 5, 4.5, 4],
    youtube: [4, 2.5, 1.8, 1.5, 1.2],
    facebook: [1.5, 0.8, 0.5, 0.4, 0.3],
    pinterest: [1.5, 1, 0.7, 0.5, 0.4]
  };
  var TIERS = ['Nano (under 10K)', 'Micro (10K-100K)', 'Mid-tier (100K-500K)', 'Macro (500K-1M)', 'Mega (1M+)'];
  var rows = $('er-rows'), MAX = 10, ARC = 408.4;

  function tierIdx(n) { return n < 10000 ? 0 : n < 100000 ? 1 : n < 500000 ? 2 : n < 1000000 ? 3 : 4; }

  function addRow(vals) {
    if (rows.children.length >= MAX) return;
    vals = vals || ['', '', '', ''];
    var r = document.createElement('div'), i = rows.children.length + 1;
    r.className = 'post-row';
    var labels = ['Likes', 'Comments', 'Shares and saves', 'Reach or views'];
    r.innerHTML = '<span class="idx">' + i + '</span>' + labels.map(function (l, k) {
      return '<input type="number" min="0" inputmode="numeric" aria-label="Post ' + i + ' ' + l + '" value="' + vals[k] + '">';
    }).join('') + '<button type="button" class="rm" aria-label="Remove post ' + i + '">&times;</button>';
    rows.appendChild(r);
    r.querySelector('.rm').addEventListener('click', function () { r.remove(); renumber(); update(); });
    r.querySelectorAll('input').forEach(function (inp) { inp.addEventListener('input', update); });
    $('er-add').disabled = rows.children.length >= MAX;
  }
  function renumber() {
    Array.prototype.forEach.call(rows.children, function (r, i) { r.querySelector('.idx').textContent = i + 1; });
    $('er-add').disabled = rows.children.length >= MAX;
  }

  function update() {
    var f = parseFloat($('er-followers').value) || 0, plat = $('er-platform').value;
    var n = 0, sumRate = 0, totInt = 0, totReach = 0, intForReach = 0;
    Array.prototype.forEach.call(rows.children, function (r) {
      var v = Array.prototype.map.call(r.querySelectorAll('input'), function (x) { return parseFloat(x.value) || 0; });
      var inter = v[0] + v[1] + v[2];
      if (inter === 0 && v[3] === 0) return;
      n++; totInt += inter;
      if (f > 0) sumRate += inter / f * 100;
      if (v[3] > 0) { totReach += v[3]; intForReach += inter; }
    });
    var rate = n ? sumRate / n : 0;
    var t = tierIdx(f), bench = BENCH[plat][t], ratio = bench ? rate / bench : 0;
    $('er-n').textContent = n;
    $('er-rate').textContent = rate.toFixed(2) + '%';
    $('er-reach').textContent = totReach > 0 ? (intForReach / totReach * 100).toFixed(2) + '%' : 'Add reach';
    $('er-bench').textContent = bench.toFixed(1) + '%';
    $('er-bench-t').textContent = 'Avg ' + bench + '%';
    $('er-avg').textContent = n ? Math.round(totInt / n).toLocaleString() : '0';
    $('er-tier').textContent = TIERS[t];

    var pos = Math.min(1, ratio / 3);
    $('er-arc').style.strokeDashoffset = ARC * (1 - pos);
    $('er-needle').style.transform = 'rotate(' + (-90 + pos * 180) + 'deg)';

    var label, text;
    if (!n || !f) { label = 'Waiting for data'; text = 'Add your followers and at least one post to see how you compare.'; }
    else if (ratio < 0.5) { label = 'Low'; text = 'Your engagement is under half the typical rate for ' + TIERS[t].split(' ')[0].toLowerCase() + ' accounts. Focus on content people save and share, and reply to every comment for a few weeks.'; }
    else if (ratio < 0.9) { label = 'Below average'; text = 'Slightly under the benchmark for your tier. Stronger hooks in the first second and clearer calls to comment usually close the gap.'; }
    else if (ratio < 1.3) { label = 'Healthy'; text = 'Right around the benchmark for your size. Brands will see you as a safe, solid partner. Lead with audience fit in your pitches.'; }
    else if (ratio < 2) { label = 'High'; text = 'Above the benchmark for your tier. Put this number at the top of your media kit and price toward the top of your range.'; }
    else { label = 'Exceptional'; text = 'More than double the typical rate for your size. That is rare and very attractive to brands, so do not undercharge.'; }
    var b = $('er-badge');
    if (b.textContent !== label) { b.textContent = label; b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop'); }
    $('er-verdict').textContent = text;
  }

  $('er-add').addEventListener('click', function () { addRow(); update(); var last = rows.lastElementChild; if (last) last.querySelector('input').focus(); });
  $('er-sample').addEventListener('click', function () {
    rows.innerHTML = '';
    [[612, 38, 41, 9800], [540, 22, 30, 8700], [890, 64, 77, 14200], [470, 19, 25, 7600], [705, 41, 52, 11000]].forEach(addRow);
    update();
  });
  $('er-followers').addEventListener('input', update);
  $('er-platform').addEventListener('change', update);
  [[612, 38, 41, 9800], [540, 22, 30, 8700], [890, 64, 77, 14200]].forEach(addRow);
  update();
})();
