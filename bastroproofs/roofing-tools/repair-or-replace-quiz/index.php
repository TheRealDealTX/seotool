<?php
$slug = 'repair-or-replace-quiz';
$toolFaqs = [
    ['q' => 'Can a quiz really tell me if I need a new roof?', 'a' => 'No quiz replaces an inspection, but the questions mirror what a roofer weighs: age, extent of damage, leak history, shingle condition, structure and how long you will stay. It points you in the right direction before you call.'],
    ['q' => 'What roof age usually means replacement in Bastrop?', 'a' => 'Architectural shingle roofs in Central Texas often reach the end of their service life around 18 to 25 years. Age alone is not decisive, but combined with widespread wear it usually is.'],
    ['q' => 'Is it worth repairing a roof I plan to sell soon?', 'a' => 'Often yes. If the roof is otherwise sound, a solid repair and a clean inspection report can satisfy buyers. If the roof is near the end of its life, buyers and lenders may ask for replacement or a credit.'],
];
$toolBody = <<<'HTML'
<h2>How the Quiz Scores Your Roof</h2>
<p>Each answer adds points toward replacement. Young roofs with isolated damage and no leak history score toward <a href="/services/roof-repair-bastrop-tx/">roof repair</a>. Older roofs with widespread wear, repeated leaks or structural concerns score toward <a href="/services/roof-replacement-bastrop-tx/">roof replacement</a>. How long you plan to stay matters too: the longer your horizon, the more a new roof's full lifespan pays off.</p>
<h2>Why the Answer Is Not Always Obvious</h2>
<p>A single leak on a 22-year-old roof might still be repairable, and a five-year-old roof with hail damage on every slope might need replacing through insurance. That is why every recommendation from a <a href="/">Bastrop roofer</a> on our team comes after a hands-on <a href="/services/roof-inspection-bastrop-tx/">roof inspection</a>, with photos so you can see what we see.</p>
HTML;
require dirname(__DIR__, 2) . '/includes/templates/tool.php';
