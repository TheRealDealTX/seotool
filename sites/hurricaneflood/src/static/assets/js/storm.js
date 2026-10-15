/* HurricaneFlood.com - menu, wind-or-water checklist, deductible calculator, lead form. No dependencies. */
(function () {
  "use strict";

  /* mobile menu */
  var tog = document.querySelector("[data-navtoggle]");
  var nav = document.getElementById("topnav");
  if (tog && nav) {
    tog.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      tog.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        tog.setAttribute("aria-expanded", "false");
        tog.focus();
      }
    });
  }

  /* wind or water? checklist
     Each question carries data-wind / data-water weights applied to a "yes".
     The pin moves from WIND (left) to WATER (right). */
  var ww = document.querySelector("[data-ww]");
  if (ww) {
    var qs = ww.querySelectorAll("[data-q]");
    var pin = ww.querySelector("[data-pin]");
    var verdict = ww.querySelector("[data-verdict]");
    var steps = ww.querySelector("[data-steps]");
    var count = ww.querySelector("[data-count]");
    var reset = ww.querySelector("[data-reset]");

    var STEPS = {
      none: ["Answer the questions on the left. Each one is a clue adjusters and engineers look for."],
      wind: [
        "Your homeowners or condo policy (windstorm / hurricane coverage) is the main policy in play.",
        "Photograph roof, soffit, window and wall openings before temporary repairs, then tarp and keep receipts.",
        "Check your hurricane deductible on the declarations page; it usually applies instead of the all-other-perils deductible.",
        "Report the claim promptly: Florida generally bars a new claim not noticed within 1 year of the date of loss (s. 627.70132)."
      ],
      mixed: [
        "Expect a wind-versus-water fight. Open claims on BOTH your homeowners policy and your flood policy, if you have one.",
        "Measure and photograph the interior water line, then document everything above it separately.",
        "Get your own estimate split by cause: wind and wind-driven rain damage versus flood damage.",
        "Read the denial letter for flood, surface-water or anti-concurrent causation language and get advice before accepting it."
      ],
      water: [
        "Flood or storm surge damage is usually excluded by homeowners policies; a flood policy (NFIP or private) is where that part of the loss is paid.",
        "NFIP: file a signed proof of loss within 60 days after the loss unless FEMA extends it, and keep a copy.",
        "Still look up: roofs, ceilings and upper walls above the water line can be separate wind damage under your homeowners policy.",
        "No flood policy? Ask about FEMA Individual Assistance if a disaster is declared, and still report any wind damage."
      ]
    };

    function update() {
      var wind = 0, water = 0, answered = 0, denied = false;
      qs.forEach(function (q) {
        var on = q.querySelector("input:checked");
        if (!on) return;
        answered++;
        if (on.value === "yes") {
          wind += parseFloat(q.getAttribute("data-wind") || "0");
          water += parseFloat(q.getAttribute("data-water") || "0");
          if (q.hasAttribute("data-denied")) denied = true;
        }
      });
      count.textContent = answered + " of " + qs.length + " answered";
      var total = wind + water;
      var pos = total ? Math.round((water / total) * 100) : 50;
      pin.style.left = Math.min(97, Math.max(3, pos)) + "%";
      pin.setAttribute("aria-valuenow", String(pos));
      var key, label;
      if (!total) { key = "none"; label = answered ? "Not enough clues yet" : "Start the checklist"; }
      else if (pos <= 33) { key = "wind"; label = "Mostly wind signs"; }
      else if (pos >= 67) { key = "water"; label = "Mostly flood / surge signs"; }
      else { key = "mixed"; label = "Mixed wind and water loss"; }
      verdict.textContent = label;
      var list = STEPS[key].slice();
      if (denied) list.unshift("Your insurer has already blamed flood. A denial or partial denial can be challenged; have the letter, policy and photos reviewed before any deadline runs.");
      steps.innerHTML = "";
      list.forEach(function (t) { var li = document.createElement("li"); li.textContent = t; steps.appendChild(li); });
    }
    ww.addEventListener("change", update);
    if (reset) reset.addEventListener("click", function () {
      ww.querySelectorAll("input:checked").forEach(function (i) { i.checked = false; });
      update();
    });
    update();
  }

  /* hurricane deductible calculator */
  var calc = document.querySelector("[data-calc]");
  if (calc) {
    var fmt = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
    var run = function () {
      var lim = parseFloat(calc.querySelector("[name=limit]").value) || 0;
      var pct = parseFloat(calc.querySelector("[name=pct]").value) || 0;
      var used = parseFloat(calc.querySelector("[name=used]").value) || 0;
      var aop = parseFloat(calc.querySelector("[name=aop]").value) || 0;
      var dmg = parseFloat(calc.querySelector("[name=damage]").value) || 0;
      var ded = pct >= 1 ? lim * pct / 100 : 500;
      var remaining = Math.max(0, ded - used);
      var applied = used > 0 ? Math.max(remaining, aop) : ded;
      var pay = Math.max(0, dmg - applied);
      calc.querySelector("[data-out]").innerHTML =
        "Hurricane deductible: <b>" + fmt(ded) + "</b><br>Deductible applied to this hurricane: <b>" + fmt(applied) +
        "</b><br>Estimated covered wind damage after deductible: <b>" + fmt(pay) + "</b>";
    };
    calc.addEventListener("input", run);
    run();
  }

  /* lead forms */
  document.querySelectorAll("[data-lead]").forEach(function (form) {
    var out = form.querySelector("[data-lead-out]");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      out.className = "lead-out";
      var bad = Array.prototype.find.call(form.querySelectorAll("[required]"), function (el) {
        return el.type === "checkbox" ? !el.checked : !el.value.trim();
      });
      if (bad) {
        out.classList.add("err");
        out.textContent = bad.type === "checkbox" ? "Please check the acknowledgment box." : "Please complete: " + (form.querySelector('label[for="' + bad.id + '"]') || {}).textContent;
        bad.focus();
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      out.textContent = "Sending...";
      var data = new FormData(form);
      data.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: data })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (j) {
          if (j.ok) {
            out.classList.add("ok");
            out.textContent = "Thank you, " + (j.name || "there") + ". Your request was received; someone from The Lawgical Firm will contact you. If your situation is urgent, call (407) 433-4131.";
            form.reset();
          } else {
            out.classList.add("err");
            out.textContent = j.error || "Something went wrong. Please call (407) 433-4131.";
          }
        })
        .catch(function () {
          out.classList.add("err");
          out.textContent = "Network error. Please call (407) 433-4131.";
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
