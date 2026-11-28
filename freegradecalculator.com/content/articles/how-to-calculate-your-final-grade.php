<?php
return [
  'slug'        => 'how-to-calculate-your-final-grade',
  'title'       => 'How to Calculate Final Grades (Formulas, Percentages & Examples)',
  'meta_title'  => 'How to Calculate Final Grades: Formula + Examples',
  'description' => 'Learn how to calculate final grades with percentages, points, and weighted categories, how teachers calculate grades, and what you need on your final.',
  'keyword'     => 'how to calculate final grades',
  'category'    => 'Grades',
  'date'        => '2025-10-06',
  'updated'     => '2026-11-22',
  'author'      => 'FGC Editorial Team',
  'hero'        => 'exam-answer-sheet',
  'hero_alt'    => 'Student filling in a test answer sheet with a pencil',
  'excerpt'     => 'Points or weighted categories? Here is exactly how final grades are calculated, the formulas teachers use, and how to figure out what you need on your final exam.',
  'related_tools' => ['final-grade-calculator', 'weighted-grade-calculator', 'points-grade-calculator', 'semester-grade-calculator'],
  'faqs'        => [
    ["How do you calculate your final grade in a class?", "If your class uses points, add up all the points you earned, divide by all the points possible, and multiply by 100. If it uses weighted categories, multiply each category average by its weight (as a decimal) and add the results. Your syllabus tells you which system your teacher uses."],
    ["How do you calculate grades with percentages?", "Divide the points you earned by the points possible and multiply by 100. For example, 43 out of 50 is 43 ÷ 50 = 0.86, or 86%. Then compare the percentage to your school's grading scale to get the letter grade."],
    ["How do I calculate what I need on my final exam?", "Use required = (desired grade − current grade × (1 − w)) ÷ w, where w is the final's weight as a decimal. With an 84% current grade, a final worth 25%, and an 80% goal: (80 − 84 × 0.75) ÷ 0.25 = 68%."],
    ["Can I just average my assignment percentages?", "Only if every assignment is worth the same number of points and your class does not use weighted categories. Otherwise a simple average of percentages gives the wrong answer, because it treats a 10-point quiz the same as a 100-point test."],
    ["Do teachers round final grades?", "Many do, but it depends on the teacher, the school, and the gradebook software. Some round to the nearest whole percent (so 89.5 becomes 90), some never round, and some use their judgment for borderline grades. Check your syllabus or ask your teacher."],
    ["What if my category weights do not add up to 100%?", "That usually means some categories, often the final exam, have not been graded yet. Divide your weighted total by the sum of the weights you used. For example, 67 points from categories worth 80% total gives 67 ÷ 0.80 = 83.75%."],
  ],
  'body'        => <<<'HTML'
<p class="lead">To calculate final grades, you need to know which system your class uses. In a <strong>points system</strong>, you divide total points earned by total points possible. In a <strong>weighted system</strong>, you multiply each category's average by its weight and add the results. Either way, you end up with a percentage that maps to a letter grade.</p>

<p>This guide walks through how to calculate final grades step by step, with real numbers: calculating grades with percentages, adding grades up in a points system, the weighted formula for grades, how teachers actually calculate grades, and how to figure out what you need on your final exam.</p>

<div class="key-takeaways"><h3>Key takeaways</h3><ul>
<li><strong>Percentage</strong> = points earned ÷ points possible × 100.</li>
<li><strong>Points system:</strong> add all points earned, add all points possible, then divide.</li>
<li><strong>Weighted system:</strong> final grade = Σ (category % × category weight).</li>
<li><strong>Score needed on a final</strong> = (desired − current × (1 − w)) ÷ w.</li>
<li>Averaging percentages directly is the most common mistake. It only works when every item is worth the same.</li>
</ul></div>

<h2 id="how-final-grades-are-calculated">How to calculate final grades: the two systems</h2>

<p>How final grades are calculated depends on your teacher, but almost every US class uses one of two methods, and your syllabus will tell you which one. Look for a list of categories with percentages (weighted) or a total number of points for the course (points-based).</p>

<div class="compare">
<div class="compare-col"><h4>Points-based</h4><ul><li>Every assignment is worth a set number of points</li><li>Bigger assignments are worth more points</li><li>Grade = total earned ÷ total possible</li><li>Easy to track yourself</li></ul></div>
<div class="compare-col"><h4>Weighted categories</h4><ul><li>Assignments are grouped (homework, tests, final)</li><li>Each group has a weight, like 40%</li><li>Grade = Σ (category average × weight)</li><li>Tests and finals usually carry the most weight</li></ul></div>
</div>

<p>Some teachers combine both: points within each category, then weights across categories. That is the most common setup in high school and college gradebooks.</p>

<h2 id="calculating-grades-with-percentages">Calculating grades with percentages</h2>

<p>Every grade calculation starts here. To calculate the percentage for a single assignment, divide what you earned by what was possible, then multiply by 100.</p>

<div class="formula">Percentage = (points earned ÷ points possible) × 100</div>

<div class="example-box"><h4>Worked example: single assignments</h4>
<p>Quiz: 17 out of 20 → 17 ÷ 20 = 0.85 → <strong>85%</strong><br>
Test: 43 out of 50 → 43 ÷ 50 = 0.86 → <strong>86%</strong><br>
Essay: 68 out of 75 → 68 ÷ 75 = 0.9066… → <strong>90.7%</strong></p>
</div>

<p>If you know how many questions you missed rather than how many you got right, subtract first: 25 questions with 4 wrong means 21 right, and 21 ÷ 25 = 84%. The <a href="/test-grade-calculator">test grade calculator</a> does this for you and shows every possible score in a chart.</p>

<p>Once you have a percentage, compare it to your school's grading scale. A common US scale looks like this (schools vary, especially at the edges):</p>

<div class="table-wrap"><table class="data-table"><thead><tr><th>Percentage</th><th>Letter</th><th>Percentage</th><th>Letter</th></tr></thead><tbody>
<tr><td>97–100</td><td>A+</td><td>77–79</td><td>C+</td></tr>
<tr><td>93–96</td><td>A</td><td>73–76</td><td>C</td></tr>
<tr><td>90–92</td><td>A-</td><td>70–72</td><td>C-</td></tr>
<tr><td>87–89</td><td>B+</td><td>67–69</td><td>D+</td></tr>
<tr><td>83–86</td><td>B</td><td>63–66</td><td>D</td></tr>
<tr><td>80–82</td><td>B-</td><td>60–62</td><td>D-</td></tr>
<tr><td colspan="2"></td><td>Below 60</td><td>F</td></tr>
</tbody></table></div>

<h2 id="how-to-add-grades-up">How to add grades up in a points system</h2>

<p>In a points-based class, you do not average percentages. You add up the raw points. This is the simplest way to compute grades, and it is how many teachers set up their gradebooks.</p>

<ol class="steps">
<li><strong>Add the points you earned.</strong> Total every score from every graded assignment.</li>
<li><strong>Add the points possible.</strong> Total the maximum score of the same assignments.</li>
<li><strong>Divide and multiply by 100.</strong> Earned ÷ possible × 100 = your grade.</li>
</ol>

<div class="example-box"><h4>Worked example: points system</h4>
<p>Quiz: 18 / 20<br>
Homework set: 45 / 50<br>
Unit test: 82 / 100<br>
Project: 47 / 50</p>
<p>Points earned = 18 + 45 + 82 + 47 = <strong>192</strong><br>
Points possible = 20 + 50 + 100 + 50 = <strong>220</strong><br>
Grade = 192 ÷ 220 = 0.8727… → <strong>87.3% (B+)</strong></p>
</div>

<div class="callout callout-warn"><strong>Common mistake</strong><p>Those four scores are 90%, 90%, 82%, and 94%. Averaging the percentages gives (90 + 90 + 82 + 94) ÷ 4 = 89.0%, which is too high. The 100-point test should count twice as much as the 50-point items, and the points method handles that automatically.</p></div>

<p>Have a long list of assignments? Paste them into the <a href="/points-grade-calculator">points grade calculator</a> to total everything at once.</p>

<figure class="figure">
  <img src="/assets/img/photos/hand-writing-notebook.webp" width="1200" height="800" alt="Hand writing figures in a spiral notebook" loading="lazy">
  <figcaption>Keeping a running list of points earned and possible makes it easy to know your grade any day of the term.</figcaption>
</figure>

<h2 id="formula-for-grades">The weighted formula for grades</h2>

<p>Most high school and college classes use weighted categories. The calculating grades formula multiplies each category average by its weight and adds them up:</p>

<div class="formula">Final grade = (avg₁ × w₁) + (avg₂ × w₂) + … + (avgₙ × wₙ)</div>

<p>Write each weight as a decimal (40% = 0.40). If the weights add up to 100%, the result is your grade as a percentage.</p>

<div class="example-box"><h4>Worked example: weighted categories</h4>
<p>Homework (20%): 95% → 0.20 × 95 = 19.0<br>
Quizzes (20%): 84% → 0.20 × 84 = 16.8<br>
Tests (40%): 78% → 0.40 × 78 = 31.2<br>
Final exam (20%): 88% → 0.20 × 88 = 17.6</p>
<p>Final grade = 19.0 + 16.8 + 31.2 + 17.6 = <strong>84.6% (B)</strong></p>
</div>

<figure class="illustration">
  <svg viewBox="0 0 640 210" role="img" aria-label="Stacked bar showing contributions to an 84.6 percent final grade: homework 19, quizzes 16.8, tests 31.2, final 17.6">
    <rect x="40" y="70" width="560" height="50" rx="6" fill="var(--surface)" stroke="var(--line)" stroke-width="2"/>
    <rect x="40" y="70" width="106" height="50" rx="6" fill="var(--c1)"/>
    <rect x="146" y="70" width="94" height="50" fill="var(--c2)"/>
    <rect x="240" y="70" width="175" height="50" fill="var(--c3)"/>
    <rect x="415" y="70" width="99" height="50" fill="var(--c4)"/>
    <g font-family="inherit" font-size="13" fill="var(--ink)" text-anchor="middle">
      <text x="93" y="55">Homework 19.0</text><text x="193" y="148">Quizzes 16.8</text><text x="327" y="55">Tests 31.2</text><text x="464" y="148">Final 17.6</text>
    </g>
    <g font-family="inherit" font-size="13" fill="var(--muted)">
      <text x="40" y="190">0</text><text x="514" y="190" text-anchor="middle">84.6</text><text x="600" y="190" text-anchor="end">100</text>
    </g>
    <line x1="514" y1="60" x2="514" y2="175" stroke="var(--ink)" stroke-width="2" stroke-dasharray="4 4"/>
  </svg>
  <figcaption>Each category adds its weighted share. Tests are only 78%, but at 40% weight they contribute the most points.</figcaption>
</figure>

<h3>When the weights do not add up to 100%</h3>
<p>Mid-semester, some categories (often the final) have no grades yet. Most gradebooks then divide by the weights that do have grades. Using the same class before the final:</p>

<div class="example-box"><h4>Worked example: final not graded yet</h4>
<p>19.0 + 16.8 + 31.2 = 67.0 weighted points from 20% + 20% + 40% = 80% of the grade<br>
Current grade = 67.0 ÷ 0.80 = <strong>83.75%</strong></p>
</div>

<p>The <a href="/weighted-grade-calculator">weighted grade calculator</a> does this normalization automatically and tells you when your weights do not total 100. For more detail, see <a href="/blog/how-to-calculate-weighted-grades">how to calculate weighted grades</a>.</p>

[[tool:weighted-grade-calculator]]

<h2 id="how-do-teachers-calculate-grades">How do teachers calculate grades?</h2>

<p>Teachers use the same math above, usually inside gradebook software that does the calculation for them. What differs from class to class is the set of policies layered on top. Here is what to look for in your syllabus:</p>

<ul>
<li><strong>Category weights.</strong> Tests and finals commonly carry the most weight, but every teacher sets their own split.</li>
<li><strong>Dropped scores.</strong> Some teachers drop your lowest quiz or homework grade, which can raise a category average noticeably.</li>
<li><strong>Late and missing work.</strong> A missing assignment is usually entered as a zero, which hurts far more than a low score. Late penalties vary.</li>
<li><strong>Extra credit.</strong> Usually added as bonus points within a category, which means it is weighted like that category.</li>
<li><strong>Rounding.</strong> Some teachers round 89.5% up to 90%; others do not round at all. Ask if you are near a cutoff.</li>
<li><strong>Curves.</strong> A curve adjusts scores after a hard test. See <a href="/blog/how-to-curve-grades">how to curve grades</a> for the common methods.</li>
<li><strong>Standards-based grading.</strong> Some schools grade mastery of skills on a 1–4 scale instead of percentages. Read about <a href="/blog/standards-based-grading">standards-based grading</a> if your report card looks different.</li>
</ul>

<figure class="figure">
  <img src="/assets/img/photos/teacher-classroom.webp" width="1200" height="800" alt="Teacher standing at the front of a classroom with students" loading="lazy">
  <figcaption>Your teacher's syllabus lists the categories, weights, and policies that decide your final grade.</figcaption>
</figure>

<div class="callout callout-info"><strong>For teachers</strong><p>If you grade tests by hand, the <a href="/easy-grader">EZ Grader</a> gives you a printable chart of every possible number wrong and the matching percentage, so you do not have to divide for each paper.</p></div>

<h2 id="what-you-need-on-the-final">How to calculate what you need on a final</h2>

<p>This is the question most students actually have in December and May. If you know your current grade and how much the final exam is worth, you can solve for the score you need:</p>

<div class="formula">Required final score = (desired grade − current grade × (1 − w)) ÷ w</div>

<p>Here <em>w</em> is the final's weight as a decimal. If the final is worth 25%, w = 0.25 and (1 − w) = 0.75.</p>

<div class="example-box"><h4>Worked example: what do I need on my final?</h4>
<p>Current grade: 84% &nbsp;·&nbsp; Final exam weight: 25%</p>
<p>The part of your grade already locked in: 84 × 0.75 = 63.0 points</p>
<p>For an 80% (B-): (80 − 63) ÷ 0.25 = 17 ÷ 0.25 = <strong>68%</strong><br>
For an 85%: (85 − 63) ÷ 0.25 = 22 ÷ 0.25 = <strong>88%</strong><br>
For a 90% (A-): (90 − 63) ÷ 0.25 = 27 ÷ 0.25 = <strong>108%</strong>, not possible without extra credit</p>
</div>

<figure class="illustration">
  <svg viewBox="0 0 640 260" role="img" aria-label="Bar chart of final exam scores needed with an 84 percent current grade and a 25 percent final: 108 for an A, 68 for a B, 28 for a C, already secured for a D">
    <line x1="80" y1="200" x2="600" y2="200" stroke="var(--line)" stroke-width="2"/>
    <line x1="80" y1="56" x2="600" y2="56" stroke="var(--line)" stroke-dasharray="4 4"/>
    <text x="72" y="60" font-family="inherit" font-size="12" fill="var(--muted)" text-anchor="end">100%</text>
    <text x="72" y="204" font-family="inherit" font-size="12" fill="var(--muted)" text-anchor="end">0%</text>
    <rect x="110" y="44" width="80" height="156" rx="4" fill="var(--c5)"/>
    <rect x="240" y="102" width="80" height="98" rx="4" fill="var(--c1)"/>
    <rect x="370" y="160" width="80" height="40" rx="4" fill="var(--c2)"/>
    <rect x="500" y="196" width="80" height="4" fill="var(--c4)"/>
    <g font-family="inherit" font-size="14" fill="var(--ink)" text-anchor="middle" font-weight="700">
      <text x="150" y="36">108%</text><text x="280" y="94">68%</text><text x="410" y="152">28%</text><text x="540" y="186">secured</text>
    </g>
    <g font-family="inherit" font-size="13" fill="var(--muted)" text-anchor="middle">
      <text x="150" y="224">A (90)</text><text x="280" y="224">B (80)</text><text x="410" y="224">C (70)</text><text x="540" y="224">D (60)</text>
    </g>
  </svg>
  <figcaption>With an 84% and a 25% final, an A is out of reach, a B needs 68%, and a D is already locked in even with a zero.</figcaption>
</figure>

<p>Why is the D "secured"? Because (60 − 63) ÷ 0.25 = −12%. A negative answer means you would clear that grade even with a zero on the final. (We do not recommend testing that.) The <a href="/final-grade-calculator">final grade calculator</a> runs this formula and gives you the A, B, C, and D table in one click.</p>

[[tool:final-grade-calculator]]

<h3>What you need on a final in a points class</h3>
<p>In a points-based class, work with totals instead of weights. Suppose you have 380 of 450 points so far, the final is worth 150 points, and you want an 80% overall.</p>

<div class="example-box"><h4>Worked example: points-based final</h4>
<p>Total points in the course = 450 + 150 = 600<br>
Points needed for 80% = 0.80 × 600 = 480<br>
Points still needed = 480 − 380 = 100<br>
Score needed on the final = 100 ÷ 150 = <strong>66.7%</strong></p>
</div>

<p>If you still have other assignments left besides the final, the <a href="/raise-my-grade-calculator">raise my grade calculator</a> works out the average you need on all remaining work.</p>

<h2 id="final-exam-grades-and-semester-grades">Final exam grades and semester grades</h2>

<p>Many high schools calculate a semester grade from two quarter grades plus a final exam. A common split is 40% for each quarter and 20% for the final, though your school may use 45/45/10 or something else entirely.</p>

<div class="example-box"><h4>Worked example: semester grade</h4>
<p>Quarter 1: 88% × 0.40 = 35.2<br>
Quarter 2: 81% × 0.40 = 32.4<br>
Final exam: 75% × 0.20 = 15.0</p>
<p>Semester grade = 35.2 + 32.4 + 15.0 = <strong>82.6%</strong></p>
<p>On the scale above, 82.6% is a B- if your school does not round, or a B (83%) if it rounds to the nearest whole number. That is exactly why rounding policies matter near a cutoff.</p>
</div>

<p>The <a href="/semester-grade-calculator">semester grade calculator</a> uses the 40/40/20 split by default, lets you change the weights, and can also solve for the final exam score you need.</p>

<h2 id="tools-for-checking-your-math">A calculator you can trust</h2>

<p>Gradebook apps are convenient, but it helps to check the math yourself, especially before a final. Any basic calculator works for the formulas on this page, and a scientific calculator makes multi-step problems faster. If you need one for class anyway, this is a reliable, test-approved option:</p>

[[product:ti-30xs]]

<figure class="figure">
  <img src="/assets/img/photos/scientific-calculator.webp" width="1200" height="900" alt="Graphing calculator lying on a wooden desk" loading="lazy">
  <figcaption>Any calculator handles these formulas. The hard part is knowing which formula your class uses.</figcaption>
</figure>

<h2 id="points-inside-weighted-categories">How to compute grades when points and weights are combined</h2>

<p>Many classes use points <em>inside</em> each category and weights <em>across</em> categories. To compute a grade like this, do the points method for each category first, then apply the weighted formula.</p>

<div class="example-box"><h4>Worked example: hybrid gradebook</h4>
<p><strong>Tests (50%):</strong> 88/100, 71/100, 90/100 → 249 ÷ 300 = <strong>83%</strong><br>
<strong>Homework (30%):</strong> 132 of 150 points → 132 ÷ 150 = <strong>88%</strong><br>
<strong>Labs (20%):</strong> 54 of 60 points → 54 ÷ 60 = <strong>90%</strong></p>
<p>Final grade = (0.50 × 83) + (0.30 × 88) + (0.20 × 90) = 41.5 + 26.4 + 18.0 = <strong>85.9% (B)</strong></p>
</div>

<p>Notice that a single 71 on one test only lowered the test category to 83%, because it is pooled with the other two tests before the weight is applied. That is how most online gradebooks show your grade, so if you can see category averages in your school's portal, you can skip straight to the weighted step.</p>

<h2 id="how-one-assignment-changes-your-grade">How one assignment can change your grade</h2>

<p>Knowing the formulas lets you answer "what if" questions before they happen. Go back to the points example above, where you had 192 out of 220 points (87.3%). Here is what happens with the next few assignments:</p>

<div class="table-wrap"><table class="data-table"><thead><tr><th>Next assignment</th><th>New total</th><th>New grade</th></tr></thead><tbody>
<tr><td>100-point test, score 95</td><td>287 / 320</td><td>89.7% (B+)</td></tr>
<tr><td>100-point test, score 70</td><td>262 / 320</td><td>81.9% (B-)</td></tr>
<tr><td>20-point homework, missing (0)</td><td>192 / 240</td><td>80.0% (B-)</td></tr>
</tbody></table></div>

<p>The last row is the one students underestimate. Skipping a single 20-point homework assignment dropped the grade more than seven points, from 87.3% to 80.0%, even more than scoring 70 on a test worth five times as many points. Turning in something, even late or incomplete, is almost always better than a zero.</p>

<p>Early in a term, each assignment moves your grade a lot because there are few points in the gradebook. Late in the term, the same score barely moves it. That is why the final exam is often the only thing left that can still change your grade in a big way.</p>

<h2 id="common-mistakes">Common grade-calculating mistakes</h2>

<ol class="steps">
<li><strong>Averaging percentages in a points class.</strong> A 10-point quiz and a 200-point project are not equal. Add points, not percentages.</li>
<li><strong>Forgetting zeros.</strong> Missing work counts. Leave it out of your calculation and your estimate will be too high.</li>
<li><strong>Using percents instead of decimals for weights.</strong> 40% × 78 = 31.2 only when you write 40% as 0.40. Multiplying by 40 gives 3,120.</li>
<li><strong>Ignoring ungraded categories.</strong> If the final is not graded yet, divide by the weights you used, or your grade will look too low.</li>
<li><strong>Guessing the weights.</strong> Check the syllabus or the online gradebook. Every teacher sets their own.</li>
</ol>

<h2 id="conclusion">Wrapping up</h2>

<p>Now you know how to calculate final grades in either system. For a points class, add up earned and possible points and divide. For a weighted class, multiply each category average by its weight and add. To find what you need on the final, use (desired − current × (1 − w)) ÷ w. And when in doubt about rounding, dropped scores, or curves, ask your teacher; those policies vary from class to class.</p>

<p>When you are ready to see how your class grades affect your GPA, read <a href="/blog/what-is-gpa">what is GPA</a> or plug your grades into the <a href="/gpa-calculator">GPA calculator</a>.</p>
HTML,
];
