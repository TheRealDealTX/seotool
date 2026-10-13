<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['About Us', '/about-us/']];
page_start([
    'title' => 'About Houston Public Adjusters | Licensed Public Insurance Adjusters',
    'desc' => 'Houston Public Adjusters are licensed public insurance adjusters who represent policyholders, not insurance companies. Meet Joseph Dittman and learn how we work.',
    'path' => '/about-us/',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'AboutPage', 'name' => 'About Houston Public Adjusters', 'url' => SITE_URL . '/about-us/', 'mainEntity' => ['@id' => SITE_URL . '/#business']]],
]);
echo page_hero('About Houston Public Adjusters', 'Insurance claims are supposed to bring relief after property damage. In reality, they often create frustration, delays and confusion &mdash; especially for Houston property owners facing complex policies and aggressive insurance tactics. That&rsquo;s where we come in.', $crumbs, 'Houston public insurance adjusters');
?>
<div class="wrap layout-sidebar">
  <div class="prose">
    <p>We are a team of licensed public adjusters dedicated to representing <strong>policyholders, not insurance companies</strong>. Our role is simple but powerful: we help homeowners and business owners throughout Houston document their losses accurately, challenge unfair claim decisions and pursue the full settlement their insurance policies allow.</p>
    <p>When disaster strikes, insurance companies already have experts working for them. We believe you deserve the same level of representation. Houston Public Adjusters is operated by <?= LEGAL_NAME ?>, Texas public adjuster license #<?= LICENSE_NO ?>, and works alongside our statewide sister firm, <a href="https://txpublicadjusting.com/" target="_blank" rel="noopener">TX Public Adjusting</a>.</p>

    <h2>Who We Serve</h2>
    <p>Houston is a diverse city with equally diverse property risks. From sudden storms to long-term water damage, no two claims are ever the same. We work with a wide range of clients, including:</p>
    <ul class="checklist">
      <li>Homeowners dealing with storm, fire, water or structural damage</li>
      <li>Business owners facing interrupted operations and property losses</li>
      <li>Property managers handling multi-unit or commercial claims</li>
      <li>Landlords navigating complex coverage and tenant-related issues</li>
    </ul>
    <p>Whether your claim is residential or commercial, small or large, we approach every case with the same focus: accuracy, persistence and accountability.</p>

    <h2>What Makes Public Adjusters Different</h2>
    <p>Most people only interact with insurance adjusters after a loss &mdash; but those adjusters work for the insurance company, not for you. A public adjuster changes the balance.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Insurance Company Adjuster</th><th>Public Adjuster (Us)</th></tr></thead>
      <tbody>
        <tr><td>Represents the insurer</td><td>Represents the policyholder</td></tr>
        <tr><td>Focuses on cost control</td><td>Focuses on fair compensation</td></tr>
        <tr><td>Manages multiple claims</td><td>Focuses on your claim</td></tr>
        <tr><td>Interprets policy conservatively</td><td>Interprets policy to your benefit</td></tr>
      </tbody>
    </table></div>
    <p>We step in to manage the technical, time-consuming and often overwhelming parts of the claim so you don&rsquo;t have to.</p>

    <h2>Meet Joseph Dittman</h2>
    <div class="author-box" style="margin-top:0">
      <img src="<?= AUTHOR['photo'] ?>" alt="Joseph Dittman, licensed Texas public adjuster" width="96" height="96" loading="lazy">
      <div><p class="author-name"><a href="<?= AUTHOR['url'] ?>">Joseph Dittman</a> &middot; <?= AUTHOR['title'] ?></p>
      <p>Joseph is the licensed public adjuster behind Houston Public Adjusters and TX Public Adjusting. He documents losses with Matterport 3D imaging, builds estimates in Xactimate and Symbility &mdash; the same platforms insurers use &mdash; and negotiates directly with carriers on behalf of Texas homeowners and businesses. Joseph also writes the claim guides on our <a href="/blog/">blog</a>.</p></div>
    </div>

    <h2>Our Approach</h2>
    <p>At Houston Public Adjusters, we don&rsquo;t believe in shortcuts or cookie-cutter claims. Every property, policy and loss scenario deserves a tailored strategy. Our process typically includes:</p>
    <ul class="checklist">
      <li>Comprehensive damage inspection to identify visible and hidden losses</li>
      <li>Detailed documentation including photos, measurements, moisture mapping and 3D scans</li>
      <li>Policy analysis to uncover all applicable coverages</li>
      <li>Claim preparation and submission with accurate Xactimate valuations</li>
      <li>Direct negotiation with the insurance company on your behalf</li>
      <li>Ongoing follow-up until the claim is resolved</li>
    </ul>
    <p>We stay involved from start to finish. No handoffs. No guesswork. And no disappearing once paperwork is filed.</p>

    <h2>Why Houston Property Owners Choose Us</h2>
    <p>Houston presents unique insurance challenges: severe weather patterns, flood-prone areas, aging infrastructure and high claim volumes after major events like <a href="/houston-storm-history/">Harvey, Uri and Beryl</a>. Experience matters here. Clients choose us because we offer:</p>
    <ul class="checklist">
      <li>Local expertise with Houston-area claims and insurers</li>
      <li>Licensed public adjusters who understand Texas regulations</li>
      <li>Clear communication without jargon or runarounds</li>
      <li>No upfront fees &mdash; we only get paid if we recover for you</li>
      <li>Relentless advocacy when claims stall, delay or underpay</li>
    </ul>
    <p>We don&rsquo;t promise miracles. We promise diligence, transparency and effort &mdash; every step of the way.</p>

    <h2>Transparency You Can Trust</h2>
    <p>One of the biggest frustrations policyholders face is not knowing where their claim stands. We make communication a priority. What you can expect from us:</p>
    <ul class="checklist">
      <li>Honest assessments of claim strengths and limitations</li>
      <li>Regular updates throughout the process</li>
      <li>Clear explanations of timelines and next steps</li>
      <li>Straight answers &mdash; even when they&rsquo;re not what you want to hear</li>
    </ul>
    <p>Our goal isn&rsquo;t just a better settlement. It&rsquo;s peace of mind during a stressful time.</p>

    <h2>Ethics and Advocacy</h2>
    <p>We take our responsibility seriously. As licensed public adjusters, we are bound by the Texas Insurance Code and professional ethical standards that require us to act in your best interest.</p>
    <div class="two-col" style="gap:20px">
      <div><h3>We never:</h3><ul class="checklist xlist"><li>Inflate damages</li><li>Misrepresent facts</li><li>Pressure clients into unrealistic expectations</li></ul></div>
      <div><h3>We do:</h3><ul class="checklist"><li>Defend legitimate claims</li><li>Push back against unfair denials</li><li>Hold insurance companies accountable to their policies</li></ul></div>
    </div>
    <p>Your claim is your financial recovery. We treat it that way.</p>

    <h2>When Should You Call a Public Adjuster?</h2>
    <p>Many clients reach out too late &mdash; after mistakes have already limited their claim. Others call early and avoid costly missteps altogether. You should consider contacting us if:</p>
    <ul class="checklist">
      <li>Your claim was denied or underpaid</li>
      <li>The insurance process feels overwhelming</li>
      <li>You&rsquo;re asked to provide extensive documentation</li>
      <li>The insurer keeps delaying or changing adjusters</li>
      <li>You want an expert review before accepting a settlement</li>
    </ul>
    <p>Early involvement often leads to stronger outcomes &mdash; but help is available at nearly any stage of the claim.</p>

    <h2>Our Commitment to Houston</h2>
    <p>Houston isn&rsquo;t just our service area &mdash; it&rsquo;s our community. We understand the stress that property damage causes because we&rsquo;ve seen it firsthand, again and again. Our commitment is simple: advocate fiercely, communicate clearly, act ethically and deliver measurable value.</p>
    <p>When you work with Houston Public Adjusters, you&rsquo;re not hiring a call center or a volume-based operation. You&rsquo;re partnering with professionals who take your loss personally.</p>

    <h2>Let&rsquo;s Talk About Your Claim</h2>
    <p>Every claim starts with a conversation. If you&rsquo;re unsure whether you need a public adjuster &mdash; or whether your claim is being handled fairly &mdash; we invite you to reach out. A consultation costs nothing. The insight can change everything.</p>
  </div>
  <aside class="sidebar">
    <div class="side-card sticky"><?= lead_form('lead-about', 'Free Claim Review', 'Houston Public Adjusters is here to protect your claim, your property and your peace of mind.', true) ?></div>
  </aside>
</div>
<?php
page_end();
