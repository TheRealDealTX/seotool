// Tiny Homes Blueprint - mobile nav, plan filters and small shared helpers.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('nav-open', open);
    };
    toggle.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    nav.querySelectorAll('.sub-toggle').forEach(function (b) {
      b.addEventListener('click', function () {
        var li = b.parentElement;
        var open = li.classList.toggle('open');
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
    // Close on link tap (including same-page anchors), Escape, or growing back to desktop width.
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); toggle.focus(); }
    });
    var mq = window.matchMedia('(min-width: 1021px)');
    var onMq = function () { if (mq.matches) setOpen(false); };
    if (mq.addEventListener) mq.addEventListener('change', onMq); else mq.addListener(onMq);
  }

  // Plan catalog filters: any <form class="filters" data-target="..."> with selects named
  // style / beds / type / size / sort filters the .plan-card elements inside the target.
  document.querySelectorAll('form.filters').forEach(function (form) {
    var grid = document.querySelector(form.dataset.target);
    if (!grid) return;
    var count = form.querySelector('.filter-count');
    function apply() {
      var el = form.elements;
      var val = function (n) { return el.namedItem(n) ? el.namedItem(n).value : ''; };
      var style = val('style'), beds = val('beds'), type = val('type'), size = val('size'), sort = val('sort');
      var cards = Array.prototype.slice.call(grid.querySelectorAll('.plan-card:not(.plan-custom)')), shown = 0;
      cards.forEach(function (c) {
        var sq = +c.dataset.sqft, range = size ? size.split('-') : null;
        var ok = (!style || (' ' + c.dataset.styles + ' ').indexOf(' ' + style + ' ') > -1) &&
                 (!beds || +c.dataset.beds >= +beds) &&
                 (!type || (type === 'loft' ? c.dataset.loft === '1' : c.dataset.type === type)) &&
                 (!range || (sq >= +range[0] && sq <= +range[1]));
        c.hidden = !ok; if (ok) shown++;
      });
      if (sort) {
        var k = sort.split('-'), dir = k[1] === 'desc' ? -1 : 1;
        cards.sort(function (a, b) { return (a.dataset[k[0]] - b.dataset[k[0]]) * dir; })
             .forEach(function (c) { c.parentNode.insertBefore(c, c.parentNode.querySelector('.plan-custom')); });
      }
      if (count) count.textContent = shown + (shown === 1 ? ' plan' : ' plans');
      var empty = document.querySelector(form.dataset.empty);
      if (empty) empty.hidden = shown > 0;
    }
    form.addEventListener('change', apply);
    form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    apply();
  });
})();

// Shared number formatting for the calculators.
window.THB = {
  usd: function (n) { return '$' + Math.round(n).toLocaleString('en-US'); },
  num: function (n, d) { return Number(n).toLocaleString('en-US', { maximumFractionDigits: d || 0 }); }
};
