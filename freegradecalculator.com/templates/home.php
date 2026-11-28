<?php
$faqs = [
    ['Is this grade calculator really free?', 'Yes. Every calculator on FreeGradeCalculator is 100% free, with no account, no email and no limits. The site is supported by unobtrusive Amazon affiliate links to study supplies.'],
    ['How does the grade calculator work?', 'Enter each grade category (tests, quizzes, homework, participation), the percentage of your final grade it is worth, and your score. The calculator multiplies each score by its weight, adds the results and divides by the total weight, then converts the percentage into a letter grade and 4.0 GPA points.'],
    ['Can I enter letter grades instead of percentages?', 'Yes. Type a letter such as A-, B+ or C and the calculator converts it to a typical percentage (for example, A- = 91.5%) before averaging. For the most accurate result, use the exact percentage from your gradebook.'],
    ['Is this a gradebook calculator for teachers too?', 'Yes. Teachers use the same weighted grades checker to verify report-card grades, plus dedicated tools such as the EZ Grader chart, the grade curve calculator and the class average calculator.'],
    ['What if my category weights don’t add up to 100%?', 'The calculator divides by the total weight you entered, so partial weights still work. That’s handy mid-semester, when only some categories have grades yet. A note under the result tells you when this happens.'],
    ['Are my grades saved or shared?', 'Your numbers never leave your device. Calculations happen in your browser, and your last entries are stored only in your browser’s local storage so you can pick up where you left off. Tap Reset to clear them.'],
    ['What grading scale do you use?', 'The standard US scale: A 93–96, A- 90–92, B+ 87–89, B 83–86, and so on down to F below 60, with A/A+ = 4.0, A- = 3.7, B+ = 3.3 and B = 3.0 GPA points. Schools vary, so always check your syllabus.'],
];
$schema = [
    ['@type' => 'WebApplication', 'name' => 'Grade Calculator', 'url' => SITE_URL . '/', 'applicationCategory' => 'EducationalApplication', 'operatingSystem' => 'Any (web browser)', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'description' => 'Free weighted grade calculator and gradebook calculator online for students and teachers.'],
    faq_schema($faqs),
];
page_start([
    'title' => 'Grade Calculator – Free Weighted Grades Checker & GPA Tools',
    'description' => 'Free grade calculator: check your weighted class grade, find what you need on the final, and convert to GPA. A fast, private gradebook calculator online.',
    'path' => '/', 'schema' => $schema, 'tools_js' => true, 'body_class' => 'page-home', 'image' => 'graduation-caps-sky',
]);
$popular = array_filter(tools(), fn($t) => $t[4]);
?>
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><div class="hero-grid"></div><div class="blob blob-1"></div><div class="blob blob-2"></div><div class="blob blob-3"></div></div>
  <div class="floaters" aria-hidden="true"><span class="floater f1">A+ 98%</span><span class="floater f2">GPA 3.87</span><span class="floater f3">B+ → A-</span><span class="floater f4">Final: 84%</span></div>
  <div class="wrap hero-inner">
    <div class="reveal in">
      <span class="eyebrow"><span>New</span> 29 free calculators for students &amp; teachers</span>
      <h1>The free grade calculator for <span class="grad-text typed" data-words='["every class.","your final.","your GPA.","teachers.","finals week."]'>every class.</span></h1>
      <p class="lead">Check your weighted grade in seconds, find exactly what you need on the final, and turn any score into a letter and GPA. A gradebook calculator online that works beautifully on your phone.</p>
      <div class="hero-badges">
        <span class="hero-badge"><?= icon('check') ?> No sign-up</span><span class="hero-badge"><?= icon('shield') ?> Private — stays on your device</span><span class="hero-badge"><?= icon('phone') ?> Built for mobile</span>
      </div>
      <div class="hero-cta"><a class="btn btn-primary" href="#calculator"><?= icon('zap') ?> Calculate my grade</a><a class="btn btn-ghost" href="/tools"><?= icon('grid') ?> Browse all tools</a></div>
    </div>
    <div class="reveal in reveal-d2" id="calculator"><?php $tag = 'h2'; include ROOT . '/widgets/weighted-grade-calculator.php'; ?></div>
  </div>
</section>

<section aria-label="Popular calculators" style="padding:6px 0 10px">
  <div class="marquee"><div class="marquee-track">
    <?php for ($k = 0; $k < 2; $k++) foreach (tools() as $s => $t): ?><a href="/<?= e($s) ?>"<?= $k ? ' tabindex="-1" aria-hidden="true"' : '' ?>><?= icon($t[2]) ?> <?= e($t[0]) ?></a><?php endforeach; ?>
  </div></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="counters">
      <div class="counter reveal"><b data-count="29">0</b><span>Free calculators</span></div>
      <div class="counter reveal reveal-d1"><b data-count="0" data-suffix="">0</b><span>Sign-ups required</span></div>
      <div class="counter reveal reveal-d2"><b data-count="100" data-suffix="%">0</b><span>Private &amp; on-device</span></div>
      <div class="counter reveal reveal-d3"><b data-count="4.0" data-suffix="">0</b><span>GPA scale, plus weighted 5.0</span></div>
    </div>
  </div>
