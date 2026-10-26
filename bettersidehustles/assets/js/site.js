/* Better Side Hustles — navigation, scroll effects and the money-themed
   visuals (floating coins, earnings ticker, coin bursts). Every animation
   is skipped when the visitor prefers reduced motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BSH = window.BSH = {};

  /* ----------------------------------------------------------- navigation */
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open);
    });
  }
  document.querySelectorAll('.menu-btn').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = b.parentNode, open = !li.classList.contains('open');
      document.querySelectorAll('.has-menu.open').forEach(function (x) { x.classList.remove('open'); });
      li.classList.toggle('open', open);
      b.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-menu')) document.querySelectorAll('.has-menu.open').forEach(function (x) { x.classList.remove('open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.body.classList.remove('nav-open');
      document.querySelectorAll('.has-menu.open').forEach(function (x) { x.classList.remove('open'); });
    }
  });

  var toTop = document.querySelector('.to-top');
  var progress = document.querySelector('.read-progress span');
  var article = document.querySelector('.article-body');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (toTop) toTop.classList.toggle('show', y > 900);
    if (progress && article) {
      var r = article.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, -r.top / (r.height - window.innerHeight)));
      progress.style.transform = 'scaleX(' + p + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* ------------------------------------------------- reveal + count up */
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      if (en.target.hasAttribute('data-countup')) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }) : null;
  document.querySelectorAll('.reveal, [data-countup]').forEach(function (el) {
    if (io && !reduce) io.observe(el); else { el.classList.add('in'); }
  });

  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-countup'));
    var pre = el.getAttribute('data-prefix') || '', suf = el.getAttribute('data-suffix') || '';
    if (reduce) { el.textContent = pre + end.toLocaleString() + suf; return; }
    var t0 = null, dur = 1400;
    function step(t) {
      t0 = t0 || t;
      var k = Math.min(1, (t - t0) / dur), ease = 1 - Math.pow(1 - k, 3);
      el.textContent = pre + Math.round(end * ease).toLocaleString() + suf;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ------------------------------------------------ TOC active section */
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && io) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove('active'); });
          map[en.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-15% 0px -75% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* --------------------------------------------- floating coins canvas */
  function coinField(canvas) {
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    var density = parseFloat(canvas.getAttribute('data-density') || '1');
    var items = [], w, h, running = false, raf;
    function resize() {
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(46, w * h / 26000) * density);
      items = [];
      for (var i = 0; i < n; i++) items.push(spawn(true));
    }
    function spawn(anywhere) {
      var kind = Math.random();
      return {
        x: Math.random() * w, y: anywhere ? Math.random() * h : h + 40,
        r: 7 + Math.random() * 13, vy: 0.25 + Math.random() * 0.6, vx: (Math.random() - 0.5) * 0.25,
        rot: Math.random() * Math.PI * 2, vr: (Math.random() - 0.5) * 0.02, flip: Math.random() * Math.PI * 2,
        kind: kind < 0.62 ? 'coin' : kind < 0.85 ? 'bill' : 'spark', a: 0.35 + Math.random() * 0.5
      };
    }
    function drawCoin(p) {
      var sx = Math.abs(Math.cos(p.flip)) * 0.85 + 0.15;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.scale(sx, 1); ctx.globalAlpha = p.a;
      var g = ctx.createRadialGradient(-p.r * 0.3, -p.r * 0.3, p.r * 0.1, 0, 0, p.r);
      g.addColorStop(0, '#fff6c2'); g.addColorStop(0.55, '#f4c84a'); g.addColorStop(1, '#c8901a');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, p.r, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = 'rgba(140,90,10,.55)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(0, 0, p.r * 0.74, 0, Math.PI * 2); ctx.stroke();
      if (sx > 0.45) {
        ctx.fillStyle = 'rgba(120,75,5,.75)'; ctx.font = '700 ' + (p.r * 1.05) + 'px "Source Sans 3", sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('$', 0, p.r * 0.05);
      }
      ctx.restore();
    }
    function drawBill(p) {
      var bw = p.r * 2.6, bh = p.r * 1.3, sk = Math.cos(p.flip) * 0.35;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.transform(1, sk * 0.3, 0, 1, 0, 0); ctx.globalAlpha = p.a * 0.9;
      ctx.fillStyle = '#7ED957'; roundRect(-bw / 2, -bh / 2, bw, bh, 3); ctx.fill();
      ctx.strokeStyle = 'rgba(20,90,30,.55)'; ctx.lineWidth = 1; roundRect(-bw / 2 + 3, -bh / 2 + 3, bw - 6, bh - 6, 2); ctx.stroke();
      ctx.fillStyle = 'rgba(20,90,30,.7)'; ctx.beginPath(); ctx.arc(0, 0, bh * 0.28, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    }
    function drawSpark(p) {
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.globalAlpha = p.a * (0.5 + 0.5 * Math.sin(p.flip * 3));
      ctx.fillStyle = '#ffffff'; var s = p.r * 0.45;
      ctx.beginPath(); ctx.moveTo(0, -s); ctx.lineTo(s * 0.25, -s * 0.25); ctx.lineTo(s, 0); ctx.lineTo(s * 0.25, s * 0.25);
      ctx.lineTo(0, s); ctx.lineTo(-s * 0.25, s * 0.25); ctx.lineTo(-s, 0); ctx.lineTo(-s * 0.25, -s * 0.25); ctx.closePath(); ctx.fill();
      ctx.restore();
    }
    function roundRect(x, y, w2, h2, r) {
      ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w2, y, x + w2, y + h2, r); ctx.arcTo(x + w2, y + h2, x, y + h2, r);
      ctx.arcTo(x, y + h2, x, y, r); ctx.arcTo(x, y, x + w2, y, r); ctx.closePath();
    }
    function frame() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < items.length; i++) {
        var p = items[i];
        p.y -= p.vy; p.x += p.vx + Math.sin(p.flip) * 0.15; p.rot += p.vr; p.flip += 0.02 + p.vy * 0.02;
        if (p.y < -40) items[i] = spawn(false);
        if (p.kind === 'coin') drawCoin(p); else if (p.kind === 'bill') drawBill(p); else drawSpark(p);
      }
      if (running) raf = requestAnimationFrame(frame);
    }
    resize();
    window.addEventListener('resize', function () { clearTimeout(canvas._t); canvas._t = setTimeout(resize, 200); });
    if (reduce) { frame(); return; }
    new IntersectionObserver(function (en) {
      running = en[0].isIntersecting;
      cancelAnimationFrame(raf);
      if (running) raf = requestAnimationFrame(frame);
    }).observe(canvas);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { running = false; cancelAnimationFrame(raf); }
    });
  }
  document.querySelectorAll('.coin-canvas').forEach(coinField);

  /* ------------------------------------------------------- coin burst */
  BSH.coinBurst = function (anchor) {
    if (reduce || !anchor) return;
    var r = anchor.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + Math.min(r.height, 60) / 2;
    for (var i = 0; i < 14; i++) {
      var c = document.createElement('span');
      c.className = 'burst-coin';
      c.textContent = '$';
      var ang = Math.random() * Math.PI * 2, dist = 50 + Math.random() * 90;
      c.style.left = cx + 'px'; c.style.top = cy + 'px';
      c.style.setProperty('--dx', Math.cos(ang) * dist + 'px');
      c.style.setProperty('--dy', (Math.sin(ang) * dist - 40) + 'px');
      c.style.setProperty('--rot', (Math.random() * 720 - 360) + 'deg');
      document.body.appendChild(c);
      setTimeout(c.remove.bind(c), 1100);
    }
  };

  /* ------------------------------------------------ earnings ticker */
  var ticker = document.querySelector('.earn-feed');
  if (ticker) {
    var feed = [
      ['Fiverr', 'Logo design order', 85], ['DoorDash', 'Dinner rush · 4 orders', 46.5], ['Udemy', 'Course sale', 12.4],
      ['Rover', 'Dog walk · 30 min', 22], ['Uber', 'Airport ride', 38.75], ['Shopify', 'Print-on-demand tee', 14.2],
      ['Semrush', 'Affiliate commission', 200], ['TaskRabbit', 'Furniture assembly', 70], ['Skillshare', 'Monthly royalties', 63.1],
      ['Instacart', 'Grocery batch', 31], ['Etsy', 'Digital planner sale', 9.5], ['Upwork', 'Copywriting milestone', 150]
    ];
    var total = ticker.closest('.phone').querySelector('[data-total]');
    var sum = 0, k = 0;
    function push() {
      var f = feed[k++ % feed.length];
      sum += f[2];
      var li = document.createElement('li');
      li.innerHTML = '<span class="app">' + f[0].charAt(0) + '</span><span class="what"><b>' + f[0] + '</b><small>' + f[1] + '</small></span><span class="amt">+$' + f[2].toFixed(2) + '</span>';
      ticker.insertBefore(li, ticker.firstChild);
      while (ticker.children.length > 4) ticker.removeChild(ticker.lastChild);
      if (total) total.textContent = '$' + sum.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    for (var n = 0; n < 3; n++) push();
    if (!reduce) setInterval(push, 2600);
  }

  /* -------------------------------------- spotlight glow on cards */
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.addEventListener('pointermove', function (e) {
      var c = e.target.closest && e.target.closest('.glow');
      if (!c) return;
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  }

  /* ----------------------------------------------- blog filter + search */
  var grid = document.querySelector('[data-filter-grid]');
  if (grid) {
    var cards = grid.querySelectorAll('.post-card');
    var q = document.querySelector('[data-filter-search]');
    var chips = document.querySelectorAll('[data-filter-cat]');
    var empty = document.querySelector('[data-filter-empty]');
    var count = document.querySelector('[data-filter-count]');
    var params = new URLSearchParams(location.search);
    var cat = params.get('cat') || 'all';
    if (q && params.get('q')) q.value = params.get('q');
    function apply() {
      var term = q ? q.value.trim().toLowerCase() : '';
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.getAttribute('data-cat') === cat) && (!term || c.getAttribute('data-title').indexOf(term) > -1);
        c.hidden = !ok; if (ok) shown++;
      });
      chips.forEach(function (ch) { ch.classList.toggle('active', ch.getAttribute('data-filter-cat') === cat); });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = shown;
      var u = new URL(location.href);
      cat === 'all' ? u.searchParams.delete('cat') : u.searchParams.set('cat', cat);
      term ? u.searchParams.set('q', term) : u.searchParams.delete('q');
      history.replaceState(null, '', u);
    }
    chips.forEach(function (ch) { ch.addEventListener('click', function () { cat = ch.getAttribute('data-filter-cat'); apply(); }); });
    if (q) q.addEventListener('input', apply);
    apply();
  }

  /* ---------------------------------------- city finder (home page) */
  var finder = document.querySelector('[data-city-finder]');
  if (finder) {
    var input = finder.querySelector('input');
    var list = finder.querySelector('ul');
    var cities = JSON.parse(finder.getAttribute('data-cities'));
    function render(term) {
      term = term.trim().toLowerCase();
      var hits = cities.filter(function (c) { return !term || c[0].toLowerCase().indexOf(term) > -1 || c[1].toLowerCase() === term; }).slice(0, term ? 8 : 0);
      list.innerHTML = hits.map(function (c) { return '<li><a href="' + c[2] + '"><span>' + c[0] + '</span><small>' + c[1] + '</small></a></li>'; }).join('') ||
        (term ? '<li class="none">No guide for that city yet — <a href="/blog/?cat=city-guides">see all city guides</a></li>' : '');
    }
    input.addEventListener('input', function () { render(input.value); });
    finder.addEventListener('submit', function (e) {
      e.preventDefault();
      var a = list.querySelector('a');
      if (a) location.href = a.href;
    });
  }
})();
