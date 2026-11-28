# freegradecalculator.com — content spec

The site is custom PHP. Content lives in plain PHP files that **return an array**.
No PHP logic inside content files — only the returned array. Use nowdoc strings
(`<<<'HTML' ... HTML`) for HTML so `$` signs are safe. US English. Audience:
US high-school and college students, parents, and teachers. Tone: friendly,
expert, concrete, no fluff, no "in today's fast-paced world". Short paragraphs
(2–4 sentences) — most readers are on phones.

## 1. Articles — `content/articles/{slug}.php`

```php
<?php
return [
  'slug'        => 'how-to-calculate-cumulative-gpa',
  'title'       => 'How to Calculate Cumulative GPA (Step-by-Step With Examples)',   // H1
  'meta_title'  => 'How to Calculate Cumulative GPA: Formula + Examples',            // <= 60 chars
  'description' => '...',                                                           // 140-158 chars, contains keyword
  'keyword'     => 'how to calculate cumulative gpa',
  'category'    => 'GPA',            // one of: GPA, Grades, Test Prep, Teaching, Study Tips
  'date'        => '2026-03-14',     // published (given to you)
  'updated'     => '2026-03-14',     // may equal date
  'author'      => 'FGC Editorial Team',
  'hero'        => 'study-group-table',      // photo name from the list below (no extension)
  'hero_alt'    => 'Descriptive alt text',
  'excerpt'     => 'One or two sentence teaser for cards.',
  'related_tools' => ['cumulative-gpa-calculator', 'gpa-calculator', 'target-gpa-calculator'],
  'faqs'        => [ ['Question?', 'Answer as plain text or light HTML.'], ... ],  // 5-7 FAQs, rendered + FAQPage schema
  'body'        => <<<'HTML'
<p class="lead">Opening paragraph that answers the query fast…</p>
...
HTML,
];
```

Rules for `body`:
* **At least 2,000 words in `body`** (FAQs are extra). Aim 2,200–2,800.
* Do NOT include the H1 or the FAQ section in body (both are rendered by the template).
* Sections are `<h2 id="kebab-id">`. A table of contents is generated automatically from H2s.
  Use `<h3>` for sub-sections.
* Use the keyword naturally in the first 100 words, one H2, and the conclusion.
* Include **at least 3 photos** and **at least 2 inline SVG illustrations/charts** (see components).
* Include 2–4 tool CTAs with `[[tool:slug]]` and 1 product shortcode where it fits naturally
  (`[[product:key]]` single, or `[[products:key1,key2,key3]]` grid).
* Link internally to other articles/tools with root-relative links: `/gpa-calculator`, `/blog/what-is-gpa`.
* Facts must be accurate. Do not invent statistics, studies, or quotes. When describing policies that
  vary (GPA scales, curves), say they vary by school.

### Components (CSS already exists for these)

```html
<p class="lead">Larger intro paragraph.</p>

<div class="key-takeaways"><h3>Key takeaways</h3><ul><li>…</li></ul></div>

<figure class="figure">
  <img src="/assets/img/photos/study-group-table.webp" width="1200" height="800" alt="…" loading="lazy">
  <figcaption>Caption text.</figcaption>
</figure>

<div class="callout callout-tip"><strong>Pro tip</strong><p>…</p></div>      <!-- also callout-info, callout-warn -->

<div class="formula">GPA = Σ (grade points × credits) ÷ Σ credits</div>

<div class="example-box"><h4>Worked example</h4><p>…</p></div>

<div class="table-wrap"><table class="data-table"><thead><tr><th>…</th></tr></thead><tbody>…</tbody></table></div>

<ol class="steps"><li><strong>Step title.</strong> Explanation…</li></ol>   <!-- numbered step cards -->

<div class="compare"><div class="compare-col"><h4>Weighted</h4><ul>…</ul></div><div class="compare-col"><h4>Unweighted</h4><ul>…</ul></div></div>

<figure class="illustration">
  <svg viewBox="0 0 640 300" role="img" aria-label="Describe the chart">
    … shapes using fill="var(--c1)" etc. Text: fill="var(--ink)" or fill="var(--muted)",
    font-size 12-16, font-family="inherit". Background: none (page provides it).
  </svg>
  <figcaption>What the illustration shows.</figcaption>
</figure>
```
Illustration palette CSS variables: `--c1` indigo, `--c2` cyan, `--c3` amber, `--c4` emerald,
`--c5` rose, `--c6` violet, `--ink` main text, `--muted` secondary text, `--line` gridlines,
`--surface` card background. SVGs must look good in light and dark mode, so ONLY use these variables
for colors (no hex). Keep SVG simple: bar charts, scales, flow diagrams, number lines, gauges,
icon-style scenes. Each SVG under ~4 KB.

