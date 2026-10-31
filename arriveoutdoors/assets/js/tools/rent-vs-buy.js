/* Rent vs Buy Camping Gear Calculator */
(function () {
  "use strict";
  var $ = AO.$, $$ = AO.$$;
  function money(n) { return "$" + Math.round(n).toLocaleString(); }
  function calc() {
    var trips = Math.max(0, AO.num("#trips")), years = Math.max(1, AO.num("#years")), resale = AO.num("#resale") / 100;
    var rows = "", buyT = 0, rentT = 0, n = trips * years;
    $$("#items tbody tr").forEach(function (tr) {
      var on = tr.querySelector("input[type=checkbox]").checked;
      var buy = AO.num(tr.querySelector(".buy")), rent = AO.num(tr.querySelector(".rent"));
      var name = tr.dataset.name, cell = tr.querySelector(".be");
      if (!on) { cell.textContent = "—"; return; }
      var net = buy * (1 - resale);
      var be = rent > 0 ? Math.ceil(net / rent) : Infinity;
      cell.textContent = isFinite(be) ? be + " trips" : "—";
      buyT += net; rentT += rent * n;
      rows += "<li><span>" + name + "</span><span>" + (rent * n < net ? "Rent" : "Buy") + "</span></li>";
    });
    var save = Math.abs(buyT - rentT), better = rentT < buyT ? "Renting" : "Buying";
    $("#result").innerHTML = "<div class='result-big'>" + better + " wins</div><p class='result-sub'>Over " + n + " trip" + (n === 1 ? "" : "s") + " (" + trips + " a year for " + years + " year" + (years === 1 ? "" : "s") + "), " + better.toLowerCase() + " saves about " + money(save) + ".</p>" +
      "<ul class='result-list'><li><span>Cost to buy (after resale)</span><span>" + money(buyT) + "</span></li><li><span>Cost to rent every trip</span><span>" + money(rentT) + "</span></li></ul>" +
      "<h3>Item by item</h3><ul class='result-list'>" + rows + "</ul>" +
      "<div class='callout tip'>Rent first for gear you'll replace as you learn what you like (packs, tents); buy early for items that need a personal fit or hygiene (boots, sleeping pad, sleeping bag liner).</div>";
  }
  $("#rentform").addEventListener("input", calc);
  $("#rentform").addEventListener("change", calc);
  calc();
})();
