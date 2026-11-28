<?php
return [
  'h1'          => 'SAT Superscore Calculator',
  'meta_title'  => 'SAT Superscore Calculator – Combine Your Best Scores',
  'description' => 'Free SAT superscore calculator: enter Reading & Writing and Math scores from up to 4 test dates to see your best sections, superscore, and top single sitting.',
  'lead'        => 'Enter your SAT section scores from up to four test dates to see your best Reading and Writing and Math scores, your superscore, and your best single-sitting total.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the SAT superscore calculator</h2>
<ol class="steps">
  <li><strong>Enter your first test date.</strong> Type your Reading and Writing score and your Math score. Each section is scored from 200 to 800.</li>
  <li><strong>Add more test dates.</strong> Fill in up to four sittings. Leave unused rows blank.</li>
  <li><strong>Read your results.</strong> The calculator shows your best Reading and Writing score, your best Math score, your superscore (the sum of those two bests), and your best single-sitting total.</li>
</ol>

<h2 id="what-is-superscore">What is an SAT superscore?</h2>
<p>A superscore combines your highest section scores across every SAT you have taken. Instead of looking only at one test day, a college that superscores takes your best Reading and Writing score from any date and adds it to your best Math score from any date.</p>
<div class="formula">Superscore = Best Reading and Writing + Best Math</div>
<p>Your best single sitting is simply the highest total score you earned on one test date. Colleges that do not superscore usually look at this number instead.</p>

<div class="example-box"><h4>Worked example</h4>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Test date</th><th>Reading and Writing</th><th>Math</th><th>Total</th></tr></thead>
<tbody>
<tr><td>March</td><td>610</td><td>650</td><td>1260</td></tr>
<tr><td>June</td><td>660</td><td>620</td><td>1280</td></tr>
<tr><td>August</td><td>640</td><td>690</td><td>1330</td></tr>
</tbody></table></div>
<p>Best Reading and Writing: <strong>660</strong> (June). Best Math: <strong>690</strong> (August).</p>
<p>Superscore = 660 + 690 = <strong>1350</strong>. Best single sitting = <strong>1330</strong> (August).</p>
<p>Superscoring adds 20 points over this student's best single test day.</p>
</div>

<h2 id="college-policies">How colleges use superscores</h2>
<p>Policies vary by college, and they can change from year to year, so always check each school's admissions website. In general you will see three approaches:</p>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Policy</th><th>What the college looks at</th></tr></thead>
<tbody>
<tr><td>Superscore</td><td>Your best section scores across all dates.</td></tr>
<tr><td>Highest sitting</td><td>Your best total from a single test date.</td></tr>
<tr><td>All scores</td><td>Every score you have taken, though many still focus on the highest.</td></tr>
</tbody></table></div>
<p>College Board's Score Choice lets you choose which test dates to send to many colleges, but some schools ask you to send every score. Test-optional and test-required policies also differ by school, so a strong superscore matters more at some colleges than others.</p>

<h2 id="score-ranges">Understanding SAT section scores</h2>
<p>The digital SAT has two sections, Reading and Writing and Math, each scored from 200 to 800 in 10-point steps. Your total is the sum of the two, from 400 to 1600. Because each section is scored on its own scale, a jump in one section never lowers the other, which is exactly what makes superscoring possible.</p>
<p>Small section gains add up. Raising your Math score by 40 points on a retake raises your superscore by 40 points, even if your Reading and Writing score dropped that day. That is why many students target one section per retake instead of trying to improve everything at once.</p>
<div class="callout callout-info"><strong>Note</strong><p>The superscore calculated here is the simple sum of your best section scores. A college may calculate or display it differently on its own forms, so follow its instructions when reporting.</p></div>

<h2 id="tips">Tips for getting the most from superscoring</h2>
<ul>
  <li><strong>Focus your prep.</strong> If your Reading and Writing score is already strong, you can spend your next test prep mostly on Math, since only your best score in each section counts at superscoring schools.</li>
  <li><strong>Plan your retakes.</strong> Many students take the SAT two or three times. Leave enough time between dates to actually improve, and keep application deadlines in mind.</li>
  <li><strong>Compare to the college's range.</strong> Look up the middle 50% score range for the schools on your list. Our guide to <a href="/blog/what-is-a-good-sat-score">what makes a good SAT score</a> explains how to read those ranges.</li>
  <li><strong>Report scores carefully.</strong> On applications, follow each college's instructions exactly about whether to list a superscore or individual test dates.</li>
  <li><strong>Consider the ACT too.</strong> Some students score better on the ACT. Check your composite with the <a href="/act-score-calculator">ACT score calculator</a>.</li>
</ul>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Enter a hypothetical next test date with the section score you are aiming for. The calculator instantly shows how much your superscore would rise if you hit it.</p></div>
HTML,
  'faqs'        => [
    ['How do you calculate an SAT superscore?', 'Take your highest Reading and Writing score from any test date and add it to your highest Math score from any test date. For example, 660 and 690 give a superscore of 1350.'],
    ['Do all colleges superscore the SAT?', 'No. Many colleges superscore, but some use your highest single sitting or ask for all scores. Check each college\'s admissions website for its current policy.'],
    ['What is the highest possible SAT superscore?', 'The highest possible score is 1600: 800 in Reading and Writing plus 800 in Math.'],
    ['How many test dates can I enter?', 'You can enter up to four SAT test dates. The calculator finds your best score in each section across all of them.'],
    ['What is my best single-sitting score?', 'It is the highest total (Reading and Writing plus Math) you earned on one test date. Colleges that do not superscore usually use this number.'],
  ],
];