### Photo library (`/assets/img/photos/{name}.webp`, all 1200 px wide; height listed)
boy-laptop-homework 800 · boy-video-lesson 801 · calculus-chalkboard 800 · charts-analysis 795 ·
classroom-hands-up 800 · coffee-laptop-study 800 · college-group-study 800 · college-students-outdoors 800 ·
data-analysis-desk 800 · desk-with-books 801 · diplomas 800 · empty-classroom 800 · exam-answer-sheet 782 ·
finance-budget-desk 800 · girl-online-lesson 800 · graduates-celebrating 800 · graduation-caps-sky 800 ·
hand-writing-notebook 800 · homework-help-laptop 801 · kids-on-laptop 837 · kids-reading-teacher 800 ·
kids-taking-test 800 · laptop-notebook-top 800 · learn-math-tiles 669 · lecture-hall 857 · math-whiteboard 800 ·
online-class-desk 801 · online-class-notes 801 · parent-tutoring 808 · question-marks 801 ·
scientific-calculator 900 · smiling-student-laptop 800 · stressed-student-books 722 · student-at-computer 801 ·
student-holding-books 800 · student-laptop-couch 800 · students-hallway 987 · students-on-steps 801 ·
study-group-table 800 · study-table-top 800 · teach-blocks 801 · teacher-chalkboard 743 · teacher-classroom 800 ·
teacher-lecturing 800 · teacher-recording-lesson 800 · top-view-study-desk 800 · writing-notes 800

Descriptions: math-whiteboard = boy solving exponent problems on whiteboard; calculus-chalkboard = hand writing
calculus on chalkboard; exam-answer-sheet = student filling in a test sheet with pencil; kids-taking-test = kids
writing at classroom desks; teach-blocks = wooden blocks spelling TEACH; learn-math-tiles = Scrabble tiles
"LEARN MATH"; question-marks = paper question-mark speech bubbles; stressed-student-books = tired student between
stacks of books; diplomas = rolled diplomas with red ribbons; lecture-hall = empty university lecture hall;
scientific-calculator = Casio graphing calculator on wood; charts-analysis = pen over printed bar/line charts;
parent-tutoring = mother helping son study; teacher-chalkboard = teacher writing on chalkboard; others are
self-explanatory (students studying on laptops, notebooks, classrooms, graduation).

### Tool slugs (link as `/slug`, CTA as `[[tool:slug]]`)
weighted-grade-calculator, final-grade-calculator, test-grade-calculator, points-grade-calculator,
letter-grade-calculator, semester-grade-calculator, raise-my-grade-calculator, rubric-grade-calculator,
gpa-calculator, high-school-gpa-calculator, cumulative-gpa-calculator, gpa-converter,
cgpa-to-percentage-calculator, target-gpa-calculator, easy-grader, grade-curve-calculator,
class-average-calculator, attendance-percentage-calculator, act-score-calculator, sat-superscore-calculator,
percentage-calculator, average-calculator, weighted-average-calculator, fraction-calculator,
scientific-calculator, word-counter, pomodoro-timer, exam-countdown, student-loan-calculator
(The homepage `/` is the main grade calculator.)

### Article slugs (link as `/blog/slug`)
what-is-gpa, how-to-calculate-your-final-grade, how-to-calculate-cumulative-gpa, weighted-vs-unweighted-gpa,
what-is-a-good-gpa, is-a-3-0-gpa-good, how-to-raise-your-gpa, how-to-convert-percentage-to-gpa,
how-to-calculate-weighted-grades, how-to-curve-grades, what-is-a-good-sat-score, standards-based-grading

