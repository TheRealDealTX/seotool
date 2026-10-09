/* The Painted Room — scroll and interaction effects. No dependencies. */
(function () {
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = d.querySelector('.site-header');
  var bar = d.querySelector('.progress');

  // Mobile menu
  var toggle = d.querySelector('.nav-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    var open = root.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open);
  });
  d.querySelectorAll('.menu a').forEach(function (a) {
    a.addEventListener('click', function () { root.classList.remove('nav-open'); });
  });

  // Reveal on scroll
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px', threshold: .08 }) : null;
  d.querySelectorAll('.reveal,.reveal-l,.stagger').forEach(function (el) {
    io ? io.observe(el) : el.classList.add('in');
  });

  // Counters
  var cio = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target, to = +el.dataset.count, t0 = null;
      cio.unobserve(el);
      if (reduce) { el.textContent = to + (el.dataset.suffix || ''); return; }
      (function step(t) {
        t0 = t0 || t;
        var p = Math.min((t - t0) / 1600, 1), v = Math.round(to * (1 - Math.pow(1 - p, 3)));
        el.textContent = v + (el.dataset.suffix || '');
        if (p < 1) requestAnimationFrame(step);
      })(performance.now());
    });
  }, { threshold: .5 }) : null;
  d.querySelectorAll('[data-count]').forEach(function (el) { cio && cio.observe(el); });

  // Word-by-word quote highlight
  var quote = d.querySelector('.big-quote[data-words]');
  if (quote) {
    quote.innerHTML = quote.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w">' + w + '</span>'; }).join(' ');
  }
  var words = quote ? quote.querySelectorAll('.w') : [];

  // TOC highlight
  var tocLinks = d.querySelectorAll('.toc a');
  var heads = Array.prototype.map.call(tocLinks, function (a) { return d.getElementById(a.hash.slice(1)); });

  var para = d.querySelectorAll('[data-speed]');
  var hs = d.querySelector('.hscroll'), track = hs && hs.querySelector('.hscroll-track');
  function sizeHs() {
    if (!hs || !track) return;
    if (window.innerWidth <= 820) { hs.style.removeProperty('--hs-h'); return; }
    var extra = track.scrollWidth - window.innerWidth + 120;
    hs.style.setProperty('--hs-h', (window.innerHeight + Math.max(extra, 0)) + 'px');
  }
  sizeHs();
  window.addEventListener('resize', sizeHs);

  var lastY = 0, ticking = false;
  function onScroll() {
    var y = window.scrollY, h = root.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (header) {
      header.classList.toggle('scrolled', y > 30);
      header.classList.toggle('hide', y > 400 && y > lastY && !root.classList.contains('nav-open'));
    }
    lastY = y;
    if (!reduce) {
      para.forEach(function (el) {
        var r = el.getBoundingClientRect(), mid = r.top + r.height / 2 - window.innerHeight / 2;
        el.style.transform = 'translate3d(0,' + (mid * -parseFloat(el.dataset.speed)).toFixed(1) + 'px,0) rotate(' + (el.dataset.rot ? (mid * el.dataset.rot).toFixed(2) : 0) + 'deg)';
      });
      if (hs && track && window.innerWidth > 820) {
        var r = hs.getBoundingClientRect(), span = hs.offsetHeight - window.innerHeight;
        var p = Math.min(Math.max(-r.top / span, 0), 1);
        track.style.transform = 'translate3d(' + (-p * (track.scrollWidth - window.innerWidth + 120)).toFixed(1) + 'px,0,0)';
      }
    }
    if (words.length) {
      var qr = quote.getBoundingClientRect();
      var qp = Math.min(Math.max((window.innerHeight * .85 - qr.top) / (qr.height + window.innerHeight * .4), 0), 1);
      var n = Math.round(qp * words.length);
      words.forEach(function (w, i) { w.classList.toggle('on', i < n); });
    }
    if (tocLinks.length) {
      var cur = 0;
      heads.forEach(function (hd, i) { if (hd && hd.getBoundingClientRect().top < 160) cur = i; });
      tocLinks.forEach(function (a, i) { a.classList.toggle('active', i === cur); });
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  // Card tilt
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    d.querySelectorAll('.card').forEach(function (c) {
      c.addEventListener('mousemove', function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.style.transform = 'perspective(900px) rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 6) + 'deg) translateY(-6px)';
      });
      c.addEventListener('mouseleave', function () { c.style.transform = ''; });
    });
    // Cursor swatch
    var cur = d.createElement('div'); cur.className = 'cursor'; d.body.appendChild(cur);
    var cx = 0, cy = 0, tx = 0, ty = 0;
    d.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; cur.style.opacity = 1; });
    d.addEventListener('mouseleave', function () { cur.style.opacity = 0; });
    d.querySelectorAll('a,button,.chip').forEach(function (el) {
      el.addEventListener('mouseenter', function () { cur.classList.add('big'); });
      el.addEventListener('mouseleave', function () { cur.classList.remove('big'); });
    });
    (function loop() {
      cx += (tx - cx) * .18; cy += (ty - cy) * .18;
      cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px) translate(-50%,-50%)';
      requestAnimationFrame(loop);
    })();
  }

  // Room scheme mixer
  var mixer = d.querySelector('.mixer');
  if (mixer) {
    var room = mixer.querySelector('.room'), note = mixer.querySelector('.mixer-note');
    var state = {};
    mixer.querySelectorAll('.dots').forEach(function (g) {
      var prop = g.dataset.prop;
      g.querySelectorAll('.dot').forEach(function (b) {
        if (b.getAttribute('aria-pressed') === 'true') state[prop] = b.dataset.name;
        b.addEventListener('click', function () {
          g.querySelectorAll('.dot').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
          b.setAttribute('aria-pressed', 'true');
          room.style.setProperty('--' + prop, b.dataset.color);
          state[prop] = b.dataset.name;
          if (note) note.textContent = 'Walls in ' + state.wall + ', a ' + state.sofa + ' sofa and ' + state.art + ' on the walls — ' + (b.dataset.tip || '');
        });
      });
    });
  }

  // Contact form → composes an email (no data is stored on the server)
  var form = d.querySelector('form[data-mailto]');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form), body = '';
    f.forEach(function (v, k) { if (k !== 'subject') body += k + ': ' + v + '\n'; });
    window.location.href = 'mailto:' + form.dataset.mailto + '?subject=' + encodeURIComponent(f.get('subject') || 'Enquiry') + '&body=' + encodeURIComponent(body);
  });
})();
