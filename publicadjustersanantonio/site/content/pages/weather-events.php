<?php
return [
    'template'    => 'weather-events',
    'title'       => 'Recent Weather Events in San Antonio & Bexar County',
    'seo_title'   => 'Recent San Antonio Storm Reports | Bexar County Weather Events',
    'description' => 'Recent weather events in San Antonio and Bexar County: hail, wind, tornado, and flood reports from the National Weather Service, updated automatically.',
    'lead'        => 'Preliminary hail, wind, tornado, and flood reports for Bexar County from the National Weather Service, collected automatically so you can see what was reported and when.',
    'kicker'      => 'Automatically Updated',
    'image'       => '/assets/img/featured/page-weather-events.webp',
    'image_alt'   => 'Hailstones and storm debris on a lawn after a San Antonio thunderstorm',
    'faqs' => [
        ['q' => 'What is a Local Storm Report?', 'a' => '<p>A Local Storm Report (LSR) is a preliminary report the National Weather Service issues when it receives information about hazardous weather, such as hail, damaging wind, a tornado, or flooding. Reports come from trained spotters, emergency managers, law enforcement, the public, and weather instruments.</p>'],
        ['q' => 'How often is this page updated?', 'a' => '<p>The page automatically checks the National Weather Service API every hour for new Local Storm Reports from NWS Austin/San Antonio, and also checks the Iowa Environmental Mesonet archive of the same reports. Duplicates are removed and corrections are applied.</p>'],
        ['q' => 'Why is the storm that hit my house not listed?', 'a' => '<p>A report exists only if someone observed and reported the weather to the NWS. Many storms, especially at night or in less populated areas, produce damage without any report. The absence of a report does not mean a storm did not affect your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius or date window, and rely on photos and a professional inspection.</p>'],
        ['q' => 'Can I use these reports in my insurance claim?', 'a' => '<p>Yes, as supporting documentation. A report showing hail or high wind near your property on your date of loss can help establish when a storm occurred. It does not prove your building was damaged, and it does not decide coverage. Pair it with photos, an inspection, and an estimate.</p>'],
        ['q' => 'Are flooded low water crossings on this page?', 'a' => '<p>When the NWS issues a Local Storm Report for flash flooding, such as road closures at low water crossings or high water rescues, it appears here. Keep in mind that flood damage to a building is generally excluded from standard homeowners and commercial policies and is usually covered, if at all, by a separate flood policy.</p>'],
    ],
    'body' => <<<'HTML'
<h2>What are Local Storm Reports?</h2>
<p>The reports above are <strong>Local Storm Reports (LSRs)</strong> issued by the National Weather Service Austin/San Antonio office, located in New Braunfels, which serves San Antonio, Bexar County, and the surrounding region. An LSR is a short, preliminary notice that hazardous weather was observed: hail and its estimated size, a measured or estimated wind gust, wind damage such as downed trees or power lines, a tornado or funnel cloud, flash flooding, or heavy rain.</p>
<p>The information comes from several kinds of sources:</p>
<ul>
<li><strong>Trained storm spotters</strong> who report hail size, wind, and other conditions.</li>
<li><strong>Emergency managers, law enforcement, and fire departments</strong> who report damage, flooded roads, and high water rescues.</li>
<li><strong>Broadcast media and the public</strong>, often through phone calls, mPING reports, or social media posts with photos.</li>
<li><strong>Instruments</strong> such as the airport weather stations at San Antonio International and Randolph that record measured wind gusts.</li>
</ul>
<p>Because LSRs are issued quickly, sometimes while a storm is still in progress, sizes, speeds, times, and locations can be estimates. The NWS may later revise them, and the verified record is published months later in the NOAA Storm Events Database, which you can search on our <a href="/storm-history/">storm history</a> page.</p>

<h2>How this page updates</h2>
<p>This page is maintained automatically. Every hour, the site checks the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a> API for new Local Storm Report products from NWS Austin/San Antonio and keeps the reports that fall in Bexar County. It also checks the Iowa Environmental Mesonet archive, which stores copies of the same NWS reports, to fill in anything that has rolled off the NWS feed.</p>
<p>When the same report appears in both sources, the duplicate is removed. When the NWS issues a correction to an earlier report, the corrected version replaces the original. If an update cannot reach the data sources, the page keeps showing the reports from the last successful update and says so in the notice at the top.</p>

<h2>How to use storm reports in an insurance claim</h2>
<p>If your home or business was damaged, a report near your property on your date of loss can be useful supporting evidence. It helps show that a storm with hail or damaging wind actually occurred in your area, which can matter when an insurer questions the date or cause of damage. That question comes up often in San Antonio, where more than one spring hailstorm may cross the same neighborhood in a single season.</p>
<ol>
<li><strong>Note your date of loss.</strong> Write down when the storm hit and what you saw or heard.</li>
<li><strong>Find matching reports.</strong> Look for reports on that date here, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by city or ZIP code and distance.</li>
<li><strong>Save a copy.</strong> Screenshot or print the report, including its time, location, and source.</li>
<li><strong>Add it to your claim file</strong> together with your photos, video, and repair estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> helps you organize everything.</li>
</ol>
<p>For a look at how often hail falls in Bexar County and when, read our <a href="/san-antonio-hail-season-storm-data/">San Antonio hail season storm data</a> article.</p>

<h2>Limitations to keep in mind</h2>
<ul>
<li><strong>Reports reflect where observers were.</strong> Damaging hail or wind can fall where no one reported it, and a report a few miles away does not mean your property saw the same conditions.</li>
<li><strong>A report is not a damage finding.</strong> It does not prove that a specific roof, window, or wall was damaged. That requires a physical inspection.</li>
<li><strong>Preliminary data changes.</strong> Hail sizes and wind speeds may be estimates and may be revised.</li>
<li><strong>Coverage depends on your policy.</strong> Weather records support a claim; your policy terms, exclusions, and deductibles determine what is covered.</li>
</ul>
<p>If your insurer disputes the date or cause of storm damage, a licensed public adjuster can help review the evidence. Learn more about our <a href="/services/storm-damage-claims/">storm damage claim services</a>.</p>
HTML,
];
