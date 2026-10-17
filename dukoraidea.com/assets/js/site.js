/* dukoraidea.com — site script: nav, effects, interactive light tools */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Header + mobile nav ---------- */
  var header = $(".site-header");
  var toggle = $(".nav-toggle");
  var nav = $("#main-nav");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(!document.body.classList.contains("nav-open"));
    });
    $$("a", nav).forEach(function (a) {
      a.addEventListener("click", function () { setNav(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) { setNav(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 960 && document.body.classList.contains("nav-open")) setNav(false);
    });
  }
  var toTop = $(".to-top");
  var progress = $(".reading-progress");
  var article = $(".prose");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (progress && article) {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      progress.style.transform = "scaleX(" + p + ")";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Firefly canvas ---------- */
  $$("canvas.fireflies").forEach(function (cv) {
    if (reduce) return;
    var ctx = cv.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var flies = [], w = 0, h = 0, running = true;
    var colors = ["255,197,107", "255,214,150", "255,138,91", "157,140,255", "94,230,201"];
    function size() {
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(70, (w * h) / 16000));
      flies = [];
      for (var i = 0; i < n; i++) {
        flies.push({
          x: Math.random() * w, y: Math.random() * h,
          r: Math.random() * 2.2 + 0.6, vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25 - 0.08,
          p: Math.random() * Math.PI * 2, s: Math.random() * 0.02 + 0.006,
          c: colors[i % 5 === 0 ? 3 + (i % 2) : Math.floor(Math.random() * 3)]
        });
      }
    }
    function tick() {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < flies.length; i++) {
        var f = flies[i];
        f.x += f.vx; f.y += f.vy; f.p += f.s;
        if (f.x < -10) f.x = w + 10; if (f.x > w + 10) f.x = -10;
        if (f.y < -10) f.y = h + 10; if (f.y > h + 10) f.y = -10;
        var a = 0.35 + 0.65 * Math.abs(Math.sin(f.p));
        var g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 7);
        g.addColorStop(0, "rgba(" + f.c + "," + a + ")");
        g.addColorStop(1, "rgba(" + f.c + ",0)");
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(f.x, f.y, f.r * 7, 0, Math.PI * 2); ctx.fill();
      }
      requestAnimationFrame(tick);
    }
    size();
    window.addEventListener("resize", size);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !running) { running = true; tick(); } else if (!vis) { running = false; }
      }).observe(cv);
    }
    tick();
  });

  /* hero spotlight follows pointer */
  var spot = $(".hero");
  if (spot && !reduce && window.matchMedia("(pointer:fine)").matches) {
    spot.addEventListener("pointermove", function (e) {
      var r = spot.getBoundingClientRect();
      spot.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100) + "%");
      spot.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100) + "%");
    });
  }

  /* ---------- Tabs ---------- */
  $$("[data-tabs]").forEach(function (box) {
    var btns = $$("[role=tab]", box);
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () { select(i); });
      b.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          var n = (i + (e.key === "ArrowRight" ? 1 : -1) + btns.length) % btns.length;
          select(n); btns[n].focus();
        }
      });
    });
    function select(n) {
      btns.forEach(function (b, i) {
        var on = i === n;
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.tabIndex = on ? 0 : -1;
        document.getElementById(b.getAttribute("aria-controls")).hidden = !on;
      });
    }
  });

  /* ---------- Gallery ---------- */
  $$("[data-gallery]").forEach(function (g) {
    var main = $(".gallery-main img", g);
    $$(".gallery-thumbs button", g).forEach(function (b, _, all) {
      b.addEventListener("click", function () {
        all.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        main.style.opacity = 0;
        setTimeout(function () {
          main.src = b.dataset.src; main.srcset = ""; main.alt = b.dataset.alt; main.style.opacity = 1;
        }, 180);
      });
    });
  });

  /* ---------- Blog filters ---------- */
  $$("[data-filters]").forEach(function (box) {
    var cards = $$("[data-cat]", document.getElementById(box.dataset.filters));
    $$("button", box).forEach(function (b, _, all) {
      b.addEventListener("click", function () {
        all.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        var c = b.dataset.cat;
        cards.forEach(function (card) { card.classList.toggle("is-hidden", c !== "all" && card.dataset.cat !== c); });
      });
    });
  });

  /* ---------- TOC active state ---------- */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
          var a = map[en.target.id]; if (a) a.classList.add("is-active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) tio.observe(el); });
  }

  /* ---------- Tools ---------- */
  function fmt(n, d) { return Number(n).toLocaleString("en-US", { maximumFractionDigits: d === undefined ? 0 : d, minimumFractionDigits: d || 0 }); }
  function seg(box, cb) {
    var btns = $$("button", box);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true"); cb(b.dataset.v);
      });
    });
  }
  function bindRange(input, out, suffix, fn) {
    var upd = function () { out.textContent = (fn ? fn(input.value) : input.value) + (suffix || ""); };
    input.addEventListener("input", upd); upd();
  }

  /* Fairy-light battery-life calculator */
  $$('[data-tool="battery"]').forEach(function (t) {
    var cell = $("[name=cell]", t), leds = $("[name=leds]", t), bright = $("[name=bright]", t), hours = $("[name=hours]", t);
    var mode = 1;
    bindRange(leds, $("[data-out=leds]", t));
    bindRange(bright, $("[data-out=bright]", t), "%");
    bindRange(hours, $("[data-out=hours]", t), " h");
    seg($(".seg", t), function (v) { mode = parseFloat(v); calc(); });
    var row = $(".led-row", t);
    function calc() {
      var cap = parseFloat(cell.value);            // usable mAh of one cell (cells in series share capacity)
      var n = parseInt(leds.value, 10);
      var b = parseInt(bright.value, 10) / 100;
      var perLed = 0.75;                           // mA per micro LED at full brightness (typical copper-wire string)
      var draw = Math.max(4, n * perLed * b * mode + 2);  // +2 mA controller overhead
      var runtime = (cap * 0.85) / draw;           // 85% of rated capacity is realistically usable
      var perNight = parseFloat(hours.value);
      var nights = runtime / perNight;
      $("[data-out=runtime]", t).innerHTML = fmt(runtime, runtime < 10 ? 1 : 0) + "<small>hours</small>";
      $("[data-out=draw]", t).textContent = fmt(draw, 1) + " mA";
      $("[data-out=nights]", t).textContent = fmt(nights, nights < 10 ? 1 : 0) + " nights";
      $("[data-out=month]", t).textContent = fmt(Math.ceil(30 / Math.max(nights, 0.1))) + " battery set" + (Math.ceil(30 / Math.max(nights, 0.1)) === 1 ? "" : "s");
      $(".battery-bar span", t).style.width = Math.min(100, runtime / 3) + "%";
      var show = Math.min(60, Math.max(6, Math.round(n / 4)));
      if (row.children.length !== show) {
        row.innerHTML = "";
        for (var i = 0; i < show; i++) {
          var dot = document.createElement("i");
          dot.style.setProperty("--d", (1.4 + Math.random() * 2) + "s");
          dot.style.setProperty("--dl", (Math.random() * 2) + "s");
          row.appendChild(dot);
        }
      }
      row.style.opacity = 0.25 + b * 0.75;
      row.style.setProperty("--anim", mode < 1 ? "running" : "paused");
      $$("i", row).forEach(function (d) { d.style.animationPlayState = mode < 1 ? "running" : "paused"; });
    }
    [cell, leds, bright, hours].forEach(function (el) { el.addEventListener("input", calc); el.addEventListener("change", calc); });
    calc();
  });

  /* LED strip length & power-supply calculator */
  var PSU = [12, 24, 36, 48, 60, 72, 100, 120, 150, 200, 240, 300, 350, 400, 500, 600];
  $$('[data-tool="strip"]').forEach(function (t) {
    var len = $("[name=len]", t), dens = $("[name=dens]", t), wpm = $("[name=wpm]", t), unit = "ft", volts = 12, color = "#ffc56b";
    var vis = $(".strip-vis", t);
    seg($(".seg[data-k=unit]", t), function (v) {
      var m = unit === "ft" ? len.value * 0.3048 : len.value;
      unit = v;
      len.max = v === "ft" ? 100 : 30; len.step = v === "ft" ? 1 : 0.5;
      len.value = v === "ft" ? Math.round(m / 0.3048) : Math.round(m * 2) / 2;
      calc();
    });
    seg($(".seg[data-k=volts]", t), function (v) { volts = parseInt(v, 10); calc(); });
    $$(".swatch-row button", t).forEach(function (b, _, all) {
      b.addEventListener("click", function () {
        all.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true"); color = b.dataset.c; calc();
      });
    });
    dens.addEventListener("change", function () { wpm.value = dens.selectedOptions[0].dataset.w; calc(); });
    function calc() {
      var meters = unit === "ft" ? len.value * 0.3048 : parseFloat(len.value);
      $("[data-out=len]", t).textContent = len.value + " " + unit;
      var watts = meters * parseFloat(wpm.value || 0);
      var amps = watts / volts;
      var need = watts * 1.2;
      var psu = PSU.filter(function (p) { return p >= need; })[0];
      var leds = Math.round(meters * parseInt(dens.value, 10));
      var cutLeds = volts === 5 ? 1 : volts === 12 ? 3 : 6;
      if (dens.value === "cob") cutLeds = 0;
      var cutCm = dens.value === "cob" ? (volts === 24 ? 5 : 2.5) : (100 / parseInt(dens.value, 10)) * cutLeds;
      var injectAt = volts === 5 ? 2.5 : volts === 12 ? 5 : 10;
      $("[data-out=watts]", t).innerHTML = fmt(watts, 1) + "<small>watts</small>";
      $("[data-out=amps]", t).textContent = fmt(amps, 2) + " A at " + volts + " V";
      $("[data-out=psu]", t).textContent = psu ? psu + " W (" + volts + " V, " + fmt(psu / volts, 1) + " A)" : "Split into several runs";
      $("[data-out=leds]", t).textContent = dens.value === "cob" ? "Continuous COB" : fmt(leds) + " LEDs";
      $("[data-out=cut]", t).textContent = "every " + fmt(cutCm / (unit === "ft" ? 2.54 : 1), 2) + (unit === "ft" ? " in" : " cm");
      var inj = meters > injectAt;
      $("[data-out=inject]", t).textContent = inj ? "Yes: feed power every ~" + (unit === "ft" ? fmt(injectAt / 0.3048) + " ft" : injectAt + " m") : "Not needed for this run";
      var segs = Math.max(1, Math.ceil(meters / injectAt));
      vis.innerHTML = "";
      for (var i = 0; i < segs; i++) vis.appendChild(document.createElement("span"));
      vis.style.setProperty("--strip", color);
    }
    [len, wpm].forEach(function (el) { el.addEventListener("input", calc); });
    calc();
  });

  /* Color temperature & mood picker */
  function kelvinRGB(k) {
    var t = k / 100, r, g, b;
    r = t <= 66 ? 255 : 329.698727446 * Math.pow(t - 60, -0.1332047592);
    g = t <= 66 ? 99.4708025861 * Math.log(t) - 161.1195681661 : 288.1221695283 * Math.pow(t - 60, -0.0755148492);
    b = t >= 66 ? 255 : (t <= 19 ? 0 : 138.5177312231 * Math.log(t - 10) - 305.0447927307);
    return [r, g, b].map(function (v) { return Math.round(Math.max(0, Math.min(255, v))); });
  }
  function hex(rgb) { return "#" + rgb.map(function (v) { return ("0" + v.toString(16)).slice(-2); }).join(""); }
  function hslHex(h, s, l) {
    s /= 100; l /= 100;
    var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l);
    var f = function (n) { return Math.round(255 * (l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))))); };
    return [f(0), f(8), f(4)];
  }
  var KMOODS = [
    [2400, "Candlelight", "Wind-down hour, bedrooms and fairy-light jars. Very little blue light."],
    [2900, "Warm white", "Living rooms, dining and the classic fairy-light glow most people love."],
    [3500, "Soft neutral", "Kitchens, bathrooms and hobby corners where you want warmth and clarity."],
    [4300, "Cool white", "Desks, garages and craft tables where detail matters."],
    [5600, "Daylight", "Task lighting, photo setups and plant shelves. Too crisp for evenings."]
  ];
  var MOODS = {
    sleep: { k: 2200, name: "Sleep", tip: "Dim, very warm light (2,200K or deep amber) in the last hour before bed." },
    relax: { k: 2700, name: "Relax", tip: "Warm white around 2,700K at 30 to 50% brightness feels cozy without being dark." },
    read: { k: 3500, name: "Read", tip: "Neutral 3,000 to 4,000K keeps text crisp without the clinical feel." },
    focus: { k: 5000, name: "Focus", tip: "Cool 4,500 to 5,500K light helps for detailed work and daytime study." },
    party: { hue: 285, name: "Party", tip: "Saturated purples, pinks and blues; set strips to slow fade or music-sync." },
    movie: { hue: 225, name: "Movie", tip: "Low blue bias light behind the TV reduces eye strain in a dark room." }
  };
  $$('[data-tool="color"]').forEach(function (t) {
    var k = $("[name=kelvin]", t), hue = $("[name=hue]", t), bright = $("[name=cbright]", t);
    var prev = $(".room-preview", t), mode = "white";
    function paint(rgb) {
      var b = parseInt(bright.value, 10) / 100;
      var col = hex(rgb);
      prev.style.setProperty("--lc", col);
      prev.style.filter = "brightness(" + (0.45 + b * 0.75) + ")";
      $("[data-out=hex]", t).textContent = col.toUpperCase();
      $("[data-out=bright]", t).textContent = bright.value + "%";
      $(".rp-label", t).textContent = mode === "white" ? fmt(k.value) + "K" : "RGB " + col.toUpperCase();
    }
    function fromK() {
      mode = "white";
      var kv = parseInt(k.value, 10);
      $("[data-out=kelvin]", t).textContent = fmt(kv) + "K";
      var m = KMOODS[0];
      KMOODS.forEach(function (x) { if (kv >= x[0] - 300) m = x; });
      $("[data-out=name]", t).textContent = m[1];
      $("[data-out=use]", t).textContent = m[2];
      paint(kelvinRGB(kv));
    }
    function fromHue() {
      mode = "rgb";
      $("[data-out=hue]", t).textContent = hue.value + "°";
      $("[data-out=name]", t).textContent = "Color mode";
      $("[data-out=use]", t).textContent = "Accent and party lighting. Pair a saturated color with a warm white lamp so faces still look natural.";
      paint(hslHex(parseInt(hue.value, 10), 95, 58));
    }
    k.addEventListener("input", fromK);
    hue.addEventListener("input", fromHue);
    bright.addEventListener("input", function () { mode === "white" ? fromK() : fromHue(); });
    $$("[data-mood]", t).forEach(function (b, _, all) {
      b.addEventListener("click", function () {
        all.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        var m = MOODS[b.dataset.mood];
        if (m.k) { k.value = m.k; fromK(); } else { hue.value = m.hue; fromHue(); }
        $("[data-out=use]", t).textContent = m.tip;
      });
    });
    fromK();
  });

  /* Patio string-light planner */
  $$('[data-tool="patio"]').forEach(function (t) {
    var W = $("[name=pw]", t), L = $("[name=pl]", t), strand = $("[name=strand]", t), spacing = $("[name=spacing]", t);
    var layout = "perimeter", svg = $(".patio-svg", t);
    bindRange(W, $("[data-out=pw]", t), " ft");
    bindRange(L, $("[data-out=pl]", t), " ft");
    seg($(".seg", t), function (v) { layout = v; calc(); });
    function runs(w, l) {
      var r = [], i, n;
      if (layout === "perimeter") r = [[0, 0, w, 0], [w, 0, w, l], [w, l, 0, l], [0, l, 0, 0]];
      if (layout === "zigzag") {
        n = Math.max(2, Math.round(l / 6));
        for (i = 0; i < n; i++) r.push([i % 2 ? w : 0, (l / n) * i, i % 2 ? 0 : w, (l / n) * (i + 1)]);
      }
      if (layout === "parallel") {
        n = Math.max(2, Math.round(l / 6) + 1);
        for (i = 0; i < n; i++) r.push([0, (l / (n - 1)) * i, w, (l / (n - 1)) * i]);
      }
      if (layout === "canopy") {
        var pts = [[0, 0], [w / 2, 0], [w, 0], [w, l / 2], [w, l], [w / 2, l], [0, l], [0, l / 2]];
        pts.forEach(function (p) { r.push([w / 2, l / 2, p[0], p[1]]); });
      }
      return r;
    }
    function calc() {
      var w = parseFloat(W.value), l = parseFloat(L.value);
      var rs = runs(w, l), total = 0, anchors = {};
      rs.forEach(function (s) {
        total += Math.hypot(s[2] - s[0], s[3] - s[1]);
        anchors[s[0].toFixed(1) + "," + s[1].toFixed(1)] = 1; anchors[s[2].toFixed(1) + "," + s[3].toFixed(1)] = 1;
      });
      var withSag = total * 1.1 + 6;               // ~10% for drape + 6 ft to reach the outlet
      var strands = Math.ceil(withSag / parseFloat(strand.value));
      var bulbs = Math.round(total / parseFloat(spacing.value));
      $("[data-out=total]", t).innerHTML = fmt(withSag) + "<small>feet of lights</small>";
      $("[data-out=strands]", t).textContent = strands + " × " + strand.value + " ft strand" + (strands === 1 ? "" : "s");
      $("[data-out=bulbs]", t).textContent = "about " + fmt(bulbs) + " bulbs";
      $("[data-out=anchors]", t).textContent = Object.keys(anchors).length + " anchor points";
      $("[data-out=wire]", t).textContent = fmt(total * 1.05) + " ft of guide wire";
      // drawing
      var pad = 28, vw = 400, vh = 280, sx = (vw - pad * 2) / w, sy = (vh - pad * 2) / l, s = Math.min(sx, sy);
      var ox = (vw - w * s) / 2, oy = (vh - l * s) / 2;
      var out = '<rect x="' + ox + '" y="' + oy + '" width="' + w * s + '" height="' + l * s + '" rx="8" fill="rgba(255,255,255,.03)" stroke="rgba(255,255,255,.18)" stroke-dasharray="4 5"/>';
      var dots = "";
      rs.forEach(function (sg, idx) {
        var x1 = ox + sg[0] * s, y1 = oy + sg[1] * s, x2 = ox + sg[2] * s, y2 = oy + sg[3] * s;
        var mx = (x1 + x2) / 2, my = (y1 + y2) / 2 + 10;
        out += '<path d="M' + x1 + " " + y1 + " Q" + mx + " " + my + " " + x2 + " " + y2 + '" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.2"/>';
        var len = Math.hypot(sg[2] - sg[0], sg[3] - sg[1]), nb = Math.max(2, Math.round(len / parseFloat(spacing.value)));
        for (var i = 1; i < nb; i++) {
          var u = i / nb, bx = (1 - u) * (1 - u) * x1 + 2 * (1 - u) * u * mx + u * u * x2, by = (1 - u) * (1 - u) * y1 + 2 * (1 - u) * u * my + u * u * y2;
          dots += '<circle class="bulb-dot" cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="3.2" fill="#ffc56b" style="animation-delay:' + ((i * 0.37 + idx * 0.21) % 2.2).toFixed(2) + 's;filter:drop-shadow(0 0 4px #ffc56b)"/>';
        }
      });
      Object.keys(anchors).forEach(function (a) {
        var p = a.split(",");
        out += '<circle cx="' + (ox + p[0] * s) + '" cy="' + (oy + p[1] * s) + '" r="5" fill="#0a0d1c" stroke="#5ee6c9" stroke-width="2"/>';
      });
      out += '<text x="' + (vw / 2) + '" y="' + (vh - 6) + '" fill="rgba(255,255,255,.5)" font-size="11" text-anchor="middle" font-family="Manrope, sans-serif">' + w + ' ft × ' + l + ' ft • teal rings = anchor points</text>';
      svg.innerHTML = out + dots;
    }
    [W, L, strand, spacing].forEach(function (el) { el.addEventListener("input", calc); el.addEventListener("change", calc); });
    calc();
  });

  /* Year in footer */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
