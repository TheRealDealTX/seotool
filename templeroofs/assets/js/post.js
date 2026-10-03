/* Blog post: reading progress bar and "On this page" table of contents. */
(function () {
  'use strict';
  var body = document.querySelector('[data-post-body]');
  if (!body) return;

  var bar = document.querySelector('[data-progress]');
  if (bar) {
    var ticking = false;
    var update = function () {
      var rect = body.getBoundingClientRect();
      var total = rect.height - window.innerHeight * 0.6;
      var p = Math.min(Math.max(-rect.top / (total > 0 ? total : 1), 0), 1);
      bar.style.transform = 'scaleX(' + p.toFixed(3) + ')';
      ticking = false;
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  var toc = document.querySelector('[data-toc]');
  var heads = body.querySelectorAll(':scope > h2');
  if (!toc || heads.length < 3) return;
  var list = toc.querySelector('ol');
  var links = [];
  heads.forEach(function (h, i) {
    if (!h.id) {
      h.id = (h.textContent || 'section').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60) || 'section-' + i;
    }
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    li.appendChild(a);
    list.appendChild(li);
    links.push(a);
  });
  toc.hidden = false;
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    heads.forEach(function (h) { io.observe(h); });
  }
})();
