/* stonecoatedroofs.com — header, effects, popup, forms */
(function () {
  "use strict";
  var d = document, root = d.documentElement, body = d.body;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }

  /* header + progress */
  var header = d.querySelector(".site-header"), bar = d.querySelector(".progress");
  function onScroll() {
    var y = window.scrollY || root.scrollTop;
    if (header) header.classList.toggle("scrolled", y > 8);
    if (bar) { var h = root.scrollHeight - innerHeight; bar.style.transform = "scaleX(" + (h > 0 ? y / h : 0) + ")"; }
  }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  var toggle = d.querySelector(".menu-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var open = body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { body.classList.remove("nav-open"); }); });

  /* split headline words */
  $$(".split-words").forEach(function (el) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) { frag.appendChild(d.createTextNode(t)); return; }
            var w = d.createElement("span"); w.className = "w";
            var s = d.createElement("span"); s.style.setProperty("--i", i++); s.textContent = t;
            w.appendChild(s); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    })(el);
  });

  /* reveal + counters + meters */
  function count(el) {
    var end = parseFloat(el.getAttribute("data-count")), dec = (el.getAttribute("data-count").split(".")[1] || "").length;
    if (reduce) { el.textContent = end.toFixed(dec); return; }
    var t0 = null, dur = 1600;
    function step(t) {
      t0 = t0 || t; var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (end * e).toFixed(dec);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function reveal(el) {
    el.classList.add("in");
    $$("[data-count]", el).forEach(count);
    if (el.hasAttribute("data-count")) count(el);
    $$(".meter .bar i", el).forEach(function (i) { i.style.width = i.getAttribute("data-w") + "%"; });
  }
  var targets = $$(".rv, .split-words, .stat, .layers, .reveal-group");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(reveal);

  /* steps progress line */
  var steps = d.querySelector(".steps");
  if (steps) addEventListener("scroll", function () {
    var r = steps.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * 0.75 - r.top) / r.height));
    steps.style.setProperty("--p", (p * 100).toFixed(1) + "%");
  }, { passive: true });

  /* pointer glow + tilt on cards */
  if (!reduce && matchMedia("(hover: hover)").matches) {
    $$(".card, .post-card").forEach(function (c) {
      if (!c.querySelector(".glow")) { var g = d.createElement("span"); g.className = "glow"; c.appendChild(g); }
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty("--mx", (e.clientX - r.left) + "px");
        c.style.setProperty("--my", (e.clientY - r.top) + "px");
        if (c.classList.contains("tilt")) {
          var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
          c.style.transform = "perspective(900px) rotateY(" + (x * 8) + "deg) rotateX(" + (-y * 8) + "deg) translateY(-4px)";
        }
      });
      c.addEventListener("pointerleave", function () { if (c.classList.contains("tilt")) c.style.transform = ""; });
    });
    /* hero image parallax + frame tilt */
    var frame = d.querySelector(".hero-visual .frame"), img = frame && frame.querySelector("img");
    if (frame) {
      addEventListener("scroll", function () { var y = scrollY; if (y < 900 && img) img.style.transform = "translateY(" + (-y * 0.08) + "px)"; }, { passive: true });
      var hv = d.querySelector(".hero");
      hv.addEventListener("pointermove", function (e) {
        var x = e.clientX / innerWidth - 0.5, y = e.clientY / innerHeight - 0.5;
        frame.style.transform = "perspective(1200px) rotateY(" + (-6 + x * 8) + "deg) rotateX(" + (3 - y * 6) + "deg)";
      });
    }
    /* magnetic buttons */
    $$(".btn.mag").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * 0.18) + "px," + ((e.clientY - r.top - r.height / 2) * 0.25) + "px)";
      });
      b.addEventListener("pointerleave", function () { b.style.transform = ""; });
    });
  }

  /* hail canvas in hero */
  var cv = d.querySelector("canvas.hail");
  if (cv && !reduce) {
    var ctx = cv.getContext("2d"), W, H, dpr = Math.min(2, devicePixelRatio || 1), stones = [], bursts = [], running = true;
    function size() { W = cv.offsetWidth; H = cv.offsetHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    size(); addEventListener("resize", size);
    var N = Math.round(Math.min(70, W / 18));
    function mk(top) { return { x: Math.random() * W * 1.2 - W * 0.1, y: top ? Math.random() * H : -20 - Math.random() * H * 0.5, r: 0.8 + Math.random() * 2.4, v: 2 + Math.random() * 4, a: 0.15 + Math.random() * 0.45 }; }
    for (var i = 0; i < N; i++) stones.push(mk(true));
    function roofY(x) { /* gentle roofline near the bottom */ var m = W * 0.62; return H - 40 - Math.max(0, 120 - Math.abs(x - m) * 0.32); }
    function frameFn() {
      if (!running) return;
      ctx.clearRect(0, 0, W, H);
      ctx.strokeStyle = "rgba(217,138,99,.22)"; ctx.lineWidth = 1.5; ctx.beginPath();
      for (var x = 0; x <= W; x += 8) { var y = roofY(x); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
      for (var j = 0; j < stones.length; j++) {
        var s = stones[j]; s.y += s.v; s.x += s.v * 0.18;
        if (s.y > roofY(s.x)) { bursts.push({ x: s.x, y: roofY(s.x), t: 0 }); stones[j] = mk(false); continue; }
        ctx.beginPath(); ctx.fillStyle = "rgba(255,255,255," + s.a + ")"; ctx.arc(s.x, s.y, s.r, 0, 6.283); ctx.fill();
      }
      for (var k = bursts.length - 1; k >= 0; k--) {
        var b = bursts[k]; b.t += 1;
        ctx.beginPath(); ctx.strokeStyle = "rgba(242,196,166," + (0.5 - b.t / 40) + ")"; ctx.arc(b.x, b.y, b.t * 0.7, Math.PI, 0); ctx.stroke();
        if (b.t > 20) bursts.splice(k, 1);
      }
      requestAnimationFrame(frameFn);
    }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) {
      var vis = es[0].isIntersecting; if (vis && !running) { running = true; requestAnimationFrame(frameFn); } else if (!vis) running = false;
    }).observe(cv);
    requestAnimationFrame(frameFn);
  }

  /* tabs */
  $$("[data-tabs]").forEach(function (wrap) {
    var btns = $$("[role=tab]", wrap), panels = $$("[role=tabpanel]", wrap);
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () {
        btns.forEach(function (x, j) { x.setAttribute("aria-selected", i === j); panels[j].classList.toggle("on", i === j); });
        $$(".meter .bar i", panels[i]).forEach(function (m) { m.style.width = "0"; setTimeout(function () { m.style.width = m.getAttribute("data-w") + "%"; }, 30); });
      });
    });
  });

  /* comparison picker */
  var cmp = d.querySelector("[data-cmp]");
  if (cmp) {
    var data = JSON.parse(cmp.getAttribute("data-cmp")), head = cmp.querySelector("thead th:last-child");
    $$(".cmp-pick button", cmp).forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".cmp-pick button", cmp).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var k = b.getAttribute("data-k"), rows = data[k];
        head.textContent = b.textContent;
        $$("tbody tr", cmp).forEach(function (tr, i) { var c = tr.lastElementChild; c.textContent = rows[i]; c.classList.remove("hl"); void c.offsetWidth; c.classList.add("hl"); });
        var link = cmp.querySelector(".cmp-link"); if (link) { link.href = data._links[k]; link.textContent = "Read: stone coated vs " + b.textContent.toLowerCase() + " →"; }
      });
    });
  }

  /* city filter */
  $$("[data-city-filter]").forEach(function (inp) {
    var list = d.querySelector(inp.getAttribute("data-city-filter"));
    inp.addEventListener("input", function () {
      var q = inp.value.trim().toLowerCase();
      $$("a", list).forEach(function (a) { a.style.display = a.textContent.toLowerCase().indexOf(q) > -1 ? "" : "none"; });
    });
  });

  /* table of contents */
  var toc = d.querySelector(".toc ol"), prose = d.querySelector(".prose");
  if (toc && prose) {
    var hs = $$("h2", prose);
    if (hs.length < 3) { toc.closest(".toc").remove(); }
    else {
      hs.forEach(function (h, i) {
        if (!h.id) h.id = (h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "s") + "-" + i;
        var li = d.createElement("li"), a = d.createElement("a"); a.href = "#" + h.id; a.textContent = h.textContent; li.appendChild(a); toc.appendChild(li);
      });
      if ("IntersectionObserver" in window) {
        var links = $$("a", toc), tio = new IntersectionObserver(function (es) {
          es.forEach(function (e) { if (e.isIntersecting) links.forEach(function (l) { l.classList.toggle("on", l.getAttribute("href") === "#" + e.target.id); }); });
        }, { rootMargin: "-20% 0px -70% 0px" });
        hs.forEach(function (h) { tio.observe(h); });
      }
    }
  }

  /* copy link */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var u = location.href.split("#")[0];
      (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () { b.textContent = "Link copied"; }, function () { prompt("Copy this link", u); });
    });
  });

  /* forms -> /quote.php */
  function wireForm(f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = f.querySelector(".form-msg"), btn = f.querySelector("[type=submit]");
      var phone = f.querySelector("[name=phone]");
      if (phone && phone.value.replace(/\D/g, "").length < 10) { msg.className = "form-msg err"; msg.textContent = "Please enter a 10-digit phone number."; phone.focus(); return; }
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      var fd = new FormData(f); fd.append("page", location.pathname);
      fetch(f.action, { method: "POST", body: fd, headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (j) {
          if (j && j.ok) {
            msg.className = "form-msg ok"; msg.textContent = "Thanks — your request is in. A Stone Coated Roofs specialist will call you shortly.";
            f.reset(); store.set("scr_lead", Date.now());
            if (window.gtag) gtag("event", "generate_lead", { form: f.getAttribute("data-form") || "quote" });
          } else throw new Error((j && j.error) || "fail");
        })
        .catch(function (err) {
          msg.className = "form-msg err";
          msg.textContent = (err && err.message && err.message !== "fail" ? err.message + " " : "") + "Something went wrong — please call " + (f.getAttribute("data-phone") || "us") + ".";
        })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  }
  $$("form.lead").forEach(wireForm);

  /* auto popup after 3 seconds */
  var pop = d.getElementById("quote-popup");
  if (pop) {
    var lastClose = parseInt(store.get("scr_pop_closed") || "0", 10), lead = store.get("scr_lead");
    var suppressed = body.hasAttribute("data-no-popup") || lead || (Date.now() - lastClose < 24 * 3600 * 1000);
    var prevFocus;
    function open() {
      if (pop.classList.contains("open")) return;
      prevFocus = d.activeElement; pop.classList.add("open"); pop.setAttribute("aria-hidden", "false"); body.classList.add("popup-lock");
      setTimeout(function () { var f = pop.querySelector("input:not(.hp input)"); if (f) f.focus({ preventScroll: true }); }, 350);
    }
    function close() {
      pop.classList.remove("open"); pop.setAttribute("aria-hidden", "true"); body.classList.remove("popup-lock");
      store.set("scr_pop_closed", Date.now()); if (prevFocus && prevFocus.focus) prevFocus.focus();
    }
    if (!suppressed) setTimeout(open, 3000);
    $$("[data-open-quote]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); open(); }); });
    $$("[data-close]", pop).forEach(function (b) { b.addEventListener("click", close); });
    pop.addEventListener("click", function (e) { if (e.target === pop) close(); });
    d.addEventListener("keydown", function (e) {
      if (!pop.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "Tab") {
        var f = $$("button, input, select, textarea, a[href]", pop).filter(function (x) { return x.offsetParent !== null; });
        if (!f.length) return;
        if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    });
  }
})();
