(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var PHONE = "(407) 433-4131";

  /* Mobile menu */
  var btn = $("[data-menu]"), drawer = $("#drawer");
  if (btn && drawer) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      drawer.hidden = open;
    });
  }

  /* Table of contents: open on desktop, highlight the section in view */
  var toc = $("[data-toc]");
  if (toc) {
    var det = $("details", toc);
    if (det && window.matchMedia("(min-width: 1000px)").matches) det.open = true;
    var links = $$("a[href^='#']", toc);
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    if ("IntersectionObserver" in window) {
      var current = null;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            if (current) current.classList.remove("is-active");
            current = map[e.target.id];
            if (current) current.classList.add("is-active");
          }
        });
      }, { rootMargin: "-80px 0px -70% 0px" });
      Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) io.observe(h); });
    }
    links.forEach(function (a) {
      a.addEventListener("click", function () {
        if (det && !window.matchMedia("(min-width: 1000px)").matches) det.open = false;
      });
    });
  }

  /* Glossary filter */
  var q = $("[data-gloss-q]");
  if (q) {
    var items = $$("[data-term]"), groups = $$("[data-gloss-group]"), empty = $("[data-gloss-empty]"), count = $("[data-gloss-count]");
    q.addEventListener("input", function () {
      var v = q.value.trim().toLowerCase(), shown = 0;
      items.forEach(function (it) {
        var hit = !v || it.textContent.toLowerCase().indexOf(v) !== -1;
        it.hidden = !hit; if (hit) shown++;
      });
      groups.forEach(function (g) { g.hidden = !$$("[data-term]:not([hidden])", g).length; });
      if (empty) empty.hidden = shown !== 0;
      if (count) count.textContent = shown + (shown === 1 ? " term" : " terms");
    });
  }

  /* Lead form */
  $$("[data-lead]").forEach(function (f) {
    var out = $("[data-out]", f), sub = $("button[type=submit]", f);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!f.reportValidity || f.reportValidity()) {
        out.className = "form-out"; out.textContent = "Sending…"; sub.disabled = true;
        var body = new URLSearchParams(new FormData(f));
        body.append("page", location.pathname);
        fetch("/api/lead.php", { method: "POST", body: body })
          .then(function (r) { return r.json(); })
          .then(function (d) {
            if (d.ok) {
              out.className = "form-out ok";
              out.textContent = "Thank you, " + d.name + ". Your request was received and someone from The Lawgical Firm will contact you. To talk now, call " + PHONE + ".";
              f.reset();
            } else {
              out.className = "form-out err"; out.textContent = d.error || ("Something went wrong. Please call " + PHONE + ".");
            }
          })
          .catch(function () { out.className = "form-out err"; out.textContent = "We could not send your request. Please call " + PHONE + "."; })
          .then(function () { sub.disabled = false; });
      }
    });
  });
})();
