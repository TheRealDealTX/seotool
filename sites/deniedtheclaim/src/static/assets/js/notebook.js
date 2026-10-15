/* Denied the Claim: menu, lead form, deadline worksheet. No dependencies. */
(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var PHONE = "(407) 433-4131", TEL = "+14074334131";

  /* Mobile menu */
  var btn = document.querySelector("[data-menu]"), nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? "Close" : "Menu";
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.textContent = "Menu"; btn.focus(); }
    });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.textContent = "Menu"; }); });
  }

  /* Lead forms */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  $$("[data-lead]").forEach(function (f) {
    var out = f.querySelector("[data-out]"), submit = f.querySelector("button[type=submit]");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      out.className = "form-out";
      var bad = $$("[required]", f).filter(function (el) { return el.type === "checkbox" ? !el.checked : !el.value.trim(); });
      if (bad.length) {
        out.className = "form-out err";
        out.textContent = bad[0].type === "checkbox" ? "Please check the acknowledgment box." : "Please fill in: " + (f.querySelector('label[for="' + bad[0].id + '"]') || {}).textContent;
        bad[0].focus();
        return;
      }
      out.textContent = "Sending…"; submit.disabled = true;
      var body = new URLSearchParams(new FormData(f));
      body.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: body })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.ok) {
            out.innerHTML = "Thank you, " + esc(d.name) + ". Your request reached The Lawgical Firm. Someone will contact you soon; to talk now, call <a href=\"tel:" + TEL + "\">" + PHONE + "</a>.";
            f.reset();
          } else { out.className = "form-out err"; out.textContent = d.error || "Something went wrong. Please call " + PHONE + "."; }
        })
        .catch(function () { out.className = "form-out err"; out.textContent = "We could not send the form. Please call " + PHONE + "."; })
        .then(function () { submit.disabled = false; });
    });
  });

  /* Deadline worksheet: general Florida periods counted from the date of loss */
  function addMonths(d, m) {
    var r = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + m, d.getUTCDate()));
    if (r.getUTCDate() !== d.getUTCDate()) r = new Date(Date.UTC(r.getUTCFullYear(), r.getUTCMonth(), 0));
    return r;
  }
  function fmt(d) { return d.toLocaleDateString("en-US", { timeZone: "UTC", month: "long", day: "numeric", year: "numeric" }); }
  $$("[data-deadlines]").forEach(function (box) {
    var input = box.querySelector("[data-dol]"), out = box.querySelector("[data-dl-out]");
    input.max = new Date().toISOString().slice(0, 10);
    input.addEventListener("change", function () {
      var v = input.value;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) { out.innerHTML = "<li>Enter a date to see the general Florida timelines.</li>"; return; }
      var p = v.split("-"), dol = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])), now = new Date();
      var rows = [
        ["Notice of a new or reopened claim", addMonths(dol, 12), "s. 627.70132(2)"],
        ["Notice of a supplemental claim", addMonths(dol, 18), "s. 627.70132(2)"],
        ["Lawsuit for breach of the policy (outside limit)", addMonths(dol, 60), "s. 95.11(2)(e)"]
      ];
      var html = rows.map(function (r) {
        var past = r[1] < now ? " &mdash; <strong>this date has passed</strong>" : "";
        return "<li>" + r[0] + ": <b>" + fmt(r[1]) + "</b> <span class=\"cite\">" + r[2] + "</span>" + past + "</li>";
      }).join("");
      if (dol < new Date(Date.UTC(2022, 11, 16))) {
        html += "<li>Your loss is before December 16, 2022. Older versions of s. 627.70132 gave longer notice windows for many earlier losses, so the notice dates above may be shorter than what applies to you.</li>";
      }
      html += "<li>Pre-suit notice must be filed with DFS at least 10 business days before any lawsuit (s. 627.70152), and the policy may set its own shorter conditions such as prompt notice.</li>";
      out.innerHTML = html;
    });
  });
})();
