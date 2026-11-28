<?php
return [
  'slug'        => 'how-to-calculate-weighted-grades',
  'title'       => 'How to Calculate Weighted Grades (Formula + Worked Examples)',
  'meta_title'  => 'How to Calculate Weighted Grades: Formula & Examples',
  'description' => 'Learn how to calculate weighted grades step by step: the formula, worked examples, what to do when weights don\'t add to 100%, and common mistakes to avoid.',
  'keyword'     => 'how to calculate weighted grades',
  'category'    => 'Grades',
  'date'        => '2026-04-21',
  'updated'     => '2026-04-21',
  'author'      => 'FGC Editorial Team',
  'hero'        => 'top-view-study-desk',
  'hero_alt'    => 'Top-down view of a study desk with notebooks, a laptop and a calculator',
  'excerpt'     => 'Multiply each category score by its weight, add the results, and divide by the total weight. Here is the formula with real class examples.',
  'related_tools' => ['weighted-grade-calculator', 'final-grade-calculator', 'points-grade-calculator'],
  'faqs'        => [
    ['How do you calculate a weighted grade?', 'Multiply each category score (as a percentage) by its weight, add those products together, and divide by the sum of the weights. If the weights already add to 100%, dividing by 1.00 (or 100%) leaves the number unchanged.'],
    ['What if my category weights don\'t add up to 100%?', 'Divide your weighted total by the weights you actually have scores for. For example, if only 80% of the grade has been graded so far, divide the weighted sum by 0.80 to get your current grade.'],
    ['Is a weighted grade the same as a weighted GPA?', 'No. A weighted grade is your percentage in one class, built from categories like homework and tests. A weighted GPA is a grade point average where honors or AP classes earn extra points. See <a href="/blog/weighted-vs-unweighted-gpa">weighted vs. unweighted GPA</a>.'],
    ['Should I average my test percentages or add up points?', 'Follow your teacher\'s gradebook. Many gradebooks total the points inside a category (so a 100-point test counts twice as much as a 50-point quiz), while others average each assignment\'s percentage equally. The two methods can give slightly different results.'],
    ['How much will my final exam change my grade?', 'It depends on the final\'s weight. Use the formula required = (desired − current × (1 − w)) ÷ w, where w is the final\'s weight as a decimal, or plug your numbers into the <a href="/final-grade-calculator">final grade calculator</a>.'],
    ['Why does my weighted grade differ from my total points percentage?', 'Because weighting changes how much each point is worth. A point in a 40% test category is worth more than a point in a 10% homework category, so your weighted grade and your raw points percentage rarely match.'],
  ],
  'body'        => <<<'HTML'
<p class="lead">To calculate weighted grades, multiply each category score by its weight, add the results, and divide by the total weight. That is the whole method. If your class counts tests as 40%, quizzes as 30%, homework as 20%, and participation as 10%, each score gets scaled by its share before everything is added up.</p>

<p>This guide on how to calculate weighted grades walks through the formula, several worked examples from real-looking classes, what to do when weights don't add to 100%, and how to figure out what you need on the final. You can follow along by hand or check your numbers with our free calculator.</p>

<div class="key-takeaways"><h3>Key takeaways</h3><ul>
<li>Weighted grade = Σ (score × weight) ÷ Σ weights.</li>
<li>Convert weights to decimals (40% = 0.40) before multiplying.</li>
<li>If only part of the grade has been graded, divide by the weights you have so far.</li>
<li>Points inside a category are usually totaled first, then the category percentage is weighted.</li>
<li>Your weighted grade and your raw points percentage are rarely the same number.</li>
</ul></div>

<h2 id="what-is-a-weighted-grade">What is a weighted grade?</h2>

<p>A weighted grade is a class average where some kinds of work count more than others. Instead of every point being worth the same, your teacher assigns each category a percentage of the final grade. Those percentages are the weights.</p>

<p>A typical high school syllabus might say: tests 40%, quizzes 30%, homework 20%, participation 10%. College syllabi often look like: midterm 25%, final exam 30%, problem sets 30%, labs 15%. The categories and weights vary by teacher and school, so always check your syllabus or online gradebook.</p>

<p>The opposite of a weighted grade is a <strong>total points</strong> system. There, you simply add every point you earned and divide by every point possible. A 100-point test automatically counts more than a 10-point homework assignment, but there are no category percentages. If your class works that way, the <a href="/points-grade-calculator">points grade calculator</a> is the better tool.</p>

<figure class="figure">
  <img src="/assets/img/photos/hand-writing-notebook.webp" width="1200" height="800" alt="Student writing category scores in a spiral notebook" loading="lazy">
  <figcaption>Writing each category's score and weight in a list makes the math much easier to check.</figcaption>
</figure>

<h2 id="weighted-grade-formula">The weighted grade formula</h2>

<p>Here is the formula your teacher's gradebook uses behind the scenes:</p>

<div class="formula">Weighted grade = (S₁ × W₁ + S₂ × W₂ + … + Sₙ × Wₙ) ÷ (W₁ + W₂ + … + Wₙ)</div>

<p>S is each category's score as a percentage, and W is that category's weight. When the weights add up to 100% (or 1.00 as decimals), the division at the end changes nothing, so you can skip it. When they don't, that division is what keeps your answer on a 0–100 scale.</p>

<figure class="illustration">
  <svg viewBox="0 0 640 220" role="img" aria-label="Flow diagram: each category score is multiplied by its weight, the products are added, then divided by the total weight to get the weighted grade">
    <rect x="10" y="30" width="130" height="44" rx="8" fill="var(--c1)"/>
    <text x="75" y="57" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">Score × weight</text>
    <rect x="10" y="88" width="130" height="44" rx="8" fill="var(--c2)"/>
    <text x="75" y="115" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">Score × weight</text>
    <rect x="10" y="146" width="130" height="44" rx="8" fill="var(--c4)"/>
    <text x="75" y="173" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">Score × weight</text>
    <path d="M140 52 L230 110 M140 110 L230 110 M140 168 L230 110" stroke="var(--line)" stroke-width="3" fill="none"/>
    <circle cx="260" cy="110" r="32" fill="var(--c3)"/>
    <text x="260" y="117" text-anchor="middle" font-size="22" font-family="inherit" fill="var(--ink)">Σ</text>
    <path d="M292 110 L360 110" stroke="var(--line)" stroke-width="3"/>
    <rect x="360" y="82" width="120" height="56" rx="8" fill="var(--c6)"/>
    <text x="420" y="106" text-anchor="middle" font-size="13" font-family="inherit" fill="var(--surface)">÷ total</text>
    <text x="420" y="124" text-anchor="middle" font-size="13" font-family="inherit" fill="var(--surface)">weight</text>
    <path d="M480 110 L530 110" stroke="var(--line)" stroke-width="3"/>
    <rect x="530" y="82" width="100" height="56" rx="8" fill="var(--c5)"/>
    <text x="580" y="115" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">Grade %</text>
    <text x="320" y="210" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">Multiply, add, then divide by the weights you have</text>
  </svg>
  <figcaption>The weighted grade formula in three moves: multiply, add, divide.</figcaption>
</figure>

<h2 id="step-by-step">How to calculate weighted grades step by step</h2>

<ol class="steps">
<li><strong>List your categories and weights.</strong> Copy them from your syllabus or gradebook, for example homework 20%, quizzes 30%, tests 40%, participation 10%.</li>
<li><strong>Find your score in each category.</strong> Use the category percentage your gradebook shows, or total the points in that category and divide (points earned ÷ points possible × 100).</li>
<li><strong>Convert each weight to a decimal.</strong> Divide by 100: 20% becomes 0.20, 30% becomes 0.30.</li>
<li><strong>Multiply each score by its weight.</strong> A 92% in a 0.20 category contributes 92 × 0.20 = 18.4 points.</li>
<li><strong>Add the products.</strong> This is your weighted total.</li>
<li><strong>Divide by the sum of the weights.</strong> If the weights add to 1.00, your total is already your grade. If not, divide by what they do add to.</li>
<li><strong>Convert to a letter grade.</strong> Use your school's scale. On the common US scale, 90–92 is an A-, 83–86 is a B, and so on (scales vary by school).</li>
</ol>

<h2 id="worked-examples">Worked examples</h2>

<p>Let's run the method on a few situations students actually run into. All math is shown so you can copy the pattern with your own numbers.</p>

<div class="example-box"><h4>Example 1: A standard high school class</h4>
<p>Your syllabus says homework 20%, quizzes 30%, tests 40%, participation 10%. Your category averages are homework 92%, quizzes 85%, tests 78%, participation 100%.</p>
<p>Homework: 92 × 0.20 = 18.4<br>Quizzes: 85 × 0.30 = 25.5<br>Tests: 78 × 0.40 = 31.2<br>Participation: 100 × 0.10 = 10.0</p>
<p>Total: 18.4 + 25.5 + 31.2 + 10.0 = <strong>85.1%</strong>. The weights add to 1.00, so no extra division is needed. On the standard scale, 85.1% is a <strong>B</strong>.</p>
</div>

<p>Notice what happened to the tests. A 78% is a C+, but because the other categories were strong, the overall grade is still a solid B. At the same time, tests are 40% of the grade, so raising that 78 is the fastest way to raise the whole class grade.</p>

<figure class="illustration">
  <svg viewBox="0 0 640 170" role="img" aria-label="Stacked bar showing how homework contributes 18.4, quizzes 25.5, tests 31.2 and participation 10 points to an 85.1 percent grade">
    <rect x="20" y="50" width="600" height="50" rx="6" fill="none" stroke="var(--line)" stroke-width="2"/>
    <rect x="20" y="50" width="110.4" height="50" fill="var(--c1)"/>
    <rect x="130.4" y="50" width="153" height="50" fill="var(--c2)"/>
    <rect x="283.4" y="50" width="187.2" height="50" fill="var(--c4)"/>
    <rect x="470.6" y="50" width="60" height="50" fill="var(--c3)"/>
    <text x="75" y="80" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">18.4</text>
    <text x="207" y="80" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">25.5</text>
    <text x="377" y="80" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--surface)">31.2</text>
    <text x="500" y="80" text-anchor="middle" font-size="14" font-family="inherit" fill="var(--ink)">10</text>
    <text x="575" y="80" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">lost 14.9</text>
    <text x="75" y="125" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">Homework</text>
    <text x="207" y="125" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">Quizzes</text>
    <text x="377" y="125" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">Tests</text>
    <text x="500" y="125" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">Particip.</text>
    <text x="320" y="30" text-anchor="middle" font-size="15" font-family="inherit" fill="var(--ink)">Weighted grade = 85.1 out of 100</text>
    <text x="20" y="155" font-size="12" font-family="inherit" fill="var(--muted)">0</text>
    <text x="620" y="155" text-anchor="end" font-size="12" font-family="inherit" fill="var(--muted)">100</text>
  </svg>
  <figcaption>Each category's contribution to the 85.1% in Example 1. The test category has the most points to gain.</figcaption>
