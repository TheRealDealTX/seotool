// Tiny Homes Blueprint - mobile nav, plan filters and small shared helpers.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('.sub-toggle').forEach(function (b) {
      b.addEventListener('click', function () {
        var li = b.parentElement;
        var open = li.classList.toggle('open');
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }

  // Plan catalog filters: any <form class="filters" data-target="..."> with selects named
  // style / beds / floors / sort filters the .plan-card elements inside the target.
  document.querySelectorAll('form.filters').forEach(function (form) {
    var grid = document.querySelector(form.dataset.target);
    if (!grid) return;
    var count = form.querySelector('.filter-count');
    function apply() {
      var el = form.elements;
      var style = el.namedItem('style') ? el.namedItem('style').value : '';
      var beds = el.beds.value, floors = el.floors.value, sort = el.sort.value;
      var cards = Array.prototype.slice.call(grid.querySelectorAll('.plan-card')), shown = 0;
      cards.forEach(function (c) {
        var ok = (!style || (' ' + c.dataset.styles + ' ').indexOf(' ' + style + ' ') > -1) &&
                 (!beds || +c.dataset.beds >= +beds) && (!floors || c.dataset.floors === floors);
        c.hidden = !ok; if (ok) shown++;
      });
      if (sort) {
        var k = sort.split('-'), dir = k[1] === 'desc' ? -1 : 1;
        cards.sort(function (a, b) { return (a.dataset[k[0]] - b.dataset[k[0]]) * dir; })
             .forEach(function (c) { grid.appendChild(c); });
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
