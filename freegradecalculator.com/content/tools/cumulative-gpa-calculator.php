<?php
return [
  'h1'          => 'Cumulative GPA Calculator',
  'meta_title'  => 'Cumulative GPA Calculator – Combine Terms & Credits',
  'description' => 'Free cumulative GPA calculator: start with your current GPA and credits, add one or more terms, and see your new cumulative GPA and total credits instantly.',
  'lead'        => 'Combine your current cumulative GPA with one or more new terms to see your updated overall GPA and total credits.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the cumulative GPA calculator</h2>
<p>Your cumulative GPA is the average of every graded credit you've taken, not just this semester. This cumulative GPA calculator combines what you have so far with any number of new terms.</p>
<ol class="steps">
  <li><strong>Enter your current cumulative GPA.</strong> You'll find it on your transcript or student portal.</li>
  <li><strong>Enter the credits earned.</strong> The total graded credits behind that GPA. (Credits from pass/fail or transfer courses often aren't included, so use the GPA credits figure if your transcript lists one.)</li>
  <li><strong>Add a term.</strong> Enter the term GPA and the credits for that term.</li>
  <li><strong>Add more terms if needed.</strong> Combine a fall and spring semester, or project the next two years.</li>
  <li><strong>Read the results.</strong> You'll see your new cumulative GPA and total credits.</li>
</ol>

<h2 id="formula">The cumulative GPA formula</h2>
<p>Each GPA is weighted by the credits behind it. Multiply each GPA by its credits to get quality points, add them, and divide by total credits.</p>
<div class="formula">Cumulative GPA = Σ (GPA × credits) ÷ Σ credits</div>

<div class="example-box"><h4>Worked example</h4>
<p>You have a 3.10 cumulative GPA over 60 credits. Then you finish two more semesters: a 3.60 over 15 credits and a 3.40 over 16 credits.</p>
<p>Current: 3.10 × 60 = 186.0<br>Fall: 3.60 × 15 = 54.0<br>Spring: 3.40 × 16 = 54.4</p>
<p>Total quality points: 186.0 + 54.0 + 54.4 = 294.4<br>Total credits: 60 + 15 + 16 = 91</p>
<p>New cumulative GPA: 294.4 ÷ 91 = <strong>3.24</strong></p>
</div>

<h2 id="why-not-average">Why you can't just average your GPAs</h2>
<p>Averaging 3.10, 3.60, and 3.40 gives 3.37, which is wrong. That treats a 15-credit semester the same as the 60 credits behind your existing GPA. Because your current GPA represents four times as many credits as one new term, it carries four times the weight.</p>
<p>This is also why a cumulative GPA moves slowly. Two strong semesters above raised the GPA by about 0.14, not 0.4.</p>

<h2 id="term-vs-cumulative">Term GPA vs. cumulative GPA</h2>
<div class="compare">
  <div class="compare-col"><h4>Term GPA</h4><ul><li>One semester or quarter</li><li>Can swing a lot term to term</li><li>Used for dean's list, probation</li></ul></div>
  <div class="compare-col"><h4>Cumulative GPA</h4><ul><li>Every graded credit so far</li><li>Changes gradually</li><li>Used for graduation honors, transcripts, applications</li></ul></div>
</div>
<p>Need your term GPA first? Calculate it course by course with the <a href="/gpa-calculator">GPA calculator</a>, then bring the result here. For a step-by-step explanation with more examples, see <a href="/blog/how-to-calculate-cumulative-gpa">how to calculate cumulative GPA</a>.</p>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Using total credits instead of GPA credits.</strong> If you have pass/fail or transfer credits, your transcript may list two credit totals. Use the one that counts toward GPA.</li>
  <li><strong>Rounding too early.</strong> Use your GPA to two or three decimals. Rounding 3.146 down to 3.1 over 60 credits can shift the result.</li>
  <li><strong>Forgetting repeated courses.</strong> If your school replaces a retaken grade, the old credits come out of the total. Your registrar's policy decides this.</li>
  <li><strong>Mixing scales.</strong> Combine only GPAs on the same scale. Don't mix a weighted high school GPA with an unweighted one.</li>
</ul>

<h2 id="planning">Use it to plan ahead</h2>
<p>Enter a projected GPA for future terms to see where you'll end up. Continuing the example, if the student adds 30 more credits at a 3.50, the new cumulative GPA would be (294.4 + 105.0) ÷ 121 = 399.4 ÷ 121 = <strong>3.30</strong>. Two more solid semesters bring the GPA up to a 3.3, a common cutoff for honors programs and scholarships at many schools.</p>
<p>Running a few projections like this (an optimistic one, a realistic one, and a cautious one) shows the range you can expect by graduation. Want to work backward from a goal instead? The <a href="/target-gpa-calculator">target GPA calculator</a> tells you the GPA you need on your remaining credits.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>The more credits you've completed, the harder your GPA is to move. If you're aiming for a cutoff like 3.0 or 3.5, act early. One great semester freshman year does more than one great semester senior year.</p></div>
HTML,
  'faqs'        => [
    ["How do I calculate cumulative GPA?", "Multiply each GPA by its credits, add those quality points together, and divide by the total credits. A 3.10 over 60 credits plus a 3.60 over 15 and a 3.40 over 16 gives 294.4 ÷ 91 = 3.24."],
    ["Can I just average my semester GPAs?", "Only if every semester has the same number of credits. Otherwise you must weight each GPA by its credits, or the result will be off."],
    ["Can I add more than one term?", "Yes. Add as many terms as you need, each with its own GPA and credits. The calculator combines them all with your current cumulative GPA."],
    ["How fast can I raise my cumulative GPA?", "It depends on how many credits you already have. With 60 credits at 3.10, a 3.60 semester of 15 credits raises your cumulative GPA to 3.20."],
    ["Where do I find my current cumulative GPA and credits?", "Your unofficial transcript or student portal lists both. Use the credits that count toward GPA, which may differ from total credits earned."],
  ],
];
