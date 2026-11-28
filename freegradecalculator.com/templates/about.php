<?php page_start(['title' => 'About Us | Free Grade Calculator', 'description' => 'FreeGradeCalculator builds free, private grade, GPA and study calculators for students, parents and teachers. Learn who we are and how our tools work.', 'path' => '/about-us', 'schema' => [breadcrumb_schema([['Home', '/'], ['About us', '/about-us']])], 'image' => 'students-on-steps']); ?>
<section class="page-hero"><div class="hero-bg" aria-hidden="true"><div class="blob blob-1"></div><div class="blob blob-2"></div></div><div class="wrap"><?= breadcrumbs_html([['Home', '/'], ['About us', '/about-us']]) ?><h1>Making grades less stressful</h1><p class="lead">We build free, fast and private calculators that answer the grading questions students and teachers ask every day.</p></div></section>
<div class="wrap">
  <div class="split" style="padding:20px 0 40px">
    <div class="photo-stack reveal in"><?= photo('students-on-steps', 'Students studying together on campus steps', '', false) ?></div>
    <div class="prose reveal in">
      <h2>Why we built FreeGradeCalculator</h2>
      <p>Every semester, millions of students do the same anxious math: <em>What’s my grade right now? What do I need on the final? Will this B hurt my GPA?</em> Most online calculators answer one question, bury it under ads, or don’t work well on a phone.</p>
      <p>We wanted one trustworthy place for all of it — weighted grades, finals, GPA, test scores and everyday study math — designed first for the phone in your pocket.</p>
      <h2>Our principles</h2>
      <ul class="check-list">
        <li><span><b>Free forever.</b> No accounts, paywalls or limits.</span></li>
        <li><span><b>Private by design.</b> Calculations run in your browser; we never see your grades.</span></li>
        <li><span><b>Transparent math.</b> Every tool shows its formula and a worked example.</span></li>
        <li><span><b>Accurate and honest.</b> Grading policies vary, so we explain assumptions and point you to your syllabus.</span></li>
      </ul>
    </div>
  </div>
  <div class="prose" style="margin:0 auto 40px">
    <h2>How we keep things accurate</h2>
    <p>Our tools use the standard US grading scale and the formulas schools publish in their catalogs. Guides are written and reviewed by our editorial team and updated when policies change (for example, the move to the digital SAT and the enhanced ACT). If you spot something that doesn’t match your school, email us at <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a> — we read every message.</p>
    <h2>How we keep the site free</h2>
    <p>Some pages recommend study supplies with Amazon affiliate links. If you buy through them, we may earn a small commission at no cost to you. It never affects our calculators or advice. Read our <a href="/affiliate-disclosure">affiliate disclosure</a>.</p>
  </div>
  <div class="cta-band reveal in" style="margin-bottom:20px"><h2>Have an idea for a calculator?</h2><p>Tell us what you’d like to see next — we build new tools based on reader requests.</p><a class="btn" href="/contact"><?= icon('mail') ?> Contact us</a></div>
</div>
<?php page_end();
