/* Kingwood Roofers — site interactions: menu, reveal, process, TOC, forms, lead popup, estimator tabs. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function store(kind) { try { return window[kind]; } catch (e) { return null; } }
  function sget(k) { try { var s = store("sessionStorage"); return s ? s.getItem(k) : null; } catch (e) { return null; } }
  function sset(k, v) { try { var s = store("sessionStorage"); if (s) s.setItem(k, v); } catch (e) { } }

  /* ----- scroll lock shared by menu and popup ----- */
  var lockedY = 0, locks = 0;
  function lock() {
    if (locks++ > 0) return;
    lockedY = window.scrollY;
    document.body.style.top = -lockedY + "px";
    document.body.classList.add("menu-locked");
  }
  function unlock() {
    if (locks === 0 || --locks > 0) return;
    document.body.classList.remove("menu-locked");
    document.body.style.top = "";
    var sb = doc.style.scrollBehavior; doc.style.scrollBehavior = "auto";
    window.scrollTo(0, lockedY);
    doc.style.scrollBehavior = sb;
  }

  /* ----- mobile menu (works without JS via :target) ----- */
  var menu = document.getElementById("mobile-menu");
  var menuBtn = document.querySelector("[data-menu-open]");
  var menuTimer;
  function openMenu() {
    clearTimeout(menuTimer);
    menu.classList.add("open");
    menu.setAttribute("aria-hidden", "false");
    menuBtn.setAttribute("aria-expanded", "true");
    lock();
    requestAnimationFrame(function () { requestAnimationFrame(function () { menu.classList.add("visible"); }); });
    var c = menu.querySelector(".mm-close"); if (c) c.focus({ preventScroll: true });
  }
  function closeMenu(focusBtn) {
    if (!menu.classList.contains("open")) return;
    menu.classList.remove("visible");
    menu.setAttribute("aria-hidden", "true");
    menuBtn.setAttribute("aria-expanded", "false");
    unlock();
    menuTimer = setTimeout(function () { menu.classList.remove("open"); }, reduce ? 0 : 250);
    if (focusBtn) menuBtn.focus({ preventScroll: true });
  }
  if (menu && menuBtn) {
    menuBtn.addEventListener("click", function (ev) { ev.preventDefault(); openMenu(); });
    menu.querySelectorAll("[data-menu-close]").forEach(function (el) {
      el.addEventListener("click", function (ev) { ev.preventDefault(); closeMenu(true); });
    });
    menu.querySelectorAll(".mm-body a, .mm-foot a").forEach(function (el) {
      el.addEventListener("click", function () { closeMenu(false); });
    });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closeMenu(true); });
    window.addEventListener("resize", function () { if (window.innerWidth > 980) closeMenu(false); });
    window.addEventListener("pageshow", function () { closeMenu(false); });
  }

  /* ----- scroll effects ----- */
  var navbar = document.querySelector(".navbar");
  var steps = [].slice.call(document.querySelectorAll(".pstep"));
  var pending = [].slice.call(document.querySelectorAll("[data-reveal]"));
  var ticking = false;
  function onScroll() {
    if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 120);
    var mid = window.innerHeight * 0.75;
    steps.forEach(function (s) { s.classList.toggle("lit", s.getBoundingClientRect().top < mid); });
    if (pending.length) {
      pending = pending.filter(function (el) {
        if (el.classList.contains("in")) return false;
        if (el.getBoundingClientRect().top < window.innerHeight) { el.classList.add("in"); return false; }
        return true;
      });
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    pending.forEach(function (el) { io.observe(el); });
  } else {
    pending.forEach(function (el) { el.classList.add("in"); });
  }
  onScroll();
  window.addEventListener("load", onScroll);

  /* ----- article table of contents ----- */
  var toc = document.querySelector(".toc ul");
  var heads = [].slice.call(document.querySelectorAll(".prose h2"));
  if (toc && heads.length) {
    heads.forEach(function (h, i) {
      if (!h.id) h.id = "s" + (i + 1) + "-" + h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40);
      var li = document.createElement("li"), a = document.createElement("a");
      a.href = "#" + h.id; a.textContent = h.textContent; li.appendChild(a); toc.appendChild(li);
    });
    var links = toc.querySelectorAll("a");
    window.addEventListener("scroll", function () {
      var cur = 0;
      heads.forEach(function (h, i) { if (h.getBoundingClientRect().top < 140) cur = i; });
      links.forEach(function (a, i) { a.classList.toggle("active", i === cur); });
    }, { passive: true });
  } else if (toc) {
    toc.closest(".box").remove();
  }

  /* ----- estimator tabs (homepage) ----- */
  document.querySelectorAll(".est-tabs").forEach(function (list) {
    var tabs = [].slice.call(list.querySelectorAll("[role=tab]"));
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        tabs.forEach(function (o) {
          var on = o === t;
          o.setAttribute("aria-selected", on ? "true" : "false");
          var p = document.getElementById(o.getAttribute("aria-controls"));
          if (p) p.hidden = !on;
        });
      });
    });
  });

  /* ----- lead forms ----- */
  document.querySelectorAll("form.lead-form").forEach(function (form) {
    var t = form.querySelector("input[name=t]");
    if (t) t.value = String(Date.now());
    var page = form.querySelector("input[name=page]");
    if (page) page.value = location.pathname;
    form.addEventListener("submit", function (ev) {
      if (!window.fetch || !window.FormData) return;
      ev.preventDefault();
      var status = form.querySelector(".form-status");
      var btn = form.querySelector("button[type=submit]");
      var label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      status.className = "form-status"; status.textContent = "";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (res) {
          if (res.ok) {
            sset("kr-lead", "1");
            window.location.href = "/thank-you/";
          } else {
            status.textContent = res.message || "Something went wrong. Please call us instead.";
            status.className = "form-status err";
            btn.disabled = false; btn.innerHTML = label;
          }
        })
        .catch(function () {
          status.textContent = "We couldn't send that just now. Please call (512) 297-7580.";
          status.className = "form-status err";
          btn.disabled = false; btn.innerHTML = label;
        });
    });
  });

  /* ----- lead popup: opens 4 seconds after load, once per browser session ----- */
  var pop = document.getElementById("lead-popup");
  if (pop && !sget("kr-popup") && !sget("kr-lead")) {
    var lastFocus = null, popTimer;
    var openPop = function () {
      // Don't interrupt someone who is typing into another form or has the menu open.
      var a = document.activeElement;
      if ((a && /INPUT|SELECT|TEXTAREA/.test(a.tagName) && !pop.contains(a)) || (menu && menu.classList.contains("open"))) {
        popTimer = setTimeout(openPop, 4000);
        return;
      }
      sset("kr-popup", "1");
      lastFocus = a;
      pop.classList.add("open");
      pop.setAttribute("aria-hidden", "false");
      lock();
      requestAnimationFrame(function () { requestAnimationFrame(function () { pop.classList.add("visible"); }); });
      var first = pop.querySelector("input[name=name]");
      if (first && window.innerWidth > 640) first.focus({ preventScroll: true });
    };
    var closePop = function () {
      clearTimeout(popTimer);
      if (!pop.classList.contains("open")) return;
      pop.classList.remove("visible");
      pop.setAttribute("aria-hidden", "true");
      unlock();
      setTimeout(function () { pop.classList.remove("open"); }, reduce ? 0 : 300);
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    };
    pop.querySelectorAll("[data-popup-close]").forEach(function (el) { el.addEventListener("click", closePop); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closePop(); });
    popTimer = setTimeout(openPop, 4000);
  }

  /* ----- footer year ----- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
