<?php
// Inline SVG illustrations (no external images needed).

function art_hero_house() {
    return <<<SVG
<svg viewBox="0 0 560 440" role="img" aria-label="Galveston beach house in hurricane winds">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16456b"/><stop offset="1" stop-color="#0b2540"/></linearGradient>
    <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f8fc4"/><stop offset="1" stop-color="#0b4f78"/></linearGradient>
    <radialGradient id="eye" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e6f4fb" stop-opacity=".9"/><stop offset=".25" stop-color="#9fc3dc" stop-opacity=".5"/><stop offset="1" stop-color="#9fc3dc" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="560" height="440" rx="28" fill="url(#sky)"/>
  <g transform="translate(430 90)" opacity=".85">
    <circle r="80" fill="url(#eye)"/>
    <g fill="none" stroke="#cfe4f3" stroke-width="7" stroke-linecap="round" opacity=".75">
      <path d="M0-58C-40-56-62-20-50 12"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="9s" repeatCount="indefinite"/></path>
      <path d="M0 58C40 56 62 20 50-12"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="9s" repeatCount="indefinite"/></path>
      <path d="M-30-24C-10-40 20-36 30-14"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="6s" repeatCount="indefinite"/></path>
    </g>
    <circle r="9" fill="#0b2540"/>
  </g>
  <g stroke="#cfe4f3" stroke-width="3" stroke-linecap="round" opacity=".6">
    <path d="M20 120h120"><animate attributeName="opacity" values="0;.8;0" dur="1.8s" repeatCount="indefinite"/></path>
    <path d="M60 160h160"><animate attributeName="opacity" values="0;.8;0" dur="1.5s" begin=".4s" repeatCount="indefinite"/></path>
    <path d="M10 200h90"><animate attributeName="opacity" values="0;.8;0" dur="2s" begin=".8s" repeatCount="indefinite"/></path>
  </g>
  <g stroke="#58b6e0" stroke-width="2" opacity=".5">
    <path d="M80 40l-18 40M130 30l-18 40M180 45l-18 40M230 30l-18 40M280 40l-18 40M330 30l-18 40"/>
  </g>
  <path d="M0 360c60-18 120-18 180 0s120 18 180 0 120-18 200 0v80H0z" fill="url(#sea)"/>
  <path d="M0 380c60-14 120-14 180 0s120 14 180 0 120-14 200 0" stroke="#e6f4fb" stroke-width="3" fill="none" opacity=".6"/>
  <g transform="translate(150 150)">
    <g fill="#8a6d4b"><rect x="18" y="150" width="12" height="80"/><rect x="118" y="150" width="12" height="80"/><rect x="218" y="150" width="12" height="80"/></g>
    <rect x="8" y="140" width="232" height="14" fill="#6b5337"/>
    <rect x="18" y="62" width="212" height="80" fill="#f7f1e6"/>
    <g fill="#1f8fc4"><rect x="40" y="82" width="38" height="36" rx="3"/><rect x="170" y="82" width="38" height="36" rx="3"/></g>
    <rect x="104" y="80" width="40" height="62" rx="3" fill="#0b2540"/>
    <path d="M-6 66 124 0l130 66z" fill="#344050"/>
    <path d="M-6 66 124 0l130 66" fill="none" stroke="#0b2540" stroke-width="5" stroke-linejoin="round"/>
    <g fill="#f97316">
      <rect x="150" y="20" width="22" height="9" rx="2" transform="rotate(-25 160 25)"><animateTransform attributeName="transform" type="translate" values="0 0;90 -60" dur="2.4s" repeatCount="indefinite" additive="sum"/><animate attributeName="opacity" values="1;0" dur="2.4s" repeatCount="indefinite"/></rect>
      <rect x="180" y="34" width="20" height="8" rx="2" transform="rotate(-10 190 38)"><animateTransform attributeName="transform" type="translate" values="0 0;110 -40" dur="2.9s" begin=".6s" repeatCount="indefinite" additive="sum"/><animate attributeName="opacity" values="1;0" dur="2.9s" begin=".6s" repeatCount="indefinite"/></rect>
    </g>
    <path d="M40 40 L 70 25" stroke="#f97316" stroke-width="3" stroke-dasharray="4 5"/>
  </g>
  <g transform="translate(34 300)">
    <rect width="150" height="58" rx="12" fill="#fff"/>
    <text x="16" y="25" font-family="Barlow, sans-serif" font-weight="800" font-size="13" fill="#475569">WIND GUSTS</text>
    <text x="16" y="48" font-family="Barlow, sans-serif" font-weight="800" font-size="22" fill="#ea580c">110+ MPH</text>
  </g>
  <g transform="translate(380 300)">
    <rect width="150" height="58" rx="12" fill="#fff"/>
    <text x="16" y="25" font-family="Barlow, sans-serif" font-weight="800" font-size="13" fill="#475569">CLAIM STATUS</text>
    <text x="16" y="48" font-family="Barlow, sans-serif" font-weight="800" font-size="22" fill="#16a34a">REOPENED ✓</text>
  </g>
</svg>
SVG;
}

