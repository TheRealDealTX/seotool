<?php
return [
    'title'       => 'Free Insurance Claim Tools for San Marcos Property Owners',
    'seo_title'   => 'Free Insurance Claim Tools | San Marcos & Hays County',
    'description' => 'Free insurance claim tools for San Marcos and Hays County: settlement calculator, documentation checklist, storm lookup, live weather, and NOAA storm history.',
    'lead'        => 'Free, no-sign-up tools that help San Marcos and Hays County homeowners and business owners check the weather record, organize evidence, and understand the numbers on a property insurance claim.',
    'kicker'      => 'Resources',
    'image'       => '/assets/img/featured/page-claim-tools.webp',
    'image_alt'   => 'Laptop with insurance claim tools and a storm map of the San Marcos area',
    'wide'        => true,
    'faqs' => [
        ['q' => 'Do I have to create an account to use these claim tools?', 'a' => '<p>No. Every tool on this page is free and open to anyone. The calculator and the documentation checklist work entirely inside your browser, so the numbers and notes you type are not sent to us.</p>'],
        ['q' => 'Will these tools tell me whether my damage is covered?', 'a' => '<p>No tool can make a coverage decision. They help you find weather records, keep evidence organized, and follow the math an insurer uses. Whether a loss is covered depends on your policy wording and the facts. If you want a licensed professional to look at your situation, request a <a href="/free-claim-review/">Free Claim Review</a>.</p>'],
        ['q' => 'Where does the weather and storm information come from?', 'a' => '<p>Current conditions come from the National Weather Service observation station at San Marcos Regional Airport (KHYI). Forecasts, alerts, and preliminary storm reports come from the NWS Austin/San Antonio office in New Braunfels. The historical record comes from the NOAA NCEI Storm Events Database for Hays County. Each tool links back to its source.</p>'],
        ['q' => 'I live in Lockhart, Seguin, or New Braunfels. Are the storm tools useful for me?', 'a' => '<p>Partly. The storm history on this site covers Hays County, so you will see Hays County reports that fall inside your search radius, but events logged only in Caldwell, Guadalupe, or Comal County are not included. For those, search the <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA Storm Events Database</a> by county.</p>'],
    ],
    'body' => <<<'HTML'
<p>A property insurance claim usually turns on three questions: what happened, what it damaged, and what the repair is worth. These free insurance claim tools help San Marcos and Hays County property owners answer each one with something more solid than memory. They were built for the kinds of losses this part of Central Texas actually sees, from spring hail along the I-35 corridor to flash flooding near the Blanco and San Marcos Rivers and the occasional hard freeze.</p>

[[tools-grid]]

<h2>Which claim tool fits your situation</h2>
<table>
<thead><tr><th>If you need to…</th><th>Start with</th><th>What you get</th></tr></thead>
<tbody>
<tr><td>Confirm a hail or wind storm on your date of loss</td><td><a href="/storm-lookup/">Storm event lookup</a></td><td>NOAA and NWS reports within a set distance of your city or ZIP code</td></tr>
<tr><td>See what was reported in the last few days or weeks</td><td><a href="/weather-events/">Recent weather events</a></td><td>Preliminary NWS Local Storm Reports for Hays County, updated automatically</td></tr>
<tr><td>Research older storms or a whole hail season</td><td><a href="/storm-history/">Storm history</a></td><td>The searchable NOAA record for Hays County back to the 1950s</td></tr>
<tr><td>Keep an eye on an incoming storm</td><td><a href="/weather/">Live San Marcos weather</a></td><td>Current conditions at KHYI, the 7-day forecast, and active alerts</td></tr>
<tr><td>Gather the right photos and paperwork</td><td><a href="/claim-documentation-checklist/">Documentation checklist</a></td><td>A printable checklist by damage type with progress tracking</td></tr>
<tr><td>Understand an insurer’s estimate or first check</td><td><a href="/claim-calculator/">Settlement calculator</a></td><td>RCV, depreciation, deductible, and out-of-pocket math in plain numbers</td></tr>
<tr><td>Find out what the repair must include under local code</td><td><a href="/local-building-codes/">San Marcos building codes</a></td><td>Adopted codes, the local reroof-permit rule, and Permit Center contacts</td></tr>
</tbody>
</table>

<h2>A practical order for using the tools after a storm</h2>
<ol>
<li><strong>Pin down the date.</strong> Check the recent weather events page in the first days after a storm. If the storm was months ago, use the storm lookup or storm history instead. Save a copy of any report that matches your date and area.</li>
<li><strong>Document before anything changes.</strong> Open the checklist for your type of loss and work through it before tarping, cleanup, or tear-out covers the evidence. Keep receipts for emergency work.</li>
<li><strong>Read the estimate with the calculator open.</strong> When the insurer’s estimate arrives, enter its replacement cost, depreciation, and deductible. Seeing the actual cash value payment and the recoverable depreciation separately clears up a lot of confusion about why the first check is smaller than the repair bid.</li>
<li><strong>Check local code items.</strong> If repairs will need a permit or code upgrades, compare what the City of San Marcos (or your own city) requires with what the estimate includes.</li>
</ol>

<h2>What the tools cannot do</h2>
<p>A storm report near your house shows that weather was observed nearby; it does not prove your roof was hit, and a missing report does not prove it was not. The calculator follows standard settlement math but cannot read your specific endorsements or sublimits. The checklist is a guide, not a list of everything an insurer may ask for. Use the tools as a starting point and rely on a physical inspection and your actual policy for the answers that matter.</p>
<p>If your claim has been <a href="/services/denied-insurance-claims/">denied</a>, <a href="/services/underpaid-insurance-claims/">underpaid</a>, or <a href="/services/delayed-insurance-claims/">stalled</a>, a <a href="/">San Marcos public adjuster</a> can review the policy, your documentation, and the insurer’s estimate with you. Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement.</p>
HTML,
];
