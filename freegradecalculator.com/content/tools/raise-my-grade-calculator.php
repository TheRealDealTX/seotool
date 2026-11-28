<?php
return [
  'h1'          => 'Raise My Grade Calculator',
  'meta_title'  => 'Raise My Grade Calculator – What Do I Need to Score?',
  'description' => 'Free raise my grade calculator: enter points earned, points possible and points still to come to see the average you need to raise your grade to your target.',
  'lead'        => 'Find the average you need on your remaining assignments to raise your grade to your target, plus your best and worst possible final grade.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the raise my grade calculator</h2>
<p>"Can I still get a B in this class?" This raise my grade calculator answers that for classes graded on total points. It looks at what you've earned, what's left, and tells you the average you need from here on.</p>
<ol class="steps">
  <li><strong>Enter points earned so far.</strong> Add up the points on everything graded, or copy the total from your school portal.</li>
  <li><strong>Enter points possible so far.</strong> The maximum points on that same graded work.</li>
  <li><strong>Enter points still to come.</strong> The total points for the rest of the term: remaining homework, tests, projects, and the final.</li>
  <li><strong>Enter your target percentage.</strong> For example, 80 for a B- or 90 for an A-.</li>
  <li><strong>Read the results.</strong> You'll see the average percentage you need on the remaining work, plus the highest and lowest final grade still possible.</li>
</ol>

<h2 id="formula">The formula</h2>
<p>Your final grade will be all points earned divided by all points in the course. Solving for the points you still need gives:</p>
<div class="formula">Needed % = (Target × (Possible so far + Remaining) − Earned so far) ÷ Remaining</div>
<p>The range of outcomes comes from two extremes:</p>
<div class="formula">Highest possible = (Earned + Remaining) ÷ (Possible + Remaining)<br>Lowest possible = Earned ÷ (Possible + Remaining)</div>

<div class="example-box"><h4>Worked example</h4>
<p>You've earned 340 out of 425 points so far (80%). There are 200 points left in the term, and you want an 85%.</p>
<p>Total course points: 425 + 200 = 625<br>Points needed for 85%: 0.85 × 625 = 531.25<br>Points still needed: 531.25 − 340 = 191.25<br>Average needed: 191.25 ÷ 200 = <strong>95.6%</strong></p>
<p>Highest possible grade: (340 + 200) ÷ 625 = <strong>86.4%</strong>. Lowest possible: 340 ÷ 625 = <strong>54.4%</strong>.</p>
<p>An 85 is still reachable, but it takes near-perfect work. An 82, on the other hand, would need (0.82 × 625 − 340) ÷ 200 = 86.3%, a much more realistic target.</p>
</div>

<h2 id="reading-results">How to read your results</h2>
<ul>
  <li><strong>Needed average over 100%:</strong> The target can't be reached without extra credit. Compare it with the highest possible grade to find a realistic goal.</li>
  <li><strong>Needed average under your current average:</strong> You're on track. Keep doing what you're doing.</li>
  <li><strong>The lowest possible grade:</strong> This is what happens if you earn zero on everything left. It shows how much is still at stake.</li>
</ul>

<h2 id="why-it-gets-harder">Why raising a grade gets harder late in the term</h2>
<p>Early in a term, few points have been graded, so each new assignment moves your grade a lot. By the last few weeks, most points are locked in. In the example above, the remaining 200 points are only 32% of the course, so even a perfect score lifts the grade from 80% to just 86.4%.</p>
<p>Compare that with midterm. If the same student had earned 170 out of 212 points (about 80%) with 413 points still to come, the needed average for an 85% would be (0.85 × 625 − 170) ÷ 413 = 87.5%, far more manageable than 95.6%.</p>
<p>That's why it pays to check your grade early. Running this calculator early, when most of the points are still ahead, gives you far more room to move.</p>

<h2 id="tips">Tips to raise your grade</h2>
<ul>
  <li><strong>Find the big-point items.</strong> One 100-point test matters more than five 10-point worksheets.</li>
  <li><strong>Turn in every assignment.</strong> A zero hurts far more than a mediocre score. Even half credit on a missing assignment adds points.</li>
  <li><strong>Ask about retakes and extra credit.</strong> Policies vary by teacher, so ask early.</li>
  <li><strong>Check for grading errors.</strong> Compare your returned work with the portal.</li>
</ul>
<p>For more strategies, read <a href="/blog/how-to-raise-your-gpa">how to raise your GPA</a>. If your class uses weighted categories instead of points, the <a href="/final-grade-calculator">final grade calculator</a> is the better tool for planning your exam score.</p>
<div class="callout callout-warn"><strong>Points classes only</strong><p>This calculator assumes your grade is total points earned divided by total points possible. In a weighted class (for example, Tests 50%, Homework 20%), the math is different.</p></div>
HTML,
  'faqs'        => [
    ["How do I figure out what I need to raise my grade?", "Multiply your target percentage by the total course points (graded plus remaining), subtract the points you've already earned, and divide by the remaining points. That's the average you need on everything left."],
    ["What is the highest grade I can still get?", "Add all remaining points to what you've earned and divide by the total course points. In the example, (340 + 200) ÷ 625 = 86.4%."],
    ["Can I raise my grade from a C to a B?", "It depends on how many points are left. Enter your numbers: if the needed average is 100% or less, it's possible. The earlier in the term, the easier it is."],
    ["Why does my grade barely move after a good test?", "Late in the term, most points are already counted, so each new assignment is a small share of the total. A 100% on a 50-point quiz barely moves a 1,000-point course."],
    ["Does this work for weighted classes?", "No. It assumes a total-points system. For weighted classes, use the weighted grade calculator or the final grade calculator."],
  ],
];
