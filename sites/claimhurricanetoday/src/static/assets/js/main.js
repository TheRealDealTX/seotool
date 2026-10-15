/* claimhurricanetoday.com - menu, deadline calculator, checklist, lead form. No dependencies. */
(function () {
  "use strict";

  /* ---------- mobile menu ---------- */
  var toggle = document.querySelector("[data-navtoggle]");
  var drawer = document.getElementById("drawer");
  if (toggle && drawer) {
    toggle.addEventListener("click", function () {
      var open = drawer.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---------- storage helpers (private mode / blocked storage safe) ---------- */
  function load(key) {
    try { return JSON.parse(window.localStorage.getItem(key) || "null"); } catch (e) { return null; }
  }
  function save(key, val) {
    try { window.localStorage.setItem(key, JSON.stringify(val)); } catch (e) { /* ignore */ }
  }

  /* ---------- date helpers (calendar dates, UTC to avoid DST drift) ---------- */
  var DAY = 86400000;
  function parseDate(v) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v || "");
    if (!m) return null;
    return Date.UTC(+m[1], +m[2] - 1, +m[3]);
  }
  function addMonths(t, n) {
    var d = new Date(t), y = d.getUTCFullYear(), mo = d.getUTCMonth() + n, day = d.getUTCDate();
    var last = new Date(Date.UTC(y, mo + 1, 0)).getUTCDate();   // clamp Feb 29 / 31st
    return Date.UTC(y, mo, Math.min(day, last));
  }
  function today() {
    var n = new Date();
    return Date.UTC(n.getFullYear(), n.getMonth(), n.getDate());
  }
  function fmt(t) {
    return new Date(t).toLocaleDateString("en-US", { timeZone: "UTC", weekday: "short", year: "numeric", month: "long", day: "numeric" });
  }
  function clockRow(what, t, now) {
    var left = Math.round((t - now) / DAY);
    var past = left < 0;
    var label = past ? Math.abs(left) + "<small>days ago</small>" : left + "<small>days left</small>";
    if (left === 0) label = "0<small>today</small>";
    return '<div class="clock' + (past ? " past" : "") + '"><span class="what">' + what + '</span><span class="when">' +
      fmt(t) + '</span><span class="left">' + label + "</span></div>";
  }

  /* ---------- deadline calculator (s. 627.70132 / s. 627.70131) ---------- */
  var REFORM = Date.UTC(2022, 11, 16);   // SB 2-A effective date
  Array.prototype.forEach.call(document.querySelectorAll("[data-calc]"), function (form) {
    var out = form.querySelector("[data-calc-out]");
    var dolIn = form.querySelector("[name=dol]");
    var repIn = form.querySelector("[name=reported]");
    var memo = load("cht-calc") || {};
    if (memo.dol && dolIn) dolIn.value = memo.dol;
    if (memo.reported && repIn) repIn.value = memo.reported;

    function run(e) {
      if (e) e.preventDefault();
      var dol = parseDate(dolIn.value), now = today(), html = "";
      if (dol === null) {
        out.hidden = false;
        out.innerHTML = '<div class="calc-warn">Enter the date of loss (for a hurricane, the date it made landfall).</div>';
        return;
      }
      if (dol > now) {
        out.hidden = false;
        out.innerHTML = '<div class="calc-warn">That date is in the future. Enter the hurricane\'s landfall date.</div>';
        return;
      }
      save("cht-calc", { dol: dolIn.value, reported: repIn ? repIn.value : "" });
      html += clockRow("New or reopened claim: notice to insurer (1 year)", addMonths(dol, 12), now);
      html += clockRow("Supplemental claim: notice to insurer (18 months)", addMonths(dol, 18), now);
      var rep = repIn ? parseDate(repIn.value) : null;
      if (rep !== null && rep >= dol) {
        html += clockRow("Insurer must acknowledge your claim (7 days)", rep + 7 * DAY, now);
        html += clockRow("Insurer must pay or deny, absent tolling (60 days)", rep + 60 * DAY, now);
      }
      if (dol < REFORM) {
        html += '<div class="calc-warn"><strong>Older loss:</strong> this date is before December 16, 2022. Different (generally longer) notice deadlines applied to many earlier losses, and which rule governs can depend on your policy dates. Have an attorney check it.</div>';
      } else if (addMonths(dol, 12) - now < 90 * DAY) {
        html += '<div class="calc-warn"><strong>Short window:</strong> under 90 days remain to give notice of a new or reopened claim. Report it now, in writing, and keep proof.</div>';
      }
      out.innerHTML = html;
      out.hidden = false;
    }
    form.addEventListener("submit", run);
    if (memo.dol && dolIn && dolIn.value) run();
  });

  /* ---------- progress checklist ---------- */
  var list = document.querySelector("[data-checklist]");
  if (list) {
    var KEY = "cht-checklist-v1";
    var state = load(KEY) || {};
    var boxes = list.querySelectorAll("input[type=checkbox][data-k]");
    var bar = document.querySelector("[data-progress-bar]");
    var num = document.querySelector("[data-progress-num]");
    function refresh() {
      var done = 0;
      Array.prototype.forEach.call(boxes, function (b) { if (b.checked) done++; });
      var pct = boxes.length ? Math.round(done / boxes.length * 100) : 0;
      if (bar) bar.style.width = pct + "%";
      if (num) num.textContent = done + " / " + boxes.length + " done";
      Array.prototype.forEach.call(list.querySelectorAll(".phase"), function (ph) {
        var all = ph.querySelectorAll("input[data-k]"), d = 0;
        Array.prototype.forEach.call(all, function (b) { if (b.checked) d++; });
        var c = ph.querySelector("[data-phase-count]");
        if (c) c.textContent = d + " of " + all.length;
      });
    }
    Array.prototype.forEach.call(boxes, function (b) {
      b.checked = !!state[b.getAttribute("data-k")];
      b.addEventListener("change", function () {
        state[b.getAttribute("data-k")] = b.checked;
        save(KEY, state);
        refresh();
      });
    });
    var reset = document.querySelector("[data-checklist-reset]");
    if (reset) reset.addEventListener("click", function () {
      state = {};
      save(KEY, state);
      Array.prototype.forEach.call(boxes, function (b) { b.checked = false; });
      refresh();
    });
    refresh();
  }

  /* ---------- lead form ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("form[data-lead]"), function (form) {
    var status = form.querySelector("[data-lead-status]");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      status.className = "lf-status full";
      status.textContent = "Sending...";
      var data = new FormData(form);
      data.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.ok, j: j }; }); })
        .then(function (res) {
          if (res.ok) {
            status.className = "lf-status full ok";
            status.textContent = "Thank you, " + (res.j.name || "") + ". We received your request and will reach out soon. If your deadline is close, call us now.";
            form.reset();
          } else {
            status.className = "lf-status full err";
            status.textContent = (res.j && res.j.error) || "Something went wrong. Please call us.";
          }
        })
        .catch(function () {
          status.className = "lf-status full err";
          status.textContent = "We could not send your request. Please call us instead.";
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
