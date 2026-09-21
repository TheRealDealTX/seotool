/* Hutto Roofers - shared site behavior (sticky header + mobile nav).
   No framework, no build step. */
(() => {
  const state = { headers: [] };

  const closeMenu = (root) => {
    const nav = root && root.querySelector('.nav-links');
    const button = root && root.querySelector('.menu-btn');
    if (!nav || !button) return;
    nav.classList.remove('is-open');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', 'Open navigation');
    button.textContent = '☰';
  };

  const discoverHeaders = () => {
    document.querySelectorAll('.site-header').forEach((header) => {
      if (header.dataset.hrReady) return;
      const root = header.closest('.site');
      const sentinel = root && root.querySelector('.header-sentinel');
      const placeholder = root && root.querySelector('.header-placeholder');
      if (!root || !sentinel || !placeholder) return;
      header.dataset.hrReady = 'true';
      state.headers.push({ header, sentinel, placeholder, threshold: 0 });
    });
  };

  const updateHeaders = () => {
    state.headers.forEach(({ header, placeholder, threshold }) => {
      const fixed = window.scrollY > threshold;
      header.classList.toggle('is-fixed', fixed);
      placeholder.style.height = fixed ? `${header.offsetHeight}px` : '0px';
    });
  };

  const measureHeaders = () => {
    discoverHeaders();
    state.headers = state.headers.filter(({ header }) => header.isConnected);
    state.headers.forEach((item) => {
      const wasFixed = item.header.classList.contains('is-fixed');
      if (wasFixed) item.header.classList.remove('is-fixed');
      item.placeholder.style.height = '0px';
      item.threshold = item.sentinel.getBoundingClientRect().top + window.scrollY;
      if (wasFixed) item.header.classList.add('is-fixed');
    });
    updateHeaders();
  };

  document.addEventListener('click', (event) => {
    const button = event.target.closest('.menu-btn');
    if (button) {
      const root = button.closest('.site');
      const nav = root && root.querySelector('.nav-links');
      if (!nav) return;
      const open = nav.classList.toggle('is-open');
      button.setAttribute('aria-expanded', String(open));
      button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      button.textContent = open ? '✕' : '☰';
      return;
    }
    const navLink = event.target.closest('.nav-links a');
    if (navLink) closeMenu(navLink.closest('.site'));
  });

  document.addEventListener('submit', (event) => {
    if (!event.target.matches('[data-estimate-form]')) return;
    event.preventDefault();
    window.alert('Thanks! Connect this form to your preferred form handler or CRM before publishing.');
  });

  let resizeTimer;
  window.addEventListener('scroll', updateHeaders, { passive: true });
  window.addEventListener('resize', () => {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(measureHeaders, 120);
  });

  const initialize = () => window.requestAnimationFrame(measureHeaders);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measureHeaders);
})();
