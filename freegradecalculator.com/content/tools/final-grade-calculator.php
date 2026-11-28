<?php
return [
  'h1'          => 'Final Grade Calculator',
  'meta_title'  => 'Final Grade Calculator – What Do I Need on My Final?',
  'description' => 'Free final grade calculator: enter your current grade, the grade you want, and the final exam weight to see the score you need on your final for an A, B or C.',
  'lead'        => 'Find out exactly what score you need on your final exam to finish the class with the grade you want.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the final grade calculator</h2>
<p>This final grade calculator answers one question: what do I need on my final? It works for any class where the final exam counts as a set percentage of your overall grade.</p>
<ol class="steps">
  <li><strong>Enter your current grade.</strong> Use your grade in the class right now, before the final. Type a percentage like 84 or a letter like B.</li>
  <li><strong>Enter the grade you want.</strong> This is your target for the whole class, such as 90 or A-.</li>
  <li><strong>Enter the final exam weight.</strong> Your syllabus will say something like "Final exam: 20% of course grade." Enter 20.</li>
  <li><strong>Read the result.</strong> You'll see the score you need on the final, plus a table showing what you'd need for an A (90), B (80), C (70), and D (60).</li>
</ol>

<h2 id="formula">The final exam grade formula</h2>
<p>Your course grade after the final is a blend of your current grade and your final exam score. Solving that blend for the final score gives this formula:</p>
<div class="formula">Required final score = (Desired grade − Current grade × (1 − w)) ÷ w</div>
<p>Here <em>w</em> is the final exam weight written as a decimal, so 20% becomes 0.20. The calculator handles the conversion for you.</p>

<div class="example-box"><h4>Worked example</h4>
<p>You have an 84% in the class, your final is worth 20%, and you want at least an 80% (a B-).</p>
<p>Current grade × (1 − 0.20) = 84 × 0.80 = 67.2</p>
<p>(80 − 67.2) ÷ 0.20 = 12.8 ÷ 0.20 = <strong>64%</strong></p>
<p>You need a 64 on the final to keep a B-. The table would also show you need 114 for a 90 (not possible without extra credit), 14 for a 70, and that a 60 is already locked in.</p>
</div>

<h2 id="reading-results">Interpreting your result</h2>
<ul>
  <li><strong>Over 100%:</strong> Your target isn't reachable on the final alone unless your teacher offers extra credit. Look at the next grade down in the table.</li>
  <li><strong>Between 0 and 100%:</strong> That's your goal score. Add a few points of margin, since a rounding policy or a late-posted assignment can shift things.</li>
  <li><strong>Below 0%:</strong> You've already secured that grade, even with a zero on the final. (Some teachers require you to take or pass the final regardless, so check your syllabus.)</li>
</ul>

<h2 id="final-test-score">Using it as a final test score calculator</h2>
<p>The same math works for any single heavily weighted assessment: a unit test worth 25%, a final project worth 30%, or a cumulative exam at the end of a semester. As long as you know the weight and your grade before it, this works as a final test score calculator too.</p>
<p>If your class is split into quarters and a semester exam, the <a href="/semester-grade-calculator">semester grade calculator</a> handles the quarter 1, quarter 2, and final exam weights separately.</p>

<h2 id="common-mistakes">Common mistakes when calculating finals</h2>
<ul>
  <li><strong>Using the wrong current grade.</strong> Your current grade should not include the final. If your portal already shows a placeholder zero for the final, your real current grade is higher than displayed.</li>
  <li><strong>Mixing up course weight and points.</strong> If your class uses total points instead of percentage weights, the final's weight is its points divided by all points in the course. For points-based classes, a points-based "what do I need" tool such as our raise my grade calculator is a better fit.</li>
  <li><strong>Ignoring category weights.</strong> If the final sits inside a "Tests" category rather than standing alone, its true weight is smaller than the category's weight.</li>
  <li><strong>Assuming letter cutoffs.</strong> The A/B/C/D table uses 90/80/70/60. Many schools use those cutoffs, but some use 93 for an A or a 7-point scale.</li>
</ul>

<h2 id="free-grading-calculator">A free online grading calculator for students and teachers</h2>
<p>Think of this page as a grading calculator for finals. Students use it to plan study time before exam week. Teachers use it as a quick grading book calculator to answer the inevitable "what do I need on the final?" question without opening a spreadsheet. It's free, needs no account, and runs in your browser.</p>
<p>Need to score the exam itself once it's turned in? A final exam grader like the <a href="/test-grade-calculator">test grade calculator</a> turns the number of questions missed into a percentage and letter grade.</p>
<p>For a full walkthrough of how teachers combine categories and finals, read <a href="/blog/how-to-calculate-your-final-grade">how to calculate your final grade</a>.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Run the calculator twice: once for the grade you want and once for the grade you can't fall below. The gap between those two scores tells you how much room for error you have going into the exam.</p></div>
HTML,
  'faqs'        => [
    ["What do I need on my final to get an A?", "Enter your current grade, 90 as the desired grade, and the final exam weight. The calculator uses required = (90 − current × (1 − w)) ÷ w and also shows the A row in its results table."],
    ["How is a final grade calculated?", "Your course grade equals your current grade times (1 − final weight) plus your final exam score times the final weight. For example, 84 × 0.80 + 64 × 0.20 = 80."],
    ["What if the calculator says I need more than 100%?", "Your target can't be reached with the final exam alone. Unless your teacher offers extra credit or drops a low score, aim for the next grade down."],
    ["Can I enter letter grades?", "Yes. Both your current grade and your desired grade can be entered as a percentage or a letter grade."],
    ["Does this work as a final exam grader for teachers?", "Teachers can use it to tell students what they need on the final. To grade the exam itself, the test grade calculator or the EZ grader turns number wrong into a percentage."],
    ["What if my final exam is worth points instead of a percentage?", "Divide the final's points by the total points in the course to get its weight. For example, a 200-point final in a 1,000-point course has a 20% weight."],
  ],
];
