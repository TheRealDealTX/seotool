<?php
return [
  'h1'          => 'GPA Converter',
  'meta_title'  => 'GPA Converter – Percentage & Letter Grade to 4.0 GPA',
  'description' => 'Free GPA converter: turn a percentage or letter grade into 4.0-scale GPA points, or convert a GPA back to a typical letter grade and percentage range.',
  'lead'        => 'Convert a percentage or letter grade to a 4.0 GPA, or turn a GPA back into its typical letter grade and percentage range.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the GPA converter</h2>
<p>Grades show up in different formats: a percentage on a test, a letter on a report card, a GPA on a transcript. This GPA converter translates between them on the standard US 4.0 scale.</p>
<ol class="steps">
  <li><strong>Choose a direction.</strong> Convert a percentage or letter grade to GPA, or a GPA to a letter and percentage range.</li>
  <li><strong>Enter your value.</strong> For example, 88 (a percentage), B+ (a letter), or 3.3 (a GPA).</li>
  <li><strong>Read the result.</strong> Percentages and letters convert to 4.0 GPA points and the matching letter. A GPA converts to its typical letter grade and percentage range.</li>
  <li><strong>Check the table.</strong> The full conversion table is shown below the converter for quick reference.</li>
</ol>

<h2 id="conversion-table">Percentage to GPA conversion table</h2>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Percentage</th><th>Letter</th><th>4.0 GPA</th></tr></thead><tbody>
<tr><td>97–100</td><td>A+</td><td>4.0</td></tr>
<tr><td>93–96</td><td>A</td><td>4.0</td></tr>
<tr><td>90–92</td><td>A-</td><td>3.7</td></tr>
<tr><td>87–89</td><td>B+</td><td>3.3</td></tr>
<tr><td>83–86</td><td>B</td><td>3.0</td></tr>
<tr><td>80–82</td><td>B-</td><td>2.7</td></tr>
<tr><td>77–79</td><td>C+</td><td>2.3</td></tr>
<tr><td>73–76</td><td>C</td><td>2.0</td></tr>
<tr><td>70–72</td><td>C-</td><td>1.7</td></tr>
<tr><td>67–69</td><td>D+</td><td>1.3</td></tr>
<tr><td>63–66</td><td>D</td><td>1.0</td></tr>
<tr><td>60–62</td><td>D-</td><td>0.7</td></tr>
<tr><td>Below 60</td><td>F</td><td>0.0</td></tr>
</tbody></table></div>

<h2 id="how-it-works">How the conversion works</h2>
<p>A single grade converts by lookup: find the percentage range, read the letter, read the GPA points.</p>
<div class="formula">Percentage → letter (by range) → 4.0 grade points</div>
<p>Going the other way, a GPA maps back to the letter with that point value and its percentage range. Keep in mind that a GPA is usually an average of many classes, so it describes a typical grade, not any one grade you actually earned.</p>

<div class="example-box"><h4>Worked examples</h4>
<p><strong>88%</strong> → falls in 87–89 → <strong>B+</strong> → <strong>3.3</strong></p>
<p><strong>A-</strong> → <strong>3.7</strong> (90–92%)</p>
<p><strong>3.0 GPA</strong> → typical of a <strong>B</strong> average → roughly <strong>83–86%</strong></p>
</div>

<h2 id="average-of-grades">Converting a whole report card</h2>
<p>To turn several percentages into one GPA, convert each class first, then average the grade points, weighting by credits if your classes have different credit values.</p>
<p>For example, classes at 95%, 88%, 84%, and 91% (equal credits) convert to 4.0, 3.3, 3.0, and 3.7. Their average is 14.0 ÷ 4 = <strong>3.5</strong>.</p>
<p>Don't average the percentages and then convert. The average of those four percentages is 89.5%, which could read as a B+ (3.3) or an A- (3.7) depending on rounding, and neither matches the true 3.5. For a full multi-class calculation with credits, use the <a href="/gpa-calculator">GPA calculator</a>.</p>

<h2 id="when-to-use">When a GPA converter comes in handy</h2>
<ul>
  <li><strong>Forms that ask for a 4.0 GPA.</strong> Scholarship, internship, and program applications sometimes ask for a GPA when your school reports percentages. Convert each class, then average the grade points. If the form gives its own instructions, follow those.</li>
  <li><strong>Checking a single class.</strong> Want to know what an 82% in chemistry does to your GPA? It's a B-, worth 2.7.</li>
  <li><strong>Reading a transcript.</strong> If someone tells you they have a 3.7, the reverse conversion shows that's an A- average, typically 90–92%.</li>
</ul>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Converting an average percentage.</strong> As shown above, convert each class first, then average.</li>
  <li><strong>Treating a GPA as an exact percentage.</strong> A GPA describes a range, not a single score.</li>
  <li><strong>Forgetting credits.</strong> A 4-credit class counts more than a 1-credit class in a real GPA.</li>
  <li><strong>Mixing scales.</strong> A weighted high school GPA (where AP classes can earn a 5.0) won't line up with this unweighted 4.0 table. Convert unweighted grades only.</li>
</ul>

<h2 id="scales-vary">Scales vary by school</h2>
<ul>
  <li><strong>Different cutoffs:</strong> Some schools use 90–100 for every A, or a 7-point scale where an A starts at 93.</li>
  <li><strong>No plus/minus:</strong> Some schools give a B 3.0 whether it's an 80 or an 89.</li>
  <li><strong>A+ above 4.0:</strong> A few colleges count an A+ as 4.3.</li>
  <li><strong>Weighted GPAs:</strong> High schools that add points for Honors and AP classes can produce GPAs above 4.0. Use the <a href="/high-school-gpa-calculator">high school GPA calculator</a> for that.</li>
</ul>
<p>When an official GPA matters, such as for an application or scholarship, use the GPA on your transcript. Our article on <a href="/blog/how-to-convert-percentage-to-gpa">how to convert percentage to GPA</a> walks through more scenarios.</p>
HTML,
  'faqs'        => [
    ["What GPA is an 85%?", "On the standard US scale, 85% is a B, which equals 3.0 on a 4.0 scale."],
    ["What percentage is a 3.5 GPA?", "A 3.5 sits between a B+ (3.3, 87–89%) and an A- (3.7, 90–92%), so it roughly corresponds to the high 80s to around 90%. Because GPA is an average, there's no exact single percentage."],
    ["What letter grade is a 3.0 GPA?", "A 3.0 GPA equals a B average, which typically corresponds to 83–86%."],
    ["How do I convert a percentage to a 4.0 GPA?", "Find the letter grade for your percentage, then look up its grade points: for example, 91% is an A-, worth 3.7."],
    ["Is a 4.0 GPA the same as 100%?", "No. A 4.0 means straight A's, which on this scale covers anything from 93% to 100%. A+ and A are both 4.0."],
  ],
];
