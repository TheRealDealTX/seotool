/* Cart page: lines, totals, saved items, shareable lists, retailer checkout. */
(() => {
  'use strict';
  const G = window.Gap; if (!G) return;
  const $ = (s, r = document) => r.querySelector(s);
  const { money, esc, kindImg } = G;

  // A shared list link (?list=path*qty,path*qty) merges into this visitor's cart once.
  const shared = new URLSearchParams(location.search).get('list');
  if (shared) {
    G.catalog().then(cat => {
      const c = G.cart();
      shared.split(',').forEach(tok => {
        const [p, q] = tok.split('*'), x = cat.find(i => i.p === p); if (!x) return;
        const hit = c.find(i => i.p === p); if (hit) hit.q = Math.max(hit.q, +q || 1); else c.push({ p, n: x.n, pr: x.pr, k: x.k, q: +q || 1 });
      });
      G.setCart(c); history.replaceState(null, '', '/cart/'); G.toast('Shared gear list loaded');
    });
  }

  function draw() {
    const c = G.cart(), lines = $('[data-cart-lines]');
    const n = c.reduce((a, i) => a + i.q, 0), t = c.reduce((a, i) => a + i.q * i.pr, 0);
    $('[data-cart-count-inline]').textContent = n;
    $('[data-sum-items]').textContent = n; $('[data-sum-total]').textContent = money(t);
    $('[data-cart-empty]').hidden = c.length > 0;
    $('.cart-layout').hidden = !c.length;
    lines.innerHTML = c.map(i => `<li class="cart-line" data-p="${esc(i.p)}"><img src="${kindImg(i.k)}" alt="" width="70" height="70">
      <div><a class="name" href="${esc(i.p)}">${esc(i.n)}</a><div class="unit">${money(i.pr)} typical each</div><button class="remove" type="button" data-remove>Remove</button></div>
      <div class="qty" data-line-qty><button type="button" aria-label="Less" data-d="-1">−</button><input type="number" min="1" max="99" value="${i.q}" aria-label="Quantity"><button type="button" aria-label="More" data-d="1">+</button></div>
      <span class="line-total">${money(i.q * i.pr)}</span></li>`).join('');
  }
  function drawSaved() {
    const s = G.saved(), grid = $('[data-saved-grid]');
    $('[data-saved-count-inline]').textContent = s.length;
    $('[data-saved-empty]').hidden = s.length > 0;
    grid.innerHTML = s.map(i => `<article class="card" data-product='${esc(JSON.stringify(i))}'>
      <a class="card-media" href="${esc(i.p)}"><span class="rings"></span><img src="${kindImg(i.k)}" alt=""></a>
      <button class="heart on" type="button" aria-label="Remove from saved" data-save><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8 3.2 4 7 4c2.1 0 3.6 1.2 5 3 1.4-1.8 2.9-3 5-3 3.8 0 6.1 4 4.6 7.7C19.5 16.4 12 21 12 21z"/></svg></button>
      <div class="card-body"><h3 class="card-title"><a href="${esc(i.p)}">${esc(i.n)}</a></h3>
      <div class="card-foot"><span class="price"><small>Typical</small> ${money(i.pr)}</span><button class="btn btn-sm btn-cart" type="button" data-add>Add</button></div></div></article>`).join('');
  }
  const setQty = (p, q) => { const c = G.cart(), it = c.find(i => i.p === p); if (!it) return; it.q = Math.max(1, Math.min(99, q)); G.setCart(c); };
  document.addEventListener('click', e => {
    const line = e.target.closest('.cart-line');
    if (line && e.target.closest('[data-remove]')) { G.setCart(G.cart().filter(i => i.p !== line.dataset.p)); return; }
    if (line && e.target.closest('[data-d]')) { const it = G.cart().find(i => i.p === line.dataset.p); setQty(line.dataset.p, it.q + +e.target.closest('[data-d]').dataset.d); }
    if (e.target.closest('[data-share]')) {
      const url = location.origin + '/cart/?list=' + G.cart().map(i => i.p + '*' + i.q).join(',');
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(() => G.toast('List link copied'), () => prompt('Copy this link', url));
    }
    if (e.target.closest('[data-print]')) print();
    if (e.target.closest('[data-checkout]')) {
      const ul = $('[data-checkout-links]');
      ul.innerHTML = G.cart().map(i => `<li><a href="/go/?p=${encodeURIComponent(i.p)}" target="_blank" rel="sponsored nofollow noopener"><span>${esc(i.n)} × ${i.q}</span><span>Check price ↗</span></a></li>`).join('');
      $('.checkout-dialog').showModal();
    }
  });
  document.addEventListener('change', e => { const line = e.target.closest('.cart-line'); if (line && e.target.matches('input')) setQty(line.dataset.p, +e.target.value || 1); });
  document.addEventListener('gap:cart', draw); document.addEventListener('gap:saved', drawSaved);
  draw(); drawSaved();
})();
