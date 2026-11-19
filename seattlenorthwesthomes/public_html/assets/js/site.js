/* Seattle Northwest Homes — mobile nav + listing photo lightbox. No dependencies. */
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var gallery = document.querySelector('[data-gallery]');
  if (!gallery) return;
  var links = Array.prototype.slice.call(gallery.querySelectorAll('a'));
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Photo viewer');
  box.innerHTML = '<img alt=""><button class="lb-prev" aria-label="Previous photo">&#8249;</button>' +
    '<button class="lb-next" aria-label="Next photo">&#8250;</button><button class="lb-close" aria-label="Close">&times;</button>';
  document.body.appendChild(box);
  var img = box.querySelector('img');
  var i = 0;
  function show(n) {
    i = (n + links.length) % links.length;
    img.src = links[i].href;
    img.alt = links[i].querySelector('img').alt;
  }
  function close() { box.classList.remove('open'); document.body.style.overflow = ''; }
  links.forEach(function (a, n) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      show(n);
      box.classList.add('open');
      document.body.style.overflow = 'hidden';
      box.querySelector('.lb-close').focus();
    });
  });
  box.querySelector('.lb-prev').addEventListener('click', function () { show(i - 1); });
  box.querySelector('.lb-next').addEventListener('click', function () { show(i + 1); });
  box.querySelector('.lb-close').addEventListener('click', close);
  box.addEventListener('click', function (ev) { if (ev.target === box) close(); });
  document.addEventListener('keydown', function (ev) {
    if (!box.classList.contains('open')) return;
    if (ev.key === 'Escape') close();
    if (ev.key === 'ArrowLeft') show(i - 1);
    if (ev.key === 'ArrowRight') show(i + 1);
  });
})();
