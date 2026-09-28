<?php
$meta['title'] = 'About Joseph Dittman | Galveston Public Adjuster';
$meta['description'] = 'Meet Joseph Dittman, licensed Texas public adjuster representing Galveston County homeowners and businesses on TWIA, hurricane, fire and flood claims.';
$meta['crumb'] = 'About';
$meta['schema'][] = ['@type' => 'AboutPage', 'url' => SITE_URL . '/about/', 'mainEntity' => ['@type' => 'Person', 'name' => AUTHOR, 'jobTitle' => AUTHOR_ROLE, 'image' => SITE_URL . AUTHOR_PHOTO, 'worksFor' => ['@id' => SITE_URL . '/#business']]];
echo page_hero(icon('user', 18) . ' About us', 'About Galveston Public Adjuster', 'We represent policyholders — never insurance companies. When a storm, fire or flood hits your property, our job is to make sure your insurance pays what your policy promises.', art_adjuster());
?>
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <img class="adjuster-photo" src="<?= AUTHOR_PHOTO ?>" alt="<?= AUTHOR ?>, licensed Texas public adjuster" width="320" height="320" style="margin:0 0 20px">
      <span class="kicker">Meet your adjuster</span>
      <h2><?= AUTHOR ?></h2>
      <p><?= AUTHOR ?> is a licensed Texas public adjuster who represents homeowners, landlords and businesses across Galveston Island and Galveston County. Joseph's focus is the claims that matter most on the coast: TWIA windstorm and hurricane losses, fire and smoke damage, flood and water claims, and claims that have been denied or underpaid.</p>
      <p>Joseph handles each file personally — from the first inspection to the final payment. Joseph also writes the weekly guides on our <a href="/blog/">blog</a>, built on the questions Galveston owners ask most.</p>
      <p>Galveston Public Adjuster is a service of <strong><?= FIRM ?></strong> (Texas Department of Insurance public adjuster license <strong>#<?= LICENSE_NO ?></strong>), the firm behind <a href="<?= SISTER_SITE ?>" rel="noopener">TX Public Adjusting</a>, which represents homeowners and businesses across Texas — from hurricanes on the coast to hail and tornadoes inland.</p>
      <p>Every claim is documented with <strong>Matterport 3D imaging</strong> and estimated in <strong>Xactimate</strong>, the same estimating software insurance carriers use, so nothing is overlooked and every line item can be defended.</p>
      <?= phone_link('btn btn-cta btn-lg', icon('phone', 20) . ' Call for an expert consultation') ?>
    </div>
    <div class="grid g2 reveal">
      <div class="card"><div class="badge-ico"><?= icon('shield', 28) ?></div><h3>We work for you</h3><p>Texas law requires our contracts to state "We represent the insured only." We mean it.</p></div>
      <div class="card hot"><div class="badge-ico"><?= icon('dollar', 28) ?></div><h3>No recovery, no fee</h3><p>Nothing up front. Our fee is a percentage of the claim payment, capped by Texas law.</p></div>
      <div class="card"><div class="badge-ico"><?= icon('search', 28) ?></div><h3>We document everything</h3><p>Roof to slab, room by room. Claims are won with evidence.</p></div>
      <div class="card"><div class="badge-ico"><?= icon('check', 28) ?></div><h3>Honest answers</h3><p>If your claim doesn't need a public adjuster, we'll tell you.</p></div>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap narrow">
    <div class="section-head"><span class="kicker">Our commitments</span><h2>What you can expect</h2></div>
    <ul class="checks">
      <li>A licensed Texas public adjuster on your file — not a call center.</li>
      <li>A TDI-approved contract you can rescind in writing within 72 hours of signing.</li>
      <li>Your name on every claim check — we never take control of your money.</li>
      <li>No involvement in repairs: we don't sell roofs, so our estimate has only one purpose — your claim.</li>
      <li>Regular updates until the claim is paid.</li>
    </ul>
    <?= banner('Talk to Joseph about your claim.', 'Call for an expert consultation — free and without obligation.') ?>
  </div>
</section>
