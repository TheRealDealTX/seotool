/* Relics Film Lab — interactions */
(function () {
  "use strict";
  var d = document, w = window, reduce = w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k) || "null"); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }

  // header shadow
  var hdr = $(".hdr");
  function onScroll() { if (hdr) hdr.classList.toggle("is-scrolled", w.scrollY > 10); }
  w.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // mobile nav
  var burger = $(".burger"), nav = $(".nav");
  var ICO_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  var ICO_X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  function setNav(open) {
    if (!burger || !nav) return;
    if (open && hdr) nav.style.setProperty("--navtop", Math.max(0, hdr.getBoundingClientRect().bottom) + "px");
    nav.classList.toggle("is-open", open); burger.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", open); burger.setAttribute("aria-label", open ? "Close menu" : "Menu");
    burger.innerHTML = open ? ICO_X : ICO_MENU;
    d.documentElement.style.overflow = open ? "hidden" : "";
  }
  if (burger && nav) {
    burger.addEventListener("click", function () { setNav(!nav.classList.contains("is-open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    d.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("is-open")) { setNav(false); burger.focus(); } });
    w.addEventListener("resize", function () { if (w.innerWidth > 980 && nav.classList.contains("is-open")) setNav(false); });
  }
  // desktop "Shop" dropdown also opens on click/tap (touch laptops, tablets)
  $$(".nav button[aria-haspopup]").forEach(function (b) {
    b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", function (e) { e.stopPropagation(); var li = b.parentNode, open = !li.classList.contains("is-open");
      li.classList.toggle("is-open", open); b.setAttribute("aria-expanded", open); });
  });
  d.addEventListener("click", function (e) { if (e.target.closest(".nav__drop")) return;
    $$(".nav>li.is-open").forEach(function (li) { li.classList.remove("is-open"); var b = $("button", li); if (b) b.setAttribute("aria-expanded", "false"); }); });

  // reveal on scroll
  if ("IntersectionObserver" in w && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("is-in"); }); }

  // counters
  $$(".counter[data-to]").forEach(function (el) {
    var to = +el.dataset.to, done = false;
    function run() { if (done) return; done = true; var t0 = performance.now();
      (function tick(t) { var p = Math.min(1, (t - t0) / 1400); el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))).toLocaleString() + (el.dataset.suffix || "");
        if (p < 1) requestAnimationFrame(tick); })(t0); }
    if (reduce || !("IntersectionObserver" in w)) { el.textContent = to.toLocaleString() + (el.dataset.suffix || ""); return; }
    new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { run(); o.disconnect(); } }).observe(el);
  });

  // hero parallax + cursor halo + card tilt (pointer devices only)
  var fine = w.matchMedia("(hover:hover) and (pointer:fine)").matches;
  var heroImg = $(".hero__bg img");
  if (heroImg && !reduce) w.addEventListener("scroll", function () { heroImg.style.translate = "0 " + (w.scrollY * 0.25) + "px"; }, { passive: true });
  if (fine && !reduce) {
    var halo = d.createElement("div"); halo.className = "halo"; d.body.appendChild(halo);
    w.addEventListener("pointermove", function (e) { halo.style.left = e.clientX + "px"; halo.style.top = e.clientY + "px"; }, { passive: true });
    $$(".card").forEach(function (c) {
      c.addEventListener("pointermove", function (e) { var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.style.transform = "perspective(900px) rotateY(" + (x * 7) + "deg) rotateX(" + (-y * 7) + "deg) translateY(-4px)"; });
      c.addEventListener("pointerleave", function () { c.style.transform = ""; });
    });
    var frame = $(".pdp__frame");
    if (frame) frame.addEventListener("pointermove", function (e) { var r = frame.getBoundingClientRect();
      frame.style.setProperty("--zx", ((e.clientX - r.left) / r.width * 100) + "%"); frame.style.setProperty("--zy", ((e.clientY - r.top) / r.height * 100) + "%"); });
  }

  // toast
  var toastEl;
  function toast(msg) { if (!toastEl) { toastEl = d.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); d.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("is-on"); clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("is-on"); }, 2200); }

  // wishlist
  function wl() { return store("relics_wishlist") || []; }
  function paintWl() { var list = wl(); $$(".js-wl-count").forEach(function (b) { b.textContent = list.length || ""; });
    $$(".heart[data-slug]").forEach(function (h) { var on = list.indexOf(h.dataset.slug) > -1; h.classList.toggle("is-on", on); h.setAttribute("aria-pressed", on); }); }
  d.addEventListener("click", function (e) {
    var h = e.target.closest(".heart[data-slug]"); if (!h) return; e.preventDefault();
    var list = wl(), i = list.indexOf(h.dataset.slug);
    if (i > -1) { list.splice(i, 1); toast("Removed from your wishlist"); } else { list.push(h.dataset.slug); toast("Saved to your wishlist"); }
    store("relics_wishlist", list); paintWl();
  });
  paintWl();

  // search index (lazy)
  var idx = null;
  function loadIdx(cb) { if (idx) return cb(idx); fetch("/assets/search.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; cb(j); }).catch(function () { cb([]); }); }
  function card(p) { return '<a href="' + p.u + '">' + (p.i ? '<img src="' + p.i + '" alt="" loading="lazy">' : "<i></i>") + "<span>" + p.n + "<small>" + p.c + "</small></span></a>"; }

  // wishlist page
  var wlPage = $("#wishlist-grid");
  if (wlPage) loadIdx(function (all) { var list = wl(), map = {}; all.forEach(function (p) { map[p.s] = p; });
    var items = list.map(function (s) { return map[s]; }).filter(Boolean);
    wlPage.innerHTML = items.length ? items.map(function (p) { return '<div class="search__res">' + card(p) + "</div>"; }).join("") : '<p class="muted">Your wishlist is empty. Tap the heart on any camera to save it here.</p>'; });

  var ov = $(".search"), inp = ov && $("input", ov), res = ov && $(".search__res", ov);
  function openSearch() { if (!ov) return; ov.classList.add("is-open"); d.documentElement.style.overflow = "hidden"; setTimeout(function () { inp.focus(); }, 30); loadIdx(function () { }); }
  function closeSearch() { if (!ov) return; ov.classList.remove("is-open"); d.documentElement.style.overflow = ""; }
  $$(".js-search").forEach(function (b) { b.addEventListener("click", openSearch); });
  if (ov) {
    ov.addEventListener("click", function (e) { if (e.target === ov) closeSearch(); });
    inp.addEventListener("input", function () { var q = inp.value.toLowerCase().trim(); if (!q) { res.innerHTML = ""; return; }
      loadIdx(function (all) { var t = q.split(/\s+/); var hits = all.filter(function (p) { var h = (p.n + " " + p.c + " " + (p.k || "")).toLowerCase(); return t.every(function (x) { return h.indexOf(x) > -1; }); }).slice(0, 14);
        res.innerHTML = hits.length ? hits.map(card).join("") : '<p class="muted">No matches — try a brand like “Canon” or a format like “120”.</p>'; }); });
  }
  d.addEventListener("keydown", function (e) { if (e.key === "Escape") closeSearch(); if (e.key === "/" && !/input|textarea/i.test(d.activeElement.tagName)) { e.preventDefault(); openSearch(); } });

  // collection filters
  var grid = $("#pgrid");
  if (grid) {
    var cards = $$(".card", grid), chips = $$(".chip[data-brand]"), sort = $("#sort"), count = $(".toolbar .count");
    var brand = "all";
    function apply() { var n = 0; cards.forEach(function (c) { var ok = brand === "all" || c.dataset.brand === brand; c.style.display = ok ? "" : "none"; if (ok) n++; });
      if (count) count.textContent = n + (n === 1 ? " item" : " items"); }
    var bsel = $("#brand");
    function setBrand(v) { brand = v; chips.forEach(function (x) { x.classList.toggle("is-on", x.dataset.brand === v); }); if (bsel) bsel.value = v; apply(); }
    chips.forEach(function (ch) { ch.addEventListener("click", function () { setBrand(ch.dataset.brand); }); });
    if (bsel) bsel.addEventListener("change", function () { setBrand(bsel.value); });
    if (sort) sort.addEventListener("change", function () { var v = sort.value;
      cards.sort(function (a, b) { if (v === "az") return a.dataset.name.localeCompare(b.dataset.name); if (v === "za") return b.dataset.name.localeCompare(a.dataset.name);
        if (v === "lo") return (+a.dataset.price) - (+b.dataset.price); if (v === "hi") return ((+b.dataset.price === 99999 ? -1 : +b.dataset.price) - (+a.dataset.price === 99999 ? -1 : +a.dataset.price)); if (v === "old") return (+a.dataset.year || 9999) - (+b.dataset.year || 9999); if (v === "new") return (+b.dataset.year || 0) - (+a.dataset.year || 0); return (+a.dataset.rank) - (+b.dataset.rank); });
      cards.forEach(function (c) { grid.appendChild(c); }); });
    apply();
  }

  // newsletter (mailto, no backend)
  $$(".js-news").forEach(function (f) { f.addEventListener("submit", function (e) { e.preventDefault(); var em = $("input", f).value;
    w.location.href = "mailto:info@relicsfilmlab.com?subject=" + encodeURIComponent("Join the Relics list") + "&body=" + encodeURIComponent("Please add " + em + " to the Relics Film Lab newsletter."); }); });

  // outbound affiliate click label (for analytics later)
  // outbound Amazon clicks -> GTM dataLayer event "amazon_click" (use as a Custom Event trigger in Tag Manager)
  d.addEventListener("click", function (e) { var a = e.target.closest('a[href*="amazon.com/"]'); if (!a) return;
    w.dataLayer = w.dataLayer || [];
    w.dataLayer.push({ event: "amazon_click", amazon_item: a.dataset.amz || "", amazon_url: a.href, page_path: location.pathname }); });
})();
