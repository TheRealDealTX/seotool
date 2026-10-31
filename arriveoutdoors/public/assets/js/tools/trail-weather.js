/* Trail Weather Forecast & Hike Score */
(function () {
  "use strict";
  var $ = AO.$, out = $("#result"), status = $("#status");
  function show(place) {
    $("#place-name").textContent = place.name;
    AO.renderForecast(out, place);
    var p = new URLSearchParams({ lat: place.lat.toFixed(4), lon: place.lon.toFixed(4), name: place.name });
    history.replaceState(null, "", "?" + p.toString());
    AO.store.set("lastPlace", place);
  }
  AO.placePicker($("#place"), show);
  $("#locate").addEventListener("click", function () { AO.locateMe(show, status); });
  AO.$$("[data-lat]").forEach(function (b) {
    b.addEventListener("click", function () {
      show({ name: b.dataset.name, lat: +b.dataset.lat, lon: +b.dataset.lon, elevation: b.dataset.elev ? +b.dataset.elev : undefined });
    });
  });
  var q = new URLSearchParams(location.search), last = AO.store.get("lastPlace", null);
  if (q.get("lat")) show({ name: q.get("name") || "Selected place", lat: +q.get("lat"), lon: +q.get("lon") });
  else if (last) show(last);
})();