</figure>

<div class="example-box"><h4>Example 2: Weights that don't add to 100% yet</h4>
<p>Midway through the semester, your class is weighted homework 15%, labs 25%, tests 40%, and final exam 20%. You haven't taken the final, so only 80% of your grade exists. Your scores: homework 95%, labs 88%, tests 81%.</p>
<p>Homework: 95 × 0.15 = 14.25<br>Labs: 88 × 0.25 = 22.00<br>Tests: 81 × 0.40 = 32.40</p>
<p>Weighted total: 14.25 + 22.00 + 32.40 = 68.65. Total weight so far: 0.15 + 0.25 + 0.40 = 0.80.</p>
<p>Current grade: 68.65 ÷ 0.80 = <strong>85.8%</strong> (a B).</p>
</div>

<p>This is the step most people miss. If you stopped at 68.65, you'd think you were failing. Dividing by the weight you've actually completed gives the grade your gradebook shows. Our <a href="/weighted-grade-calculator">weighted grade calculator</a> does this automatically: if your weights don't total 100, it normalizes by the total weight and tells you it did.</p>

[[tool:weighted-grade-calculator]]

<div class="example-box"><h4>Example 3: Finding the category score from points</h4>
<p>Your tests category has three tests: 42/50, 78/100, and 88/100.</p>
<p><strong>Totaling points:</strong> (42 + 78 + 88) ÷ (50 + 100 + 100) = 208 ÷ 250 = <strong>83.2%</strong>.</p>
<p><strong>Averaging percentages:</strong> 42/50 = 84%, 78/100 = 78%, 88/100 = 88%. Average = (84 + 78 + 88) ÷ 3 = <strong>83.3%</strong>.</p>
</div>

