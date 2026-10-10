(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function store(key, val) {
    try { if (val === undefined) return localStorage.getItem(key); localStorage.setItem(key, val); } catch (e) { return null; }
  }

  /* theme */
  var themeBtn = $(".theme-toggle");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var dark = doc.dataset.theme ? doc.dataset.theme === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
    doc.dataset.theme = dark ? "light" : "dark";
    store("hb-theme", doc.dataset.theme);
  });

  /* header + progress */
  var header = $(".site-header");
  var bar = $(".progress span");
  var tocBar = $(".toc__bar"), tocLabel = $(".toc__label");
  var article = $(".post .prose");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-stuck", y > 10);
    var max = document.body.scrollHeight - innerHeight;
    if (bar) bar.style.setProperty("--p", max > 0 ? Math.min(1, y / max) : 0);
    if (article && tocBar) {
      var r = article.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, (innerHeight * .4 - r.top) / r.height));
      tocBar.style.setProperty("--p", p);
      tocLabel.textContent = Math.round(p * 100) + "% read";
    }
  }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* nav */
  var navToggle = $(".nav-toggle");
  if (navToggle) navToggle.addEventListener("click", function () {
    var open = document.body.classList.toggle("nav-open");
    navToggle.setAttribute("aria-expanded", open);
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  $$(".nav__dropbtn").forEach(function (b) {
    b.addEventListener("click", function () {
      var li = b.parentNode, open = li.classList.toggle("is-open");
      b.setAttribute("aria-expanded", open);
    });
  });
  document.addEventListener("click", function (e) {
    $$(".nav__drop.is-open").forEach(function (li) {
      if (!li.contains(e.target)) { li.classList.remove("is-open"); $(".nav__dropbtn", li).setAttribute("aria-expanded", "false"); }
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.body.classList.remove("nav-open");
      if (navToggle) navToggle.setAttribute("aria-expanded", "false");
      $$(".nav__drop.is-open").forEach(function (li) { li.classList.remove("is-open"); });
    }
  });

  /* reveal on scroll */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: .08 });
    $$(".reveal").forEach(function (el, i) {
      if (!el.style.transitionDelay && el.closest(".grid")) el.style.transitionDelay = (i % 3) * 90 + "ms";
      io.observe(el);
    });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  /* tilt + glare */
  if (finePointer && !reduce) {
    $$("[data-tilt]").forEach(function (el) {
      var max = el.classList.contains("feature") ? 4 : 7;
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.setProperty("--ry", ((x - .5) * max * 2).toFixed(2) + "deg");
        el.style.setProperty("--rx", ((.5 - y) * max * 2).toFixed(2) + "deg");
        el.style.setProperty("--ty", "-6px");
        el.style.setProperty("--glare-x", (x * 100) + "%");
        el.style.setProperty("--glare-y", (y * 100) + "%");
        if (!el.classList.contains("reveal")) el.style.transform = "perspective(900px) rotateX(" + ((.5 - y) * max) + "deg) rotateY(" + ((x - .5) * max) + "deg)";
        el.classList.add("is-tilting");
      });
      el.addEventListener("pointerleave", function () {
        ["--ry", "--rx", "--ty"].forEach(function (p) { el.style.removeProperty(p); });
        if (!el.classList.contains("reveal")) el.style.transform = "";
        el.classList.remove("is-tilting");
      });
    });
  }

  /* hero parallax floaters */
  var floaters = $$(".floater");
  if (floaters.length && finePointer && !reduce) {
    addEventListener("pointermove", function (e) {
      var dx = e.clientX / innerWidth - .5, dy = e.clientY / innerHeight - .5;
      floaters.forEach(function (f) {
        var d = parseFloat(f.dataset.depth) || 1;
        f.style.setProperty("--mx", (-dx * 40 * d).toFixed(1) + "px");
        f.style.setProperty("--my", (-dy * 40 * d).toFixed(1) + "px");
      });
    }, { passive: true });
  }

  /* rotating word */
  var rot = $(".rotator");
  if (rot && !reduce) {
    var words = rot.dataset.words.split("|"), wi = 0;
    setInterval(function () {
      wi = (wi + 1) % words.length;
      var span = document.createElement("span");
      span.className = "rotator__word";
      span.textContent = words[wi];
      rot.replaceChildren(span);
    }, 2400);
  }

  /* counters */
  if (!reduce && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = +el.dataset.count, t0 = performance.now();
        cio.unobserve(el);
        (function tick(t) {
          var k = Math.min(1, (t - t0) / 1200);
          el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3)));
          if (k < 1) requestAnimationFrame(tick);
        })(t0);
      });
    });
    $$("[data-count]").forEach(function (el) { el.textContent = "0"; cio.observe(el); });
  }

  /* confetti */
  var colors = ["#ff5a4e", "#ffc23d", "#14b8a6", "#7c3aed", "#22a447", "#ff4d8d"];
  function burst(x, y) {
    if (reduce) return;
    for (var i = 0; i < 26; i++) {
      var c = document.createElement("span");
      c.className = "confetti";
      var a = Math.random() * Math.PI * 2, d = 60 + Math.random() * 120;
      c.style.left = x + "px"; c.style.top = y + "px";
      c.style.background = colors[i % colors.length];
      c.style.setProperty("--x", Math.cos(a) * d + "px");
      c.style.setProperty("--y", Math.sin(a) * d + 80 + "px");
      c.style.setProperty("--rot", (Math.random() * 720 - 360) + "deg");
      document.body.appendChild(c);
      setTimeout(c.remove.bind(c), 1100);
    }
  }
  $$("[data-confetti]").forEach(function (b) {
    b.addEventListener("pointerdown", function (e) { burst(e.clientX, e.clientY); });
  });

  /* season tabs */
  var tabs = $$(".season__btn");
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (o) { o.setAttribute("aria-selected", o === t); });
      $$(".season__panel").forEach(function (p) { p.hidden = p.dataset.panel !== t.dataset.season; });
    });
  });
  // open the tab for the upcoming holiday season
  if (tabs.length) {
    var m = new Date().getMonth(), pick = m <= 1 ? 0 : m === 2 ? 1 : m <= 9 ? 2 : m === 10 ? 3 : 4;
    if (m >= 3 && m <= 7) pick = 2;
    tabs[pick].click();
  }

  /* craft picker live count (home) */
  var picker = $(".picker__form");
  if (picker) {
    var all = window.HB_INDEX || [];
    var n = $(".picker__n", picker);
    var update = function () {
      var f = new FormData(picker), t = f.get("time"), l = f.get("level");
      var c = all.filter(function (p) { return (!t || p.t === t) && (!l || p.l === l); }).length;
      n.textContent = all.length ? c + (c === 1 ? " match" : " matches") : "";
    };
    picker.addEventListener("change", update);
    update();
  }

  /* projects filter */
  var grid = $(".grid--filter");
  if (grid) {
    var cards = $$(".card", grid), q = $(".filters input[name=q]");
    var selT = $(".filters select[name=time]"), selL = $(".filters select[name=level]");
    var chips = $$(".chip"), count = $(".filters__count b"), empty = $(".empty");
    var state = { cat: "", q: "", time: "", level: "" };
    var params = new URLSearchParams(location.search);
    ["cat", "q", "time", "level"].forEach(function (k) { if (params.get(k)) state[k] = params.get(k); });
    function apply(push) {
      var words = state.q.toLowerCase().split(/\s+/).filter(Boolean), shown = 0;
      cards.forEach(function (c) {
        var ok = (!state.cat || c.dataset.cat === state.cat) && (!state.time || c.dataset.time === state.time) &&
          (!state.level || c.dataset.level === state.level) &&
          words.every(function (w) { return c.dataset.search.indexOf(w) > -1; });
        c.hidden = !ok;
        if (ok) { shown++; c.classList.add("is-in"); }
      });
      count.textContent = shown;
      empty.hidden = shown > 0;
      chips.forEach(function (ch) { ch.setAttribute("aria-pressed", ch.dataset.cat === state.cat); });
      q.value = state.q; selT.value = state.time; selL.value = state.level;
      if (push) {
        var p = new URLSearchParams();
        Object.keys(state).forEach(function (k) { if (state[k]) p.set(k, state[k]); });
        history.replaceState(null, "", location.pathname + (p.toString() ? "?" + p : "") + location.hash);
      }
    }
    chips.forEach(function (ch) { ch.addEventListener("click", function () { state.cat = ch.dataset.cat; apply(true); }); });
    q.addEventListener("input", function () { state.q = q.value; apply(true); });
    selT.addEventListener("change", function () { state.time = selT.value; apply(true); });
    selL.addEventListener("change", function () { state.level = selL.value; apply(true); });
    $("[data-reset]").addEventListener("click", function () { state = { cat: "", q: "", time: "", level: "" }; apply(true); });
    apply(false);
    if (location.hash === "#search") setTimeout(function () { q.focus(); }, 300);
  }

  /* materials checklist (remembered per project) */
  var post = $(".post");
  if (post) {
    var key = "hb-check-" + post.dataset.slug, boxes = $$(".check input", post), done = $(".box__done");
    var saved = (store(key) || "").split(",");
    boxes.forEach(function (b, i) { b.checked = saved.indexOf(String(i)) > -1; });
    var sync = function (celebrate) {
      var on = [];
      boxes.forEach(function (b, i) { if (b.checked) on.push(i); });
      store(key, on.join(","));
      done.textContent = on.length === boxes.length ? "All set, let’s make it! ✨" : on.length ? on.length + " of " + boxes.length + " gathered" : "";
      if (celebrate && on.length === boxes.length) { var r = done.getBoundingClientRect(); burst(r.left + r.width / 2, r.top); }
    };
    boxes.forEach(function (b) { b.addEventListener("change", function () { sync(true); }); });
    sync(false);

    /* toc highlight */
    var links = $$(".toc a");
    if (links.length && "IntersectionObserver" in window) {
      var tio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id); });
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      links.forEach(function (a) { var s = $(a.getAttribute("href")); if (s) tio.observe(s); });
    }
  }

  /* copy link */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      var done = function () {
        var t = document.createElement("div"); t.className = "toast"; t.textContent = "Link copied!";
        document.body.appendChild(t); setTimeout(t.remove.bind(t), 1800);
        burst(e.clientX, e.clientY);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(done, function () {});
    });
  });
})();
