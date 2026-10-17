/* Oh, Mother Mine DIY — interactive DIY tools. Each tool boots from its data-tool root. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var num = function (el, d) { var v = parseFloat(el && el.value); return isNaN(v) ? (d || 0) : v; };
  function pop(el) { if (!el) return; el.classList.remove("pop"); void el.offsetWidth; el.classList.add("pop"); }
  function money(v) { return "$" + Math.round(v).toLocaleString("en-US"); }
  function bindOutputs(root) {
    $$("input[type=range][data-out]", root).forEach(function (r) {
      var o = $("#" + r.getAttribute("data-out"));
      var fmt = function () { if (o) o.textContent = (r.getAttribute("data-prefix") || "") + r.value + (r.getAttribute("data-unit") || ""); };
      r.addEventListener("input", fmt); fmt();
    });
  }
  function seg(root, name, cb) {
    var btns = $$('[data-seg="' + name + '"] button', root);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        cb(b.getAttribute("data-val"));
      });
    });
  }

  /* =================== Paint calculator =================== */
  var pc = $('[data-tool="paint"]');
  if (pc) {
    var mode = "walls";
    var furniture = { "side-table": 14, "nightstand": 18, "chair": 12, "coffee-table": 22, "dining-table": 34, "bookshelf": 42, "dresser": 52, "buffet": 60, "kitchen-island": 70 };
    bindOutputs(pc);
    seg(pc, "mode", function (v) {
      mode = v;
      var price = $("#pc-price", pc), lbl = $('label[for="pc-price"]', pc);
      lbl.textContent = v === "furniture" ? "Price per quart ($)" : "Price per gallon ($)";
      price.value = v === "furniture" ? 28 : 40;
      $$("[data-mode-panel]", pc).forEach(function (p) { p.hidden = p.getAttribute("data-mode-panel") !== v; });
      calc();
    });
    function cansHTML(gal, qt) {
      var color = (pc.querySelector("input[name=swatch]:checked") || {}).value || "#c8553d", h = "", i;
      for (i = 0; i < Math.min(gal, 14); i++) h += '<span class="can" style="--swatch:' + color + ';animation-delay:' + (i * 0.06) + 's"></span>';
      for (i = 0; i < qt; i++) h += '<span class="can small" style="--swatch:' + color + ';animation-delay:' + ((gal + i) * 0.06) + 's"></span>';
      return h;
    }
    function calc() {
      var coats = num($("#pc-coats", pc), 2), price = num($("#pc-price", pc), 40), out = $("#pc-big", pc), unit = $("#pc-unit", pc), list = $("#pc-list", pc), cans = $("#pc-cans", pc);
      if (mode === "furniture") {
        var area = (furniture[$("#pc-piece", pc).value] || 20) * num($("#pc-qty", pc), 1);
        if ($("#pc-inside", pc).checked) area *= 1.35;
        var cover = 150; /* sq ft per quart, typical chalk-style furniture paint */
        var quarts = area * coats / cover;
        var q = Math.max(1, Math.ceil(quarts * 1.1 * 2) / 2);
        out.textContent = q % 1 ? q.toFixed(1) : q; unit.textContent = q === 1 ? "quart" : "quarts";
        list.innerHTML = "<li><span>Paintable surface</span><b>" + Math.round(area) + " sq ft</b></li>" +
          "<li><span>Coats</span><b>" + coats + "</b></li>" +
          "<li><span>Includes 10% extra for touch-ups</span><b>✓</b></li>" +
          "<li><span>Estimated paint cost</span><b>" + money(Math.ceil(q) * price) + "</b></li>";
        cans.innerHTML = cansHTML(0, Math.ceil(q));
      } else {
        var L = num($("#pc-len", pc), 12), W = num($("#pc-wid", pc), 12), H = num($("#pc-ht", pc), 8);
        var doors = num($("#pc-doors", pc), 1), wins = num($("#pc-wins", pc), 2);
        var wall = 2 * (L + W) * H - doors * 20 - wins * 15;
        if ($("#pc-ceiling", pc).checked) wall += L * W;
        wall = Math.max(0, wall);
        var coverage = num($("#pc-surface", pc), 375);
        var gallons = wall * coats / coverage;
        var primer = $("#pc-primer", pc).checked ? wall / 300 : 0;
        var g = Math.floor(gallons), rem = gallons - g, qts = Math.ceil(rem * 4 - 0.05);
        if (qts >= 3) { g += 1; qts = 0; }
        if (g === 0 && qts === 0) qts = 1;
        out.textContent = (Math.ceil(gallons * 10) / 10).toFixed(1); unit.textContent = "gallons of paint";
        list.innerHTML = "<li><span>Paintable area</span><b>" + Math.round(wall) + " sq ft</b></li>" +
          "<li><span>Buy</span><b>" + (g ? g + " gal" : "") + (g && qts ? " + " : "") + (qts ? qts + " qt" : "") + "</b></li>" +
          (primer ? "<li><span>Primer</span><b>" + (Math.ceil(primer * 4) / 4).toFixed(2) + " gal</b></li>" : "") +
          "<li><span>Estimated paint cost</span><b>" + money(g * price + qts * price / 3.2 + Math.ceil(primer) * price * 0.7) + "</b></li>";
        cans.innerHTML = cansHTML(g, qts);
      }
      pop(out);
    }
    pc.addEventListener("input", calc);
    pc.addEventListener("change", calc);
    calc();
  }

  /* =================== Chalk paint mixer =================== */
  var cm = $('[data-tool="chalk"]');
  if (cm) {
    /* amounts per 1 cup of flat/eggshell latex paint */
    var recipes = {
      plaster: { name: "Plaster of Paris", add: [["plaster of Paris", 1 / 3], ["cool water", 1 / 3]], note: "Stir the plaster into the cool water until it's lump-free and smooth like pancake batter, then mix it into the paint. Use within a day — plaster sets up over time." },
      calcium: { name: "Calcium carbonate", add: [["calcium carbonate powder", 1 / 3], ["water", 2.5 / 16]], note: "Make a paste with the water first, then stir it into the paint. Smooth, and it keeps a little longer than the plaster version." },
      soda: { name: "Baking soda", add: [["baking soda", 1 / 8]], note: "Sift the baking soda and stir it straight in a little at a time. Easiest to find — expect a slightly grittier texture, so sand lightly between coats." }
    };
    var current = "plaster";
    bindOutputs(cm);
    seg(cm, "recipe", function (v) { current = v; mix(); });
    function measure(cups) {
      if (cups >= 0.24) {
        var whole = Math.floor(cups), frac = cups - whole, fracs = [[0, ""], [0.125, "⅛"], [0.25, "¼"], [1 / 3, "⅓"], [0.375, "⅜"], [0.5, "½"], [0.625, "⅝"], [2 / 3, "⅔"], [0.75, "¾"], [0.875, "⅞"], [1, ""]], best = fracs[0];
        fracs.forEach(function (f) { if (Math.abs(f[0] - frac) < Math.abs(best[0] - frac)) best = f; });
        if (best[0] === 1) { whole += 1; best = fracs[0]; }
        return (whole ? whole + (best[1] ? " " : "") : "") + best[1] + (whole > 1 || (whole === 1 && best[1]) ? " cups" : " cup");
      }
      var tbsp = cups * 16;
      if (tbsp >= 0.9) return (Math.round(tbsp * 2) / 2) + " tbsp";
      return Math.max(1, Math.round(tbsp * 3)) + " tsp";
    }
    function mix() {
      var cups = num($("#cm-cups", cm), 2), r = recipes[current];
      var rows = "<li><span>Flat or eggshell latex paint</span><b>" + measure(cups) + "</b></li>";
      r.add.forEach(function (a) { rows += "<li><span>" + a[0].charAt(0).toUpperCase() + a[0].slice(1) + "</span><b>" + measure(a[1] * cups) + "</b></li>"; });
      $("#cm-list", cm).innerHTML = rows;
      $("#cm-note", cm).textContent = r.note;
      var sq = Math.round(cups * 22);
      var big = $("#cm-big", cm); big.textContent = sq; pop(big);
      var fits = sq < 30 ? "a picture frame or small stool" : sq < 60 ? "a side table or nightstand (2 coats)" : sq < 110 ? "a chair set or coffee table (2 coats)" : sq < 170 ? "a 6-drawer dresser (2 coats)" : "a buffet or several pieces";
      $("#cm-fits", cm).textContent = fits;
      var jar = $("#cm-jar-fill", cm);
      if (jar) jar.setAttribute("height", Math.min(150, 20 + cups * 16)), jar.setAttribute("y", 190 - Math.min(150, 20 + cups * 16));
      var color = (cm.querySelector("input[name=swatch]:checked") || {}).value;
      if (color && jar) jar.setAttribute("fill", color);
    }
    cm.addEventListener("input", mix);
    cm.addEventListener("change", mix);
    mix();
  }

  /* =================== Project finder quiz =================== */
  var qz = $('[data-tool="quiz"]');
  if (qz) {
    var posts = JSON.parse($("#quiz-data").textContent);
    var steps = $$(".q-step", qz), bar = $(".quiz-progress i", qz), answers = {}, idx = 0;
    function show(i) {
      idx = i;
      steps.forEach(function (s, j) { s.classList.toggle("active", j === i); });
      bar.style.width = (i / (steps.length - 1) * 100) + "%";
      var h = steps[i].querySelector("h2"); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      qz.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    $$(".q-opt", qz).forEach(function (b) {
      b.addEventListener("click", function () {
        answers[b.closest(".q-step").getAttribute("data-q")] = b.getAttribute("data-val");
        if (idx + 1 === steps.length - 1) results();
        show(idx + 1);
      });
    });
    $$(".q-back", qz).forEach(function (b) { b.addEventListener("click", function () { show(Math.max(0, idx - 1)); }); });
    var restart = $(".q-restart", qz); if (restart) restart.addEventListener("click", function () { answers = {}; show(0); });
    function results() {
      var scored = posts.map(function (p) {
        var s = 0, cost = parseFloat(String(p.cost).replace(/[^0-9.]/g, "")) || 0;
        var hours = /min/i.test(p.time) ? 0.5 : parseFloat(String(p.time).replace(/[^0-9.]/g, "")) || 1;
        if (/day|weekend/i.test(p.time)) hours = 8;
        if (answers.who === "kids") s += p.cat === "kids-crafts" ? 6 : (p.diff === "Easy" ? 2 : -2);
        if (answers.who === "gift") s += p.cat === "handmade-gifts" ? 6 : (p.cat === "holiday-decor" ? 2 : 0);
        if (answers.who === "home") s += (p.cat === "home-decor" || p.cat === "furniture-makeovers" || p.cat === "home-organization") ? 3 : 0;
        if (answers.time === "quick") s += hours <= 1.5 ? 4 : hours <= 3 ? 1 : -3;
        if (answers.time === "afternoon") s += hours > 1 && hours <= 5 ? 3 : 0;
        if (answers.time === "weekend") s += hours >= 4 ? 3 : 0;
        if (answers.budget === "low") s += cost <= 15 ? 4 : cost <= 30 ? 1 : -3;
        if (answers.budget === "mid") s += cost > 10 && cost <= 60 ? 3 : 0;
        if (answers.budget === "high") s += cost > 40 ? 3 : 1;
        if (answers.vibe === "farmhouse") s += /furniture|wreath|farmhouse|distress|chalk/i.test(p.slug) ? 4 : 0;
        if (answers.vibe === "seasonal") s += p.cat === "holiday-decor" ? 5 : 0;
        if (answers.vibe === "organized") s += p.cat === "home-organization" ? 5 : 0;
        if (answers.vibe === "fresh") s += /terracotta|color|mason|budget|dollar|candle/i.test(p.slug) ? 4 : 0;
        return { p: p, s: s };
      }).sort(function (a, b) { return b.s - a.s; }).slice(0, 3);
      $("#quiz-results", qz).innerHTML = scored.map(function (x, i) {
        var p = x.p;
        return '<article class="card reveal in" style="--d:' + (i * 0.12) + 's"><a class="card-media" href="' + p.url + '"><img src="' + p.img + '" alt="' + p.alt.replace(/"/g, "&quot;") + '" loading="lazy" width="720" height="480"><span class="card-tag">' + (i === 0 ? "Best match" : "Great fit") + '</span></a>' +
          '<div class="card-body"><div class="card-meta"><span class="diff ' + p.diff.toLowerCase() + '">' + p.diff + '</span><span>' + p.time + '</span><span>' + p.cost + '</span></div>' +
          '<h3><a href="' + p.url + '">' + p.title + '</a></h3><p>' + p.excerpt + '</p><a class="more" href="' + p.url + '">Start this project →</a></div></article>';
      }).join("");
    }
    show(0);
  }

  /* =================== Makeover budget planner =================== */
  var bp = $('[data-tool="budget"]');
  if (bp) {
    var presets = {
      living: [["Paint + supplies", 70, 70], ["Thrifted coffee table makeover", 45, 280], ["DIY throw pillow covers (4)", 30, 120], ["Gallery wall frames", 40, 160], ["Plants + terracotta pots", 35, 90], ["Curtains + rod", 60, 110]],
      bedroom: [["Paint + supplies", 60, 60], ["Painted dresser makeover", 55, 450], ["Upholstered headboard (DIY)", 80, 350], ["Lamp shade refresh", 15, 60], ["Bedding layers", 90, 160], ["Wall art (printables)", 20, 120]],
      kitchen: [["Cabinet paint + primer", 120, 120], ["New cabinet hardware", 60, 60], ["Open shelf (DIY)", 45, 180], ["Peel-and-stick backsplash", 90, 400], ["Organizers + labels", 30, 85]],
      kids: [["Paint + accent wall", 55, 55], ["Toy storage cubbies (upcycled)", 40, 180], ["Reading nook canopy", 25, 90], ["Kids' art display wall", 15, 70], ["Rug", 70, 120]],
      porch: [["Door paint", 30, 30], ["Seasonal wreath (DIY)", 25, 85], ["Planters + mums", 45, 90], ["Painted welcome sign", 15, 60], ["Outdoor pillow covers", 25, 70], ["String lights", 25, 25]]
    };
    var rows = $("#bp-rows", bp);
    bindOutputs(bp);
    function rowHTML(r) {
      return '<div class="budget-row"><input aria-label="Item" value="' + r[0].replace(/"/g, "&quot;") + '"><input aria-label="DIY cost" type="number" min="0" step="5" value="' + r[1] + '"><input aria-label="Store-bought cost" type="number" min="0" step="5" value="' + r[2] + '"><button type="button" class="rm" aria-label="Remove item">×</button></div>';
    }
    function load(room) { rows.innerHTML = presets[room].map(rowHTML).join(""); calc(); }
    rows.addEventListener("click", function (e) { if (e.target.classList.contains("rm")) { e.target.parentNode.remove(); calc(); } });
    $("#bp-add", bp).addEventListener("click", function () { rows.insertAdjacentHTML("beforeend", rowHTML(["New item", 20, 50])); rows.lastElementChild.querySelector("input").select(); calc(); });
    $("#bp-room", bp).addEventListener("change", function () { load(this.value); });
    function calc() {
      var budget = num($("#bp-budget", bp), 400), diy = 0, store = 0;
      $$(".budget-row", rows).forEach(function (r) { var i = r.querySelectorAll("input"); diy += num(i[1]); store += num(i[2]); });
      var buffer = $("#bp-buffer", bp).checked ? diy * 0.1 : 0, total = diy + buffer, left = budget - total, saved = Math.max(0, store - total);
      var big = $("#bp-big", bp); big.textContent = money(total); pop(big);
      var pct = Math.min(100, total / Math.max(1, budget) * 100), m = $("#bp-meter", bp);
      m.style.width = pct + "%"; m.classList.toggle("over", left < 0);
      $("#bp-status", bp).textContent = left >= 0 ? money(left) + " left in your budget" : money(-left) + " over budget — trim an item or two";
      $("#bp-list", bp).innerHTML = "<li><span>DIY items</span><b>" + money(diy) + "</b></li>" + (buffer ? "<li><span>10% oops buffer</span><b>" + money(buffer) + "</b></li>" : "") +
        "<li><span>Store-bought equivalent</span><b>" + money(store) + "</b></li><li><span>You save by DIYing</span><b style=\"color:var(--mustard)\">" + money(saved) + "</b></li>";
      var C = 2 * Math.PI * 60, frac = store ? Math.min(1, total / store) : 0;
      $("#bp-donut-diy", bp).setAttribute("stroke-dasharray", (C * frac) + " " + C);
      $("#bp-donut-label", bp).textContent = store ? Math.round(saved / store * 100) + "%" : "0%";
    }
    bp.addEventListener("input", calc);
    $("#bp-buffer", bp).addEventListener("change", calc);
    load("living");
  }

  /* =================== Color palette generator =================== */
  var cp = $('[data-tool="palette"]');
  if (cp) {
    var harmony = "analogous";
    function hexToHsl(hex) {
      var r = parseInt(hex.substr(1, 2), 16) / 255, g = parseInt(hex.substr(3, 2), 16) / 255, b = parseInt(hex.substr(5, 2), 16) / 255;
      var mx = Math.max(r, g, b), mn = Math.min(r, g, b), h = 0, s = 0, l = (mx + mn) / 2;
      if (mx !== mn) { var d = mx - mn; s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; }
      return [h, s * 100, l * 100];
    }
    function hslToHex(h, s, l) {
      h = ((h % 360) + 360) % 360; s = Math.max(0, Math.min(100, s)) / 100; l = Math.max(0, Math.min(100, l)) / 100;
      var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l);
      var f = function (n) { return Math.round(255 * (l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))))).toString(16).padStart(2, "0"); };
      return "#" + f(0) + f(8) + f(4);
    }
    function lum(hex) { var c = [1, 3, 5].map(function (i) { var v = parseInt(hex.substr(i, 2), 16) / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
    var names = [[0, "Rose"], [15, "Terracotta"], [30, "Clay"], [42, "Honey"], [55, "Mustard"], [75, "Olive"], [110, "Sage"], [160, "Eucalyptus"], [190, "Lagoon"], [210, "Denim"], [235, "Indigo"], [270, "Lavender"], [300, "Plum"], [335, "Berry"], [360, "Rose"]];
    function nameOf(hex) {
      var hsl = hexToHsl(hex), base = names.reduce(function (a, b) { return Math.abs(b[0] - hsl[0]) < Math.abs(a[0] - hsl[0]) ? b : a; })[1];
      if (hsl[1] < 12) base = hsl[2] > 85 ? "Linen" : hsl[2] > 60 ? "Greige" : hsl[2] > 30 ? "Stone" : "Charcoal";
      var pre = hsl[2] > 82 ? "Whisper " : hsl[2] > 65 ? "Soft " : hsl[2] < 28 ? "Deep " : "";
      return pre + base;
    }
    function build(base) {
      var hsl = hexToHsl(base), h = hsl[0], s = hsl[1], l = hsl[2], out;
      switch (harmony) {
        case "complementary": out = [[h, s, l], [h, s * 0.4, 92], [h + 180, s * 0.8, l], [h + 180, s * 0.35, 80], [h, s * 0.5, 22]]; break;
        case "triadic": out = [[h, s, l], [h + 120, s * 0.7, l + 5], [h + 240, s * 0.7, l + 5], [h, s * 0.2, 94], [h + 240, s * 0.3, 22]]; break;
        case "split": out = [[h, s, l], [h + 150, s * 0.7, l], [h + 210, s * 0.7, l], [h, s * 0.25, 93], [h + 180, s * 0.25, 24]]; break;
        case "mono": out = [[h, s, 94], [h, s * 0.9, 78], [h, s, l], [h, s, Math.max(12, l - 22)], [h, s * 0.6, 14]]; break;
        default: out = [[h - 30, s * 0.8, l + 8], [h - 15, s * 0.9, l + 2], [h, s, l], [h + 15, s * 0.9, l - 6], [h, s * 0.25, 93]];
      }
      return out.map(function (c) { return hslToHex(c[0], c[1], Math.max(8, Math.min(96, c[2]))); });
    }
    function render() {
      var base = $("#cp-base", cp).value, pal = build(base), box = $("#cp-palette", cp);
      box.innerHTML = pal.map(function (c) { var dark = lum(c) > 0.45; return '<button type="button" style="--c:' + c + ';--tx:' + (dark ? "#2a1f1a" : "#fff") + '" data-hex="' + c + '" aria-label="Copy ' + c + '">' + nameOf(c) + "<small>" + c.toUpperCase() + "</small></button>"; }).join("");
      /* 60-30-10: lightest = walls, mid = big furniture, base = accent */
      var byL = pal.slice().sort(function (a, b) { return lum(b) - lum(a); });
      var set = function (id, c) { var el = $("#" + id, cp); if (el) el.setAttribute("fill", c); };
      set("rp-wall", byL[0]); set("rp-sofa", byL[2]); set("rp-rug", byL[1]); set("rp-pillow", base); set("rp-art", byL[3]); set("rp-vase", byL[4]); set("rp-floor", hslToHex(hexToHsl(byL[4])[0], 20, 32));
      $("#cp-hex", cp).textContent = base.toUpperCase();
      $("#cp-tips", cp).innerHTML = "<li><span>Walls (60%)</span><b>" + nameOf(byL[0]) + "</b></li><li><span>Big pieces (30%)</span><b>" + nameOf(byL[2]) + "</b></li><li><span>Accents (10%)</span><b>" + nameOf(base) + "</b></li>";
    }
    $("#cp-palette", cp).addEventListener("click", function (e) {
      var b = e.target.closest("button[data-hex]"); if (!b) return;
      var hex = b.getAttribute("data-hex").toUpperCase();
      if (navigator.clipboard) navigator.clipboard.writeText(hex).then(function () { window.OMM.toast(hex + " copied!"); }, function () { window.OMM.toast(hex); });
      else window.OMM.toast(hex);
    });
    seg(cp, "harmony", function (v) { harmony = v; render(); });
    $("#cp-base", cp).addEventListener("input", render);
    $$("[data-preset]", cp).forEach(function (b) { b.addEventListener("click", function () { $("#cp-base", cp).value = b.getAttribute("data-preset"); render(); }); });
    $("#cp-random", cp).addEventListener("click", function () {
      $("#cp-base", cp).value = hslToHex(Math.random() * 360, 35 + Math.random() * 40, 40 + Math.random() * 25);
      var modes = ["analogous", "complementary", "triadic", "split", "mono"]; harmony = modes[Math.floor(Math.random() * modes.length)];
      $$('[data-seg="harmony"] button', cp).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-val") === harmony ? "true" : "false"); });
      render();
    });
    render();
  }
})();
