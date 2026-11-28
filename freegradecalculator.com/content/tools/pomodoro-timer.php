<?php
return [
  'h1'          => 'Pomodoro Timer for Studying',
  'meta_title'  => 'Pomodoro Timer – Free 25/5 Study Timer Online',
  'description' => 'Free Pomodoro timer for studying: 25-minute focus sessions with 5-minute breaks and a 15-minute long break every 4 rounds. Fully editable, with a chime.',
  'lead'        => 'Study in focused 25-minute sessions with built-in short and long breaks, a progress ring, a chime when time is up, and a count of completed sessions.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the Pomodoro timer</h2>
<ol class="steps">
  <li><strong>Name your task.</strong> Type what you are working on, such as "Chapter 6 bio notes" or "Calc problem set 4." The label stays on screen so you remember what this session is for.</li>
  <li><strong>Check the settings.</strong> The defaults are 25 minutes of focus, a 5-minute short break, and a 15-minute long break after every 4 focus sessions. Edit any of them to fit your schedule.</li>
  <li><strong>Start the focus session.</strong> The progress ring shows how much time is left. Work on one task only until the chime sounds.</li>
  <li><strong>Take your break.</strong> Step away from your desk. After four focus sessions, take the long break.</li>
  <li><strong>Watch your count grow.</strong> The completed-session counter tracks how many Pomodoros you finished, which is a simple way to measure a study day.</li>
</ol>

<h2 id="what-is-pomodoro">What is the Pomodoro Technique?</h2>
<p>The Pomodoro Technique is a time-management method developed by Francesco Cirillo in the late 1980s, named after the tomato-shaped kitchen timer he used as a student. The idea is simple: work in short, timed bursts with real breaks in between. Knowing a break is coming makes it easier to start, and a fixed end point makes it easier to ignore your phone until then.</p>
<div class="formula">1 cycle = 4 × focus + 3 × short break + 1 × long break</div>
<div class="example-box"><h4>Worked example: one full cycle</h4>
<p>With the default settings, one full cycle is 4 × 25 + 3 × 5 + 15 = 100 + 15 + 15 = <strong>130 minutes</strong>, about 2 hours and 10 minutes.</p>
<p>That gives you <strong>100 minutes</strong> of focused study. If you need 5 hours of focused review before an exam, that is 300 ÷ 25 = <strong>12 Pomodoros</strong>, or three full cycles.</p>
</div>

<h2 id="choosing-settings">Choosing your focus and break lengths</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Setup</th><th>Focus / short / long</th><th>Good for</th></tr></thead>
<tbody>
<tr><td>Classic</td><td>25 / 5 / 15</td><td>Most homework, reading, and flashcards</td></tr>
<tr><td>Short sessions</td><td>15 / 3 / 10</td><td>Getting started when you are procrastinating, or younger students</td></tr>
<tr><td>Deep work</td><td>50 / 10 / 20</td><td>Essays, coding, and long problem sets where warming up takes time</td></tr>
</tbody></table></div>
<p>There is no perfect length. If you keep getting interrupted at minute 20, shorten the focus session. If you are deep in a problem when the chime rings, try a longer one next time.</p>

<h2 id="who-its-for">Who the Pomodoro method works best for</h2>
<p>Pomodoros are especially helpful if you struggle to start assignments, get pulled away by your phone, or lose track of time during long study nights. Breaking the work into fixed blocks turns "study for the test" into a series of small, finishable steps. Students who already focus for long stretches may prefer longer sessions, and the editable settings let you adjust without giving up the structure.</p>

<h2 id="study-tips">How to study better with Pomodoros</h2>
<ul>
  <li><strong>Plan sessions before you start.</strong> Break a big assignment into chunks that fit one Pomodoro each: outline the essay, write the introduction, find three sources.</li>
  <li><strong>Put your phone out of reach.</strong> A timer only helps if the 25 minutes are actually distraction-free. Silence notifications on your laptop too.</li>
  <li><strong>Make breaks real breaks.</strong> Stand up, stretch, refill your water, or look out a window. Scrolling social media tends to make it harder to get back into focus.</li>
  <li><strong>Write down distractions.</strong> If you remember something you need to do, jot it on paper and return to your task. Handle it during the break.</li>
  <li><strong>Mix in active recall.</strong> Spend some sessions quizzing yourself or doing practice problems instead of rereading notes.</li>
  <li><strong>Track your sessions per subject.</strong> Seeing "6 Pomodoros on chemistry this week" shows where your time actually goes.</li>
</ul>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Have a big test coming up? Use the <a href="/exam-countdown">exam countdown</a> to work out how many study hours you need per day, then divide by 25 minutes to plan your daily number of Pomodoros.</p></div>
<p>Writing an essay in Pomodoros? Pair each session with a word goal in the <a href="/word-counter">word counter</a> so you can see your progress add up.</p>
HTML,
  'faqs'        => [
    ['What is a Pomodoro timer?', 'A Pomodoro timer alternates focused work sessions with short breaks. The classic pattern is 25 minutes of focus and a 5-minute break, with a longer break after every four sessions.'],
    ['Can I change the Pomodoro lengths?', 'Yes. The focus session, short break, and long break are all editable. The defaults are 25, 5, and 15 minutes, with a long break every 4 sessions.'],
    ['How long is one full Pomodoro cycle?', 'With default settings, four focus sessions, three short breaks, and one long break total 130 minutes, including 100 minutes of focused work.'],
    ['Does the timer make a sound when time is up?', 'Yes. A chime plays at the end of each focus session and break so you do not have to watch the clock.'],
    ['Is the Pomodoro Technique good for studying?', 'Many students find it helps them start tasks and avoid distractions because each session is short and has a clear end. Adjust the lengths until they fit how you work.'],
  ],
];
