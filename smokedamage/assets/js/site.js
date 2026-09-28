/* SmokeDamage.com — site script: header, nav, popup, claim form, tracking.
   No dependencies. Loaded with `defer` on every page. */
(function () {
  "use strict";
  var d = document, w = window;
  d.documentElement.classList.remove("no-js");

  /* ---------------- Analytics helper ----------------
     Sends events to GA4 (if configured) and dataLayer. Never include claim
     documents, messages, names, emails or phone numbers in event params. */
  function track(name, params) {
    params = params || {};
    params.page_path = location.pathname;
    try {
      w.dataLayer = w.dataLayer || [];
      w.dataLayer.push(Object.assign({ event: name }, params));
      if (typeof w.gtag === "function") w.gtag("event", name, params);
    } catch (e) { /* ignore */ }
  }
  w.sdTrack = track;

  d.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("tel:") === 0) track("phone_click", { link_location: a.getAttribute("data-loc") || "content" });
    else if (href.indexOf("mailto:") === 0) track("email_click", { link_location: a.getAttribute("data-loc") || "content" });
    else if (a.hasAttribute("data-cta")) track("cta_click", { cta: a.getAttribute("data-cta") });
  });

  /* ---------------- Header ---------------- */
  var header = d.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("scrolled", w.scrollY > 8); }
  w.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Desktop dropdowns: click/Enter toggles (hover handled by CSS), Esc closes.
  d.querySelectorAll(".has-dropdown > button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.parentElement, open = !li.classList.contains("open");
      d.querySelectorAll(".has-dropdown.open").forEach(function (o) { o.classList.remove("open"); o.firstElementChild.setAttribute("aria-expanded", "false"); });
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  d.addEventListener("click", function (e) {
    if (!e.target.closest(".has-dropdown")) d.querySelectorAll(".has-dropdown.open").forEach(function (o) { o.classList.remove("open"); o.firstElementChild.setAttribute("aria-expanded", "false"); });
  });

  // Mobile nav
  var toggle = d.querySelector(".menu-toggle"), mnav = d.getElementById("mobile-nav");
  var lastFocus = null;
  function setNav(open) {
    if (!mnav) return;
    mnav.classList.toggle("open", open);
    mnav.setAttribute("aria-hidden", open ? "false" : "true");
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
    d.body.style.overflow = open ? "hidden" : "";
    if (open) { lastFocus = d.activeElement; var f = mnav.querySelector(".close"); if (f) f.focus(); }
    else if (lastFocus) lastFocus.focus();
  }
  if (toggle) toggle.addEventListener("click", function () { setNav(!mnav.classList.contains("open")); });
  if (mnav) mnav.addEventListener("click", function (e) { if (e.target.closest(".close") || e.target.classList.contains("scrim")) setNav(false); });

  /* ---------------- Focus trap for dialogs ---------------- */
  function trap(container, e) {
    if (e.key !== "Tab") return;
    var f = container.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  /* ---------------- Popup ----------------
     Once per visitor session, after ~5 seconds, never on contact/admin pages
     or after the visitor has submitted the form. */
  var modal = d.getElementById("claim-modal");
  var popupFocus = null;
  function store(kind, key, val) {
    try { var s = kind === "l" ? w.localStorage : w.sessionStorage; if (val === undefined) return s.getItem(key); s.setItem(key, val); } catch (e) { return null; }
  }
  function openModal() {
    if (!modal) return;
    popupFocus = d.activeElement;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    var c = modal.querySelector(".modal-close"); if (c) c.focus();
    store("s", "sd_popup_seen", "1");
    store("l", "sd_popup_seen_at", String(Date.now()));
    track("popup_view");
  }
  function closeModal() {
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    if (popupFocus && popupFocus.focus) popupFocus.focus();
  }
  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target.closest(".modal-close") || e.target.classList.contains("scrim")) { closeModal(); track("popup_close"); }
      var cta = e.target.closest("a");
      if (cta) track("popup_conversion", { action: (cta.getAttribute("href") || "").indexOf("tel:") === 0 ? "call" : "review" });
    });
    modal.addEventListener("keydown", function (e) { trap(modal.querySelector(".modal-card"), e); });
    var cfg = w.SD || {};
    var suppressed = /^\/(contact|admin|thank-you)/.test(location.pathname) || store("s", "sd_popup_seen") || store("l", "sd_lead_sent");
    var seenAt = parseInt(store("l", "sd_popup_seen_at") || "0", 10);
    if (seenAt && Date.now() - seenAt < 7 * 864e5) suppressed = true; // first-time visitors only (7 days)
    if (cfg.popupEnabled !== false && !suppressed) {
      setTimeout(function () {
        // Admin can switch the popup off at runtime without a rebuild.
        fetch("/api/settings.php", { credentials: "omit" }).then(function (r) { return r.ok ? r.json() : {}; })
          .catch(function () { return {}; })
          .then(function (s) { if (s && s.popup_enabled === false) return; if (!d.querySelector(".mobile-nav.open")) openModal(); });
      }, (cfg.popupDelay || 5) * 1000);
    }
  }
  d.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (modal && modal.classList.contains("open")) closeModal();
      if (mnav && mnav.classList.contains("open")) setNav(false);
      d.querySelectorAll(".has-dropdown.open").forEach(function (o) { o.classList.remove("open"); });
    }
    if (mnav && mnav.classList.contains("open")) trap(mnav.querySelector(".panel"), e);
  });

  /* ---------------- Reveal on scroll ---------------- */
  if ("IntersectionObserver" in w) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    d.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else d.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); });

  /* ---------------- TOC active state ---------------- */
  var tocLinks = d.querySelectorAll(".toc a");
  if (tocLinks.length && "IntersectionObserver" in w) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove("active"); }); var a = map[en.target.id]; if (a) a.classList.add("active"); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var h = d.getElementById(id); if (h) tio.observe(h); });
  }

  /* ---------------- Claim review form ---------------- */
  var form = d.getElementById("claim-form");
  if (form) {
    var started = false;
    form.addEventListener("input", function () { if (!started) { started = true; track("form_start", { form: "claim_review" }); } }, { once: false });
    // Prefill from query string (e.g. from calculators): ?status=Denied&source=scope-calculator
    try {
      var q = new URLSearchParams(location.search);
      var st = q.get("status"); if (st && form.claim_status) { [].forEach.call(form.claim_status.options, function (o) { if (o.value === st) form.claim_status.value = st; }); }
      var src = q.get("source"); if (src && form.source) form.source.value = src.replace(/[^a-z0-9-]/gi, "").slice(0, 40);
      var dmg = (q.get("damage") || "").split(","); form.querySelectorAll('input[name="damage[]"]').forEach(function (c) { if (dmg.indexOf(c.value) > -1) c.checked = true; });
      var summary = sessionStorageGet("sd_scope_summary"); if (summary && form.message && !form.message.value && src === "scope-calculator") form.message.value = summary;
    } catch (e) { /* ignore */ }
    if (form.started_at) form.started_at.value = String(Date.now());

    function sessionStorageGet(k) { try { return w.sessionStorage.getItem(k); } catch (e) { return null; } }
    function setErr(field, msg) {
      var wrap = field.closest(".field"); if (!wrap) return;
      var el = wrap.querySelector(".error");
      if (msg) {
        field.setAttribute("aria-invalid", "true");
        if (!el) { el = d.createElement("span"); el.className = "error"; el.id = field.id + "-err"; wrap.appendChild(el); }
        el.textContent = msg;
        var db = (field.getAttribute("aria-describedby") || "").split(" ").filter(Boolean);
        if (db.indexOf(el.id) === -1) db.push(el.id);
        field.setAttribute("aria-describedby", db.join(" "));
      } else {
        field.removeAttribute("aria-invalid");
        if (el) el.remove();
      }
    }
    function validate() {
      var bad = null;
      [["full_name", "Please enter your name."], ["phone", "Please enter a phone number we can reach you at."], ["email", "Please enter your email address."], ["city", "Please enter the Texas city where the property is located."]].forEach(function (r) {
        var f = form.elements[r[0]]; if (!f) return;
        var v = (f.value || "").trim(), msg = v ? "" : r[1];
        if (!msg && r[0] === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Please enter a valid email address.";
        if (!msg && r[0] === "phone" && v.replace(/\D/g, "").length < 10) msg = "Please enter a 10-digit phone number.";
        setErr(f, msg); if (msg && !bad) bad = f;
      });
      var zip = form.elements.zip;
      if (zip && zip.value && !/^\d{5}$/.test(zip.value.trim())) { setErr(zip, "ZIP code should be 5 digits."); bad = bad || zip; } else if (zip) setErr(zip, "");
      var files = form.querySelector('input[type="file"]');
      if (files && files.files) {
        var total = 0, tooMany = files.files.length > 8;
        [].forEach.call(files.files, function (f) { total += f.size; });
        var fmsg = tooMany ? "Please attach up to 8 files." : (total > 20 * 1024 * 1024 ? "Attachments must total 20 MB or less." : "");
        setErr(files, fmsg); if (fmsg) bad = bad || files;
      }
      return bad;
    }
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = validate();
      if (bad) { bad.focus(); return; }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true; var label = btn.textContent; btn.textContent = "Sending…";
      status.className = "form-status"; status.textContent = "";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }).then(function (j) { j.status = r.status; return j; }); })
        .then(function (j) {
          if (j.ok) {
            track("form_submit", { form: "claim_review", claim_status: form.claim_status ? form.claim_status.value : "", property_type: form.property_type ? form.property_type.value : "", source: form.source ? form.source.value : "" });
            store("l", "sd_lead_sent", "1");
            location.href = "/contact/thank-you/";
          } else {
            status.className = "form-status show err";
            status.textContent = j.error || "Something went wrong sending your request. Please call +1 (844) 537-1427 or email info@smokedamage.com.";
            btn.disabled = false; btn.textContent = label;
          }
        })
        .catch(function () {
          status.className = "form-status show err";
          status.textContent = "We couldn't reach the server. Please call +1 (844) 537-1427 or email info@smokedamage.com.";
          btn.disabled = false; btn.textContent = label;
        });
    });
  }
})();
