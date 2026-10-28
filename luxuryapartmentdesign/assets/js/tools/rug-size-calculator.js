(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('rug-form'), out = document.getElementById('rug-result');
  if (!form) return;
  var SIZES = [[3, 5], [4, 6], [5, 8], [6, 9], [8, 10], [9, 12], [10, 14], [12, 15]];
  var RUNNERS = [[2.5, 6], [2.5, 8], [2.5, 10], [2.5, 12], [3, 12], [3, 14]];
  var BED = { twin: [5, 8], full: [6, 9], queen: [8, 10], king: [9, 12], cal: [9, 12] };
  var BED_IN = { twin: [38, 75], full: [54, 75], queen: [60, 80], king: [76, 80], cal: [72, 84] };

  function fits(s, maxL, maxW) { return Math.max(s[0], s[1]) <= maxL && Math.min(s[0], s[1]) <= maxW; }
  function largest(list, maxL, maxW) { var best = null; list.forEach(function (s) { if (fits(s, maxL, maxW)) best = s; }); return best; }
  function smallestAtLeast(list, l, w) { for (var i = 0; i < list.length; i++) if (list[i][1] >= l && list[i][0] >= w) return list[i]; return null; }
  function label(s) { return s[0] + "' × " + s[1] + "'"; }

  function draw(roomL, roomW, rug) {
    var W = 320, pad = 10, sc = (W - pad * 2) / Math.max(roomL, roomW), rl = roomL * sc, rw = roomW * sc;
    var gl = Math.max(rug[0], rug[1]) * sc, gw = Math.min(rug[0], rug[1]) * sc;
    var H = rw + pad * 2;
    return '<svg class="diagram" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Rug placement diagram">' +
      '<rect x="' + pad + '" y="' + pad + '" width="' + rl + '" height="' + rw + '" fill="#f6f1e8" stroke="#1c1a17" stroke-width="2"/>' +
      '<rect x="' + (pad + (rl - gl) / 2) + '" y="' + (pad + (rw - gw) / 2) + '" width="' + gl + '" height="' + gw + '" fill="#d4ae5e" fill-opacity=".55" stroke="#b88a2e" stroke-dasharray="4 3"/>' +
      '<text x="' + (W / 2) + '" y="' + (pad + rw / 2 + 4) + '" text-anchor="middle" font-size="12" fill="#1c1a17">' + label(rug) + ' rug</text></svg>';
  }

  L.bind(form, function (v) {
    var L1 = Math.max(v.len, v.wid), W1 = Math.min(v.len, v.wid);
    if (!L1 || !W1) { out.innerHTML = '<p>Enter your room size.</p>'; return; }
    var small = W1 < 10, border = small ? 0.75 : 1.25;  // 9 in. or 15 in. of floor each side
    var maxL = L1 - border * 2, maxW = W1 - border * 2, rug, notes = [], sub = '';

    if (v.room === 'hall') {
      var maxRl = L1 - 1, maxRw = W1 - 0.67;
      rug = W1 >= 4.5 && L1 <= 8 ? largest(SIZES, L1 - 1.5, W1 - 1.5) : largest(RUNNERS, maxRl, maxRw);
      sub = W1 >= 4.5 && L1 <= 8 ? 'An entry rug sized to the space' : 'A runner for your hallway';
      notes.push('Leave about 4–6 in. of floor on each side of a runner and 6–12 in. at each end.');
      notes.push('Make sure the front door clears the rug when it swings open; low-pile or flatweave works best.');
    } else if (v.room === 'dining') {
      var needL = (v.tl + 48) / 12, needW = (v.tw + 48) / 12;
      rug = smallestAtLeast(SIZES, needL, needW);
      sub = 'Table plus at least 24 in. on every side, so chairs stay on the rug when pulled out';
      notes.push('Minimum rug size for your table: ' + L.fmt(needW) + "' × " + L.fmt(needL) + "'.");
      if (rug && !fits(rug, L1, W1)) notes.push('That rug is close to your room size. Consider a custom size, or a smaller table.');
      if (!rug) { rug = largest(SIZES, maxL, maxW); notes.push('Your table needs more than 12 × 15 ft; consider a custom or bound broadloom rug.'); }
      notes.push('Round tables work beautifully on round rugs: aim for a diameter about 4 ft larger than the table.');
    } else if (v.room === 'bedroom') {
      rug = BED[v.bed];
      var b = BED_IN[v.bed];
      sub = 'Under the bottom two-thirds of the bed, extending 18–24 in. beyond each side';
      if (!fits(rug, maxL, maxW)) {
        notes.push('Your room is tight for a full-size rug under the bed. Try two runners (2.5\' × ' + Math.ceil(b[1] / 12) + "') along each side, or a smaller rug at the foot.");
      }
      notes.push('Start the rug 6–12 in. in front of the nightstands so they sit on bare floor, or bring it under them in larger rooms.');
    } else {
      var target = v.layout === 'all' ? [maxW, maxL] : v.layout === 'front' ? [Math.min(maxW, 9), Math.min(maxL, 12)] : [Math.min(maxW, 6), Math.min(maxL, 9)];
      rug = largest(SIZES, target[1], target[0]) || [3, 5];
      sub = v.layout === 'all' ? 'Large enough for every piece of seating to sit fully on the rug'
        : v.layout === 'front' ? 'Front legs of the sofa and chairs on the rug, at least 6–8 in. in'
        : 'A smaller anchor under the coffee table (works best with compact seating)';
      if (v.layout === 'float') notes.push('A rug that floats in the middle with no furniture touching can look small. Front legs on is the safer choice.');
      notes.push('Leave ' + (small ? '8–12' : '12–18') + ' in. of bare floor between the rug and the walls.');
      if (rug[0] * rug[1] < 40 && v.layout !== 'float') notes.push('If in doubt, size up. An oversized rug almost always looks more expensive than an undersized one.');
    }
    var gapL = (L1 - Math.max(rug[0], rug[1])) / 2 * 12, gapW = (W1 - Math.min(rug[0], rug[1])) / 2 * 12;
    out.innerHTML = '<p class="result__label">Recommended rug</p><p class="result__big">' + label(rug) + '</p><p class="result__sub">' + sub + '</p>' +
      draw(L1, W1, rug) +
      '<div class="result-stats"><div class="stat"><b>' + Math.round(gapW) + ' in.</b><span>floor showing on the long sides</span></div><div class="stat"><b>' + Math.round(gapL) + ' in.</b><span>floor showing at each end</span></div></div>' +
      '<ul>' + notes.map(function (n) { return '<li>' + n + '</li>'; }).join('') + '</ul>';
  });
})();
