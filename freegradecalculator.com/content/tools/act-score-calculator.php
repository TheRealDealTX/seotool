<?php
return [
  'h1'          => 'ACT Score Calculator',
  'meta_title'  => 'ACT Score Calculator – Enhanced ACT Composite & STEM',
  'description' => 'Free ACT score calculator for the enhanced ACT: enter English, Math, and Reading scores to get your composite, add Science for STEM, or use legacy scoring.',
  'lead'        => 'Enter your ACT section scores (1–36) to calculate your composite under the enhanced ACT or the legacy four-section format, plus your STEM score.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the ACT score calculator</h2>
<ol class="steps">
  <li><strong>Enter your section scores.</strong> Type your English, Math, and Reading scale scores, each from 1 to 36.</li>
  <li><strong>Add Science if you took it.</strong> Science is optional on the enhanced ACT. Enter it to see your STEM score.</li>
  <li><strong>Choose the scoring format.</strong> By default the calculator uses the enhanced ACT, where the composite comes from English, Math, and Reading. Turn on "include Science (legacy ACT)" if you want the older four-section composite, for example to compare with a score from before the change.</li>
  <li><strong>Read your results.</strong> You get your composite score and, if you entered Math and Science, your STEM score.</li>
</ol>

<h2 id="enhanced-act">What changed with the enhanced ACT</h2>
<p>ACT rolled out a shorter, updated version of the test starting in spring 2025 for online national test dates and on all national test dates from September 2025, with school-day testing following. The biggest scoring change: <strong>the composite is now the rounded average of English, Math, and Reading only</strong>. Science became optional and is reported as a separate score, along with a STEM score that combines Math and Science. The optional Writing test is also still reported separately.</p>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Section</th><th>Enhanced ACT</th><th>In the composite?</th></tr></thead>
<tbody>
<tr><td>English</td><td>50 questions, 35 min</td><td>Yes</td></tr>
<tr><td>Math</td><td>45 questions, 50 min</td><td>Yes</td></tr>
<tr><td>Reading</td><td>36 questions, 40 min</td><td>Yes</td></tr>
<tr><td>Science (optional)</td><td>40 questions, 40 min</td><td>No (reported separately and in STEM)</td></tr>
</tbody></table></div>
<p>Test details can change, so check act.org for the latest official specifications and for each college's policy on whether it wants Science scores.</p>

<h2 id="formula">ACT composite formula</h2>
<div class="formula">Enhanced composite = (English + Math + Reading) ÷ 3, rounded</div>
<div class="formula">Legacy composite = (English + Math + Reading + Science) ÷ 4, rounded</div>
<div class="formula">STEM score = (Math + Science) ÷ 2, rounded</div>
<p>Scores are rounded to the nearest whole number, and a fraction of exactly .5 rounds up. So an average of 27.5 becomes 28, while 27.25 becomes 27.</p>

<div class="example-box"><h4>Worked example</h4>
<p>Section scores: English 28, Math 25, Reading 30, Science 26.</p>
<p><strong>Enhanced composite:</strong> (28 + 25 + 30) ÷ 3 = 83 ÷ 3 = 27.67, which rounds to <strong>28</strong>.</p>
<p><strong>Legacy composite:</strong> (28 + 25 + 30 + 26) ÷ 4 = 109 ÷ 4 = 27.25, which rounds to <strong>27</strong>.</p>
<p><strong>STEM score:</strong> (25 + 26) ÷ 2 = 25.5, which rounds up to <strong>26</strong>.</p>
</div>
<p>As the example shows, the same student can get a different composite under each format, which is why the toggle is useful when comparing an older score report with a newer one.</p>

<h2 id="what-if">Using the calculator for "what if" planning</h2>
<p>Because the composite is an average, you can work backward from a goal. Multiply your target composite by 3 to get the section total you need, then subtract 1 so you still round up: a 30 requires an average of at least 29.5, which on three sections means a total of 89 (89 ÷ 3 = 29.67). If your current sections add up to 83, you need 6 more points spread across English, Math, and Reading.</p>

<h2 id="tips">Tips for raising your ACT composite</h2>
<ul>
  <li><strong>Find the cheapest points.</strong> Because the composite is an average of three sections, raising your lowest section by 3 points lifts your composite by 1. Plug in "what if" scores to see which section gives you the biggest jump.</li>
  <li><strong>Watch the rounding line.</strong> If your average is 27.33, you need only 1 more point in a single section to reach 27.67 and a rounded 28. If it is 27.0, you need 2 more points total to reach 28.</li>
  <li><strong>Decide on Science early.</strong> If you are applying to engineering, science, or other STEM programs, check whether those colleges want a Science or STEM score before you register.</li>
  <li><strong>Ask about superscoring.</strong> Many colleges superscore the ACT, combining your best section scores from different test dates. Policies vary, so check each school's admissions page.</li>
  <li><strong>Compare with the SAT.</strong> If you have taken both tests, see where your SAT stands with the <a href="/sat-superscore-calculator">SAT superscore calculator</a> and read <a href="/blog/what-is-a-good-sat-score">what is a good SAT score</a> for context on score ranges.</li>
</ul>
HTML,
  'faqs'        => [
    ['How is the ACT composite score calculated now?', 'On the enhanced ACT, the composite is the average of your English, Math, and Reading scores, rounded to the nearest whole number. Science is optional and does not count toward the composite.'],
    ['Is Science still on the ACT?', 'Yes, but it is optional on the enhanced ACT. If you take it, you receive a separate Science score and a STEM score that combines Math and Science.'],
    ['How is the ACT STEM score calculated?', 'The STEM score is the average of your Math and Science scores, rounded to the nearest whole number. For example, Math 25 and Science 26 give a STEM score of 26.'],
    ['Does the ACT round composite scores up?', 'The composite is rounded to the nearest whole number, and exactly .5 rounds up. An average of 27.5 becomes 28, while 27.25 becomes 27.'],
    ['Can I calculate my composite the old way with Science?', 'Yes. Turn on the "include Science (legacy ACT)" option to average all four sections, which matches the composite used before the enhanced ACT.'],
    ['Do colleges require the ACT Science section?', 'It depends on the college and sometimes the program. Some STEM programs may want a Science or STEM score, so check each school\'s testing policy.'],
  ],
];
