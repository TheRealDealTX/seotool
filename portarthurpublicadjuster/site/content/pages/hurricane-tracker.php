<?php
return [
    'template'    => 'hurricane-tracker',
    'title'       => 'Live Hurricane Tracker for Port Arthur, TX',
    'seo_title'   => 'Port Arthur Hurricane Tracker | Live NHC Storm Map',
    'description' => 'Track active hurricanes and tropical storms with live National Hurricane Center data, distance from Port Arthur, NWS alerts, and a storm-season checklist.',
    'lead'        => 'Active Atlantic storms, their distance from Port Arthur, and any tropical watches or warnings for Jefferson County, pulled live from the National Hurricane Center and the National Weather Service.',
    'kicker'      => 'Weather Tools',
    'image'       => '/assets/img/featured/page-hurricane-tracker.webp',
    'image_alt'   => 'Radar image of a tropical storm approaching the Texas coast',
    'hide_hero_cta' => true,
    'faqs' => [
        ['q' => 'Where does the hurricane tracker data come from?', 'a' => '<p>Storm positions, intensity, and advisory links come from the National Hurricane Center\'s public <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">CurrentStorms feed</a>. Watches and warnings for Port Arthur come from the National Weather Service alert service. The page refreshes the data about every 15 minutes.</p>'],
        ['q' => 'Is this tracker an official forecast?', 'a' => '<p>No. It shows the latest official center positions so you can see how far a system is from Port Arthur. For forecasts, cones, and evacuation decisions, always use the National Hurricane Center, NWS Lake Charles, and Jefferson County emergency management.</p>'],
        ['q' => 'When should I review my insurance before a hurricane?', 'a' => '<p>Before a storm is in the Gulf. Many insurers stop writing or changing coverage once a storm is close (a "binding restriction"), and a new National Flood Insurance Program policy generally has a 30-day waiting period. Review your homeowners, TWIA windstorm, and flood policies at the start of the season.</p>'],
        ['q' => 'What should I do with my insurance after a hurricane passes?', 'a' => '<p>Stay safe first. Then photograph damage before cleanup, make temporary repairs to prevent more damage and keep receipts, report the claim to every insurer that may apply (homeowners, TWIA, flood), and write down claim numbers and adjuster names. Our <a href="/claim-documentation-checklist/">documentation checklist</a> walks through each step, and a <a href="/free-claim-review/">Free Claim Review</a> can help you sort out which policy covers what.</p>'],
    ],
    'body' => <<<'HTML'
<h2>Why Port Arthur watches the tropics closely</h2>
<p>Port Arthur sits on the upper Texas coast between Sabine Lake and the Gulf, and Jefferson County has felt nearly every kind of tropical impact: Hurricane Rita's winds in 2005, Hurricane Ike's 14&ndash;15 foot storm surge at Sabine Pass in 2008, Hurricane Harvey's record-setting rain in 2017, Tropical Storm Imelda's flooding in 2019, and Hurricanes Laura and Delta in 2020. The NOAA records behind those events are on our <a href="/storm-history/">storm history</a> page.</p>
<p>A tropical system does not need to make landfall here to cause damage. Wind-driven rain, tornadoes in outer rain bands, and days of heavy rainfall can damage homes and businesses well away from the center. That is why this tracker shows distance from Port Arthur alongside each storm.</p>

<h2>How to read the tracker</h2>
<ul>
  <li><strong>Storm cards</strong> list each active system's category, maximum sustained winds, central pressure, movement, and straight-line distance from Port Arthur, with links to the official NHC advisory and cone graphics.</li>
  <li><strong>The map</strong> marks the latest center positions and rings at 200, 400, and 800 miles from Port Arthur. It does not show the forecast track or cone&mdash;open the NHC graphics for that.</li>
  <li><strong>Tropical alerts</strong> show any hurricane, tropical storm, or storm surge watches and warnings the National Weather Service has issued for the Port Arthur area.</li>
</ul>

<h2>Insurance steps to take before a storm</h2>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Policy</th><th scope="col">What to check</th></tr></thead>
<tbody>
<tr><td>Homeowners or commercial property</td><td>Whether wind and hail are covered or excluded, the wind/hail or named-storm deductible, and additional living expense limits.</td></tr>
<tr><td>TWIA windstorm (if wind is excluded)</td><td>Dwelling and contents limits, the deductible percentage, and whether recent repairs have a TDI WPI-8 certificate.</td></tr>
<tr><td>Flood (NFIP or private)</td><td>Building and contents limits, deductibles, and the 30-day waiting period for new NFIP policies.</td></tr>
</tbody></table></div>
<p>Turn your percentage deductible into dollars with our <a href="/hurricane-deductible-calculator/">hurricane deductible calculator</a>, and take date-stamped photos of your home and belongings now so you have a "before" record. If a storm does damage your property, a Port Arthur Public Adjuster can help you document the loss and work through each claim; see our <a href="/services/hurricane-damage-claims/">hurricane damage claims</a> and <a href="/services/twia-windstorm-claims/">TWIA windstorm claims</a> pages.</p>
HTML,
];
