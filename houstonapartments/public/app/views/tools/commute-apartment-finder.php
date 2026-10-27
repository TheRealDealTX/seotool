<div class="tool-grid2 commute">
  <div class="tool-form">
    <label class="field">Work, school or place you visit often<input name="cf_addr" placeholder="e.g. 6565 Fannin St, Houston" autocomplete="street-address"></label>
    <div class="quick-places">
      <button type="button" data-place="29.7070,-95.4010">Texas Medical Center</button>
      <button type="button" data-place="29.7560,-95.3650">Downtown</button>
      <button type="button" data-place="29.7400,-95.4620">Galleria / Uptown</button>
      <button type="button" data-place="29.7840,-95.6360">Energy Corridor</button>
      <button type="button" data-place="29.5530,-95.0930">NASA / Clear Lake</button>
    </div>
    <label class="field">How far will you travel? <output data-out="miles">8 miles</output><input type="range" name="cf_miles" min="2" max="30" value="8"></label>
    <p class="tr-note" data-out="drive">About 15–25 minutes by car outside rush hour.</p>
    <button type="button" class="btn btn-grad btn-block" data-find>Show this area</button>
    <p class="form-msg" data-out="msg" role="status"></p>
  </div>
  <div class="tool-result map-result">
    <div id="commute-map" class="commute-map"></div>
    <a class="btn btn-grad btn-block" data-out="link" href="/apartments/" hidden>See apartments in this area</a>
  </div>
</div>
