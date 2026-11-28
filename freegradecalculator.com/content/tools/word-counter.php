<?php
return [
  'h1'          => 'Word Counter for Essays',
  'meta_title'  => 'Word Counter – Free Essay Word & Character Count',
  'description' => 'Free word counter for essays: count words, characters, sentences, and paragraphs, see reading and speaking time, spot repeated words, and track a word goal.',
  'lead'        => 'Paste your essay to count words, characters, sentences, and paragraphs, see reading and speaking time, and track progress toward a word goal.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the word counter</h2>
<ol class="steps">
  <li><strong>Paste or type your text.</strong> Drop in an essay, a personal statement, a discussion post, or speech notes. The counts update as you type.</li>
  <li><strong>Check the counts.</strong> You get words, characters with spaces, characters without spaces, sentences, and paragraphs.</li>
  <li><strong>See reading and speaking time.</strong> Useful for presentations and timed speeches.</li>
  <li><strong>Review your top repeated words.</strong> The list shows which words you use most so you can vary your vocabulary.</li>
  <li><strong>Set a word goal (optional).</strong> Enter a target, such as 1,000 words, and a progress bar fills as you write.</li>
</ol>

<h2 id="what-it-counts">What the word counter measures</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Count</th><th>Why it matters for students</th></tr></thead>
<tbody>
<tr><td>Words</td><td>Most essay assignments and application prompts set a word limit or minimum.</td></tr>
<tr><td>Characters (with spaces)</td><td>Many online forms limit characters, not words, and usually count spaces.</td></tr>
<tr><td>Characters (without spaces)</td><td>Some instructors and translation tasks count only letters and punctuation.</td></tr>
<tr><td>Sentences</td><td>Helps you check average sentence length and readability.</td></tr>
<tr><td>Paragraphs</td><td>Shows whether your essay structure matches the assignment (for example, a five-paragraph essay).</td></tr>
<tr><td>Reading time</td><td>Estimated at 238 words per minute, a typical silent reading speed for adults.</td></tr>
<tr><td>Speaking time</td><td>Estimated at 130 words per minute, a comfortable pace for a speech or presentation.</td></tr>
</tbody></table></div>

<h2 id="formulas">How reading and speaking time are estimated</h2>
<div class="formula">Reading time (minutes) = Words ÷ 238</div>
<div class="formula">Speaking time (minutes) = Words ÷ 130</div>
<div class="example-box"><h4>Worked example</h4>
<p>A 1,500-word research essay takes about 1,500 ÷ 238 = <strong>6.3 minutes</strong> to read and about 1,500 ÷ 130 = <strong>11.5 minutes</strong> to read aloud.</p>
<p>Going the other way: for a 5-minute class presentation at 130 words per minute, aim for about 5 × 130 = <strong>650 words</strong> of speaking notes.</p>
</div>
<p>Everyone reads and speaks at a different pace, so treat these as estimates. Rehearse out loud with a timer before any timed speech.</p>

<h2 id="common-limits">Common word limits students run into</h2>
<ul>
  <li><strong>Common App personal statement:</strong> up to 650 words. Many students aim for 550–650.</li>
  <li><strong>Common App activity descriptions:</strong> up to 150 characters each, which is why the character count matters.</li>
  <li><strong>College supplemental essays:</strong> often 100–400 words, set by each college.</li>
  <li><strong>Class essays:</strong> set by your teacher, often as a range such as 800–1,200 words.</li>
</ul>
<p>Limits change and differ by school and application, so always check the current prompt.</p>

<h2 id="page-length">Words per page</h2>
<p>Teachers sometimes assign essays by pages instead of words. As a rough guide, a double-spaced page in 12-point Times New Roman with 1-inch margins holds about 250–300 words, and a single-spaced page holds about twice that. Font, spacing, and paragraph breaks change the number, so use the word count when your teacher gives a word range and the page count only as an estimate.</p>

<h2 id="tips">Tips for hitting your word count the right way</h2>
<ul>
  <li><strong>Over the limit? Cut filler first.</strong> Words like "really," "very," "in order to," and "the fact that" can usually go without losing meaning.</li>
  <li><strong>Use the repeated-words list.</strong> If "important" shows up nine times, swap some for more precise words or rewrite the sentences.</li>
  <li><strong>Under the minimum? Add evidence, not fluff.</strong> Another example, quote, or explanation of why your evidence matters makes the essay stronger and longer at the same time.</li>
  <li><strong>Check sentence length.</strong> Divide words by sentences. If your average is above 25 words, try breaking up long sentences.</li>
  <li><strong>Write in focused blocks.</strong> Set a word goal for each session and pair it with the <a href="/pomodoro-timer">Pomodoro timer</a>, for example 300 words per 25-minute focus session.</li>
</ul>
<div class="callout callout-info"><strong>Note</strong><p>Different programs count words slightly differently, especially with hyphenated words, numbers, and URLs. If your teacher or an application portal uses its own counter, a small difference of a few words is normal, so leave a little buffer below a hard limit.</p></div>
<p>Have an essay due on a deadline? Set up the <a href="/exam-countdown">countdown timer</a> to see exactly how many days and hours you have left.</p>
HTML,
  'faqs'        => [
    ['How is reading time calculated?', 'Reading time is your word count divided by 238 words per minute, a typical adult silent reading speed. A 1,500-word essay takes about 6.3 minutes to read.'],
    ['How many words is a 5-minute speech?', 'At a speaking pace of 130 words per minute, a 5-minute speech is about 650 words. Your own pace may be faster or slower, so practice with a timer.'],
    ['Does the word counter count characters with and without spaces?', 'Yes. It shows both, which helps with forms that limit characters, such as college application activity descriptions.'],
    ['Can I set a word goal?', 'Yes. Enter a target word count and a progress bar shows how close you are as you type.'],
    ['Why does my word count differ from Google Docs or Word?', 'Programs treat hyphenated words, numbers, and symbols slightly differently, so counts can vary by a few words. Leave a small buffer under strict limits.'],
  ],
];
