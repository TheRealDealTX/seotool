<?php
$slug = 'storm-damage-checklist';
$toolFaqs = [
    ['q' => 'Should I climb on my roof to check for storm damage?', 'a' => 'No. Wet, damaged roofs are dangerous, and walking on hail-bruised shingles can make damage worse. Every item on this checklist can be checked from the ground, the yard or inside the attic.'],
    ['q' => 'What if I see dents on gutters but no leaks?', 'a' => 'Dented soft metals are a strong sign hail was large enough to bruise shingles. Leaks often appear months later, so schedule an inspection soon while the storm date is fresh for any insurance claim.'],
    ['q' => 'How soon after a storm should I get an inspection?', 'a' => 'As soon as practical, ideally within days. Prompt inspections catch damage before it leaks, and many insurance policies require timely reporting of storm losses.'],
];
$toolBody = <<<'HTML'
<h2>Using This Checklist After a Bastrop Storm</h2>
<p>Spring hail and summer wind storms roll through Bastrop County every year. When one passes, wait until it is safe, then walk the property with this checklist on your phone. Every item has a weight based on how strongly it signals roof damage. Shingles in the yard or a new ceiling stain count far more than a dented mailbox.</p>
<h2>What Happens Next</h2>
<ol>
<li>Photograph everything you checked, with dates.</li>
<li>Schedule a free <a href="/services/roof-inspection-bastrop-tx/">roof inspection</a>. We document hail and wind damage slope by slope.</li>
<li>If damage is confirmed, contact your insurer. We can meet the adjuster on site.</li>
<li>Get repairs or a replacement through our <a href="/services/storm-damage-roof-repair-bastrop-tx/">storm damage</a> and <a href="/services/hail-damage-roof-repair-bastrop-tx/">hail damage roof repair</a> services.</li>
</ol>
<p>Active leak right now? Skip the checklist and call <a href="tel:+15122977580">(512) 297-7580</a> for <a href="/services/emergency-roof-repair-bastrop-tx/">emergency roof repair</a> from <a href="/">Bastrop Roofing</a>.</p>
HTML;
require dirname(__DIR__, 2) . '/includes/templates/tool.php';
