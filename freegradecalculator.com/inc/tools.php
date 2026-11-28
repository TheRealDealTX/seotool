<?php
// Tool registry: slug => [name, category, icon, short description, popular?]
// Page copy for each tool lives in content/tools/{slug}.php
function tool_categories(): array {
    return [
        'grades'    => ['Grade Calculators', 'Work out course, test and final exam grades', 'grad'],
        'gpa'       => ['GPA Calculators', 'High school, college & cumulative GPA', 'cap'],
        'teachers'  => ['Teacher Tools', 'Grading charts, curves & class stats', 'apple'],
        'test-prep' => ['Test Prep', 'ACT & SAT score tools', 'target'],
        'math'      => ['Math Calculators', 'Percentages, averages, fractions & more', 'calc'],
        'study'     => ['Study Tools', 'Timers, countdowns, word counts & money', 'book'],
    ];
}
function tools(): array {
    static $t = null;
    if ($t !== null) return $t;
    $t = [
      'weighted-grade-calculator' => ['Weighted Grade Calculator', 'grades', 'scale', 'Combine categories like tests, homework and quizzes by weight.', 1],
      'final-grade-calculator'    => ['Final Grade Calculator', 'grades', 'flag', 'Find the score you need on your final exam.', 1],
      'test-grade-calculator'     => ['Test Grade Calculator', 'grades', 'check', 'Turn questions wrong into a percentage and letter.', 1],
      'points-grade-calculator'   => ['Points Grade Calculator', 'grades', 'plus', 'Add up points earned vs. points possible.', 0],
      'letter-grade-calculator'   => ['Letter Grade Calculator', 'grades', 'letter', 'Convert any percentage into a letter grade.', 0],
      'semester-grade-calculator' => ['Semester Grade Calculator', 'grades', 'calendar', 'Combine quarter grades and the final exam.', 0],
      'raise-my-grade-calculator' => ['Raise My Grade Calculator', 'grades', 'trend', 'See what you need on remaining work to hit a target.', 1],
      'rubric-grade-calculator'   => ['Rubric Grade Calculator', 'grades', 'grid', 'Convert rubric scores into percentages.', 0],
      'gpa-calculator'            => ['College GPA Calculator', 'gpa', 'cap', 'Semester and cumulative GPA on a 4.0 scale.', 1],
      'high-school-gpa-calculator'=> ['High School GPA Calculator', 'gpa', 'school', 'Weighted and unweighted GPA with Honors & AP.', 1],
      'cumulative-gpa-calculator' => ['Cumulative GPA Calculator', 'gpa', 'layers', 'Combine terms into an overall GPA.', 1],
      'gpa-converter'             => ['GPA Converter', 'gpa', 'swap', 'Percentage and letter grades to the 4.0 scale.', 0],
      'cgpa-to-percentage-calculator' => ['CGPA to Percentage', 'gpa', 'percent', 'Convert 10-point CGPA to percentage and back.', 0],
      'target-gpa-calculator'     => ['Target GPA Calculator', 'gpa', 'target', 'The GPA you need to reach your goal.', 0],
      'easy-grader'               => ['EZ Grader', 'teachers', 'table', 'Instant grading chart for any number of questions.', 1],
      'grade-curve-calculator'    => ['Grade Curve Calculator', 'teachers', 'bell', 'Curve a set of scores five different ways.', 0],
      'class-average-calculator'  => ['Class Average Calculator', 'teachers', 'chart', 'Mean, median, std. deviation & grade distribution.', 0],
      'attendance-percentage-calculator' => ['Attendance Calculator', 'study', 'user-check', 'Attendance % and how many classes you can miss.', 0],
      'act-score-calculator'      => ['ACT Score Calculator', 'test-prep', 'award', 'Composite and STEM score from section scores.', 0],
      'sat-superscore-calculator' => ['SAT Superscore Calculator', 'test-prep', 'star', 'Combine your best SAT section scores.', 0],
      'percentage-calculator'     => ['Percentage Calculator', 'math', 'percent', 'Percent of, what percent, and percent change.', 1],
      'average-calculator'        => ['Average Calculator', 'math', 'sigma', 'Mean, median, mode and range of a list.', 0],
      'weighted-average-calculator' => ['Weighted Average Calculator', 'math', 'scale', 'Average values by their weights.', 0],
      'fraction-calculator'       => ['Fraction Calculator', 'math', 'divide', 'Add, subtract, multiply & divide fractions with steps.', 0],
      'scientific-calculator'     => ['Scientific Calculator', 'math', 'calc', 'Trig, logs, powers and more — right in your browser.', 1],
      'word-counter'              => ['Word Counter', 'study', 'text', 'Words, characters and reading time for essays.', 0],
      'pomodoro-timer'            => ['Pomodoro Study Timer', 'study', 'clock', 'Focus sessions and breaks with a chime.', 1],
      'exam-countdown'            => ['Exam Countdown', 'study', 'hourglass', 'Live countdown and daily study-hours plan.', 0],
      'student-loan-calculator'   => ['Student Loan Calculator', 'study', 'dollar', 'Monthly payment and total interest.', 0],
    ];
    return $t;
}
function tool_meta(string $slug): ?array {
    $t = tools()[$slug] ?? null;
    if (!$t) return null;
    return ['slug' => $slug, 'name' => $t[0], 'cat' => $t[1], 'icon' => $t[2], 'short' => $t[3], 'popular' => (bool) $t[4]];
}
function tool_related(string $slug, int $n = 4): array {
    $m = tool_meta($slug); $out = [];
    foreach (tools() as $s => $t) if ($s !== $slug && $t[1] === $m['cat']) $out[] = $s;
    foreach (tools() as $s => $t) if ($s !== $slug && !in_array($s, $out) && $t[4]) $out[] = $s;
    return array_slice($out, 0, $n);
}
