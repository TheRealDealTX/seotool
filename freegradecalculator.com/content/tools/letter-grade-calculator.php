<?php
return [
  'h1'          => 'Letter Grade Calculator',
  'meta_title'  => 'Letter Grade Calculator – Percentage to Letter Grade',
  'description' => 'Free letter grade calculator: convert any percentage to a letter grade (A+ to F) and 4.0 GPA points using the standard US grading scale, with the full table.',
  'lead'        => 'Type a percentage to see its letter grade and GPA points on the standard US grading scale.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the letter grade calculator</h2>
<p>Your teacher posts an 88.5%. Is that a B+ or an A-? This letter grade calculator converts any percentage into a letter grade and the matching GPA points.</p>
<ol class="steps">
  <li><strong>Enter your percentage.</strong> Use your score on a test or your overall class grade.</li>
  <li><strong>Read the letter grade.</strong> The result shows the letter (A+ through F) and its 4.0-scale GPA points.</li>
  <li><strong>Check the table.</strong> The full grading scale appears below, with your row highlighted so you can see how close you are to the next letter.</li>
</ol>

<h2 id="grading-scale">The standard US grading scale</h2>
<p>This is the plus/minus scale used by many US high schools and colleges. It's the scale the calculator uses.</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Letter</th><th>Percentage</th><th>GPA points</th></tr></thead><tbody>
<tr><td>A+</td><td>97–100</td><td>4.0</td></tr>
<tr><td>A</td><td>93–96</td><td>4.0</td></tr>
<tr><td>A-</td><td>90–92</td><td>3.7</td></tr>
<tr><td>B+</td><td>87–89</td><td>3.3</td></tr>
<tr><td>B</td><td>83–86</td><td>3.0</td></tr>
<tr><td>B-</td><td>80–82</td><td>2.7</td></tr>
<tr><td>C+</td><td>77–79</td><td>2.3</td></tr>
<tr><td>C</td><td>73–76</td><td>2.0</td></tr>
<tr><td>C-</td><td>70–72</td><td>1.7</td></tr>
<tr><td>D+</td><td>67–69</td><td>1.3</td></tr>
<tr><td>D</td><td>63–66</td><td>1.0</td></tr>
<tr><td>D-</td><td>60–62</td><td>0.7</td></tr>
<tr><td>F</td><td>Below 60</td><td>0.0</td></tr>
</tbody></table></div>

<h2 id="how-it-works">How the conversion works</h2>
<p>There's no arithmetic formula here, just a lookup. The calculator finds the range your percentage falls into and returns that letter.</p>
<div class="formula">Letter grade = the scale row where lower cutoff ≤ your % ≤ upper cutoff</div>
<p>Each full letter spans 10 points (90s are A's, 80s are B's), and each letter is split into thirds for plus and minus. The top of each band (7–9) is a plus, the middle (3–6) is plain, and the bottom (0–2) is a minus. The A band is the exception: 97–100 is A+, but both A+ and A are worth 4.0 on most college scales.</p>

<div class="example-box"><h4>Worked examples</h4>
<p><strong>84%</strong> falls in 83–86, so it's a <strong>B</strong> worth <strong>3.0</strong> GPA points.</p>
<p><strong>91%</strong> falls in 90–92, so it's an <strong>A-</strong> worth <strong>3.7</strong>.</p>
<p><strong>78%</strong> falls in 77–79, so it's a <strong>C+</strong> worth <strong>2.3</strong>.</p>
</div>

<h2 id="decimals">What about decimals like 89.5?</h2>
<p>The scale above uses whole numbers, which leaves gaps like 89.5 or 92.7. Schools handle these differently. Many teachers round to the nearest whole number, so 89.5 becomes 90 (an A-), while others truncate, so 89.9 stays a B+. If you're right on the line, check your syllabus or ask.</p>

<h2 id="scales-vary">Grading scales vary by school</h2>
<ul>
  <li><strong>10-point scale without plus/minus:</strong> A 90–100, B 80–89, C 70–79, D 60–69, F below 60. Same letter bands, just no pluses or minuses.</li>
  <li><strong>7-point scale:</strong> Some districts use A 93–100, B 85–92, C 77–84, D 70–76.</li>
  <li><strong>A+ worth more than 4.0:</strong> A few colleges count A+ as 4.3. Most cap it at 4.0.</li>
</ul>
<p>If your school's scale differs, use the table above as a general guide and your handbook for the official answer.</p>

<h2 id="next-letter">How close are you to the next letter?</h2>
<p>The highlighted row in the table shows where you stand, but it also shows what you're aiming for. Each letter band is only three or four points wide, so a single assignment can push you over a line.</p>
<div class="example-box"><h4>Example</h4>
<p>You have an 86% in a class. That's a B (3.0), but the B+ band starts at 87, just one point away. Moving from B to B+ raises that class's GPA points from 3.0 to 3.3.</p>
<p>Across three classes with grades of B+, A-, and B, the unweighted average is (3.3 + 3.7 + 3.0) ÷ 3 = 3.33. Bump the B up to a B+ and it becomes (3.3 + 3.7 + 3.3) ÷ 3 = 3.43.</p>
</div>
<p>Small moves near a cutoff add up, which is why it pays to know the exact boundaries for your school.</p>

<h2 id="next-steps">From letter grades to GPA</h2>
<p>Once you have letter grades for every class, you can turn them into a GPA. College students can use the <a href="/gpa-calculator">GPA calculator</a>, which weights each letter by credit hours. If you want to go the other way, from a GPA back to a percentage range, the <a href="/gpa-converter">GPA converter</a> does both directions. Our guide on <a href="/blog/how-to-convert-percentage-to-gpa">how to convert percentage to GPA</a> explains the full process.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Look at how far you are from the next cutoff, not just the letter. An 86% and an 83% are both B's, but the 86 is one good quiz away from a B+.</p></div>
HTML,
  'faqs'        => [
    ["What letter grade is an 85%?", "On the standard US scale, 85% is a B (83–86), worth 3.0 GPA points."],
    ["Is an 89 a B+ or an A-?", "An 89 is a B+ (87–89). An A- starts at 90. Some teachers round 89.5 or higher up to 90, so check your teacher's rounding policy."],
    ["What percentage is a C?", "A plain C is 73–76%. C+ is 77–79% and C- is 70–72%."],
    ["What is a failing grade?", "On this scale, anything below 60% is an F, worth 0.0 GPA points. Some schools set the passing line differently."],
    ["Is an A+ worth more than an A in GPA?", "On the scale this calculator uses, both A+ and A are worth 4.0. A few colleges give A+ a 4.3, so check your school's policy."],
  ],
];
