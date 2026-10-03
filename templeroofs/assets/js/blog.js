/* Blog index: instant client-side filtering (the form also works without JS via ?q=). */
(function () {
  'use strict';
  var input = document.querySelector('[data-blog-search]');
  var items = document.querySelectorAll('[data-blog-list] .blog-item');
  var empty = document.querySelector('[data-blog-empty]');
  if (!input || !items.length) return;
  input.addEventListener('input', function () {
    var terms = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    var shown = 0;
    items.forEach(function (el) {
      var hay = el.getAttribute('data-search') || '';
      var match = terms.every(function (t) { return hay.indexOf(t) > -1; });
      el.hidden = !match;
      if (match) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  });
})();
