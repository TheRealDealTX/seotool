/* Roof Estimate Pro — site behaviour: header, menus, motion, hero quick
   estimate, tool-hub filter and the contact/claim forms. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header shadow on scroll
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle"), nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  // Tools dropdown
  document.querySelectorAll(".nav-drop").forEach(function (d) {
    var btn = d.querySelector("button"), timer;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = d.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    if (window.matchMedia("(hover: hover) and (min-width: 961px)").matches) {
      d.addEventListener("mouseenter", function () { clearTimeout(timer); d.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
      d.addEventListener("mouseleave", function () { timer = setTimeout(function () { d.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 160); });
    }
  });
  document.addEventListener("click", function (e) {
    document.querySelectorAll(".nav-drop.open").forEach(function (d) { if (!d.contains(e.target)) { d.classList.remove("open"); d.querySelector("button").setAttribute("aria-expanded", "false"); } });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    document.querySelectorAll(".nav-drop.open").forEach(function (d) { d.classList.remove("open"); d.querySelector("button").focus(); });
  });

  // Scroll reveal
  var rev = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rev.forEach(function (el) { io.observe(el); });
  } else rev.forEach(function (el) { el.classList.add("in"); });

  // Spotlight on tool cards
  document.addEventListener("pointermove", function (e) {
    var c = e.target.closest && e.target.closest(".tool-card");
    if (!c) return;
    var r = c.getBoundingClientRect();
    c.style.setProperty("--mx", (e.clientX - r.left) + "px");
    c.style.setProperty("--my", (e.clientY - r.top) + "px");
  });

  // Count-up stats
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, to = +el.getAttribute("data-count"), t0 = performance.now();
        co.unobserve(el);
        if (reduce) { el.textContent = to.toLocaleString(); return; }
        (function step(t) {
          var k = Math.min(1, (t - t0) / 1400), e2 = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(to * e2).toLocaleString();
          if (k < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { co.observe(c); });
  }

  // Hero quick estimate (same unit prices as the full replacement calculator)
  // Runs after every deferred script, so data.js (loaded after this file) is ready.
  document.addEventListener("DOMContentLoaded", initQuick);
  function initQuick() {
  var q = document.getElementById("quick-est");
  if (!q || !window.REP_DATA) return;
  {
    var D = window.REP_DATA;
    var out = q.querySelector(".big"), area = q.querySelector("#q-area"), areaOut = q.querySelector("#q-area-out");
    var tween = { v: 0, raf: 0 };
    function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
    function calc() {
      var sqft = +area.value, stories = +q.querySelector("#q-stories").value, rise = +q.querySelector("#q-pitch").value;
      var mat = D.materials.filter(function (m) { return m.key === q.querySelector("#q-mat").value; })[0] || D.materials[0];
      var reg = (D.regions.filter(function (r) { return r.key === q.querySelector("#q-region").value; })[0] || { factor: 1 }).factor;
      areaOut.textContent = sqft.toLocaleString() + " sq ft";
      var pf = Math.sqrt(1 + Math.pow(rise / 12, 2));
      var roofSf = (sqft / stories) * 1.18 * pf; // eaves, garage and porch allowance
      var waste = 1 + (D.waste[mat.waste] || D.waste.shingle).moderate / 100;
      var squares = roofSf / 100;
      var steep = rise >= 11 ? 1.3 : rise >= 9 ? 1.2 : rise >= 7 ? 1.1 : 1;
      var story = stories >= 3 ? 1.15 : stories === 2 ? 1.08 : 1;
      var labor = (mat.lab + 75) * steep * story * reg;
      var perSq = (mat.mat + mat.acc) * waste * 1.0825 + labor;
      var total = squares * perSq * 1.2;
      var low = total * 0.9, high = total * 1.15;
      q.querySelector(".sq").textContent = squares.toFixed(1) + " squares · " + Math.round(roofSf).toLocaleString() + " sq ft of roof";
      var from = tween.v, t0 = performance.now(); tween.v = total;
      cancelAnimationFrame(tween.raf);
      (function step(t) {
        var k = reduce ? 1 : Math.min(1, (t - t0) / 420), e = 1 - Math.pow(1 - k, 3), m = from + (total - from) * e;
        out.innerHTML = money(m * 0.9) + " <em>–</em> " + money(m * 1.15);
        if (k < 1) tween.raf = requestAnimationFrame(step); else out.innerHTML = money(low) + " <em>–</em> " + money(high);
      })(t0);
    }
    q.addEventListener("input", calc); calc();
  }
  }

  // Tool hub filter chips
  var chips = document.querySelectorAll(".chip[data-filter]");
  chips.forEach(function (ch) {
    ch.addEventListener("click", function () {
      var f = ch.getAttribute("data-filter");
      chips.forEach(function (c) { c.setAttribute("aria-pressed", c === ch ? "true" : "false"); });
      document.querySelectorAll("[data-group]").forEach(function (card) {
        card.hidden = !(f === "all" || card.getAttribute("data-group") === f);
      });
    });
  });

  // Estimate hand-off from a calculator into the contact form
  var hand = null;
  try { hand = JSON.parse(sessionStorage.getItem("rep_handoff") || "null"); } catch (e) {}
  var msg = document.querySelector('form[data-form] textarea[name="message"]');
  if (hand && msg && /[?&]tool=/.test(location.search)) {
    var box = document.getElementById("handoff");
    msg.value = "I used the " + hand.tool + " and would like a professional estimator to review it.\n\n" +
      (hand.lines || []).join("\n") + "\n\nEstimate link: " + hand.url + "\n\n";
    var src = document.querySelector('form[data-form] input[name="source_tool"]');
    if (src) src.value = hand.tool;
    if (box) { box.hidden = false; box.querySelector("b").textContent = hand.tool; }
  }

  // Forms → /api/contact.php
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    var started = Date.now();
    var ts = form.querySelector('input[name="ts"]'); if (ts) ts.value = String(started);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status"), btn = form.querySelector('button[type="submit"]');
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var files = form.querySelectorAll('input[type="file"]'), total = 0;
      files.forEach(function (f) { Array.prototype.forEach.call(f.files || [], function (x) { total += x.size; }); });
      if (total > 20 * 1024 * 1024) { status.className = "form-status err"; status.textContent = "Attachments are over 20 MB in total. Please send fewer or smaller files, or email them to us."; return; }
      btn.disabled = true; var label = btn.innerHTML; btn.innerHTML = "Sending…";
      fetch(form.getAttribute("action"), { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (j) {
          if (j && j.ok) {
            status.className = "form-status ok";
            status.textContent = j.message || "Thanks — your request is in. An estimator will be in touch shortly.";
            form.reset(); try { sessionStorage.removeItem("rep_handoff"); } catch (e2) {}
            if (j.redirect) location.href = j.redirect;
          } else throw new Error((j && j.error) || "send failed");
        })
        .catch(function (err) {
          status.className = "form-status err";
          status.textContent = (err && err.message && err.message !== "send failed" ? err.message + " " : "") + "We couldn't send that just now. Please call (210) 903-9471 or email contact@roofestimatepro.com.";
        })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  // Copyright year
  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
