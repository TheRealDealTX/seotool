<?php
return [
  'h1'          => 'High School GPA Calculator',
  'meta_title'  => 'High School GPA Calculator – Weighted & Unweighted',
  'description' => 'Free high school GPA calculator: enter grades, credits and course level (Regular, Honors, AP/IB) to see your weighted and unweighted GPA side by side.',
  'lead'        => 'Enter your classes, grades, credits, and course level to see your weighted and unweighted high school GPA at the same time.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the high school GPA calculator</h2>
<p>High school transcripts often show two GPAs: unweighted, on a plain 4.0 scale, and weighted, with extra points for harder classes. This high school GPA calculator shows both at once, so you can see exactly what your Honors and AP classes add.</p>
<ol class="steps">
  <li><strong>Add a row for each class.</strong> Include every class that counts toward your GPA.</li>
  <li><strong>Choose your letter grade.</strong> Use the final grade for the semester or year.</li>
  <li><strong>Enter the credits.</strong> Many schools give 1 credit for a year-long class and 0.5 for a semester class. Check your transcript.</li>
  <li><strong>Select the course type.</strong> Regular, Honors, or AP/IB.</li>
  <li><strong>Read your results.</strong> You'll see your unweighted GPA and your weighted GPA.</li>
</ol>

<h2 id="formula">How weighted and unweighted GPA are calculated</h2>
<p>Both use the same credit-weighted average. The only difference is the point value of each grade.</p>
<div class="formula">GPA = Σ (grade points × credits) ÷ Σ credits</div>
<div class="compare">
  <div class="compare-col"><h4>Unweighted</h4><ul><li>A = 4.0, B = 3.0, C = 2.0</li><li>Course level doesn't matter</li><li>Maximum 4.0</li></ul></div>
  <div class="compare-col"><h4>Weighted</h4><ul><li>Honors: +0.5</li><li>AP / IB: +1.0</li><li>F gets no boost (stays 0)</li></ul></div>
</div>
<p>So an A in an AP class is 4.0 unweighted and 5.0 weighted. A B in an Honors class is 3.0 unweighted and 3.5 weighted.</p>

<div class="example-box"><h4>Worked example</h4>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Class</th><th>Type</th><th>Grade</th><th>Unweighted</th><th>Weighted</th></tr></thead><tbody>
<tr><td>English 11</td><td>Honors</td><td>A</td><td>4.0</td><td>4.5</td></tr>
<tr><td>Biology</td><td>AP</td><td>B</td><td>3.0</td><td>4.0</td></tr>
<tr><td>Algebra II</td><td>Regular</td><td>A-</td><td>3.7</td><td>3.7</td></tr>
<tr><td>US History</td><td>AP</td><td>B+</td><td>3.3</td><td>4.3</td></tr>
<tr><td>Spanish III</td><td>Regular</td><td>B</td><td>3.0</td><td>3.0</td></tr>
</tbody></table></div>
<p>All classes are 1 credit. Unweighted: 17.0 ÷ 5 = <strong>3.40</strong>. Weighted: 19.5 ÷ 5 = <strong>3.90</strong>.</p>
<p>The two AP classes and one Honors class add half a point to this student's GPA.</p>
</div>

<h2 id="half-credit">Example: adding a half-credit class</h2>
<p>Semester-long classes such as health or an elective often carry 0.5 credits, so they count half as much as a full-year class. Add a regular Health class with an A (0.5 credit) to the example above:</p>
<p>Unweighted: (17.0 + 4.0 × 0.5) ÷ 5.5 = 19.0 ÷ 5.5 = <strong>3.45</strong><br>Weighted: (19.5 + 4.0 × 0.5) ÷ 5.5 = 21.5 ÷ 5.5 = <strong>3.91</strong></p>
<p>The A lifted the unweighted GPA but barely moved the weighted one, because a regular A (4.0) is only slightly above the weighted average of 3.90. If you entered that class as 1 credit by mistake, you'd overstate its effect, which is why the credits column matters.</p>

<h2 id="schools-vary">Weighting rules vary by school</h2>
<p>There's no single national rule for weighted GPA. The +0.5 Honors and +1.0 AP/IB system is common, but your school might:</p>
<ul>
  <li>Give the same boost to Honors and AP classes.</li>
  <li>Weight only grades of C or higher.</li>
  <li>Exclude PE, health, or electives from GPA.</li>
  <li>Use a 100-point or 5.0-based scale instead.</li>
</ul>
<p>Your school counselor or student handbook will have the official method. Use this calculator as a close estimate and to compare scenarios.</p>

<h2 id="colleges">How colleges look at your GPA</h2>
<p>Colleges see the GPA on your transcript, but many also recalculate it their own way, often using only core academic classes. That's one reason both numbers matter. A strong unweighted GPA shows consistent grades; a high weighted GPA shows you took on challenging courses. Our guide to <a href="/blog/weighted-vs-unweighted-gpa">weighted vs. unweighted GPA</a> covers this in detail, and <a href="/blog/what-is-a-good-gpa">what is a good GPA</a> puts your number in context.</p>

<h2 id="tips">Tips</h2>
<ul>
  <li><strong>Use credits, not class count.</strong> A semester class at 0.5 credits counts half as much as a year-long class.</li>
  <li><strong>Don't overload for weight alone.</strong> A C in AP (3.0 weighted) is worth less than an A in Honors (4.5 weighted) and drags down your unweighted GPA.</li>
  <li><strong>Watch your unweighted GPA too.</strong> Weighted GPAs above 4.0 look impressive, but the unweighted number is what many scholarship forms and some college applications ask for. Keep both in view when you plan next year's schedule.</li>
  <li><strong>Enter final grades, not progress grades.</strong> Your GPA uses the grade recorded on your transcript, usually the semester or year-end grade, not a mid-quarter progress report.</li>
  <li><strong>Track it each semester.</strong> To combine terms over four years, use the <a href="/cumulative-gpa-calculator">cumulative GPA calculator</a>.</li>
</ul>
HTML,
  'faqs'        => [
    ["What is the difference between weighted and unweighted GPA?", "Unweighted GPA uses a 4.0 scale for every class. Weighted GPA adds points for harder classes: in this calculator, +0.5 for Honors and +1.0 for AP or IB."],
    ["Is an A in an AP class a 5.0?", "On the weighting used here, yes: an A (4.0) plus the 1.0 AP boost equals 5.0 weighted. It's still a 4.0 unweighted."],
    ["Does an F get the AP or Honors boost?", "No. An F stays 0.0 in both weighted and unweighted GPA."],
    ["How many credits is a high school class?", "Many schools give 1 credit for a year-long class and 0.5 for a one-semester class, but this varies. Your transcript lists the credits for each course."],
    ["Do colleges use weighted or unweighted GPA?", "Both appear on transcripts, and many colleges recalculate GPA using their own rules, often focusing on core academic classes."],
    ["What if my school weights classes differently?", "Weighting rules vary by school. Use this calculator as an estimate and check your student handbook or counselor for your official GPA."],
  ],
];
