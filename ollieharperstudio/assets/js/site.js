// ollieharperstudio.com — header, nav, reveals, tilt, cursor glow, coloring studio, contact form.
(function () {
  document.documentElement.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var header = document.querySelector('.site-header');
  var onScroll = function () { header && header.classList.toggle('scrolled', window.scrollY > 10); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var toggle = document.querySelector('.nav-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open);
  });

  // Scroll reveal, staggered within each parent.
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) {
      var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.classList.contains('reveal'); });
      el.style.setProperty('--rd', (sibs.indexOf(el) % 6) * 0.08 + 's');
      io.observe(el);
    });
  } else items.forEach(function (el) { el.classList.add('in'); });

  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    // 3D tilt on cards
    document.querySelectorAll('.card, .post-card').forEach(function (card) {
      card.addEventListener('mousemove', function (ev) {
        var r = card.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - .5, y = (ev.clientY - r.top) / r.height - .5;
        card.style.transform = 'perspective(900px) rotateY(' + x * 8 + 'deg) rotateX(' + -y * 8 + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
    // Soft glow that follows the cursor
    var glow = document.createElement('div'); glow.className = 'glow'; document.body.appendChild(glow);
    var gx = 0, gy = 0, tx = 0, ty = 0;
    window.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; glow.style.opacity = 1; });
    (function loop() { gx += (tx - gx) * .12; gy += (ty - gy) * .12; glow.style.left = gx + 'px'; glow.style.top = gy + 'px'; requestAnimationFrame(loop); })();
    // Hero art parallax
    var art = document.querySelector('.hero-art');
    if (art) window.addEventListener('mousemove', function (e) {
      var x = e.clientX / window.innerWidth - .5, y = e.clientY / window.innerHeight - .5;
      art.style.transform = 'translate(' + x * -18 + 'px,' + y * -18 + 'px)';
    });
  }

  // Colouring studio: click a region to paint it with the chosen color.
  var studio = document.querySelector('[data-studio]');
  if (studio) {
    var current = '#ef5b3c', history = [];
    var swatches = studio.querySelectorAll('.palette button');
    swatches.forEach(function (b) {
      b.addEventListener('click', function () {
        swatches.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true'); current = b.dataset.color;
      });
    });
    var picker = studio.querySelector('input[type=color]');
    if (picker) picker.addEventListener('input', function () {
      swatches.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); }); current = picker.value;
    });
    var regions = studio.querySelectorAll('.cz');
    regions.forEach(function (p) {
      p.setAttribute('tabindex', '0');
      var paint = function () { history.push([p, p.getAttribute('fill')]); p.setAttribute('fill', current); };
      p.addEventListener('click', paint);
      p.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); paint(); } });
    });
    var act = function (name, fn) { var b = studio.querySelector('[data-' + name + ']'); if (b) b.addEventListener('click', fn); };
    act('undo', function () { var h = history.pop(); if (h) h[0].setAttribute('fill', h[1]); });
    act('clear', function () { history = []; regions.forEach(function (p) { p.setAttribute('fill', '#fff'); }); });
    act('surprise', function () {
      var cols = Array.prototype.map.call(swatches, function (b) { return b.dataset.color; });
      regions.forEach(function (p, i) {
        setTimeout(function () { p.setAttribute('fill', cols[Math.floor(Math.random() * cols.length)]); }, reduce ? 0 : i * 40);
      });
    });
    act('download', function () {
      var svgEl = studio.querySelector('svg');
      var data = new XMLSerializer().serializeToString(svgEl);
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([data], { type: 'image/svg+xml' }));
      a.download = 'ollie-harper-coloring-page.svg'; document.body.appendChild(a); a.click(); a.remove();
    });
  }

  // Contact form: opens the visitor's mail app with the brief pre-filled.
  var form = document.querySelector('form[data-mailto]');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form), lines = [];
    f.forEach(function (v, k) { if (k !== 'name') lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ': ' + v); });
    var subject = 'Project enquiry from ' + (f.get('name') || 'the website');
    window.location.href = 'mailto:' + form.dataset.mailto + '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(lines.join('\n\n'));
  });
})();