function art_fire() {
    return <<<SVG
<svg viewBox="0 0 520 400" role="img" aria-label="Fire and smoke damaged home illustration">
  <defs><linearGradient id="fs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b1d12"/><stop offset="1" stop-color="#0b2540"/></linearGradient>
  <radialGradient id="fl" cx=".5" cy=".8" r=".7"><stop offset="0" stop-color="#fde68a"/><stop offset=".45" stop-color="#f97316"/><stop offset="1" stop-color="#b91c1c" stop-opacity="0"/></radialGradient></defs>
  <rect width="520" height="400" rx="28" fill="url(#fs)"/>
  <g fill="#64748b" opacity=".55">
    <circle cx="300" cy="90" r="40"><animate attributeName="cy" values="110;40" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="4s" repeatCount="indefinite"/></circle>
    <circle cx="340" cy="80" r="30"><animate attributeName="cy" values="120;30" dur="3.2s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="3.2s" begin="1s" repeatCount="indefinite"/></circle>
    <circle cx="270" cy="70" r="26"><animate attributeName="cy" values="115;20" dur="3.6s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="3.6s" begin="2s" repeatCount="indefinite"/></circle>
  </g>
  <rect x="120" y="190" width="280" height="150" fill="#f7f1e6"/>
  <path d="M100 196 260 110l160 86z" fill="#1f2937"/>
  <rect x="150" y="220" width="60" height="50" fill="#1f2937"/><rect x="300" y="220" width="60" height="50" fill="#1f2937"/>
  <ellipse cx="330" cy="255" rx="40" ry="46" fill="url(#fl)"><animate attributeName="ry" values="46;54;46" dur="1s" repeatCount="indefinite"/></ellipse>
  <path d="M290 190c20-30 60-30 80 0" stroke="#111827" stroke-width="18" fill="none" opacity=".5"/>
  <rect x="230" y="260" width="50" height="80" fill="#0b2540"/>
  <rect y="340" width="520" height="60" fill="#0b2540"/>
  <g transform="translate(30 30)"><rect width="170" height="58" rx="12" fill="#fff"/><text x="16" y="25" font-family="Barlow, sans-serif" font-weight="800" font-size="13" fill="#475569">SMOKE &amp; SOOT</text><text x="16" y="48" font-family="Barlow, sans-serif" font-weight="800" font-size="20" fill="#ea580c">OFTEN MISSED</text></g>
</svg>
SVG;
}

function art_twia() {
    return <<<SVG
<svg viewBox="0 0 520 400" role="img" aria-label="TWIA claim file with windstorm damage">
  <defs><linearGradient id="tw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e4a73"/><stop offset="1" stop-color="#061a2e"/></linearGradient></defs>
  <rect width="520" height="400" rx="28" fill="url(#tw)"/>
  <g transform="translate(70 50) rotate(-4)"><rect width="250" height="310" rx="14" fill="#fff"/>
    <rect x="24" y="26" width="120" height="16" rx="4" fill="#0b2540"/><rect x="24" y="56" width="200" height="8" rx="4" fill="#dbe3ec"/><rect x="24" y="74" width="170" height="8" rx="4" fill="#dbe3ec"/>
    <rect x="24" y="104" width="200" height="60" rx="8" fill="#e6f4fb"/><text x="36" y="130" font-family="Barlow, sans-serif" font-weight="800" font-size="14" fill="#1f8fc4">WINDSTORM CLAIM</text><text x="36" y="152" font-family="Barlow, sans-serif" font-weight="700" font-size="13" fill="#475569">Date of loss · Photos · Estimate</text>
    <rect x="24" y="182" width="200" height="8" rx="4" fill="#dbe3ec"/><rect x="24" y="200" width="150" height="8" rx="4" fill="#dbe3ec"/><rect x="24" y="218" width="180" height="8" rx="4" fill="#dbe3ec"/>
    <g transform="translate(120 240) rotate(-12)"><rect width="110" height="44" rx="6" fill="none" stroke="#dc2626" stroke-width="4"/><text x="12" y="30" font-family="Barlow, sans-serif" font-weight="800" font-size="20" fill="#dc2626">DENIED</text></g>
  </g>
  <g transform="translate(250 150) rotate(6)"><rect width="210" height="200" rx="14" fill="#fff" stroke="#16a34a" stroke-width="4"/>
    <text x="20" y="40" font-family="Barlow, sans-serif" font-weight="800" font-size="16" fill="#0b2540">RE-INSPECTED &amp;</text><text x="20" y="62" font-family="Barlow, sans-serif" font-weight="800" font-size="16" fill="#0b2540">DOCUMENTED</text>
    <g fill="#16a34a"><circle cx="30" cy="96" r="9"/><circle cx="30" cy="126" r="9"/><circle cx="30" cy="156" r="9"/></g>
    <g fill="#dbe3ec"><rect x="48" y="91" width="130" height="10" rx="5"/><rect x="48" y="121" width="110" height="10" rx="5"/><rect x="48" y="151" width="140" height="10" rx="5"/></g>
  </g>
  <g stroke="#58b6e0" stroke-width="3" stroke-linecap="round" opacity=".7"><path d="M360 60h120"/><path d="M390 90h90"/><path d="M340 120h60"/></g>
</svg>
SVG;
}