<p>The two answers are close here, but they can drift apart when assignments have very different point values. Totaling points gives the 50-point test half the influence of each 100-point test. Averaging percentages treats all three tests equally. Most gradebooks total points within a category, but some teachers set it up the other way, so check if your number doesn't match.</p>

<figure class="figure">
  <img src="/assets/img/photos/student-at-computer.webp" width="1200" height="801" alt="Student checking an online gradebook on a desktop computer" loading="lazy">
  <figcaption>Your online gradebook usually lists each category's percentage and weight, which is all you need for the formula.</figcaption>
</figure>

<div class="example-box"><h4>Example 4: Weighted vs. total points on the same work</h4>
<p>You earned 190/200 homework points (95%) and 160/200 test points (80%).</p>
<p><strong>Total points:</strong> 350 ÷ 400 = <strong>87.5%</strong> (B+).</p>
<p><strong>Weighted, homework 30% and tests 70%:</strong> 95 × 0.30 + 80 × 0.70 = 28.5 + 56.0 = <strong>84.5%</strong> (B).</p>
</div>

<p>Same scores, different grade. Because tests carry 70% of the weight, your weaker test scores pull harder. This is why you can't just add up all your points in a weighted class and expect to match the gradebook.</p>

<h2 id="what-you-need-on-the-final">Using weighted grades to plan for the final</h2>

