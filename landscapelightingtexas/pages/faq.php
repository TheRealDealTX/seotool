<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Landscape Lighting FAQ';
$P['lead'] = 'Straight answers to the questions Texas homeowners ask us most, from cost and LED efficiency to installation day, HOAs and warranties. Can’t find yours? Call <a href="' . PHONE_HREF . '">' . PHONE . '</a> or <a href="/quote/">send us a note</a>.';
?>
<section class="section">
  <div class="container narrow">
    <p class="lead-p reveal">Landscape Lighting Texas has answered these questions on more than 1,400 projects across the state. The answers below are general guidance; every property is different, which is why our consultations and estimates are always free.</p>
    <ul class="pill-list reveal">
      <li><a href="#cost">Cost &amp; quotes</a></li>
      <li><a href="#design">Design</a></li>
      <li><a href="#installation">Installation</a></li>
      <li><a href="#led">LED &amp; energy</a></li>
      <li><a href="#smart">Smart controls</a></li>
      <li><a href="#maintenance">Maintenance &amp; warranty</a></li>
      <li><a href="#area">Service area &amp; HOA</a></li>
    </ul>
  </div>
</section>

<div id="cost"></div>
<?php faqs([
    ['How much does landscape lighting cost in Texas?', '<p>Most residential landscape lighting projects in Texas range from <strong>$2,500 to $12,000</strong>, depending on property size, the number of fixtures and how complex the installation is. A starter package for a typical home runs $2,500–$5,000, while comprehensive estate lighting can exceed $20,000.</p><p>These are planning ranges. We provide a detailed, itemized quote with zero obligation, so you know exactly what you are getting before you decide. For a ballpark of your own, try the <a href="/landscape-lighting-cost-calculator/">landscape lighting cost calculator</a>.</p>'],
    ['How much does each landscape light cost installed?', '<p>Professionally installed, most fixtures land around <strong>$250–$450 each</strong>. That figure covers the fixture and lamp, its share of the transformer and cable, connections, labor and on-site aiming. Architectural-grade brass fixtures, in-grade well lights and pool or water-feature lights sit at the higher end; simple path lights in open beds sit at the lower end.</p>'],
    ['Is the estimate really free?', '<p>Yes. Consultations and estimates are free and carry no obligation. Your quote is itemized by fixture type, transformer, wiring, controls and labor, so you can see where the money goes and adjust the scope if you want to phase the project.</p>'],
    ['Can I install my lighting in phases?', '<p>Absolutely, and many clients do. A common plan starts with the front facade, entry and walkway, then adds trees, the backyard or the pool later. We size the first transformer with spare capacity and plan cable routes so later phases connect cleanly.</p>'],
], 'Cost & Quotes', 'Pricing'); ?>

<div id="design"></div>
<?php faqs([
    ['How many lights does my property need?', '<p>It depends on what you want to feature, not the square footage. A front elevation with an entry, two or three trees and a walkway often needs 12 to 20 fixtures; a full property with backyard and pool can need 30 or more. Good design is about strategic placement: lighting focal points and leaving some areas softly dark creates depth.</p>'],
    ['What color temperature is best for landscape lighting?', '<p>For most Texas homes, warm white between <strong>2700K and 3000K</strong>. 2700K flatters brick, cedar and warm limestone; 3000K keeps foliage looking natural and suits cooler stone. We keep the whole system consistent so nothing looks mismatched. Compare them yourself in the <a href="/tools/color-temperature-visualizer/">color temperature visualizer</a>.</p>'],
    ['What is the difference between uplighting, downlighting and moonlighting?', '<p><strong>Uplighting</strong> places fixtures at ground level aimed up at a facade, column or tree for drama. <strong>Downlighting</strong> mounts fixtures above, on eaves, pergolas or trees, for soft, natural light on patios and paths. <strong>Moonlighting</strong> is downlighting from high in a tree canopy, so branches cast dappled shadows on the ground below, a beautiful fit for mature live oaks. See our <a href="/landscape-lighting-complete-guide/">complete guide</a> for more techniques.</p>'],
    ['Will my lighting bother the neighbors?', '<p>It shouldn’t. We use shielded fixtures, glare guards and careful aiming so you see the lit surface, not the bulb. We follow dark-sky practice: no light aimed off the property or into the sky, and warm color temperatures that are easier on the eyes.</p>'],
], 'Design', 'Planning'); ?>

<div id="installation"></div>
<?php faqs([
    ['How long does installation take?', '<p>Most residential installations are completed in <strong>one day</strong>. Larger estate projects or commercial properties may take two to three days. We schedule around your convenience and make sure everything is working, and aimed, by nightfall on the final day.</p>'],
    ['Will installation damage my lawn or landscaping?', '<p>We take exceptional care of your property. Low-voltage cable is buried with narrow-blade trenching tools that barely disturb turf, and we hand-dig around roots, irrigation lines and existing plantings. Any turf we disturb is restored, and we leave the property clean.</p>'],
    ['Is low-voltage landscape lighting safe?', '<p>Yes. A low-voltage system runs at about 12 volts after the transformer, which is far safer around people, pets and irrigation than line voltage. The transformer plugs into a weatherproof GFCI outlet, and our connections are sealed against moisture.</p>'],
    ['How deep is the wire buried, and what gauge do you use?', '<p>Low-voltage cable is typically buried about 6 inches deep in beds and turf. We use 12-gauge or 10-gauge direct-burial cable, depending on the load and distance, and lay it out in a hub pattern to control voltage drop so the last fixture is as bright as the first. Run the numbers with the <a href="/tools/transformer-calculator/">transformer and voltage drop calculator</a>.</p>'],
], 'Installation', 'Install Day'); ?>

