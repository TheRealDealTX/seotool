/* Alabama Insurance Appraiser — site interactions (no dependencies) */
(function () {
  "use strict";
  var d = document, w = window, root = d.documentElement;
  root.classList.add("js");
  var reduce = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = w.matchMedia && w.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---------- header, progress bar, parallax, back-to-top ---------- */
  var header = d.querySelector("[data-header]");
  var bar = d.querySelector(".progress span");
  var toTop = d.querySelector("[data-to-top]");
  var parallax = d.querySelectorAll(".hero-bg, .page-hero-bg");
  var ticking = false;
  function onScroll() {
    var y = w.scrollY || root.scrollTop;
    if (header) header.classList.toggle("scrolled", y > 30);
    if (bar) {
      var h = root.scrollHeight - w.innerHeight;
      bar.style.setProperty("--p", h > 0 ? Math.min(y / h, 1) : 0);
    }
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (!reduce) parallax.forEach(function (el) {
      if (y < w.innerHeight * 1.2) el.style.setProperty("--parallax", (y * 0.28).toFixed(1) + "px");
    });
    drawSteps();
    ticking = false;
  }
  w.addEventListener("scroll", function () { if (!ticking) { ticking = true; w.requestAnimationFrame(onScroll); } }, { passive: true });
  if (toTop) toTop.addEventListener("click", function () { w.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- mobile nav + dropdowns ---------- */
  var toggle = d.querySelector("[data-nav-toggle]");
  function navTop() {
    if (header) root.style.setProperty("--nav-top", Math.max(0, header.getBoundingClientRect().bottom) + "px");
  }
  w.addEventListener("resize", navTop);
  if (toggle) toggle.addEventListener("click", function () {
    navTop();
    var open = d.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", open);
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  d.querySelectorAll(".dd-btn").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault();
      var li = b.parentElement, open = !li.classList.contains("open");
      d.querySelectorAll(".has-dd.open").forEach(function (o) { if (o !== li) { o.classList.remove("open"); o.querySelector(".dd-btn").setAttribute("aria-expanded", "false"); } });
      li.classList.toggle("open", open);
      b.setAttribute("aria-expanded", open);
    });
  });
  d.addEventListener("click", function (e) {
    if (!e.target.closest(".has-dd")) d.querySelectorAll(".has-dd.open").forEach(function (o) { o.classList.remove("open"); });
  });
  d.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      d.querySelectorAll(".has-dd.open").forEach(function (o) { o.classList.remove("open"); });
      if (d.body.classList.contains("nav-open") && toggle) toggle.click();
    }
  });

  /* ---------- headline word-split reveal ---------- */
  d.querySelectorAll("[data-split]").forEach(function (el) {
    if (reduce) return;
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
            var o = d.createElement("span"); o.className = "w";
            var s = d.createElement("span"); s.textContent = part; s.style.setProperty("--i", i++);
            o.appendChild(s); frag.appendChild(o);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.classList.contains("grad-text")) {
          // keep gradient text as one unit: background-clip:text breaks on transformed children
          var ow = d.createElement("span"); ow.className = "w";
          n.parentNode.replaceChild(ow, n); ow.appendChild(n); n.style.setProperty("--i", i++);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    })(el);
    el.classList.add("split-words");
  });

  /* ---------- reveal on scroll (with stagger inside grids) ---------- */
  d.querySelectorAll(".grid, .city-grid, .stats, .steps, .faq, .hero-badges").forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (c, n) { c.style.setProperty("--d", Math.min(n * 0.07, 0.5) + "s"); });
  });
  var reveals = d.querySelectorAll(".reveal, .step");
  if ("IntersectionObserver" in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else reveals.forEach(function (el) { el.classList.add("in"); });

  /* ---------- animated counters ---------- */
  var counters = d.querySelectorAll("[data-count]");
  function runCounter(el) {
    var end = parseFloat(el.getAttribute("data-count")), dur = 1600, t0 = null;
    if (reduce) { el.textContent = end; return; }
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(end * e);
      if (p < 1) w.requestAnimationFrame(step);
    }
    w.requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in w) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { runCounter(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  } else counters.forEach(function (c) { c.textContent = c.getAttribute("data-count"); });

  /* ---------- process line drawing ---------- */
  var stepLists = d.querySelectorAll(".steps");
  function drawSteps() {
    stepLists.forEach(function (s) {
      var r = s.getBoundingClientRect(), vh = w.innerHeight;
      var p = (vh * 0.75 - r.top) / r.height;
      s.style.setProperty("--draw", Math.max(0, Math.min(1, p)).toFixed(3));
    });
  }

  /* ---------- spotlight + tilt + magnetic buttons (fine pointers only) ---------- */
  if (finePointer && !reduce) {
    d.querySelectorAll(".spot").forEach(function (c) {
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty("--mx", (e.clientX - r.left) + "px");
        c.style.setProperty("--my", (e.clientY - r.top) + "px");
        if (c.classList.contains("tilt")) {
          var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
          c.style.transform = "perspective(900px) rotateX(" + (-y * 6).toFixed(2) + "deg) rotateY(" + (x * 6).toFixed(2) + "deg) translateY(-4px)";
        }
      });
      c.addEventListener("pointerleave", function () { c.style.transform = ""; });
    });
    d.querySelectorAll(".magnetic").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty("--bx", ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + "px");
        b.style.setProperty("--by", ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + "px");
      });
      b.addEventListener("pointerleave", function () { b.style.setProperty("--bx", "0px"); b.style.setProperty("--by", "0px"); });
    });
  }

  /* ---------- table of contents for long pages ---------- */
  var prose = d.querySelector("[data-prose]"), toc = d.querySelector("[data-toc]");
  if (prose && toc) {
    var hs = prose.querySelectorAll(":scope > h2");
    if (hs.length >= 3) {
      var ol = toc.querySelector("ol"), links = [];
      hs.forEach(function (h, n) {
        if (!h.id) h.id = (h.textContent || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "s" + n;
        var li = d.createElement("li"), a = d.createElement("a");
        a.href = "#" + h.id; a.textContent = h.textContent; li.appendChild(a); ol.appendChild(li); links.push(a);
      });
      toc.hidden = false;
      if ("IntersectionObserver" in w) {
        var to = new IntersectionObserver(function (es) {
          es.forEach(function (en) {
            if (en.isIntersecting) links.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id); });
          });
        }, { rootMargin: "-20% 0px -70% 0px" });
        hs.forEach(function (h) { to.observe(h); });
      }
    }
  }

  /* ---------- lead form ---------- */
  d.querySelectorAll("[data-lead-form]").forEach(function (f) {
    var ts = f.querySelector('[name="ts"]'), pg = f.querySelector('[name="page"]');
    if (ts) ts.value = Math.floor(Date.now() / 1000);
    if (pg) pg.value = location.pathname;
    var status = f.querySelector(".form-status");
    var btnEl = f.querySelector('button[type="submit"]');
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = null;
      f.querySelectorAll("[required]").forEach(function (el) {
        var ok = el.type === "checkbox" ? el.checked : el.value.trim() !== "";
        if (ok && el.type === "email") ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
        if (ok && el.name === "phone") ok = el.value.replace(/\D/g, "").length >= 10;
        el.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !bad) bad = el;
      });
      if (bad) {
        status.className = "form-status err";
        status.textContent = "Please complete the highlighted fields (a valid email and a 10-digit phone number).";
        bad.focus();
        return;
      }
      btnEl.disabled = true;
      status.className = "form-status";
      status.textContent = "Sending…";
      fetch(f.action, { method: "POST", body: new FormData(f), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res.ok) {
            f.reset(); if (ts) ts.value = Math.floor(Date.now() / 1000);
            status.className = "form-status ok";
            status.textContent = res.message || "Thank you — your claim details were sent. We'll be in touch shortly.";
            (w.dataLayer = w.dataLayer || []).push({ event: "generate_lead", form_page: location.pathname });
          } else {
            status.className = "form-status err";
            status.textContent = res.message || "Something went wrong. Please call (844) 537-1427 or email info@alabamainsuranceappraiser.com.";
          }
        })
        .catch(function () {
          status.className = "form-status err";
          status.textContent = "Network error. Please call (844) 537-1427 or email info@alabamainsuranceappraiser.com.";
        })
        .then(function () { btnEl.disabled = false; });
    });
  });

  /* ---------- glossary filter ---------- */
  var gq = d.querySelector("[data-gloss-search]");
  if (gq) gq.addEventListener("input", function () {
    var q = gq.value.trim().toLowerCase();
    d.querySelectorAll(".term").forEach(function (t) { t.hidden = q && t.textContent.toLowerCase().indexOf(q) === -1; });
  });

  onScroll();
})();
