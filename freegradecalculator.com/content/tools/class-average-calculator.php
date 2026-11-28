<?php
return [
  'h1'          => 'Class Average Calculator',
  'meta_title'  => 'Class Average Calculator – Mean, Median & Grade Spread',
  'description' => 'Free class average calculator for teachers: paste scores to get the mean, median, mode, range, standard deviation, and a letter-grade distribution chart.',
  'lead'        => 'Paste your students\' scores to get the class average, median, mode, range, standard deviation, and a letter-grade distribution chart in one step.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the class average calculator</h2>
<ol class="steps">
  <li><strong>Paste the scores.</strong> Copy a column of scores from your gradebook or spreadsheet and paste it in. Commas, spaces, or line breaks all work.</li>
  <li><strong>Read the summary.</strong> You get the count, mean (average), median, mode, range, minimum, maximum, and standard deviation.</li>
  <li><strong>Check the distribution.</strong> The bar chart shows how many students fall into each letter-grade band, so you can see at a glance whether the test was too hard, too easy, or about right.</li>
</ol>

<h2 id="formulas">What each statistic means</h2>
<div class="formula">Class average (mean) = Sum of all scores ÷ Number of scores</div>
<ul>
  <li><strong>Count:</strong> how many scores you entered.</li>
  <li><strong>Mean:</strong> the ordinary average. It is what most people mean by "class average."</li>
  <li><strong>Median:</strong> the middle score when the list is sorted. With an even count, it is the average of the two middle scores.</li>
  <li><strong>Mode:</strong> the score that appears most often. A class can have more than one mode, or none.</li>
  <li><strong>Range:</strong> the highest score minus the lowest score.</li>
  <li><strong>Minimum and maximum:</strong> the lowest and highest scores.</li>
  <li><strong>Standard deviation:</strong> how spread out the scores are around the mean. The calculator uses the population standard deviation, since a class roster is the whole group rather than a sample.</li>
</ul>
<div class="formula">σ = √( Σ (score − mean)² ÷ N )</div>

<div class="example-box"><h4>Worked example</h4>
<p>Eight quiz scores: 72, 85, 85, 90, 68, 95, 78, 88.</p>
<p><strong>Mean:</strong> the sum is 661, so 661 ÷ 8 = <strong>82.6</strong> (82.625).</p>
<p><strong>Median:</strong> sorted, the list is 68, 72, 78, 85, 85, 88, 90, 95. The two middle scores are 85 and 85, so the median is <strong>85</strong>.</p>
<p><strong>Mode:</strong> 85 (it appears twice). <strong>Range:</strong> 95 − 68 = <strong>27</strong>. <strong>Standard deviation:</strong> about <strong>8.6</strong>.</p>
<p><strong>Distribution:</strong> 2 A's (90, 95), 3 B's (85, 85, 88), 2 C's (72, 78), 1 D (68), and no F's.</p>
</div>

<h2 id="interpreting">How to read the results</h2>
<p>The mean and median together tell you a lot. When the mean is noticeably lower than the median, as in the example above, a few low scores are pulling the average down while most of the class did fine. When they are close, the scores are fairly balanced.</p>
<p>Standard deviation tells you how consistent the class was. A small standard deviation (say 5) means most students scored close to the average. A large one (15 or more) means a wide gap between the strongest and weakest results, which can be a sign that some students missed a key concept.</p>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>What you see</th><th>What it may mean</th></tr></thead>
<tbody>
<tr><td>Low mean, small spread</td><td>The test was hard for almost everyone, or a topic was not fully taught yet.</td></tr>
<tr><td>High mean, small spread</td><td>The class mastered the material, or the test was easy.</td></tr>
<tr><td>Mean well below median</td><td>A handful of very low scores; consider checking in with those students.</td></tr>
<tr><td>Large spread, two clusters</td><td>The class may be split between students who got a concept and those who did not.</td></tr>
</tbody></table></div>

<h2 id="mean-vs-median">Should you report the mean or the median?</h2>
<p>Most gradebooks and report cards use the mean, so it is the number parents and students expect when they ask for the class average. The median is often the better number for your own planning, because it shows how the typical student did without being dragged around by one or two extreme scores.</p>
<p>A quick check: if the mean and median are within a couple of points, either one describes the class well. If they are far apart, share both, or look at the distribution chart before drawing conclusions about how the test went.</p>

<h2 id="tips">Tips for teachers</h2>
<ul>
  <li><strong>Leave out missing work.</strong> A zero for an unsubmitted test drags the average down and can hide how the students who took it actually did. Calculate with and without zeros if you are unsure.</li>
  <li><strong>Compare sections.</strong> Run each class period separately to see whether one group needs a review day.</li>
  <li><strong>Decide on a curve with data.</strong> If the mean is far below what you expected, the <a href="/grade-curve-calculator">grade curve calculator</a> lets you try several curves on the same list.</li>
  <li><strong>Students can use it too.</strong> When a teacher posts all the scores (without names), students can see where their own score falls.</li>
</ul>
<p>Only need a basic average of any list of numbers? The <a href="/average-calculator">average calculator</a> gives the mean, median, mode, range, sum, and count.</p>
HTML,
  'faqs'        => [
    ['How do you calculate a class average?', 'Add up every student\'s score and divide by the number of students. For example, scores totaling 661 across 8 students give a class average of 82.6.'],
    ['What is the difference between the mean and the median class score?', 'The mean is the arithmetic average. The median is the middle score when the list is sorted. A few very low or very high scores move the mean more than the median.'],
    ['Which standard deviation does this calculator use?', 'It uses the population standard deviation, dividing by the number of scores, because a class roster is usually the entire group you care about.'],
    ['Can I paste scores from Google Sheets or Excel?', 'Yes. Copy the column of scores and paste it in. Line breaks, commas, and spaces are all accepted as separators.'],
    ['What does the grade distribution chart show?', 'It counts how many scores fall into each letter-grade band, so you can see how the class did as a whole.'],
  ],
];
