(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var LISTINGS = window.WCA_LISTINGS || [];
  window.WCA = { $: $, $$: $$, money: money, store: store };

  /* nav */
  var tog = $('.nav-toggle'), nav = $('#nav');
  if (tog) tog.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); tog.setAttribute('aria-expanded', o);
    document.body.classList.toggle('nav-open', o);
  });
  $$('.sub-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
      var d = b.closest('.dropdown'), o = d.classList.toggle('open');
      b.setAttribute('aria-expanded', o); b.textContent = o ? '▴' : '▾';
    });
  });

  /* favorites */
  function favs() { return store.get('wca_favs', []); }
  function paintFavs() {
    var f = favs();
    $$('[data-fav]').forEach(function (b) { b.setAttribute('aria-pressed', f.indexOf(+b.dataset.fav) > -1); });
    $$('.fav-count').forEach(function (c) { c.textContent = f.length; c.hidden = !f.length; });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-fav]'); if (!b) return;
    e.preventDefault();
    var id = +b.dataset.fav, f = favs(), i = f.indexOf(id);
    if (i > -1) f.splice(i, 1); else f.push(id);
    store.set('wca_favs', f); paintFavs(); renderFavorites();
  });
  paintFavs();

  /* compare */
  function cmp() { return store.get('wca_cmp', []); }
  function paintCompare() {
    var c = cmp();
    $$('[data-compare]').forEach(function (x) { x.checked = c.indexOf(+x.dataset.compare) > -1; });
    var bar = $('[data-compare-bar]');
    if (bar) {
      bar.hidden = c.length === 0;
      $('[data-compare-count]', bar).textContent = c.length;
      $('[data-compare-go]', bar).href = '/compare/?ids=' + c.join(',');
    }
  }
  document.addEventListener('change', function (e) {
    var x = e.target.closest('[data-compare]'); if (!x) return;
    var id = +x.dataset.compare, c = cmp(), i = c.indexOf(id);
    if (x.checked && i < 0) { if (c.length >= 3) { c.shift(); } c.push(id); }
    if (!x.checked && i > -1) c.splice(i, 1);
    store.set('wca_cmp', c); paintCompare();
  });
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-compare-clear]')) { store.set('wca_cmp', []); paintCompare(); }
  });
  paintCompare();

  var picker = $('[data-compare-picker]');
  if (picker) picker.addEventListener('submit', function () {
    var ids = $$('select', picker).map(function (s) { return s.value; }).filter(Boolean);
    picker.querySelector('[name=ids]').value = ids.join(',');
    $$('select', picker).forEach(function (s) { s.disabled = true; });
    store.set('wca_cmp', ids.map(Number));
  });

  function cardHTML(l, extra) {
    return '<article class="card listing-card">' + (extra || '') +
      '<a class="card-img" href="' + l.url + '"><img src="' + l.img + '" alt="" loading="lazy" width="640" height="427"></a>' +
      '<button class="fav-btn" type="button" data-fav="' + l.id + '" aria-label="Save">♥</button>' +
      '<div class="card-body"><h3><a href="' + l.url + '">' + esc(l.name) + '</a></h3><p class="muted addr">' + esc(l.address) + '</p>' +
      '<p class="price">' + esc(l.rent) + '</p><ul class="chips"><li>' + esc(l.beds) + '</li><li>' + esc(l.petsLabel) + '</li></ul></div></article>';
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  window.WCA.cardHTML = cardHTML; window.WCA.esc = esc;

  function renderFavorites() {
    var box = $('[data-favorites]'); if (!box) return;
    var f = favs(), items = LISTINGS.filter(function (l) { return f.indexOf(l.id) > -1; });
    if (!items.length) { box.innerHTML = '<p class="muted">Tap the ♥ on any listing to save it here. Favorites are stored only in this browser.</p>'; return; }
    box.innerHTML = items.map(function (l) { return cardHTML(l); }).join('');
    paintFavs();
  }
  renderFavorites();

  /* directory filters */
  var dir = $('[data-directory]');
  if (dir) {
    var cards = $$('.listing-card', dir), grid = $('[data-grid]', dir), state = {};
    cards.forEach(function (c) { c._d = JSON.parse(c.dataset.json); });
    var qs = new URLSearchParams(location.search);
    var f = function (k) { return $('[data-f="' + k + '"]', dir); };
    if (qs.get('q')) f('q').value = qs.get('q');
    if (qs.get('beds')) f('beds').value = qs.get('beds');
    if (qs.get('max')) f('max').value = qs.get('max');
    if (qs.get('pets')) f('pets').checked = true;
    var maxOut = $('[data-out="max"]', dir);

    function apply() {
      var q = f('q').value.trim().toLowerCase(), beds = f('beds').value, max = +f('max').value,
        pets = f('pets').checked, inc = f('income').checked, claimed = f('claimed').checked, type = f('type').value,
        ams = $$('[data-f="am"]:checked', dir).map(function (x) { return new RegExp(x.value, 'i'); });
      maxOut.textContent = max >= 3000 ? 'Any' : money(max);
      var n = 0, visible = [];
      cards.forEach(function (c) {
        var d = c._d, ok = true, hay = (d.name + ' ' + d.address + ' ' + d.amen.join(' ') + ' ' + d.type).toLowerCase();
        if (q && hay.indexOf(q) < 0) ok = false;
        if (beds !== '') {
          var b = +beds;
          if (d.bmin == null) ok = false;
          else if (b === 3 ? d.bmax < 3 : (d.bmin > b || d.bmax < b)) ok = false;
        }
        if (max < 3000 && (!d.rmin || d.rmin > max)) ok = false;
        if (pets && !d.pets) ok = false;
        if (inc && !d.income) ok = false;
        if (claimed && !d.claimed) ok = false;
        if (type && d.type !== type) ok = false;
        ams.forEach(function (re) { if (!re.test(d.amen.join(' '))) ok = false; });
        c.hidden = !ok; if (ok) { n++; visible.push(d); }
      });
      $('[data-count]', dir).textContent = n;
      $('[data-empty]', dir).hidden = n > 0;
      if (window._dirMap) drawMarkers(visible);
    }
    function sort() {
      var s = $('[data-sort]', dir).value;
      var arr = cards.slice();
      var r = function (d, hi) { return d.rmin || (hi ? -1 : 99999); };
      if (s === 'low') arr.sort(function (a, b) { return r(a._d) - r(b._d); });
      if (s === 'high') arr.sort(function (a, b) { return r(b._d, 1) - r(a._d, 1); });
      if (s === 'name') arr.sort(function (a, b) { return a._d.name.localeCompare(b._d.name); });
      if (s === 'new') arr.sort(function (a, b) { return (b._d.year || 0) - (a._d.year || 0); });
      arr.forEach(function (c) { grid.appendChild(c); });
    }
    dir.addEventListener('input', apply);
    dir.addEventListener('change', function (e) { if (e.target.matches('[data-sort]')) sort(); apply(); });
    $$('[data-reset]').forEach(function (b) { b.addEventListener('click', function () {
      $$('[data-f]', dir).forEach(function (x) { if (x.type === 'checkbox') x.checked = false; else if (x.type === 'range') x.value = x.max; else x.value = ''; });
      apply();
    }); });

    // map
    var markers = [];
    function drawMarkers(list) {
      markers.forEach(function (m) { m.remove(); }); markers = [];
      var b = [];
      list.forEach(function (d) {
        if (d.lat == null) return;
        var m = L.marker([d.lat, d.lng]).addTo(window._dirMap)
          .bindPopup('<div class="map-pop"><img src="' + d.img + '" width="200" height="133" alt=""><a href="' + d.url + '">' + esc(d.name) + '</a><br>' + esc(d.rent) + '<br>' + esc(d.beds) + '</div>');
        markers.push(m); b.push([d.lat, d.lng]);
      });
      if (b.length) window._dirMap.fitBounds(b, { padding: [30, 30], maxZoom: 15 });
    }
    function showMap() {
      var el = $('#map'); el.hidden = false;
      if (!window._dirMap && window.L) {
        window._dirMap = L.map(el, { scrollWheelZoom: false }).setView([39.66, -84.24], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(window._dirMap);
      }
      setTimeout(function () { window._dirMap && window._dirMap.invalidateSize(); apply(); }, 50);
    }
    $$('[data-view]', dir).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('[data-view]', dir).forEach(function (x) { x.classList.toggle('active', x === b); });
        if (b.dataset.view === 'map') showMap(); else $('#map').hidden = true;
      });
    });
    if (location.hash === '#map') { var mb = $('[data-view="map"]', dir); mb && mb.click(); }
    apply();
  }

  /* gallery */
  var gal = $('[data-gallery]');
  if (gal) {
    var main = $('[data-gallery-main]', gal);
    $$('.gallery-thumbs button', gal).forEach(function (b) {
      b.addEventListener('click', function () {
        main.src = b.dataset.src;
        $$('.gallery-thumbs button', gal).forEach(function (x) { x.classList.toggle('active', x === b); });
      });
    });
  }
  var share = $('[data-share]');
  if (share) share.addEventListener('click', function () {
    if (navigator.share) navigator.share({ title: document.title, url: location.href });
    else { navigator.clipboard && navigator.clipboard.writeText(location.href); share.textContent = '✓ Link copied'; }
  });

  /* single maps */
  function simpleMap(el, list, zoom) {
    if (!el || !window.L) return;
    var m = L.map(el, { scrollWheelZoom: false });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }).addTo(m);
    var b = [];
    list.forEach(function (d) {
      if (d.lat == null) return;
      L.marker([d.lat, d.lng]).addTo(m).bindPopup(d.url ? '<div class="map-pop"><a href="' + d.url + '">' + esc(d.name) + '</a><br>' + esc(d.rent || '') + '</div>' : esc(d.name));
      b.push([d.lat, d.lng]);
    });
    if (b.length === 1) m.setView(b[0], zoom || 15); else if (b.length) m.fitBounds(b, { padding: [30, 30] });
  }
  var lm = $('#listing-map');
  if (lm) simpleMap(lm, [{ lat: +lm.dataset.lat, lng: +lm.dataset.lng, name: lm.dataset.name }], 15);
  var gm = $('#guide-map');
  if (gm) simpleMap(gm, LISTINGS);

  /* listing cost calculator */
  var cc = $('[data-cost-calc]');
  if (cc) {
    var util = [110, 135, 165, 200], net = 60;
    var calc = function () {
      var g = function (k) { return +$('[data-c="' + k + '"]', cc).value || 0; };
      var o = function (k, v) { $('[data-o="' + k + '"]', cc).textContent = v; };
      var rent = g('rent'), u = util[g('beds')], pet = g('pets') * 35, ins = g('ins');
      var t = rent + u + net + pet + ins;
      o('rent', money(rent)); o('util', money(u)); o('net', money(net)); o('pet', money(pet)); o('ins', money(ins)); o('total', money(t) + '/mo');
      o('income', money(rent / 0.3 * 12));
    };
    cc.addEventListener('input', calc); calc();
  }

  /* home mini calculator */
  var mi = $('#mc-income');
  if (mi) {
    var mc = function () {
      var inc = +mi.value, rent = Math.round(inc * 0.3 / 10) * 10;
      $('#mc-out').innerHTML = money(inc) + ' → about <strong>' + money(rent) + '/mo</strong> in rent';
      var n = LISTINGS.filter(function (l) { return l.rmin && l.rmin <= rent; }).length;
      $('#mc-match').innerHTML = n ? n + ' West Carrollton communities advertise rents starting at or below that. <a href="/apartments/?max=' + rent + '">See them →</a>' : 'Try a higher income or explore <a href="/apartments/income-based/">income-based options</a>.';
    };
    mi.addEventListener('input', mc); mc();
  }

  /* submit form label */
  var sf = $('[data-submit-form]');
  if (sf) {
    var lbl = $('[data-submit-label]', sf);
    var upd = function () {
      var paid = (sf.querySelector('[name=plan]:checked') || {}).value === 'paid';
      lbl.textContent = paid ? 'Continue to payment & publish' : 'Submit free listing for review';
    };
    sf.addEventListener('change', upd); upd();
  }
})();
