<?php
defined('TR_ROOT') || exit;
$crumbs = [['Terms of Use', '/terms-of-use/']];
layout_start([
    'title' => 'Terms of Use', 'description' => 'Terms for using templeroofs.com, including our roofing tools, weather information and general roofing content.',
    'path' => '/terms-of-use/', 'crumbs' => $crumbs,
]);
page_hero(['h1' => 'Terms of Use', 'lead' => 'Effective October 3, 2026. Please read these terms before using templeroofs.com.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true]);
?>
<div class="container container--narrow">
  <article class="prose legal">
    <p>By using templeroofs.com (the "site"), operated by Temple Roofers, you agree to these terms. If you do not agree, please do not use the site.</p>
    <h2>General information only</h2>
    <p>Articles, guides and other content on this site are general information about roofing in Central Texas. They are not professional advice for your specific property, and they are not legal, insurance or financial advice. Every roof is different; a professional inspection is the only reliable way to assess your roof's condition.</p>
    <h2>Roofing tools and estimates</h2>
    <p>The roof replacement cost calculator, roof pitch and area calculator and storm damage self-check are planning aids. Their results are approximations based on the inputs you enter and on illustrative assumptions that may not reflect current material prices, labor rates or the conditions of your roof. Results are not quotes, bids or binding estimates, and the self-check does not diagnose damage or predict insurance outcomes. Only a written estimate following an on-site inspection reflects actual pricing.</p>
    <h2>Weather information</h2>
    <p>Weather conditions, forecasts and alerts are provided by third-party sources (Open-Meteo and the National Weather Service) and may be delayed, incomplete or inaccurate. The roof-weather indicator is informational only and is not an official warning. Always follow official National Weather Service alerts and local emergency officials for safety decisions.</p>
    <h2>Insurance</h2>
    <p>Temple Roofers is a roofing contractor, not a licensed public adjuster or insurance company. We do not negotiate claims on your behalf, interpret your policy or guarantee coverage. Texas law requires policyholders to pay their own deductible, and we do not waive, absorb or rebate deductibles.</p>
    <h2>Safety</h2>
    <p>Nothing on this site is an instruction to climb onto a roof. Roofs can be slippery, steep and structurally compromised after storms. Leave rooftop work to trained professionals with proper safety equipment.</p>
    <h2>Images</h2>
    <p>Photographs on this site are licensed stock images used for illustration and do not depict specific Temple Roofers projects unless stated.</p>
    <h2>Acceptable use</h2>
    <p>Do not misuse the site, submit false or automated form entries, attempt to disrupt its operation or access non-public areas.</p>
    <h2>Intellectual property</h2>
    <p>Site text, design and tools are owned by Temple Roofers or used with permission. You may share links to our pages, but please do not copy substantial portions of the content without permission.</p>
    <h2>Limitation of liability</h2>
    <p>The site is provided "as is" without warranties of any kind. To the extent permitted by law, Temple Roofers is not liable for losses arising from use of the site or reliance on its content, tools or weather information.</p>
    <h2>Governing law</h2>
    <p>These terms are governed by the laws of the State of Texas.</p>
    <h2>Changes and contact</h2>
    <p>We may update these terms at any time; the effective date above shows the latest revision. Questions? Call <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_intl')) ?></a> or visit our <a href="/contact/">contact page</a>. See also our <a href="/privacy-policy/">Privacy Policy</a>.</p>
  </article>
</div>
<?php layout_end();
