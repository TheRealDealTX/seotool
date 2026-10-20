<?php
return [
    'template'    => 'weather-events',
    'title'       => 'Recent Weather Events in Port Arthur & Jefferson County',
    'seo_title'   => 'Recent Port Arthur Storm Reports | Jefferson County Weather',
    'description' => 'Recent weather events in Port Arthur and Jefferson County: wind, hail, tornado, and flood reports from the National Weather Service, updated automatically.',
    'lead'        => 'Preliminary wind, hail, tornado, and flood reports for Jefferson County from the National Weather Service, collected automatically so you can see what was reported and when.',
    'kicker'      => 'Automatically Updated',
    'image'       => '/assets/img/featured/page-weather-events.webp',
    'image_alt'   => 'Storm debris and downed branches on a street after a Jefferson County thunderstorm',
    'faqs' => [
        ['q' => 'What is a Local Storm Report?', 'a' => '<p>A Local Storm Report (LSR) is a preliminary report the National Weather Service issues when it receives information about hazardous weather, such as hail, damaging wind, a tornado, or flooding. Reports come from trained spotters, emergency managers, law enforcement, the public, and weather instruments.</p>'],
        ['q' => 'How often is this page updated?', 'a' => '<p>The page automatically checks the National Weather Service API every hour for new Local Storm Reports from NWS Lake Charles, and also checks the Iowa Environmental Mesonet archive of the same reports. Duplicates are removed and corrections are applied.</p>'],
        ['q' => 'Why is the storm that hit my house not listed?', 'a' => '<p>A report exists only if someone observed and reported the weather to the NWS. Many storms, especially at night or during a hurricane, produce damage without any report. The absence of a report does not mean a storm did not affect your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius or date window, and rely on photos and a professional inspection.</p>'],
        ['q' => 'Can I use these reports in my insurance claim?', 'a' => '<p>Yes, as supporting documentation. A report showing high wind or flooding near your property on your date of loss can help establish when a storm occurred. It does not prove your building was damaged, and it does not decide coverage. Pair it with photos, an inspection, and an estimate.</p>'],
    ],
    'body' => <<<'HTML'
<h2>What are Local Storm Reports?</h2>
<p>The reports above are <strong>Local Storm Reports (LSRs)</strong> issued by the National Weather Service office in Lake Charles, Louisiana, which serves Southeast Texas, including Port Arthur and the rest of Jefferson County. An LSR is a short, preliminary notice that hazardous weather was observed: a measured or estimated wind gust, wind damage such as downed trees or power lines, hail and its estimated size, a tornado or funnel cloud, flash flooding, storm surge, or heavy rain.</p>
<p>The information comes from several kinds of sources:</p>
<ul>
<li><strong>Trained storm spotters</strong> who report wind, hail, flooding, and other conditions.</li>
<li><strong>Emergency managers, law enforcement, and fire departments</strong> who report damage and flooding.</li>
<li><strong>The public</strong>, often through phone calls or social media posts with photos.</li>
<li><strong>Instruments</strong> such as airport weather stations and rain gauges that record measured gusts and rainfall.</li>
</ul>
<p>Because LSRs are issued quickly, sometimes while a storm is still in progress, sizes, speeds, times, and locations can be estimates. The NWS may later revise them, and the verified record is published months later in the NOAA Storm Events Database, which you can search on our <a href="/storm-history/">storm history</a> page.</p>

<h2>How this page updates</h2>
<p>This page is maintained automatically. Every hour, the site checks the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a> API for new Local Storm Report products from NWS Lake Charles and keeps the reports that fall in and around Jefferson County. It also checks the Iowa Environmental Mesonet archive, which stores copies of the same NWS reports, to fill in anything that has rolled off the NWS feed.</p>
<p>When the same report appears in both sources, the duplicate is removed. When the NWS issues a correction to an earlier report, the corrected version replaces the original. If an update cannot reach the data sources, the page keeps showing the reports from the last successful update and says so in the notice at the top. For tropical systems that are still offshore, check the <a href="/hurricane-tracker/">hurricane tracker</a>.</p>

<h2>How to use storm reports in an insurance claim</h2>
<p>If your home or business was damaged, a report near your property on your date of loss can be useful supporting evidence. It helps show that a storm with damaging wind, hail, or flooding actually occurred in your area, which can matter when an insurer questions the date or cause of damage.</p>
<ol>
<li><strong>Note your date of loss.</strong> Write down when the storm hit and what you saw or heard.</li>
<li><strong>Find matching reports.</strong> Look for reports on that date here, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by city or ZIP code and distance.</li>
<li><strong>Save a copy.</strong> Screenshot or print the report, including its time, location, and source.</li>
<li><strong>Add it to your claim file</strong> together with your photos, video, and repair estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> helps you organize everything.</li>
</ol>
<p>For a deeper explanation of documenting a loss, read <a href="/how-to-document-storm-damage-port-arthur/">how to document storm damage in Port Arthur</a>.</p>

<h2>Limitations to keep in mind</h2>
<ul>
<li><strong>Reports reflect where observers were.</strong> Damaging wind or flooding can occur where no one reported it, and a report a few miles away does not mean your property saw the same conditions.</li>
<li><strong>A report is not a damage finding.</strong> It does not prove that a specific roof, window, or wall was damaged. That requires a physical inspection.</li>
<li><strong>Preliminary data changes.</strong> Wind speeds, hail sizes, and rainfall totals may be estimates and may be revised.</li>
<li><strong>Coverage depends on your policy.</strong> Weather records support a claim; your policy terms, exclusions, and deductibles determine what is covered.</li>
</ul>
<p>If your insurer disputes the date or cause of storm damage, a licensed public adjuster can help review the evidence. Learn more about our <a href="/services/storm-damage-claims/">storm damage claim services</a>.</p>
HTML,
];
