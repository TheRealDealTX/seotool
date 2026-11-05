/* /get-matched/ lender-match tool. No data leaves the browser except
   anonymous Google Analytics events. To add a paid partner / affiliate offer,
   fill in PARTNER below: it is shown above the SBA Lender Match button. */
(function(){
  var PARTNER = { name: "", url: "", blurb: "" };   // e.g. {name:"Acme Funding", url:"https://...?ref=sbarates", blurb:"Prequalify in 5 minutes"}
  var SBA_LENDER_MATCH = "https://www.sba.gov/funding-programs/loans/lender-match";

  var f = document.getElementById("gm"), out = document.getElementById("gm-out");
  if (!f || !out) return;
  var R = window.SBA_RATES, L = window.SBA_LENDERS || [], NAT = window.SBA_NATIONAL || [], ST = window.SBA_STATES || {};
  var $ = function(id){ return document.getElementById(id); };
  function esc(s){ return String(s).replace(/[&<>"']/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }
  function money(n){ return "$" + Math.round(n).toLocaleString("en-US"); }
  function track(name, params){ try { if (window.gtag) gtag("event", name, params || {}); } catch (e) {} }

  // prefill from the CTA link (?state=TX&industry=...&amount=...)
  var q = new URLSearchParams(location.search);
  if (q.get("state") && ST[q.get("state")]) $("gm-state").value = q.get("state");
  if (q.get("industry")) {
    var want = "/SBA-Loan/" + encodeURIComponent(q.get("industry")).replace(/%2C/g, "%2C") + "/";
    [].forEach.call($("gm-ind").options, function(o){ if (decodeURIComponent(o.value) === decodeURIComponent(want)) $("gm-ind").value = o.value; });
  }
  if (q.get("amount")) {
    var a = +q.get("amount"), sel = $("gm-amt"), best = sel.options[0].value;
    [].forEach.call(sel.options, function(o){ if (Math.abs(+o.value - a) < Math.abs(+best - a)) best = o.value; });
    sel.value = best;
  }
  var source = q.get("from") || "direct";

  function cap(amount){
    var c = R.variable_caps;
    for (var i = 0; i < c.length; i++) if (amount <= c[i].max) return R.prime + c[i].spread;
    return R.prime + c[c.length - 1].spread;
  }
  function program(amount, use){
    if (amount > 5000000) return ["504 (plus a bank loan)", "Above the $5 million 7(a) limit. A 504 project can be much larger because the bank and CDC split it; otherwise you need a conventional loan."];
    if (use === "re") return ["504 or 7(a)", "Owner-occupied property usually fits the fixed-rate 504 (about 10% down). A 7(a) real estate loan runs up to 25 years and can bundle working capital."];
    if (use === "equip" && amount >= 250000) return ["504 or 7(a)", "Long-life equipment can go into a 504 at a fixed rate; smaller or mixed purchases are simpler as a 7(a)."];
    if (amount <= 50000) return ["Microloan or small 7(a)", "Under $50,000 a nonprofit SBA microlender or an SBA Express loan is usually fastest. Small 7(a) loans need no collateral."];
    if (use === "buy") return ["7(a)", "Business and franchise purchases are the classic 7(a) loan: up to 10 years (25 with real estate) and at least 10% equity."];
    if (use === "start") return ["7(a) or Microloan", "Start-ups qualify, but expect to show industry experience, a plan with projections and at least 10% equity."];
    if (amount <= 500000) return ["SBA Express or 7(a)", "Under $500,000, an SBA Express loan can close in weeks because the lender approves it in-house."];
    return ["7(a)", "The standard SBA loan up to $5 million, for working capital, equipment, refinancing and acquisitions."];
  }

  f.addEventListener("submit", function(ev){
    ev.preventDefault();
    var st = $("gm-state").value;
    if (!st) { $("gm-state").focus(); return; }
    var amt = +$("gm-amt").value, use = $("gm-use").value, ind = $("gm-ind").value;
    var indName = ind ? $("gm-ind").options[$("gm-ind").selectedIndex].text : "";
    var p = program(amt, use), rate = cap(Math.min(amt, 5000000));
    var local = L.filter(function(x){ return x[2] === st; });
    var h = '<h2>Your SBA match' + (ST[st] ? ' in ' + esc(ST[st]) : '') + '</h2>';
    h += '<div class="facts"><div><span>Program that fits</span><strong>' + esc(p[0]) + '</strong></div>' +
         '<div><span>Highest variable rate allowed</span><strong class="num">' + rate.toFixed(2) + '%</strong></div>' +
         '<div><span>Prime rate today</span><strong class="num">' + R.prime.toFixed(2) + '%</strong></div></div>';
    h += '<p>' + esc(p[1]) + ' Lenders can and often do price below the cap, so compare at least two quotes.</p>';
    if (PARTNER.url) {
      h += '<div class="partner"><strong>' + esc(PARTNER.name) + '</strong><p>' + esc(PARTNER.blurb) + '</p>' +
           '<a class="btn-match" rel="sponsored noopener" target="_blank" href="' + esc(PARTNER.url) + '" data-out="partner">Check my options</a>' +
           '<p class="src">Sponsored. We may be paid if you apply.</p></div>';
    }
    h += '<h3>SBA lenders in our directory for ' + esc(ST[st] || st) + '</h3>';
    if (local.length) {
      h += '<ul class="link-grid">' + local.map(function(x){ return '<li><a href="' + x[1] + '">' + esc(x[0]) + '</a> <small>' + esc(x[3]) + '</small></li>'; }).join("") + '</ul>';
    } else {
      h += '<p>We don\'t have a profile for a lender in this state yet. The national SBA lenders below lend in every state, and SBA Lender Match covers local banks and credit unions.</p>';
    }
    h += '<h3>High-volume SBA lenders that lend nationwide</h3><ul class="link-grid">' +
         NAT.map(function(x){ return '<li><a href="' + x[1] + '">' + esc(x[0]) + '</a></li>'; }).join("") + '</ul>';
    if (ind) h += '<p>Read the <a href="' + ind + '">' + esc(indName) + ' SBA loan guide</a> for what lenders look for in your industry.</p>';
    h += '<h3>Get introduced to lenders for free</h3><p>The SBA\'s Lender Match sends your request to participating SBA lenders, who reply within about two business days if they\'re interested. It\'s free and run by the SBA.</p>' +
         '<p><a class="btn-match" target="_blank" rel="noopener" href="' + SBA_LENDER_MATCH + '" data-out="sba-lender-match">Continue to SBA Lender Match</a></p>' +
         '<p class="src">Before you apply, gather your documents: see the <a href="/blog/SBA-Loan-Documentation/">SBA loan documentation checklist</a> and <a href="/blog/SBA-borrower-eligibility/">who is eligible</a>.</p>';
    out.innerHTML = h; out.classList.add("on");
    out.scrollIntoView({behavior: "smooth", block: "start"});
    track("lender_match_submit", {state: st, amount: amt, use: use, industry: indName || "other", source: source});
  });
  out.addEventListener("click", function(ev){
    var a = ev.target.closest("a"); if (!a) return;
    track("lender_match_click", {target: a.getAttribute("data-out") || a.getAttribute("href"), source: source});
  });
})();
