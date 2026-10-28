(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('budget-form'), out = document.getElementById('budget-result');
  if (!form) return;
  var CATS = [
    ['furniture', 'Furniture', '#1c1a17'],
    ['lighting', 'Lighting', '#b88a2e'],
    ['textiles', 'Rugs & textiles', '#d4ae5e'],
    ['art', 'Art & wall decor', '#8a7d6b'],
    ['windows', 'Window treatments', '#cbbfae'],
    ['accessories', 'Accessories & plants', '#7f8a6e'],
    ['contingency', 'Contingency', '#e6ddcd']
  ];
  var BASE = {
    living:  { furniture: 45, lighting: 10, textiles: 15, art: 10, windows: 8, accessories: 5, contingency: 7 },
    bedroom: { furniture: 50, lighting: 8, textiles: 18, art: 7, windows: 8, accessories: 3, contingency: 6 },
    dining:  { furniture: 52, lighting: 14, textiles: 10, art: 9, windows: 6, accessories: 3, contingency: 6 },
    office:  { furniture: 50, lighting: 14, textiles: 8, art: 8, windows: 6, accessories: 7, contingency: 7 },
    studio:  { furniture: 50, lighting: 10, textiles: 14, art: 8, windows: 8, accessories: 3, contingency: 7 }
  };
  var SHIFT = {
    comfort:   { furniture: 4, textiles: 3, art: -3, accessories: -2, windows: -2 },
    statement: { art: 4, lighting: 3, furniture: -3, textiles: -2, accessories: -2 },
    storage:   { furniture: 6, accessories: -2, art: -2, textiles: -2 }
  };
  var DIY = { art: -4, accessories: -2, furniture: 4, lighting: 2 };
  var SPLURGE = {
    living: ['Sofa (you use it every day)', 'A large enough rug', 'Lamps you see and touch'],
    bedroom: ['Mattress and pillows', 'Bedding in natural fibers', 'Bedside lighting'],
    dining: ['Chairs that are comfortable for a long dinner', 'A pendant or chandelier', 'A solid table'],
    office: ['An ergonomic chair', 'A good desk lamp', 'A desk at the right height'],
    studio: ['A sofa or sofa bed you love', 'A mattress', 'Multi-functional storage']
  };
  var SAVE = ['Trend-led cushions and throws', 'Side tables and accessories', 'Frames (buy affordable, upgrade the mat)', 'Plants (start small and grow)'];
  var NOTES = {
    furniture: function (v) { return v.prio === 'storage' ? 'Prioritize closed storage: sideboards, beds with drawers, tall cabinets.' : 'Put the most into the pieces you sit or sleep on.'; },
    lighting: function () { return 'At least three sources per room; dimmers multiply the effect.'; },
    textiles: function () { return 'Size the rug correctly before choosing the pattern.'; },
    art: function (v) { return v.diy === 'diy' ? 'Frame your own prints or make large abstract canvases.' : 'One large piece beats several small ones.'; },
    windows: function () { return 'Rod, rings and floor-length panels, hung high and wide.'; },
    accessories: function () { return 'Edit to a few objects in odd-numbered groups.'; },
    contingency: function () { return 'For delivery, assembly, hardware and surprises.'; }
  };
  L.bind(form, function (v) {
    var pct = Object.assign({}, BASE[v.room]);
    var sh = SHIFT[v.prio];
    for (var k in sh) pct[k] += sh[k];
    if (v.diy === 'diy') for (var d in DIY) pct[d] += DIY[d];
    if (v.room === 'bedroom' && v.prio === 'statement') { pct.textiles += 2; pct.art -= 2; }
    var sum = 0; for (var s in pct) { pct[s] = Math.max(2, pct[s]); sum += pct[s]; }
    var total = Math.max(0, v.total);
    var rows = CATS.map(function (c) { var p = pct[c[0]] / sum * 100; return [c, p, Math.round(total * p / 100 / 5) * 5]; });
    out.innerHTML = '<p class="result__label">Suggested split</p><p class="result__big">$' + L.fmt(total, 0) + '</p>' +
      '<div class="budget-bar">' + rows.map(function (r) { return '<span style="width:' + r[1] + '%;background:' + r[0][2] + '" title="' + r[0][1] + '"></span>'; }).join('') + '</div>' +
      '<div class="table-wrap"><table class="data-table budget-table"><thead><tr><th>Category</th><th>What to buy</th><th>Budget</th></tr></thead><tbody>' +
      rows.map(function (r) {
        return '<tr><td><span class="swatch" style="background:' + r[0][2] + '"></span>' + r[0][1] + ' <small>(' + Math.round(r[1]) + '%)</small></td><td>' + NOTES[r[0][0]](v) + '</td><td>$' + L.fmt(r[2], 0) + '</td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<div class="field-row"><div><p class="field__label">Splurge on</p><ul>' + SPLURGE[v.room].map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div>' +
      '<div><p class="field__label">Save on</p><ul>' + SAVE.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div></div>' +
      (total < 1500 ? '<p>On a tight budget? Read <a href="/how-to-make-your-apartment-look-expensive/">how to make your apartment look expensive</a> for high-impact, low-cost moves.</p>' : '');
  });
})();
