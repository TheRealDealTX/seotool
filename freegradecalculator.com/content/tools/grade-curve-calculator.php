<?php
return [
  'h1'          => 'Grade Curve Calculator',
  'meta_title'  => 'Grade Curve Calculator – Curve Test Scores 5 Ways',
  'description' => 'Free grade curve calculator: paste scores and curve them with a flat curve, added points, square root, target average, or bell curve. See the new average.',
  'lead'        => 'Paste a list of test scores, pick a curving method, and see every original and curved score side by side with the new class average.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the grade curve calculator</h2>
<ol class="steps">
  <li><strong>Paste your scores.</strong> Enter the class scores as percentages, one per line or separated by commas or spaces.</li>
  <li><strong>Choose a curve method.</strong> Pick a flat curve, add points, square-root curve, target average, or bell curve (each is explained below).</li>
  <li><strong>Fill in the setting for that method.</strong> For example, the number of points to add, the target class average, or the target mean and standard deviation.</li>
  <li><strong>Decide on capping.</strong> Turn on the cap at 100 if no student should end up above 100%.</li>
  <li><strong>Review the table.</strong> The results show each original score next to its curved score, plus the new class average.</li>
</ol>

<h2 id="curve-methods">The five curve methods and their formulas</h2>
<p>There is no single "correct" way to curve grades. Each method below changes scores differently, and schools and departments have their own rules about whether and how curves are allowed.</p>
<h3>1. Flat curve (top score becomes 100)</h3>
<p>Find the gap between the highest score and 100, then add that gap to every score. Everyone gains the same number of points.</p>
<div class="formula">Curved = Score + (100 − Highest score)</div>
<h3>2. Add N points</h3>
<p>You choose the bonus, such as 5 points, and every student gets it. This is the simplest curve to explain to a class.</p>
<div class="formula">Curved = Score + N</div>
<h3>3. Square-root curve</h3>
<p>Take the square root of the percentage and multiply by 10. Low scores rise the most, high scores rise a little, and 100 stays 100.</p>
<div class="formula">Curved = 10 × √Score</div>
<h3>4. Shift to a target class average</h3>
<p>The calculator adds the difference between your target average and the current average to every score, so the class mean lands exactly on your target.</p>
<div class="formula">Curved = Score + (Target average − Current average)</div>
<h3>5. Bell curve (target mean and standard deviation)</h3>
<p>Each score is converted to its distance from the mean in standard deviations, then rescaled to the mean and spread you choose. This keeps every student's relative position but changes both the center and the spread.</p>
<div class="formula">Curved = Target mean + (Score − Mean) × (Target SD ÷ SD)</div>

<div class="example-box"><h4>Worked example</h4>
<p>Five scores: 62, 70, 78, 85, 88. The original average is 383 ÷ 5 = <strong>76.6</strong>.</p>
<p><strong>Flat curve:</strong> the top score is 88, so add 12 points. New scores: 74, 82, 90, 97, 100. New average: <strong>88.6</strong>.</p>
<p><strong>Square-root curve:</strong> 10 × √62 = 78.74, 10 × √70 = 83.67, 10 × √78 = 88.32, 10 × √85 = 92.20, 10 × √88 = 93.81. New average: about <strong>87.3</strong>.</p>
<p><strong>Target average of 80:</strong> 80 − 76.6 = 3.4, so every score gains 3.4 points and the new average is exactly <strong>80</strong>.</p>
</div>

<h2 id="choosing">Which curve should you use?</h2>
<div class="compare">
<div class="compare-col"><h4>Same boost for everyone</h4><ul><li>Flat curve</li><li>Add N points</li><li>Target average</li><li>Easy to explain; keeps the gaps between students the same</li></ul></div>
<div class="compare-col"><h4>Boost depends on the score</h4><ul><li>Square-root curve</li><li>Bell curve</li><li>Helps struggling students more (square root) or reshapes the whole distribution (bell)</li></ul></div>
</div>
<p>A flat curve makes sense when one question was confusing or a test ran long and the whole class lost points. A square-root curve is popular when the test was simply too hard, because it lifts a 49 to a 70 but only moves a 96 to about 98. A bell curve is mostly used in large college courses that grade on a set distribution. For a deeper discussion of fairness and policy, read our guide on <a href="/blog/how-to-curve-grades">how to curve grades</a>.</p>

<h2 id="reading-results">Reading the curved results</h2>
<p>The results table lists each original score beside its curved score, and the new class average appears below it. Compare the two averages to see how big the curve really is. A flat curve that raises the average from 76.6 to 88.6 is a 12-point curve for everyone, while a square-root curve that lands at 87.3 gives the lowest scorer a 16.7-point boost and the top scorer only 5.8 points.</p>
<p>Try more than one method on the same list. Seeing the curved scores side by side often makes the right choice obvious, especially when you want to help students near the passing line without inflating the top of the class.</p>

<h2 id="tips">Tips and common mistakes</h2>
<ul>
  <li><strong>Check for outliers first.</strong> With a flat curve, one near-perfect score means almost no curve for anyone. Some teachers use the second-highest score instead.</li>
  <li><strong>Cap at 100 when adding points.</strong> Adding 8 points to a 96 gives 104. Turn on the cap unless you deliberately allow extra credit.</li>
  <li><strong>A bell curve can lower scores.</strong> If the target mean is below the current mean, or the target SD is smaller, some students go down. Double-check before posting grades.</li>
  <li><strong>Tell students the method.</strong> A curve is easier to accept when everyone knows the rule in advance.</li>
  <li><strong>Look at the full picture.</strong> Run the scores through the <a href="/class-average-calculator">class average calculator</a> to see the median, spread, and grade distribution before deciding whether a curve is needed.</li>
</ul>
HTML,
  'faqs'        => [
    ['How do you curve a test so the highest score is 100?', 'Subtract the highest score from 100 and add the difference to every student. If the top score is 88, everyone gets 12 extra points. This is called a flat curve.'],
    ['What is a square-root curve?', 'A square-root curve replaces each score with 10 times its square root. A 64 becomes 80, an 81 becomes 90, and 100 stays 100, so lower scores get the biggest boost.'],
    ['How do I curve grades to a specific class average?', 'Subtract the current average from the target average and add that number to every score. The new class average will equal your target.'],
    ['What does curving on a bell curve mean?', 'It rescales scores so the class has a chosen mean and standard deviation. Each student keeps the same relative position, but the center and spread of the scores change.'],
    ['Can curving lower a student\'s grade?', 'Methods that only add points cannot. A bell curve can, if you pick a target mean below the current mean or a smaller standard deviation.'],
    ['Should curved scores be capped at 100?', 'Usually, yes. Most teachers cap curved scores at 100 so no one ends up above a perfect score. The calculator has an option to cap.'],
  ],
];