<p>Once you know your current weighted grade, you can work backward to find the score you need on a final exam or the last big project. The formula is:</p>

<div class="formula">Required final score = (Desired grade − Current grade × (1 − w)) ÷ w</div>

<p>Here, w is the final's weight as a decimal. Let's continue Example 2, where your current grade is 85.8125% and the final is worth 20% (w = 0.20).</p>

<div class="example-box"><h4>Example 5: What do I need on the final?</h4>
<p><strong>To finish with an 85%:</strong> (85 − 85.8125 × 0.80) ÷ 0.20 = (85 − 68.65) ÷ 0.20 = 16.35 ÷ 0.20 = <strong>81.75%</strong>.</p>
<p><strong>To finish with a 90%:</strong> (90 − 68.65) ÷ 0.20 = 21.35 ÷ 0.20 = <strong>106.75%</strong>. Unless there's extra credit, a 90 is out of reach.</p>
</div>

<p>Knowing this early helps you decide where to spend study time. If an A is mathematically impossible, protecting your B (and putting extra hours into a class where an A is still possible) can be the smarter move. Run your own numbers in the <a href="/final-grade-calculator">final grade calculator</a>, or read our full guide on <a href="/blog/how-to-calculate-your-final-grade">how to calculate your final grade</a>.</p>

[[tool:final-grade-calculator]]

<h2 id="letter-grades-in-categories">What if a category shows a letter grade?</h2>

<p>Some gradebooks show a letter (like A- or B+) instead of a percentage. To use the formula, convert each letter to a number first. Two common approaches:</p>

<ul>
<li><strong>Use a percentage from your school's scale.</strong> If your teacher's scale says B+ is 87–89, you might use 88 as a reasonable midpoint. This works when you don't know the exact percentage.</li>
<li><strong>Use grade points.</strong> Some teachers weight letter grades on a 4.0 scale (A = 4.0, B = 3.0) and then convert the weighted result back to a letter. The math is identical; only the units change.</li>
</ul>

<p>Midpoints are an estimate, so your result may be off by a point or so. If you can see the exact percentage in your gradebook, use that instead. Our <a href="/letter-grade-calculator">letter grade calculator</a> shows the full standard US scale if you need a reference.</p>

<div class="table-wrap"><table class="data-table"><thead><tr><th>Letter</th><th>Percent range</th><th>4.0 points</th></tr></thead><tbody>
<tr><td>A</td><td>93–96</td><td>4.0</td></tr>
<tr><td>A-</td><td>90–92</td><td>3.7</td></tr>
<tr><td>B+</td><td>87–89</td><td>3.3</td></tr>
<tr><td>B</td><td>83–86</td><td>3.0</td></tr>
<tr><td>B-</td><td>80–82</td><td>2.7</td></tr>
<tr><td>C+</td><td>77–79</td><td>2.3</td></tr>
<tr><td>C</td><td>73–76</td><td>2.0</td></tr>
</tbody></table></div>

<p>That table follows a common US scale (A+ is 97–100). Plenty of schools use a simpler 10-point scale (90–100 = A) or skip plus and minus grades, so check yours.</p>

<h2 id="dropped-scores-extra-credit">Dropped scores and extra credit</h2>

<p>Two common syllabus rules change the category score before any weighting happens. Handle them first, then plug the adjusted category percentage into the formula as usual.</p>

<div class="example-box"><h4>Example 6: Dropping the lowest quiz</h4>
<p>Your five quizzes (all 20 points) are 18, 15, 9, 17, and 19. Without the drop: 78 ÷ 100 = 78%. Your teacher drops the lowest score, so remove the 9: (18 + 15 + 17 + 19) ÷ 80 = 69 ÷ 80 = <strong>86.25%</strong>.</p>
<p>In a 30% quiz category, that drop is worth (86.25 − 78) × 0.30 ≈ <strong>2.5 points</strong> on your overall grade.</p>
</div>

