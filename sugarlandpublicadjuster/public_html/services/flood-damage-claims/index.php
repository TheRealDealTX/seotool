<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';

$path = '/services/flood-damage-claims/';
$title = 'Flood Damage Claims';
$desc = 'Sugar Land public adjuster for NFIP and private flood claims. We document building and contents losses, meet deadlines and resolve wind vs. flood disputes.';
$crumbs = [['Home', '/'], ['Services', '/services/'], [$title, $path]];

$faqs = [
    ['Does my homeowners insurance cover flooding in Sugar Land?',
     '<p>No. Standard homeowners policies exclude flood—rising surface water, overflowing rivers and bayous, and storm surge. Flood damage is covered only by a separate policy from the National Flood Insurance Program (NFIP) or a private flood insurer.</p>'],
    ['How long do I have to file an NFIP proof of loss?',
     '<p>Under the standard NFIP policy, a signed and sworn proof of loss is generally due within 60 days of the date of loss. FEMA sometimes extends that deadline after major disasters. Check your policy and any FEMA bulletins for your event, and don’t assume the adjuster’s report counts as your proof of loss.</p>'],
    ['Can I buy flood insurance right before a storm?',
     '<p>NFIP policies usually have a 30-day waiting period before coverage takes effect, with limited exceptions such as policies tied to a new mortgage. Private flood waiting periods vary. Buying when a storm is already in the Gulf is generally too late.</p>'],
    ['My house had both wind and flood damage. Which policy pays?',
     '<p>Both may. Wind damage—roof, windows, wind-driven rain—falls under your homeowners or windstorm policy, while rising-water damage falls under flood insurance. Carriers on each side sometimes blame the other peril. A public adjuster documents the evidence for each so neither claim is shortchanged.</p>'],
];

page_start([
    'title' => 'Flood Damage Claims | Sugar Land Public Adjuster',
    'description' => $desc,
    'path' => $path,
    'breadcrumbs' => $crumbs,
    'schema' => [service_schema('Flood insurance claims', $desc, $path), faq_schema($faqs, $path)],
]);
page_hero('Flood Insurance Claims in Sugar Land, TX',
    'Flood claims run on strict federal rules, tight deadlines and separate building and contents limits. A Sugar Land public adjuster helps you document the loss, meet the proof-of-loss deadline and get paid what the policy allows.',
    $crumbs, 'Claim services');
