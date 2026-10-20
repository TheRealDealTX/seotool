<?php
return [
    'template'    => 'storm-lookup',
    'title'       => 'Storm Event Lookup for Dallas Properties',
    'seo_title'   => 'Storm Event Lookup | Hail & Wind Reports Near Dallas ZIP Codes',
    'description' => 'Storm event lookup for Dallas and Dallas County: search NOAA and NWS hail, wind, tornado, and flood reports near your city or ZIP code by date and radius.',
    'lead'        => 'Search official NOAA and National Weather Service storm reports near a Dallas-area city or ZIP code to see what was recorded around your date of loss.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-storm-lookup.webp',
    'image_alt'   => 'Map of storm report locations around Dallas, Texas',
    'faqs' => [
        ['q' => 'Do I need to enter my street address?', 'a' => '<p>No. The storm lookup uses the center point of the city or ZIP code you enter. We do not ask for or store street addresses. Keep in mind that distances are measured from that center point, not from your property.</p>'],
        ['q' => 'What data does the storm lookup search?', 'a' => '<p>It searches verified records from the NOAA NCEI Storm Events Database for Dallas County and preliminary Local Storm Reports issued by the National Weather Service Fort Worth/Dallas office. County- and zone-wide events such as winter storms, ice storms, and extreme cold are included when you set a date or date range.</p>'],
        ['q' => 'I live in Plano, Carrollton, or Grand Prairie. Will this work for me?', 'a' => '<p>Partly. The verified NOAA history here covers Dallas County, so reports from inside Dallas County within your radius will appear. Much of Plano is in Collin County, and parts of Carrollton, Grand Prairie, Richardson, and Rowlett extend into Collin, Denton, Tarrant, or Rockwall County. Events recorded only in those counties are not in this dataset; search the <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA Storm Events Database</a> for those counties directly.</p>'],
        ['q' => 'Why did my search return no results?', 'a' => '<p>Try a wider radius, a longer date window, or "Hail, wind &amp; more" as the event type. If there is still nothing, it may simply mean no one reported the storm. Many storms cause damage without an official report, so a missing record does not prove your property was unaffected.</p>'],
        ['q' => 'Will a matching storm report get my claim approved?', 'a' => '<p>No tool or report can guarantee a claim outcome. A nearby report is supporting evidence that a storm occurred. Your insurer will still evaluate the actual damage, the cause, and your policy terms.</p>'],
    ],
    'body' => <<<'HTML'
<h2>How the storm event lookup works</h2>
<p>This storm event lookup helps Dallas and Dallas County property owners find official weather reports near a location and date. Enter a city or ZIP code, choose a search radius, and optionally add the approximate date of loss. The tool measures the distance from the <strong>center point</strong> of that city or ZIP code to each report that has coordinates and lists the ones inside your radius.</p>
<p>Results draw on two sources:</p>
<ul>
<li><strong>NOAA NCEI Storm Events Database</strong> &ndash; the verified federal record, published a few months after events occur. For Dallas County it holds more than 2,100 entries, including 841 hail reports since 1955 and 109 tornadoes since 1952. You can browse it in full on the <a href="/storm-history/">storm history</a> page.</li>
<li><strong>National Weather Service Local Storm Reports</strong> &ndash; preliminary reports from NWS Fort Worth/Dallas that appear within hours of a storm. The newest ones are also listed on the <a href="/weather-events/">recent weather events</a> page.</li>
</ul>
<p>Some events, such as winter storms, ice storms, and extreme cold, are recorded for a whole county or NWS forecast zone rather than a single point. Those county- and zone-wide events appear in your results when you set a date or date range that matches them. Winter Storm Uri in February 2021 is an example.</p>

<h2>Tips for better results</h2>
<ul>
<li><strong>Start with your date of loss and a &plusmn;7-day window.</strong> People often remember the week of a storm but not the exact day, and a storm that runs late at night may be logged on the following date.</li>
<li><strong>Use a date range in spring.</strong> April and May are the peak months for hail in Dallas County, and more than one hailstorm can cross the same part of town in a single season. If you discovered damage later, search the whole March&ndash;June season, and remember the smaller October bump.</li>
<li><strong>Widen the radius if nothing appears.</strong> Reports cluster where people were when the storm passed. If your neighborhood shows nothing within 3 or 5 miles, try 10 or 20 miles and read where each report actually was.</li>
<li><strong>Filter by event type</strong> once you know what you are looking for, such as hail for a dented roof, wind for missing shingles and fallen trees, or tornado for structural damage.</li>
<li><strong>Read the narrative.</strong> NOAA location names are reference points (for example, "Gribble," "Sowers," or "Bouchard"), and the narrative usually names the actual city or streets, such as Harry Hines Blvd. or Skillman St.</li>
</ul>

<h2>Documenting what you find</h2>
<p>If you find a report that matches your date and area, save it. Open the linked NCEI record or note the NWS report details, then screenshot or print it with the date, time, location, magnitude, and source visible. Add it to your claim file together with:</p>
<ul>
<li>Dated photos and video of the damage, ideally taken before any cleanup or repairs.</li>
<li>Notes on when you noticed the damage and what you saw during the storm.</li>
<li>Your claim number, adjuster contacts, and a log of communications.</li>
<li>Repair estimates and receipts for emergency mitigation such as tarping.</li>
</ul>
<p>Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> walks through this step by step, and <a href="/document-hail-damage-for-an-insurance-claim/">how to document hail damage for an insurance claim</a> covers roof photos in more detail.</p>

<h2>Limitations: nearby does not mean damaged</h2>
<p>A storm report is evidence that weather was observed at a place and time. It is <strong>not proof that your property was damaged</strong>, and it does not decide coverage. Hail and wind can vary sharply over short distances, so a report three miles away may not reflect what happened at your building. The opposite is also true: storms frequently damage properties where no one filed a report.</p>
<p>Also remember that preliminary NWS reports may contain estimated sizes, speeds, and locations that are later revised, and that distances here are measured from a city or ZIP center, not your address. Use these records as one part of your documentation alongside a physical inspection. If your insurer disputes the date or cause of storm damage, a Dallas Public Adjuster can help review the evidence; see our <a href="/services/storm-damage-claims/">storm damage claims</a> and <a href="/services/hail-damage-claims/">hail damage claims</a> pages.</p>
HTML,
];
