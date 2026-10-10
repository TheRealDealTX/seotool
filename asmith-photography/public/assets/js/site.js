/* asmith.photography — interactions. No dependencies. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }

  /* Aperture intro: once per browser session */
  var iris = $(".iris");
  if (iris) {
    if (reduce || store("iris")) { iris.classList.add("gone"); }
    else {
      store("iris", "1");
      requestAnimationFrame(function () { setTimeout(function () { iris.classList.add("open"); }, 250); });
      setTimeout(function () { iris.classList.add("gone"); }, 1500);
    }
  }

  /* Header: solid after scroll, hides on scroll down */
  var header = $(".site-header"), lastY = 0;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle("solid", y > 40);
      header.classList.toggle("hide", y > 400 && y > lastY && !doc.classList.contains("menu-open"));
    }
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* Mobile menu */
  var btn = $(".menu-btn");
  if (btn) btn.addEventListener("click", function () {
    var open = doc.classList.toggle("menu-open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { doc.classList.remove("menu-open"); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") doc.classList.remove("menu-open"); });

  /* Split headline into words/chars for the type reveal */
  $$(".split").forEach(function (el) {
    var i = 0;
    function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (word) {
            if (!word) return;
            if (/^\s+$/.test(word)) { frag.appendChild(document.createTextNode(" ")); return; }
            var w = document.createElement("span"); w.className = "w";
            word.split("").forEach(function (c) {
              var s = document.createElement("span"); s.className = "ch"; s.textContent = c;
              s.style.transitionDelay = (0.25 + i++ * 0.022) + "s"; w.appendChild(s);
            });
            frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1) walk(n);
      });
    }
    el.setAttribute("aria-label", el.textContent.trim());
    walk(el);
    setTimeout(function () { el.classList.add("in"); }, iris && !iris.classList.contains("gone") ? 650 : 60);
  });

  /* Reveal + darkroom "develop" on scroll */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }) : null;
  $$(".reveal, .develop").forEach(function (el, i) {
    if (!io || reduce) { el.classList.add("in"); return; }
    el.style.transitionDelay = (i % 3) * 0.08 + "s";
    io.observe(el);
  });

  /* Word-by-word light-up statement */
  var words = $$(".statement .dim");
  function lightStatement() {
    if (!words.length) return;
    var vh = window.innerHeight;
    words.forEach(function (w) { w.classList.toggle("lit", w.getBoundingClientRect().top < vh * 0.72); });
  }
  if (words.length) { window.addEventListener("scroll", lightStatement, { passive: true }); lightStatement(); }

  /* Hero: HUD frame counter + roaming focus box + parallax */
  var counter = $("[data-counter]"), focus = $(".viewfinder .focus"), heroImg = $(".hero-media img");
  if (counter) {
    var shots = 1;
    setInterval(function () { shots = shots % 36 + 1; counter.textContent = (shots < 10 ? "0" : "") + shots + "/36"; }, 2400);
  }
  if (focus && !reduce) {
    var spots = [[50, 42], [36, 30], [64, 52], [44, 60], [58, 34]], k = 0;
    setInterval(function () {
      k = (k + 1) % spots.length; focus.classList.remove("locked");
      focus.style.left = spots[k][0] + "%"; focus.style.top = spots[k][1] + "%";
      setTimeout(function () { focus.classList.add("locked"); }, 700);
    }, 2600);
  }
  var aHero = $(".a-hero .hero-media img");
  if (aHero && !reduce) {
    window.addEventListener("scroll", function () {
      var y = window.scrollY; if (y > window.innerHeight) return;
      aHero.style.transform = "scale(1.08) translateY(" + (y * 0.18) + "px)";
    }, { passive: true });
  }

  /* 3D tilt on story frames */
  if (fine && !reduce) {
    $$(".card .frame").forEach(function (f) {
      f.addEventListener("pointermove", function (e) {
        var r = f.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        f.style.transform = "perspective(900px) rotateY(" + (x * 6) + "deg) rotateX(" + (-y * 6) + "deg)";
      });
      f.addEventListener("pointerleave", function () { f.style.transform = ""; });
    });
  }

  /* Custom cursor */
  if (fine && !reduce) {
    var cur = document.createElement("div"); cur.className = "cursor"; cur.innerHTML = "<span>VIEW</span>";
    document.body.appendChild(cur);
    var cx = 0, cy = 0, tx = 0, ty = 0;
    window.addEventListener("pointermove", function (e) { tx = e.clientX; ty = e.clientY; cur.classList.add("on"); }, { passive: true });
    document.addEventListener("pointerleave", function () { cur.classList.remove("on"); });
    (function loop() { cx += (tx - cx) * 0.2; cy += (ty - cy) * 0.2; cur.style.transform = "translate(" + cx + "px," + cy + "px)"; requestAnimationFrame(loop); })();
    $$(".card, .cat").forEach(function (el) {
      el.addEventListener("pointerenter", function () { cur.classList.add("big"); });
      el.addEventListener("pointerleave", function () { cur.classList.remove("big"); });
    });
  }

  /* Article: reading progress + table of contents highlight */
  var bar = $(".progress"), prose = $(".prose");
  if (bar && prose) {
    var toc = $$(".toc a"), heads = toc.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var tick = function () {
      var r = prose.getBoundingClientRect(), total = r.height - window.innerHeight * 0.6;
      bar.style.transform = "scaleX(" + Math.min(1, Math.max(0, -r.top / total)) + ")";
      var cur = 0; heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top < 160) cur = i; });
      toc.forEach(function (a, i) { a.classList.toggle("on", i === cur); });
    };
    window.addEventListener("scroll", tick, { passive: true }); tick();
  }

  /* Journal filters + search */
  var chips = $$(".chip[data-filter]"), q = $("#q"), cards = $$(".journal-grid .card"), empty = $(".empty");
  if (cards.length) {
    var active = "all";
    var apply = function () {
      var term = q ? q.value.trim().toLowerCase() : "", shown = 0;
      cards.forEach(function (c) {
        var ok = (active === "all" || c.dataset.cat === active) && (!term || c.dataset.text.indexOf(term) > -1);
        c.classList.toggle("hidden", !ok); if (ok) { shown++; c.classList.add("in"); }
      });
      if (empty) empty.style.display = shown ? "none" : "block";
    };
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        active = c.dataset.filter;
        chips.forEach(function (o) { o.setAttribute("aria-pressed", o === c ? "true" : "false"); });
        apply();
        try { history.replaceState(null, "", active === "all" ? location.pathname : "#" + active); } catch (e) {}
      });
    });
    if (q) q.addEventListener("input", apply);
    var h = location.hash.slice(1), pre = chips.filter(function (c) { return c.dataset.filter === h; })[0];
    if (pre) pre.click();
  }

  /* Exposure lab */
  var lab = $(".lab");
  if (lab) {
    var img = $(".lab-view img", lab), noise = $(".lab-view .noise", lab), note = $(".lab-note", lab);
    var A = [1.4, 2, 2.8, 4, 5.6, 8, 11, 16], S = [30, 60, 125, 250, 500, 1000, 2000, 4000], I = [100, 200, 400, 800, 1600, 3200, 6400];
    var fa = $("#ap", lab), fs = $("#sh", lab), fi = $("#iso", lab);
    var meter = $(".meter", lab);
    for (var m = -6; m <= 6; m++) { var t = document.createElement("i"); if (m === 0) t.className = "zero"; meter.appendChild(t); }
    var ticks = $$("i", meter);
    var render = function () {
      var a = A[fa.value], s = S[fs.value], iso = I[fi.value];
      $("#apv", lab).textContent = "f/" + a; $("#shv", lab).textContent = "1/" + s; $("#isov", lab).textContent = "ISO " + iso;
      // Exposure relative to f/4, 1/250, ISO 400 (a correct exposure for the sample frame).
      var ev = Math.log2(Math.pow(4 / a, 2) * (250 / s) * (iso / 400));
      var stops = Math.max(-6, Math.min(6, Math.round(ev)));
      ticks.forEach(function (t, i) { var v = i - 6; t.classList.toggle("on", v !== 0 && (stops > 0 ? v > 0 && v <= stops : v < 0 && v >= stops)); });
      var bright = Math.pow(2, ev * 0.55), dof = Math.max(0, (4 - a) * 0.9), motion = s < 125 ? (125 / s) * 0.9 : 0;
      img.style.filter = "brightness(" + bright.toFixed(2) + ") blur(" + (dof * 0.35 + motion).toFixed(2) + "px) contrast(" + (ev > 1.5 ? 0.85 : 1.05) + ")";
      noise.style.opacity = Math.min(0.85, (Math.log2(iso / 100)) * 0.13).toFixed(2);
      var msg;
      if (ev > 1.5) msg = "Overexposed by about " + Math.round(ev) + " stops: highlights are gone. Close down, speed up, or drop the ISO.";
      else if (ev < -1.5) msg = "Underexposed by about " + Math.round(-ev) + " stops. Open up, slow the shutter, or push the ISO and accept the grain.";
      else if (s < 125) msg = "Exposure is right, but at 1/" + s + " a moving skater will blur. Great for panning; risky handheld.";
      else if (a <= 2) msg = "Wide open at f/" + a + ": razor-thin focus, soft background. Nail the eyes.";
      else if (iso >= 3200) msg = "Clean exposure at ISO " + iso + ", with visible grain. Some film shooters chase that look on purpose.";
      else msg = "A balanced frame. This is the starting point most skate and street shooters dial in before the action starts.";
      note.textContent = msg;
    };
    [fa, fs, fi].forEach(function (r) { r.addEventListener("input", render); });
    render();
  }

  /* Contact form */
  var form = $("#contact-form");
  if (form) {
    var ok = $(".notice", form.parentNode);
    if (/[?&]sent=1/.test(location.search) && ok) ok.classList.add("show");
    form.addEventListener("submit", function () { var b = $("button[type=submit]", form); if (b) { b.disabled = true; b.textContent = "Sending…"; } });
  }

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
