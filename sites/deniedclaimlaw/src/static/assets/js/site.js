(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var PHONE = '<a href="tel:+14074334131">(407) 433-4131</a>';
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  /* index (mobile nav) */
  var tog = document.querySelector("[data-navtoggle]"), nav = document.getElementById("volnav");
  if (tog && nav) {
    tog.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      tog.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* table of contents: collapse on small screens, highlight current section */
  var toc = document.querySelector("[data-toc]");
  if (toc) {
    if (window.matchMedia("(max-width: 999px)").matches) toc.removeAttribute("open");
    var links = $$("a", toc), map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && map[e.target.id]) {
            links.forEach(function (a) { a.classList.remove("on"); });
            map[e.target.id].classList.add("on");
          }
        });
      }, { rootMargin: "0px 0px -70% 0px" });
      Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) io.observe(h); });
    }
  }

  /* lead form */
  $$("[data-lead-form]").forEach(function (f) {
    var out = f.querySelector("[data-lead-out]"), btn = f.querySelector("button[type=submit]");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!f.checkValidity()) {
        out.className = "fout err";
        out.textContent = "Please complete the required fields (name, phone, city or ZIP) and check the consent box.";
        var bad = f.querySelector(":invalid"); if (bad) bad.focus();
        return;
      }
      out.className = "fout"; out.textContent = "Sending…"; btn.disabled = true;
      var body = new URLSearchParams(new FormData(f));
      body.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: body })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.ok) {
            out.innerHTML = "<strong>Thank you, " + esc(d.name) + ".</strong> Your request reached The Lawgical Firm. Someone from the firm will contact you. For faster help call " + PHONE + ".";
            f.reset();
          } else {
            out.className = "fout err"; out.innerHTML = esc(d.error || "Something went wrong.") + " You can also call " + PHONE + ".";
          }
        })
        .catch(function () { out.className = "fout err"; out.innerHTML = "We could not send your request. Please call " + PHONE + "."; })
        .then(function () { btn.disabled = false; });
    });
  });

  /* deadline calculator (Florida claim deadlines page) */
  var calc = document.querySelector("[data-calc]");
  if (calc) {
    var input = calc.querySelector("input"), list = calc.querySelector("[data-calc-out]");
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", year: "numeric", month: "long", day: "numeric", timeZone: "UTC" }); };
    var add = function (d, m) {
      var r = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + m, 1));
      var last = new Date(Date.UTC(r.getUTCFullYear(), r.getUTCMonth() + 1, 0)).getUTCDate();
      r.setUTCDate(Math.min(d.getUTCDate(), last));
      return r;
    };
    var run = function () {
      if (!input.value) { list.innerHTML = ""; return; }
      var p = input.value.split("-"), d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2]));
      var today = new Date(), rows = [
        ["Notice of a new or reopened claim (s. 627.70132)", add(d, 12)],
        ["Notice of a supplemental claim (s. 627.70132)", add(d, 18)],
        ["Lawsuit for breach of the policy (s. 95.11(2)(e))", add(d, 60)]
      ];
      list.innerHTML = rows.map(function (r) {
        var past = r[1] < today ? " &middot; <em>this date has passed</em>" : "";
        return "<li>" + r[0] + "<b>" + fmt(r[1]) + "</b><span>Estimate only" + past + "</span></li>";
      }).join("");
    };
    input.addEventListener("change", run);
    input.addEventListener("input", run);
  }
})();
