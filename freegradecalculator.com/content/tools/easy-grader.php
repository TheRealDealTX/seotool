<?php
return [
  'h1'          => 'Easy Grader (EZ Grader) for Teachers',
  'meta_title'  => 'EZ Grader – Free Easy Grader Chart for Teachers',
  'description' => 'Free EZ Grader for teachers: enter the number of questions or points (1–200) and get a printable easy grader chart of wrong answers, percent, and letter.',
  'lead'        => 'Enter how many questions or points your test has and get a full, printable EZ grader chart showing number wrong, number right, percentage, and letter grade.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the easy grader</h2>
<p>This free easy grader works like the classic cardboard EZ grader slide chart that teachers have kept in their desk drawers for decades, except it builds the chart for any test length in a second. You never have to hunt for the right row or squint at tiny print.</p>
<ol class="steps">
  <li><strong>Enter the number of questions or points.</strong> Type any whole number from 1 to 200. Use the question count for a test where every item is worth one point, or the total points for a quiz with point values.</li>
  <li><strong>Turn on half-point steps if you need them.</strong> If you give partial credit in half points, switch on the half-point option and the chart adds rows for 0.5, 1.5, 2.5 wrong, and so on.</li>
  <li><strong>Read across the row.</strong> Find the number a student got wrong. The same row shows the number right, the percentage score, and the letter grade.</li>
  <li><strong>Print it.</strong> Print the chart and keep it next to your stack of papers so you can grade a whole class set without touching a calculator.</li>
</ol>

<h2 id="formula">The EZ grader formula</h2>
<p>Every row in the chart comes from one simple formula. The percentage is the share of questions or points the student earned.</p>
<div class="formula">Percent = (Total − Number wrong) ÷ Total × 100</div>
<p>Because every question has the same value, each wrong answer costs the same number of percentage points: 100 ÷ Total. On a 20-question quiz, each miss costs 5 points. On a 25-question test, each miss costs 4 points. On a 40-question test, each miss costs 2.5 points.</p>

<div class="example-box"><h4>Worked example</h4>
<p>A 25-question vocabulary test. A student misses 3 questions.</p>
<p>Number right = 25 − 3 = 22. Percent = 22 ÷ 25 × 100 = <strong>88%</strong>, which is a <strong>B+</strong> on the standard scale (87–89).</p>
<p>With half-point steps on a 20-point quiz, a student who loses 2.5 points earns 17.5 ÷ 20 × 100 = <strong>87.5%</strong>.</p>
</div>

<h2 id="letter-scale">Letter grade scale used in the chart</h2>
<p>The letter column uses the common US plus/minus scale. Many schools use a different cutoff (some start an A at 94 or use only straight letters), so check your district or syllabus policy before you record grades.</p>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Letter</th><th>Percent</th><th>Letter</th><th>Percent</th></tr></thead>
<tbody>
<tr><td>A+</td><td>97–100</td><td>C+</td><td>77–79</td></tr>
<tr><td>A</td><td>93–96</td><td>C</td><td>73–76</td></tr>
<tr><td>A-</td><td>90–92</td><td>C-</td><td>70–72</td></tr>
<tr><td>B+</td><td>87–89</td><td>D+</td><td>67–69</td></tr>
<tr><td>B</td><td>83–86</td><td>D</td><td>63–66</td></tr>
<tr><td>B-</td><td>80–82</td><td>D-</td><td>60–62</td></tr>
<tr><td colspan="2"></td><td>F</td><td>Below 60</td></tr>
</tbody></table></div>
<p>Want to look up a single percentage instead of a whole chart? The <a href="/letter-grade-calculator">letter grade calculator</a> converts any percentage to a letter and GPA points.</p>

<h2 id="tips">Tips for grading faster with an EZ grader</h2>
<ul>
  <li><strong>Mark wrong answers, not right ones.</strong> Counting misses is faster than counting correct answers, and the chart is organized by number wrong.</li>
  <li><strong>Use points for mixed tests.</strong> If your test has 30 multiple-choice items worth 1 point and 5 short answers worth 4 points, enter 50 total points and count points lost.</li>
  <li><strong>Print one chart per test length.</strong> Teachers who give 10-, 20-, and 25-question quizzes often keep a printed chart for each, clipped to a grading folder.</li>
  <li><strong>Watch the rounding.</strong> On tests where each miss is worth a fraction of a point, a score like 89.5% may land just under a cutoff. Decide your rounding rule before you start grading so every student is treated the same.</li>
  <li><strong>Students can use it too.</strong> Kids who know how many questions they missed can check their own score right after a test is returned.</li>
</ul>

<div class="callout callout-tip"><strong>Pro tip</strong><p>Grading a single student test where you know the number right rather than wrong? The <a href="/test-grade-calculator">test grade calculator</a> lets you enter either one and shows the same percent and letter.</p></div>

<h2 id="why-use-it">Why teachers still love the easy grader</h2>
<p>A paper EZ grader only comes in a few sizes, gets lost, and wears out. An online easy grader handles odd test lengths like 37 questions or 112 points just as easily as 20 or 50. Because the chart lists every possible score at once, you can also see at a glance how many misses separate a B from a C, which helps when you are writing a test and deciding how many questions to include.</p>
<p>The tool runs in your browser and is free. Nothing you type is needed beyond the test length, so there is no student data to worry about.</p>
HTML,
  'faqs'        => [
    ['What is an EZ grader?', 'An EZ grader (or easy grader) is a chart that shows the percentage score for every possible number of wrong answers on a test of a given length. Teachers use it to grade quickly without doing the division for each paper.'],
    ['How do I calculate a grade from the number wrong?', 'Subtract the number wrong from the total, divide by the total, and multiply by 100. For example, 3 wrong out of 25 is 22 ÷ 25 × 100 = 88%.'],
    ['How many questions can the easy grader handle?', 'Any whole number from 1 to 200 questions or points. Turn on half-point steps if you give partial credit in halves.'],
    ['Can I print the EZ grader chart?', 'Yes. The chart is printable, so you can keep a paper copy next to the tests you are grading.'],
    ['What grading scale does the chart use?', 'It uses the standard US plus/minus scale (A 93–96, B 83–86, and so on, with F below 60). Schools and teachers set their own scales, so confirm your school policy.'],
  ],
];
