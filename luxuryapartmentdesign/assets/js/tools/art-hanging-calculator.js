(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('art-form'), out = document.getElementById('art-result');
  if (!form) return;
  L.bind(form, function (v) {
    var center = v.center + (v.ceil >= 10 ? 3 : v.ceil > 9 ? 1.5 : 0);
    var notes = [], nail, bottom, top, html = '';
    if (v.mode === 'gallery') {
      var gw = v.cols * v.aw + (v.cols - 1) * v.gap, gh = v.rows * v.ah + (v.rows - 1) * v.gap;
      var gTop = center + gh / 2;
      nail = gTop - v.drop;
      html = '<p class="result__label">Top row nail height</p><p class="result__big">' + L.fmt(nail) + ' in.</p>' +
        '<p class="result__sub">' + L.ftin(nail) + ' from the floor, for frames ' + v.aw + ' × ' + v.ah + ' in.</p>' +
        '<div class="result-stats"><div class="stat"><b>' + L.fmt(gw) + '″ × ' + L.fmt(gh) + '″</b><span>overall gallery size</span></div>' +
        '<div class="stat"><b>' + L.fmt(v.aw + v.gap) + ' in.</b><span>between nails, left to right</span></div>' +
        '<div class="stat"><b>' + L.fmt(v.ah + v.gap) + ' in.</b><span>between rows of nails</span></div></div>';
      notes.push('Treat the whole grid as one piece of art: its center sits at ' + L.fmt(center) + ' in.');
      notes.push('Lay the arrangement out on the floor first, or tape paper templates to the wall.');
      bottom = gTop - gh; top = gTop;
      if (gh > 0) html += svg(v, gTop, gw, gh, true);
    } else {
      if (v.mode === 'furniture') {
        bottom = v.fh + 9;
        top = bottom + v.ah;
        var ratio = v.aw / v.fw;
        notes.push('Bottom of the frame sits 9 in. above the furniture (the 8–10 in. sweet spot).');
        if (ratio < 0.6) notes.push('<strong>Art is narrow for this piece</strong> (' + Math.round(ratio * 100) + '% of its width). Aim for about two-thirds (60–75%), or hang a pair or trio side by side. Ideal width: ' + Math.round(v.fw * 0.6) + '–' + Math.round(v.fw * 0.75) + ' in.');
        else if (ratio > 0.8) notes.push('<strong>Art is wider than ideal</strong> (' + Math.round(ratio * 100) + '%). Keep it within about 75% of the furniture width so it does not overhang visually.');
        else notes.push('Great proportion: the art is ' + Math.round(ratio * 100) + '% of the furniture width (ideal is 60–75%).');
      } else {
        bottom = center - v.ah / 2;
        top = center + v.ah / 2;
        notes.push('The center of the art sits at ' + L.fmt(center) + ' in., roughly average eye level.');
      }
      nail = top - v.drop;
      html = '<p class="result__label">Put the nail at</p><p class="result__big">' + L.fmt(nail) + ' in.</p>' +
        '<p class="result__sub">' + L.ftin(nail) + ' from the floor' + (v.drop ? ', allowing ' + v.drop + ' in. of hanger drop' : '') + '</p>' +
        '<div class="result-stats"><div class="stat"><b>' + L.fmt(top) + ' in.</b><span>top of frame</span></div><div class="stat"><b>' + L.fmt(bottom) + ' in.</b><span>bottom of frame</span></div><div class="stat"><b>' + L.fmt((top + bottom) / 2) + ' in.</b><span>center of art</span></div></div>' +
        svg(v, top, v.aw, v.ah, false);
      if (v.aw > 30) notes.push('For pieces wider than about 30 in., use two hooks spaced about a third in from each side so the frame stays level.');
    }
    if (v.ceil >= 9.5) notes.push('With ' + v.ceil + ' ft ceilings the center has been raised slightly so the art does not look low.');
    if (top > v.ceil * 12 - 6) notes.push('<strong>Too tall:</strong> the top of the art would be within 6 in. of the ceiling. Choose a smaller piece or lower the arrangement.');
    out.innerHTML = html + '<ul>' + notes.map(function (n) { return '<li>' + n + '</li>'; }).join('') + '</ul>';
  });

  function svg(v, top, w, h, gallery) {
    var ceilIn = v.ceil * 12, W = 320, H = 260, sc = (H - 20) / ceilIn;
    var x0 = W / 2 - (w * sc) / 2, y = 10 + (ceilIn - top) * sc, s = '';
    if (gallery) {
      for (var r = 0; r < v.rows; r++) for (var c = 0; c < v.cols; c++)
        s += '<rect x="' + (x0 + c * (v.aw + v.gap) * sc) + '" y="' + (y + r * (v.ah + v.gap) * sc) + '" width="' + v.aw * sc + '" height="' + v.ah * sc + '" fill="#d4ae5e" fill-opacity=".5" stroke="#b88a2e"/>';
    } else {
      s = '<rect x="' + x0 + '" y="' + y + '" width="' + w * sc + '" height="' + h * sc + '" fill="#d4ae5e" fill-opacity=".5" stroke="#b88a2e"/>';
    }
    var furn = v.mode === 'furniture' ? '<rect x="' + (W / 2 - v.fw * sc / 2) + '" y="' + (10 + (ceilIn - v.fh) * sc) + '" width="' + v.fw * sc + '" height="' + v.fh * sc + '" fill="#e6ddcd" stroke="#6d665b"/>' : '';
    var person = '<g fill="#cfc6b6"><circle cx="30" cy="' + (10 + (ceilIn - 63) * sc) + '" r="' + 5 * sc + '"/><rect x="' + (30 - 7 * sc) + '" y="' + (10 + (ceilIn - 57) * sc) + '" width="' + 14 * sc + '" height="' + 57 * sc + '" rx="3"/></g>';
    return '<svg class="diagram" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Wall elevation showing art placement">' +
      '<rect x="0" y="10" width="' + W + '" height="' + ceilIn * sc + '" fill="#fbf8f2"/><line x1="0" x2="' + W + '" y1="' + (10 + ceilIn * sc) + '" y2="' + (10 + ceilIn * sc) + '" stroke="#1c1a17" stroke-width="2"/>' +
      person + furn + s +
      '<line x1="0" x2="' + W + '" y1="' + (10 + (ceilIn - v.center) * sc) + '" y2="' + (10 + (ceilIn - v.center) * sc) + '" stroke="#b88a2e" stroke-dasharray="3 4"/>' +
      '<text x="' + (W - 6) + '" y="' + (6 + (ceilIn - v.center) * sc) + '" text-anchor="end" font-size="10" fill="#b88a2e">' + v.center + ' in. eye level</text></svg>';
  }
})();
