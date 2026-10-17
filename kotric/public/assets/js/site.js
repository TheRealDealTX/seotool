/* Kotric — shared site script: navigation, effects and the interactive tools. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- Mobile navigation ---------- */
  var header = $(".site-header");
  var toggle = $(".nav-toggle");
  var mobile = $("#mobile-nav");
  function setNav(open) {
    if (!header || !toggle) return;
    header.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    doc.classList.toggle("nav-locked", open);
    if (mobile) mobile.setAttribute("aria-hidden", open ? "false" : "true");
    if (open && mobile) { var f = mobile.querySelector("a"); if (f) setTimeout(function () { f.focus(); }, 50); }
  }
  if (toggle) {
    toggle.addEventListener("click", function () { setNav(!header.classList.contains("nav-open")); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("nav-open")) { setNav(false); toggle.focus(); }
    });
    if (mobile) $$("a", mobile).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
    window.addEventListener("resize", function () { if (window.innerWidth > 920) setNav(false); });
  }

  /* ---------- Header shadow, back-to-top, reading progress ---------- */
  var toTop = $(".to-top");
  var bar = $(".read-progress");
  var article = $(".prose");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (toTop) toTop.classList.toggle("show", y > 700);
    if (bar && article) {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      bar.style.width = (p * 100).toFixed(1) + "%";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else reveals.forEach(function (el) { el.classList.add("in"); });

  /* ---------- Count-up numbers ---------- */
  $$("[data-count]").forEach(function (el) {
    var end = parseInt(el.getAttribute("data-count"), 10), suf = el.getAttribute("data-suffix") || "";
    var run = function () {
      var t0 = null;
      var step = function (t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / 1400);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suf;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if ("IntersectionObserver" in window) {
      var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); o.disconnect(); } });
      o.observe(el);
    } else el.textContent = end + suf;
  });

  /* ---------- Hero collage parallax ---------- */
  var collage = $(".collage");
  if (collage && window.matchMedia("(pointer:fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var figs = $$("figure", collage);
    collage.parentElement.addEventListener("mousemove", function (e) {
      var r = collage.getBoundingClientRect();
      var x = (e.clientX - r.left - r.width / 2) / r.width, y = (e.clientY - r.top - r.height / 2) / r.height;
      figs.forEach(function (f, i) {
        var d = (i + 1) * 10;
        f.style.translate = (x * d).toFixed(1) + "px " + (y * d).toFixed(1) + "px";
      });
    });
  }

  /* ---------- Table of contents highlight ---------- */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var ho = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          var a = map[e.target.id]; if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) ho.observe(h); });
  }

  /* ---------- Copy link ---------- */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var done = function () { var t = b.textContent; b.textContent = "Link copied ✓"; setTimeout(function () { b.textContent = t; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
    });
  });

  /* ---------- Tutorial steps: tap to tick off ---------- */
  $$(".steps").forEach(function (list, li) {
    var key = "kotric-steps-" + location.pathname + "-" + li;
    var saved = store.get(key) || [];
    $$("li", list).forEach(function (item, i) {
      if (saved.indexOf(i) > -1) item.classList.add("done");
      item.setAttribute("tabindex", "0");
      item.setAttribute("role", "checkbox");
      item.setAttribute("aria-checked", item.classList.contains("done") ? "true" : "false");
      var flip = function (e) {
        if (e.target.closest("a")) return;
        item.classList.toggle("done");
        item.setAttribute("aria-checked", item.classList.contains("done") ? "true" : "false");
        store.set(key, $$("li", list).map(function (x, j) { return x.classList.contains("done") ? j : -1; }).filter(function (j) { return j > -1; }));
      };
      item.addEventListener("click", flip);
      item.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(e); } });
    });
  });

  /* ---------- Chip groups (generic single-select) ---------- */
  function chipGroup(root, onChange) {
    $$(".chip", root).forEach(function (c) {
      c.addEventListener("click", function () {
        $$(".chip", root).forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        c.setAttribute("aria-pressed", "true");
        onChange(c.getAttribute("data-v"));
      });
    });
  }

  /* ---------- Blog category filter ---------- */
  var bf = $("#blog-filter");
  if (bf) chipGroup(bf, function (v) {
    $$(".post-grid [data-cat]").forEach(function (card) {
      card.style.display = (v === "all" || card.getAttribute("data-cat") === v) ? "" : "none";
    });
  });

  /* ---------- Homepage project picker ---------- */
  var picker = $("#picker");
  if (picker) {
    var ideas = JSON.parse($("#picker-data").textContent);
    var state = { time: "hour", skill: "nosew", mood: "home" };
    var out = $(".picker-result", picker);
    var render = function () {
      var best = null, bestScore = -1;
      ideas.forEach(function (it) {
        var s = (it.time === state.time ? 2 : 0) + (it.skill === state.skill ? 3 : 0) + (it.mood === state.mood ? 2 : 0);
        if (s > bestScore) { bestScore = s; best = it; }
      });
      out.style.opacity = 0;
      setTimeout(function () {
        out.innerHTML = '<img src="' + best.img + '" alt="" width="110" height="110" loading="lazy"><div><h4>' + best.title +
          '</h4><p>' + best.text + '</p><span class="pill">⏱ ' + best.label + '</span><span class="pill">' + (best.skill === "nosew" ? "No sewing" : best.skill === "hand" ? "Hand stitching" : "Machine sewing") +
          '</span> <a href="' + best.url + '">See how →</a></div>';
        out.style.opacity = 1;
      }, 180);
    };
    $$(".picker-q", picker).forEach(function (q) {
      chipGroup(q, function (v) { state[q.getAttribute("data-k")] = v; render(); });
    });
    render();
  }

  /* ---------- 41 projects: filter, search, made-it tracker ---------- */
  var plist = $("#proj-list");
  if (plist) {
    var items = $$(".proj", plist), q = $("#proj-q"), filter = "all";
    var madeKey = "kotric-made-" + location.pathname;
    var made = store.get(madeKey) || [];
    var prog = $("#proj-prog"), progBar = $("#proj-bar");
    var updateProg = function () {
      var n = $$(".proj input[type=checkbox]:checked", plist).length;
      if (prog) prog.textContent = n + " / " + items.length + " made";
      if (progBar) progBar.style.width = (n / items.length * 100) + "%";
    };
    items.forEach(function (it) {
      var cb = $("input[type=checkbox]", it);
      if (!cb) return;
      if (made.indexOf(it.id) > -1) { cb.checked = true; it.classList.add("is-made"); }
      cb.addEventListener("change", function () {
        it.classList.toggle("is-made", cb.checked);
        store.set(madeKey, items.filter(function (x) { var c = $("input[type=checkbox]", x); return c && c.checked; }).map(function (x) { return x.id; }));
        updateProg();
      });
    });
    var apply = function () {
      var term = (q && q.value || "").toLowerCase().trim(), shown = 0;
      items.forEach(function (it) {
        var okF = filter === "all" || (it.getAttribute("data-tags") || "").split(" ").indexOf(filter) > -1 || (filter === "made" && it.classList.contains("is-made"));
        var okQ = !term || it.textContent.toLowerCase().indexOf(term) > -1;
        it.hidden = !(okF && okQ);
        if (!it.hidden) shown++;
      });
      var e = $(".empty-note"); if (e) e.style.display = shown ? "none" : "block";
    };
    var fb = $("#proj-filter"); if (fb) chipGroup(fb, function (v) { filter = v; apply(); });
    if (q) q.addEventListener("input", apply);
    updateProg();
  }

  /* ---------- Contact form ---------- */
  var cf = $("#contact-form");
  if (cf && window.fetch && window.FormData) {
    cf.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = $("#contact-note"), btn = $("button[type=submit]", cf);
      btn.disabled = true;
      fetch(cf.action, { method: "POST", body: new FormData(cf), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          note.className = "notice show" + (d.ok ? "" : " err");
          note.textContent = d.message;
          if (d.ok) cf.reset();
        })
        .catch(function () {
          note.className = "notice show err";
          note.innerHTML = 'Something went wrong. Please email us directly at <a href="mailto:info@kotric.com">info@kotric.com</a>.';
        })
        .then(function () { btn.disabled = false; });
    });
  }

  /* ================= Calculators ================= */
  var num = function (el) { var v = parseFloat(el && el.value); return isNaN(v) ? 0 : v; };
  var fmt = function (n, d) { return (Math.round(n * Math.pow(10, d || 2)) / Math.pow(10, d || 2)).toString(); };
  var FRACS = [[0, ""], [0.125, "⅛"], [0.25, "¼"], [0.375, "⅜"], [0.5, "½"], [0.625, "⅝"], [0.75, "¾"], [0.875, "⅞"], [1, ""]];
  var yardFrac = function (y) {
    var w = Math.floor(y), r = y - w, best = FRACS[0];
    FRACS.forEach(function (f) { if (f[0] >= r - 1e-9 && (best[0] < r - 1e-9 || f[0] < best[0])) best = f; });
    if (best[0] === 1) { w += 1; best = FRACS[0]; }
    return (w ? w : "") + (best[1] ? (w ? " " : "") + best[1] : (w ? "" : "0"));
  };

  /* Fabric yardage calculator */
  var yc = $("#yardage-calc");
  if (yc) {
    var unitBtns = $$(".seg button", yc), unit = "in";
    var calcY = function () {
      var k = unit === "cm" ? 1 / 2.54 : 1;
      var pw = num($("#y-w", yc)) * k, pl = num($("#y-l", yc)) * k, qty = Math.max(1, Math.round(num($("#y-q", yc)))),
        sa = num($("#y-sa", yc)) * k, fw = parseFloat($("#y-fw", yc).value), shrink = parseFloat($("#y-sh", yc).value) || 0;
      var cw = pw + 2 * sa, cl = pl + 2 * sa;
      var out = $("#y-out", yc);
      if (!pw || !pl) { out.innerHTML = '<span class="lbl">Enter your piece size</span>'; return; }
      var usable = fw - 1; // selvedges
      var orient = function (a, b) {
        if (a > usable) return null;
        var per = Math.floor(usable / a), rows = Math.ceil(qty / per);
        return { per: per, rows: rows, len: rows * b, w: a, l: b };
      };
      var o1 = orient(cw, cl), o2 = orient(cl, cw);
      var best = (o1 && o2) ? (o1.len <= o2.len ? o1 : o2) : (o1 || o2);
      if (!best) { out.innerHTML = '<div class="lbl">Too wide</div><p>Each piece is wider than a ' + fw + '" bolt. Try 108" wide-back fabric or piece it.</p>'; return; }
      var inches = best.len * (1 + shrink / 100);
      var yards = Math.ceil(inches / 4.5) / 8; // round up to nearest 1/8 yd
      var meters = inches * 0.0254;
      out.innerHTML = '<div class="lbl">Buy at least</div><div class="big">' + yardFrac(yards) + ' yd</div>' +
        '<ul><li>' + fmt(meters, 2) + ' m (' + fmt(inches, 1) + '" of length)</li>' +
        '<li>Cut size per piece: ' + fmt(cw, 2) + '" × ' + fmt(cl, 2) + '"</li>' +
        '<li>' + best.per + ' piece' + (best.per > 1 ? 's' : '') + ' across the width × ' + best.rows + ' row' + (best.rows > 1 ? 's' : '') + '</li>' +
        (shrink ? '<li>Includes ' + shrink + '% pre-wash shrinkage</li>' : '') + '</ul>' + vizSvg(usable, best, qty);
    };
    var vizSvg = function (usable, b, qty) {
      var W = 300, sc = W / usable, H = Math.min(260, b.len * sc + 4), rows = Math.min(b.rows, 12), s = "";
      var n = 0;
      for (var r = 0; r < rows; r++) for (var c = 0; c < b.per && n < qty; c++, n++)
        s += '<rect x="' + (c * b.w * sc + 1).toFixed(1) + '" y="' + (r * b.l * sc + 1).toFixed(1) + '" width="' + (b.w * sc - 2).toFixed(1) + '" height="' + (b.l * sc - 2).toFixed(1) + '" rx="3" fill="#eaa79f" stroke="#cf5a35" stroke-dasharray="4 3"/>';
      return '<div class="viz"><svg viewBox="0 0 ' + W + ' ' + Math.max(40, H) + '" role="img" aria-label="Cutting layout preview"><rect x="0" y="0" width="' + W + '" height="' + Math.max(40, H) + '" fill="#fbf6ef"/>' + s + '</svg></div>';
    };
    unitBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        unitBtns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true"); unit = b.getAttribute("data-u");
        $$(".u", yc).forEach(function (s) { s.textContent = unit === "cm" ? "cm" : "in"; });
        calcY();
      });
    });
    $$("input,select", yc).forEach(function (i) { i.addEventListener("input", calcY); });
    calcY();
  }

  /* Fleece tie blanket calculator */
  var tb = $("#tie-calc");
  if (tb) {
    var SIZES = { baby: [36, 36], throw: [50, 60], twin: [60, 84], lap: [45, 55], custom: null };
    var sizeSel = $("#t-size", tb);
    var calcT = function () {
      var preset = SIZES[sizeSel.value];
      if (preset) { $("#t-w", tb).value = preset[0]; $("#t-l", tb).value = preset[1]; }
      $("#t-custom", tb).style.display = sizeSel.value === "custom" ? "" : "none";
      var w = num($("#t-w", tb)), l = num($("#t-l", tb)), fl = num($("#t-f", tb)), sp = num($("#t-s", tb)) || 1;
      var cw = w + 2 * fl, cl = l + 2 * fl;
      var yards = Math.ceil((cl + 2) / 4.5) / 8; // +2" to square up
      var bolt = cw > 58 ? " (wider than 58–60\" fleece — piece it or turn it)" : "";
      var tiesW = Math.max(0, Math.floor(w / sp)), tiesL = Math.max(0, Math.floor(l / sp));
      var ties = 2 * tiesW + 2 * tiesL;
      var mins = Math.round(ties * 0.4 + 20);
      $("#t-out", tb).innerHTML = '<div class="lbl">Fleece per layer</div><div class="big">' + yardFrac(yards) + ' yd</div><ul>' +
        '<li>Buy two pieces (top + backing): ' + yardFrac(yards * 2) + ' yd total' + bolt + '</li>' +
        '<li>Cut each layer to ' + fmt(cw, 1) + '" × ' + fmt(cl, 1) + '"</li>' +
        '<li>Remove a ' + fl + '" × ' + fl + '" square from each corner</li>' +
        '<li>Cut fringe every ' + sp + '": about ' + ties + ' knots</li>' +
        '<li>Allow roughly ' + (mins >= 60 ? Math.floor(mins / 60) + ' h ' + (mins % 60) + ' min' : mins + ' min') + ' to tie</li></ul>' + blanketSvg(w, l, fl);
    };
    var blanketSvg = function (w, l, fl) {
      var W = 300, sc = W / (w + 2 * fl), H = (l + 2 * fl) * sc, f = fl * sc, s = '';
      for (var x = f; x < W - f - 1; x += 8) s += '<line x1="' + x.toFixed(1) + '" y1="0" x2="' + x.toFixed(1) + '" y2="' + f.toFixed(1) + '"/><line x1="' + x.toFixed(1) + '" y1="' + (H - f).toFixed(1) + '" x2="' + x.toFixed(1) + '" y2="' + H.toFixed(1) + '"/>';
      for (var y = f; y < H - f - 1; y += 8) s += '<line x1="0" y1="' + y.toFixed(1) + '" x2="' + f.toFixed(1) + '" y2="' + y.toFixed(1) + '"/><line x1="' + (W - f).toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + W + '" y2="' + y.toFixed(1) + '"/>';
      return '<div class="viz"><svg viewBox="-2 -2 ' + (W + 4) + ' ' + (H + 4).toFixed(0) + '" role="img" aria-label="Blanket layout preview"><rect x="' + f.toFixed(1) + '" y="' + f.toFixed(1) + '" width="' + (W - 2 * f).toFixed(1) + '" height="' + (H - 2 * f).toFixed(1) + '" fill="#6f9076" rx="2"/><g stroke="#cf5a35" stroke-width="2">' + s + '</g></svg></div>';
    };
    $$("input,select", tb).forEach(function (i) { i.addEventListener("input", calcT); });
    calcT();
  }

  /* Sewing unit converter */
  var uc = $("#unit-calc");
  if (uc) {
    var calcU = function () {
      var v = num($("#u-v", uc)), from = $("#u-from", uc).value;
      var toIn = { in: 1, cm: 1 / 2.54, mm: 1 / 25.4, yd: 36, m: 39.3701, ft: 12 }[from];
      var inch = v * toIn;
      var eighths = Math.round(inch * 8) / 8, w = Math.floor(eighths), fr = FRACS.filter(function (f) { return Math.abs(f[0] - (eighths - w)) < 1e-9; })[0];
      var nice = (w ? w : "") + (fr && fr[1] ? (w ? " " : "") + fr[1] : (w ? "" : "0")) + '"';
      $("#u-out", uc).innerHTML = '<div class="lbl">Equals</div><div class="big">' + nice + '</div><ul>' +
        '<li>' + fmt(inch, 3) + ' inches</li><li>' + fmt(inch * 2.54, 2) + ' cm · ' + fmt(inch * 25.4, 1) + ' mm</li>' +
        '<li>' + fmt(inch / 36, 3) + ' yards · ' + fmt(inch * 0.0254, 3) + ' meters</li>' +
        '<li>Nearest common seam allowance: ' + nearestSA(inch) + '</li></ul>';
    };
    var nearestSA = function (inch) {
      var sas = [["¼\" (quilting)", .25], ["⅜\" (garments, some patterns)", .375], ["½\" (bags, home décor)", .5], ["⅝\" (US commercial patterns)", .625], ["1 cm (European patterns)", .3937], ["1.5 cm (European garments)", .5906]];
      var b = sas[0]; sas.forEach(function (s) { if (Math.abs(s[1] - inch) < Math.abs(b[1] - inch)) b = s; });
      return b[0];
    };
    $$("input,select", uc).forEach(function (i) { i.addEventListener("input", calcU); });
    calcU();
  }

  /* No-sew method quiz */
  var qz = $("#nosew-quiz");
  if (qz) {
    var steps = $$(".qstep", qz), qbar = $(".qbar i", qz), score = {}, idx = 0;
    var show = function (i) {
      steps.forEach(function (s, j) { s.classList.toggle("on", j === i); });
      qbar.style.width = (i / (steps.length - 1) * 100) + "%";
    };
    $$(".opt", qz).forEach(function (o) {
      o.addEventListener("click", function () {
        o.getAttribute("data-s").split(",").forEach(function (p) { var kv = p.split(":"); score[kv[0]] = (score[kv[0]] || 0) + parseInt(kv[1], 10); });
        idx++;
        if (idx === steps.length - 1) {
          var best = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; })[0];
          $$(".qres", qz).forEach(function (r) { r.style.display = r.getAttribute("data-r") === best ? "" : "none"; });
        }
        show(idx);
      });
    });
    var again = $(".q-again", qz);
    if (again) again.addEventListener("click", function () { score = {}; idx = 0; show(0); });
    show(0);
  }
})();