### Amazon product keys (for `[[product:key]]`)
ti-84-plus-ce, ti-30xs, casio-fx-991ex, casio-fx-115es, ti-nspire-cx-ii, academic-planner, index-cards,
highlighters, noise-cancelling-headphones, desk-lamp, sticky-notes, teacher-gradebook, grading-pens,
visual-timer, sat-study-guide, act-prep-guide, straight-a-book, make-it-stick-book, laptop-stand, desk-whiteboard

## 2. Tool page copy — `content/tools/{slug}.php`

```php
<?php
return [
  'h1'          => 'Final Grade Calculator',
  'meta_title'  => 'Final Grade Calculator – What Do I Need on My Final?',   // <= 60 chars
  'description' => '...',            // 140-158 chars
  'lead'        => 'One sentence shown under the H1, above the calculator.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the final grade calculator</h2>
<ol class="steps"><li>…</li></ol>
<h2 id="formula">The formula</h2>
<div class="formula">…</div>
<div class="example-box"><h4>Example</h4>…</div>
… more sections (tips, interpreting results, common mistakes, related scale table) …
HTML,
  'faqs'        => [ ['Q?', 'A.'], ... ],   // 4-6
];
```
Body: 600–900 words, H2s with ids, uses the components above (no photos required; one optional),
1–3 internal links to related tools/articles, accurate formulas matching what the tool does
(see the tool description given to you). Do not describe UI elements that the tool does not have.

## 3. Keywords the old site ranked for (must be targeted on these pages)

* **`/` homepage** (main weighted grade calculator): grade calculator, grades checker, gradebook calculator online, class calculator.
* **`/final-grade-calculator`**: final grade calculator, grading calculator for finals, final test score calculator,
  free online grading calculator, final exam grader, grading book calculator.
* **`/blog/how-to-calculate-your-final-grade`**: calculate final grades / how to calculate final grades,
  how to calculate grades by percentage(s) / calculating grades with percentages / how to calculate percentage for
  grades, how final grades are calculated, how to compute grades, formula for grades / calculating grades formula,
  how to add grades (up), how do teachers calculate grades, how to calculate what you need on a final, final exam grades.
* **`/blog/what-is-gpa`**: gpa, what is gpa / what does gpa mean / gpa meaning / gpa def, how is gpa determined /
  what is gpa based on, what is term gpa, what is overall gpa / academic gpa vs total gpa, what is a passing gpa
  (5,400/mo — give it its own H2), mean gpa, gpa score.

Use these as H2/H3 phrasings and in body copy naturally — no stuffing.

## 4. What each tool does (copy must match exactly)

1. **weighted-grade-calculator** — rows of (category name, weight %, score as % or letter like A-). Outputs weighted
   %, letter grade and 4.0 GPA points. If weights don't add to 100 it normalizes by the total weight and says so.
   Add/remove rows. (The homepage hosts the same calculator.)
2. **final-grade-calculator** — inputs: current grade (% or letter), desired grade (% or letter), final exam weight %.
   Output: score needed on the final, plus a table of the score needed for an A (90), B (80), C (70), D (60).
   Formula: required = (desired − current × (1 − w)) ÷ w.
3. **test-grade-calculator** — total questions (or points) and number wrong (toggle to number right). Output: % score,
   letter grade, and a full chart of every possible number wrong → %.
4. **points-grade-calculator** — rows of assignments with points earned / points possible. Output: total earned,
   total possible, %, letter.
5. **letter-grade-calculator** — percentage → letter grade + GPA points using the standard US scale (A+ 97–100,
   A 93–96, A- 90–92, B+ 87–89, B 83–86, B- 80–82, C+ 77–79, C 73–76, C- 70–72, D+ 67–69, D 63–66, D- 60–62, F <60).
   Shows the full scale table with the matching row highlighted.
6. **semester-grade-calculator** — quarter 1 grade, quarter 2 grade, final exam grade with weights (default 40/40/20).
   Output semester grade + letter; second mode: score needed on the final to hit a target semester grade.
7. **raise-my-grade-calculator** — points earned so far, points possible so far, points still to come, target %.
   Output: average % needed on remaining work; also the highest and lowest final grade still possible.
