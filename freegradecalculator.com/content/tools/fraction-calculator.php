<?php
return [
  'h1'          => 'Fraction Calculator',
  'meta_title'  => 'Fraction Calculator – Add, Subtract, Multiply, Divide',
  'description' => 'Free fraction calculator with steps: add, subtract, multiply, or divide fractions and mixed numbers. Get the simplified fraction, mixed number, and decimal.',
  'lead'        => 'Add, subtract, multiply, or divide two fractions or mixed numbers and get the simplified answer, mixed number, decimal, and the steps to get there.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the fraction calculator</h2>
<ol class="steps">
  <li><strong>Enter the first fraction.</strong> Type a numerator and denominator. For a mixed number like 2 1/3, enter the whole number too.</li>
  <li><strong>Choose an operation.</strong> Pick +, −, ×, or ÷.</li>
  <li><strong>Enter the second fraction.</strong> Again, a simple fraction or a mixed number.</li>
  <li><strong>Read the answer and steps.</strong> You get the result as a simplified fraction, as a mixed number, and as a decimal, plus the steps so you can follow the work or check your homework.</li>
</ol>

<h2 id="rules">Fraction rules for each operation</h2>
<p>The calculator first turns any mixed number into an improper fraction, does the operation, and then simplifies by dividing the top and bottom by their greatest common factor.</p>
<h3>Adding and subtracting</h3>
<div class="formula">a/b ± c/d = (a × d ± c × b) ÷ (b × d)</div>
<p>You need a common denominator before you can add or subtract. Using the least common denominator keeps the numbers small.</p>
<h3>Multiplying</h3>
<div class="formula">a/b × c/d = (a × c) ÷ (b × d)</div>
<h3>Dividing</h3>
<div class="formula">a/b ÷ c/d = a/b × d/c</div>
<p>To divide, flip the second fraction (take its reciprocal) and multiply. You cannot divide by a fraction equal to zero.</p>
<h3>Converting a mixed number</h3>
<div class="formula">w n/d = (w × d + n) ÷ d</div>

<div class="example-box"><h4>Worked example 1: adding a mixed number</h4>
<p>2 1/3 + 3/4</p>
<p>Step 1: convert 2 1/3 to an improper fraction: (2 × 3 + 1)/3 = 7/3.</p>
<p>Step 2: find a common denominator. The LCD of 3 and 4 is 12, so 7/3 = 28/12 and 3/4 = 9/12.</p>
<p>Step 3: add the numerators: 28/12 + 9/12 = <strong>37/12</strong>.</p>
<p>Step 4: 37/12 is already in lowest terms. As a mixed number it is <strong>3 1/12</strong>, and as a decimal about <strong>3.0833</strong>.</p>
</div>
<div class="example-box"><h4>Worked example 2: dividing fractions</h4>
<p>5/6 ÷ 2/3 = 5/6 × 3/2 = 15/12. Dividing top and bottom by 3 gives <strong>5/4</strong>, which is <strong>1 1/4</strong> or <strong>1.25</strong>.</p>
</div>

<h2 id="simplifying">Simplifying fractions</h2>
<p>A fraction is in simplest form when the numerator and denominator share no common factor other than 1. To simplify, find the greatest common factor (GCF) and divide both by it. For 18/24 the GCF is 6, so 18/24 = 3/4. The calculator always shows the fully simplified result.</p>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Fraction</th><th>Simplified</th><th>Decimal</th><th>Percent</th></tr></thead>
<tbody>
<tr><td>4/8</td><td>1/2</td><td>0.5</td><td>50%</td></tr>
<tr><td>6/8</td><td>3/4</td><td>0.75</td><td>75%</td></tr>
<tr><td>10/15</td><td>2/3</td><td>0.667</td><td>66.7%</td></tr>
<tr><td>18/24</td><td>3/4</td><td>0.75</td><td>75%</td></tr>
<tr><td>12/20</td><td>3/5</td><td>0.6</td><td>60%</td></tr>
</tbody></table></div>
<p>Need a fraction as a percentage, like a test score of 18/24? Divide to get the decimal and multiply by 100, or use the <a href="/percentage-calculator">percentage calculator</a>.</p>

<h2 id="mixed-numbers">Mixed numbers and improper fractions</h2>
<p>An improper fraction has a numerator bigger than its denominator, like 37/12. A mixed number writes the same value as a whole number plus a proper fraction, like 3 1/12. To convert an improper fraction, divide: 37 ÷ 12 is 3 with a remainder of 1, so 37/12 = 3 1/12.</p>
<p>Teachers often want final answers as mixed numbers in word problems (3 1/4 cups of flour) and as improper fractions in algebra. The calculator shows both, so you can use whichever format your assignment asks for.</p>

<h2 id="tips">Tips for fraction homework</h2>
<ul>
  <li><strong>Try it yourself first.</strong> Work the problem on paper, then use the steps to find exactly where your answer went off track.</li>
  <li><strong>Cross-simplify before multiplying.</strong> In 4/9 × 3/8, cancel the 4 with the 8 and the 3 with the 9 first: you get 1/3 × 1/2 = 1/6 with smaller numbers.</li>
  <li><strong>Never add denominators.</strong> 1/2 + 1/3 is not 2/5. Find a common denominator: 3/6 + 2/6 = 5/6.</li>
  <li><strong>Watch negative signs.</strong> Keep the sign with the numerator so it is easy to track through each step.</li>
  <li><strong>Check with decimals.</strong> 37/12 ≈ 3.08, and 2 1/3 + 3/4 ≈ 2.33 + 0.75 = 3.08. If the decimals match, your fraction answer is right.</li>
</ul>
<p>For problems that mix fractions with powers, roots, or trig, use the <a href="/scientific-calculator">scientific calculator</a>.</p>
HTML,
  'faqs'        => [
    ['How do you add fractions with different denominators?', 'Find a common denominator, rewrite each fraction with it, then add the numerators. For 1/3 + 3/4, the common denominator is 12, so 4/12 + 9/12 = 13/12, or 1 1/12.'],
    ['How do you divide fractions?', 'Flip the second fraction and multiply. For example, 5/6 ÷ 2/3 = 5/6 × 3/2 = 15/12, which simplifies to 5/4 or 1 1/4.'],
    ['Can the fraction calculator handle mixed numbers?', 'Yes. Enter the whole number along with the numerator and denominator. The calculator converts it to an improper fraction, solves the problem, and shows the result as a mixed number too.'],
    ['How do I simplify a fraction?', 'Divide the numerator and denominator by their greatest common factor. 18/24 simplifies to 3/4 because both numbers divide evenly by 6.'],
    ['Does the calculator show the steps?', 'Yes. Along with the simplified fraction, mixed number, and decimal, it shows the steps used to reach the answer.'],
  ],
];
