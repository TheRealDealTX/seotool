/* galvestonpublicadjuster.com — nav, lead popup, forms, reveal animations, calculators */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };

  // Mobile nav
  var toggle = $('.nav-toggle'), nav = $('#nav');
  if (toggle && nav) toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Lead popup: appears after 5 seconds on the site, once per browser session.
  var modal = $('#lead-modal');
  function openModal() {
    if (!modal || !modal.hidden) return;
    modal.hidden = false;
    store.set('gpa-popup', '1');
    var first = $('input[name=name]', modal); if (first) setTimeout(function () { first.focus(); }, 50);
  }
  function closeModal() { if (modal) modal.hidden = true; }
  if (modal) {
    $$('[data-close]', modal).forEach(function (b) { b.addEventListener('click', closeModal); });
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
    var skip = /^\/(contact|thank-you)\//.test(location.pathname);
    if (!skip && !store.get('gpa-popup')) setTimeout(openModal, 5000);
    $$('[data-open-popup]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); openModal(); }); });
  }

  // Lead forms: submit with fetch, fall back to a normal POST.
  $$('form[data-lead]').forEach(function (form) {
    var page = $('input[name=page]', form); if (page) page.value = location.href;
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var btn = $('button[type=submit]', form), status = $('.form-status', form);
      btn.disabled = true; status.className = 'form-status'; status.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          status.textContent = d.message; status.className = 'form-status ' + (d.ok ? 'ok' : 'err');
          if (d.ok) { form.reset(); store.set('gpa-popup', '1'); if (window.gtag) gtag('event', 'generate_lead'); }
          btn.disabled = false;
        })
        .catch(function () { form.submit(); });
    });
  });

  // Reveal + animated bars
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      $$('.bar-fill[data-w]', en.target).forEach(function (b) { b.style.width = b.getAttribute('data-w') + '%'; });
      io.unobserve(en.target);
    });
  }, { threshold: .15 }) : null;
  $$('.reveal, .bars').forEach(function (el) {
    if (io) io.observe(el); else { el.classList.add('in'); $$('.bar-fill[data-w]', el).forEach(function (b) { b.style.width = b.getAttribute('data-w') + '%'; }); }
  });

  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };

  /* ---------- Calculator 1: shingle wind damage ---------- */
  var sc = $('#shingle-calc');
  if (sc) {
    var el = function (id) { return $('#' + id, sc); };
    var svgNS = 'http://www.w3.org/2000/svg';
    var roof = el('roof-shingles');
    // Build shingle grid once (7 courses on a gable roof plane, trapezoid).
    var shingles = [];
    var seed = 7; var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
    for (var row = 0; row < 7; row++) {
      var y = 96 + row * 26, inset = 150 - row * 20, w = 44;
      var x0 = 70 + inset, x1 = 630 - inset;
      var off = row % 2 ? w / 2 : 0;
      for (var x = x0 - off; x < x1; x += w) {
        var xx = Math.max(x, x0), ww = Math.min(x + w, x1) - xx;
        if (ww < 8) continue;
        var r = document.createElementNS(svgNS, 'rect');
        r.setAttribute('x', xx + 1); r.setAttribute('y', y); r.setAttribute('width', ww - 2); r.setAttribute('height', 27); r.setAttribute('rx', 2);
        r.setAttribute('class', 'shingle');
        var edge = (row === 0 || xx === x0 || x + w >= x1) ? 1 : 0; // ridge/rake/eave edges fail first
        r.dataset.v = (rnd() * 0.75 + edge * 0.3).toFixed(3);
        r.setAttribute('fill', ['#3b4656', '#344050', '#414d5e', '#2f3a48'][Math.floor(rnd() * 4)]);
        roof.appendChild(r); shingles.push(r);
      }
    }
    shingles.sort(function (a, b) { return b.dataset.v - a.dataset.v; });

    var LEVELS = [
      { max: .6, name: 'Minimal', cls: '', text: 'Winds are well under what this roof is rated for. Damage is unlikely unless shingles were already loose or improperly nailed.' },
      { max: .8, name: 'Low', cls: 'warn', text: 'Expect stress on seal strips at ridges, rakes and corners. A few tabs may unseal or flutter — damage that is easy to miss from the ground.' },
      { max: 1, name: 'Moderate', cls: 'bad', text: 'Creased and unsealed shingles are likely in edge and corner zones. Creased shingles have lost their wind resistance and are a covered windstorm loss — insurers often miss them.' },
      { max: 1.25, name: 'High', cls: 'severe', text: 'Winds exceed the effective rating. Missing shingles along ridges, rakes and eaves, exposed underlayment and leaks are likely. Photograph everything before tarping.' },
      { max: 99, name: 'Severe', cls: 'severe', text: 'Widespread shingle loss and possible decking exposure and interior water damage. This is hurricane-level loss — document, mitigate, and get the claim reviewed before accepting any offer.' }
    ];

    var update = function () {
      var wind = +el('wind').value, rating = +el('rating').value, age = +el('age').value;
      var exp = +el('exposure').value, nails = +el('nails').value;
      el('wind-out').value = wind + ' mph';
      el('age-out').value = age + ' yrs';
      var ageF = age < 5 ? 1 : age < 10 ? .9 : age < 15 ? .8 : age < 20 ? .7 : .6;
      var effRating = rating * ageF * nails;
      var effWind = wind * exp;
      var ratio = effWind / effRating;
      var lvl = LEVELS.filter(function (l) { return ratio < l.max; })[0];
      var pct = Math.max(0, Math.min(85, 100 / (1 + Math.exp(-7 * (ratio - 1.2)))));
      if (ratio < .6) pct = 0;
      var q = 0.00256 * effWind * effWind; // velocity pressure, psf
      el('r-eff').textContent = Math.round(effRating) + ' mph';
      el('r-psf').textContent = q.toFixed(1) + ' psf';
      el('r-pull').textContent = Math.round(q * 1.54) + ' lb';
      el('r-pct').textContent = pct < 1 ? '<1%' : Math.round(pct) + '%';
      el('r-level').textContent = lvl.name;
      el('meter').style.left = Math.min(100, ratio / 1.5 * 100) + '%';
      var v = el('verdict'); v.className = 'verdict ' + lvl.cls;
      v.innerHTML = '<strong>' + lvl.name + ' damage risk.</strong> ' + lvl.text;
      el('svg-wind').textContent = wind + ' MPH';
      // Animate shingles: lift (creased) then blow off.
      var n = shingles.length, lost = Math.round(n * pct / 100), lifted = Math.round(n * Math.min(1, ratio > .7 ? (ratio - .7) * 1.4 : 0));
      shingles.forEach(function (s, i) {
        if (i < lost) { s.style.transform = 'translate(' + (40 + i % 5 * 30) + 'px,-' + (30 + i % 7 * 12) + 'px) rotate(' + (25 + i % 4 * 20) + 'deg)'; s.style.opacity = 0; }
        else if (i < lost + lifted) { s.style.transform = 'rotateX(0) skewX(-8deg) scaleY(.82)'; s.style.opacity = 1; s.setAttribute('stroke', '#f97316'); }
        else { s.style.transform = ''; s.style.opacity = 1; s.removeAttribute('stroke'); }
      });
      $$('.gust', sc).forEach(function (g, i) { g.style.animationDuration = Math.max(.5, 2.6 - wind / 80) + 's'; g.style.display = i < Math.ceil(wind / 30) ? '' : 'none'; });
      var mk = el('scale-marker'); mk.setAttribute('x', 70 + Math.min(180, wind) / 180 * 560 - 2);
    };
    $$('input, select', sc).forEach(function (i) { i.addEventListener('input', update); });
    update();
  }

  /* ---------- Calculator 2: claim payout & deductible ---------- */
  var cc = $('#claim-calc');
  if (cc) {
    var g = function (id) { return $('#' + id, cc); };
    var calc = function () {
      var cov = +g('coverage').value || 0, dedPct = +g('ded').value, damage = +g('damage').value || 0, offer = +g('offer').value || 0, fee = +g('fee').value / 100;
      var ded = dedPct < 1 ? cov * dedPct : dedPct; // <1 means % of Coverage A, else flat $
      var netOffer = Math.max(0, offer - ded);
      var fullNet = Math.max(0, Math.min(damage, cov) - ded);
      var paFee = fullNet * fee; // conservative: fee on the entire payment, not just the increase
      var paNet = Math.max(0, fullNet - paFee);
      var gap = Math.max(0, paNet - netOffer);
      g('o-ded').textContent = money(ded);
      g('o-offer').textContent = money(netOffer);
      g('o-full').textContent = money(fullNet);
      g('o-pa').textContent = money(paNet);
      g('o-gap').textContent = (gap > 0 ? '+' : '') + money(gap);
      var max = Math.max(netOffer, fullNet, 1);
      g('b-offer').style.width = netOffer / max * 100 + '%';
      g('b-full').style.width = fullNet / max * 100 + '%';
      g('b-pa').style.width = paNet / max * 100 + '%';
      g('b-offer-v').textContent = money(netOffer); g('b-full-v').textContent = money(fullNet); g('b-pa-v').textContent = money(paNet);
      g('o-under').textContent = damage > 0 ? Math.max(0, Math.round((1 - Math.min(offer, damage) / damage) * 100)) + '%' : '—';
      var msg = g('o-msg');
      if (gap > 0) { msg.className = 'verdict bad'; msg.innerHTML = '<strong>Your offer may be ' + money(gap) + ' short of what you would net with representation.</strong> That is after our fee and your deductible. Call ' + '<a href="tel:+18325035866">(832) 503-5866</a> for an expert consultation before you sign anything.'; }
      else { msg.className = 'verdict'; msg.innerHTML = '<strong>The offer looks close to the documented damage.</strong> Make sure the estimate includes code upgrades, overhead &amp; profit, and hidden damage before accepting.'; }
    };
    $$('input, select', cc).forEach(function (i) { i.addEventListener('input', calc); });
    calc();
  }
})();
