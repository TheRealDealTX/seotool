(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('curtain-form'), out = document.getElementById('curtain-result');
  if (!form) return;
  var STD = [63, 84, 95, 96, 108, 120];
  var EXTRA = { float: -0.5, kiss: 0, break: 2, puddle: 7 };
  var NAMES = { float: 'floats ½ in. above the floor', kiss: 'just kisses the floor', break: 'breaks on the floor with about 2 in. extra', puddle: 'puddles with about 7 in. extra' };
  L.bind(form, function (v) {
    var ext = v.ww >= 60 ? 12 : 10;
    var rod = v.ww + ext * 2;
    var mountAbove = v.above >= 10 ? v.above - 5 : Math.max(v.above - 2, Math.min(4, v.above));
    var rodHeight = v.below + v.wh + mountAbove;          // from floor
    var length = rodHeight + EXTRA[v.len];
    var fabric = rod * v.full, panels = Math.ceil(fabric / v.pw - 0.05);
    if (panels < 2) panels = 2;
    var stdLen = STD.filter(function (s) { return s >= length - 0.5; })[0];
    var stdNote = stdLen ? (stdLen - length > 3 ? 'Buy ' + stdLen + ' in. panels and hem them to ' + L.fmt(length) + ' in., or hang the rod ' + L.fmt(stdLen - length) + ' in. higher if the ceiling allows.' : 'Buy ' + stdLen + ' in. panels.') : 'You need panels longer than 120 in.; look for extra-long or custom curtains.';
    out.innerHTML = '<p class="result__label">Curtain panel length</p><p class="result__big">' + L.fmt(length) + ' in.</p>' +
      '<p class="result__sub">So the fabric ' + NAMES[v.len] + '. ' + stdNote + '</p>' +
      '<div class="result-stats">' +
      '<div class="stat"><b>' + L.fmt(rod) + ' in.</b><span>rod width (' + ext + ' in. past the frame each side)</span></div>' +
      '<div class="stat"><b>' + L.fmt(rodHeight) + ' in.</b><span>rod height from the floor (' + L.fmt(mountAbove) + ' in. above the frame)</span></div>' +
      '<div class="stat"><b>' + panels + ' panels</b><span>' + v.pw + ' in. wide for ' + v.full + '× fullness (' + L.fmt(fabric) + ' in. of fabric)</span></div></div>' +
      '<ul><li>Hanging the rod high and wide makes the window, and the ceiling, look bigger. With the panels open, the fabric should cover the wall, not the glass.</li>' +
      (v.above < 6 ? '<li>Your window is close to the ceiling, so mount the rod just below the ceiling or use a ceiling-mounted track.</li>' : '<li>Mount brackets 4–6 in. below the ceiling or crown molding when you have the room.</li>') +
      (panels % 2 ? '<li>An odd number of panels is fine for a one-way draw; for a pair that meets in the middle, round up to ' + (panels + 1) + '.</li>' : '') +
      '<li>Renting? Tension rods or adhesive-free brackets that use existing holes avoid new drilling. Ask your landlord first.</li></ul>';
  });
})();