8. **rubric-grade-calculator** — rubric points earned and total rubric points (e.g. 18/24, or 3.25/4 for a 4-point
   rubric) → % and letter, plus a conversion chart for every whole/half score.
9. **gpa-calculator** (college) — course rows (name, letter grade A+…F, credits). 4.0 scale (A+ = 4.0, A 4.0, A- 3.7,
   B+ 3.3, B 3.0, B- 2.7, C+ 2.3, C 2.0, C- 1.7, D+ 1.3, D 1.0, D- 0.7, F 0). Output semester GPA, credits, quality
   points. Optional: previous cumulative GPA + credits → new cumulative GPA.
10. **high-school-gpa-calculator** — course rows (grade letter, credits, type Regular / Honors / AP-IB). Outputs
    unweighted GPA and weighted GPA (Honors +0.5, AP/IB +1.0; F gets no boost). Notes schools vary.
11. **cumulative-gpa-calculator** — current cumulative GPA + credits earned; add one or more terms (term GPA +
    credits). Output new cumulative GPA and total credits. Formula: Σ(GPA×credits) ÷ Σcredits.
12. **gpa-converter** — percentage or letter → 4.0 GPA (and letter), and GPA → typical letter/percentage range, using
    the scale above. Includes the full conversion table.
13. **cgpa-to-percentage-calculator** — 10-point CGPA × 9.5 (CBSE convention) with an editable multiplier; reverse
    percentage → CGPA; and a note that universities may publish their own formula.
14. **target-gpa-calculator** — current GPA, credits completed, target GPA, credits remaining/next term → GPA
    needed on those credits; says if > 4.0 (not reachable) .
15. **easy-grader** (EZ Grader for teachers) — number of questions/points (1–200), optional half-point steps →
    full chart of number wrong → number right → %, letter; printable.
16. **grade-curve-calculator** — paste a list of scores; methods: (a) flat curve so the top score becomes 100,
    (b) add N points to everyone, (c) square-root curve 10×√score, (d) shift to a target class average,
    (e) bell curve: rescale to target mean and standard deviation. Shows original vs curved table + new average;
    option to cap at 100.
17. **class-average-calculator** — paste scores → count, mean, median, mode, range, min, max, standard deviation
    (population), and a letter-grade distribution bar chart.
18. **attendance-percentage-calculator** — classes held, classes attended, required % (default 75) → current
    attendance %, how many classes you can miss and stay above the requirement, or how many in a row you must
    attend to reach it.
19. **act-score-calculator** — English, Math, Reading, Science scores (1–36). Composite = average rounded to the
    nearest whole number (.5 rounds up). Default: enhanced ACT (2025+) composite of English, Math and Reading with
    Science optional/separate; toggle "include Science (legacy ACT)". Also shows STEM score = average of Math and
    Science (rounded).
20. **sat-superscore-calculator** — up to 4 test dates, each with Reading & Writing and Math (200–800). Output best
    section scores, superscore (sum of bests), and best single-sitting total.
21. **percentage-calculator** — three modes: X% of Y; X is what % of Y; % change from X to Y.
22. **average-calculator** — list of numbers → mean, median, mode, range, sum, count.
23. **weighted-average-calculator** — value + weight rows → weighted average, Σweights.
24. **fraction-calculator** — two fractions (or mixed numbers), + − × ÷ → simplified fraction, mixed number,
    decimal, with steps.
25. **scientific-calculator** — keypad: + − × ÷, parentheses, x², xʸ, √, sin/cos/tan (+ inverse), DEG/RAD,
    log, ln, π, e, n!, %, ±, history of results; keyboard input supported.
26. **word-counter** — words, characters (with/without spaces), sentences, paragraphs, reading time (238 wpm),
    speaking time (130 wpm), top repeated words; optional word goal with progress bar.
27. **pomodoro-timer** — focus/short break/long break (default 25/5/15, long break every 4), editable, progress
    ring, chime, completed-session counter, current task label.
28. **exam-countdown** — exam name + date/time → live days/hours/minutes/seconds countdown; enter total study
    hours needed → hours per day; saved in the browser.
29. **student-loan-calculator** — loan amount, APR %, term years (standard repayment) → monthly payment, total
    interest, total paid, and a yearly balance chart. Formula M = P·r / (1 − (1+r)^−n).
