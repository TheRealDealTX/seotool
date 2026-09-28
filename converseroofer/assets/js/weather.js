/* Live weather for Converse, TX — Open-Meteo (no key) + NWS active alerts. */
(function(){
  var cfg = window.CR_CONFIG || {};
  var lat = cfg.lat || 29.518, lon = cfg.lon || -98.316, tz = cfg.timezone || 'America/Chicago';

  var CODES = {
    0:['Clear','☀️'],1:['Mostly clear','🌤️'],2:['Partly cloudy','⛅'],3:['Overcast','☁️'],
    45:['Fog','🌫️'],48:['Freezing fog','🌫️'],51:['Light drizzle','🌦️'],53:['Drizzle','🌦️'],55:['Heavy drizzle','🌧️'],
    56:['Freezing drizzle','🌧️'],57:['Freezing drizzle','🌧️'],61:['Light rain','🌧️'],63:['Rain','🌧️'],65:['Heavy rain','🌧️'],
    66:['Freezing rain','🌧️'],67:['Freezing rain','🌧️'],71:['Light snow','🌨️'],73:['Snow','🌨️'],75:['Heavy snow','❄️'],77:['Snow grains','🌨️'],
    80:['Rain showers','🌦️'],81:['Showers','🌧️'],82:['Heavy showers','⛈️'],85:['Snow showers','🌨️'],86:['Snow showers','🌨️'],
    95:['Thunderstorm','⛈️'],96:['Thunderstorm w/ hail','🌩️'],99:['Severe storm w/ hail','🌩️']
  };
  function desc(c){ return CODES[c] || ['—','🌡️']; }
  function dayName(iso){ return new Date(iso + 'T12:00:00').toLocaleDateString('en-US',{weekday:'short'}); }
  function mmdd(iso){ var d = new Date(iso + 'T12:00:00'); return (d.getMonth()+1) + '/' + d.getDate(); }
  function $(id){ return document.getElementById(id); }
  function riskFor(code, gust, pp){
    if (code === 96 || code === 99) return 'high';
    if (code === 95 || code === 82 || gust >= 45) return 'mod';
    if (pp >= 60 && code >= 80) return 'mod';
    return 'low';
  }

  var url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon +
    '&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_gusts_10m,wind_direction_10m' +
    '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_gusts_10m_max' +
    '&hourly=precipitation_probability,weather_code' +
    '&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=' + encodeURIComponent(tz) + '&forecast_days=7';

  fetch(url).then(function(r){ return r.json(); }).then(function(d){
    var c = d.current, dd = d.daily;
    var now = desc(c.weather_code);

    // Mini widget (home page)
    var mini = $('wx-mini');
    if (mini) {
      mini.innerHTML = '<span class="ic">' + now[1] + '</span><div><span class="t">' + Math.round(c.temperature_2m) + '°F</span><small>' + now[0] + ' · Converse, TX · gusts ' + Math.round(c.wind_gusts_10m) + ' mph</small></div><a href="weather">7-day &amp; alerts →</a>';
    }

    // Full page
    if ($('wx-temp')) {
      $('wx-temp').textContent = Math.round(c.temperature_2m) + '°';
      $('wx-icon').textContent = now[1];
      $('wx-desc').textContent = now[0];
      $('wx-feels').textContent = Math.round(c.apparent_temperature) + '°F';
      $('wx-hum').textContent = c.relative_humidity_2m + '%';
      $('wx-wind').textContent = Math.round(c.wind_speed_10m) + ' mph';
      $('wx-gust').textContent = Math.round(c.wind_gusts_10m) + ' mph';
      $('wx-precip').textContent = (c.precipitation || 0).toFixed(2) + ' in';
      $('wx-updated').textContent = new Date(c.time).toLocaleString('en-US',{timeZone: tz, weekday:'short', hour:'numeric', minute:'2-digit'});

      // Storm risk (next 48h)
      var worst = 'low';
      var rank = {low:0, mod:1, high:2};
      for (var i = 0; i < 2 && i < dd.time.length; i++) {
        var r = riskFor(dd.weather_code[i], dd.wind_gusts_10m_max[i], dd.precipitation_probability_max[i]);
        if (rank[r] > rank[worst]) worst = r;
      }
      var pill = $('wx-risk');
      pill.className = 'risk-pill ' + worst;
      pill.textContent = worst === 'high' ? 'HIGH — hail/severe storms possible' : worst === 'mod' ? 'MODERATE — thunderstorms or strong gusts possible' : 'LOW — no severe weather in the forecast';

      var days = $('wx-days');
      days.innerHTML = '';
      dd.time.forEach(function(t, i){
        var w = desc(dd.weather_code[i]);
        var risk = riskFor(dd.weather_code[i], dd.wind_gusts_10m_max[i], dd.precipitation_probability_max[i]);
        var el = document.createElement('div');
        el.className = 'wx-day' + (risk !== 'low' ? ' risk' : '');
        el.innerHTML = '<div class="d">' + (i === 0 ? 'Today' : dayName(t)) + '</div><div class="small">' + mmdd(t) + '</div><div class="ic" title="' + w[0] + '">' + w[1] + '</div>' +
          '<div><span class="hi">' + Math.round(dd.temperature_2m_max[i]) + '°</span> <span class="lo">' + Math.round(dd.temperature_2m_min[i]) + '°</span></div>' +
          '<div class="pp">' + (dd.precipitation_probability_max[i] || 0) + '% rain</div>' +
          '<div class="small">gusts ' + Math.round(dd.wind_gusts_10m_max[i]) + ' mph</div>' +
          '<div class="small">' + w[0] + '</div>';
        days.appendChild(el);
      });
    }
  }).catch(function(){
    var mini = $('wx-mini'); if (mini) mini.style.display = 'none';
    if ($('wx-desc')) $('wx-desc').textContent = 'Live weather is temporarily unavailable.';
    if ($('wx-days')) $('wx-days').innerHTML = '<div class="wx-day" style="grid-column:1/-1">Forecast unavailable right now. See <a href="https://forecast.weather.gov/MapClick.php?lat=29.518&lon=-98.316" target="_blank" rel="noopener">weather.gov</a>.</div>';
    if ($('wx-risk')) { $('wx-risk').className = 'risk-pill low'; $('wx-risk').textContent = 'Unavailable — check NWS'; }
  });

  // NWS active alerts for this point
  var box = $('wx-alerts');
  if (box) {
    fetch('https://api.weather.gov/alerts/active?point=' + lat + ',' + lon, {headers: {'Accept': 'application/geo+json'}})
      .then(function(r){ return r.json(); })
      .then(function(d){
        var feats = (d && d.features) || [];
        if (!feats.length) {
          box.innerHTML = '<div class="alert info"><h4>No active NWS alerts for Converse, TX</h4><p>Checked ' + new Date().toLocaleTimeString('en-US',{timeZone: tz, hour:'numeric', minute:'2-digit'}) + ' Central. Alerts come from the National Weather Service Austin/San Antonio office.</p></div>';
          return;
        }
        box.innerHTML = feats.map(function(f){
          var p = f.properties || {};
          var sev = (p.severity || '').toLowerCase();
          var cls = (sev === 'extreme' || sev === 'severe') ? 'severe' : (sev === 'moderate' ? 'watch' : 'info');
          var until = p.ends || p.expires;
          return '<div class="alert ' + cls + '"><h4>' + (p.event || 'Alert') + '</h4><p>' + (p.headline || '') + (until ? ' — until ' + new Date(until).toLocaleString('en-US',{timeZone: tz, weekday:'short', hour:'numeric', minute:'2-digit'}) : '') + '</p></div>';
        }).join('');
      })
      .catch(function(){
        box.innerHTML = '<div class="alert info"><h4>Alert feed unavailable</h4><p>Check <a href="https://www.weather.gov/ewx/" target="_blank" rel="noopener">weather.gov/ewx</a> for current NWS Austin/San Antonio alerts.</p></div>';
      });
  }
})();
