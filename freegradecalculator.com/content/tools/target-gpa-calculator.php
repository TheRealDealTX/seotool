<?php
return [
  'h1'          => 'Target GPA Calculator',
  'meta_title'  => 'Target GPA Calculator – What GPA Do I Need?',
  'description' => 'Free target GPA calculator: enter your current GPA, credits completed, goal GPA and remaining credits to find the GPA you need to reach your target GPA.',
  'lead'        => 'Find the GPA you need on your remaining or next-term credits to reach your target cumulative GPA.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the target GPA calculator</h2>
<p>Whether you're chasing a 3.0 for a scholarship, a 3.5 for honors, or a minimum GPA for a major, this target GPA calculator works backward from your goal. It tells you the GPA you need on the credits you have left.</p>
<ol class="steps">
  <li><strong>Enter your current GPA.</strong> Your cumulative GPA from your transcript or portal.</li>
  <li><strong>Enter credits completed.</strong> The graded credits behind that GPA.</li>
  <li><strong>Enter your target GPA.</strong> The cumulative GPA you want to reach.</li>
  <li><strong>Enter remaining credits.</strong> Use all the credits left until graduation, or just next term's credits to see what one semester can do.</li>
  <li><strong>Read the result.</strong> You'll see the GPA you need on those credits. If it's above 4.0, the calculator tells you the target isn't reachable with those credits.</li>
</ol>

<h2 id="formula">The target GPA formula</h2>
<p>Your target cumulative GPA times your total credits gives the quality points you need. Subtract what you've already earned, then divide by the remaining credits.</p>
<div class="formula">Needed GPA = (Target × (Completed + Remaining) − Current × Completed) ÷ Remaining</div>

<div class="example-box"><h4>Worked example</h4>
<p>You have a 3.0 GPA over 60 credits and want to graduate with a 3.3. You have 30 credits left.</p>
<p>Quality points needed: 3.3 × (60 + 30) = 3.3 × 90 = 297<br>Quality points earned: 3.0 × 60 = 180<br>Quality points still needed: 297 − 180 = 117</p>
<p>Needed GPA: 117 ÷ 30 = <strong>3.90</strong></p>
<p>That's mostly A's and A-'s for your remaining credits. Tough, but reachable.</p>
</div>

<div class="example-box"><h4>Example: a target that's out of reach</h4>
<p>Same student (3.0 over 60 credits), but aiming for a 3.5 after just one more 15-credit semester.</p>
<p>(3.5 × 75 − 180) ÷ 15 = (262.5 − 180) ÷ 15 = 82.5 ÷ 15 = <strong>5.50</strong></p>
<p>That's above 4.0, so it isn't reachable in one semester. Even a perfect 4.0 would bring the cumulative GPA to (180 + 60) ÷ 75 = 3.20.</p>
</div>

<div class="example-box"><h4>Example: a one-semester goal</h4>
<p>Instead of a long-term target, the same student sets a short-term goal: a 3.1 cumulative GPA after next term's 15 credits.</p>
<p>(3.1 × 75 − 180) ÷ 15 = (232.5 − 180) ÷ 15 = 52.5 ÷ 15 = <strong>3.50</strong></p>
<p>A 3.5 semester is a realistic stepping stone. Hitting it, then repeating it, keeps the long-term 3.3 goal within reach.</p>
</div>

<h2 id="reading-results">What your result means</h2>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Needed GPA</th><th>What it roughly means</th></tr></thead><tbody>
<tr><td>Below your current GPA</td><td>You're on track. Keep it steady.</td></tr>
<tr><td>Up to about 3.0</td><td>A B average on remaining credits</td></tr>
<tr><td>3.3 to 3.7</td><td>Mostly B+ and A- grades</td></tr>
<tr><td>3.7 to 4.0</td><td>Mostly A's, very little room for error</td></tr>
<tr><td>Above 4.0</td><td>Not reachable with these credits on a 4.0 scale</td></tr>
</tbody></table></div>

<h2 id="tips">Tips for reaching a GPA goal</h2>
<ul>
  <li><strong>Start early.</strong> The fewer credits you've completed, the more each new grade moves your GPA. A target that's impossible senior year may be easy sophomore year.</li>
  <li><strong>Set milestones.</strong> Run the calculator with only next term's credits to set a semester goal, then again with all remaining credits for the big picture.</li>
  <li><strong>Check retake policies.</strong> Some schools replace a failed grade when you retake the course, which can raise your GPA faster than new credits alone.</li>
  <li><strong>Balance your schedule.</strong> Pairing a demanding course with ones you're confident in makes a high term GPA more realistic.</li>
</ul>
<p>Read <a href="/blog/how-to-raise-your-gpa">how to raise your GPA</a> for more strategies, and see <a href="/blog/what-is-a-good-gpa">what is a good GPA</a> if you're still choosing a goal.</p>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Using total credits instead of GPA credits.</strong> Pass/fail and transfer credits often don't count toward GPA.</li>
  <li><strong>Mixing weighted and unweighted GPAs.</strong> This calculator flags anything above 4.0 as unreachable, so use an unweighted GPA.</li>
  <li><strong>Forgetting graduation credit totals.</strong> Remaining credits should be what's actually left, not a guess. Your degree audit or academic advisor can confirm the number.</li>
  <li><strong>Treating the result as a guarantee.</strong> The needed GPA assumes every remaining credit is graded. Pass/fail courses, withdrawals, or retakes can change the math, so rerun it whenever your plans change.</li>
</ul>
<p>Once you've finished a term, update your numbers with the <a href="/cumulative-gpa-calculator">cumulative GPA calculator</a> and run your target again.</p>
HTML,
  'faqs'        => [
    ["How do I calculate the GPA I need to reach my goal?", "Multiply your target GPA by your total credits (completed plus remaining), subtract your current GPA times credits completed, and divide by the remaining credits."],
    ["Can I raise my GPA from 3.0 to 3.5 in one semester?", "It depends on your credits. With 60 credits at 3.0 and 15 more credits, you'd need a 5.5, which isn't possible. With fewer completed credits, it may be."],
    ["What does it mean if the needed GPA is above 4.0?", "Your target can't be reached with the credits you entered on a 4.0 scale. Try more remaining credits or a lower target."],
    ["Should I enter credits for next term or until graduation?", "Either works. Next term's credits shows what one semester needs; credits until graduation shows the long-term average you need."],
    ["Does this work for high school GPA?", "Yes, if you use an unweighted 4.0 GPA and the credit system your high school uses. Weighted GPAs above 4.0 aren't supported by the reachability check."],
  ],
];
