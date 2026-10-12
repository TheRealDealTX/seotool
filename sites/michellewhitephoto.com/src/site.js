/* Michelle White Photo — header, mobile nav, hero slideshow, reveals, parallax, gallery lightbox */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* header state */
  var header = document.querySelector('.site-header');
  var hero = document.querySelector('.hero, .page-hero');
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    var heroH = hero ? hero.offsetHeight - 90 : 0;
    if (header) {
      header.classList.toggle('is-over-hero', !!hero && y < heroH);
      header.classList.toggle('is-solid', !hero || y >= heroH);
      header.classList.toggle('is-hidden', y > lastY && y > 400 && !doc.classList.contains('nav-open'));
    }
    lastY = y;
  }
  onScroll();

  /* mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  function setNav(open) {
    doc.classList.toggle('nav-open', open);
    if (toggle) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
    if (open && nav) { var first = nav.querySelector('a'); if (first) setTimeout(function () { first.focus(); }, 350); }
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setNav(!doc.classList.contains('nav-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && doc.classList.contains('nav-open')) { setNav(false); toggle.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 960 && doc.classList.contains('nav-open')) setNav(false); });
  }

  /* hero slideshow */
  var slides = [].slice.call(document.querySelectorAll('.hero-slide'));
  var dots = [].slice.call(document.querySelectorAll('.hero-dots button'));
  var cur = 0, timer;
  function show(i) {
    slides[cur].classList.remove('is-active'); if (dots[cur]) dots[cur].classList.remove('is-active');
    cur = (i + slides.length) % slides.length;
    var img = slides[cur].querySelector('img');
    if (img && img.loading === 'lazy') img.loading = 'eager';
    slides[cur].classList.add('is-active'); if (dots[cur]) dots[cur].classList.add('is-active');
  }
  function play() { clearInterval(timer); if (!reduce) timer = setInterval(function () { show(cur + 1); }, 6500); }
  if (slides.length > 1) {
    dots.forEach(function (d, i) { d.addEventListener('click', function () { show(i); play(); }); });
    play();
  }

  /* scroll reveal */
  var revealEls = document.querySelectorAll('.reveal, .reveal-img');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* parallax + reading progress */
  var par = [].slice.call(document.querySelectorAll('[data-parallax]'));
  var bar = document.querySelector('.progress');
  var ticking = false;
  function frame() {
    ticking = false;
    var vh = window.innerHeight;
    if (!reduce) par.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var speed = parseFloat(el.getAttribute('data-parallax')) || 0.15;
      var off = (r.top + r.height / 2 - vh / 2) * -speed;
      el.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
    });
    if (bar) {
      var h = document.documentElement.scrollHeight - vh;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ')';
    }
  }
  window.addEventListener('scroll', function () {
    onScroll();
    if (!ticking) { ticking = true; requestAnimationFrame(frame); }
  }, { passive: true });
  frame();

  /* gallery filters */
  var filterBtns = document.querySelectorAll('.filters button');
  filterBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      filterBtns.forEach(function (x) { x.classList.toggle('is-active', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      document.querySelectorAll('.gallery figure').forEach(function (fig) {
        fig.classList.toggle('is-hidden', f !== 'all' && fig.getAttribute('data-cat') !== f);
      });
    });
  });

  /* lightbox */
  var figs = [].slice.call(document.querySelectorAll('.gallery figure'));
  if (figs.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML = '<img alt=""><button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous image">&#8249;</button><button class="lb-next" aria-label="Next image">&#8250;</button><div class="lb-count"></div>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img'), lbCount = lb.querySelector('.lb-count'), idx = 0, opener = null;
    function visible() { return figs.filter(function (f) { return !f.classList.contains('is-hidden'); }); }
    function open(i) {
      var v = visible(); idx = (i + v.length) % v.length;
      var im = v[idx].querySelector('img');
      lbImg.src = im.getAttribute('data-full') || im.currentSrc || im.src;
      lbImg.alt = im.alt;
      lbCount.textContent = (idx + 1) + ' / ' + v.length;
      lb.classList.add('is-open'); doc.classList.add('lb-open');
    }
    function close() { lb.classList.remove('is-open'); doc.classList.remove('lb-open'); if (opener) opener.focus(); }
    figs.forEach(function (f) {
      f.setAttribute('tabindex', '0');
      f.setAttribute('role', 'button');
      function go() { opener = f; open(visible().indexOf(f)); lb.querySelector('.lb-close').focus(); }
      f.addEventListener('click', go);
      f.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { open(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { open(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') open(idx - 1);
      if (e.key === 'ArrowRight') open(idx + 1);
    });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) open(idx + (dx < 0 ? 1 : -1));
    });
  }

  /* footer year */
  var yr = document.querySelector('[data-year]');
  if (yr) yr.textContent = new Date().getFullYear();
})();