function art_adjuster() {
    return <<<SVG
<svg viewBox="0 0 520 420" role="img" aria-label="Public adjuster inspecting a storm damaged roof">
  <defs><linearGradient id="ad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6f4fb"/><stop offset="1" stop-color="#f7f1e6"/></linearGradient></defs>
  <rect width="520" height="420" rx="28" fill="url(#ad)"/>
  <circle cx="430" cy="80" r="40" fill="#fde68a"/>
  <path d="M40 250 260 110l220 140z" fill="#344050"/>
  <g fill="#2f3a48" stroke="#1f2937" stroke-width="1.5">
    <rect x="150" y="190" width="40" height="18"/><rect x="190" y="190" width="40" height="18"/><rect x="230" y="190" width="40" height="18"/><rect x="270" y="190" width="40" height="18"/><rect x="310" y="190" width="40" height="18"/>
    <rect x="120" y="208" width="40" height="18"/><rect x="160" y="208" width="40" height="18"/><rect x="200" y="208" width="40" height="18"/><rect x="280" y="208" width="40" height="18"/><rect x="320" y="208" width="40" height="18"/>
  </g>
  <rect x="240" y="208" width="40" height="18" fill="#c8b18a"/>
  <rect x="240" y="208" width="40" height="18" fill="none" stroke="#ea580c" stroke-width="3" stroke-dasharray="5 4"/>
  <rect x="80" y="250" width="360" height="130" fill="#fff"/>
  <rect x="120" y="280" width="70" height="60" fill="#1f8fc4"/><rect x="330" y="280" width="70" height="60" fill="#1f8fc4"/><rect x="226" y="290" width="68" height="90" fill="#0b2540"/>
  <g transform="translate(300 120)"><circle cx="16" cy="0" r="14" fill="#f2c9a0"/><rect x="0" y="16" width="32" height="44" rx="10" fill="#f97316"/><rect x="3" y="-16" width="26" height="10" rx="5" fill="#fff"/><path d="M32 30l26-16" stroke="#0b2540" stroke-width="6" stroke-linecap="round"/><rect x="52" y="4" width="22" height="16" rx="3" fill="#0b2540"/></g>
  <g transform="translate(40 30)"><rect width="190" height="62" rx="12" fill="#fff" stroke="#dbe3ec"/><text x="16" y="26" font-family="Barlow, sans-serif" font-weight="800" font-size="13" fill="#475569">CREASED SHINGLES</text><text x="16" y="49" font-family="Barlow, sans-serif" font-weight="800" font-size="20" fill="#0b2540">DOCUMENTED ✓</text></g>
</svg>
SVG;
}

/** Circular wind gauge; $mph out of $max. */
function art_gauge($mph, $max = 160) {
    $pct = min(1, $mph / $max);
    $len = 251.3; // 2πr for r=40
    $dash = round($len * .75 * $pct, 1);
    $col = $mph >= 111 ? '#dc2626' : ($mph >= 74 ? '#ea580c' : '#eab308');
    return '<svg class="gauge" viewBox="0 0 100 100" role="img" aria-label="' . (int)$mph . ' mph">'
        . '<circle cx="50" cy="50" r="40" fill="none" stroke="#e9f1f7" stroke-width="10" stroke-dasharray="' . round($len * .75, 1) . ' ' . $len . '" transform="rotate(135 50 50)" stroke-linecap="round"/>'
        . '<circle cx="50" cy="50" r="40" fill="none" stroke="' . $col . '" stroke-width="10" stroke-dasharray="' . $dash . ' ' . $len . '" transform="rotate(135 50 50)" stroke-linecap="round"/>'
        . '<text x="50" y="52" text-anchor="middle" font-family="Barlow, sans-serif" font-weight="800" font-size="24" fill="#0b2540">' . (int)$mph . '</text>'
        . '<text x="50" y="68" text-anchor="middle" font-family="Barlow, sans-serif" font-weight="700" font-size="10" fill="#475569">MPH</text></svg>';
}
