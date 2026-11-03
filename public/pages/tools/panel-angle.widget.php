<?php defined('SCC') || exit; ?>
<div class="tool" data-tool="panel-angle">
  <div class="tool-head"><?= icon('angle', 22) ?><strong>Solar Panel Angle Calculator</strong><span>Tilt + direction for your location</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
      <div class="field">
        <label for="pa-city">Your location</label>
        <select id="pa-city" name="city">
          <option value="">Choose a city…</option>
          <optgroup label="United States">
            <option value="61.2">Anchorage, AK</option><option value="33.7">Atlanta, GA</option><option value="42.4">Boston, MA</option>
            <option value="41.9">Chicago, IL</option><option value="32.8">Dallas, TX</option><option value="39.7">Denver, CO</option>
            <option value="21.3">Honolulu, HI</option><option value="29.8">Houston, TX</option><option value="36.2">Las Vegas, NV</option>
            <option value="34.1">Los Angeles, CA</option><option value="25.8">Miami, FL</option><option value="45.0">Minneapolis, MN</option>
            <option value="36.2">Nashville, TN</option><option value="40.7" selected>New York, NY</option><option value="33.4">Phoenix, AZ</option>
            <option value="45.5">Portland, OR</option><option value="40.8">Salt Lake City, UT</option><option value="29.4">San Antonio, TX</option>
            <option value="37.8">San Francisco, CA</option><option value="47.6">Seattle, WA</option><option value="38.9">Washington, DC</option>
          </optgroup>
          <optgroup label="Canada">
            <option value="51.0">Calgary</option><option value="45.4">Ottawa</option><option value="43.7">Toronto</option><option value="49.3">Vancouver</option>
          </optgroup>
          <optgroup label="UK, Ireland & Europe">
            <option value="52.4">Amsterdam</option><option value="52.5">Berlin</option><option value="53.3">Dublin</option><option value="56.0">Edinburgh</option>
            <option value="51.5">London</option><option value="40.4">Madrid</option><option value="53.5">Manchester</option><option value="48.9">Paris</option>
          </optgroup>
          <optgroup label="Australia & New Zealand">
            <option value="-36.9">Auckland</option><option value="-27.5">Brisbane</option><option value="-37.8">Melbourne</option>
            <option value="-32.0">Perth</option><option value="-33.9">Sydney</option>
          </optgroup>
          <optgroup label="Africa, Asia & Latin America">
            <option value="-33.9">Cape Town</option><option value="28.6">Delhi</option><option value="25.2">Dubai</option>
            <option value="-26.2">Johannesburg</option><option value="6.5">Lagos</option><option value="14.6">Manila</option>
            <option value="19.4">Mexico City</option><option value="19.1">Mumbai</option><option value="-1.3">Nairobi</option>
            <option value="24.7">Riyadh</option><option value="-23.6">São Paulo</option><option value="1.4">Singapore</option>
          </optgroup>
        </select>
      </div>
      <div class="field">
        <label for="pa-lat">Latitude <output data-for="lat" data-dec="1" data-suffix="°"></output></label>
        <div class="row2">
          <input id="pa-lat" type="number" name="lat" min="-70" max="70" step="0.1" value="40.7" inputmode="decimal">
          <button type="button" class="btn btn-line btn-sm" data-geo><?= icon('compass', 16) ?> Use my location</button>
        </div>
        <small>Negative numbers = southern hemisphere. Your location never leaves your device.</small>
      </div>
      <div class="field">
        <span class="lbl">Optimize for</span>
        <div class="seg">
          <label><input type="radio" name="goal" value="winter" checked><span>Winter-first (recommended)</span></label>
          <label><input type="radio" name="goal" value="year"><span>Year-round</span></label>
          <label><input type="radio" name="goal" value="summer"><span>Summer</span></label>
        </div>
        <small>Solar cameras run short of power in winter, not summer, so a steeper winter-biased tilt keeps the battery fuller when it matters.</small>
      </div>
      <div class="field">
        <span class="lbl">Snow where you live?</span>
        <div class="seg">
          <label><input type="radio" name="snow" value="0" checked><span>Rarely</span></label>
          <label><input type="radio" name="snow" value="1"><span>Regular snow</span></label>
        </div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="result-hero">
        <div class="big" data-o="tilt">40°</div>
        <p data-o="summary"></p>
      </div>
      <div class="panel-viz" data-o="viz"></div>
      <div class="results" style="margin-top:12px">
        <div class="res"><b data-o="w">—</b><span>Winter tilt</span></div>
        <div class="res"><b data-o="sp">—</b><span>Spring &amp; fall tilt</span></div>
        <div class="res"><b data-o="su">—</b><span>Summer tilt</span></div>
        <div class="res"><b data-o="noon">—</b><span>Lowest noon sun (winter solstice)</span></div>
      </div>
      <h4>Noon sun height through the year</h4>
      <div class="chart" data-o="chart"></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button><button type="button" class="btn btn-line btn-sm" data-act="print">Print</button></div>
      <p class="tool-note">Tilt is measured from horizontal (0° = flat, 90° = vertical). Point the panel at true south/north, not magnetic: check your local magnetic declination with NOAA’s calculator.</p>
    </div>
  </form>
</div>
