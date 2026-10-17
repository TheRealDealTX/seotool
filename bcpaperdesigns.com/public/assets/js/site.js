/* BC Paper Designs — site script: header, mobile nav, effects, shared bunting renderer */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key) || "null");
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }
  function toast(msg) {
    var t = $(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("show"); }, 2200);
  }
  window.BC = { store: store, toast: toast, reduce: reduce };

  /* ---------- Header + mobile nav ---------- */
  var header = $(".site-header");
  var toggle = $(".nav-toggle");
  var nav = $("#site-nav");
  var backdrop = $(".nav-backdrop");
  var mq = window.matchMedia("(max-width: 960px)");

  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    if (nav && mq.matches) nav.setAttribute("aria-hidden", open ? "false" : "true");
    if (open && nav) { var first = nav.querySelector("a,button"); if (first) setTimeout(function () { first.focus(); }, 60); }
  }
  function syncNavMode() {
    if (!nav) return;
    if (mq.matches) { nav.setAttribute("aria-hidden", document.body.classList.contains("nav-open") ? "false" : "true"); }
    else { nav.removeAttribute("aria-hidden"); setNav(false); }
  }
  if (toggle) toggle.addEventListener("click", function () { setNav(!document.body.classList.contains("nav-open")); });
  if (backdrop) backdrop.addEventListener("click", function () { setNav(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && document.body.classList.contains("nav-open")) { setNav(false); toggle && toggle.focus(); }
    if (e.key === "Escape") $$(".has-sub.open").forEach(function (li) { closeSub(li); });
  });
  if (nav) {
    nav.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (a && mq.matches) setNav(false);
    });
    // keep focus inside the drawer while open on mobile
    nav.addEventListener("keydown", function (e) {
      if (e.key !== "Tab" || !mq.matches || !document.body.classList.contains("nav-open")) return;
      var items = $$("a,button", nav).filter(function (el) { return el.offsetParent !== null; });
      items.unshift(toggle);
      var i = items.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
      else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
    });
  }
  if (mq.addEventListener) mq.addEventListener("change", syncNavMode); else if (mq.addListener) mq.addListener(syncNavMode);
  syncNavMode();

  function closeSub(li) { li.classList.remove("open"); var b = li.querySelector(".nav-sub-toggle"); if (b) b.setAttribute("aria-expanded", "false"); }
  $$(".nav-sub-toggle").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var li = btn.parentElement, open = !li.classList.contains("open");
      $$(".has-sub.open").forEach(function (o) { if (o !== li) closeSub(o); });
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-sub") && !mq.matches) $$(".has-sub.open").forEach(closeSub);
  });

  var toTop = $(".to-top"), prog = $(".read-progress"), article = $("[data-progress]");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (prog && article) {
      var r = article.getBoundingClientRect(), total = r.height - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / (total > 0 ? total : 1)));
      prog.style.transform = "scaleX(" + p + ")";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else reveals.forEach(function (el) { el.classList.add("in"); });

  /* ---------- Floating shapes parallax ---------- */
  var shapeWraps = $$(".float-shapes");
  if (shapeWraps.length && !reduce && window.matchMedia("(hover:hover)").matches) {
    window.addEventListener("pointermove", function (e) {
      var cx = e.clientX / window.innerWidth - 0.5, cy = e.clientY / window.innerHeight - 0.5;
      shapeWraps.forEach(function (w) {
        $$("i", w).forEach(function (el, i) {
          var depth = (i % 4 + 1) * 9;
          el.style.transform = "translate(" + (cx * depth) + "px," + (cy * depth) + "px)";
        });
      });
    }, { passive: true });
  }

  /* ---------- Card tilt ---------- */
  if (!reduce && window.matchMedia("(hover:hover)").matches) {
    $$("[data-tilt]").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = "perspective(800px) rotateY(" + (x * 8) + "deg) rotateX(" + (-y * 8) + "deg) translateY(-4px)";
      });
      card.addEventListener("pointerleave", function () { card.style.transform = ""; });
    });
  }

  /* ---------- Confetti ---------- */
  var canvas, ctx, parts = [], raf = 0;
  var COLORS = ["#ff6f61", "#ffcf5a", "#5cc9b5", "#ab97ff", "#8fd3ff", "#ffc6c0"];
  function confetti(x, y, n) {
    if (reduce) return;
    if (!canvas) {
      canvas = document.createElement("canvas"); canvas.id = "confetti"; canvas.setAttribute("aria-hidden", "true");
      document.body.appendChild(canvas); ctx = canvas.getContext("2d");
    }
    var dpr = window.devicePixelRatio || 1;
    canvas.width = innerWidth * dpr; canvas.height = innerHeight * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    for (var i = 0; i < (n || 120); i++) {
      var a = Math.random() * Math.PI * 2, s = 4 + Math.random() * 9;
      parts.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 6, w: 6 + Math.random() * 7, h: 8 + Math.random() * 10,
        r: Math.random() * 6, vr: (Math.random() - 0.5) * 0.4, c: COLORS[i % COLORS.length], life: 0, shape: i % 3 });
    }
    if (!raf) raf = requestAnimationFrame(tick);
  }
  function tick() {
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    parts = parts.filter(function (p) { return p.life < 220 && p.y < innerHeight + 40; });
    parts.forEach(function (p) {
      p.life++; p.vy += 0.22; p.vx *= 0.985; p.x += p.vx; p.y += p.vy; p.r += p.vr;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillStyle = p.c;
      if (p.shape === 0) ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * Math.abs(Math.cos(p.life / 8)));
      else if (p.shape === 1) { ctx.beginPath(); ctx.arc(0, 0, p.w / 2, 0, 7); ctx.fill(); }
      else { ctx.beginPath(); ctx.moveTo(0, -p.h / 2); ctx.lineTo(p.w / 2, p.h / 2); ctx.lineTo(-p.w / 2, p.h / 2); ctx.fill(); }
      ctx.restore();
    });
    raf = parts.length ? requestAnimationFrame(tick) : 0;
    if (!raf) ctx.clearRect(0, 0, innerWidth, innerHeight);
  }
  window.BC.confetti = confetti;
  $$("[data-confetti]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      var r = el.getBoundingClientRect();
      confetti(e.clientX || r.left + r.width / 2, e.clientY || r.top + r.height / 2, 140);
    });
  });
  var heroBurst = $("[data-confetti-load]");
  if (heroBurst && !reduce) setTimeout(function () { var r = heroBurst.getBoundingClientRect(); confetti(r.left + r.width / 2, r.top + 40, 90); }, 900);

  /* ---------- Bunting renderer (shared with tools) ---------- */
  var FONTS = { serif: "Fraunces, Georgia, serif", sans: "'Plus Jakarta Sans', Arial, sans-serif", script: "Caveat, cursive" };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function flagShape(shape, w, h) {
    if (shape === "swallow") return '<path d="M0 0H' + w + "V" + h + "L" + w / 2 + " " + h * 0.74 + "L0 " + h + 'Z"/>';
    if (shape === "scallop") return '<path d="M0 0H' + w + "V" + h * 0.62 + "A" + w / 2 + " " + w / 2 + " 0 0 1 0 " + h * 0.62 + 'Z"/>';
    if (shape === "circle") return '<circle cx="' + w / 2 + '" cy="' + w / 2 + '" r="' + w / 2 + '"/>';
    return '<path d="M0 0H' + w + "L" + w / 2 + " " + h + 'Z"/>';
  }
  function flagLetterY(shape, w, h) {
    if (shape === "circle") return w / 2 + w * 0.17;
    if (shape === "scallop") return h * 0.5;
    if (shape === "swallow") return h * 0.44;
    return h * 0.4;
  }
  function flag(ch, i, o, w, h) {
    var col = o.colors[i % o.colors.length];
    var fs = o.font === "script" ? w * 0.74 : w * 0.56;
    var txt = ch === " " ? "" : '<text x="' + w / 2 + '" y="' + flagLetterY(o.shape, w, h) + '" text-anchor="middle" dominant-baseline="middle" font-family="' + FONTS[o.font || "serif"] + '" font-weight="700" font-size="' + fs + '" fill="' + (o.ink || "#ffffff") + '">' + esc(ch) + "</text>";
    var deco = o.dots ? '<circle cx="' + w * 0.18 + '" cy="' + h * 0.07 + '" r="' + w * 0.035 + '" fill="#fff" opacity=".85"/><circle cx="' + w * 0.82 + '" cy="' + h * 0.07 + '" r="' + w * 0.035 + '" fill="#fff" opacity=".85"/>' : "";
    return '<g fill="' + col + '">' + flagShape(o.shape, w, h) + "</g>" + deco + txt;
  }
  // Returns an SVG string of the whole bunting (lines wrap at o.perRow letters)
  function bunting(text, o) {
    o = o || {}; o.colors = (o.colors && o.colors.length) ? o.colors : COLORS; o.shape = o.shape || "pennant";
    var w = 100, h = o.shape === "circle" ? 100 : 130, gap = 14, sag = o.sag == null ? 26 : o.sag;
    var words = String(text || "").toUpperCase().replace(/\s+/g, " ").trim();
    if (!words) words = "PARTY";
    if (o.font === "script") words = String(text || "Party").replace(/\s+/g, " ").trim() || "Party";
    var per = o.perRow || 14, lines = [], cur = "";
    words.split(" ").forEach(function (word) {
      if ((cur + (cur ? " " : "") + word).length > per && cur) { lines.push(cur); cur = word; } else cur += (cur ? " " : "") + word;
    });
    if (cur) lines.push(cur);
    var maxLen = Math.max.apply(null, lines.map(function (l) { return l.length; }));
    var W = maxLen * (w + gap) + 40, rowH = h + sag + 50, H = lines.length * rowH + 10;
    var out = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Banner reading ' + esc(lines.join(" ")) + '">';
    var idx = 0;
    lines.forEach(function (line, li) {
      var n = line.length, lw = n * (w + gap) - gap, x0 = (W - lw) / 2, y0 = li * rowH + 22;
      var half = lw / 2 + 20, mid = x0 + lw / 2;
      out += '<path d="M' + (x0 - 20) + " " + y0 + " Q" + mid + " " + (y0 + sag * 2) + " " + (x0 + lw + 20) + " " + y0 + '" fill="none" stroke="' + (o.string || "#2a2140") + '" stroke-width="3" stroke-linecap="round" opacity=".7"/>';
      for (var i = 0; i < n; i++) {
        var cx = x0 + i * (w + gap) + w / 2, t = (cx - mid) / half;
        var y = y0 + sag * (1 - t * t), ang = Math.atan(-2 * sag * t / half) * 180 / Math.PI * 0.9;
        var delay = (i * 0.17).toFixed(2);
        out += '<g transform="translate(' + (cx - w / 2) + "," + y + ") rotate(" + ang.toFixed(2) + " " + w / 2 + ' 0)"><g class="flag" style="animation-delay:-' + delay + 's">' + flag(line[i], idx++, o, w, h) + "</g></g>";
      }
    });
    return out + "</svg>";
  }
  // Single large flag (for printing one letter per page)
  function bigFlag(ch, i, o) {
    o.shape = o.shape || "pennant";
    var w = 100, h = o.shape === "circle" ? 100 : 130;
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 ' + (w + 4) + " " + (h + 4) + '">' + flag(ch, i, o, w, h).replace(/<g fill="([^"]+)">/, '<g fill="$1" stroke="#cfc6bb" stroke-width=".4" stroke-dasharray="2 2">') + "</svg>";
  }
  window.BC.bunting = bunting; window.BC.bigFlag = bigFlag;

  // Live bunting demos
  $$("[data-live-bunting]").forEach(function (box) {
    var input = document.getElementById(box.getAttribute("data-live-bunting"));
    var colors = (box.getAttribute("data-colors") || "").split(",").filter(Boolean);
    var shape = box.getAttribute("data-shape") || "pennant";
    var str = box.getAttribute("data-string") || "#2a2140";
    function draw() { box.innerHTML = bunting(input ? input.value : box.getAttribute("data-text"), { colors: colors, shape: shape, perRow: +(box.getAttribute("data-per") || 12), dots: true, string: str }); }
    if (input) input.addEventListener("input", draw);
    draw();
  });

  /* ---------- Set explorer tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$('[role="tab"]', wrap);
    function show(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab; t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute("aria-controls"));
        if (p) { p.hidden = !on; if (on) { p.classList.remove("panel-in"); void p.offsetWidth; p.classList.add("panel-in"); } }
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { show(t); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = null;
        if (k === "ArrowDown" || k === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (k === "ArrowUp" || k === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); show(n, true); }
      });
    });
  });

  /* ---------- Palette swatches: copy hex ---------- */
  $$(".swatch[data-hex]").forEach(function (sw) {
    sw.addEventListener("click", function () {
      var hex = sw.getAttribute("data-hex");
      var done = function () { sw.classList.add("copied"); toast("Copied " + hex); setTimeout(function () { sw.classList.remove("copied"); }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(hex).then(done, done); else done();
    });
  });

  /* ---------- Checklists (saved per page) ---------- */
  $$("[data-checklist]").forEach(function (box) {
    var key = "bc-check-" + box.getAttribute("data-checklist");
    var inputs = $$('input[type="checkbox"]', box), saved = store(key) || {};
    var ring = $(".ring", box), label = $(".ring span", box);
    function update() {
      var done = inputs.filter(function (i) { return i.checked; }).length, p = inputs.length ? Math.round(done / inputs.length * 100) : 0;
      if (ring) ring.style.setProperty("--p", p); if (label) label.textContent = p + "%";
      var state = {}; inputs.forEach(function (i) { state[i.value] = i.checked; }); store(key, state);
      if (p === 100 && !box._party) { box._party = true; var r = box.getBoundingClientRect(); confetti(r.left + r.width / 2, r.top + 60, 160); toast("All set. Time to party!"); }
      if (p < 100) box._party = false;
    }
    inputs.forEach(function (i) { if (saved[i.value]) i.checked = true; i.addEventListener("change", update); });
    box._party = inputs.length && inputs.every(function (i) { return i.checked; });
    update();
    var reset = $("[data-reset]", box);
    if (reset) reset.addEventListener("click", function () { inputs.forEach(function (i) { i.checked = false; }); update(); });
    var pr = $("[data-print]", box);
    if (pr) pr.addEventListener("click", function () { window.print(); });
  });

  /* ---------- Collection filter ---------- */
  $$("[data-filter-grid]").forEach(function (wrap) {
    var grid = $(wrap.getAttribute("data-filter-grid")), cards = $$("[data-tags]", grid);
    var chips = $$("[data-filter]", wrap), search = $("input[type=search]", wrap), empty = $(".empty", wrap.parentElement);
    var active = "all";
    function apply() {
      var q = (search && search.value || "").trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var ok = (active === "all" || c.getAttribute("data-tags").indexOf(active) > -1) && (!q || c.textContent.toLowerCase().indexOf(q) > -1);
        c.style.display = ok ? "" : "none"; if (ok) shown++;
      });
      if (empty) empty.style.display = shown ? "none" : "block";
    }
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        active = ch.getAttribute("data-filter");
        chips.forEach(function (c) { c.setAttribute("aria-pressed", c === ch ? "true" : "false"); });
        apply();
      });
    });
    if (search) search.addEventListener("input", apply);
  });

  /* ---------- TOC active state ---------- */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove("active"); }); var a = map[en.target.id]; if (a) a.classList.add("active"); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) tio.observe(el); });
  }

  /* ---------- Contact form → email draft ---------- */
  var cf = $("#contact-form");
  if (cf) cf.addEventListener("submit", function (e) {
    e.preventDefault();
    var f = cf.elements, to = cf.getAttribute("data-to");
    var subject = "[" + f.topic.value + "] " + (f.event_date.value ? "Party on " + f.event_date.value + " - " : "") + f.name.value;
    var body = "Name: " + f.name.value + "\nEmail: " + f.email.value + "\nTopic: " + f.topic.value + "\nTheme: " + f.theme.value + "\nParty date: " + f.event_date.value + "\n\n" + f.message.value;
    window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    var st = $(".form-status", cf); if (st) st.textContent = "Your email app should open with the message ready to send. If it doesn't, write to " + to + ".";
  });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
