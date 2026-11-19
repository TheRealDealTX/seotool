/* Vintique Flea — site script: nav toggle, affiliate helper, treasure wheel. */
(function () {
  'use strict';
  var TAG = 'josephrayditt-20';

  window.VF = {
    tag: TAG,
    amazon: function (query) {
      return 'https://www.amazon.com/s?k=' + encodeURIComponent(query) + '&tag=' + TAG;
    },
    shopUrl: function (slug) { return '/shop/' + slug + '/'; }
  };

  function ready(fn) {
    if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    // Mobile nav
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        nav.classList.toggle('is-open', !open);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && nav.classList.contains('is-open')) {
          toggle.setAttribute('aria-expanded', 'false');
          nav.classList.remove('is-open');
          toggle.focus();
        }
      });
    }

    // Treasure wheel
    var btn = document.getElementById('wheel-spin');
    var disc = document.getElementById('wheel-disc');
    var out = document.getElementById('wheel-result');
    var dataEl = document.getElementById('wheel-data');
    if (btn && disc && out && dataEl) {
      var items = [];
      try { items = JSON.parse(dataEl.textContent); } catch (e) { items = []; }
      var rotation = 0;
      var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var esc = function (s) {
        return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
      };
      btn.addEventListener('click', function () {
        if (!items.length) return;
        btn.disabled = true;
        out.innerHTML = '';
        var pick = items[Math.floor(Math.random() * items.length)];
        rotation += 1440 + Math.floor(Math.random() * 360);
        disc.style.transform = 'rotate(' + rotation + 'deg)';
        setTimeout(function () {
          out.innerHTML =
            '<p class="wr-cat">' + esc(pick.c) + '</p>' +
            '<h3><span aria-hidden="true">' + esc(pick.i) + '</span> ' + esc(pick.n) + '</h3>' +
            '<p>' + esc(pick.note) + '</p>' +
            '<div class="btn-row"><a class="btn btn--small btn--primary" href="' + esc(pick.u) + '" target="_blank" rel="sponsored nofollow noopener">See on Amazon</a>' +
            '<a class="btn btn--small btn--ghost" href="' + esc(pick.cu) + '">More ' + esc(pick.c) + '</a></div>';
          btn.disabled = false;
          btn.textContent = 'Spin again';
        }, reduced ? 50 : 3300);
      });
    }
  });
})();
