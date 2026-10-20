<?php
return [
    'template'    => 'weather-events',
    'title'       => 'Recent Weather Events in San Marcos & Hays County',
    'seo_title'   => 'Recent San Marcos Storm Reports | Hays County Weather Events',
    'description' => 'Recent weather events in San Marcos and Hays County: preliminary NWS hail, wind, tornado, and flash flood reports, updated automatically every hour.',
    'lead'        => 'Preliminary hail, wind, tornado, and flood reports for Hays County from the National Weather Service, gathered automatically so you can see what was reported, where, and when.',
    'kicker'      => 'Automatically Updated',
    'image'       => '/assets/img/featured/page-weather-events.webp',
    'image_alt'   => 'Hailstones and broken branches on a lawn after a Central Texas thunderstorm',
    'faqs' => [
        ['q' => 'What is a Local Storm Report?', 'a' => '<p>A Local Storm Report (LSR) is a short, preliminary notice the National Weather Service issues when it learns of hazardous weather such as hail, damaging wind, a tornado, or flooding. Reports come from trained spotters, emergency managers, law enforcement, the public, and automated weather instruments.</p>'],
        ['q' => 'How often do the Hays County storm reports update?', 'a' => '<p>The site checks the National Weather Service for new Local Storm Reports from NWS Austin/San Antonio about once an hour and also checks the Iowa Environmental Mesonet archive of the same reports. Duplicates are removed and corrected reports replace the originals.</p>'],
        ['q' => 'The storm that damaged my house is not listed. Why?', 'a' => '<p>A report exists only if someone saw the weather and passed it to the NWS. Storms at night or over rural parts of Hays County often cause damage without any report. A missing report does not mean the storm missed your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius or date window, and rely on photos and an inspection.</p>'],
        ['q' => 'Can I use these reports in my insurance claim?', 'a' => '<p>Yes, as supporting documentation. A report of hail or high wind near your property on your date of loss helps establish that a storm occurred. It does not prove your building was damaged or decide coverage, so pair it with photos, an inspection, and an estimate.</p>'],
        ['q' => 'Do flooded roads and low water crossings show up here?', 'a' => '<p>When the NWS issues a flash flood report, such as water over a road or a high water rescue, it appears on this page. Keep in mind that flood damage to a building is generally excluded from standard homeowners and commercial policies and is usually covered, if at all, under a separate flood policy. See our <a href="/services/flood-damage-claims/">flood damage claims</a> page.</p>'],
    ],
    'body' => <<<'HTML'
<h2>About these NWS Local Storm Reports</h2>
<p>The recent weather events above are <strong>Local Storm Reports (LSRs)</strong> issued by the National Weather Service Austin/San Antonio office in New Braunfels, the forecast office responsible for San Marcos and all of Hays County. Each LSR is a quick notice that something hazardous was observed: hail with an estimated size, a measured or estimated wind gust, wind damage such as downed trees or power lines, a tornado or funnel cloud, flash flooding, or heavy rainfall.</p>
<p>Reports come from many places:</p>
<ul>
<li><strong>Trained storm spotters</strong> who report hail size, wind, and flooding.</li>
<li><strong>Emergency managers, police, and fire departments</strong> who report damage, road closures at low water crossings, and water rescues.</li>
<li><strong>Media and the public</strong>, often by phone, through the mPING app, or with photos posted to social media.</li>
<li><strong>Automated instruments</strong>, such as the weather station at San Marcos Regional Airport (KHYI), which record measured gusts and rainfall.</li>
</ul>
<p>Because LSRs go out fast, sometimes while the storm is still in progress, sizes, speeds, times, and locations may be estimates. The NWS can revise them, and the verified version appears months later in the NOAA Storm Events Database, which you can search on our <a href="/storm-history/">Hays County storm history</a> page.</p>

<h2>How the page stays current</h2>
<p>No one has to update this page by hand. About once an hour, the site asks the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a> for new Local Storm Report products from NWS Austin/San Antonio and keeps the reports located in and around Hays County. It also checks the Iowa Environmental Mesonet, a university archive that stores copies of the same NWS reports, to catch anything that has already rolled off the NWS feed.</p>
<p>When the same report shows up in both sources, only one copy is kept. When the NWS issues a correction, the corrected report replaces the original. If an update cannot reach either source, the page keeps the reports from the last successful update and says so in the notice at the top.</p>

<h2>Preliminary reports vs. the official NOAA record</h2>
<table>
<thead><tr><th></th><th>NWS Local Storm Reports (this page)</th><th>NOAA Storm Events Database</th></tr></thead>
<tbody>
<tr><td>Timing</td><td>Minutes to hours after the event</td><td>Usually a few months later</td></tr>
<tr><td>Status</td><td>Preliminary and may be revised</td><td>Reviewed and finalized by the NWS</td></tr>
<tr><td>Detail</td><td>Brief remarks, estimated sizes and speeds</td><td>Fuller narratives, sometimes storm survey findings</td></tr>
<tr><td>Best use</td><td>Confirming a recent storm quickly</td><td>Researching older storms and seasonal patterns</td></tr>
<tr><td>Where to find it</td><td>Here and in the <a href="/storm-lookup/">storm lookup</a></td><td><a href="/storm-history/">Storm history</a> and the <a href="/storm-lookup/">storm lookup</a></td></tr>
</tbody>
</table>

<h2>Using storm reports to support a claim</h2>
<p>A report near your property on your date of loss can be useful evidence that a hailstorm or damaging wind actually reached your area. That matters when an insurer questions the date or cause of damage, which comes up often in Hays County, where spring storms tracking along I-35 can hit San Marcos, Kyle, and Buda within the same season.</p>
<ol>
<li><strong>Write down your date of loss</strong> and what you saw or heard during the storm.</li>
<li><strong>Look for matching reports</strong> on this page, or search by city or ZIP code and distance with the <a href="/storm-lookup/">storm lookup tool</a>.</li>
<li><strong>Save a copy</strong> with the time, location, magnitude, and source visible.</li>
<li><strong>Add it to your claim file</strong> with your photos, video, and repair estimates. The <a href="/claim-documentation-checklist/">claim documentation checklist</a> can help you organize everything.</li>
</ol>
<p>For background on when hail is most common here, read <a href="/san-marcos-hail-season-storm-data/">San Marcos hail season storm data</a>.</p>

<h2>Limitations to keep in mind</h2>
<ul>
<li><strong>Reports follow the observers.</strong> Damaging hail or wind can fall where nobody reported it, and a report a few miles away does not mean your property saw the same thing.</li>
<li><strong>A report is not a damage finding.</strong> Only a physical inspection can show whether a particular roof, window, or wall was damaged.</li>
<li><strong>Preliminary numbers change.</strong> Hail sizes and wind speeds may be estimated and later revised.</li>
<li><strong>Your policy decides coverage.</strong> Weather records support a claim; the policy terms, exclusions, and deductibles determine what is paid.</li>
</ul>
<p>If your insurer disputes the date or cause of storm damage, a <a href="/">San Marcos public adjuster</a> can help review the evidence. Learn more about our <a href="/services/storm-damage-claims/">storm damage claims</a> and <a href="/services/hail-damage-claims/">hail damage claims</a> services.</p>
HTML,
];