?>
<div class="container content-layout">
  <article class="prose">
    <p>Sugar Land sits along the Brazos River and is laced with creeks, bayous and drainage channels, including Oyster Creek. Much of the city is protected by levee improvement districts (LIDs) that maintain levees, pump stations and drainage systems—protection that has held through major river crests. Even so, heavy rainfall can overwhelm local drainage, and homes outside the levee system or in low-lying pockets can take on water in a single storm.</p>
    <p>Flood claims work differently from every other claim on this site. Your homeowners policy almost certainly excludes flood, and flood policies—especially those written through the National Flood Insurance Program—have their own rules, forms and deadlines. As a public adjuster in Sugar Land, we help homeowners and business owners navigate those rules and document the claim correctly from the start.</p>

    <h2>Flood insurance basics</h2>
    <p>Flood damage is covered only by a flood policy. Most Texas homeowners who carry one have an NFIP policy, administered by FEMA and often sold through private carriers under the Write Your Own program. A growing number carry private flood policies, whose terms vary widely and may offer higher limits or additional coverages.</p>
    <ul class="checklist">
      <li><strong>Building coverage</strong> pays for the structure: foundation, walls, flooring, electrical and plumbing systems, HVAC, water heaters, built-in appliances and cabinets.</li>
      <li><strong>Contents coverage</strong> is purchased separately and pays for furniture, clothing, electronics and other personal property.</li>
      <li><strong>Waiting periods:</strong> NFIP policies usually take effect 30 days after purchase, with limited exceptions.</li>
      <li><strong>Limits:</strong> NFIP residential building and contents limits are capped by federal rules; excess or private flood coverage can sit above them.</li>
      <li><strong>Valuation:</strong> how contents and certain building items are valued (replacement cost or actual cash value) depends on the policy form and occupancy.</li>
    </ul>
    <p>The NFIP also limits coverage in basements and in enclosed areas below the lowest elevated floor of elevated buildings. Those restrictions matter less for most Sugar Land homes, which are typically built slab-on-grade, but they are important if your property has a below-grade space or an elevated design.</p>

    <div class="callout callout-warn">
      <p><strong>Watch the proof-of-loss deadline.</strong> Under the standard NFIP policy, a signed, sworn proof of loss is generally due within 60 days of the date of loss. FEMA sometimes extends that deadline after a major disaster, but you should confirm the deadline for your policy and event in writing. Missing it can jeopardize payment of amounts you could otherwise recover.</p>
    </div>

    <h2>The Brazos River and Sugar Land flood history</h2>
    <p>The Brazos River has tested Fort Bend County repeatedly. In June 2016, the river crested at 54.74 feet at the Richmond gauge. During Hurricane Harvey in 2017, it reached a record crest of 55.19 feet at the same gauge, prompting evacuations and putting enormous pressure on the levee systems that protect much of Sugar Land. Harvey’s rainfall also flooded homes far from the river through overwhelmed streets, creeks and drainage.</p>
    <p>Our <a href="/sugar-land-storm-history/">Sugar Land storm history</a> page covers these events in more detail, and you can track current river and weather alerts on our <a href="/sugar-land-weather/">live Sugar Land weather</a> page.</p>

    <h2>How flood claims are handled</h2>
    <ol>
      <li><strong>Report the loss</strong> to your flood carrier immediately and get a claim number.</li>
      <li><strong>Document before cleanup:</strong> the waterline in every room, outside high-water marks, and every damaged item.</li>
      <li><strong>Mitigate:</strong> remove standing water, wet drywall, insulation and flooring to prevent mold, and keep samples or photos.</li>
      <li><strong>Inventory contents</strong> with descriptions, ages and replacement prices.</li>
      <li><strong>Review the adjuster’s report</strong> line by line against your own estimate.</li>
      <li><strong>File the proof of loss</strong> on time, with supporting documentation, and request any supplemental payments.</li>
    </ol>

    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Peril</th><th>Usually covered by</th><th>Examples</th></tr>
        </thead>
        <tbody>
          <tr><td>Rising surface water</td><td>Flood policy (NFIP or private)</td><td>River overflow, overwhelmed street drainage, water entering at ground level</td></tr>
          <tr><td>Wind</td><td>Homeowners or windstorm policy</td><td>Missing shingles, broken windows, fallen trees</td></tr>
          <tr><td>Wind-driven rain through storm openings</td><td>Homeowners policy</td><td>Ceiling and wall damage from water entering through a damaged roof</td></tr>
          <tr><td>Plumbing failure</td><td>Homeowners policy</td><td>Burst pipes, appliance leaks—see <a href="/services/water-damage-claims/">water damage claims</a></td></tr>
        </tbody>
      </table>
    </div>

    <h2>Wind vs. flood causation disputes</h2>
    <p>After a hurricane, the same house may have damage from both wind and rising water. That is where disputes start. The homeowners carrier may say interior damage came from floodwater, while the flood carrier may say it came from wind-driven rain. Ceilings, upper walls and attic insulation usually point to roof damage and wind; a consistent waterline around the lower walls points to flood. We document both carefully and coordinate the claims so damage doesn’t fall through the gap. For the wind side, see our <a href="/services/hurricane-wind-damage-claims/">hurricane and wind damage claims</a> page.</p>

    <h2>Common flood claim problems</h2>
    <ul class="checklist x">
      <li>Accepting the adjuster’s estimate without checking room measurements and quantities</li>
      <li>Missing drywall height, insulation, baseboards, cabinets or doors that absorbed water</li>
      <li>Leaving out items like water heaters, HVAC components and electrical work</li>
      <li>Incomplete contents inventories</li>
      <li>Missing the proof-of-loss deadline or filing one without full support</li>
    </ul>
    <p>Most of these problems come down to documentation. Flood adjusters work from measurements and photos, so a clear record of the waterline height in each room, the materials that were wet, and the condition of each damaged item is what supports a complete payment—and any later request for more.</p>

    <h2>Why work with a Sugar Land public adjuster on a flood claim</h2>
    <p>Flood policies are federal contracts with little room for error. A Sugar Land public adjuster understands the forms, the deadlines and the documentation the NFIP expects, and builds an estimate that captures everything the policy covers. We also help coordinate the flood claim with your homeowners claim when wind is involved, and we stay with the claim through supplemental requests.</p>
    <p>Texas law caps public adjuster fees at 10% of the settlement, and there is no upfront cost. If your flood claim has been underpaid or denied, see our <a href="/services/denied-underpaid-claims/">denied and underpaid claims</a> page, or <a href="/contact/">contact us</a> for a free claim review.</p>

    <h2>Flood claim FAQ</h2>
    <?php faq_list($faqs); ?>
  </article>
  <?php sidebar_cta(); ?>
</div>
<?php page_end(); ?>
