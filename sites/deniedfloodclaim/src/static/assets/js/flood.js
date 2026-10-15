(function () {
  "use strict";

  // Mobile menu
  var burger = document.querySelector("[data-burger]");
  var nav = document.getElementById("topnav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("open", !open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        burger.setAttribute("aria-expanded", "false");
        nav.classList.remove("open");
        burger.focus();
      }
    });
  }

  // Free case review forms -> /api/lead.php
  document.querySelectorAll("[data-intake]").forEach(function (form) {
    var out = form.querySelector("[data-intake-out]");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      out.className = "in-out";
      if (!form.checkValidity()) {
        var bad = form.querySelector(":invalid");
        out.textContent = "Please complete the highlighted fields and check the acknowledgment box.";
        out.classList.add("err");
        if (bad) bad.focus();
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      out.textContent = "Sending…";
      var data = new FormData(form);
      data.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: data })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (j) {
          if (j && j.ok) {
            form.reset();
            out.textContent = "Thank you, " + (j.name || "there") + ". Your request was received. Someone from The Lawgical Firm will contact you. If a deadline is close, please also call (407) 433-4131.";
            out.classList.add("ok");
          } else {
            out.textContent = (j && j.error) || "Something went wrong. Please call (407) 433-4131.";
            out.classList.add("err");
          }
        })
        .catch(function () {
          out.textContent = "Network error. Please call (407) 433-4131.";
          out.classList.add("err");
        })
        .then(function () { btn.disabled = false; });
    });
  });

  // NFIP deadline calculator
  var calc = document.querySelector("[data-calc]");
  if (calc) {
    var loss = calc.querySelector("[name=loss]");
    var denial = calc.querySelector("[name=denial]");
    var fmt = function (d) {
      return d.toLocaleDateString("en-US", { weekday: "short", year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
    };
    var parse = function (v) {
      if (!v) return null;
      var p = v.split("-");
      return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2]));
    };
    var addDays = function (d, n) { return new Date(d.getTime() + n * 86400000); };
    var addYear = function (d) {
      var y = new Date(d.getTime());
      y.setUTCFullYear(y.getUTCFullYear() + 1);
      return y;
    };
    var set = function (key, val) {
      var o = calc.querySelector("[data-out=" + key + "]");
      if (o) o.textContent = val;
    };
    var run = function () {
      var l = parse(loss.value), d = parse(denial.value);
      set("pol", l ? fmt(addDays(l, 60)) : "Enter the date of loss");
      set("appeal", d ? fmt(addDays(d, 60)) : "Enter the denial letter date");
      set("suit", d ? fmt(addYear(d)) : "Enter the denial letter date");
      try { localStorage.setItem("dfc-calc", JSON.stringify({ l: loss.value, d: denial.value })); } catch (e) {}
    };
    try {
      var saved = JSON.parse(localStorage.getItem("dfc-calc") || "null");
      if (saved) { loss.value = saved.l || ""; denial.value = saved.d || ""; }
    } catch (e) {}
    loss.addEventListener("input", run);
    denial.addEventListener("input", run);
    run();
  }

  // Highlight the current section in the guide table of contents
  var tocLinks = document.querySelectorAll(".toc a[href^='#']");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("on"); });
          var a = map[en.target.id];
          if (a) a.classList.add("on");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }
})();
