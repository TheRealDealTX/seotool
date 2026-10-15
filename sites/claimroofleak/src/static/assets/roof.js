/* claimroofleak.com - menu, "covered or not?" helper, intake form. No dependencies. */
(function () {
  "use strict";

  // Menu
  var burger = document.querySelector("[data-burger]");
  var menu = document.getElementById("menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") !== "true";
      burger.setAttribute("aria-expanded", String(open));
      menu.classList.toggle("open", open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("open")) {
        burger.setAttribute("aria-expanded", "false");
        menu.classList.remove("open");
        burger.focus();
      }
    });
  }

  // Covered-or-not helper
  var helper = document.querySelector("[data-helper]");
  if (helper) {
    var out = helper.querySelector("[data-verdict]");
    var R = {
      start: ["", "Pick an answer to each question", "Your result will appear here. It is a rough guide based on how most Florida homeowners policies are written, not a coverage decision."],
      good: ["good", "Looks like the kind of leak policies are written to cover",
        "A leak that starts suddenly because a storm, wind, hail or a falling tree opened the roof is the classic covered loss under most Florida homeowners policies. Interior water damage that follows is usually part of the same claim. Report it promptly, photograph everything, and make temporary repairs to stop more water from coming in. <a href=\"/roof-leak-insurance-claim-florida/\">How to file a roof leak claim in Florida</a>."],
      mixed: ["mixed", "Partly covered, partly disputed is common here",
        "When water has been getting in for a while, insurers often pay for the storm damage to the roof but deny interior damage as long-term seepage, or point to the 14-day / repeated-leakage exclusion many policies contain. How long the leak really lasted, and why, is a factual question that can be investigated. <a href=\"/roof-leak-water-damage-mold-claim/\">Water damage and mold from a roof leak</a>."],
      hard: ["hard", "Expect a wear-and-tear fight, but check the facts",
        "Policies generally exclude wear and tear, deterioration and poor maintenance, so a leak blamed only on an old roof is often denied. But many “old roof” denials involve a real wind or hail event the adjuster discounted, and damage caused by a covered event can be covered even on an older roof. <a href=\"/wear-and-tear-roof-denial/\">Wear and tear roof denials</a>."],
      unsure: ["mixed", "The cause decides the claim",
        "Coverage turns on what opened the roof and when. Write down the first date you saw water, check local weather for storms around then, and get a roofer or engineer to document the damage before repairs. <a href=\"/roof-damage-insurance-claim-florida/\">Roof damage insurance claims in Florida</a>."]
    };
    var extra = {
      denied: " <strong>Already denied?</strong> A denial letter can be reviewed and challenged. See <a href=\"/roof-leak-claim-denied/\">roof leak claim denied: what to do next</a>.",
      low: " <strong>Paid too little?</strong> Underpaid roof claims often come down to repair-vs-replace, code upgrades and the 25% rule. See <a href=\"/florida-25-percent-roof-rule/\">the Florida 25% roof rule</a>."
    };
    var tag = { good: "Usually covered", mixed: "Often disputed", hard: "Often denied", "": "General information" };

    var render = function () {
      var v = function (n) { var c = helper.querySelector('input[name="' + n + '"]:checked'); return c ? c.value : ""; };
      var cause = v("cause"), time = v("time"), status = v("status");
      var key = "start";
      if (cause) {
        if (cause === "storm") key = time === "long" ? "mixed" : "good";
        else if (cause === "slow") key = "mixed";
        else if (cause === "age") key = "hard";
        else key = "unsure";
      }
      var r = R[key];
      out.setAttribute("data-tone", r[0]);
      out.innerHTML = '<span class="tag">' + tag[r[0]] + "</span><h3>" + r[1] + "</h3><p>" + r[2] + (extra[status] || "") + "</p>";
    };
    helper.addEventListener("change", render);
    render();
  }

  // Intake forms
  var forms = document.querySelectorAll("[data-intake]");
  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = form.querySelector("[data-out]");
      msg.className = "intake-out";
      var bad = Array.prototype.filter.call(form.querySelectorAll("[required]"), function (el) {
        return el.type === "checkbox" ? !el.checked : !el.value.trim();
      });
      if (bad.length) {
        msg.classList.add("err");
        msg.textContent = "Please complete the highlighted fields and the consent box.";
        bad[0].focus();
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      msg.textContent = "Sending…";
      var data = new FormData(form);
      data.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: data })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (j) {
          if (j.ok) {
            form.reset();
            msg.classList.add("ok");
            msg.textContent = "Thank you, " + (j.first || "there") + ". The Lawgical Firm will reach out soon. If your home is taking on water now, call (407) 433-4131.";
          } else {
            msg.classList.add("err");
            msg.textContent = j.error || "Something went wrong. Please call (407) 433-4131.";
          }
        })
        .catch(function () {
          msg.classList.add("err");
          msg.textContent = "Connection problem. Please call (407) 433-4131.";
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
