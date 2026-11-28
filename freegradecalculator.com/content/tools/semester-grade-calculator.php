<?php
return [
  'h1'          => 'Semester Grade Calculator',
  'meta_title'  => 'Semester Grade Calculator – Quarters + Final Exam',
  'description' => 'Free semester grade calculator: combine quarter 1, quarter 2 and final exam grades with custom weights, or find the final exam score you need for a target.',
  'lead'        => 'Combine your two quarter grades and your final exam into a semester grade, or find the final exam score you need.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the semester grade calculator</h2>
<p>Many high schools build a semester grade from two quarter grades plus a semester final exam. This semester grade calculator has two modes: one calculates your semester grade, the other works backward to the final exam score you need.</p>
<h3>Mode 1: Calculate your semester grade</h3>
<ol class="steps">
  <li><strong>Enter your quarter 1 grade.</strong> Use the percentage from your report card or portal.</li>
  <li><strong>Enter your quarter 2 grade.</strong> Same as above.</li>
  <li><strong>Enter your final exam grade.</strong> Your score on the semester exam.</li>
  <li><strong>Check the weights.</strong> The default is 40% / 40% / 20%. Change them to match your school, for example 45 / 45 / 10.</li>
  <li><strong>Read the result.</strong> You'll get your semester grade as a percentage and a letter grade.</li>
</ol>
<h3>Mode 2: Find the final exam score you need</h3>
<p>Switch modes, enter your two quarter grades, the weights, and the semester grade you're aiming for. The calculator tells you the score you need on the final.</p>

<h2 id="formula">The semester grade formula</h2>
<div class="formula">Semester grade = Q1 × w₁ + Q2 × w₂ + Final × w₃</div>
<p>The weights are decimals that add to 1 (40% = 0.40). For the score needed on the final, the formula is rearranged:</p>
<div class="formula">Final needed = (Target − Q1 × w₁ − Q2 × w₂) ÷ w₃</div>

<div class="example-box"><h4>Worked example: semester grade</h4>
<p>Quarter 1: 88. Quarter 2: 82. Final exam: 75. Weights 40 / 40 / 20.</p>
<p>88 × 0.40 = 35.2<br>82 × 0.40 = 32.8<br>75 × 0.20 = 15.0</p>
<p>35.2 + 32.8 + 15.0 = <strong>83%</strong>, a <strong>B</strong>.</p>
</div>

<div class="example-box"><h4>Worked example: final exam needed</h4>
<p>Same quarter grades (88 and 82), same weights, and you want an 85 for the semester.</p>
<p>(85 − 35.2 − 32.8) ÷ 0.20 = 17 ÷ 0.20 = <strong>85</strong></p>
<p>You need an 85 on the final exam to finish the semester with an 85.</p>
</div>

<h2 id="weights-vary">Semester weights vary by school</h2>
<p>There's no national standard. Common splits include:</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Q1</th><th>Q2</th><th>Final exam</th><th>Where you might see it</th></tr></thead><tbody>
<tr><td>40%</td><td>40%</td><td>20%</td><td>A common high school default</td></tr>
<tr><td>45%</td><td>45%</td><td>10%</td><td>Schools with lighter exams</td></tr>
<tr><td>37.5%</td><td>37.5%</td><td>25%</td><td>Schools with heavier exams</td></tr>
<tr><td>50%</td><td>50%</td><td>0%</td><td>Exam-exempt students or classes</td></tr>
</tbody></table></div>
<p>Your student handbook or course syllabus will list the exact split. If you're not sure, ask your teacher before exam week.</p>

<h2 id="year-end-grade">From semester grades to a year-end grade</h2>
<p>For year-long courses, some schools record each semester grade separately on the transcript, while others average the two into one final course grade. If yours averages them equally, the math is simple.</p>
<div class="example-box"><h4>Example</h4>
<p>Semester 1: 83. Semester 2: 87. Equal weight: (83 + 87) ÷ 2 = <strong>85</strong>, a B.</p>
</div>
<p>Because the year-end grade depends on both semesters, a weak fall semester can still be balanced by a strong spring. Ask your counselor how your school records year-long classes, since it affects how your GPA is calculated too.</p>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Using letter grades instead of percentages.</strong> A "B" could be anywhere from 83 to 86. Use the actual percentage from each quarter for an accurate result.</li>
  <li><strong>Weights that don't add to 100.</strong> Make sure your three weights total 100%, or the result won't mean much.</li>
  <li><strong>Confusing semester and final grades.</strong> Some schools average two semesters into a year-end final grade. That's a separate step after this one.</li>
  <li><strong>Forgetting the cap.</strong> If the calculator says you need more than 100 on the final, the target isn't reachable on the exam alone.</li>
</ul>

<h2 id="related">Related calculators</h2>
<p>If your class uses one overall grade plus a final instead of quarters, the <a href="/final-grade-calculator">final grade calculator</a> is a simpler fit. And once you have semester grades for every class, the <a href="/high-school-gpa-calculator">high school GPA calculator</a> turns them into weighted and unweighted GPAs.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Because each quarter usually counts twice as much as the final, a strong second quarter often matters more than cramming for the exam. Run the numbers mid-quarter while there's still time to act.</p></div>
HTML,
  'faqs'        => [
    ["How is a semester grade calculated?", "Usually as a weighted average of quarter 1, quarter 2, and the semester final. With 40/40/20 weights, grades of 88, 82, and 75 give 35.2 + 32.8 + 15 = 83%."],
    ["What do I need on my semester final?", "Switch to the second mode and enter your quarter grades, weights, and target semester grade. The calculator uses (target − Q1 × w1 − Q2 × w2) ÷ w3."],
    ["Can I change the 40/40/20 weights?", "Yes. The weights are editable, so you can enter 45/45/10, 37.5/37.5/25, or whatever your school uses."],
    ["How much does a semester exam affect my grade?", "With a 20% weight, every 10 points on the exam moves your semester grade by 2 points. With a 10% weight, it moves by 1 point."],
    ["Does this work for trimesters?", "It's built for two quarters plus a final. For other setups, the weighted grade calculator lets you add as many weighted rows as you need."],
  ],
];
