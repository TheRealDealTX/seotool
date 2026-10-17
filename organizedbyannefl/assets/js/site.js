/* Organized by Anne — site interactions */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- sticky header ---- */
  var header = document.querySelector(".site-header");
  var toTop = document.querySelector(".to-top");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 10);
    if (toTop) toTop.classList.toggle("is-on", y > 700);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---- mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("mobile-nav");
  function setNav(open) {
    if (!toggle || !drawer) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    if (open) drawer.removeAttribute("inert"); else drawer.setAttribute("inert", "");
    document.body.classList.toggle("nav-open", open);
    if (open) { var first = drawer.querySelector("a, button"); if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 200); }
  }
  if (toggle && drawer) {
    toggle.addEventListener("click", function () { setNav(toggle.getAttribute("aria-expanded") !== "true"); });
    drawer.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("is-open")) { setNav(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080 && drawer.classList.contains("is-open")) setNav(false); });
    drawer.querySelectorAll(".m-sub-toggle").forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") !== "true";
        b.setAttribute("aria-expanded", String(open));
        document.getElementById(b.getAttribute("aria-controls")).classList.toggle("is-open", open);
      });
    });
  }

  /* ---- reveal on scroll ---- */
  var revealEls = document.querySelectorAll(".reveal, .reveal-img, [data-reveal]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---- hero word rotator ---- */
  document.querySelectorAll(".rotator").forEach(function (r) {
    var items = r.querySelectorAll("span");
    if (items.length < 2 || reduce) return;
    var i = 0;
    setInterval(function () {
      var cur = items[i];
      cur.classList.remove("is-active"); cur.classList.add("is-leaving");
      setTimeout(function () { cur.classList.remove("is-leaving"); }, 600);
      i = (i + 1) % items.length;
      items[i].classList.add("is-active");
    }, 2400);
  });

  /* ---- hero parallax (pointer) ---- */
  var art = document.querySelector(".hero-art");
  if (art && !reduce && window.matchMedia("(pointer: fine)").matches) {
    var cards = art.querySelectorAll("[data-depth]");
    art.closest(".hero").addEventListener("pointermove", function (e) {
      var rx = (e.clientX / window.innerWidth - 0.5), ry = (e.clientY / window.innerHeight - 0.5);
      cards.forEach(function (c) {
        var d = parseFloat(c.getAttribute("data-depth"));
        c.style.transform = "translate3d(" + (rx * d) + "px," + (ry * d) + "px,0)";
      });
    });
  }

  /* ---- scroll parallax for bands ---- */
  var px = document.querySelectorAll("[data-parallax]");
  if (px.length && !reduce) {
    var ticking = false;
    var update = function () {
      px.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        var p = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
        el.style.transform = "translate3d(0," + (p * -40) + "px,0)";
      });
      ticking = false;
    };
    window.addEventListener("scroll", function () { if (!ticking) { requestAnimationFrame(update); ticking = true; } }, { passive: true });
    update();
  }

  /* ---- card tilt ---- */
  if (!reduce && window.matchMedia("(pointer: fine)").matches) {
    document.querySelectorAll("[data-tilt]").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = "perspective(900px) rotateX(" + (-y * 6) + "deg) rotateY(" + (x * 6) + "deg) translateY(-4px)";
      });
      card.addEventListener("pointerleave", function () { card.style.transform = ""; });
    });
  }

  /* ---- clutter -> calm ---- */
  var stage = document.querySelector(".calm-stage");
  if (stage) {
    var btns = document.querySelectorAll("[data-calm]");
    var label = stage.querySelector(".calm-label");
    var setCalm = function (calm) {
      stage.classList.toggle("is-calm", calm);
      btns.forEach(function (b) { b.setAttribute("aria-pressed", String((b.getAttribute("data-calm") === "1") === calm)); });
      if (label) label.textContent = calm ? "After: calm" : "Before: clutter";
    };
    btns.forEach(function (b) { b.addEventListener("click", function () { setCalm(b.getAttribute("data-calm") === "1"); }); });
    if ("IntersectionObserver" in window && !reduce) {
      var once = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { setTimeout(function () { setCalm(true); }, 900); once.disconnect(); }
      }, { threshold: 0.5 });
      once.observe(stage);
    }
  }

  /* ---- room picker ---- */
  var picker = document.querySelector("[data-picker]");
  if (picker) {
    var data = JSON.parse(picker.querySelector("script[type='application/json']").textContent);
    var out = picker.querySelector(".picker-out");
    var chips = picker.querySelectorAll(".chip");
    var render = function (key) {
      var d = data[key]; if (!d) return;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-key") === key)); });
      out.querySelector(".po-img img").src = d.img;
      out.querySelector(".po-img img").alt = d.alt;
      var body = out.querySelector(".po-body");
      body.classList.remove("fade"); void body.offsetWidth; body.classList.add("fade");
      body.querySelector("h3").textContent = d.title;
      body.querySelector("p").textContent = d.tip;
      var a = body.querySelector("a"); a.href = d.href; a.firstChild.textContent = d.cta + " ";
    };
    chips.forEach(function (c) { c.addEventListener("click", function () { render(c.getAttribute("data-key")); }); });
  }

  /* ---- blog filter ---- */
  var filter = document.querySelector(".blog-filter");
  if (filter) {
    var posts = document.querySelectorAll(".post-card[data-cat]");
    filter.addEventListener("click", function (e) {
      var b = e.target.closest(".chip"); if (!b) return;
      var cat = b.getAttribute("data-cat");
      filter.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", String(c === b)); });
      posts.forEach(function (p) { p.hidden = !(cat === "all" || p.getAttribute("data-cat") === cat); });
    });
  }

  /* ---- reading progress + toc ---- */
  var prog = document.querySelector(".progress");
  var article = document.querySelector(".prose[data-article]");
  if (prog && article) {
    var tocLinks = document.querySelectorAll(".toc a");
    var heads = Array.prototype.map.call(tocLinks, function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var onRead = function () {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      prog.style.transform = "scaleX(" + p + ")";
      var active = -1;
      heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top < 160) active = i; });
      tocLinks.forEach(function (a, i) { a.classList.toggle("is-active", i === active); });
    };
    window.addEventListener("scroll", onRead, { passive: true });
    onRead();
  }

  /* ---- forms (contact + tips signup) ---- */
  document.querySelectorAll("form[data-ajax]").forEach(function (form) {
    var ts = form.querySelector("input[name='ts']");
    if (ts) ts.value = String(Date.now());
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      var btn = form.querySelector("button[type='submit']");
      if (!form.checkValidity()) { form.reportValidity(); return; }
      btn.disabled = true;
      var fd = new FormData(form);
      fetch(form.action, { method: "POST", body: fd, headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (j) {
          status.className = "form-status " + (j.ok ? "ok" : "err");
          status.textContent = j.ok ? (form.getAttribute("data-ok") || "Thank you! We'll be in touch soon.")
            : (j.error || "Something went wrong. Please email info@organizedbyannefl.com.");
          if (j.ok) form.reset();
        })
        .catch(function () {
          status.className = "form-status err";
          status.textContent = "We couldn't send that just now. Please email info@organizedbyannefl.com.";
        })
        .then(function () { btn.disabled = false; if (ts) ts.value = String(Date.now()); });
    });
  });
})();
