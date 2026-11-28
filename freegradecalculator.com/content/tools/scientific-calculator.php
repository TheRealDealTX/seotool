<?php
return [
  'h1'          => 'Scientific Calculator',
  'meta_title'  => 'Free Online Scientific Calculator for Students',
  'description' => 'Free online scientific calculator for students: trig in degrees or radians, logs, powers, roots, factorials, π and e, plus result history and keyboard input.',
  'lead'        => 'A free online scientific calculator with trig, logs, powers, roots, and factorials, plus a history of your results and full keyboard support.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the scientific calculator</h2>
<ol class="steps">
  <li><strong>Choose DEG or RAD.</strong> Set the angle mode before any trig problem. Use degrees for most geometry and high-school trig, radians for calculus and physics formulas written in radians.</li>
  <li><strong>Type your expression.</strong> Click the keys or type on your keyboard. Use parentheses to group parts of the problem.</li>
  <li><strong>Press equals.</strong> The answer appears and is added to your history, so you can look back at earlier results while working through a problem set.</li>
</ol>

<h2 id="functions">What the keys do</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Key</th><th>What it does</th><th>Example</th></tr></thead>
<tbody>
<tr><td>+ − × ÷</td><td>Basic operations</td><td>12 × 4 = 48</td></tr>
<tr><td>( )</td><td>Group terms so they are calculated first</td><td>(3 + 5) × 2 = 16</td></tr>
<tr><td>x²</td><td>Square a number</td><td>7² = 49</td></tr>
<tr><td>xʸ</td><td>Raise to any power</td><td>2¹⁰ = 1024</td></tr>
<tr><td>√</td><td>Square root</td><td>√144 = 12</td></tr>
<tr><td>sin, cos, tan</td><td>Trig functions (uses DEG or RAD)</td><td>sin 30° = 0.5</td></tr>
<tr><td>sin⁻¹, cos⁻¹, tan⁻¹</td><td>Inverse trig: find the angle</td><td>tan⁻¹ 1 = 45°</td></tr>
<tr><td>log</td><td>Base-10 logarithm</td><td>log 1000 = 3</td></tr>
<tr><td>ln</td><td>Natural log (base e)</td><td>ln e = 1</td></tr>
<tr><td>π, e</td><td>Constants</td><td>π ≈ 3.14159, e ≈ 2.71828</td></tr>
<tr><td>n!</td><td>Factorial</td><td>5! = 120</td></tr>
<tr><td>%</td><td>Percent</td><td>50% = 0.5</td></tr>
<tr><td>±</td><td>Change the sign</td><td>8 becomes −8</td></tr>
</tbody></table></div>

<h2 id="order-of-operations">Order of operations</h2>
<p>The calculator follows the standard order of operations taught in US math classes, often remembered as PEMDAS: parentheses, exponents, multiplication and division (left to right), then addition and subtraction (left to right).</p>
<div class="formula">2 + 3 × 4² = 2 + 3 × 16 = 2 + 48 = 50</div>
<p>If you want the addition to happen first, add parentheses: (2 + 3) × 4² = 5 × 16 = 80. When in doubt, use more parentheses rather than fewer.</p>

<div class="example-box"><h4>Worked example: right triangle</h4>
<p>A right triangle has legs of 3 and 4. Find the hypotenuse and the angle opposite the side of length 3.</p>
<p><strong>Hypotenuse:</strong> √(3² + 4²) = √(9 + 16) = √25 = <strong>5</strong>.</p>
<p><strong>Angle (DEG mode):</strong> tan⁻¹(3 ÷ 4) = tan⁻¹(0.75) ≈ <strong>36.87°</strong>.</p>
<p>Check: sin(36.87°) ≈ 0.6, which matches opposite ÷ hypotenuse = 3 ÷ 5.</p>
</div>

<h2 id="deg-vs-rad">Degrees vs. radians: the most common mistake</h2>
<p>The single biggest source of wrong answers on a scientific calculator is the angle mode. In DEG mode, sin(30) = 0.5. In RAD mode, sin(30) means the sine of 30 radians, which is about −0.988. Same keys, completely different answer.</p>
<div class="compare">
<div class="compare-col"><h4>Use DEG when</h4><ul><li>The problem uses the ° symbol</li><li>You are in geometry or intro trig</li><li>Angles look like 30, 45, 90</li></ul></div>
<div class="compare-col"><h4>Use RAD when</h4><ul><li>Angles include π, like π/6</li><li>You are in precalculus, calculus, or physics</li><li>Formulas use radians by definition</li></ul></div>
</div>
<p>To convert: degrees × π ÷ 180 = radians, and radians × 180 ÷ π = degrees. So 180° = π radians.</p>

<h2 id="common-uses">Common problems you can solve</h2>
<ul>
  <li><strong>Exponential growth:</strong> $1,000 growing 5% a year for 10 years is 1000 × 1.05¹⁰ ≈ 1,628.89.</li>
  <li><strong>Scientific notation:</strong> 6.02 × 10²³ divided by 2 is 3.01 × 10²³. Use xʸ for the power of 10.</li>
  <li><strong>Logarithms in chemistry:</strong> the pH of a solution with [H⁺] = 0.001 is −log(0.001) = 3.</li>
  <li><strong>Combinations:</strong> the number of ways to choose 2 of 5 items is 5! ÷ (2! × 3!) = 120 ÷ 12 = 10.</li>
  <li><strong>Unit circle check:</strong> in RAD mode, cos(π) = −1 and sin(π ÷ 2) = 1.</li>
</ul>

<h2 id="tips">Tips for students</h2>
<ul>
  <li><strong>Use the keyboard to go faster.</strong> Type numbers, operators, and parentheses directly instead of clicking every key.</li>
  <li><strong>Check your history.</strong> Your earlier results are saved in the history list, which helps when one answer feeds the next step of a problem.</li>
  <li><strong>Estimate first.</strong> If √50 comes out as 70, something went wrong. A quick mental estimate (a bit more than 7) catches typing errors.</li>
  <li><strong>Know the test rules.</strong> Many classes and exams require a specific handheld calculator, and online calculators are usually not allowed during tests. Practice with the type you will use on exam day.</li>
</ul>
<p>Working with fractions? The <a href="/fraction-calculator">fraction calculator</a> keeps answers as exact fractions and shows the steps. For quick percent problems, try the <a href="/percentage-calculator">percentage calculator</a>.</p>
HTML,
  'faqs'        => [
    ['Why does my calculator give the wrong answer for sin or cos?', 'It is almost always the angle mode. sin(30) is 0.5 in DEG mode but about −0.988 in RAD mode. Switch to the mode your problem uses.'],
    ['What is the difference between log and ln?', 'log is the base-10 logarithm, so log 1000 = 3. ln is the natural logarithm with base e, so ln e = 1.'],
    ['Can I type on my keyboard instead of clicking?', 'Yes. The calculator supports keyboard input for numbers, operators, and parentheses.'],
    ['Does the scientific calculator follow order of operations?', 'Yes. It applies parentheses first, then exponents, then multiplication and division, then addition and subtraction. Use parentheses to control the order.'],
    ['How do I calculate a factorial?', 'Enter the number and press n!. For example, 5! = 5 × 4 × 3 × 2 × 1 = 120.'],
    ['Does the calculator keep a history?', 'Yes. Each result is added to a history list so you can refer back to earlier answers.'],
  ],
];