<p>Extra credit works differently from class to class. Sometimes it's added to a single category (bonus points on one test), sometimes it's its own small category, and sometimes it's added straight to the final percentage. Each version changes the math, so ask your teacher which one applies before counting on it. If bonus points go into a category, add them to "points earned" but not to "points possible."</p>

<h2 id="common-mistakes">Common weighted grade mistakes</h2>

<div class="callout callout-warn"><strong>Watch out</strong><p>The biggest mistake is forgetting to divide by the total weight when some categories are still empty. It makes your grade look far lower than it really is.</p></div>

<ul>
<li><strong>Adding raw points across categories.</strong> In a weighted class, 10 homework points and 10 test points are not worth the same. Calculate each category's percentage first.</li>
<li><strong>Using whole-number weights without adjusting.</strong> If you multiply by 40 instead of 0.40, divide by 100 at the end (or by the total of the whole-number weights).</li>
<li><strong>Counting an empty category as zero.</strong> A category with no grades yet should be left out, not entered as 0%. A real zero (a missing assignment) is different and should be counted.</li>
<li><strong>Ignoring dropped scores.</strong> Some teachers drop the lowest quiz or homework grade. If yours does, remove it before finding the category percentage.</li>
<li><strong>Rounding too early.</strong> Keep a couple of decimals until the end. Rounding each category can shift your final grade across a letter boundary.</li>
</ul>

<figure class="figure">
  <img src="/assets/img/photos/exam-answer-sheet.webp" width="1200" height="782" alt="Student filling in a test answer sheet with a pencil" loading="lazy">
  <figcaption>Tests often carry the biggest weight, so a few extra points there move your grade more than anything else.</figcaption>
</figure>

<h2 id="raise-your-grade">How to use weights to raise your grade</h2>

<p>Weights don't just tell you your grade. They tell you where effort pays off most. A one-point gain in a 40% category raises your class grade by 0.4 points, while a one-point gain in a 10% category raises it by only 0.1.</p>

<div class="callout callout-tip"><strong>Pro tip</strong><p>Multiply each category's weight by the points you've lost there (100 minus your score). The category with the biggest result is where your grade has the most room to grow.</p></div>

<p>From Example 1: tests lose 22 points × 0.40 = 8.8 points of class grade, quizzes lose 15 × 0.30 = 4.5, homework loses 8 × 0.20 = 1.6, and participation loses nothing. Test prep is clearly the priority. Our guide to <a href="/blog/how-to-raise-your-gpa">raising your GPA</a> covers study strategies that help on high-weight assessments.</p>

<p>Small categories still matter, though. Homework and participation are often the easiest points to secure, and a missing assignment counted as zero can drag a small category down fast. A planner that tracks due dates for each category helps you avoid those easy losses.</p>

[[product:academic-planner]]

<h2 id="weighted-grades-vs-weighted-gpa">Weighted grades vs. weighted GPA</h2>

<p>The word "weighted" shows up in two different places, and it's easy to mix them up.</p>

<div class="compare"><div class="compare-col"><h4>Weighted grade</h4><ul><li>Your percentage in one class</li><li>Built from categories (homework, tests, labs)</li><li>Weights come from the syllabus</li><li>Result is a percent and a letter</li></ul></div><div class="compare-col"><h4>Weighted GPA</h4><ul><li>An average across all your classes</li><li>Honors and AP/IB classes earn extra grade points</li><li>Boosts are set by the school and vary</li><li>Result is a number like 3.8 or 4.2</li></ul></div></div>

<p>College GPA uses a similar idea with credits: a 4-credit class counts more than a 1-credit class. That's a credit-weighted average, and you can calculate it with the <a href="/gpa-calculator">GPA calculator</a>. For high school honors and AP boosts, see <a href="/blog/weighted-vs-unweighted-gpa">weighted vs. unweighted GPA</a>.</p>

<h2 id="summary">The bottom line</h2>

<p>Knowing how to calculate weighted grades takes the mystery out of your gradebook. Multiply each category score by its weight, add the results, and divide by the total weight you've completed. Then use that number to plan for your final and to decide which category deserves your next study session.</p>

<p>If you'd rather not do the arithmetic, enter your categories into the <a href="/weighted-grade-calculator">weighted grade calculator</a>. It handles uneven weights, letter-grade inputs, and gives you your percentage, letter grade, and 4.0 grade points in one step.</p>
HTML,
];
