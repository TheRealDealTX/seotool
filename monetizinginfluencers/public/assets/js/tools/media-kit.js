/* Media Kit Builder */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var form = $('mk-form');
  if (!form) return;
  var KEY = 'mi-media-kit-v1', defaults = {}, saveTimer;

  Array.prototype.forEach.call(form.elements, function (el) { if (el.name) defaults[el.name] = el.value; });

  function val(n) { return (form.elements[n].value || '').trim(); }
  function text(id, s) { $(id).textContent = s; }
  function li(label, value) {
    var l = document.createElement('li'), a = document.createElement('span'), b = document.createElement('b');
    a.textContent = label; b.textContent = value; l.appendChild(a); l.appendChild(b); return l;
  }

  function render() {
    var name = val('name') || 'Your Name';
    text('k-name', name);
    text('k-initials', name.split(/\s+/).map(function (w) { return w.charAt(0); }).join('').slice(0, 2).toUpperCase());
    text('k-handle', val('handle') || '@yourhandle');
    text('k-location', val('location') || 'Location');
    text('k-niche', val('niche') || 'Your niche');
    text('k-bio', val('bio') || 'A short bio about you and what your audience loves.');
    $('kit').style.setProperty('--accent', val('color') || '#8b5cf6');

    var stats = $('k-stats'); stats.innerHTML = '';
    [['ig', 'Instagram'], ['tt', 'TikTok'], ['yt', 'YouTube'], ['pin', 'Pinterest / other'], ['er', 'Engagement'], ['views', 'Monthly views']].forEach(function (p) {
      var v = val(p[0]); if (!v) return;
      var d = document.createElement('div'), b = document.createElement('b'), s = document.createElement('small');
      d.className = 'kit-stat'; b.textContent = v; s.textContent = p[1]; d.appendChild(b); d.appendChild(s); stats.appendChild(d);
    });

    var aud = $('k-aud'); aud.innerHTML = '';
    if (val('age')) aud.appendChild(li('Age', val('age')));
    if (val('gender')) aud.appendChild(li('Gender', val('gender')));
    if (val('countries')) aud.appendChild(li('Top countries', val('countries')));

    var rates = $('k-rates'); rates.innerHTML = '';
    val('services').split('\n').forEach(function (line) {
      line = line.trim(); if (!line) return;
      var parts = line.split('=');
      rates.appendChild(li(parts[0].trim(), (parts[1] || '').trim() || 'Ask'));
    });

    var brands = $('k-brands'); brands.innerHTML = '';
    val('brands').split(',').forEach(function (b) {
      b = b.trim(); if (!b) return;
      var s = document.createElement('span'); s.textContent = b; brands.appendChild(s);
    });
    text('k-email', val('email') || 'you@email.com');
  }

  function save() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      var data = {};
      Array.prototype.forEach.call(form.elements, function (el) { if (el.name) data[el.name] = el.value; });
      try { localStorage.setItem(KEY, JSON.stringify(data)); text('mk-saved', 'Draft saved in this browser.'); }
      catch (e) { text('mk-saved', 'Could not save a draft in this browser (private mode?). Your kit still works.'); }
    }, 400);
  }

  function load(data) {
    Object.keys(data).forEach(function (k) { if (form.elements[k]) form.elements[k].value = data[k]; });
  }

  try { var saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) load(saved); } catch (e) { /* storage unavailable */ }

  form.addEventListener('input', function () { render(); save(); });
  $('mk-print').addEventListener('click', function () {
    document.body.classList.add('mk-printing');
    window.print();
  });
  window.addEventListener('afterprint', function () { document.body.classList.remove('mk-printing'); });
  $('mk-reset').addEventListener('click', function () {
    load(defaults); render();
    try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
    text('mk-saved', 'Example restored.');
  });
  render();
})();
