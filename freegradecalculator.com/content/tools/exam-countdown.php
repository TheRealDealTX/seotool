<?php
return [
  'h1'          => 'Exam Countdown Timer',
  'meta_title'  => 'Exam Countdown – How Many Days Until My Exam?',
  'description' => 'Free exam countdown timer: enter your exam date and time for a live countdown in days, hours, minutes, and seconds, plus the study hours you need per day.',
  'lead'        => 'Enter your exam name, date, and time to get a live countdown and find out how many hours a day you need to study to be ready.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the exam countdown</h2>
<ol class="steps">
  <li><strong>Name your exam.</strong> For example, "AP Biology," "Calc 2 Final," or "SAT."</li>
  <li><strong>Enter the date and time.</strong> Use the start time of the exam so the countdown ends exactly when you sit down to test.</li>
  <li><strong>Watch the live countdown.</strong> It shows the days, hours, minutes, and seconds remaining and updates every second.</li>
  <li><strong>Enter the total study hours you need.</strong> The calculator divides those hours across the time left and tells you how many hours to study per day.</li>
  <li><strong>Come back anytime.</strong> Your countdown is saved in your browser, so it is still there when you reopen the page on the same device.</li>
</ol>

<h2 id="formula">Study hours per day formula</h2>
<div class="formula">Hours per day = Total study hours needed ÷ Days remaining</div>
<div class="example-box"><h4>Worked example</h4>
<p>Your chemistry final is 12 days away, and you estimate you need 30 hours of review.</p>
<p>Hours per day = 30 ÷ 12 = <strong>2.5 hours per day</strong>.</p>
<p>That is six 25-minute focus sessions a day (6 × 25 = 150 minutes). If you wait until there are only 5 days left, the same 30 hours becomes 30 ÷ 5 = <strong>6 hours per day</strong>, which is much harder to fit around classes.</p>
</div>

<h2 id="estimating-hours">How many study hours do you need?</h2>
<p>There is no universal number, and it depends on the course, how well you already know the material, and how much the exam counts. A practical way to estimate:</p>
<ul>
  <li><strong>List every topic or chapter</strong> the exam covers.</li>
  <li><strong>Rate each one</strong> as solid, shaky, or new to you.</li>
  <li><strong>Assign time:</strong> for example, 30 minutes for each solid topic, 1.5 hours for each shaky one, and 3 hours for each new one.</li>
  <li><strong>Add time for a practice test</strong> and for reviewing what you got wrong on it.</li>
</ul>
<p>Not sure how much the final matters? Check what score you need with the <a href="/final-grade-calculator">final grade calculator</a>. If you only need a 65 to keep your A, you can shift some hours to a class where the final carries more weight.</p>

<h2 id="study-plan">Turning the countdown into a study plan</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Time left</th><th>Focus</th></tr></thead>
<tbody>
<tr><td>3+ weeks</td><td>Organize notes, fill gaps, start spaced review of early units.</td></tr>
<tr><td>1–2 weeks</td><td>Practice problems and active recall; take a timed practice test.</td></tr>
<tr><td>2–4 days</td><td>Review mistakes from practice tests, make a one-page summary sheet.</td></tr>
<tr><td>Night before</td><td>Light review only, pack what you need, and get a full night of sleep.</td></tr>
</tbody></table></div>

<h2 id="multiple-exams">Planning for several exams at once</h2>
<p>Finals week often stacks several tests within a few days. Work out the study hours for each exam separately, then add them up and divide by the days until the first exam to see your real daily workload. Front-load the subject whose exam comes first, but keep a short daily review of the later ones so nothing goes untouched for a week.</p>

<h2 id="tips">Tips for using an exam countdown</h2>
<ul>
  <li><strong>Start the countdown early.</strong> The earlier you set it, the smaller your daily hours, and the more time your memory has to consolidate between review sessions.</li>
  <li><strong>Plan in focus sessions.</strong> Divide your hours per day into 25-minute blocks with the <a href="/pomodoro-timer">Pomodoro timer</a>. 2.5 hours is six sessions, which feels much more doable.</li>
  <li><strong>Leave buffer days.</strong> Plan to finish your study hours a day or two before the exam in case you get sick or another assignment takes longer than expected.</li>
  <li><strong>Recalculate when plans change.</strong> Missed a day? Update your remaining hours and the per-day number adjusts.</li>
  <li><strong>Double-check the exam time.</strong> Confirm the date, start time, and time zone (for online exams) on your official schedule or admission ticket.</li>
</ul>
<div class="callout callout-info"><strong>Note</strong><p>Your countdown is stored only in this browser. Clearing your browser data, using private browsing, or switching devices will reset it, so keep your exam date written down somewhere else too.</p></div>
HTML,
  'faqs'        => [
    ['How do I count down to my exam?', 'Enter the exam name, date, and start time. The countdown shows the days, hours, minutes, and seconds left and updates live.'],
    ['How many hours a day should I study for an exam?', 'Divide the total hours you need by the days remaining. For example, 30 hours of review with 12 days left works out to 2.5 hours per day.'],
    ['Will my exam countdown be saved?', 'Yes, it is saved in your browser on this device. Clearing browser data or using a different device or private window will not show it.'],
    ['How far in advance should I start studying for a final?', 'It depends on the course and how much material there is, but starting one to three weeks ahead lets you spread the work into manageable daily sessions.'],
    ['Can I use this for the SAT, ACT, or AP exams?', 'Yes. Enter any exam name and date, including standardized tests, AP exams, or class finals.'],
  ],
];
