/* Katy Roofer — site interactions: header, nav, scroll effects, forms. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ----- mobile menu (works without JS via :target; JS adds animation, scroll lock, Esc) ----- */
  var menu = document.getElementById("mobile-menu");
  var menuBtn = document.querySelector("[data-menu-open]");
  var closeTimer, lockedY = 0;
  // Pin the page while the menu is open (works on iOS too) and put it back exactly where it was.
  function lockScroll() {
    lockedY = window.scrollY;
    document.body.style.top = -lockedY + "px";
    document.body.classList.add("menu-locked");
  }
  function unlockScroll() {
    if (!document.body.classList.contains("menu-locked")) return;
    document.body.classList.remove("menu-locked");
    document.body.style.top = "";
    var html = doc.style.scrollBehavior; doc.style.scrollBehavior = "auto";
    window.scrollTo(0, lockedY);
    doc.style.scrollBehavior = html;
  }
  function openMenu() {
    clearTimeout(closeTimer);
    menu.classList.add("open");
    menu.setAttribute("aria-hidden", "false");
    menuBtn.setAttribute("aria-expanded", "true");
    lockScroll();
    requestAnimationFrame(function () { requestAnimationFrame(function () { menu.classList.add("visible"); }); });
    var c = menu.querySelector(".mm-close"); if (c) c.focus({ preventScroll: true });
  }
  function closeMenu(focusBtn) {
    if (!menu.classList.contains("open")) return;
    menu.classList.remove("visible");
    menu.setAttribute("aria-hidden", "true");
    menuBtn.setAttribute("aria-expanded", "false");
    unlockScroll();
    closeTimer = setTimeout(function () { menu.classList.remove("open"); }, reduce ? 0 : 300);
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeMenu(false); });
    window.addEventListener("pageshow", function () { closeMenu(false); });  // back button from bfcache
  }

  /* ----- scroll-linked effects (one rAF loop) ----- */
  var header = document.querySelector(".site-header");
  var bar = document.querySelector(".progress span");
  var parallax = [].slice.call(document.querySelectorAll("[data-parallax]"));
  var stepLists = [].slice.call(document.querySelectorAll(".steps"));
  var ticking = false;
  var pending = [].slice.call(document.querySelectorAll("[data-reveal]"));
  function reveal(el) {
    el.classList.add("in");
    el.querySelectorAll("[data-count]").forEach(countUp);
  }

  function onScroll() {
    var y = window.scrollY;
    var h = doc.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle("scrolled", y > 24);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(y / h, 1) : 0) + ")";
    if (!reduce) {
      parallax.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > window.innerHeight) return;
        el.style.transform = "translate3d(0," + (r.top * -0.18).toFixed(1) + "px,0)";
      });
    }
    stepLists.forEach(function (list) {
      var r = list.getBoundingClientRect();
      var mid = window.innerHeight * 0.6;
      var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      list.style.setProperty("--p", p.toFixed(3));
      list.querySelectorAll(".step").forEach(function (s) {
        s.classList.toggle("lit", s.getBoundingClientRect().top < mid);
      });
    });
    // Safety net: reveal anything already on screen, even if the observer missed it.
    if (pending.length) {
      pending = pending.filter(function (el) {
        if (el.classList.contains("in")) return false;
        if (el.getBoundingClientRect().top < window.innerHeight) { reveal(el); return false; }
        return true;
      });
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("resize", onScroll);

  /* ----- reveal + counters ----- */
  function countUp(el) {
    if (el.getAttribute("data-done")) return;
    el.setAttribute("data-done", "1");
    var end = parseFloat(el.getAttribute("data-count"));
    var dec = (el.getAttribute("data-count").split(".")[1] || "").length;
    if (reduce) { el.textContent = end.toFixed(dec); return; }
    var start = null, dur = 1600;
    function step(t) {
      if (!start) start = t;
      var p = Math.min((t - start) / dur, 1);
      el.textContent = (end * (1 - Math.pow(1 - p, 3))).toFixed(dec);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("in");
        e.target.querySelectorAll("[data-count]").forEach(countUp);
        if (e.target.hasAttribute("data-count")) countUp(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    document.querySelectorAll("[data-reveal], [data-count]").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("in"); });
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
      status.className = "form-status";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (res) {
          if (res.ok) {
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

  /* ----- footer year ----- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
