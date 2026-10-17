/* Organized by Anne — interactive tools */
(function () {
  "use strict";
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function store(key, val) {
    try { if (val === undefined) return JSON.parse(localStorage.getItem(key) || "null"); localStorage.setItem(key, JSON.stringify(val)); } catch (e) { return null; }
  }
  function icon(name) { var t = document.getElementById("i-" + name); return t ? t.innerHTML : ""; }

  /* ================= Organizing time estimator ================= */
  var est = $("[data-tool='estimator']");
  if (est) {
    // base hours for one average room of each type at "moderate" clutter, one organizer
    var BASE = { closet: 4, kitchen: 7, pantry: 3, bedroom: 5, bath: 2, office: 5, garage: 9, laundry: 2, kids: 5, living: 4 };
    var LEVEL = { 1: 0.6, 2: 1, 3: 1.6 };
    var state = { level: 2, size: 2, team: 1, counts: {} };
    var saved = store("oba-estimator"); if (saved) state = Object.assign(state, saved);
    $$(".room-row", est).forEach(function (row) {
      var key = row.getAttribute("data-room");
      var out = $("output", row);
      if (state.counts[key] == null) state.counts[key] = 0;
      out.textContent = state.counts[key];
      $$("button", row).forEach(function (b) {
        b.addEventListener("click", function () {
          var n = Math.max(0, Math.min(6, state.counts[key] + parseInt(b.getAttribute("data-step"), 10)));
          state.counts[key] = n; out.textContent = n; calc();
        });
      });
    });
    $$("[data-level]", est).forEach(function (b) {
      b.addEventListener("click", function () { state.level = +b.getAttribute("data-level"); calc(); });
    });
    var size = $("#home-size", est);
    size.value = state.size;
    size.addEventListener("input", function () { state.size = +size.value; calc(); });
    $$("[data-team]", est).forEach(function (b) {
      b.addEventListener("click", function () { state.team = +b.getAttribute("data-team"); calc(); });
    });
    var sizeNames = { 1: "Compact (studio / 1BR condo)", 2: "Average (2–3 bedrooms)", 3: "Spacious (4+ bedrooms)" };
    function calc() {
      $$("[data-level]", est).forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-level") === state.level)); });
      $$("[data-team]", est).forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-team") === state.team)); });
      $("#size-name", est).textContent = sizeNames[state.size];
      var sizeMul = { 1: 0.8, 2: 1, 3: 1.3 }[state.size];
      var total = 0, parts = [];
      Object.keys(state.counts).forEach(function (k) {
        var h = state.counts[k] * BASE[k] * LEVEL[state.level] * sizeMul;
        if (h > 0) parts.push([k, h]);
        total += h;
      });
      var low = Math.round(total * 0.85), high = Math.round(total * 1.2);
      var onsiteLow = Math.max(0, Math.round(low / state.team)), onsiteHigh = Math.max(0, Math.round(high / state.team));
      var res = $(".result-card", est);
      if (total === 0) {
        $(".big", res).innerHTML = "0 <small>hrs</small>";
        $("#sessions", res).textContent = "Add a room or two to see your estimate.";
        $(".bars", res).innerHTML = "";
      } else {
        $(".big", res).innerHTML = low + "–" + high + " <small>organizer hours</small>";
        var days = Math.max(1, Math.ceil(onsiteHigh / 5));
        $("#sessions", res).textContent = "About " + onsiteLow + "–" + onsiteHigh + " hours on site with " + state.team +
          (state.team > 1 ? " organizers" : " organizer") + " — roughly " + days + (days > 1 ? " half-day to full-day sessions." : " session.");
        var max = parts.reduce(function (m, p) { return Math.max(m, p[1]); }, 0);
        var names = { closet: "Closets", kitchen: "Kitchen", pantry: "Pantry", bedroom: "Bedrooms", bath: "Baths", office: "Office", garage: "Garage", laundry: "Laundry", kids: "Kids' rooms", living: "Living" };
        $(".bars", res).innerHTML = parts.sort(function (a, b) { return b[1] - a[1]; }).map(function (p) {
          return '<div class="bar-row"><span>' + names[p[0]] + '</span><span class="track"><span class="fill" data-w="' + (p[1] / max * 100) + '"></span></span><span>' + Math.round(p[1]) + 'h</span></div>';
        }).join("");
        requestAnimationFrame(function () { $$(".fill", res).forEach(function (f) { f.style.width = f.getAttribute("data-w") + "%"; }); });
      }
      store("oba-estimator", state);
    }
    calc();
  }

  /* ================= Declutter decision helper ================= */
  var quiz = $("[data-tool='decision']");
  if (quiz) {
    var Q = JSON.parse($("script[type='application/json']", quiz).textContent);
    var stage = $(".quiz-stage", quiz), bar = $(".quiz-progress span", quiz);
    var hist = [];
    function show(id) {
      var node = Q.nodes[id];
      if (node.verdict) return verdict(node);
      bar.style.width = Math.min(90, hist.length * 22 + 10) + "%";
      stage.innerHTML = '<div class="quiz-q"><span class="eyebrow">Question ' + (hist.length + 1) + '</span><h3></h3><div class="quiz-opts"></div>' +
        '<div class="quiz-nav">' + (hist.length ? '<button type="button" class="link-btn" data-back>' + icon("rotate-ccw") + ' Back</button>' : '<span></span>') + '</div></div>';
      $("h3", stage).textContent = node.q;
      var opts = $(".quiz-opts", stage);
      node.a.forEach(function (o, i) {
        var b = document.createElement("button");
        b.type = "button";
        b.innerHTML = '<span class="k">' + String.fromCharCode(65 + i) + '</span><span></span>';
        b.lastChild.textContent = o[0];
        b.addEventListener("click", function () { hist.push(id); show(o[1]); });
        opts.appendChild(b);
      });
      var back = $("[data-back]", stage);
      if (back) back.addEventListener("click", function () { show(hist.pop()); });
      var first = $("button", opts); if (first && hist.length) first.focus({ preventScroll: true });
    }
    function verdict(v) {
      bar.style.width = "100%";
      var V = Q.verdicts[v.verdict];
      stage.innerHTML = '<div class="verdict" role="status"><div class="vi" style="background:' + V.color + '">' + icon(V.icon) + '</div>' +
        '<span class="eyebrow">Our verdict</span><h3></h3><p class="lead"></p><div class="quiz-nav" style="justify-content:center;gap:12px;flex-wrap:wrap">' +
        '<button type="button" class="btn" data-restart>' + icon("refresh-cw") + ' Try another item</button>' +
        '<button type="button" class="btn btn-ghost" data-back>' + icon("rotate-ccw") + ' Change my answer</button></div></div>';
      $("h3", stage).textContent = V.title;
      $("p", stage).textContent = v.why + " " + V.next;
      $("[data-restart]", stage).addEventListener("click", function () { hist = []; show("start"); });
      $("[data-back]", stage).addEventListener("click", function () { show(hist.pop()); });
      var tally = store("oba-decisions") || {}; tally[v.verdict] = (tally[v.verdict] || 0) + 1; store("oba-decisions", tally);
      renderTally();
    }
    function renderTally() {
      var t = store("oba-decisions") || {};
      $$("[data-tally]", quiz).forEach(function (el) { el.textContent = t[el.getAttribute("data-tally")] || 0; });
    }
    var reset = $("[data-reset-tally]", quiz);
    if (reset) reset.addEventListener("click", function () { store("oba-decisions", {}); renderTally(); });
    renderTally();
    show("start");
  }

  /* ================= 30-day challenge ================= */
  var ch = $("[data-tool='challenge']");
  if (ch) {
    var boxes = $$(".day input", ch);
    var done = store("oba-challenge") || [];
    boxes.forEach(function (b, i) { b.checked = done.indexOf(i + 1) > -1; });
    var fg = $(".ring .fg", ch), txt = $(".ring text", ch), msg = $("#challenge-msg", ch);
    var C = 2 * Math.PI * 52;
    fg.style.strokeDasharray = C;
    function upd(celebrate) {
      var n = boxes.filter(function (b) { return b.checked; }).length;
      fg.style.strokeDashoffset = C * (1 - n / boxes.length);
      txt.textContent = n + "/" + boxes.length;
      var lines = ["Pick a day and start small — fifteen minutes counts.", "Great start. Momentum beats motivation.", "You're building the habit. Keep going!", "Over halfway — your home is breathing easier.", "Almost there. The finish line is in sight!", "You did it! Thirty days of calmer spaces."];
      msg.textContent = lines[n === boxes.length ? 5 : Math.min(4, Math.ceil(n / 7.5))];
      store("oba-challenge", boxes.map(function (b, i) { return b.checked ? i + 1 : 0; }).filter(Boolean));
      if (celebrate && (n === boxes.length || n % 10 === 0) && n > 0) confetti();
    }
    boxes.forEach(function (b) { b.addEventListener("change", function () { upd(b.checked); }); });
    var rs = $("[data-reset]", ch);
    if (rs) rs.addEventListener("click", function () { if (confirm("Reset your 30-day progress?")) { boxes.forEach(function (b) { b.checked = false; }); upd(false); } });
    var pr = $("[data-print]", ch);
    if (pr) pr.addEventListener("click", function () { window.print(); });
    upd(false);
  }

  function confetti() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var wrap = document.createElement("div"); wrap.className = "confetti";
    var colors = ["#c4785a", "#7d917b", "#efd3c4", "#b99a66", "#4d614f"];
    for (var i = 0; i < 90; i++) {
      var p = document.createElement("i");
      p.style.left = Math.random() * 100 + "%";
      p.style.background = colors[i % colors.length];
      p.style.animationDuration = (2 + Math.random() * 2.5) + "s";
      p.style.animationDelay = (Math.random() * 0.6) + "s";
      p.style.transform = "rotate(" + (Math.random() * 360) + "deg)";
      wrap.appendChild(p);
    }
    document.body.appendChild(wrap);
    setTimeout(function () { wrap.remove(); }, 5500);
  }

  /* ================= Closet rod calculator ================= */
  var rod = $("[data-tool='rod']");
  if (rod) {
    // inches of rod per hanging item (on slim/velvet hangers vs standard)
    var W = { shirts: 1, pants: 1.25, dresses: 1.5, jackets: 2.5, coats: 4, suits: 3 };
    var HANG = { shirts: 38, pants: 30, dresses: 60, jackets: 38, coats: 48, suits: 42 };
    var COL = { shirts: "#7d917b", pants: "#4d614f", dresses: "#c4785a", jackets: "#b99a66", coats: "#2a2724", suits: "#857c72" };
    var inputs = $$("input[type='number'][name]", rod);
    var hanger = $("#hanger", rod), existing = $("#existing", rod);
    var saved2 = store("oba-rod");
    if (saved2) { inputs.forEach(function (i) { if (saved2[i.name] != null) i.value = saved2[i.name]; }); if (saved2.hanger) hanger.value = saved2.hanger; if (saved2.existing != null) existing.value = saved2.existing; }
    function calcRod() {
      var mult = { slim: 1, standard: 1.35, wood: 1.6 }[hanger.value];
      var total = 0, items = [], longest = 0, data = { hanger: hanger.value, existing: existing.value };
      inputs.forEach(function (i) {
        var n = Math.max(0, parseInt(i.value, 10) || 0); data[i.name] = n;
        total += n * W[i.name] * mult;
        if (n) longest = Math.max(longest, HANG[i.name]);
        for (var k = 0; k < Math.min(n, 60); k++) items.push(i.name);
      });
      var withRoom = total * 1.15; // breathing room so hangers slide
      var ft = withRoom / 12;
      var res = $(".result-card", rod);
      $(".big", res).innerHTML = (Math.round(ft * 10) / 10) + " <small>feet of rod</small>";
      var have = parseFloat(existing.value) || 0;
      var gap = $("#rod-gap", res);
      if (!have) gap.textContent = "Enter your current rod length to see if it fits.";
      else if (have >= ft) gap.textContent = "Your " + have + " ft of rod fits everything, with about " + (Math.round((have - ft) * 10) / 10) + " ft to spare.";
      else gap.textContent = "You're about " + (Math.round((ft - have) * 10) / 10) + " ft short. A double-hang section or a quick edit could close the gap.";
      $("#rod-drop", res).textContent = longest ? "Longest item needs ~" + longest + "\" of drop — " + (longest <= 40 ? "perfect for double-hang rods." : "plan at least one long-hang section.") : "";
      var viz = $(".rod-viz", rod);
      viz.innerHTML = "";
      var step = 100 / Math.max(items.length, 1);
      items.forEach(function (name, idx) {
        var h = document.createElement("span"); h.className = "hanger";
        h.style.left = (idx * step + step / 2) + "%";
        h.style.setProperty("--c", COL[name]);
        h.style.setProperty("--h", Math.round(HANG[name] * 1.4) + "px");
        viz.appendChild(h);
      });
      viz.style.height = (longest ? Math.round(longest * 1.4) + 20 : 40) + "px";
      store("oba-rod", data);
    }
    $$("input, select", rod).forEach(function (i) { i.addEventListener("input", calcRod); });
    calcRod();
  }
})();
