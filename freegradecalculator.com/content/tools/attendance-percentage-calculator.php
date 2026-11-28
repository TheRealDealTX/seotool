<?php
return [
  'h1'          => 'Attendance Percentage Calculator',
  'meta_title'  => 'Attendance Percentage Calculator – Classes You Can Miss',
  'description' => 'Free attendance percentage calculator: enter classes held and attended to see your attendance %, how many classes you can miss, or how many you must attend.',
  'lead'        => 'Enter the classes held and the classes you attended to see your attendance percentage and exactly how many classes you can miss or must attend to meet the requirement.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the attendance percentage calculator</h2>
<ol class="steps">
  <li><strong>Enter classes held.</strong> The total number of class sessions so far this term.</li>
  <li><strong>Enter classes attended.</strong> How many of those sessions you were present for.</li>
  <li><strong>Set the required percentage.</strong> It starts at 75%, a common minimum. Change it to match your school, course, or scholarship rule.</li>
  <li><strong>Read your result.</strong> You see your current attendance percentage. If you are above the requirement, the calculator tells you how many more classes you can miss and still stay at or above it. If you are below, it tells you how many classes in a row you need to attend to get back up.</li>
</ol>

<h2 id="formula">Attendance percentage formula</h2>
<div class="formula">Attendance % = Classes attended ÷ Classes held × 100</div>
<p>To find how many classes you can still skip, the calculator looks for the largest number of future absences that keeps your percentage at or above the requirement R (as a decimal):</p>
<div class="formula">Classes you can miss = floor( Attended ÷ R − Held )</div>
<p>If you are below the requirement, it finds the smallest number of classes you must attend in a row:</p>
<div class="formula">Classes needed = ceiling( (R × Held − Attended) ÷ (1 − R) )</div>

<div class="example-box"><h4>Worked example 1: how many classes can I miss?</h4>
<p>You have attended 34 of 40 classes and the requirement is 75%.</p>
<p>Current attendance = 34 ÷ 40 × 100 = <strong>85%</strong>.</p>
<p>Classes you can miss = floor(34 ÷ 0.75 − 40) = floor(45.33 − 40) = <strong>5</strong>. Check: after 5 more absences you would have 34 of 45, or 75.6%. A sixth absence would drop you to 34 of 46, or 73.9%.</p>
</div>
<div class="example-box"><h4>Worked example 2: how many classes must I attend?</h4>
<p>You have attended 27 of 40 classes, which is 67.5%, and you need 75%.</p>
<p>Classes needed = ceiling((0.75 × 40 − 27) ÷ 0.25) = ceiling(3 ÷ 0.25) = <strong>12</strong>. Check: after 12 straight classes you have 39 of 52, which is exactly 75%.</p>
</div>

<h2 id="why-it-matters">Why attendance percentage matters</h2>
<p>Attendance rules vary a lot. Some colleges and universities require a minimum percentage to sit the final exam, many high schools limit how many absences a student can have before losing course credit, and some scholarships and financial aid programs have attendance or participation conditions. Your syllabus or student handbook is the place to find the exact number and whether excused absences count.</p>
<p>Attendance also tends to track grades. Missing class means missing quizzes, in-class work, and explanations that never make it into the slides. If participation is part of your grade, each absence may cost points directly. You can see how a category like participation affects your overall grade with the <a href="/weighted-grade-calculator">weighted grade calculator</a>.</p>

<h2 id="quick-table">How much one absence costs</h2>
<p>The fewer classes held, the more each absence moves your percentage. This table shows the attendance rate after a single missed class with perfect attendance otherwise:</p>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Classes held</th><th>Attended</th><th>Attendance %</th></tr></thead>
<tbody>
<tr><td>10</td><td>9</td><td>90%</td></tr>
<tr><td>20</td><td>19</td><td>95%</td></tr>
<tr><td>40</td><td>39</td><td>97.5%</td></tr>
<tr><td>50</td><td>49</td><td>98%</td></tr>
</tbody></table></div>

<h2 id="tips">Tips for staying above the requirement</h2>
<ul>
  <li><strong>Count every session the same way your school does.</strong> Labs and tutorials sometimes count as separate sessions. Late arrivals may count as half an absence at some schools.</li>
  <li><strong>Plan for the classes still to come.</strong> Early in the term, one absence moves your percentage a lot. With 10 classes held, a single miss drops you to 90%. With 50 held, it costs only 2 points.</li>
  <li><strong>Keep a cushion.</strong> Treat the number of classes you can miss as an emergency allowance for illness, not a target.</li>
  <li><strong>Get absences documented.</strong> If your school excuses absences for medical or family reasons, submit the paperwork quickly so your official record is correct.</li>
  <li><strong>Recheck after every week.</strong> Update the numbers regularly so you are never surprised at the end of the term.</li>
</ul>
<div class="callout callout-info"><strong>Note</strong><p>This calculator assumes every class counts equally. If your school weights sessions differently or treats excused absences separately, adjust your numbers to match that policy.</p></div>
HTML,
  'faqs'        => [
    ['How do I calculate my attendance percentage?', 'Divide the classes you attended by the total classes held and multiply by 100. Attending 34 of 40 classes gives 85% attendance.'],
    ['How many classes can I miss and still have 75% attendance?', 'Divide the classes you attended by 0.75, subtract the classes held so far, and round down. With 34 of 40 attended, you can miss 5 more classes.'],
    ['How many classes do I need to attend to reach 75%?', 'Use (0.75 × classes held − classes attended) ÷ 0.25 and round up. With 27 of 40 attended, you need 12 classes in a row.'],
    ['Can I change the required attendance percentage?', 'Yes. The requirement defaults to 75%, but you can enter any percentage, such as 80% or 90%, to match your school or course.'],
    ['Do excused absences count against attendance?', 'It depends on your school. Some count every absence, others exclude excused ones. Check your handbook and enter your numbers the way your school counts them.'],
  ],
];
