<?php
return [
  'h1'          => 'CGPA to Percentage Calculator',
  'meta_title'  => 'CGPA to Percentage Calculator – Convert CGPA to %',
  'description' => 'Free CGPA to percentage calculator: convert a 10-point CGPA to a percentage with the 9.5 multiplier (editable), or turn a percentage back into CGPA.',
  'lead'        => 'Convert a 10-point CGPA to a percentage using the common 9.5 multiplier, or turn a percentage back into CGPA.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the CGPA to percentage calculator</h2>
<p>CGPA (cumulative grade point average) on a 10-point scale is used by CBSE schools and many universities in India and other countries. When an application or form asks for a percentage, you need to convert it. This CGPA to percentage calculator handles both directions.</p>
<ol class="steps">
  <li><strong>Enter your CGPA.</strong> Use the value on your marksheet or transcript, such as 8.4.</li>
  <li><strong>Check the multiplier.</strong> It's set to 9.5, the CBSE convention. If your university publishes a different multiplier, change it.</li>
  <li><strong>Read your percentage.</strong> The result appears instantly.</li>
  <li><strong>Need the reverse?</strong> Enter a percentage to convert it back to CGPA using the same multiplier.</li>
</ol>

<h2 id="formula">The CGPA to percentage formula</h2>
<div class="formula">Percentage = CGPA × 9.5</div>
<p>To convert the other way:</p>
<div class="formula">CGPA = Percentage ÷ 9.5</div>
<p>The 9.5 multiplier comes from CBSE, which has used it as an indicative conversion for its 10-point grading system. Many students and institutions use it as a general rule, but it isn't universal.</p>

<div class="example-box"><h4>Worked examples</h4>
<p><strong>CGPA to percentage:</strong> 8.4 × 9.5 = <strong>79.8%</strong></p>
<p><strong>Percentage to CGPA:</strong> 76 ÷ 9.5 = <strong>8.0 CGPA</strong></p>
<p><strong>Custom multiplier:</strong> If your university says to multiply by 10, then 8.4 × 10 = <strong>84%</strong>. Same CGPA, a 4.2-point difference, which is why using your institution's formula matters.</p>
</div>

<h2 id="quick-table">Quick CGPA to percentage table (× 9.5)</h2>
<div class="table-wrap"><table class="data-table"><thead><tr><th>CGPA</th><th>Percentage</th><th>CGPA</th><th>Percentage</th></tr></thead><tbody>
<tr><td>10.0</td><td>95.0%</td><td>7.5</td><td>71.25%</td></tr>
<tr><td>9.5</td><td>90.25%</td><td>7.0</td><td>66.5%</td></tr>
<tr><td>9.0</td><td>85.5%</td><td>6.5</td><td>61.75%</td></tr>
<tr><td>8.5</td><td>80.75%</td><td>6.0</td><td>57.0%</td></tr>
<tr><td>8.0</td><td>76.0%</td><td>5.5</td><td>52.25%</td></tr>
</tbody></table></div>
<p>Notice that a perfect 10.0 converts to 95%, not 100%. That's a feature of the 9.5 convention, not an error.</p>

<h2 id="minimum-percentage">Meeting a minimum percentage requirement</h2>
<p>Many job postings, scholarships, and admission notices set an eligibility cutoff like "minimum 60%" or "at least 75% aggregate." Use the reverse conversion to see the CGPA that cutoff corresponds to.</p>
<div class="example-box"><h4>Example</h4>
<p>A program requires at least 60%. Using the 9.5 multiplier: 60 ÷ 9.5 = <strong>6.32 CGPA</strong>.</p>
<p>For a 75% cutoff: 75 ÷ 9.5 = <strong>7.89 CGPA</strong>. A student with a 7.8 CGPA would convert to 74.1%, just under the line, while a 7.9 would convert to 75.05%.</p>
</div>
<p>When you're that close to a cutoff, check whether the organization accepts your university's official conversion, since a different formula could put you on the other side of the line.</p>

<h2 id="university-formulas">Your university may use its own formula</h2>
<p>The 9.5 rule is a convention, not a law. Many universities and boards publish their own conversion, which might use a different multiplier, subtract a constant before multiplying, or provide a lookup table. Some print the official percentage equivalent right on the transcript.</p>
<p>When a percentage is going on an official application, use the formula your institution publishes. If it's a simple multiplier, enter it in the calculator. If it's something else, follow your institution's instructions directly. When you can't find any guidance, CGPA × 9.5 is the widely recognized default, and it's a good idea to note on the form which conversion you used.</p>

<h2 id="cgpa-vs-us-gpa">CGPA vs. the US 4.0 GPA</h2>
<p>A 10-point CGPA is not the same as a US GPA, and you can't get one by simply scaling the other. US colleges and graduate programs that receive international transcripts often rely on credential evaluation services or their own admissions rules to interpret them.</p>
<p>If you're curious how percentages map to the US scale, the <a href="/gpa-converter">GPA converter</a> shows the standard US percentage-to-4.0 table, and <a href="/blog/what-is-gpa">what is GPA</a> explains how the US system works. Treat any such comparison as informal. Grading standards and percentage distributions differ a lot between countries.</p>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Using SGPA instead of CGPA.</strong> SGPA covers a single semester. Most forms want the cumulative figure.</li>
  <li><strong>Assuming 10.0 = 100%.</strong> Under the 9.5 convention, it's 95%.</li>
  <li><strong>Ignoring your university's rule.</strong> If your institution publishes a formula, it overrides the general convention.</li>
  <li><strong>Rounding before converting.</strong> Convert the exact CGPA (8.37, not 8.4), then round the percentage if the form requires it.</li>
</ul>
HTML,
  'faqs'        => [
    ["How do I convert CGPA to percentage?", "Multiply your CGPA by 9.5, the CBSE convention. For example, 8.4 × 9.5 = 79.8%. If your university publishes a different formula, use that instead."],
    ["Why multiply by 9.5?", "CBSE introduced 9.5 as an indicative multiplier for its 10-point grading system. Many schools and universities adopted it as a general rule, but not all of them."],
    ["How do I convert percentage to CGPA?", "Divide the percentage by 9.5. For example, 76% ÷ 9.5 = 8.0 CGPA."],
    ["What percentage is a 9 CGPA?", "Using the 9.5 multiplier, a 9.0 CGPA equals 85.5%."],
    ["Can I change the multiplier?", "Yes. The multiplier is editable, so if your university says to multiply by 10 or another number, enter it and the result updates."],
    ["Can I convert CGPA to a US 4.0 GPA here?", "No. A 10-point CGPA doesn't convert directly to a US GPA. US schools usually rely on credential evaluators or their own rules for international transcripts."],
  ],
];
