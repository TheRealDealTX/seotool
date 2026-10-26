/* Best Jobs Pro: navigation, scroll effects and the animated "talent network" hero. */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Mobile nav
  var toggle = $('.nav-toggle'), nav = $('#site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) document.body.classList.remove('nav-open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') document.body.classList.remove('nav-open'); });
  }

  // Header shadow once the page scrolls
  var header = $('.site-header');
  function onScroll() { if (header) header.classList.toggle('is-stuck', window.scrollY > 10); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Reveal on scroll + count-up numbers + timeline progress
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count')), suffix = el.getAttribute('data-suffix') || '', prefix = el.getAttribute('data-prefix') || '';
    if (reduce) { el.textContent = prefix + end + suffix; return; }
    var t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / 1400), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
      el.textContent = prefix + v + suffix;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        $$('[data-count]', en.target).forEach(countUp);
        if (en.target.hasAttribute('data-count')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: .15, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal, .stagger, .timeline, [data-count]').forEach(function (el) { io.observe(el); });
  } else {
    $$('.reveal, .stagger, .timeline').forEach(function (el) { el.classList.add('in'); });
    $$('[data-count]').forEach(function (el) { el.textContent = (el.getAttribute('data-prefix') || '') + el.getAttribute('data-count') + (el.getAttribute('data-suffix') || ''); });
  }

  // Typewriter job titles in the home hero
  var tw = $('[data-typewriter]');
  if (tw) {
    var words = tw.getAttribute('data-typewriter').split('|'), wi = 0, ci = words[0].length, del = true;
    if (!reduce) {
      setTimeout(function tick() {
        var w = words[wi];
        ci += del ? -1 : 1;
        tw.textContent = w.slice(0, ci);
        var wait = del ? 45 : 85;
        if (!del && ci === w.length) { del = true; wait = 1800; }
        else if (del && ci === 0) { del = false; wi = (wi + 1) % words.length; wait = 300; }
        setTimeout(tick, wait);
      }, 2200);
    }
  }

  // Subtle 3D tilt on cards
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    $$('.tilt').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        card.style.transform = 'perspective(800px) rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 6) + 'deg) translateY(-4px)';
        card.style.setProperty('--mx', (x + .5) * 100 + '%'); card.style.setProperty('--my', (y + .5) * 100 + '%');
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }

  // Talent network: candidates (light dots) and employers (coral dots) drift and connect;
  // now and then a "match" pulse runs along a link.
  function network(canvas) {
    var ctx = canvas.getContext('2d'), dpr = Math.min(2, window.devicePixelRatio || 1);
    var W, H, nodes = [], pulses = [], running = true, last = 0;
    function size() {
      var r = canvas.getBoundingClientRect(); W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(70, Math.max(24, W * H / 16000)));
      nodes = [];
      for (var i = 0; i < n; i++) nodes.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35, emp: Math.random() < .28, r: 1.6 + Math.random() * 1.8 });
    }
    function frame(t) {
      if (!running) return;
      var dt = Math.min(50, t - last || 16); last = t;
      ctx.clearRect(0, 0, W, H);
      var D = Math.min(150, W / 6);
      for (var i = 0; i < nodes.length; i++) {
        var a = nodes[i];
        a.x += a.vx * dt / 16; a.y += a.vy * dt / 16;
        if (a.x < 0 || a.x > W) a.vx *= -1;
        if (a.y < 0 || a.y > H) a.vy *= -1;
        for (var j = i + 1; j < nodes.length; j++) {
          var b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d = Math.sqrt(dx * dx + dy * dy);
          if (d < D) {
            var match = a.emp !== b.emp;
            ctx.strokeStyle = match ? 'rgba(255,87,87,' + (1 - d / D) * .45 + ')' : 'rgba(255,255,255,' + (1 - d / D) * .14 + ')';
            ctx.lineWidth = match ? 1.1 : .8;
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
            if (match && pulses.length < 6 && Math.random() < .0009) pulses.push({ a: a, b: b, k: 0 });
          }
        }
      }
      pulses = pulses.filter(function (p) {
        p.k += dt / 900;
        var x = p.a.x + (p.b.x - p.a.x) * p.k, y = p.a.y + (p.b.y - p.a.y) * p.k;
        var g = ctx.createRadialGradient(x, y, 0, x, y, 10);
        g.addColorStop(0, 'rgba(255,190,190,.95)'); g.addColorStop(1, 'rgba(255,87,87,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, 10, 0, 7); ctx.fill();
        return p.k < 1;
      });
      for (var k = 0; k < nodes.length; k++) {
        var n = nodes[k];
        ctx.fillStyle = n.emp ? '#FF5757' : 'rgba(255,255,255,.75)';
        ctx.beginPath(); ctx.arc(n.x, n.y, n.emp ? n.r + .8 : n.r, 0, 7); ctx.fill();
      }
      requestAnimationFrame(frame);
    }
    size();
    window.addEventListener('resize', function () { size(); });
    if (reduce) { frame(0); running = false; return; }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !running) { running = true; requestAnimationFrame(frame); }
        running = vis;
      }).observe(canvas);
    }
    requestAnimationFrame(frame);
  }
  $$('.net-canvas').forEach(function (c) { if (c.getContext) network(c); });

  // Blog table of contents: highlight the section in view
  var toc = $('.toc');
  if (toc && 'IntersectionObserver' in window) {
    var links = {};
    $$('a', toc).forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && links[en.target.id]) {
          $$('a', toc).forEach(function (a) { a.classList.remove('on'); });
          links[en.target.id].classList.add('on');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    $$('.prose h2[id]').forEach(function (h) { tio.observe(h); });
  }

  // Reading progress bar on articles
  var prog = $('.read-progress span'), article = $('.prose');
  if (prog && article) {
    window.addEventListener('scroll', function () {
      var r = article.getBoundingClientRect(), total = r.height - window.innerHeight;
      prog.style.width = Math.max(0, Math.min(1, -r.top / (total > 0 ? total : 1))) * 100 + '%';
    }, { passive: true });
  }

  // Job board filters
  var board = $('[data-jobboard]');
  if (board) {
    var q = $('#job-search'), chips = $$('[data-filter]'), cards = $$('.job-card', board), empty = $('.jobs-empty'), count = $('[data-jobcount]');
    var cat = 'all';
    function apply() {
      var term = (q.value || '').toLowerCase().trim(), shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.getAttribute('data-cat') === cat) && (!term || c.textContent.toLowerCase().indexOf(term) >= 0);
        c.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = shown;
    }
    chips.forEach(function (ch) {
      ch.addEventListener('click', function () {
        cat = ch.getAttribute('data-filter');
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === ch ? 'true' : 'false'); });
        apply();
      });
    });
    q.addEventListener('input', apply);
  }

  // Apply links from job cards preselect the job on the application form
  var jobSelect = $('#f-job');
  if (jobSelect) {
    var m = /[?&]job=([^&]+)/.exec(location.search);
    if (m) {
      var want = decodeURIComponent(m[1].replace(/\+/g, ' '));
      $$('option', jobSelect).forEach(function (o) { if (o.value === want) jobSelect.value = want; });
    }
    var other = $('#f-other-wrap');
    var syncOther = function () { if (other) other.hidden = jobSelect.value !== 'Other'; };
    jobSelect.addEventListener('change', syncOther); syncOther();
  }

  // File input: show the chosen file name
  $$('.file input[type=file]').forEach(function (inp) {
    inp.addEventListener('change', function () {
      var label = inp.closest('.file').querySelector('.file__name');
      if (label) label.textContent = inp.files && inp.files[0] ? inp.files[0].name : 'No file chosen';
    });
  });
})();
