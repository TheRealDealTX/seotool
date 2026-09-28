<?php
$meta['title'] = 'Shingle Wind Damage Calculator & Claim Payout Calculator';
$meta['description'] = 'See what 40–180 mph winds do to shingles by wind rating, compare 10 top manufacturers\' wind warranties, and estimate your claim payout. Free Galveston tools.';
$meta['crumb'] = 'Wind & Claim Calculators';
$meta['schema'][] = ['@type' => 'WebApplication', 'name' => 'Shingle Wind Damage Calculator', 'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'url' => SITE_URL . '/calculators/'];
$meta['schema'][] = ['@type' => 'WebApplication', 'name' => 'Claim Payout & Deductible Calculator', 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'url' => SITE_URL . '/calculators/#claim-calc'];

// Manufacturer wind warranties (research notes, Sept 2026). Warranty terms change — verify on current PDFs.
$makers = [
    ['GAF', 'Timberline HDZ', 130, 'No max-speed cap (WindProven)', 'LayerLock shingles + 4 GAF accessories (starter, underlayment, ridge cap, leak barrier or ventilation)', 'D3161 F · D7158 H', 'https://www.gaf.com/en-us/resources/warranties/windproven'],
    ['Owens Corning', 'Duration / TruDefinition Duration', 130, '160 mph', 'Total Protection Roofing System components + OC starter at eaves and rakes', 'D3161 F · D7158 H', 'https://www.owenscorning.com/en-us/roofing/warranty'],
    ['CertainTeed', 'Landmark / Landmark PRO', 110, '130 mph', 'CertainTeed starter + CertainTeed hip &amp; ridge', 'D3161 F · D7158 H', 'https://www.certainteed.com/products/residential-roofing-products/landmark-pro'],
    ['IKO', 'Cambridge', 110, '130 mph', '6 nails per shingle (high-wind application)', 'D3161 F · D7158 H', 'https://www.iko.com/na/product/cambridge/'],
    ['IKO', 'Dynasty', 130, '—', 'ArmourZone nailing strip, standard nailing', 'D3161 F · D7158 H', 'https://www.iko.com/na/document/us-iko-limited-warranty/'],
    ['Atlas', 'Pinnacle Pristine', 130, '—', 'Standard 4-nail application (6 nails on steep slope)', 'Verify on spec sheet', 'https://www.atlasroofing.com/products/roof-shingles/pinnacle-pristine-shingles'],
    ['Malarkey', 'Vista / Highlander', 110, '130 mph', '6 nails + Malarkey starter and hip/ridge', 'D7158 H', 'https://www.malarkeyroofing.com/products/shingles-overview/vista-shingles/'],
    ['TAMKO', 'Heritage', 110, '130 mph', '6-nail high-wind application + TAMKO starter with sealant at eaves and rakes', 'D3161 F · D7158 H', 'https://www.tamko.com/heritage'],
    ['DECRA', 'Stone-coated steel', 120, '—', 'Lifetime limited warranty; Miami-Dade NOA / Florida HVHZ approvals', 'Metal (Miami-Dade NOA)', 'https://www.decra.com/blog/can-metal-roofs-weather-hurricane-force-winds'],
    ['DaVinci Roofscapes', 'Composite slate &amp; shake', 110, 'Tested to 180 mph (select profiles, TAS-125)', 'Warranty mph varies by profile — verify', 'D3161 F', 'https://www.westlakeroyalbuildingproducts.com/roofing/davinci-roofscapes'],
    ['F-Wave', 'REVIA synthetic', 130, '150 mph (XTM line)', 'WeatherForce Advantage warranty', 'D3161 F · D7158 H', 'https://fwaveroofing.com/revia-shingles/'],
];
echo page_hero(icon('calc', 18) . ' Free calculators', 'What Wind Does to Shingles — Wind &amp; Claim Calculators',
    'Move the slider and watch what 40 to 180 mph winds do to a roof rated for 60, 90, 110, 130 or 150 mph. Then see how your insurance offer compares with what your claim may really be worth.');
?>
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <div class="calc" id="shingle-calc">
      <div class="calc-head"><div class="badge-ico"><?= icon('wind', 30) ?></div><div><h2>Calculator 1: Shingle Wind Damage Calculator</h2><p style="margin:0">Wind speed vs. shingle wind rating, roof age, exposure and nailing</p></div></div>
      <div class="calc-body">
        <div class="calc-controls">
          <label for="wind">Wind speed (3-second gust)
            <div class="range-row"><input type="range" id="wind" min="40" max="180" step="5" value="95"><output id="wind-out" for="wind">95 mph</output></div></label>
          <label for="rating">Shingle wind rating
            <select id="rating">
              <option value="60">60 mph — 3-tab, ASTM D3161 Class A</option>
              <option value="90">90 mph — ASTM D3161 Class D / D7158 Class D</option>
              <option value="110" selected>110 mph — ASTM D3161 Class F (standard architectural)</option>
              <option value="120">120 mph — ASTM D7158 Class G</option>
              <option value="130">130 mph — enhanced warranty (starter, ridge, 6 nails)</option>
              <option value="150">150 mph — ASTM D7158 Class H / high-wind system</option>
            </select></label>
          <label for="age">Roof age
            <div class="range-row"><input type="range" id="age" min="0" max="30" step="1" value="8"><output id="age-out" for="age">8 yrs</output></div></label>
          <label for="exposure">Location / exposure
            <select id="exposure">
              <option value="0.85">Mainland, sheltered by trees and houses</option>
              <option value="1" selected>Open coastal (most of Galveston County)</option>
              <option value="1.15">Beachfront / bayfront — open water exposure</option>
            </select></label>
          <label for="nails">Installation
            <select id="nails">
              <option value="0.93">Standard 4-nail</option>
              <option value="1" selected>High-wind 6-nail + manufacturer starter</option>
              <option value="0.8">Unknown / poorly nailed or overdriven</option>
            </select></label>
          <p class="small muted">Educational model based on ASTM test classes and typical sealant aging. It does not replace a roof inspection.</p>
        </div>
        <div class="calc-view">
          <svg viewBox="0 0 700 360" role="img" aria-label="Animated roof showing shingle damage at the selected wind speed">
            <defs><linearGradient id="csky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16456b"/><stop offset="1" stop-color="#0b2540"/></linearGradient></defs>
            <rect width="700" height="360" fill="url(#csky)"/>
            <g stroke="#cfe4f3" stroke-width="3" stroke-linecap="round" opacity=".7">
              <path class="gust" d="M0 40h90"/><path class="gust" d="M0 70h60" style="animation-delay:.3s"/><path class="gust" d="M0 25h120" style="animation-delay:.7s"/>
              <path class="gust" d="M0 55h70" style="animation-delay:1s"/><path class="gust" d="M0 85h100" style="animation-delay:.5s"/><path class="gust" d="M0 15h80" style="animation-delay:1.2s"/>
            </g>
            <path d="M60 280 220 90h260l160 190z" fill="#b08d57"/><path d="M60 280 220 90h260l160 190z" fill="none" stroke="#0b2540" stroke-width="4"/><g stroke="#8a6d3f" stroke-width="2" opacity=".6"><path d="M145 180h410M100 230h500M190 130h320"/></g>
            <g id="roof-shingles"></g>
            <rect x="80" y="280" width="540" height="40" fill="#f7f1e6"/>
            <rect x="0" y="320" width="700" height="40" fill="#0b4f78"/>
            <text id="svg-wind" x="680" y="44" text-anchor="end" font-family="Barlow, sans-serif" font-weight="800" font-size="34" fill="#fff">95 MPH</text>
            <g transform="translate(0 338)">
              <rect x="70" y="0" width="560" height="8" rx="4" fill="#58b6e0" opacity=".35"/>
              <g font-family="Barlow, sans-serif" font-size="11" font-weight="700" fill="#cfe4f3" text-anchor="middle">
                <text x="257" y="22">60</text><text x="350" y="22">90</text><text x="412" y="22">110</text><text x="474" y="22">130</text><text x="537" y="22">150</text>
              </g>
              <g fill="#cfe4f3"><rect x="256" y="-2" width="2" height="12"/><rect x="349" y="-2" width="2" height="12"/><rect x="411" y="-2" width="2" height="12"/><rect x="473" y="-2" width="2" height="12"/><rect x="536" y="-2" width="2" height="12"/></g>
              <rect id="scale-marker" x="360" y="-6" width="5" height="20" rx="2" fill="#f97316"/>
            </g>
          </svg>
          <div class="risk-meter" aria-hidden="true"><i id="meter"></i></div>
          <div class="risk-labels"><span>None</span><span>Low</span><span>Moderate</span><span>High</span><span>Severe</span></div>
          <div class="result-grid">
            <div class="result"><small>Damage risk</small><b id="r-level">—</b></div>
            <div class="result"><small>Effective rating</small><b id="r-eff">—</b></div>
            <div class="result"><small>Shingles likely lost</small><b id="r-pct">—</b></div>
            <div class="result"><small>Wind pressure</small><b id="r-psf">—</b></div>
            <div class="result"><small>Pull per exposed shingle</small><b id="r-pull">—</b></div>
            <div class="result"><small>Next step</small><b><?= phone_link('', 'Call us') ?></b></div>
          </div>
          <div class="verdict" id="verdict"></div>
        </div>
      </div>
    </div>

    <?= banner('Calculator says your roof took damage? Call for an expert consultation.', 'Creased and unsealed shingles are storm damage — and easy for insurers to miss.') ?>

    <div class="prose narrow" style="width:100%;max-width:none">
      <h2>Wind speed vs. shingle ratings: what happens to your roof</h2>
      <div class="table-wrap"><table class="data">
        <thead><tr><th>Wind (gust)</th><th>60 mph 3-tab</th><th>90 mph (Class D)</th><th>110 mph (Class F)</th><th>130 mph enhanced</th><th>150 mph (Class H)</th></tr></thead>
        <tbody>
          <tr><td><strong>50–60 mph</strong></td><td><span class="tag hot">Unsealed tabs</span></td><td><span class="tag green">Minimal</span></td><td><span class="tag green">Minimal</span></td><td><span class="tag green">Minimal</span></td><td><span class="tag green">Minimal</span></td></tr>
          <tr><td><strong>70–80 mph</strong></td><td><span class="tag red">Missing shingles</span></td><td><span class="tag hot">Creasing at edges</span></td><td><span class="tag">Seal stress</span></td><td><span class="tag green">Minimal</span></td><td><span class="tag green">Minimal</span></td></tr>
          <tr><td><strong>90–100 mph</strong></td><td><span class="tag red">Widespread loss</span></td><td><span class="tag red">Missing at ridges/rakes</span></td><td><span class="tag hot">Creasing, lifted tabs</span></td><td><span class="tag">Seal stress</span></td><td><span class="tag green">Minimal</span></td></tr>
          <tr><td><strong>110–120 mph</strong></td><td><span class="tag red">Decking exposed</span></td><td><span class="tag red">Widespread loss</span></td><td><span class="tag red">Missing shingles</span></td><td><span class="tag hot">Edge creasing</span></td><td><span class="tag">Seal stress</span></td></tr>
          <tr><td><strong>130–150 mph</strong></td><td><span class="tag red">Roof failure</span></td><td><span class="tag red">Decking exposed</span></td><td><span class="tag red">Widespread loss</span></td><td><span class="tag red">Missing shingles</span></td><td><span class="tag hot">Creasing, some loss</span></td></tr>
        </tbody>
      </table></div>
      <p class="small muted">Typical outcomes for a properly installed roof in open coastal exposure. Aged sealant, poor nailing and beachfront exposure all lower the speed at which damage starts.</p>

      <h3>What the test classes mean</h3>
      <div class="grid g3">
        <div class="card"><h3>ASTM D3161</h3><p>Fan-induced wind test, 2 hours at speed.<br><strong>Class A</strong> 60 mph · <strong>Class D</strong> 90 mph · <strong>Class F</strong> 110 mph</p></div>
        <div class="card"><h3>ASTM D7158</h3><p>Uplift-resistance test based on ASCE 7 basic wind speed.<br><strong>Class D</strong> 90 mph · <strong>Class G</strong> 120 mph · <strong>Class H</strong> 150 mph</p></div>
        <div class="card hot"><h3>Galveston requirement</h3><p>Where the code's allowable-stress wind speed exceeds 100 mph — all of the Galveston area — shingles must be <strong>D7158 Class H or D3161 Class F</strong>. See <a href="/galveston-local-code/">local code</a>.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="manufacturers">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Wind ratings by brand</span><h2>How much wind are 10 top shingle manufacturers rated for?</h2><p>Standard and enhanced wind warranties for each maker's flagship residential product.</p></div>
    <div class="bars reveal" style="max-width:900px;margin:0 auto 36px">
      <?php foreach ($makers as $m): $top = (int)preg_replace('/\D.*/', '', $m[3]) ?: $m[2]; if (str_starts_with($m[3], 'No max')) $top = 180; ?>
      <div class="bar-row"><span><strong><?= e($m[0]) ?></strong></span><div class="bar-track"><div class="bar-fill" data-w="<?= round($m[2] / 180 * 100) ?>"></div></div><b><?= $m[2] ?> mph</b></div>
      <?php endforeach ?>
    </div>
    <div class="table-wrap"><table class="data">
      <thead><tr><th>Manufacturer</th><th>Product</th><th>Standard wind warranty</th><th>Enhanced / max</th><th>What the enhanced rating requires</th><th>Test class</th></tr></thead>
      <tbody>
      <?php foreach ($makers as $m): ?>
        <tr><td><strong><?= e($m[0]) ?></strong></td><td><?= $m[1] ?></td><td><span class="tag"><?= $m[2] ?> mph</span></td><td><?= $m[3] ?></td><td><?= $m[4] ?></td><td><?= $m[5] ?> <a href="<?= e($m[6]) ?>" rel="nofollow noopener" target="_blank" class="small">source</a></td></tr>
      <?php endforeach ?>
      </tbody>
    </table></div>
    <p class="small muted">Wind warranties generally cover shingle blow-off for a limited period (often 15 years) and only when installed to the manufacturer's instructions. Terms change often — confirm against the manufacturer's current warranty document for your installation date. Compiled September 2026.</p>
    <div class="callout warn"><?= icon('alert', 24) ?><div><strong>Claim tip:</strong> A shingle's wind rating is not a damage threshold your insurer gets to use against you. Aged sealant, installation defects and turbulence at ridges and corners mean roofs are routinely damaged below their rated speed — and that damage is still a covered windstorm loss.</div></div>
  </div>
</section>

<section class="section" id="claim-calc">
  <div class="wrap">
    <div class="calc">
      <div class="calc-head"><div class="badge-ico"><?= icon('dollar', 30) ?></div><div><h2>Calculator 2: Claim Payout &amp; Deductible Calculator</h2><p style="margin:0">Your insurer's offer vs. what you could net with a public adjuster</p></div></div>
      <div class="calc-body">
        <div class="calc-controls">
          <label for="coverage">Dwelling coverage (Coverage A)<input type="number" id="coverage" value="350000" min="0" step="5000"></label>
          <label for="ded">Windstorm / hurricane deductible
            <select id="ded">
              <option value="0.01" selected>1% of Coverage A</option><option value="0.02">2% of Coverage A</option><option value="0.05">5% of Coverage A</option>
              <option value="1000">$1,000 flat</option><option value="2500">$2,500 flat</option><option value="5000">$5,000 flat</option>
            </select></label>
          <label for="offer">Insurance company's estimate (before deductible)<input type="number" id="offer" value="18000" min="0" step="500"></label>
          <label for="damage">Full documented damage (contractor / PA estimate)<input type="number" id="damage" value="42000" min="0" step="500"></label>
          <label for="fee">Public adjuster fee
            <div class="range-row"><input type="range" id="fee" min="5" max="10" step="0.5" value="10"><output for="fee" id="fee-out">10%</output></div></label>
          <p class="small muted">Texas caps public adjuster fees at 10% (Ins. Code §4102.104). This calculator applies the fee to the entire payment — a conservative assumption.</p>
        </div>
        <div class="calc-view">
          <div class="result-grid">
            <div class="result"><small>Your deductible</small><b id="o-ded">—</b></div>
            <div class="result"><small>Offer is short by</small><b id="o-under">—</b></div>
            <div class="result"><small>Extra in your pocket</small><b id="o-gap" style="color:#16a34a">—</b></div>
          </div>
          <div class="money-bars mt">
            <div class="bar-row"><span>Insurer's offer, net</span><div class="bar-track"><div class="bar-fill ins" id="b-offer"></div></div><b id="b-offer-v">—</b></div>
            <div class="bar-row"><span>Full claim, net of deductible</span><div class="bar-track"><div class="bar-fill" id="b-full"></div></div><b id="b-full-v">—</b></div>
            <div class="bar-row"><span>You net with a public adjuster</span><div class="bar-track"><div class="bar-fill pa" id="b-pa"></div></div><b id="b-pa-v">—</b></div>
          </div>
          <div class="result-grid">
            <div class="result"><small>Offer after deductible</small><b id="o-offer">—</b></div>
            <div class="result"><small>Full claim after deductible</small><b id="o-full">—</b></div>
            <div class="result"><small>Net after PA fee</small><b id="o-pa">—</b></div>
          </div>
          <div class="verdict" id="o-msg"></div>
        </div>
      </div>
    </div>
    <p class="small muted mt">Illustration only. Results depend on your policy, the documented damage and the outcome of negotiation; no recovery amount is guaranteed.</p>
  </div>
</section>
<script>document.addEventListener('input',function(e){if(e.target.id==='fee'){document.getElementById('fee-out').value=e.target.value+'%';}});</script>
