<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
return [
    'body' => <<<'HTML'
<h2>How the quiz picks your under desk elliptical</h2>
<p>Each answer changes the weight of different features. Choosing "standing" removes seated-only machines. "Circulation or limited mobility" favors motorized models that move your legs for you. "Very quiet" boosts magnetic-resistance machines with a record of silent running. Budget and who it's for fine-tune the ranking.</p>
<p>The results are matched only on fit. Our affiliate relationship with Amazon never changes which product comes out on top.</p>
<h2>Want to compare yourself?</h2>
<p>Use the <a href="/tools/compare-under-desk-ellipticals/">comparison table</a>, or go straight to the guides:</p>
<ul>
<li><a href="/what-is-the-best-under-desk-elliptical/">Best under desk elliptical overall</a></li>
<li><a href="/best-under-desk-elliptical-for-seniors/">Best for seniors</a></li>
<li><a href="/best-motorized-under-desk-elliptical/">Best motorized</a></li>
<li><a href="/quietest-under-desk-elliptical/">Quietest models</a></li>
<li><a href="/can-you-stand-on-an-under-desk-elliptical/">Options for standing</a></li>
</ul>
HTML,
    'faq' => [
        ['q' => 'What is the best under desk elliptical for most people?', 'a' => 'The Cubii JR2. It is quiet, smooth, compact and well supported. The quiz may suggest something better for your specific needs.'],
        ['q' => 'Should I get a manual or motorized under desk elliptical?', 'a' => 'Manual if you want exercise and calorie burn. Motorized if circulation, rehab or limited mobility is the goal.'],
    ],
];
