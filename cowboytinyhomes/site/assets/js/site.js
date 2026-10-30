// Cowboy Tiny Homes — sticky header, mobile nav, FAQ search/filter, design filter, form tabs.
(function () {
  var header = document.querySelector('.site-header');
  var onScroll = function () { header && header.classList.toggle('is-stuck', window.scrollY > 10); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('.sub-toggle').forEach(function (b) {
      b.addEventListener('click', function () {
        var li = b.parentElement, open = li.classList.toggle('is-open');
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && nav.classList.contains('is-open')) toggle.click();
    });
  }

  // FAQ page: live search + topic filter.
  var search = document.querySelector('[data-faq-search]');
  var groups = document.querySelectorAll('[data-faq-group]');
  var filterBtns = document.querySelectorAll('[data-faq-filter]');
  var topic = 'all';
  function applyFaq() {
    var q = search ? search.value.trim().toLowerCase() : '';
    groups.forEach(function (g) {
      var shown = 0, inTopic = topic === 'all' || g.getAttribute('data-faq-group') === topic;
      g.querySelectorAll('.faq-item').forEach(function (it) {
        var hit = inTopic && (!q || it.textContent.toLowerCase().indexOf(q) !== -1);
        it.hidden = !hit;
        if (hit) shown++;
        if (q && hit) it.open = true;
      });
      g.hidden = shown === 0;
    });
    var none = document.querySelector('[data-faq-none]');
    if (none) none.hidden = Array.prototype.some.call(groups, function (g) { return !g.hidden; });
  }
  if (search) search.addEventListener('input', applyFaq);
  filterBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      topic = b.getAttribute('data-faq-filter');
      filterBtns.forEach(function (x) { x.classList.toggle('is-active', x === b); });
      applyFaq();
    });
  });

  // House designs: category filter.
  var dBtns = document.querySelectorAll('[data-design-filter]');
  dBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-design-filter');
      dBtns.forEach(function (x) { x.classList.toggle('is-active', x === b); });
      document.querySelectorAll('[data-design]').forEach(function (c) {
        c.hidden = f !== 'all' && c.getAttribute('data-design').split(' ').indexOf(f) === -1;
      });
    });
  });

  // Contact page: Design/Build vs Remodel tabs.
  var tabs = document.querySelectorAll('[role=tab][data-panel]');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on ? 'true' : 'false');
        var p = document.getElementById(x.getAttribute('data-panel'));
        if (p) p.hidden = !on;
      });
    });
  });

  // Interactive checklists (e.g. permit checklist) with a live progress count.
  document.querySelectorAll('[data-checklist]').forEach(function (box) {
    var out = box.querySelector('[data-checklist-count]');
    var inputs = box.querySelectorAll('input[type=checkbox]');
    function upd() {
      var n = 0; inputs.forEach(function (i) { if (i.checked) n++; });
      if (out) out.textContent = n + ' of ' + inputs.length + ' done' + (n === inputs.length ? ' — you are ready to talk to the permit office.' : '');
    }
    inputs.forEach(function (i) { i.addEventListener('change', upd); });
    upd();
  });
})();
