/* Insurance Adjuster Salary - shared interactions */
(function () {
  'use strict';
  var doc = document.documentElement;
  var body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header state + scroll progress
  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.scroll-progress span');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 40);
    if (bar) {
      var max = doc.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.main-nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Number formatting helper shared with tool scripts
  window.IAS = window.IAS || {};
  IAS.money = function (n, compact) {
    if (compact && Math.abs(n) >= 1000) return '$' + (Math.round(n / 100) / 10).toLocaleString('en-US') + 'k';
    return '$' + Math.round(n).toLocaleString('en-US');
  };

  // Count-up numbers: <span data-count="76790" data-prefix="$" data-suffix="">
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count'));
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    var dec = parseInt(el.getAttribute('data-decimals') || '0', 10);
    if (reduce) { el.textContent = prefix + end.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suffix; return; }
    var start = performance.now(), dur = 1800;
    function tick(now) {
      var t = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - t, 4);
      el.textContent = prefix + (end * eased).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suffix;
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // Reveal on scroll + trigger counters / bars
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      el.classList.add('in');
      if (el.hasAttribute('data-count')) countUp(el);
      // Zero-width bars never intersect, so their track is observed and fills its children
      el.querySelectorAll(':scope > [data-width]').forEach(function (f) { f.style.width = f.getAttribute('data-width'); });
      io.unobserve(el);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }) : null;
  var watch = Array.prototype.slice.call(document.querySelectorAll('.reveal, [data-count]'));
  document.querySelectorAll('[data-width]').forEach(function (f) { if (watch.indexOf(f.parentElement) < 0) watch.push(f.parentElement); });
  watch.forEach(function (el) {
    if (io) io.observe(el);
    else {
      el.classList.add('in');
      el.querySelectorAll(':scope > [data-width]').forEach(function (f) { f.style.width = f.getAttribute('data-width'); });
    }
  });

  // Typed rotating words in hero: <span class="typed" data-words="a|b|c">
  document.querySelectorAll('.typed[data-words]').forEach(function (el) {
    var words = el.getAttribute('data-words').split('|');
    if (reduce || words.length < 2) return;
    var w = 0, i = words[0].length, deleting = true;
    function step() {
      var word = words[w];
      if (deleting) {
        i--;
        if (i <= 0) { deleting = false; w = (w + 1) % words.length; }
      } else {
        i++;
        if (i >= words[w].length) { deleting = true; el.textContent = words[w]; return setTimeout(step, 2200); }
      }
      el.textContent = words[w].slice(0, Math.max(0, i)) || ' ';
      setTimeout(step, deleting ? 45 : 85);
    }
    setTimeout(step, 2600);
  });

  // Tilt + spotlight cards
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.tilt, .spotlight').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        card.style.setProperty('--mx', (x * 100) + '%');
        card.style.setProperty('--my', (y * 100) + '%');
        if (card.classList.contains('tilt')) {
          card.style.transform = 'perspective(900px) rotateX(' + ((0.5 - y) * 6) + 'deg) rotateY(' + ((x - 0.5) * 8) + 'deg) translateY(-4px)';
        }
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }

  // Parallax on hero image
  var heroImg = document.querySelector('.hero .hero-media');
  if (heroImg && !reduce) {
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      if (y < window.innerHeight) heroImg.style.transform = 'translateY(' + (y * 0.3) + 'px)';
    }, { passive: true });
  }

  // Range inputs: paint the filled track
  function paintRange(r) {
    var pct = ((r.value - r.min) / (r.max - r.min)) * 100;
    r.style.setProperty('--pct', pct + '%');
  }
  document.querySelectorAll('input[type=range]').forEach(function (r) {
    paintRange(r);
    r.addEventListener('input', function () { paintRange(r); });
  });
  IAS.paintRange = paintRange;

  // Toast + copy promo code
  var toast = document.querySelector('.toast');
  IAS.toast = function (msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(IAS._t);
    IAS._t = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  };
  document.querySelectorAll('[data-copy]').forEach(function (el) {
    el.setAttribute('title', 'Click to copy');
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
    function copy() {
      var text = el.getAttribute('data-copy');
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { IAS.toast('Promo code "' + text + '" copied - 20% off'); });
      else IAS.toast('Promo code: ' + text);
    }
    el.addEventListener('click', copy);
    el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); copy(); } });
  });

  // Tabbed bar chart: <div data-chart='{"tabs": {...}}'>
  document.querySelectorAll('[data-chart]').forEach(function (wrap) {
    var data = JSON.parse(wrap.getAttribute('data-chart'));
    var tabsEl = wrap.querySelector('.tabs');
    var chart = wrap.querySelector('.bar-chart');
    var note = wrap.querySelector('.chart-note');
    var keys = Object.keys(data);
    var max = 0;
    keys.forEach(function (k) { data[k].rows.forEach(function (r) { max = Math.max(max, r[2]); }); });
    max = Math.ceil(max / 10000) * 10000;
    function render(k) {
      var set = data[k];
      chart.innerHTML = set.rows.map(function (r) {
        return '<div class="bar-row"><span class="name">' + r[0] + '</span><span class="track"><span class="fill" style="left:0;width:0" data-l="' + (r[1] / max * 100) + '" data-w="' + ((r[2] - r[1]) / max * 100) + '"></span></span><span class="amt">' + IAS.money(r[1], true) + '-' + IAS.money(r[2], true).slice(1) + '</span></div>';
      }).join('');
      if (note) note.textContent = set.note || '';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          chart.querySelectorAll('.fill').forEach(function (f) { f.style.left = f.getAttribute('data-l') + '%'; f.style.width = f.getAttribute('data-w') + '%'; });
        });
      });
      tabsEl.querySelectorAll('.tab').forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-key') === k ? 'true' : 'false'); });
    }
    tabsEl.innerHTML = keys.map(function (k) { return '<button class="tab" role="tab" type="button" data-key="' + k + '">' + data[k].label + '</button>'; }).join('');
    tabsEl.addEventListener('click', function (e) { var b = e.target.closest('.tab'); if (b) render(b.getAttribute('data-key')); });
    var started = false;
    if (io) {
      var cio = new IntersectionObserver(function (en) { if (en[0].isIntersecting && !started) { started = true; render(keys[0]); cio.disconnect(); } }, { threshold: 0.2 });
      cio.observe(wrap);
    } else render(keys[0]);
  });

  // Blog category filter
  var filter = document.querySelector('.filter-bar');
  if (filter) {
    filter.addEventListener('click', function (e) {
      var b = e.target.closest('.tab');
      if (!b) return;
      var cat = b.getAttribute('data-cat');
      filter.querySelectorAll('.tab').forEach(function (t) { t.setAttribute('aria-selected', t === b ? 'true' : 'false'); });
      document.querySelectorAll('.post-grid .post-card').forEach(function (c) {
        c.classList.toggle('hide', cat !== 'all' && c.getAttribute('data-cat') !== cat);
      });
    });
  }

  // Article TOC highlighting
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && io) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('active'); });
          var a = map[en.target.id];
          if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }
})();
