<?php
return [
  'h1'          => 'Weighted Average Calculator',
  'meta_title'  => 'Weighted Average Calculator – Free & Step-by-Step',
  'description' => 'Free weighted average calculator: enter each value and its weight to get the weighted average and total weight. Ideal for grades, GPA, and class categories.',
  'lead'        => 'Enter values and their weights to calculate a weighted average, along with the total of all the weights.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the weighted average calculator</h2>
<ol class="steps">
  <li><strong>Enter a value and its weight on each row.</strong> The value is the number being averaged (a score, a grade point, a price). The weight is how much it counts (a percentage, credit hours, or a quantity).</li>
  <li><strong>Add as many rows as you need.</strong> One row per item.</li>
  <li><strong>Read the results.</strong> The calculator shows the weighted average and Σweights, the sum of all the weights.</li>
</ol>

<h2 id="formula">The weighted average formula</h2>
<div class="formula">Weighted average = Σ (value × weight) ÷ Σ weights</div>
<p>Multiply each value by its weight, add those products together, then divide by the total of the weights. Because you divide by the sum of the weights, they do not need to add up to 100 or to 1. Weights of 20, 30, and 50 give the same answer as 0.2, 0.3, and 0.5, or 2, 3, and 5.</p>

<div class="example-box"><h4>Worked example 1: class grade</h4>
<p>Your class grade is made of homework (92%, weight 20), quizzes (85%, weight 30), and exams (78%, weight 50).</p>
<p>Σ (value × weight) = 92 × 20 + 85 × 30 + 78 × 50 = 1,840 + 2,550 + 3,900 = 8,290.</p>
<p>Σ weights = 20 + 30 + 50 = 100.</p>
<p>Weighted average = 8,290 ÷ 100 = <strong>82.9%</strong>. A simple average of 92, 85, and 78 would be 85, which overstates your grade because exams count the most.</p>
</div>
<div class="example-box"><h4>Worked example 2: GPA by credit hours</h4>
<p>Three courses: 4.0 for 3 credits, 3.0 for 4 credits, 3.7 for 3 credits.</p>
<p>Σ (value × weight) = 12.0 + 12.0 + 11.1 = 35.1. Σ weights = 10 credits.</p>
<p>Weighted average = 35.1 ÷ 10 = <strong>3.51</strong>.</p>
</div>

<h2 id="when-to-use">When to use a weighted average</h2>
<p>Use a weighted average any time some items count more than others. For students, that comes up constantly:</p>
<ul>
  <li><strong>Class grades with categories.</strong> Tests, homework, labs, and participation are often weighted differently in the syllabus.</li>
  <li><strong>GPA.</strong> A 4-credit course counts more than a 1-credit course, so grade points are weighted by credits.</li>
  <li><strong>Group projects.</strong> Peer evaluations or rubric criteria may carry different weights.</li>
  <li><strong>Statistics and science.</strong> Averaging results from samples of different sizes calls for weighting by sample size.</li>
</ul>
<p>If you are working out a class grade and want a letter grade and GPA points along with the percentage, the <a href="/weighted-grade-calculator">weighted grade calculator</a> is built for exactly that. For semester GPA with letter grades and credits, use the <a href="/gpa-calculator">GPA calculator</a>.</p>

<h2 id="weighted-vs-simple">Weighted average vs. simple average</h2>
<div class="compare">
<div class="compare-col"><h4>Simple average</h4><ul><li>Every value counts equally</li><li>Sum ÷ count</li><li>Fine for equally weighted quizzes</li></ul></div>
<div class="compare-col"><h4>Weighted average</h4><ul><li>Each value counts by its weight</li><li>Σ(value × weight) ÷ Σweights</li><li>Needed for category grades and GPA</li></ul></div>
</div>
<p>When every weight is the same, the weighted average equals the simple average, so you cannot go wrong by using weights.</p>

<h2 id="target-score">Finding the score you need in one category</h2>
<p>You can also use a weighted average to plan ahead. Suppose homework (92, weight 20) and quizzes (85, weight 30) are done, and the exam (weight 50) is left. To finish at 85, you need a total of 85 × 100 = 8,500 weighted points. You already have 1,840 + 2,550 = 4,390, so the exam must supply 4,110, which is 4,110 ÷ 50 = <strong>82.2</strong>. Enter that score in the calculator to confirm the result.</p>

<h2 id="tips">Tips and common mistakes</h2>
<ul>
  <li><strong>Check the total weight.</strong> If your syllabus weights should add to 100 but Σweights shows 90, you probably left out a category.</li>
  <li><strong>Leave out empty categories.</strong> If you have no grades yet in a category, do not enter it as 0. Leave it off until you have a score, and the calculator will average only the categories you entered.</li>
  <li><strong>Keep units consistent.</strong> All values should be on the same scale, such as all percentages or all 4.0 grade points.</li>
  <li><strong>Do not confuse value and weight.</strong> In a GPA calculation the grade point is the value and the credit hours are the weight, not the other way around.</li>
</ul>
HTML,
  'faqs'        => [
    ['How do you calculate a weighted average?', 'Multiply each value by its weight, add the products, and divide by the sum of the weights. For 92 (weight 20), 85 (weight 30), and 78 (weight 50), the weighted average is 8,290 ÷ 100 = 82.9.'],
    ['Do the weights have to add up to 100?', 'No. The calculator divides by the total of the weights, so weights of 2, 3, and 5 give the same result as 20, 30, and 50.'],
    ['What is the difference between a weighted average and a regular average?', 'A regular average counts every value equally. A weighted average lets some values count more than others based on their weights.'],
    ['How do I use a weighted average for GPA?', 'Enter each course\'s grade points as the value and its credit hours as the weight. The weighted average is your GPA.'],
    ['What does Σweights mean?', 'Σweights is the sum of all the weights you entered. It helps you check that you included every category.'],
  ],
];
