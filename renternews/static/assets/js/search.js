/* Renter News — client-side search over /search-index.json */
(function () {
  "use strict";
  var input = document.querySelector("[data-search-input]"), out = document.querySelector("[data-search-results]"), status = document.querySelector("[data-search-status]");
  if (!input) return;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var q = new URLSearchParams(location.search).get("q") || new URLSearchParams(location.search).get("s") || "";
  input.value = q;
  var idx = null;
  fetch("/search-index.json").then(function (r) { return r.json(); }).then(function (d) { idx = d; run(); });
  var t; input.addEventListener("input", function () { clearTimeout(t); t = setTimeout(run, 150); });
  function hl(text, terms) {
    var s = esc(text);
    terms.forEach(function (w) { if (w.length > 1) s = s.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>"); });
    return s;
  }
  function run() {
    if (!idx) return;
    var query = input.value.trim().toLowerCase();
    history.replaceState(null, "", query ? "?q=" + encodeURIComponent(query) : location.pathname);
    if (!query) { status.textContent = "Type to search " + idx.length + " stories and tools."; out.innerHTML = ""; return; }
    var terms = query.split(/\s+/);
    var res = idx.map(function (it) {
      var t = it.t.toLowerCase(), d = it.d.toLowerCase(), o = (it.city + " " + it.k + " " + it.c).toLowerCase(), b = it.b.toLowerCase(), s = 0;
      for (var i = 0; i < terms.length; i++) {
        var w = terms[i], hit = 0;
        if (t.indexOf(w) > -1) hit += 10; if (o.indexOf(w) > -1) hit += 6; if (d.indexOf(w) > -1) hit += 4; if (b.indexOf(w) > -1) hit += 1;
        if (!hit) return null; s += hit;
      }
      if (t.indexOf(query) > -1) s += 15;
      return { it: it, s: s };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 30);
    status.textContent = res.length ? res.length + " result" + (res.length > 1 ? "s" : "") + " for “" + input.value.trim() + "”" : "No results for “" + input.value.trim() + "”. Try a city name or a broader word.";
    out.innerHTML = res.map(function (r) {
      var it = r.it;
      return '<article class="card"><a class="card-media" href="' + it.u + '" tabindex="-1">' + (it.i ? '<img src="' + it.i + '" alt="" loading="lazy">' : "") + '</a><div class="card-body"><span class="chip" style="--c:' + it.col + '">' + esc(it.c) + '</span><h3 class="card-title"><a href="' + it.u + '">' + hl(it.t, terms) + '</a></h3><p class="card-dek">' + hl(it.d, terms) + '</p><div class="meta">' + (it.dt ? "<span>" + it.dt + "</span>" : "") + (it.city ? "<span>" + esc(it.city) + "</span>" : "") + "</div></div></article>";
    }).join("");
  }
})();
