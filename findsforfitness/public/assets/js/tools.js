/* findsforfitness.com - interactive tools */
(function () {
  "use strict";
  function $(root, sel) { return root.querySelector(sel); }
  function num(form, name) { var el = form.elements[name]; return el ? parseFloat(el.value) || 0 : 0; }
  function radio(form, name) { var el = form.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : ""; }
  function fmt(n) { return Math.round(n).toLocaleString("en-US"); }
  function unitToggle(form) {
    var u = radio(form, "units");
    form.querySelectorAll("[data-units]").forEach(function (row) { row.hidden = row.getAttribute("data-units") !== u; });
    return u;
  }
  function bind(form, fn) {
    form.addEventListener("input", fn);
    form.addEventListener("change", fn);
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    fn();
  }

  /* ---------- BMI ---------- */
  var bmiForm = document.querySelector('[data-tool="bmi"]');
  if (bmiForm) {
    var panel = bmiForm.closest(".tool-panel");
    bind(bmiForm, function () {
      var u = unitToggle(bmiForm), hM, kg;
      if (u === "imperial") { hM = (num(bmiForm, "ft") * 12 + num(bmiForm, "in")) * 0.0254; kg = num(bmiForm, "lb") * 0.453592; }
      else { hM = num(bmiForm, "cm") / 100; kg = num(bmiForm, "kg"); }
      if (hM < 0.9 || kg < 20) return;
      var bmi = kg / (hM * hM);
      var cat = bmi < 18.5 ? "Underweight" : bmi < 25 ? "Healthy weight" : bmi < 30 ? "Overweight" : "Obesity";
      var lo = 18.5 * hM * hM, hi = 24.9 * hM * hM;
      $(panel, "[data-bmi-value]").textContent = bmi.toFixed(1);
      $(panel, "[data-bmi-cat]").textContent = cat;
      $(panel, "[data-bmi-range]").textContent = u === "imperial"
        ? fmt(lo / 0.453592) + " - " + fmt(hi / 0.453592) + " lb" : lo.toFixed(1) + " - " + hi.toFixed(1) + " kg";
      var x = Math.max(0, Math.min(100, (bmi - 15) / 25 * 100));
      $(panel, "[data-bmi-needle]").style.setProperty("--x", x + "%");
    });
  }

  /* ---------- Calories (Mifflin-St Jeor) ---------- */
  var calForm = document.querySelector('[data-tool="calories"]');
  if (calForm) {
    var cp = calForm.closest(".tool-panel");
    bind(calForm, function () {
      var u = unitToggle(calForm), cm, kg;
      if (u === "imperial") { cm = (num(calForm, "ft") * 12 + num(calForm, "in")) * 2.54; kg = num(calForm, "lb") * 0.453592; }
      else { cm = num(calForm, "cm"); kg = num(calForm, "kg"); }
      var age = num(calForm, "age");
      if (cm < 100 || kg < 25 || age < 10) return;
      var bmr = 10 * kg + 6.25 * cm - 5 * age + (radio(calForm, "sex") === "m" ? 5 : -161);
      var tdee = bmr * parseFloat(calForm.elements.activity.value);
      var floor = radio(calForm, "sex") === "m" ? 1500 : 1200;
      var lose = Math.max(floor, tdee * 0.8), gain = tdee * 1.1;
      var set = function (k, v) { $(cp, '[data-cal="' + k + '"]').textContent = fmt(v); };
      set("bmr", bmr); set("tdee", tdee); set("lose", lose); set("keep", tdee); set("gain", gain);
      var p = Math.min(kg * 2, lose * 0.35 / 4), f = lose * 0.28 / 9, c = Math.max(0, (lose - p * 4 - f * 9) / 4);
      var tot = p * 4 + c * 4 + f * 9;
      [["p", p * 4], ["c", c * 4], ["f", f * 9]].forEach(function (m) { $(cp, '[data-macro="' + m[0] + '"]').style.width = (m[1] / tot * 100) + "%"; });
      $(cp, '[data-macro-g="p"]').textContent = fmt(p) + " g";
      $(cp, '[data-macro-g="c"]').textContent = fmt(c) + " g";
      $(cp, '[data-macro-g="f"]').textContent = fmt(f) + " g";
    });
  }

  /* ---------- Protein ---------- */
  var proForm = document.querySelector('[data-tool="protein"]');
  if (proForm) {
    var pp = proForm.closest(".tool-panel");
    var foods = [["Chicken breast", 31, "100 g / 3.5 oz"], ["Greek yogurt", 17, "170 g cup"], ["Eggs", 6, "1 large egg"],
      ["Salmon", 25, "100 g / 3.5 oz"], ["Firm tofu", 15, "120 g / half block"], ["Lentils (cooked)", 18, "1 cup"],
      ["Cottage cheese", 14, "1/2 cup"], ["Tuna (canned)", 20, "1 small can, drained"]];
    bind(proForm, function () {
      var w = num(proForm, "w"), kg = radio(proForm, "unit") === "lb" ? w * 0.453592 : w;
      var g = proForm.elements.goal.value.split(",").map(parseFloat);
      var meals = num(proForm, "meals");
      $(pp, "[data-out-meals]").textContent = meals;
      if (kg < 20) return;
      var lo = kg * g[0], hi = kg * g[1], mid = (lo + hi) / 2;
      $(pp, '[data-pro="day"]').textContent = fmt(lo) + " - " + fmt(hi) + " g";
      $(pp, '[data-pro="meal"]').textContent = "~" + fmt(mid / meals) + " g";
      var per = mid / meals, ul = $(pp, '[data-pro="foods"]');
      ul.innerHTML = "";
      foods.slice(0, 6).forEach(function (f, i) {
        var li = document.createElement("li");
        var n = per / f[1];
        li.textContent = f[0] + ": " + (n < 1.15 ? "1 x " : n.toFixed(1) + " x ") + f[2];
        li.style.animationDelay = i * 50 + "ms";
        ul.appendChild(li);
      });
    });
  }

  /* ---------- Water ---------- */
  var waterForm = document.querySelector('[data-tool="water"]');
  if (waterForm) {
    var wp = waterForm.closest(".tool-panel");
    var key = "ffs-water-" + new Date().toISOString().slice(0, 10);
    var drunk = 0;
    try { drunk = parseInt(localStorage.getItem(key), 10) || 0; } catch (e) { /* storage unavailable */ }
    var goalCups = 8;
    var glassesEl = $(wp, "[data-water-glasses]");
    function renderGlasses() {
      glassesEl.innerHTML = "";
      for (var i = 0; i < goalCups; i++) {
        var b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", "Glass " + (i + 1) + (i < drunk ? " (done)" : ""));
        if (i < drunk) b.className = "is-full";
        b.dataset.i = i;
        glassesEl.appendChild(b);
      }
      var pct = Math.min(100, Math.round(drunk / goalCups * 100));
      $(wp, "[data-water-fill]").style.height = pct + "%";
      $(wp, "[data-water-pct]").textContent = pct + "%";
    }
    function save() { try { localStorage.setItem(key, drunk); } catch (e) { /* ignore */ } }
    glassesEl.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      var i = parseInt(b.dataset.i, 10);
      drunk = i < drunk ? i : i + 1;
      save(); renderGlasses();
    });
    $(wp, "[data-water-reset]").addEventListener("click", function () { drunk = 0; save(); renderGlasses(); });
    bind(waterForm, function () {
      var w = num(waterForm, "w"), lb = radio(waterForm, "unit") === "lb" ? w : w / 0.453592;
      var ex = num(waterForm, "ex");
      $(wp, "[data-out-ex]").textContent = ex;
      if (lb < 50) return;
      var oz = lb * 0.5 + ex / 30 * 12 + (waterForm.elements.hot.checked ? 16 : 0);
      $(wp, '[data-water="oz"]').textContent = fmt(oz) + " oz";
      $(wp, '[data-water="cups"]').textContent = (oz / 8).toFixed(1) + " cups / " + (oz * 0.0295735).toFixed(1) + " L";
      goalCups = Math.max(4, Math.min(24, Math.round(oz / 8)));
      renderGlasses();
    });
  }

  /* ---------- Running pace ---------- */
  var paceForm = document.querySelector('[data-tool="pace"]');
  if (paceForm) {
    var rp = paceForm.closest(".tool-panel");
    function clock(sec) {
      sec = Math.round(sec);
      var h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60;
      return (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(s).padStart(2, "0");
    }
    paceForm.addEventListener("change", function (e) {
      if (e.target.name === "preset" && e.target.value !== "custom") {
        paceForm.elements.dist.value = e.target.value;
        paceForm.querySelector('input[name="dunit"][value="km"]').checked = true;
      }
    });
    paceForm.elements.dist.addEventListener("input", function () {
      paceForm.querySelector('input[name="preset"][value="custom"]').checked = true;
    });
    bind(paceForm, function () {
      var d = num(paceForm, "dist"), km = radio(paceForm, "dunit") === "mi" ? d * 1.609344 : d;
      var t = num(paceForm, "h") * 3600 + num(paceForm, "m") * 60 + num(paceForm, "s");
      if (km <= 0 || t <= 0) return;
      var perKm = t / km;
      $(rp, '[data-pace="km"]').textContent = clock(perKm) + " /km";
      $(rp, '[data-pace="mi"]').textContent = clock(perKm * 1.609344) + " /mi";
      $(rp, '[data-pace="speed"]').textContent = (km / t * 3600 * 0.621371).toFixed(1) + " mph";
      var races = [["1 mile", 1.609344], ["5K", 5], ["10K", 10], ["Half marathon", 21.0975], ["Marathon", 42.195]];
      $(rp, '[data-pace="races"]').innerHTML = races.map(function (r) {
        return "<tr><td>" + r[0] + "</td><td>" + clock(perKm * r[1]) + "</td></tr>";
      }).join("");
    });
  }

  /* ---------- Shoe finder quiz ---------- */
  var quiz = document.querySelector('[data-tool="quiz"]');
  if (quiz) {
    var steps = quiz.querySelectorAll(".quiz-step"), answers = {}, idx = 0;
    var barEl = $(quiz, "[data-quiz-bar]"), result = $(quiz, "[data-quiz-result]");
    function show(i) {
      steps.forEach(function (s, j) { s.classList.toggle("is-active", j === i); });
      barEl.style.width = (i / steps.length * 100) + "%";
    }
    function finish() {
      steps.forEach(function (s) { s.classList.remove("is-active"); });
      barEl.style.width = "100%";
      var a = answers, title, text, list, link = "/how-to-choose-running-shoes-for-flat-feet/", linkText = "Read the running shoe guide";
      var flat = a.arch === "flat" || (a.arch === "unsure" && a.pain === "knee");
      if (a.sport === "tennis") {
        title = flat ? "Stable court shoes with medial support" : "Supportive all-court tennis shoes";
        text = "Court sports need lateral support first. Look for a wide, flat outsole, a firm heel counter and a durable toe. " +
          (flat ? "With flat feet, pick a model with a structured midfoot or room for your insoles." : "A neutral, cushioned court shoe should suit you.");
        list = ["Wide base and low-to-the-ground feel for quick side steps", "Herringbone outsole matched to hard or clay courts", a.orthotic === "yes" ? "Removable insole so your orthotic fits" : "Firm midfoot that resists twisting"];
        link = "/best-tennis-shoes-for-flat-feet/"; linkText = "See tennis shoes for flat feet";
      } else if (a.orthotic === "yes") {
        title = "Neutral shoes + your orthotics";
        text = "Custom orthotics already control your foot motion, so a stable neutral shoe with a removable insole and enough depth usually works best. Stacking a stability shoe on top can over-correct.";
        list = ["Removable insole and extra depth", "Firm heel counter", "Bring your orthotics when you try shoes on"];
      } else if (flat && (a.pain === "knee" || a.pain === "arch")) {
        title = a.feel === "plush" ? "Max-support stability shoes" : "Motion-control or firm stability shoes";
        text = "Low arches plus discomfort suggest your feet roll inward a lot. A stability or motion-control shoe with a firm medial post or guide rails and a broad base should feel more supported.";
        list = ["Firmer foam on the inner (arch) side", "Wide midsole platform", "Consider arch-support insoles and the strengthening exercises below"];
      } else if (flat) {
        title = "Mild stability shoes";
        text = "Your arches are low but you're comfortable, so a light stability shoe gives a little guidance without feeling stiff.";
        list = ["Gentle medial support", a.feel === "light" ? "Lighter, more responsive foam" : "Balanced cushioning", "Wide toe box"];
      } else if (a.arch === "high") {
        title = "Cushioned neutral shoes";
        text = "High arches tend to absorb shock poorly, so prioritize soft, well-cushioned neutral shoes with a flexible forefoot.";
        list = ["Soft, high-stack cushioning", "Neutral platform (no medial post)", "Flexible upper"];
      } else {
        title = a.feel === "firm" ? "Stable neutral shoes" : "Versatile neutral trainers";
        text = "Your arches sound fairly typical. A neutral shoe that matches your activity and feels comfortable from the first step is the right call.";
        list = ["Fit: a thumb's width at the toe", "Heel locked in without slipping", "Comfort is the best predictor of a good shoe"];
      }
      if (a.sport === "walking" && a.sport !== "tennis") { linkText = "Read the flat-feet shoe guide"; }
      if (a.pain === "arch") list.push("Heel or arch pain? Try our plantar fasciitis stretches");
      $(result, "[data-quiz-title]").textContent = title;
      $(result, "[data-quiz-text]").textContent = text;
      $(result, "[data-quiz-list]").innerHTML = list.map(function (l) { return "<li>" + l + "</li>"; }).join("");
      var ln = $(result, "[data-quiz-link]"); ln.href = link; ln.textContent = linkText;
      result.hidden = false;
    }
    quiz.addEventListener("click", function (e) {
      var b = e.target.closest(".quiz-opts button");
      if (b) {
        var step = b.closest(".quiz-step");
        step.querySelectorAll("button").forEach(function (x) { x.classList.toggle("is-picked", x === b); });
        answers[step.getAttribute("data-q")] = b.getAttribute("data-v");
        setTimeout(function () { idx += 1; if (idx < steps.length) show(idx); else finish(); }, 220);
      }
      if (e.target.closest("[data-quiz-restart]")) {
        answers = {}; idx = 0; result.hidden = true;
        quiz.querySelectorAll(".is-picked").forEach(function (x) { x.classList.remove("is-picked"); });
        show(0);
      }
    });
    show(0);
  }

  /* ---------- Interval timer ---------- */
  var timer = document.querySelector('[data-tool="timer"]');
  if (timer) {
    var face = $(timer, ".timer-face"), ring = $(timer, "[data-timer-ring]");
    var startBtn = $(timer, "[data-timer-start]"), C = 2 * Math.PI * 88;
    var state = { running: false, phase: "ready", round: 0, left: 0, total: 0, last: 0, id: null };
    var actx = null;
    function cfg() {
      return { work: Math.max(1, parseInt(timer.querySelector('[name="work"]').value, 10) || 20),
        rest: Math.max(0, parseInt(timer.querySelector('[name="rest"]').value, 10) || 0),
        rounds: Math.max(1, parseInt(timer.querySelector('[name="rounds"]').value, 10) || 1) };
    }
    function mmss(s) { s = Math.max(0, Math.ceil(s)); return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }
    function beep(freq, dur) {
      if (!$(timer, "[data-timer-sound]").checked) return;
      try {
        actx = actx || new (window.AudioContext || window.webkitAudioContext)();
        var o = actx.createOscillator(), g = actx.createGain();
        o.frequency.value = freq; o.type = "sine"; o.connect(g); g.connect(actx.destination);
        g.gain.setValueAtTime(0.25, actx.currentTime); g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + dur);
        o.start(); o.stop(actx.currentTime + dur);
      } catch (e) { /* audio unavailable */ }
    }
    function paint() {
      var c = cfg();
      face.setAttribute("data-phase", state.phase);
      $(timer, "[data-timer-phase]").textContent = { ready: "Ready", work: "Work", rest: "Rest", done: "Done!" }[state.phase];
      $(timer, "[data-timer-time]").textContent = mmss(state.phase === "ready" ? c.work : state.left);
      $(timer, "[data-timer-round]").textContent = "Round " + state.round + " / " + c.rounds;
      var frac = state.total ? state.left / state.total : 1;
      ring.style.strokeDasharray = C;
      ring.style.strokeDashoffset = C * (1 - frac);
      $(timer, "[data-timer-total]").textContent = mmss(c.rounds * c.work + (c.rounds - 1) * c.rest).replace(/^0/, "");
    }
    function enter(phase) {
      var c = cfg();
      state.phase = phase;
      if (phase === "work") { state.round += 1; state.left = state.total = c.work; beep(880, 0.25); }
      else if (phase === "rest") { state.left = state.total = c.rest; beep(520, 0.3); }
      else if (phase === "done") { state.left = 0; state.total = 0; state.running = false; startBtn.textContent = "Start"; beep(990, 0.6); setTimeout(function () { beep(1320, 0.6); }, 250); }
      face.classList.remove("is-pulse"); void face.offsetWidth; face.classList.add("is-pulse");
    }
    function tick(ts) {
      if (!state.running) return;
      var dt = (ts - state.last) / 1000; state.last = ts;
      var before = Math.ceil(state.left);
      state.left -= dt;
      var after = Math.ceil(state.left);
      if (after !== before && after <= 3 && after > 0) beep(660, 0.12);
      if (state.left <= 0) {
        var c = cfg();
        if (state.phase === "work") {
          if (state.round >= c.rounds) enter("done");
          else if (c.rest > 0) enter("rest");
          else enter("work");
        } else enter("work");
      }
      paint();
      if (state.running) state.id = requestAnimationFrame(tick);
    }
    startBtn.addEventListener("click", function () {
      if (state.running) { state.running = false; cancelAnimationFrame(state.id); startBtn.textContent = "Resume"; return; }
      if (state.phase === "ready" || state.phase === "done") { state.round = 0; enter("work"); }
      state.running = true; state.last = performance.now(); startBtn.textContent = "Pause";
      state.id = requestAnimationFrame(tick);
    });
    function reset() {
      state.running = false; cancelAnimationFrame(state.id);
      state.phase = "ready"; state.round = 0; state.left = 0; state.total = 0; startBtn.textContent = "Start"; paint();
    }
    $(timer, "[data-timer-reset]").addEventListener("click", reset);
    timer.addEventListener("change", function (e) {
      if (e.target.name === "preset") {
        var v = e.target.value.split(",");
        timer.querySelector('[name="work"]').value = v[0];
        timer.querySelector('[name="rest"]').value = v[1];
        timer.querySelector('[name="rounds"]').value = v[2];
      }
      if (!state.running) reset();
    });
    timer.addEventListener("input", function (e) { if (e.target.type === "number" && !state.running) reset(); });
    paint();
  }
})();