<div id="led"></div>
<?php faqs([
    ['Are LED landscape lights energy efficient?', '<p>Very. Modern LED landscape lighting uses <strong>75–80% less energy</strong> than traditional halogen systems. A typical whole-property system running about six hours a night costs roughly <strong>$10–$25 per month</strong> to operate. Homeowners replacing an older halogen system often recover the cost difference in energy savings within a few years. Check your own numbers with the <a href="/tools/energy-savings-calculator/">LED energy savings calculator</a>.</p>'],
    ['How long do LED landscape lights last?', '<p>Quality integrated LEDs and LED lamps are rated for tens of thousands of hours, which works out to many years of nightly use. In practice, the fixture body, seals and connections determine lifespan, which is why we install solid brass and copper fixtures that stand up to Texas heat, humidity and hail.</p>'],
    ['Can you convert my old halogen system to LED?', '<p>Usually, yes. Depending on the condition of the fixtures, transformer and wiring, we can swap in LED lamps, replace failing fixtures, or rebuild the system. Retrofits often allow a smaller load on the transformer and a noticeable drop in your electric bill. Learn more on our <a href="/services/landscape-lighting-maintenance/">maintenance and repair</a> page.</p>'],
], 'LED & Energy', 'Efficiency'); ?>

<div id="smart"></div>
<?php faqs([
    ['Can I control my landscape lighting from my phone?', '<p>Yes. Our <a href="/services/smart-lighting-systems/">smart lighting systems</a> let you switch zones, dim, set scenes and change schedules from an app, and many integrate with popular smart-home platforms and voice assistants.</p>'],
    ['What is an astronomical timer?', '<p>An astronomical timer calculates sunset and sunrise for your location every day, so your lights turn on at dusk all year without adjusting for seasons or daylight saving time. Many clients run lights from dusk to around midnight, with entry or security zones staying on later. See dusk times for your city with the <a href="/tools/dusk-timer/">Texas dusk timer</a>.</p>'],
    ['Can different areas run on different schedules?', '<p>Yes. We divide the system into zones, such as front facade, trees, backyard and pool, so each can have its own schedule and brightness. That saves energy and gives you scenes for entertaining, everyday evenings and late-night security.</p>'],
], 'Smart Controls', 'Controls'); ?>

<div id="maintenance"></div>
<?php faqs([
    ['What warranty do you offer?', '<p>Every installation is backed by our <strong>5-year workmanship warranty</strong>. Fixtures also carry their manufacturers’ warranties, which vary by product and are often several years or longer. If something fails because of how it was installed, we fix it at no charge.</p>'],
    ['Does landscape lighting need maintenance?', '<p>A little. Plants grow, mulch shifts and lenses collect dust, pollen and hard-water spots from sprinklers. An annual tune-up covers cleaning, re-aiming, trimming back growth, checking connections and voltage, and resetting timers. Our <a href="/landscape-lighting-maintenance-checklist/">maintenance checklist</a> walks through each Texas season.</p>'],
    ['Can I add to or change my system later?', '<p>Yes. We design every system with expansion in mind. Low-voltage lighting is flexible, so it is easy to add fixtures, upgrade to smart controls, or adapt the lighting as your landscaping matures. Many clients add to their system once they see the results.</p>'],
    ['Do you repair systems another company installed?', '<p>Yes. We troubleshoot and repair most brands of low-voltage landscape lighting, including dead zones, dim fixtures, failed transformers, cut cables and corroded connections, and we can upgrade older systems to LED.</p>'],
], 'Maintenance & Warranty', 'Ownership'); ?>

<div id="area"></div>
<?php faqs([
    ['Which areas of Texas do you serve?', '<p>We work statewide, including <a href="/areas/austin/">Austin</a>, <a href="/areas/houston/">Houston</a>, <a href="/areas/dallas-fort-worth/">Dallas–Fort Worth</a>, <a href="/areas/san-antonio/">San Antonio</a>, <a href="/areas/west-texas/">West Texas</a> and the <a href="/areas/gulf-coast/">Gulf Coast</a>. If your town isn’t listed, ask; we likely serve it.</p>'],
    ['Do I need HOA approval for landscape lighting?', '<p>Many Texas HOAs require approval for exterior changes, and some set rules on fixture types, brightness or light trespass. We can provide a fixture list, product sheets and a layout to include with your application, and we design to dark-sky standards that most associations welcome.</p>'],
    ['Do you light commercial properties?', '<p>Yes. Alongside homes, we design and install lighting for commercial facades, entries, signage and grounds, including <a href="/services/security-lighting/">security and floodlighting</a> that improves visibility without harsh glare.</p>'],
], 'Service Area & HOA', 'Where We Work'); ?>

<section class="section alt">
  <div class="container">
    <?php section_head('Free Tools', 'Plan Your Lighting Before We Meet', 'Estimate costs, size a transformer or preview color temperatures with the same calculators our designers use.'); ?>
    <?php tool_cards(); ?>
  </div>
</section>

<?php cta_band('Still Have Questions?', 'Talk with a Landscape Lighting Texas designer. We will answer your questions, walk your property at dusk and send a clear, itemized quote, free.'); ?>
