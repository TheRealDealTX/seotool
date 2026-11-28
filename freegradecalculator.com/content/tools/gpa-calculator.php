<?php
return [
  'h1'          => 'GPA Calculator',
  'meta_title'  => 'GPA Calculator – College Semester & Cumulative GPA',
  'description' => 'Free college GPA calculator: enter each course\'s letter grade and credit hours to get your semester GPA, quality points and an updated cumulative GPA.',
  'lead'        => 'Enter your courses, letter grades, and credit hours to calculate your semester GPA on a 4.0 scale, and optionally your new cumulative GPA.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the GPA calculator</h2>
<p>This GPA calculator is built for college students on a 4.0 scale, where each course counts according to its credit hours. It works for any term: fall, spring, summer, or quarter.</p>
<ol class="steps">
  <li><strong>Add a row for each course.</strong> The course name is optional but helps you keep track.</li>
  <li><strong>Choose the letter grade.</strong> Pick from A+ through F.</li>
  <li><strong>Enter the credit hours.</strong> Usually 3 or 4 for lecture courses and 1 for labs or PE. Your registration page lists them.</li>
  <li><strong>Read your results.</strong> You'll see your semester GPA, total credits, and total quality points.</li>
  <li><strong>Optional: update your cumulative GPA.</strong> Enter your previous cumulative GPA and the credits behind it to see your new cumulative GPA after this term.</li>
</ol>

<h2 id="formula">The GPA formula</h2>
<p>Each letter grade has a point value. Multiply it by the course credits to get quality points, then divide total quality points by total credits.</p>
<div class="formula">GPA = Σ (grade points × credits) ÷ Σ credits</div>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Letter</th><th>Points</th><th>Letter</th><th>Points</th></tr></thead><tbody>
<tr><td>A+ / A</td><td>4.0</td><td>C</td><td>2.0</td></tr>
<tr><td>A-</td><td>3.7</td><td>C-</td><td>1.7</td></tr>
<tr><td>B+</td><td>3.3</td><td>D+</td><td>1.3</td></tr>
<tr><td>B</td><td>3.0</td><td>D</td><td>1.0</td></tr>
<tr><td>B-</td><td>2.7</td><td>D-</td><td>0.7</td></tr>
<tr><td>C+</td><td>2.3</td><td>F</td><td>0.0</td></tr>
</tbody></table></div>

<div class="example-box"><h4>Worked example</h4>
<p>A 15-credit semester:</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Course</th><th>Grade</th><th>Credits</th><th>Quality points</th></tr></thead><tbody>
<tr><td>English Composition</td><td>A-</td><td>3</td><td>3.7 × 3 = 11.1</td></tr>
<tr><td>Calculus I</td><td>B+</td><td>4</td><td>3.3 × 4 = 13.2</td></tr>
<tr><td>General Chemistry</td><td>B</td><td>4</td><td>3.0 × 4 = 12.0</td></tr>
<tr><td>US History</td><td>A</td><td>3</td><td>4.0 × 3 = 12.0</td></tr>
<tr><td>Fitness</td><td>A</td><td>1</td><td>4.0 × 1 = 4.0</td></tr>
</tbody></table></div>
<p>Total quality points: 52.3. Total credits: 15. Semester GPA: 52.3 ÷ 15 = <strong>3.49</strong>.</p>
<p><strong>Cumulative update:</strong> With a previous 3.20 cumulative GPA over 45 credits, prior quality points are 3.20 × 45 = 144. New cumulative GPA = (144 + 52.3) ÷ (45 + 15) = 196.3 ÷ 60 = <strong>3.27</strong>.</p>
</div>

<h2 id="credits-matter">Why credit hours matter</h2>
<p>A 4-credit B pulls your GPA more than a 1-credit A. In the example, the two 4-credit courses produce over half the quality points. A simple average of the five grade values (3.7, 3.3, 3.0, 4.0, 4.0) would be 3.60, noticeably higher than the true 3.49, because it ignores credits.</p>

<h2 id="one-grade">How much can one grade change your GPA?</h2>
<p>Try changing a single grade in the calculator to see its effect. In the example above, if Calculus I had been an A- instead of a B+, that course would earn 3.7 × 4 = 14.8 quality points instead of 13.2, adding 1.6 points to the total.</p>
<p>New semester GPA: 53.9 ÷ 15 = <strong>3.59</strong>, up from 3.49. One grade step in one 4-credit course moved the semester GPA by a tenth of a point. A one-step change in the 1-credit Fitness course would move it by less than 0.03.</p>
<p>That's a useful way to decide where to focus near the end of a term: put extra effort into high-credit courses that are close to the next letter grade.</p>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Including pass/fail courses.</strong> At most colleges, P/NP or S/U courses don't affect GPA. Leave them out unless your school says otherwise.</li>
  <li><strong>Counting withdrawals.</strong> A W usually doesn't count in GPA. An F does.</li>
  <li><strong>Ignoring repeat policies.</strong> Some schools replace the old grade when you retake a course; others average both. Check your registrar's policy.</li>
  <li><strong>Assuming A+ is 4.3.</strong> This calculator uses A+ = 4.0, the most common college policy. A few schools award 4.3.</li>
  <li><strong>Mixing up term and cumulative GPA.</strong> Your semester GPA covers one term. Your cumulative GPA covers every graded credit you've taken.</li>
</ul>

<h2 id="related">Planning your next semester</h2>
<p>If you're tracking several past terms, the <a href="/cumulative-gpa-calculator">cumulative GPA calculator</a> lets you add each one. Trying to reach a GPA goal for graduation, scholarships, or grad school? The <a href="/target-gpa-calculator">target GPA calculator</a> tells you the GPA you need on your remaining credits. New to all this? Start with <a href="/blog/what-is-gpa">what GPA is and how it's determined</a>.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Your GPA becomes harder to move as credits pile up. A strong semester early in college lifts your cumulative GPA much more than the same semester senior year.</p></div>
HTML,
  'faqs'        => [
    ["How do I calculate my college GPA?", "Multiply each course's grade points by its credit hours, add those quality points, and divide by your total credits. For 52.3 quality points over 15 credits, your GPA is 3.49."],
    ["What are quality points?", "Quality points are grade points multiplied by credit hours. A B+ (3.3) in a 4-credit course earns 13.2 quality points."],
    ["Is an A+ worth more than 4.0?", "Not in this calculator. It uses A+ = 4.0, which is the most common college policy. Some schools award 4.3 for an A+."],
    ["Can I calculate my cumulative GPA here?", "Yes. Enter your previous cumulative GPA and the credits it covers, and the calculator combines them with this term to show your new cumulative GPA."],
    ["Do pass/fail classes count toward GPA?", "Usually not. Most colleges exclude pass/fail courses from GPA, so leave them out unless your school counts them."],
    ["Is this for high school GPA too?", "It works for any unweighted 4.0 scale. If your high school adds points for Honors or AP classes, use the high school GPA calculator to see both weighted and unweighted GPA."],
  ],
];
