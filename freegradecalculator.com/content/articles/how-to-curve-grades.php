<?php
return [
  'slug'        => 'how-to-curve-grades',
  'title'       => 'How to Curve Grades: 5 Methods With Worked Examples',
  'meta_title'  => 'How to Curve Grades: 5 Methods Teachers Use',
  'description' => 'How to curve grades fairly: flat curve, adding points, square-root curve, shifting to a target mean, and the bell curve, with worked examples, pros and cons.',
  'keyword'     => 'how to curve grades',
  'category'    => 'Teaching',
  'date'        => '2026-08-04',
  'updated'     => '2026-08-04',
  'author'      => 'FGC Editorial Team',
  'hero'        => 'teacher-classroom',
  'hero_alt'    => 'Teacher standing at the front of a classroom reviewing results with students',
  'excerpt'     => 'Five common ways to curve a test, from adding a few points to rescaling with z-scores, all worked out on the same set of ten scores.',
  'related_tools' => ['grade-curve-calculator', 'class-average-calculator', 'easy-grader'],
  'faqs'        => [
    ['What is the easiest way to curve grades?', 'Adding the same number of points to every score is the simplest. A flat curve, where you add enough points that the top score becomes 100, is a popular version because it gives a clear reason for the size of the curve.'],
    ['Can a curve lower my grade?', 'The add-points, flat, and square-root curves never lower a score. A bell curve or a forced letter distribution can lower some scores if the target mean or spread is set below the original, which is one reason many teachers avoid them or only apply them when every score goes up.'],
    ['How does the square-root curve work?', 'Take the square root of the raw percentage and multiply by 10. A 64 becomes 10 × 8 = 80 and an 81 becomes 90. Low scores get the biggest boost, 100 stays 100, and the order of students never changes.'],
    ['What does curving on a bell curve mean?', 'It means converting each score to a z-score (how many standard deviations it sits from the class mean) and then rebuilding the score around a new mean and standard deviation you choose. Some instructors also assign letter grades by percentile, but that forced-distribution approach is less common in K–12 classrooms.'],
    ['Is curving grades fair?', 'It can be when a test turned out harder than intended and the curve is applied the same way to everyone. It is less fair when it pits students against each other or hides a problem with the test itself. Policies vary by school and department, so check yours.'],
    ['Should I cap curved scores at 100?', 'Most teachers do, so that a curve doesn\'t produce scores like 104. If you allow scores above 100, say so in advance, because it changes how much that test affects the overall grade.'],
  ],
  'body'        => <<<'HTML'
<p class="lead">To curve grades, you adjust every student's raw score using one consistent rule, such as adding points, scaling so the top score becomes 100, or rescaling to a target class average. The right method depends on why you're curving: a test that ran too hard calls for a different fix than a class average that sits a few points low.</p>

<p>This guide explains how to curve grades with the five methods teachers use most, and runs each one on the same ten test scores so you can compare the results side by side. It's written for teachers, but students who want to know what "the test was curved" actually means will find the math here too.</p>

<div class="key-takeaways"><h3>Key takeaways</h3><ul>
<li>A curve should fix a problem with the test, not change what a grade means.</li>
<li>Add-points and flat curves move everyone up by the same amount.</li>
<li>The square-root curve (10 × √score) helps low scores most and keeps 100 at 100.</li>
<li>Shifting to a target mean is a flat curve with a different goal.</li>
<li>A bell curve rescales scores with z-scores and can lower some grades, so use it carefully.</li>
</ul></div>

<h2 id="why-curve">Why teachers curve grades</h2>

<p>Most curves exist because a test didn't measure what the teacher expected. Maybe a question was ambiguous, a topic got less class time than planned, or the test simply ran longer than the period. When the whole class does worse than their homework and quiz performance suggests, a curve corrects for the test, not the students.</p>

<p>Other reasons include keeping grades consistent across sections that took different versions of an exam, and department or course policies that set a target range for averages. In many college courses, especially large intro classes, the syllabus states how curving works up front. In K–12, it's usually the individual teacher's call, and practices vary widely by school.</p>

<div class="callout callout-info"><strong>Before you curve</strong><p>Check whether a specific question caused the problem. Throwing out or re-scoring one flawed question is often fairer and easier to explain than curving the whole test.</p></div>

<figure class="figure">
  <img src="/assets/img/photos/kids-taking-test.webp" width="1200" height="800" alt="Students writing answers at their classroom desks during a test" loading="lazy">
  <figcaption>When a whole class struggles on one test, the test itself may be the issue.</figcaption>
</figure>

<h2 id="example-scores">The example scores we'll use</h2>

<p>All five methods below use the same ten raw scores out of 100:</p>

<div class="formula">88, 82, 76, 74, 70, 68, 65, 61, 58, 48</div>

<p>The sum is 690, so the class mean is 690 ÷ 10 = <strong>69.0</strong>. The highest score is 88 and the lowest is 48. The population standard deviation is about <strong>11.17</strong>, which we'll need for the bell curve. You can get all of these numbers instantly by pasting your scores into the <a href="/class-average-calculator">class average calculator</a>.</p>

<h2 id="how-to-curve-grades-methods">How to curve grades: 5 methods</h2>

<h3 id="flat-curve">1. Flat curve (top score becomes 100)</h3>

<p>Find the gap between the highest score and 100, then add that many points to everyone. It's popular because the size of the curve has a built-in justification: if one student could earn an 88, the test was doable, and the gap is treated as the test's difficulty penalty.</p>

<div class="example-box"><h4>Worked example: flat curve</h4>
<p>Top score = 88, so the curve is 100 − 88 = <strong>12 points</strong>.</p>
<p>New scores: 100, 94, 88, 86, 82, 80, 77, 73, 70, 60.</p>
<p>New mean: 69.0 + 12 = <strong>81.0</strong>.</p>
</div>

<p>A variation multiplies instead of adding: every score is multiplied by 100 ÷ top score. With a top of 88, a 70 becomes 70 × (100 ÷ 88) ≈ 79.5 and a 48 becomes about 54.5. Multiplying helps high scorers a bit more than low scorers, while adding helps everyone equally. Be clear about which version you use.</p>

<p><strong>Pros:</strong> simple, easy to explain, never lowers a score. <strong>Cons:</strong> one outlier score controls the whole curve. If your top student scored 99, the curve is just 1 point even if everyone else struggled.</p>

<h3 id="add-points">2. Add a fixed number of points</h3>

<p>You choose a number, often based on a flawed question's value or your sense of how much harder the test ran than intended, and add it to everyone.</p>

<div class="example-box"><h4>Worked example: add 5 points</h4>
<p>New scores: 93, 87, 81, 79, 75, 73, 70, 66, 63, 53.</p>
<p>New mean: 69.0 + 5 = <strong>74.0</strong>.</p>
</div>

<p><strong>Pros:</strong> the most transparent method, and it keeps the gaps between students the same. <strong>Cons:</strong> the number can feel arbitrary unless you tie it to something concrete, like "question 14 was worth 5 points and was worded badly."</p>

<h3 id="square-root-curve">3. Square-root curve</h3>

<p>Take the square root of each percentage and multiply by 10. A perfect 100 stays 100, a 0 stays 0, and everything in between rises, with low scores rising the most.</p>

<div class="formula">Curved score = 10 × √(raw score)</div>

<div class="example-box"><h4>Worked example: square-root curve</h4>
<p>88 → 10 × 9.381 = 93.8<br>82 → 90.6<br>76 → 87.2<br>74 → 86.0<br>70 → 83.7<br>68 → 82.5<br>65 → 80.6<br>61 → 78.1<br>58 → 76.2<br>48 → 10 × 6.928 = 69.3</p>
<p>New mean: about <strong>82.8</strong>.</p>
</div>

<p>The 48 gained more than 21 points while the 88 gained under 6. That compression is the point of this method: it narrows the gap between strong and struggling students while keeping everyone in the same order.</p>

<p><strong>Pros:</strong> no arbitrary number to pick, never lowers a score, 100 stays 100. <strong>Cons:</strong> it can be a big boost, which some teachers find too generous. Applied to a class that did reasonably well, it can push the average into the high 80s or 90s.</p>

<figure class="illustration">
  <svg viewBox="0 0 640 300" role="img" aria-label="Line chart comparing raw scores on the horizontal axis to square-root curved scores, which bow above the no-change diagonal">
    <line x1="60" y1="250" x2="600" y2="250" stroke="var(--line)" stroke-width="2"/>
    <line x1="60" y1="250" x2="60" y2="30" stroke="var(--line)" stroke-width="2"/>
    <line x1="60" y1="250" x2="600" y2="30" stroke="var(--muted)" stroke-width="2" stroke-dasharray="6 6"/>
    <polyline fill="none" stroke="var(--c1)" stroke-width="4" points="60,250 87,201 114,181 168,152 222,129 276,110 330,94 384,79 438,66 492,53 546,41 600,30"/>
    <circle cx="319" cy="97" r="6" fill="var(--c3)"/>
    <text x="330" y="90" font-size="13" font-family="inherit" fill="var(--ink)">48 → 69.3</text>
    <circle cx="535" cy="44" r="6" fill="var(--c4)"/>
    <text x="440" y="36" font-size="13" font-family="inherit" fill="var(--ink)">88 → 93.8</text>
    <text x="330" y="285" text-anchor="middle" font-size="13" font-family="inherit" fill="var(--muted)">Raw score (0–100)</text>
    <text x="20" y="140" font-size="13" font-family="inherit" fill="var(--muted)" transform="rotate(-90 20 140)" text-anchor="middle">Curved score</text>
    <text x="470" y="205" font-size="12" font-family="inherit" fill="var(--muted)">dashed = no change</text>
    <text x="54" y="266" text-anchor="end" font-size="12" font-family="inherit" fill="var(--muted)">0</text>
    <text x="600" y="266" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">100</text>
    <text x="54" y="35" text-anchor="end" font-size="12" font-family="inherit" fill="var(--muted)">100</text>
  </svg>
  <figcaption>The square-root curve lifts every score between 0 and 100, and the lift is largest in the lower half.</figcaption>
</figure>

<h3 id="target-mean">4. Shift to a target class average</h3>

<p>Pick the average you think the test should have produced, often based on how the same class did on similar tests, then add the difference between the target and the actual mean to every score.</p>

<div class="formula">Points to add = Target mean − Current mean</div>

<div class="example-box"><h4>Worked example: target mean of 75</h4>
<p>Points to add: 75 − 69 = <strong>6</strong>.</p>
<p>New scores: 94, 88, 82, 80, 76, 74, 71, 67, 64, 54.</p>
<p>New mean: <strong>75.0</strong>.</p>
</div>

<p>Mathematically, this is the add-points method with a principled way of choosing the number. Some teachers instead multiply every score by target ÷ current mean (here 75 ÷ 69 ≈ 1.087), which scales scores proportionally. A 70 would become about 76.1 and an 88 about 95.7. The multiplying version gives higher scorers slightly more, and it can push top scores over 100, so you'll usually want to cap.</p>

<p><strong>Pros:</strong> ties the curve to a clear, defensible goal. <strong>Cons:</strong> you need a reasonable target. Picking it after seeing the scores can look arbitrary to students.</p>

<figure class="figure">
  <img src="/assets/img/photos/charts-analysis.webp" width="1200" height="795" alt="Pen pointing at printed bar and line charts of results" loading="lazy">
  <figcaption>Looking at the score distribution before choosing a method helps you match the curve to the problem.</figcaption>
</figure>

<h3 id="bell-curve">5. Bell curve (z-score rescaling)</h3>

<p>This is the most statistical method. You convert each score into a z-score, which measures how many standard deviations it sits above or below the class mean. Then you rebuild each score around a new mean and standard deviation that you choose.</p>

<div class="formula">z = (score − mean) ÷ SD &nbsp;&nbsp;→&nbsp;&nbsp; new score = target mean + z × target SD</div>

<div class="example-box"><h4>Worked example: target mean 78, target SD 8</h4>
<p>Class mean = 69.0, SD ≈ 11.17.</p>
<p>88: z = (88 − 69) ÷ 11.17 ≈ 1.70 → 78 + 1.70 × 8 ≈ <strong>91.6</strong><br>
70: z = (70 − 69) ÷ 11.17 ≈ 0.09 → 78 + 0.09 × 8 ≈ <strong>78.7</strong><br>
65: z ≈ −0.36 → 78 − 0.36 × 8 ≈ <strong>75.1</strong><br>
48: z = (48 − 69) ÷ 11.17 ≈ −1.88 → 78 − 1.88 × 8 ≈ <strong>63.0</strong></p>
<p>All ten: 91.6, 87.3, 83.0, 81.6, 78.7, 77.3, 75.1, 72.3, 70.1, 63.0. New mean: <strong>78.0</strong>.</p>
</div>

<p>Because the new SD (8) is smaller than the original (11.17), the scores also squeeze closer together. If you set the target SD larger than the original, scores spread out instead, and low scores can drop below their raw value. With these settings every score still rises, but that's not guaranteed with other targets.</p>

<div class="callout callout-warn"><strong>Careful</strong><p>"Grading on a curve" sometimes means assigning letters by rank, such as the top 10% get A's no matter their scores. That forced distribution means students compete with each other, and a strong class can end up with lower grades than they earned. Most K–12 teachers avoid it.</p></div>

<p><strong>Pros:</strong> handles both the average and the spread, and it's standard in some university departments. <strong>Cons:</strong> hard to explain, can lower scores, and works poorly with small classes where one or two outliers swing the mean and SD.</p>

<figure class="illustration">
  <svg viewBox="0 0 640 230" role="img" aria-label="Number line comparing raw scores spread from 48 to 88 with bell-curved scores squeezed between 63 and 91.6">
    <text x="20" y="62" font-size="13" font-family="inherit" fill="var(--ink)">Raw</text>
    <line x1="80" y1="58" x2="620" y2="58" stroke="var(--line)" stroke-width="2"/>
    <g fill="var(--c5)">
      <circle cx="512" cy="58" r="7"/><circle cx="458" cy="58" r="7"/><circle cx="404" cy="58" r="7"/><circle cx="386" cy="58" r="7"/><circle cx="350" cy="58" r="7"/><circle cx="332" cy="58" r="7"/><circle cx="305" cy="58" r="7"/><circle cx="269" cy="58" r="7"/><circle cx="242" cy="58" r="7"/><circle cx="152" cy="58" r="7"/>
    </g>
    <text x="20" y="152" font-size="13" font-family="inherit" fill="var(--ink)">Curved</text>
    <line x1="80" y1="148" x2="620" y2="148" stroke="var(--line)" stroke-width="2"/>
    <g fill="var(--c2)">
      <circle cx="544" cy="148" r="7"/><circle cx="506" cy="148" r="7"/><circle cx="467" cy="148" r="7"/><circle cx="454" cy="148" r="7"/><circle cx="428" cy="148" r="7"/><circle cx="416" cy="148" r="7"/><circle cx="396" cy="148" r="7"/><circle cx="371" cy="148" r="7"/><circle cx="351" cy="148" r="7"/><circle cx="287" cy="148" r="7"/>
    </g>
    <line x1="341" y1="40" x2="341" y2="76" stroke="var(--c3)" stroke-width="3"/>
    <text x="341" y="32" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">mean 69</text>
    <line x1="422" y1="130" x2="422" y2="166" stroke="var(--c3)" stroke-width="3"/>
    <text x="422" y="184" text-anchor="middle" font-size="12" font-family="inherit" fill="var(--muted)">mean 78</text>
    <text x="80" y="215" font-size="12" font-family="inherit" fill="var(--muted)">40</text>
    <text x="620" y="215" text-anchor="end" font-size="12" font-family="inherit" fill="var(--muted)">100</text>
  </svg>
  <figcaption>The bell-curve example moves the mean from 69 to 78 and pulls scores closer together (SD from about 11.2 to 8).</figcaption>
</figure>

<h2 id="compare-methods">Comparing the methods</h2>

<p>Here's how each method treats the top, middle, and bottom of our example class:</p>

<div class="table-wrap"><table class="data-table"><thead><tr><th>Method</th><th>88 becomes</th><th>70 becomes</th><th>48 becomes</th><th>New mean</th></tr></thead><tbody>
<tr><td>Raw scores</td><td>88</td><td>70</td><td>48</td><td>69.0</td></tr>
<tr><td>Flat curve (+12)</td><td>100</td><td>82</td><td>60</td><td>81.0</td></tr>
<tr><td>Add 5 points</td><td>93</td><td>75</td><td>53</td><td>74.0</td></tr>
<tr><td>Square root</td><td>93.8</td><td>83.7</td><td>69.3</td><td>82.8</td></tr>
<tr><td>Target mean 75 (+6)</td><td>94</td><td>76</td><td>54</td><td>75.0</td></tr>
<tr><td>Bell curve (78, SD 8)</td><td>91.6</td><td>78.7</td><td>63.0</td><td>78.0</td></tr>
</tbody></table></div>

<p>The square-root and bell curves help the lowest score the most. The additive methods treat everyone identically. None of these methods change the ranking of students, which is one test of whether a curve is behaving sensibly.</p>

[[tool:grade-curve-calculator]]

<h2 id="choosing-a-method">How to choose the right curve</h2>

<ul>
<li><strong>One or two bad questions?</strong> Drop or re-score those questions, or add their point value to everyone.</li>
<li><strong>The whole test ran hard, but one student did great?</strong> Shift to a target mean rather than a flat curve, so one outlier doesn't cap the adjustment.</li>
<li><strong>Low scores are clustered far below the rest?</strong> A square-root curve lifts them most without inflating the top.</li>
<li><strong>A large class and a department grade target?</strong> A bell curve with a target mean and SD may match the policy, if the class is big enough for the statistics to be stable.</li>
</ul>

<p>Whatever you choose, decide before you look at individual names, apply it to every student, and write down the rule. If a parent or student asks, you can show the exact formula.</p>

<figure class="figure">
  <img src="/assets/img/photos/teacher-chalkboard.webp" width="1200" height="743" alt="Teacher writing on a chalkboard at the front of the class" loading="lazy">
  <figcaption>Explaining the curve's formula to the class builds trust and heads off grade disputes.</figcaption>
</figure>

<h2 id="step-by-step">Curving a test step by step</h2>

<p>Whichever method you pick, the workflow is the same. Following it in order keeps the process consistent from one test to the next.</p>

<ol class="steps">
<li><strong>Score every test first.</strong> Record raw scores before thinking about a curve, so the curve can't influence how you grade individual answers.</li>
<li><strong>Look at the numbers.</strong> Find the mean, median, highest, and lowest score. Compare the mean with how the class usually performs.</li>
<li><strong>Check for flawed questions.</strong> If most students missed the same item, review it. Fixing one question may solve the problem without a curve.</li>
<li><strong>Choose and record a method.</strong> Write down the rule (for example, "square-root curve, capped at 100") before applying it.</li>
<li><strong>Apply it to everyone.</strong> Use a spreadsheet or the curve calculator so no score is missed or rounded differently.</li>
<li><strong>Enter both scores.</strong> Keep the raw score in your records alongside the curved one in case questions come up later.</li>
<li><strong>Tell students what you did.</strong> A one-line explanation of the method avoids confusion and grade disputes.</li>
</ol>

<p>Rounding is worth deciding ahead of time too. Rounding curved scores to the nearest whole number is common, but whatever you choose, apply it the same way to every student.</p>

<h2 id="fairness">Is curving fair? Pros, cons, and alternatives</h2>

<div class="compare"><div class="compare-col"><h4>Arguments for curving</h4><ul><li>Corrects for a test that was harder than intended</li><li>Keeps grades consistent across test versions or sections</li><li>Reduces the impact of one bad testing day for the whole class</li></ul></div><div class="compare-col"><h4>Arguments against</h4><ul><li>Can hide a test-design or teaching problem</li><li>Rank-based curves make students compete</li><li>Grades can stop reflecting what students actually know</li></ul></div></div>

<p>Many teachers prefer alternatives that avoid curving altogether: test corrections for partial credit, retakes on missed standards, or dropping the lowest test score. Some schools have moved to <a href="/blog/standards-based-grading">standards-based grading</a>, where grades reflect mastery of specific skills rather than points, which makes curving largely unnecessary.</p>

<p>If you do curve, two habits keep it fair. First, apply the same rule to every student. Second, cap scores at 100 unless you've announced otherwise, because scores above 100 make one test count more toward the final grade than its weight suggests.</p>

<h2 id="for-students">What a curve means for students</h2>

<p>If your teacher announces a curve, ask which method they're using. A flat curve or added points means everyone gains the same amount. A square-root curve means lower scores gain the most. A bell curve means your new score depends on how you did compared to classmates.</p>

<p>Once you know your curved score, plug it into the <a href="/weighted-grade-calculator">weighted grade calculator</a> to see how it changes your overall class grade, or use the <a href="/final-grade-calculator">final grade calculator</a> to see what you need on the next big exam.</p>

<h2 id="quick-grading-tools">Tools that speed up grading</h2>

<p>Curving is the last step. Getting raw scores fast is the first. The <a href="/easy-grader">EZ grader</a> builds a chart of number wrong to percentage for any test length, so you can score a stack of papers quickly. Many teachers also like a dedicated gradebook for recording raw and curved scores side by side.</p>

[[product:teacher-gradebook]]

<h2 id="summary">The bottom line</h2>

<p>Learning how to curve grades comes down to picking the method that fixes the actual problem. Add points or use a flat curve for a test that ran a bit hard, a square-root curve to lift low scores, a target mean for a principled adjustment, and a bell curve only when you need to control both the average and the spread.</p>

<p>Paste your class's scores into the <a href="/grade-curve-calculator">grade curve calculator</a> to compare all five methods instantly, with an original-vs-curved table, the new class average, and an option to cap at 100.</p>
HTML,
];
