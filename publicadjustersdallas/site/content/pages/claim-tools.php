<?php
return [
    'title'       => 'Free Insurance Claim Tools',
    'seo_title'   => 'Free Insurance Claim Tools for Dallas Property Owners',
    'description' => 'Free insurance claim tools for Dallas and Dallas County: settlement calculator, documentation checklist, storm lookup, live weather, and storm history.',
    'lead'        => 'Practical, free tools for homeowners and business owners in Dallas, Dallas County, and surrounding North Texas communities, built on official NOAA and National Weather Service data.',
    'kicker'      => 'Resources',
    'image'       => '/assets/img/featured/page-claim-tools.webp',
    'image_alt'   => 'Laptop showing insurance claim tools and a storm map of Dallas',
    'wide'        => true,
    'faqs' => [
        ['q' => 'Are these claim tools really free?', 'a' => '<p>Yes. All of the tools are free to use, with no sign-up required. The calculator and checklist run in your browser, and nothing you enter in them is sent to us.</p>'],
        ['q' => 'Can these tools tell me whether my claim is covered?', 'a' => '<p>No. The tools are educational. They help you organize information and find weather records. Coverage depends on your policy terms and the facts of the loss. For a professional look at your situation, request a <a href="/free-claim-review/">Free Claim Review</a>.</p>'],
        ['q' => 'Where does the weather and storm data come from?', 'a' => '<p>Live conditions come from the National Weather Service station at Dallas Love Field (KDAL). Forecasts, alerts, and recent storm reports come from the NWS Fort Worth/Dallas office. Historical records come from the NOAA NCEI Storm Events Database for Dallas County. Each tool links to its original sources.</p>'],
        ['q' => 'Do the storm tools cover cities outside Dallas County, like Plano or Grand Prairie?', 'a' => '<p>The historical storm record on this site covers Dallas County. Several suburbs, including Plano, Carrollton, Garland, Richardson, Rowlett, and Grand Prairie, sit partly or wholly in neighboring counties. You can still search from those cities or ZIP codes, and reports inside Dallas County within your radius will appear. For events recorded in Collin, Denton, Tarrant, Rockwall, or Ellis County, search the <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA Storm Events Database</a> directly.</p>'],
    ],
    'body' => <<<'HTML'
<p>Filing a property insurance claim is easier when you understand the numbers, have your documents in order, and can show what the weather actually did on your date of loss. These free insurance claim tools are built for property owners in Dallas, Dallas County, and the surrounding North Texas cities, where spring hail, straight-line winds, tornadoes, flash flooding, and the occasional hard freeze drive most property claims.</p>

[[tools-grid]]

<h2>What each claim tool does</h2>

<h3>Insurance claim settlement calculator</h3>
<p>The <a href="/claim-calculator/">claim settlement calculator</a> shows how replacement cost value (RCV), depreciation, your deductible, policy limits, and prior payments combine into an initial payment, recoverable depreciation, and out-of-pocket cost. It is a quick way to see why the first check is often smaller than the repair estimate, especially with a percentage wind/hail deductible.</p>

<h3>Claim documentation checklist</h3>
<p>The <a href="/claim-documentation-checklist/">documentation checklist</a> gives you a step-by-step list for hail, wind, fire, water, roof, and commercial property damage. Track your progress, add notes, and print or download it. Your entries stay in your browser.</p>

<h3>Storm event lookup</h3>
<p>The <a href="/storm-lookup/">storm event lookup</a> searches NOAA and National Weather Service reports near a Dallas-area city or ZIP code, filtered by date, radius, and event type. It helps you find weather records that line up with your date of loss.</p>

<h3>Live Dallas weather</h3>
<p>The <a href="/weather/">live weather page</a> shows current conditions at Dallas Love Field, the 7-day forecast, and active NWS watches and warnings, along with storm preparation and post-storm tips.</p>

<h3>Dallas County storm history</h3>
<p>The <a href="/storm-history/">storm history</a> page lets you filter the official NOAA record for Dallas County, more than 2,100 events since 1952, by event type, date, location, hail size, and wind speed, with a timeline, map, and notable local storms such as the December 26, 2015 Garland and Rowlett tornado and the May 28, 2024 windstorm.</p>

<h3>Recent weather events</h3>
<p>The <a href="/weather-events/">recent weather events</a> page collects preliminary National Weather Service Local Storm Reports for Dallas County and updates automatically, so you can see what was reported in the days after a storm, long before the verified NOAA record is published.</p>

<h3>Dallas building codes</h3>
<p>The <a href="/local-building-codes/">local building codes</a> page explains the codes the City of Dallas enforces, when re-roofing and repairs need a permit, and how code upgrades relate to ordinance or law coverage in your policy.</p>

<h2>A simple way to use the tools together</h2>
<ol>
<li><strong>Confirm the storm.</strong> Use the storm lookup or recent weather events page to find reports near your city or ZIP code on your date of loss, and save a copy.</li>
<li><strong>Document the damage.</strong> Work through the checklist for your type of loss before cleanup or permanent repairs.</li>
<li><strong>Understand the numbers.</strong> When the insurer's estimate arrives, enter its figures in the calculator to see the ACV payment, recoverable depreciation, and what you may owe.</li>
<li><strong>Check code items.</strong> If the repair needs a permit, read the building codes page and compare the permitted scope with the insurer's estimate.</li>
</ol>

<h2>Use the tools, then get a second opinion</h2>
<p>These tools are educational. They do not decide coverage, and a nearby storm report does not prove damage at a specific property. If your claim was <a href="/services/denied-insurance-claims/">denied</a>, <a href="/services/underpaid-insurance-claims/">underpaid</a>, or <a href="/services/delayed-insurance-claims/">delayed</a>, a Dallas Public Adjuster can review your policy, documentation, and the insurer's estimate with you. Fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement.</p>
HTML,
];
