/* Shop VIP Gifts — navigation, effects and forms */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var mobileQuery = window.matchMedia("(max-width: 1040px)");

  /* ---------- Header + mobile nav ---------- */
  var header = document.querySelector(".site-header");
  var burger = document.querySelector(".burger");
  var nav = document.getElementById("main-nav");

  function setNav(open) {
    if (!nav || !burger) return;
    nav.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("nav-open", open);
    if (header) header.classList.toggle("solid", open);
    if (!open) {
      nav.querySelectorAll(".has-sub.open").forEach(function (li) {
        li.classList.remove("open");
        var b = li.querySelector(".sub-toggle");
        if (b) b.setAttribute("aria-expanded", "false");
      });
    }
  }

  if (burger && nav) {
    burger.addEventListener("click", function () {
      setNav(!nav.classList.contains("open"));
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { if (mobileQuery.matches) setNav(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { setNav(false); burger.focus(); }
    });
    var onChange = function () { if (!mobileQuery.matches) setNav(false); };
    if (mobileQuery.addEventListener) mobileQuery.addEventListener("change", onChange);
    else if (mobileQuery.addListener) mobileQuery.addListener(onChange);
  }

  document.querySelectorAll(".sub-toggle").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var li = btn.closest(".has-sub");
      var open = !li.classList.contains("open");
      document.querySelectorAll(".has-sub.open").forEach(function (o) {
        if (o !== li) { o.classList.remove("open"); o.querySelector(".sub-toggle").setAttribute("aria-expanded", "false"); }
      });
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (mobileQuery.matches) return;
    if (!e.target.closest(".has-sub")) {
      document.querySelectorAll(".has-sub.open").forEach(function (o) {
        o.classList.remove("open"); o.querySelector(".sub-toggle").setAttribute("aria-expanded", "false");
      });
    }
  });

  /* ---------- Scroll: header, to-top, reading progress ---------- */
  var toTop = document.querySelector(".to-top");
  var progress = document.querySelector(".read-progress");
  var article = document.querySelector(".prose");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 700);
    if (progress && article) {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
      progress.style.width = (p * 100) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Animated counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  function runCounter(el) {
    var end = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduced) { el.textContent = end + suffix; return; }
    var start = null, dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCounter(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });
  } else counters.forEach(runCounter);

  /* ---------- Tilt cards (pointer devices only) ---------- */
  if (!reduced && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll("[data-tilt]").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = "perspective(900px) rotateY(" + (x * 8) + "deg) rotateX(" + (-y * 8) + "deg) translateY(-4px)";
      });
      card.addEventListener("mouseleave", function () { card.style.transform = ""; });
    });
    var hv = document.querySelector(".hero-visual");
    if (hv) {
      document.querySelector(".hero").addEventListener("mousemove", function (e) {
        var x = e.clientX / window.innerWidth - 0.5, y = e.clientY / window.innerHeight - 0.5;
        hv.querySelectorAll(".hv-card").forEach(function (c, i) {
          var d = (i + 1) * 10;
          c.style.translate = (x * d) + "px " + (y * d) + "px";
        });
      });
    }
  }

  /* ---------- Gold sparkles canvas ---------- */
  var canvas = document.getElementById("sparkles");
  if (canvas && !reduced && canvas.getContext) {
    var ctx = canvas.getContext("2d"), parts = [], W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), running = true;
    function size() {
      W = canvas.offsetWidth; H = canvas.offsetHeight;
      canvas.width = W * dpr; canvas.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(90, W / 14));
      parts = [];
      for (var i = 0; i < n; i++) parts.push(make(true));
    }
    function make(anywhere) {
      return { x: Math.random() * W, y: anywhere ? Math.random() * H : H + 10, r: Math.random() * 1.8 + 0.4,
        vy: -(Math.random() * 0.35 + 0.08), vx: (Math.random() - 0.5) * 0.15, a: Math.random(), tw: Math.random() * 0.03 + 0.005 };
    }
    function draw() {
      if (!running) return;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        p.x += p.vx; p.y += p.vy; p.a += p.tw;
        if (p.y < -10) parts[i] = p = make(false);
        var alpha = 0.35 + Math.abs(Math.sin(p.a)) * 0.65;
        ctx.beginPath();
        ctx.fillStyle = "rgba(243, 220, 166," + alpha.toFixed(3) + ")";
        ctx.shadowColor = "rgba(214,177,106,.9)"; ctx.shadowBlur = 8;
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
        if (p.r > 1.7) {
          ctx.fillRect(p.x - p.r * 3, p.y - 0.3, p.r * 6, 0.6);
          ctx.fillRect(p.x - 0.3, p.y - p.r * 3, 0.6, p.r * 6);
        }
      }
      requestAnimationFrame(draw);
    }
    size(); draw();
    var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(size, 200); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !running) { running = true; draw(); } else if (!vis) running = false;
      }).observe(canvas);
    }
  }

  /* ---------- Gift-giving countdown ---------- */
  var cd = document.querySelector("[data-countdown]");
  if (cd) {
    function nthWeekday(y, m, wd, n) { var d = new Date(y, m, 1); var off = (wd - d.getDay() + 7) % 7; return new Date(y, m, 1 + off + (n - 1) * 7); }
    function events(y) {
      return [
        { k: "valentines", n: "Valentine's Day", d: new Date(y, 1, 14) },
        { k: "mothers", n: "Mother's Day", d: nthWeekday(y, 4, 0, 2) },
        { k: "fathers", n: "Father's Day", d: nthWeekday(y, 5, 0, 3) },
        { k: "bosses", n: "Boss's Day", d: new Date(y, 9, 16) },
        { k: "christmas", n: "Christmas", d: new Date(y, 11, 25) }
      ];
    }
    function upcoming() {
      var now = new Date(), y = now.getFullYear(), list = [];
      events(y).concat(events(y + 1)).forEach(function (e) { if (e.d > now) list.push(e); });
      list.sort(function (a, b) { return a.d - b.d; });
      var seen = {}, out = [];
      list.forEach(function (e) { if (!seen[e.k]) { seen[e.k] = 1; out.push(e); } });
      return out;
    }
    var evs = upcoming(), current = evs[0];
    var nameEl = cd.querySelector("[data-cd-name]"), dateEl = cd.querySelector("[data-cd-date]");
    var tabs = cd.querySelector(".cd-tabs");
    evs.forEach(function (e, i) {
      var b = document.createElement("button");
      b.type = "button"; b.textContent = e.n; if (i === 0) b.className = "active";
      b.addEventListener("click", function () {
        tabs.querySelectorAll("button").forEach(function (x) { x.className = ""; });
        b.className = "active"; current = e; tick();
      });
      tabs.appendChild(b);
    });
    function tick() {
      var diff = Math.max(0, current.d - new Date());
      var d = Math.floor(diff / 864e5), h = Math.floor(diff / 36e5) % 24, m = Math.floor(diff / 6e4) % 60, s = Math.floor(diff / 1e3) % 60;
      cd.querySelector("[data-d]").textContent = d;
      cd.querySelector("[data-h]").textContent = ("0" + h).slice(-2);
      cd.querySelector("[data-m]").textContent = ("0" + m).slice(-2);
      cd.querySelector("[data-s]").textContent = ("0" + s).slice(-2);
      nameEl.textContent = current.n;
      dateEl.textContent = current.d.toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric", year: "numeric" });
    }
    tick(); setInterval(tick, 1000);
  }

  /* ---------- Gift box toggle ---------- */
  document.querySelectorAll(".giftbox").forEach(function (g) {
    g.addEventListener("click", function () { g.classList.toggle("open"); });
  });

  /* ---------- Forms -> contact.php ---------- */
  document.querySelectorAll("form[data-ajax]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-note");
      var btn = form.querySelector("button[type=submit]");
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (res) {
          if (res && res.ok) {
            note.textContent = form.dataset.success || "Thank you — we'll be in touch soon.";
            note.style.color = ""; form.reset();
          } else throw new Error((res && res.error) || "error");
        })
        .catch(function () {
          note.innerHTML = 'Something went wrong. Please email us at <a href="mailto:info@shopvipgifts.com">info@shopvipgifts.com</a>.';
        })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; } });
    });
  });

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
