/* Collin Hughes Weddings — nav, hero slideshow, reveals, parallax, lightbox */
(function () {
  var d = document, body = d.body, hdr = d.querySelector('.hdr');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* mobile nav */
  var burger = d.querySelector('.burger'), nav = d.getElementById('site-nav');
  function setNav(open) {
    body.classList.toggle('nav-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open) { var f = nav.querySelector('a'); if (f) setTimeout(function () { f.focus(); }, 300); }
  }
  if (burger && nav) {
    burger.addEventListener('click', function () { setNav(!body.classList.contains('nav-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) { setNav(false); burger.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 960 && body.classList.contains('nav-open')) setNav(false); });
  }

  /* header state, progress bar, back-to-top, parallax */
  var bar = d.querySelector('.progress'), top = d.querySelector('.totop');
  var px = reduce ? [] : [].slice.call(d.querySelectorAll('[data-parallax]'));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY, h = d.documentElement.scrollHeight - window.innerHeight;
    if (hdr && !hdr.classList.contains('solid')) hdr.classList.toggle('scrolled', y > 40);
    if (hdr && hdr.classList.contains('solid')) hdr.classList.toggle('scrolled', y > 40);
    if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (top) top.classList.toggle('on', y > 900);
    px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute('data-parallax')) || 0.15;
      el.style.transform = 'translate3d(0,' + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + 'px,0)';
    });
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* reveal on scroll */
  var rv = d.querySelectorAll('.rv, .rv-img');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  /* hero slideshow */
  var slides = d.querySelectorAll('.hero .slides figure'), dots = d.querySelectorAll('.dots button');
  if (slides.length > 1) {
    var i = 0, timer;
    var go = function (n) {
      slides[i].classList.remove('on'); if (dots[i]) dots[i].classList.remove('on');
      i = (n + slides.length) % slides.length;
      slides[i].classList.add('on'); if (dots[i]) dots[i].classList.add('on');
    };
    var start = function () { clearInterval(timer); if (!reduce) timer = setInterval(function () { go(i + 1); }, 6500); };
    dots.forEach(function (b, n) { b.addEventListener('click', function () { go(n); start(); }); });
    start();
  }

  /* lightbox */
  var links = [].slice.call(d.querySelectorAll('.gallery a'));
  if (links.length) {
    var lb = d.createElement('div'), cur = 0;
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Photo viewer');
    lb.innerHTML = '<img alt=""><button class="x" aria-label="Close">&times;</button><button class="pv" aria-label="Previous">&lsaquo;</button><button class="nx" aria-label="Next">&rsaquo;</button>';
    body.appendChild(lb);
    var im = lb.querySelector('img');
    var show = function (n) { cur = (n + links.length) % links.length; im.src = links[cur].href; im.alt = links[cur].querySelector('img').alt; };
    var close = function () { lb.classList.remove('on'); body.style.overflow = ''; links[cur].focus(); };
    links.forEach(function (a, n) { a.addEventListener('click', function (e) { e.preventDefault(); show(n); lb.classList.add('on'); body.style.overflow = 'hidden'; lb.querySelector('.x').focus(); }); });
    lb.querySelector('.x').addEventListener('click', close);
    lb.querySelector('.pv').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.nx').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'ArrowRight') show(cur + 1);
    });
    var sx = 0;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); });
  }

  /* contact form status from ?sent= */
  var st = d.querySelector('[data-form-status]');
  if (st) {
    var q = new URLSearchParams(location.search).get('sent');
    if (q === '1') { st.textContent = 'Thank you — your note is on its way. We reply within two business days.'; st.hidden = false; }
    else if (q === '0') { st.textContent = 'Something went wrong sending your message. Please email info@collinhughesweddings.com directly.'; st.className = 'notice err'; st.hidden = false; }
  }
})();
