/* Relics Film Lab — shopper tools (runs only on /tools/* pages) */
(function () {
  "use strict";
  var d = document, $ = function (s) { return d.querySelector(s); }, $$ = function (s) { return Array.prototype.slice.call(d.querySelectorAll(s)); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var DATA = null;
  function load(cb) { if (DATA) return cb(DATA); fetch("/assets/tools-data.json").then(function (r) { return r.json(); }).then(function (j) { DATA = j; cb(j); }); }
  var AMZ = 'target="_blank" rel="sponsored nofollow noopener"';

  function camCard(c, why) {
    var buy = c.ax === 1 ? "Buy on Amazon" : c.ax === 2 ? "Closest match on Amazon" : "See listings on Amazon";
    return '<article class="tres">' + (c.i ? '<img src="' + c.i + '" alt="" loading="lazy">' : '<i class="tres__ph"></i>') +
      '<div><h3><a href="/products/' + c.s + '">' + esc(c.n) + "</a></h3><p>" + esc(c.sp) + "</p>" + (c.pr ? '<p class="tres__price">' + c.pr + ' <small>typical</small></p>' : "") + (why ? '<p class="tres__why">' + esc(why) + "</p>" : "") +
      '<div class="tres__btns"><a class="btn btn--sm" href="' + c.a + '" ' + AMZ + ">" + buy + '</a><a class="btn btn--ghost btn--sm" href="/products/' + c.s + '">Buying guide</a></div></div></article>';
  }
  function filmCard(f) {
    return '<article class="tres tres--film">' + (f.i ? '<img src="' + f.i + '" alt="" loading="lazy">' : '<i class="tres__film fcard--' + f.br + '"><b>' + f.iso + "</b></i>") + "<div><h3>" + esc(f.n) + "</h3><p>" + esc(f.fl) + " · ISO " + f.iso + (f.pr ? ' · <b class="tres__price">' + f.pr + "</b>" : "") + "</p><p class=\"tres__why\">" + esc(f.d) +
      '</p><div class="tres__btns"><a class="btn btn--sm" href="' + f.a + '" ' + AMZ + ">Buy on Amazon</a></div></div></article>";
  }

  // ---------------- camera finder
  var quiz = $("#quiz");
  if (quiz) {
    quiz.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(quiz), use = fd.get("use"), ctl = fd.get("ctl"), fmt = fd.get("fmt"), want = fd.getAll("want");
      load(function (D) {
        var scored = D.cams.map(function (c) {
          var s = 0, why = [], t = c.t;
          var catOk = { any: true, "35": c.c === "ps" || c.c === "slr", instant: c.c === "instant", mf: c.c === "mf" }[fmt];
          if (!catOk) return null;
          if (use === "movie") { if (c.c !== "movie") return null; s += 10; why.push("Shoots real Super 8 film"); }
          else if (c.c === "movie") return null;
          if (use === "everyday") { if (c.c === "ps") { s += 6; why.push("Easy everyday compact"); } if (c.c === "slr") s += 2; }
          if (use === "party") { if (c.c === "instant") { s += 8; why.push("Prints you can hand out on the spot"); } if (c.c === "ps") s += 5; }
          if (use === "learn") { if (c.c === "slr") { s += 8; why.push("Teaches exposure properly"); } if (t.indexOf("manual") > -1) s += 2; }
          if (use === "quality") { if (c.c === "mf") { s += 8; why.push("Big 120 negatives"); } if (c.c === "slr") s += 4; if (t.indexOf("fast") > -1) s += 2; }
          if (ctl === "auto") { if (t.indexOf("auto") > -1) { s += 5; why.push("Fully automatic"); } else s -= 4; }
          if (ctl === "semi") { if (t.indexOf("semi") > -1) { s += 5; why.push("Auto modes plus manual control"); } else if (t.indexOf("auto") > -1 || t.indexOf("manual") > -1) s += 1; }
          if (ctl === "manual") { if (t.indexOf("manual") > -1) { s += 5; why.push("Full manual control"); } else s -= 4; }
          want.forEach(function (w) { if (t.indexOf(w) > -1) { s += 4; why.push({ pocket: "Pocketable", zoom: "Zoom lens", fast: "Fast low-light lens", weather: "Weatherproof", nobatt: "Needs no battery" }[w]); } });
          s += Math.max(0, 6 - c.r / 20);          // popularity
          s += c.ax === 1 ? 3 : c.ax === 2 ? 1 : 0;  // available on Amazon
          if (c.i) s += 1;
          return { c: c, s: s, why: why.slice(0, 3).join(" · ") };
        }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 6);
        var out = $("#quiz-out");
        out.innerHTML = scored.length ? '<h2>Your matches</h2><div class="tresults">' + scored.map(function (x) { return camCard(x.c, x.why); }).join("") + "</div>"
          : '<p class="muted">No cameras match every answer — try "No preference" for the format.</p>';
        out.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  // ---------------- exposure calculator
  var SPEEDS = [30, 15, 8, 4, 2, 1, 1/2, 1/4, 1/8, 1/15, 1/30, 1/60, 1/125, 1/250, 1/500, 1/1000, 1/2000, 1/4000];
  var STOPS = [1.4, 2, 2.8, 4, 5.6, 8, 11, 16, 22];
  function fmtT(t) { if (t >= 1) return (Math.round(t * 10) / 10) + " s"; return "1/" + Math.round(1 / t) + " s"; }
  function nearestT(t) { return SPEEDS.reduce(function (a, b) { return Math.abs(Math.log2(b / t)) < Math.abs(Math.log2(a / t)) ? b : a; }); }
  if ($("#expo")) {
    var runE = function () {
      var iso = +$("#ex-iso").value, ev = +$("#ex-ev").value + Math.log2(iso / 100), N = +$("#ex-f").value;
      var t = N * N / Math.pow(2, ev);
      $("#ex-out").textContent = fmtT(nearestT(t)) + " at f/" + N;
      $("#ex-ev-out").textContent = "EV " + ev.toFixed(1) + " at ISO " + iso + (t > 1 / 30 ? " · use a tripod below 1/30 s" : "");
      $("#ex-pairs").innerHTML = STOPS.map(function (n) { var tt = nearestT(n * n / Math.pow(2, ev)); return '<span class="' + (n === N ? "is-on" : "") + '"><b>f/' + n + "</b>" + fmtT(tt) + "</span>"; }).join("");
    };
    ["#ex-iso", "#ex-ev", "#ex-f"].forEach(function (s) { $(s).addEventListener("change", runE); }); runE();
  }

  // ---------------- film stock finder
  var fsf = $("#fsf");
  if (fsf) {
    var runF = function () {
      var fd = new FormData(fsf), f = fd.get("f"), li = fd.get("li"), lk = fd.get("lk");
      load(function (D) {
        var res = D.films.filter(function (x) { return x.f === f; }).map(function (x) {
          var s = 0;
          if (x.li.indexOf(li) > -1) s += 4;
          if (lk === "bw") s += x.k === "bw" ? 6 : -6; else { if (x.k === "bw") s -= 3; if (x.lk.indexOf(lk) > -1) s += 4; }
          if (li === "low" && x.iso >= 400) s += 2; if (li === "bright" && x.iso <= 200) s += 1;
          return { x: x, s: s };
        }).sort(function (a, b) { return b.s - a.s; });
        $("#fsf-out").innerHTML = res.length ? '<h2>Best films for you</h2><div class="tresults">' + res.slice(0, 4).map(function (r) { return filmCard(r.x); }).join("") + "</div>" : "";
      });
    };
    fsf.addEventListener("change", runF); runF();
  }

  // ---------------- battery finder
  if ($("#bat")) {
    load(function (D) {
      $("#bat-all").innerHTML = D.bats.map(function (b) { return '<div class="batrow"><b>' + esc(b.n) + "</b><span>" + esc(b.d) + '</span><a class="btn btn--sm" href="' + b.a + '" ' + AMZ + ">Buy</a></div>"; }).join("");
      var q = $("#bat-q"), out = $("#bat-out");
      var GEN = { ps: "Most 1980s–90s point-and-shoots take AA, CR123A or CR2 batteries — check the label inside the battery door.", slr: "Most manual SLRs use LR44/SR44 button cells for the light meter (or a PX625/MR9 adapter for 1960s models).",
        instant: "Polaroid 600 and SX-70 cameras are powered by a battery inside the film pack — no separate battery needed.", mf: "Many medium format cameras are mechanical; any meter usually takes LR44 or a PX625 adapter.",
        movie: "Super 8 cameras usually run on AA batteries, often with a separate button cell for the light meter.", pocket: "110 cameras with a flash or meter usually take AAA or button cells." };
      q.addEventListener("input", function () {
        var v = q.value.toLowerCase().trim();
        if (v.length < 2) { out.innerHTML = ""; return; }
        var hits = D.cams.filter(function (c) { return c.n.toLowerCase().indexOf(v) > -1 || c.s.indexOf(v.replace(/\s+/g, "-")) > -1; }).slice(0, 8);
        out.innerHTML = hits.length ? hits.map(function (c) {
          var b = c.b === "none" ? "<b>No battery needed</b> — the exposure system is self-powered or mechanical." : c.b ? "Takes <b>" + esc(c.b) + "</b>." : esc(GEN[c.c] || "Check the battery compartment.");
          return '<div class="batrow batrow--cam"><b><a href="/products/' + c.s + '">' + esc(c.n) + "</a></b><span>" + b + "</span>" + (c.ba ? '<a class="btn btn--sm" href="' + c.ba + '" ' + AMZ + ">Buy battery</a>" : "") + "</div>";
        }).join("") : '<p class="muted">Not in our catalogue yet — see the common types below.</p>';
      });
    });
  }

  // ---------------- cost per shot
  if ($("#cps")) {
    var lastFmt = "";
    var runC = function () {
      var p = $("#cps-fmt").value.split("|"), shots = +p[0];
      if ($("#cps-fmt").value !== lastFmt) { $("#cps-film").value = p[1]; $("#cps-dev").value = p[2]; lastFmt = $("#cps-fmt").value; }
      var film = +$("#cps-film").value || 0, dev = +$("#cps-dev").value || 0, roll = film + dev, per = roll / shots;
      $("#cps-out").textContent = "$" + per.toFixed(2);
      $("#cps-roll").textContent = "$" + roll.toFixed(2) + " per roll · " + shots + " shots";
      load(function (D) {
        var label = $("#cps-fmt").selectedOptions[0].textContent, key = /120/.test(label) ? "120" : /Polaroid/.test(label) ? "instant-600" : /Instax/.test(label) ? "instant-wide" : /Disposable/.test(label) ? "disposable" : "35mm";
        var f = D.films.filter(function (x) { return x.f === key; }).slice(0, 3);
        $("#cps-shop").innerHTML = '<h3>Film for this format</h3><div class="tresults">' + f.map(filmCard).join("") + "</div>";
      });
    };
    ["#cps-fmt", "#cps-film", "#cps-dev"].forEach(function (s) { $(s).addEventListener("input", runC); }); runC();
  }

  // ---------------- depth of field
  if ($("#dof")) {
    var runD = function () {
      var c = +$("#dof-fmt").value, f = +$("#dof-fl").value, N = +$("#dof-n").value, u = $("#dof-u").value, k = u === "ft" ? 304.8 : 1000;
      var s = (+$("#dof-d").value || 1) * k, H = f * f / (N * c) + f;
      var near = s * (H - f) / (H + s - 2 * f), far = s < H ? s * (H - f) / (H - s) : Infinity;
      var fmt = function (mm) { return mm === Infinity ? "∞" : (mm / k).toFixed(mm / k < 10 ? 2 : 1) + (u === "ft" ? " ft" : " m"); };
      $("#dof-near").textContent = fmt(near); $("#dof-far").textContent = fmt(far); $("#dof-tot").textContent = far === Infinity ? "∞" : fmt(far - near); $("#dof-h").textContent = fmt(H);
      var max = Math.max(s * 3, far === Infinity ? s * 3 : far * 1.2), L = function (x) { return Math.min(100, x / max * 100); };
      $("#dof-bar").style.left = L(near) + "%"; $("#dof-bar").style.width = (far === Infinity ? 100 - L(near) : L(far) - L(near)) + "%"; $("#dof-subj").style.left = L(s) + "%";
    };
    ["#dof-fmt", "#dof-fl", "#dof-n", "#dof-d", "#dof-u"].forEach(function (s) { $(s).addEventListener("input", runD); }); runD();
  }

  // ---------------- super 8
  if ($("#s8")) {
    var mmss = function (sec) { var m = Math.floor(sec / 60), s = Math.round(sec % 60); return m + " min " + (s < 10 ? "0" : "") + s + " s"; };
    var runS = function () {
      var fps = +$("#s8-fps").value, n = +$("#s8-n").value || 1, per = 3600 / fps, mins = +$("#s8-min").value;
      $("#s8-per").textContent = mmss(per); $("#s8-run").textContent = mmss(per * n);
      $("#s8-need").textContent = mins > 0 ? Math.ceil(mins * 60 / per) + " cartridges" : "—";
      load(function (D) { $("#s8-shop").innerHTML = '<h3>Super 8 film</h3><div class="tresults">' + D.films.filter(function (x) { return x.f === "super8"; }).map(filmCard).join("") + "</div>"; });
    };
    ["#s8-fps", "#s8-n", "#s8-min"].forEach(function (s) { $(s).addEventListener("input", runS); }); runS();
  }
})();
