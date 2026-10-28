(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('light-form'), out = document.getElementById('light-result');
  if (!form) return;
  var R = {
    living:   { fc: [10, 20], k: '2700K', name: 'living room', task: 'reading lamps beside seats', accent: 'picture lights, shelf lighting or a statement floor lamp' },
    bedroom:  { fc: [10, 20], k: '2700K', name: 'bedroom', task: 'bedside lamps or wall sconces', accent: 'a small lamp on a dresser or warm LED strip behind the headboard' },
    dining:   { fc: [30, 40], k: '2700K', name: 'dining room', task: 'a pendant or chandelier over the table (bottom 30–36 in. above the tabletop)', accent: 'candles, a buffet lamp or picture lights' },
    kitchen:  { fc: [30, 40], k: '3000K', name: 'kitchen', task: 'under-cabinet LEDs over the counters', accent: 'pendants over an island or toe-kick lighting' },
    bathroom: { fc: [70, 80], k: '3000K', name: 'bathroom', task: 'sconces on either side of the mirror at about face height', accent: 'a dimmable night light or LED mirror' },
    office:   { fc: [30, 50], k: '3500–4000K', name: 'home office', task: 'an adjustable desk lamp on the opposite side to your writing hand', accent: 'a lamp on a shelf to soften video calls' },
    hall:     { fc: [5, 10], k: '2700K', name: 'hallway', task: 'a ceiling fixture every 8–10 ft', accent: 'a small lamp on a console or picture lights' }
  };
  L.bind(form, function (v) {
    var r = R[v.room], area = v.len * v.wid;
    var fc = r.fc[0] + (r.fc[1] - r.fc[0]) * v.lvl, lm = Math.round(area * fc / 10) * 10;
    var lo = Math.round(area * r.fc[0]), hi = Math.round(area * r.fc[1]);
    var bulbs = Math.max(1, Math.ceil(lm / v.bulb));
    var amb = Math.round(lm * 0.5), task = Math.round(lm * 0.3), acc = lm - amb - task;
    out.innerHTML = '<p class="result__label">Total light for your ' + r.name + '</p><p class="result__big">' + L.fmt(lm, 0) + ' lumens</p>' +
      '<p class="result__sub">' + L.fmt(area, 0) + ' sq ft × ' + L.fmt(fc, 0) + ' foot-candles. Recommended range ' + L.fmt(lo, 0) + '–' + L.fmt(hi, 0) + ' lm.</p>' +
      '<div class="result-stats"><div class="stat"><b>' + bulbs + '</b><span>bulbs at ' + v.bulb + ' lm each</span></div><div class="stat"><b>' + r.k + '</b><span>color temperature</span></div></div>' +
      '<div class="budget-bar"><span style="width:50%;background:#1c1a17"></span><span style="width:30%;background:#b88a2e"></span><span style="width:20%;background:#d4ae5e"></span></div>' +
      '<ul><li><strong>Ambient (50%) ≈ ' + L.fmt(amb, 0) + ' lm:</strong> ceiling fixture, flush mounts or recessed lights' + (v.room === 'living' || v.room === 'bedroom' ? ', or a floor lamp that bounces light off the ceiling' : '') + '.</li>' +
      '<li><strong>Task (30%) ≈ ' + L.fmt(task, 0) + ' lm:</strong> ' + r.task + '.</li>' +
      '<li><strong>Accent (20%) ≈ ' + L.fmt(acc, 0) + ' lm:</strong> ' + r.accent + '.</li>' +
      '<li>Put as many sources as you can on dimmers (smart bulbs or plug-in dimmers are renter-friendly).</li>' +
      '<li>Dark walls, high ceilings and dark floors absorb light, so aim for the top of the range.</li></ul>';
  });
})();
