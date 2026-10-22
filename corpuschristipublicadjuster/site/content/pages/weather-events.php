<?php
return [
    'template'    => 'weather-events',
    'title'       => 'Recent Weather Events in Corpus Christi & the Coastal Bend',
    'seo_title'   => 'Recent Corpus Christi Storm Reports | Coastal Bend Weather',
    'description' => 'Recent weather events in Corpus Christi and the Coastal Bend: NWS hail, wind, tornado, and flood reports for Nueces, San Patricio, Aransas, and Kleberg.',
    'lead'        => 'Preliminary hail, wind, tornado, flood, and coastal reports from the National Weather Service in Corpus Christi for Nueces, San Patricio, Aransas, and Kleberg counties, collected automatically.',
    'kicker'      => 'Automatically Updated',
    'image'       => '/assets/img/featured/page-weather-events.webp',
    'image_alt'   => 'Downed tree limbs and storm debris on a Corpus Christi street after a thunderstorm',
    'faqs' => [
        ['q' => 'What is a Local Storm Report?', 'a' => '<p>A Local Storm Report (LSR) is a preliminary report the National Weather Service issues when it receives information about hazardous weather, such as hail, damaging wind, a tornado or waterspout, flooding, or high surf and coastal flooding. Reports come from trained spotters, emergency managers, law enforcement, the public, and weather instruments.</p>'],
        ['q' => 'Which areas does this page cover?', 'a' => '<p>It covers reports for Nueces, San Patricio, Aransas, and Kleberg counties, including Corpus Christi, Padre Island, Port Aransas, Portland, Ingleside, Aransas Pass, Rockport, Robstown, and Kingsville. All four counties are served by the NWS Corpus Christi office.</p>'],
        ['q' => 'How often is this page updated?', 'a' => '<p>The site checks the National Weather Service API every hour for new Local Storm Reports from NWS Corpus Christi, and also checks the Iowa Environmental Mesonet archive of the same reports. Duplicates are removed and corrections are applied.</p>'],
        ['q' => 'Why is the storm that hit my house not listed?', 'a' => '<p>A report exists only if someone observed and reported the weather to the NWS. Many storms, especially at night or in rural parts of the county, cause damage without any report. The absence of a report does not mean a storm did not affect your property. Try the <a href="/storm-lookup/">storm lookup tool</a> with a wider radius or date window.</p>'],
        ['q' => 'Can I use these reports in my insurance claim?', 'a' => '<p>Yes, as supporting documentation. A report of hail or high wind near your property on your date of loss can help establish when a storm occurred. It does not prove your building was damaged, and it does not decide coverage. Pair it with photos, an inspection, and an estimate.</p>'],
    ],
    'body' => <<<'HTML'
<h2>What are Local Storm Reports?</h2>
<p>The reports above are <strong>Local Storm Reports (LSRs)</strong> issued by the <a href="https://www.weather.gov/crp" target="_blank" rel="noopener">National Weather Service office in Corpus Christi</a>, which serves Corpus Christi and the Coastal Bend. This page keeps the reports for <strong>Nueces, San Patricio, Aransas, and Kleberg counties</strong>. An LSR is a short, preliminary notice that hazardous weather was observed: hail and its estimated size, a measured or estimated wind gust, wind damage such as downed trees or power lines, a tornado or waterspout, flash flooding, heavy rain, or coastal flooding.</p>
<p>The information comes from several kinds of sources:</p>
<ul>
<li><strong>Trained storm spotters</strong> who report hail size, wind, and other conditions.</li>
<li><strong>Emergency managers, law enforcement, and fire departments</strong> who report damage and flooding.</li>
<li><strong>The public</strong>, often by phone or through social media posts with photos.</li>
<li><strong>Instruments</strong> such as airport stations and coastal mesonet sites that record measured wind gusts.</li>
</ul>
<p>Because LSRs are issued quickly, sometimes while a storm is still underway, sizes, speeds, times, and locations can be estimates. The NWS may revise them, and the verified record is published months later in the NOAA Storm Events Database, which you can search on our <a href="/storm-history/">storm history</a> page.</p>

<h2>How this page updates</h2>
<p>This page is maintained automatically. Every hour, the site checks the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a> API for new Local Storm Report products from NWS Corpus Christi and keeps the reports in the four covered counties. It also checks the Iowa Environmental Mesonet archive, which stores copies of the same NWS reports, to fill in anything that has rolled off the NWS feed.</p>
<p>When the same report appears in both sources, the duplicate is removed. When the NWS corrects an earlier report, the corrected version replaces the original. If an update cannot reach the data sources, the page keeps showing the reports from the last successful update and says so in the notice at the top.</p>

<h2>How to use storm reports in an insurance claim</h2>
<p>If your home or business was damaged, a report near your property on your date of loss can be useful supporting evidence. It helps show that hail, damaging wind, or tropical-storm conditions actually occurred in your area, which matters when an insurer questions the date or cause of damage.</p>
<ol>
<li><strong>Note your date of loss.</strong> Write down when the storm hit and what you saw or heard.</li>
<li><strong>Find matching reports.</strong> Look for reports on that date here, or use the <a href="/storm-lookup/">storm lookup tool</a> to search by city or ZIP code and distance.</li>
<li><strong>Save a copy.</strong> Screenshot or print the report with its time, location, and source.</li>
<li><strong>Add it to your claim file</strong> with your photos, video, and repair estimates. Our <a href="/claim-documentation-checklist/">documentation checklist</a> helps you organize everything.</li>
</ol>
<p>For more on this topic, read <a href="/noaa-weather-records-document-property-damage-corpus-christi/">how NOAA weather records can help document property damage in Corpus Christi</a>.</p>

<h2>Limitations to keep in mind</h2>
<ul>
<li><strong>Reports reflect where observers were.</strong> Hail or wind can strike where no one reported it, and a report a few miles away does not mean your property saw the same conditions.</li>
<li><strong>A report is not a damage finding.</strong> It does not prove that a specific roof, window, or wall was damaged. That takes a physical inspection.</li>
<li><strong>Preliminary data changes.</strong> Hail sizes and wind speeds may be estimates and may be revised.</li>
<li><strong>Coverage depends on your policy.</strong> Weather records support a claim; your policy terms, exclusions, and deductibles decide what is covered. Coastal surge is usually a flood-policy matter, not a TWIA or homeowners one.</li>
</ul>
<p>If your insurer disputes the date or cause of storm damage, a licensed public adjuster can help review the evidence. Learn more about our <a href="/services/storm-damage-claims/">storm damage claim services</a> and <a href="/services/wind-damage-claims/">wind damage claims</a>.</p>
HTML,
];
