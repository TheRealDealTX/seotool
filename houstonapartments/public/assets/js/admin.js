/* Houston Apartments admin — small helpers for the forms */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var csrf = document.body.getAttribute('data-csrf');

  /* ---------- photos: drag to reorder, arrows, remove ---------- */
  var box = $('[data-photos]'), keep = $('input[name=photos_keep]');
  function syncPhotos() { if (keep) keep.value = JSON.stringify($$('.ph', box).map(function (f) { return f.getAttribute('data-path'); })); }
  if (box) {
    var drag = null;
    box.addEventListener('dragstart', function (e) { drag = e.target.closest('.ph'); if (drag) drag.classList.add('dragging'); });
    box.addEventListener('dragend', function () { if (drag) drag.classList.remove('dragging'); drag = null; syncPhotos(); dirty = true; });
    box.addEventListener('dragover', function (e) {
      e.preventDefault();
      var over = e.target.closest('.ph');
      if (!drag || !over || over === drag) return;
      var r = over.getBoundingClientRect();
      box.insertBefore(drag, (e.clientX - r.left) > r.width / 2 ? over.nextSibling : over);
    });
    box.addEventListener('click', function (e) {
      var f = e.target.closest('.ph'); if (!f) return;
      if (e.target.closest('[data-remove]')) { if (confirm('Remove this photo?')) f.remove(); }
      var mv = e.target.closest('[data-move]');
      if (mv) { var d = +mv.getAttribute('data-move'); if (d < 0 && f.previousElementSibling) box.insertBefore(f, f.previousElementSibling); if (d > 0 && f.nextElementSibling) box.insertBefore(f.nextElementSibling, f); }
      syncPhotos(); dirty = true;
    });
    syncPhotos();
  }
  var newIn = $('[data-new-photos]'), prev = $('[data-new-preview]');
  if (newIn) {
    var drop = newIn.closest('.drop');
    ['dragenter', 'dragover'].forEach(function (ev) { drop.addEventListener(ev, function () { drop.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function () { drop.classList.remove('over'); }); });
    newIn.addEventListener('change', function () {
      prev.innerHTML = '';
      Array.prototype.forEach.call(newIn.files, function (file) {
        var fig = document.createElement('figure'); fig.className = 'ph';
        var img = document.createElement('img'); img.src = URL.createObjectURL(file); fig.appendChild(img); prev.appendChild(fig);
      });
    });
  }

  /* ---------- repeaters (floor plans, FAQs) ---------- */
  $$('[data-add]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var name = btn.getAttribute('data-add'), tpl = $('template[data-template="' + name + '"]'), list = $('[data-repeater="' + name + '"]');
      var i = 'n' + Date.now();
      var wrap = document.createElement('div'); wrap.innerHTML = tpl.innerHTML.replace(/__i__/g, i);
      var row = wrap.firstElementChild; list.appendChild(row);
      var first = row.querySelector('input:not([type=file]), select, textarea'); if (first) first.focus();
    });
  });
  document.addEventListener('click', function (e) { var b = e.target.closest('[data-remove-row]'); if (b) b.parentNode.remove(); });

  /* ---------- map pin ---------- */
  var pm = $('#pin-map');
  if (pm && window.L) {
    var lat = $('input[name=lat]'), lng = $('input[name=lng]');
    var has = lat.value && lng.value;
    var map = L.map(pm, { scrollWheelZoom: false }).setView(has ? [+lat.value, +lng.value] : [29.7604, -95.3698], has ? 15 : 10);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '&copy; OpenStreetMap' }).addTo(map);
    var marker = null;
    var place = function (ll, zoom) {
      if (!marker) { marker = L.marker(ll, { draggable: true }).addTo(map); marker.on('dragend', function () { set(marker.getLatLng()); }); }
      marker.setLatLng(ll); set(L.latLng(ll)); if (zoom) map.setView(ll, 16);
    };
    var set = function (ll) { lat.value = ll.lat.toFixed(6); lng.value = ll.lng.toFixed(6); dirty = true; };
    if (has) place([+lat.value, +lng.value]);
    map.on('click', function (e) { place(e.latlng); });
    $('[data-find]').addEventListener('click', function () {
      var q = ['street', 'city'].map(function (n) { return $('input[name=' + n + ']').value; }).join(', ') + ', TX ' + $('input[name=zip]').value;
      var b = this; b.disabled = true; b.textContent = 'Searching…';
      fetch('/admin/geocode/?q=' + encodeURIComponent(q)).then(function (r) { return r.json(); }).then(function (j) {
        if (j.lat) place([j.lat, j.lng], true); else alert('We couldn’t find that address. Click the map to drop the pin yourself.');
      }).finally(function () { b.disabled = false; b.textContent = '📍 Find address on map'; });
    });
    // addresses changed after a pin exists: clear it so the server re-geocodes unless the user re-places it
    $$('[data-addr]').forEach(function (i) { i.addEventListener('change', function () { if (marker && !confirm('Address changed. Keep the current map pin?')) { map.removeLayer(marker); marker = null; lat.value = ''; lng.value = ''; } }); });
  }

  /* ---------- unsaved changes warning ---------- */
  var dirty = false, form = $('[data-dirty-check]');
  if (form) {
    form.addEventListener('input', function () { dirty = true; });
    form.addEventListener('submit', function () { dirty = false; syncPhotos(); var b = $('.save-bar .primary'); b.disabled = true; b.textContent = 'Saving…'; });
    window.addEventListener('beforeunload', function (e) { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
  }

  /* ---------- leads autosave ---------- */
  $$('[data-autosave]').forEach(function (f) {
    var t, save = function () {
      var fd = new FormData(f); fd.append('ajax', '1');
      fetch(f.action, { method: 'POST', body: fd }).then(function (r) { return r.json(); }).then(function () {
        var s = $('.saved', f); s.hidden = false; setTimeout(function () { s.hidden = true; }, 1500);
        var sel = $('select', f); sel.className = 's-' + sel.value;
      });
    };
    $('select', f).addEventListener('change', save);
    $('textarea', f).addEventListener('input', function () { clearTimeout(t); t = setTimeout(save, 700); });
  });

  /* ---------- Rise import ---------- */
  var log = $('#import-log');
  function say(msg) { if (log.textContent === 'Nothing running.') log.textContent = ''; log.textContent += msg + '\n'; log.scrollTop = log.scrollHeight; }
  function post(data) {
    var fd = new FormData(); fd.append('_csrf', csrf); Object.keys(data).forEach(function (k) { fd.append(k, data[k]); });
    return fetch('/admin/import/run/', { method: 'POST', body: fd }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); });
  }
  var listBtn = $('[data-import-list]');
  if (listBtn) {
    listBtn.addEventListener('click', function () {
      var items = $('#import-list').value.split(/\s+/).filter(Boolean), force = $('#import-force').checked ? 1 : '';
      if (!items.length) return;
      listBtn.disabled = true;
      (function next(i) {
        if (i >= items.length) { say('Done.'); listBtn.disabled = false; return; }
        say('Importing ' + items[i] + ' …');
        post({ slug: items[i], force: force }).then(function (j) { j.log.forEach(say); }).catch(function (e) { say('  failed: ' + e.message); }).then(function () { next(i + 1); });
      })(0);
    });
  }
  var syncBtn = $('[data-sync]'), stopBtn = $('[data-sync-stop]'), stop = false;
  if (syncBtn) {
    stopBtn.addEventListener('click', function () { stop = true; say('Stopping after this batch…'); });
    syncBtn.addEventListener('click', function () {
      stop = false; syncBtn.disabled = true; stopBtn.hidden = false; var total = 0;
      (function batch() {
        post({}).then(function (j) {
          j.log.forEach(say); total += j.imported;
          if (j.complete || stop) { say('Finished. Imported ' + total + ' listing(s).'); syncBtn.disabled = false; stopBtn.hidden = true; return; }
          batch();
        }).catch(function (e) { say('Batch failed (' + e.message + '), retrying in 10 s…'); if (!stop) setTimeout(batch, 10000); else { syncBtn.disabled = false; stopBtn.hidden = true; } });
      })();
    });
  }
})();
