<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';

$path = '/about-us/';
$crumbs = [['Home', '/'], ['About Us', $path]];
page_start([
    'title' => 'About Us | Sugar Land Public Adjuster | +1 (832) 503-5866',
    'description' => 'Sugar Land Public Adjuster is a team of licensed public adjusters dedicated to representing policyholders, not insurance companies. Meet Joseph Dittman.',
    'path' => $path,
    'page_type' => 'AboutPage',
    'breadcrumbs' => $crumbs,
]);
page_hero('About Us', 'Licensed public adjusters who represent Sugar Land policyholders—not insurance companies.', $crumbs, 'Sugar Land Public Adjuster');
?>
<section class="section">
  <div class="container split split-60">
    <div class="prose">
      <p>Insurance claims are supposed to bring relief after property damage. In reality, they often create frustration, delays, and confusion—especially for Sugar Land property owners facing complex policies and aggressive insurance tactics. That’s where Sugar Land Public Adjuster comes in.</p>
      <p>We are a team of licensed public adjusters dedicated to representing <strong>policyholders</strong>, not insurance companies. Our role is simple but powerful: we help homeowners and business owners throughout Sugar Land document their losses accurately, challenge unfair claim decisions, and pursue the full settlement their insurance policies allow.</p>
      <p>When disaster strikes, insurance companies already have experts working for them. We believe you deserve the same level of representation.</p>
    </div>
    <div class="card">
      <h2 class="h3">At a glance</h2>
      <ul class="checklist purple">
        <li>Licensed Texas public adjusters</li>
        <li>Firm: <?= e(SITE['firm']) ?>, license #<?= e(SITE['firm_license']) ?></li>
        <li>Residential &amp; commercial claims</li>
        <li>No upfront fees—paid only from what we recover</li>
        <li>Serving Sugar Land &amp; all of Fort Bend County</li>
      </ul>
      <a class="btn btn-primary btn-block" href="tel:<?= SITE['phone_href'] ?>">Call <?= e(SITE['phone_display']) ?></a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="team-card">
      <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman, licensed Texas public adjuster" width="240" height="240" loading="lazy">
      <div>
        <p class="eyebrow">Your public adjuster</p>
        <h2>Joseph Dittman</h2>
        <p><?= e(AUTHOR['short']) ?></p>
        <p>Joseph’s team documents every loss with photos, measurements and tools like Matterport 3D imaging, then builds estimates in Xactimate and Symbility—the same estimating platforms insurers use—so every line item can be defended. He is the author of every article on the <a href="/blog/">Sugar Land Public Adjuster blog</a>.</p>
        <div class="btn-row"><a class="btn btn-primary" href="<?= e(AUTHOR['url']) ?>">Read Joseph’s full profile</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container content-layout" style="padding:0">
    <div class="prose">
      <h2>Who We Serve</h2>
      <p>Sugar Land is a diverse city with equally diverse property risks. From sudden storms to long-term water damage, no two claims are ever the same. We work with a wide range of clients, including:</p>
      <ul class="checklist">
        <li>Homeowners dealing with storm, fire, water, or structural damage</li>
        <li>Business owners facing interrupted operations and property losses</li>
        <li>Property managers handling multi-unit or commercial claims</li>
        <li>Landlords navigating complex coverage and tenant-related issues</li>
      </ul>
      <p>Whether your claim is residential or commercial, small or large, we approach every case with the same focus: accuracy, persistence, and accountability.</p>

      <h2>What Makes Public Adjusters Different</h2>
      <p>Most people only interact with insurance adjusters after a loss—but those adjusters work for the insurance company, not for you. A public adjuster changes the balance.</p>
      <div class="table-wrap"><table>
        <thead><tr><th></th><th>Insurance company adjuster</th><th>Public adjuster</th></tr></thead>
        <tbody>
          <tr><th>Works for</th><td>The insurance company</td><td>You, the policyholder</td></tr>
          <tr><th>Paid by</th><td>The insurer (salary or per-claim fee)</td><td>A percentage of your settlement—capped at 10% in Texas</td></tr>
          <tr><th>Goal</th><td>Close the claim efficiently within company guidelines</td><td>Document and recover everything your policy covers</td></tr>
          <tr><th>Time on your claim</th><td>Often one of dozens of open files</td><td>Dedicated to your claim from start to finish</td></tr>
        </tbody>
      </table></div>

      <h3>Our Role in the Claims Process</h3>
      <p>We step in to manage the technical, time-consuming, and often overwhelming parts of the claim so you don’t have to.</p>

      <h2>Our Approach</h2>
      <p>At Sugar Land Public Adjuster, we don’t believe in shortcuts or cookie-cutter claims. Every property, policy, and loss scenario deserves a tailored strategy.</p>
      <h3>Our process typically includes:</h3>
      <ul class="checklist purple">
        <li>Comprehensive damage inspection to identify visible and hidden losses</li>
        <li>Detailed documentation including photos, measurements, and reports</li>
        <li>Policy analysis to uncover all applicable coverages</li>
        <li>Claim preparation and submission with accurate valuations</li>
        <li>Direct negotiation with the insurance company on your behalf</li>
        <li>Ongoing follow-up until the claim is resolved</li>
      </ul>
      <p>We stay involved from start to finish. No handoffs. No guesswork. And no disappearing once paperwork is filed.</p>

      <h2>Why Sugar Land Property Owners Choose Us</h2>
      <p>Sugar Land presents unique insurance challenges: severe weather patterns, flood-prone areas, aging infrastructure, and high claim volumes after major events. Experience matters here.</p>
      <p>Clients choose us because we offer:</p>
      <ul class="checklist">
        <li>Local expertise with Sugar Land-area claims and insurers</li>
        <li>Licensed public adjusters who understand Texas regulations</li>
        <li>Clear communication without jargon or runarounds</li>
        <li>No upfront fees — we only get paid if we recover for you</li>
        <li>Relentless advocacy when claims stall, delay, or underpay</li>
      </ul>
      <p>We don’t promise miracles. We promise diligence, transparency, and effort—every step of the way.</p>

      <h2>Transparency You Can Trust</h2>
      <p>One of the biggest frustrations policyholders face is not knowing where their claim stands. We make communication a priority.</p>
      <h3>What you can expect from us:</h3>
      <ul>
        <li>Honest assessments of claim strengths and limitations</li>
        <li>Regular updates throughout the process</li>
        <li>Clear explanations of timelines and next steps</li>
        <li>Straight answers—even when they’re not what you want to hear</li>
      </ul>
      <p>Our goal isn’t just a better settlement. It’s peace of mind during a stressful time.</p>

      <h2>Ethics and Advocacy</h2>
      <p>We take our responsibility seriously. As public adjusters, we are bound by professional and ethical standards that require us to act in your best interest.</p>
      <div class="grid-2">
        <div class="card"><h3>We never:</h3><ul class="checklist x"><li>Inflate damages</li><li>Misrepresent facts</li><li>Pressure clients into unrealistic expectations</li></ul></div>
        <div class="card"><h3>We do:</h3><ul class="checklist"><li>Defend legitimate claims</li><li>Push back against unfair denials</li><li>Hold insurance companies accountable to their policies</li></ul></div>
      </div>
      <p class="mt-2">Your claim is your financial recovery. We treat it that way.</p>

      <h2>When Should You Call a Public Adjuster?</h2>
      <p>Many clients reach out too late—after mistakes have already limited their claim. Others call early and avoid costly missteps altogether.</p>
      <p>You should consider contacting us if:</p>
      <ul class="checklist purple">
        <li>Your claim was denied or underpaid</li>
        <li>The insurance process feels overwhelming</li>
        <li>You’re asked to provide extensive documentation</li>
        <li>The insurer keeps delaying or changing adjusters</li>
        <li>You want an expert review before accepting a settlement</li>
      </ul>
      <p>Early involvement often leads to stronger outcomes—but help is available at nearly any stage of the claim.</p>

      <h2>Our Commitment to Sugar Land</h2>
      <p>Sugar Land isn’t just our service area—it’s our community. We understand the stress that property damage causes because we’ve seen it firsthand, again and again.</p>
      <p>Our commitment is simple:</p>
      <ul class="checklist">
        <li>Advocate fiercely</li>
        <li>Communicate clearly</li>
        <li>Act ethically</li>
        <li>Deliver measurable value</li>
      </ul>
      <p>When you work with Sugar Land Public Adjuster, you’re not hiring a call center or a volume-based operation. You’re partnering with professionals who take your loss personally.</p>

      <h2>Let’s Talk About Your Claim</h2>
      <p>Every claim starts with a conversation. If you’re unsure whether you need a public adjuster—or whether your claim is being handled fairly—we invite you to reach out.</p>
      <p>A consultation costs nothing. The insight can change everything.</p>
      <p><strong>Sugar Land Public Adjuster is here to protect your claim, your property, and your peace of mind.</strong></p>
    </div>
    <?php sidebar_cta(); ?>
  </div>
</section>
<?php page_end(); ?>
