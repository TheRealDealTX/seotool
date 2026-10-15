/* Florida Home Law - menu toggle, claim deadline helper, intake form. */
(function () {
  "use strict";

  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus();
      }
    });
  }

  /* Deadline helper: date of loss -> s. 627.70132 notice windows and s. 95.11 suit window. */
  function addMonths(d, m) {
    var r = new Date(d.getFullYear(), d.getMonth() + m, d.getDate());
    if (r.getDate() !== d.getDate()) r.setDate(0); // e.g. Feb 29 -> Feb 28
    return r;
  }
  function fmt(d) {
    return d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
  }
  Array.prototype.forEach.call(document.querySelectorAll("[data-deadlines]"), function (box) {
    var input = box.querySelector("input[type=date]");
    var out = box.querySelector("[data-deadlines-out]");
    function render() {
      if (!input.value) { out.innerHTML = ""; return; }
      var p = input.value.split("-");
      var loss = new Date(+p[0], +p[1] - 1, +p[2]);
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var rows = [
        ["Report a new or reopened claim by", addMonths(loss, 12), "s. 627.70132 - 1 year"],
        ["Report a supplemental claim by", addMonths(loss, 18), "s. 627.70132 - 18 months"],
        ["Contract lawsuit window closes", addMonths(loss, 60), "s. 95.11(2)(e) - 5 years"]
      ];
      out.innerHTML = rows.map(function (r) {
        var days = Math.round((r[1] - today) / 86400000);
        var left = days < 0 ? "date has passed" : days + " days from today";
        return "<div><span>" + r[0] + "</span><b>" + fmt(r[1]) + "</b><span>" + left + " &middot; " + r[2] + "</span></div>";
      }).join("");
    }
    input.addEventListener("change", render);
    input.addEventListener("input", render);
  });

  /* Intake form -> /api/lead.php */
  Array.prototype.forEach.call(document.querySelectorAll("[data-intake]"), function (form) {
    var out = form.querySelector("[data-intake-out]");
    var btn = form.querySelector("button[type=submit]");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      out.className = "intake-out";
      if (!form.checkValidity()) {
        var bad = form.querySelector(":invalid");
        out.className = "intake-out err";
        out.textContent = "Please complete the highlighted field" + (bad && bad.labels && bad.labels[0] ? ": " + bad.labels[0].textContent.slice(0, 60) : "") + ".";
        if (bad) bad.focus();
        return;
      }
      out.textContent = "Sending…";
      btn.disabled = true;
      var data = new URLSearchParams(new FormData(form));
      data.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: data })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.ok) {
            out.textContent = "Thank you, " + d.name + ". Your request was received and someone from The Lawgical Firm will reach out. For faster help, call (407) 433-4131.";
            form.reset();
          } else {
            out.className = "intake-out err";
            out.textContent = d.error || "Something went wrong. Please call (407) 433-4131.";
          }
        })
        .catch(function () {
          out.className = "intake-out err";
          out.textContent = "We could not send your request. Please call (407) 433-4131.";
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
