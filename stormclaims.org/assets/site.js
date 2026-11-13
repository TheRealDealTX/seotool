/* stormclaims.org: mobile menu. The toggle opens the nav panel under the
   header; it closes on a link tap, Escape, a tap outside, or when the
   screen gets wide enough for the inline nav. */
(function () {
  'use strict';
  var top = document.querySelector('.top');
  var btn = top && top.querySelector('.nav-toggle');
  if (!btn) return;
  var menu = document.getElementById('nav-menu');
  var wide = window.matchMedia('(min-width: 861px)');

  function set(open) {
    top.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  function isOpen() { return top.classList.contains('open'); }

  btn.addEventListener('click', function () {
    set(!isOpen());
    if (isOpen()) { var first = menu.querySelector('a'); if (first) first.focus({ preventScroll: true }); }
  });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isOpen()) { set(false); btn.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (isOpen() && !top.contains(e.target)) set(false);
  });
  var onWide = function () { if (wide.matches) set(false); };
  if (wide.addEventListener) wide.addEventListener('change', onWide); else wide.addListener(onWide);
}());