</section>

<section class="section section-alt" id="popular">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Most used</span><h2>Popular grade &amp; GPA tools</h2><p>From “what do I need on my final?” to weighted high school GPA — pick a calculator and get an answer in seconds.</p></div>
    <div class="tool-grid"><?php foreach ($popular as $s => $t) include ROOT . '/templates/partials/tool-card.php'; ?></div>
    <p style="text-align:center;margin-top:26px"><a class="btn btn-ghost" href="/tools">See all 29 calculators <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section">
  <div class="wrap gpa-play">
    <div class="reveal">
      <span class="kicker">Try it</span>
      <h2>Slide to see your letter grade and GPA</h2>
      <p class="muted">Drag the slider to any percentage and watch it convert to a letter grade and 4.0 GPA points on the standard US scale. Need exact numbers for a whole transcript? Use the <a href="/gpa-calculator">college GPA calculator</a> or the <a href="/high-school-gpa-calculator">high school GPA calculator</a>.</p>
      <label class="lbl" for="gauge-range">Your percentage</label>
      <input class="range" id="gauge-range" type="range" min="40" max="100" step="1" value="88">
    </div>
    <div class="gauge reveal reveal-d1" aria-live="polite">
      <svg viewBox="0 0 300 180" role="img" aria-label="Grade gauge">
        <defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#f43f5e"/><stop offset=".5" stop-color="#f59e0b"/><stop offset="1" stop-color="#10b981"/></linearGradient></defs>
        <path d="M30 160 A120 120 0 0 1 270 160" fill="none" stroke="var(--line)" stroke-width="22" stroke-linecap="round"/>
        <path id="gauge-arc" d="M30 160 A120 120 0 0 1 270 160" fill="none" stroke="url(#gg)" stroke-width="22" stroke-linecap="round" style="transition:stroke-dashoffset .4s"/>
      </svg>
      <div class="gauge-val"><b id="gauge-letter">B+</b><span id="gauge-pct">88%</span> · <span id="gauge-gpa">3.3 GPA</span></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">How it works</span><h2>Check your grade in three steps</h2></div>
    <div class="how-steps">
      <div class="how-step reveal"><h3>Add your categories</h3><p>Copy the grading breakdown from your syllabus — tests 40%, homework 25%, and so on. Add or remove rows to match your class.</p></div>
      <div class="how-step reveal reveal-d1"><h3>Enter your scores</h3><p>Type percentages like 92 or letter grades like A-. Mix and match — our grades checker understands both.</p></div>
      <div class="how-step reveal reveal-d2"><h3>See your grade instantly</h3><p>Get your weighted percentage, letter grade and GPA points, with a breakdown of every category. Your entries are saved on your device.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="photo-stack reveal"><img class="parallax" src="/assets/img/photos/college-group-study.webp" srcset="/assets/img/photos/college-group-study-sm.webp 600w, /assets/img/photos/college-group-study.webp 1200w" sizes="(max-width: 900px) 100vw, 560px" width="1200" height="800" alt="College students studying together around a table" loading="lazy"><div class="ps-badge"><span class="grade-pill g-a" style="height:44px;min-width:44px;font-size:1.2rem">A</span><span><b>93.4%</b><br><small class="muted">Weighted grade</small></span></div></div>
    <div class="reveal reveal-d1">
      <span class="kicker">For students</span>
      <h2>More than a class calculator</h2>
      <p class="muted">Most grade calculators stop at one number. We built a full toolkit around the questions students actually ask during the semester:</p>
      <ul class="check-list">
        <li><span><b>What’s my grade right now?</b> The weighted <a href="/">grade calculator</a> above, or the <a href="/points-grade-calculator">points calculator</a> for points-based classes.</span></li>
        <li><span><b>What do I need on the final?</b> The <a href="/final-grade-calculator">final grade calculator</a> shows the exact score for an A, B, C or D.</span></li>
        <li><span><b>Can I still raise my grade?</b> The <a href="/raise-my-grade-calculator">raise my grade calculator</a> tells you what average to hit on the work that’s left.</span></li>
        <li><span><b>What’s my GPA?</b> <a href="/gpa-calculator">College</a>, <a href="/high-school-gpa-calculator">high school</a> and <a href="/cumulative-gpa-calculator">cumulative</a> GPA calculators.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split rev">
    <div class="photo-stack reveal"><img class="parallax" src="/assets/img/photos/teacher-classroom.webp" srcset="/assets/img/photos/teacher-classroom-sm.webp 600w, /assets/img/photos/teacher-classroom.webp 1200w" sizes="(max-width: 900px) 100vw, 560px" width="1200" height="800" alt="Teacher walking through a classroom of students" loading="lazy"><div class="ps-badge"><?= icon('table') ?><span><b>EZ</b> Grader<br><small class="muted">Print-ready charts</small></span></div></div>
    <div class="reveal reveal-d1">
      <span class="kicker">For teachers</span>
      <h2>A gradebook calculator online that saves hours</h2>
      <p class="muted">Grading a stack of quizzes? Our teacher tools are fast enough to use between classes and simple enough to share with parents.</p>
      <ul class="check-list">
        <li><span><a href="/easy-grader"><b>EZ Grader</b></a> — a printable chart of scores for any number of questions.</span></li>
        <li><span><a href="/grade-curve-calculator"><b>Grade curve calculator</b></a> — flat, square-root and bell-curve methods side by side.</span></li>
        <li><span><a href="/class-average-calculator"><b>Class average calculator</b></a> — mean, median, standard deviation and grade distribution.</span></li>
        <li><span><a href="/rubric-grade-calculator"><b>Rubric converter</b></a> — turn 4-point rubric scores into percentages.</span></li>
      </ul>
      <a class="btn btn-primary" href="/tools#teachers"><?= icon('apple') ?> Explore teacher tools</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">From the blog</span><h2>Guides to grades, GPA &amp; test scores</h2><p>Clear, worked-example explanations written for students, parents and teachers.</p></div>
    <div class="post-grid"><?php foreach (array_slice(articles(), 0, 6) as $a) include ROOT . '/templates/partials/post-card.php'; ?></div>
    <p style="text-align:center;margin-top:26px"><a class="btn btn-ghost" href="/blog">Read all guides <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="kicker">Study smarter</span><h2>Gear that helps your grades</h2><p>Calculators and study tools that teachers and top students actually recommend.</p></div>
    <?= product_grid(['ti-84-plus-ce', 'ti-30xs', 'academic-planner', 'noise-cancelling-headphones']) ?>
    <p style="text-align:center"><a class="btn btn-ghost" href="/study-supplies">See all study supplies <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section">
  <div class="wrap prose" style="margin:0 auto">
    <h2 id="about-grade-calculator">A grade calculator you can trust</h2>
    <p>FreeGradeCalculator started as a simple weighted grade calculator for US students and has grown into a one-stop toolkit for anyone with a grading question. Whether you call it a grades checker, a class calculator or a gradebook calculator, the idea is the same: plug in what you know, and see exactly where you stand — and what it will take to finish strong.</p>
    <h3>How weighted grades are calculated</h3>
    <p>Most high school and college classes use <strong>weighted categories</strong>. Each category’s average is multiplied by its weight, and the results are added together. If tests are worth 40% and you average 88%, they contribute 35.2 points; homework at 25% with a 95% average adds 23.75 points; and so on. Our calculator does this math instantly — and if your weights don’t total 100% yet, it divides by the weight you’ve entered so the result still reflects your current standing. Learn more in our guide to <a href="/blog/how-to-calculate-weighted-grades">how to calculate weighted grades</a>.</p>
    <div class="formula">Grade = Σ (category score × weight) ÷ Σ weights</div>
    <h3>From percentage to letter grade to GPA</h3>
    <p>Once you have a percentage, the calculator converts it to a letter grade and GPA points using the most common US scale (90–92 = A-, 87–89 = B+, and so on). Not sure what a GPA is or how it’s determined? Start with <a href="/blog/what-is-gpa">What Is GPA?</a>, then try the <a href="/gpa-converter">GPA converter</a>.</p>
    <h3>Planning for finals</h3>
    <p>The most common question we get is “what do I need on my final?” The <a href="/final-grade-calculator">final grade calculator</a> answers it for any target, and our step-by-step article on <a href="/blog/how-to-calculate-your-final-grade">how to calculate final grades</a> shows the formula with real examples. Pair it with the <a href="/exam-countdown">exam countdown</a> and <a href="/pomodoro-timer">Pomodoro study timer</a> to plan your review.</p>
    <?= faqs_html($faqs, 'Grade calculator FAQs') ?>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap"><div class="cta-band reveal">
    <h2>Bookmark your new favorite study tool</h2>
    <p>Every calculator is free, private and built for your phone. Press <b>Ctrl/⌘ + K</b> anytime to jump to any tool.</p>
    <a class="btn" href="/tools"><?= icon('grid') ?> Explore all calculators</a>
  </div></div>
</section>
<?php page_end(); ?>
