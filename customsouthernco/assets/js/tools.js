/* Custom Southern Co. — interactive tools */
(function () {
  "use strict";
  var NOW = new Date().getFullYear();

  function money(n) { return "$" + (Math.round(n * 100) / 100).toFixed(2); }
  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem("csc-tool:" + k) || "null");
      localStorage.setItem("csc-tool:" + k, JSON.stringify(v));
    } catch (e) { return null; }
  }

  /* ---------------- Prince Albert tin dater ---------------- */
  function tinDater(root) {
    var boxes = root.querySelectorAll("input[type=checkbox]");
    var range = root.querySelector('[data-out="range"]');
    var notes = root.querySelector('[data-out="notes"]');
    var bar = root.querySelector(".tl-range");
    var MIN = 1907, MAX = NOW;
    function pos(y) { return ((y - MIN) / (MAX - MIN)) * 100; }
    function update() {
      var lo = MIN, hi = MAX, picked = [];
      boxes.forEach(function (b) {
        if (!b.checked) return;
        lo = Math.max(lo, +b.dataset.min);
        hi = Math.min(hi, +b.dataset.max);
        picked.push(b.dataset.note);
      });
      notes.innerHTML = "";
      picked.forEach(function (n) { var li = document.createElement("li"); li.textContent = n; notes.appendChild(li); });
      range.classList.remove("is-warn");
      if (!picked.length) {
        range.textContent = "Tick a clue to start";
        bar.classList.remove("on"); bar.style.left = "0%"; bar.style.width = "100%";
      } else if (lo > hi) {
        range.textContent = "These clues don't overlap. Check whether the lid and body match.";
        range.classList.add("is-warn"); bar.classList.remove("on");
      } else {
        var hiTxt = hi >= NOW ? "today" : hi;
        range.textContent = lo === hi ? "About " + lo : "Made between " + lo + " and " + hiTxt;
        bar.classList.add("on");
        bar.style.left = pos(lo) + "%";
        bar.style.width = Math.max(2, pos(hi) - pos(lo)) + "%";
      }
    }
    boxes.forEach(function (b) { b.addEventListener("change", update); });
    update();
  }

  /* ---------------- Ball jar age finder ---------------- */
  var GLASS = {
    aqua: "Aqua glass was standard on early Ball jars and was largely phased out by the late 1930s.",
    blue: "Ball Blue was made from roughly 1909 into the late 1930s, so it pairs well with early-1900s logos.",
    clear: "Clear glass became the norm from the late 1930s onward. On an older logo it can also be an early clear variant.",
    color: "Amber, green and purple jars are uncommon. Purple often means clear glass that turned color in the sun (manganese). Modern colored jars are commemorative releases with a ® logo."
  };
  function jarDater(root) {
    var opts = root.querySelectorAll(".logo-opt");
    var era = root.querySelector('[data-out="era"]');
    var note = root.querySelector('[data-out="note"]');
    var glass = root.querySelector('[data-out="glass"]');
    opts.forEach(function (o) {
      o.addEventListener("click", function () {
        opts.forEach(function (x) { x.setAttribute("aria-pressed", String(x === o)); });
        era.textContent = "Made " + o.dataset.era;
        note.textContent = o.dataset.note;
        era.animate && era.animate([{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }], { duration: 400, easing: "ease-out" });
      });
    });
    root.querySelectorAll('input[name="glass"]').forEach(function (r) {
      r.addEventListener("change", function () { glass.textContent = GLASS[r.value] || ""; });
    });
  }

  /* ---------------- laundry detergent calculator ---------------- */
  function detergent(root) {
    var f = root.querySelector("form");
    var out = function (k) { return root.querySelector('[data-out="' + k + '"]'); };
    var BATCH_TBSP = 56;              // ~3.5 cups of finished powder
    var SODA_CUPS = 6.5, BORAX_CUPS = 8; // cups per typical box
    var saved = store("detergent");
    if (saved) Object.keys(saved).forEach(function (k) { if (f.elements[k]) f.elements[k].value = saved[k]; });
    function fill(r) { r.style.setProperty("--p", ((r.value - r.min) / (r.max - r.min)) * 100 + "%"); }
    function calc() {
      var v = {};
      ["loads", "weeks", "scoop", "pSoap", "pSoda", "pBorax", "pStore"].forEach(function (k) { v[k] = parseFloat(f.elements[k].value) || 0; });
      root.querySelectorAll("output[data-for]").forEach(function (o) { o.textContent = f.elements[o.dataset.for].value; });
      f.querySelectorAll("input[type=range]").forEach(fill);
      var totalLoads = v.loads * v.weeks;
      var loadsPerBatch = BATCH_TBSP / (v.scoop || 1.5);
      var batches = Math.max(1, Math.ceil(totalLoads / loadsPerBatch));
      var batchCost = v.pSoap + v.pSoda / SODA_CUPS + v.pBorax / BORAX_CUPS;
      var perLoad = batchCost / loadsPerBatch;
      var diyTotal = perLoad * totalLoads, storeTotal = v.pStore * totalLoads;
      out("batches").textContent = batches;
      out("perLoad").textContent = money(perLoad);
      out("save").textContent = money(Math.max(0, storeTotal - diyTotal));
      var sodaBoxes = Math.ceil(batches / SODA_CUPS), boraxBoxes = Math.ceil(batches / BORAX_CUPS);
      out("mix").innerHTML =
        "<li><span>Bars of laundry soap, grated</span><strong>" + batches + "</strong></li>" +
        "<li><span>Washing soda</span><strong>" + batches + " cup" + (batches > 1 ? "s" : "") + " (" + sodaBoxes + " box" + (sodaBoxes > 1 ? "es" : "") + ")</strong></li>" +
        "<li><span>Borax</span><strong>" + batches + " cup" + (batches > 1 ? "s" : "") + " (" + boraxBoxes + " box" + (boraxBoxes > 1 ? "es" : "") + ")</strong></li>" +
        "<li><span>Loads covered</span><strong>" + totalLoads + " of " + Math.floor(batches * loadsPerBatch) + "</strong></li>" +
        "<li><span>Total cost, DIY vs. store</span><strong>" + money(diyTotal) + " vs. " + money(storeTotal) + "</strong></li>";
      var max = Math.max(diyTotal, storeTotal) || 1;
      root.querySelector('[data-bar="diy"]').style.width = (diyTotal / max) * 100 + "%";
      root.querySelector('[data-bar="store"]').style.width = (storeTotal / max) * 100 + "%";
      var s = {};
      ["loads", "weeks", "scoop", "pSoap", "pSoda", "pBorax", "pStore"].forEach(function (k) { s[k] = f.elements[k].value; });
      store("detergent", s);
    }
    f.addEventListener("input", calc);
    f.addEventListener("change", calc);
    calc();
  }

  /* ---------------- project finder ---------------- */
  var SEASON_NAME = { spring: "Spring", summer: "Summer", fall: "Fall", christmas: "Christmas", valentine: "Valentine's", year: "Year-round" };
  function finder(root) {
    var data = window.CSC_PROJECTS || [];
    var res = root.querySelector('[data-out="results"]');
    var count = root.querySelector('[data-out="count"]');
    function val(n) { var el = root.querySelector('[name="' + n + '"]:checked') || root.querySelector('[name="' + n + '"]'); return el ? el.value : "any"; }
    function item(p, pick) {
      var a = document.createElement("a");
      a.className = "f-item" + (pick ? " is-pick" : "");
      a.href = "/" + p.s + "/";
      a.innerHTML = '<img src="/assets/img/' + p.i + '-sm.webp" alt="" loading="lazy" width="110" height="90"><span><strong></strong><small></small></span>';
      a.querySelector("strong").textContent = p.t;
      a.querySelector("small").textContent = [SEASON_NAME[p.season], p.time, p.cost, p.skill].filter(Boolean).join("  ·  ");
      return a;
    }
    function list() {
      var season = val("season"), time = val("time"), budget = val("budget"), skill = val("skill");
      return data.filter(function (p) {
        return (season === "any" || p.season === season) &&
          (time === "any" || p.min <= +time) &&
          (budget === "any" || p.usd <= +budget) &&
          (skill === "any" || skill === "Moderate" || p.skill === skill);
      });
    }
    function render(pick) {
      var rows = list();
      res.innerHTML = "";
      if (pick) rows = [rows[Math.floor(Math.random() * rows.length)]].filter(Boolean);
      rows.forEach(function (p) { res.appendChild(item(p, pick)); });
      count.textContent = pick && rows.length ? "Here's your project:" :
        rows.length ? rows.length + " project" + (rows.length > 1 ? "s" : "") + " match" + (rows.length > 1 ? "" : "es") :
        "No exact match. Try a different season or a bigger budget.";
    }
    root.addEventListener("change", function () { render(false); });
    root.querySelector('[data-act="surprise"]').addEventListener("click", function () { render(true); });
    render(false);
  }

  var INIT = { "tin-dater": tinDater, "jar-dater": jarDater, "detergent": detergent, "project-finder": finder };
  document.querySelectorAll("[data-tool]").forEach(function (el) {
    var fn = INIT[el.getAttribute("data-tool")];
    if (fn) fn(el);
  });
})();
