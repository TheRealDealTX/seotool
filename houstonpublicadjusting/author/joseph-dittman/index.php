<?php
require dirname(__DIR__, 2) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Joseph Dittman', AUTHOR['url']]];
page_start([
    'title' => 'Joseph Dittman, Licensed Texas Public Adjuster | Houston Public Adjusters',
    'desc' => 'Joseph Dittman is a licensed Texas public adjuster (Rise Public Adjusting LLC, #3356839) who represents Houston homeowners and businesses on hurricane, hail, water and fire claims.',
    'path' => AUTHOR['url'],
    'image' => AUTHOR['photo'],
    'type' => 'profile',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'ProfilePage', 'url' => SITE_URL . AUTHOR['url'], 'mainEntity' => ['@id' => SITE_URL . '/#joseph-dittman']]],
]);
?>
<section class="page-hero"><div class="wrap two-col center">
  <div>
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow">Author &amp; public adjuster</p>
    <h1>Joseph Dittman</h1>
    <p class="lede"><?= AUTHOR['title'] ?> &middot; <?= LEGAL_NAME ?> &middot; TDI license #<?= LICENSE_NO ?></p>
    <div class="hero-actions"><a class="btn btn-accent" href="tel:<?= PHONE_E164 ?>">Call Joseph: <?= PHONE_DISPLAY ?></a><a class="btn btn-ghost-light" href="sms:<?= PHONE_E164 ?>">Text</a></div>
  </div>
  <div style="text-align:center"><img src="<?= AUTHOR['photo'] ?>" alt="Joseph Dittman, licensed Texas public adjuster" width="320" height="320" style="margin:0 auto;border-radius:50%" fetchpriority="high"></div>
</div></section>
<div class="wrap layout-sidebar">
  <div class="prose">
    <h2>About Joseph</h2>
    <p>Joseph Dittman is a licensed Texas public adjuster and the adjuster behind Houston Public Adjusters and its statewide sister firm, <a href="https://txpublicadjusting.com/" target="_blank" rel="noopener">TX Public Adjusting</a>. He is licensed through <?= LEGAL_NAME ?> (Texas Department of Insurance public adjuster license #<?= LICENSE_NO ?>) and represents policyholders only &mdash; never insurance companies.</p>
    <p>Joseph handles residential and commercial claims for hurricane, hail, wind, water, fire and storm damage across Houston and Texas, from Dallas and Austin to San Antonio and the Gulf Coast. The firm reviews more than 1,400 claim files a year, which means he has seen how nearly every major carrier scopes, prices and disputes Texas property claims.</p>
    <h2>How Joseph works a claim</h2>
    <ul class="checklist">
      <li><strong>Documentation first.</strong> Matterport 3D imaging, high-resolution photos, measurements and moisture readings so nothing can be dismissed as guesswork.</li>
      <li><strong>Carrier-grade estimates.</strong> Line-item estimates in Xactimate and Symbility, the same platforms insurance companies use.</li>
      <li><strong>Policy-backed negotiation.</strong> Every request ties back to a coverage, an endorsement or the Texas Insurance Code.</li>
      <li><strong>Plain-English updates.</strong> Clients know where the claim stands and what happens next.</li>
    </ul>
    <h2>Areas of focus</h2>
    <ul class="checklist">
      <li>Hurricane, tropical storm and derecho wind claims</li>
      <li>Hail and roof claims, supplements and matching disputes</li>
      <li>Water, plumbing and freeze losses</li>
      <li>Fire, smoke and contents claims</li>
      <li>Commercial property and business interruption</li>
      <li>Denied, delayed, underpaid and reopened claims</li>
    </ul>
    <h2>Credentials</h2>
    <div class="table-wrap"><table>
      <tbody>
        <tr><td><strong>License</strong></td><td>Texas public adjuster, Texas Department of Insurance &mdash; <?= LEGAL_NAME ?>, #<?= LICENSE_NO ?></td></tr>
        <tr><td><strong>Represents</strong></td><td>Policyholders only (homeowners, landlords, businesses)</td></tr>
        <tr><td><strong>Tools</strong></td><td>Xactimate, Symbility, Matterport 3D</td></tr>
        <tr><td><strong>Service area</strong></td><td>Greater Houston and statewide Texas</td></tr>
        <tr><td><strong>Verify</strong></td><td><a href="https://www.tdi.texas.gov/agent/agent-lookup.html" target="_blank" rel="noopener">TDI license lookup</a></td></tr>
      </tbody>
    </table></div>
    <h2>Articles by Joseph Dittman</h2>
  </div>
  <aside class="sidebar">
    <div class="side-card sticky"><?= lead_form('lead-author', 'Ask Joseph about your claim', 'Free review, no obligation.', true) ?></div>
  </aside>
</div>
<section class="section alt" style="padding-top:40px"><div class="wrap"><?= post_cards(array_keys(POSTS)) ?></div></section>
<?php
page_end();
