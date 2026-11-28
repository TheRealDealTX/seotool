<?php
return [
  'h1'          => 'Average Calculator',
  'meta_title'  => 'Average Calculator – Mean, Median, Mode & Range',
  'description' => 'Free average calculator: enter a list of numbers to find the mean, median, mode, range, sum, and count. Great for test scores, homework, and statistics class.',
  'lead'        => 'Enter any list of numbers to get the mean, median, mode, range, sum, and count instantly.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the average calculator</h2>
<ol class="steps">
  <li><strong>Enter your numbers.</strong> Type or paste them separated by commas, spaces, or line breaks. Decimals and negative numbers work too.</li>
  <li><strong>Read the results.</strong> The calculator returns the mean (average), median, mode, range, sum, and count.</li>
  <li><strong>Edit and recalculate.</strong> Add or remove a number to see how it changes the average, which is handy for "what if" questions about your grades.</li>
</ol>

<h2 id="formulas">How each value is calculated</h2>
<div class="formula">Mean = Sum of the numbers ÷ Count</div>
<ul>
  <li><strong>Mean:</strong> add everything up and divide by how many numbers there are. This is what people usually mean by "average."</li>
  <li><strong>Median:</strong> sort the numbers from smallest to largest and take the middle one. If there is an even number of values, average the two middle values.</li>
  <li><strong>Mode:</strong> the value that appears most often. A list can have one mode, several modes, or no mode at all if every value appears once.</li>
  <li><strong>Range:</strong> the largest value minus the smallest value.</li>
  <li><strong>Sum:</strong> the total of all the numbers.</li>
  <li><strong>Count:</strong> how many numbers you entered.</li>
</ul>

<div class="example-box"><h4>Worked example</h4>
<p>Your five test scores this semester: 88, 92, 75, 92, 81.</p>
<p><strong>Sum:</strong> 88 + 92 + 75 + 92 + 81 = <strong>428</strong>. <strong>Count:</strong> <strong>5</strong>.</p>
<p><strong>Mean:</strong> 428 ÷ 5 = <strong>85.6</strong>.</p>
<p><strong>Median:</strong> sorted, the scores are 75, 81, 88, 92, 92, so the middle value is <strong>88</strong>.</p>
<p><strong>Mode:</strong> <strong>92</strong> (it appears twice). <strong>Range:</strong> 92 − 75 = <strong>17</strong>.</p>
</div>

<h2 id="mean-vs-median">Mean vs. median: which average should you use?</h2>
<div class="compare">
<div class="compare-col"><h4>Mean</h4><ul><li>Uses every value</li><li>Pulled up or down by extreme values</li><li>What most teachers use for test averages</li></ul></div>
<div class="compare-col"><h4>Median</h4><ul><li>Uses only the middle position</li><li>Barely affected by one very high or low value</li><li>Better for skewed data like income or home prices</li></ul></div>
</div>
<p>Here is why that matters. If one of the test scores above were a 40 instead of 75, the mean would fall to 78.6, but the median would stay at 88. One bad day hurts your mean much more than your median, and most gradebooks use the mean.</p>

<h2 id="averages-and-grades">Averages and your grades</h2>
<p>A simple average works when every score counts the same, like equally weighted quizzes. Many classes weight categories differently, though: tests might be 50% of your grade while homework is 20%. In that case, a plain average gives the wrong answer and you need the <a href="/weighted-average-calculator">weighted average calculator</a> instead.</p>
<p>Teachers looking at a whole class set of scores can use the <a href="/class-average-calculator">class average calculator</a>, which adds standard deviation and a letter-grade distribution chart.</p>

<h2 id="range-and-spread">What the range tells you</h2>
<p>The range is the simplest measure of spread. A small range means your numbers are close together, like quiz scores of 84, 86, and 88 (range 4). A large range means they vary a lot, like 55, 80, and 98 (range 43), even though both sets could have similar means.</p>
<p>For grades, a large range can point to one assignment that went badly or a topic you need to review. Look at which number sits at the low end and whether it is a one-time slip or a pattern.</p>

<h2 id="tips">Tips and common mistakes</h2>
<ul>
  <li><strong>Do not average percentages from different-sized tests.</strong> If one quiz was out of 10 and another out of 100, averaging the percentages treats them as equal. Add up the points instead.</li>
  <li><strong>Check for typos.</strong> One extra zero (900 instead of 90) can wreck a mean. The range is a quick way to spot a mistake.</li>
  <li><strong>Include zeros when they count.</strong> A missing assignment recorded as 0 is part of your average, and it pulls the mean down hard.</li>
  <li><strong>Find the score you need.</strong> To raise a five-test average from 85.6 to 87 with a sixth test, you need a total of 87 × 6 = 522, so the sixth score must be 522 − 428 = 94.</li>
</ul>
HTML,
  'faqs'        => [
    ['How do you calculate the average of a set of numbers?', 'Add all the numbers together and divide by how many numbers there are. For 88, 92, 75, 92, and 81, the sum is 428 and the average is 428 ÷ 5 = 85.6.'],
    ['What is the difference between mean, median, and mode?', 'The mean is the arithmetic average, the median is the middle value when the numbers are sorted, and the mode is the value that appears most often.'],
    ['How do I find the median with an even number of values?', 'Sort the numbers and average the two in the middle. For 70, 80, 90, 100, the median is (80 + 90) ÷ 2 = 85.'],
    ['Can a list have no mode?', 'Yes. If every number appears exactly once, there is no mode. If two or more values tie for most frequent, the list has more than one mode.'],
    ['Should I use a simple average for my class grade?', 'Only if every assignment counts equally. If categories have different weights, use a weighted average instead.'],
  ],
];
