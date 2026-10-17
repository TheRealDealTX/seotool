/* Jaz & Theo — site behavior: header, mobile nav, scroll effects, gallery
   lightbox, article TOC/progress, checklists, post filters, contact form. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- Header: solid after scroll, hide on scroll down ---- */
  var header = $(".site-header");
  var lastY = 0;
  var toTop = $(".to-top");
  var progress = $(".progress");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) {
      header.classList.toggle("solid", y > 40);
      var hide = y > lastY && y > 500 && !document.body.classList.contains("nav-open");
      header.classList.toggle("hide", hide);
    }
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (progress) {
      var art = $(".prose");
      if (art) {
        var r = art.getBoundingClientRect();
        var total = art.offsetHeight - window.innerHeight * 0.6;
        var p = Math.min(1, Math.max(0, -r.top / (total || 1)));
        progress.style.transform = "scaleX(" + p + ")";
      }
    }
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---- Mobile nav ---- */
  var toggle = $(".nav-toggle");
  var nav = $("#main-nav");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    if (open && header) header.classList.remove("hide");
    if (open) {
      var first = nav && nav.querySelector("a");
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 350);
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setNav(!document.body.classList.contains("nav-open")); });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) { setNav(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) setNav(false); });
  }

  /* ---- Split hero headline into animated words ---- */
  $$("[data-split]").forEach(function (el) {
    if (reduce) return;
    var i = 0;
    function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; }
            var outer = document.createElement("span");
            outer.className = "split-word";
            var inner = document.createElement("span");
            inner.textContent = w;
            inner.style.animationDelay = (0.15 + i++ * 0.08) + "s";
            outer.appendChild(inner);
            frag.appendChild(outer);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") {
          walk(n);
        }
      });
    }
    walk(el);
  });

  /* ---- Reveal on scroll ---- */
  var revealEls = $$(".reveal, .reveal-stagger, .img-reveal");
  if ("IntersectionObserver" in window && !reduce) {
    // A clip-path hides an element from IntersectionObserver, so .img-reveal is watched via its parent.
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var t = en.target;
        (t._revealTargets || [t]).forEach(function (x) { x.classList.add("in"); });
        io.unobserve(t);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) {
      if (el.classList.contains("img-reveal")) {
        var p = el.parentElement;
        (p._revealTargets = p._revealTargets || (p.matches(".reveal, .reveal-stagger") ? [p] : [])).push(el);
        io.observe(p);
      } else io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Parallax ---- */
  var px = $$("[data-parallax]");
  if (px.length && !reduce) {
    var ticking = false;
    var run = function () {
      px.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > window.innerHeight) return;
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.15;
        var off = (r.top + r.height / 2 - window.innerHeight / 2) * -speed;
        el.style.transform = "translate3d(0," + off.toFixed(1) + "px,0) scale(1.12)";
      });
      ticking = false;
    };
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(run); } }, { passive: true });
    run();
  }

  /* ---- Count-up numbers ---- */
  var counters = $$("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseInt(el.getAttribute("data-count"), 10), t0 = null;
        co.unobserve(el);
        if (reduce) { el.textContent = end; return; }
        var step = function (t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1400);
          el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  }

  /* ---- Tilt on tiles (pointer devices only) ---- */
  if (window.matchMedia("(hover: hover)").matches && !reduce) {
    $$(".tile").forEach(function (t) {
      t.addEventListener("mousemove", function (e) {
        var r = t.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        t.style.transform = "perspective(900px) rotateY(" + (x * 7) + "deg) rotateX(" + (-y * 7) + "deg) translateY(-4px)";
      });
      t.addEventListener("mouseleave", function () { t.style.transform = ""; });
    });
  }

  /* ---- Gallery lightbox ---- */
  var gal = $$(".gallery button");
  if (gal.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Photo viewer");
    lb.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button><button class="lb-prev" aria-label="Previous photo">&#8249;</button><button class="lb-next" aria-label="Next photo">&#8250;</button><figure><img alt=""><figcaption></figcaption></figure>';
    document.body.appendChild(lb);
    var lbImg = $("img", lb), lbCap = $("figcaption", lb), idx = 0, opener = null;
    var show = function (i) {
      idx = (i + gal.length) % gal.length;
      var b = gal[idx];
      lbImg.src = b.getAttribute("data-full");
      lbImg.alt = $("img", b).alt;
      lbCap.textContent = b.getAttribute("data-caption") || "";
    };
    var close = function () { lb.classList.remove("open"); document.body.style.overflow = ""; if (opener) opener.focus(); };
    gal.forEach(function (b, i) {
      b.addEventListener("click", function () { opener = b; show(i); lb.classList.add("open"); document.body.style.overflow = "hidden"; $(".lb-close", lb).focus(); });
    });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { show(idx - 1); });
    $(".lb-next", lb).addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
    var sx = null;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      sx = null;
    });
  }

  /* ---- Article TOC highlighting ---- */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var ho = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          map[en.target.id].classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    $$(".prose h2[id]").forEach(function (h) { ho.observe(h); });
  }

  /* ---- Copy link ---- */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = b.getAttribute("data-copy");
      var done = function () { b.setAttribute("aria-label", "Link copied"); b.classList.add("copied"); setTimeout(function () { b.setAttribute("aria-label", "Copy link"); }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, done); else done();
    });
  });

  /* ---- Tickable checklists (remembered per page) ---- */
  $$(".checklist").forEach(function (cl, n) {
    var items = $$("li", cl);
    if (!items.length) return;
    var key = "jt-cl:" + location.pathname + ":" + n;
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (e) { saved = []; }
    var bar = document.createElement("div");
    bar.className = "cl-progress";
    bar.innerHTML = '<span></span><button type="button">Reset</button>';
    cl.appendChild(bar);
    var update = function () {
      var done = items.filter(function (li) { return li.classList.contains("done"); }).length;
      $("span", bar).textContent = done + " of " + items.length + " done";
      try { localStorage.setItem(key, JSON.stringify(items.map(function (li) { return li.classList.contains("done") ? 1 : 0; }))); } catch (e) {}
    };
    items.forEach(function (li, i) {
      li.setAttribute("role", "checkbox");
      li.setAttribute("tabindex", "0");
      if (saved[i]) li.classList.add("done");
      li.setAttribute("aria-checked", li.classList.contains("done") ? "true" : "false");
      var flip = function () { li.classList.toggle("done"); li.setAttribute("aria-checked", li.classList.contains("done") ? "true" : "false"); update(); };
      li.addEventListener("click", flip);
      li.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(); } });
    });
    $("button", bar).addEventListener("click", function () { items.forEach(function (li) { li.classList.remove("done"); li.setAttribute("aria-checked", "false"); }); update(); });
    update();
  });

  /* ---- Client-side post filter (journal page) ---- */
  var fb = $("[data-filter-bar]");
  if (fb) {
    var cards = $$("[data-cat]");
    $$("button", fb).forEach(function (b) {
      b.addEventListener("click", function () {
        var c = b.getAttribute("data-f");
        $$("button", fb).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        cards.forEach(function (card) { card.classList.toggle("is-hidden", c !== "all" && card.getAttribute("data-cat") !== c); });
      });
    });
  }

  /* ---- Contact form (AJAX to contact.php, falls back to normal POST) ---- */
  $$("form[data-ajax]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var st = $(".form-status", f), btn = $("button[type=submit]", f);
      btn.disabled = true;
      st.className = "form-status";
      fetch(f.action, { method: "POST", body: new FormData(f), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          st.className = "form-status " + (d.ok ? "ok" : "err");
          st.textContent = d.ok ? "Thank you — your note is on its way. We reply within two business days." : (d.error || "Something went wrong. Please email info@jazandtheo.com instead.");
          if (d.ok) f.reset();
        })
        .catch(function () { st.className = "form-status err"; st.textContent = "Network error. Please email info@jazandtheo.com instead."; })
        .then(function () { btn.disabled = false; });
    });
  });

  /* ---- Year ---- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
