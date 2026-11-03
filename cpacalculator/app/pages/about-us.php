<?php
defined('CPA') or exit;
$P['title'] = 'About CPA Calculator — Making CPA-Level Tax Tools Simple';
$P['description'] = 'CPA Calculator builds free, accurate tax and accounting calculators that explain the math in plain English for employees, freelancers and small businesses.';
$P['pageType'] = 'AboutPage';
echo simple_hero('Making CPA-level tools simple for everyone', 'You shouldn’t need an accounting degree to understand your own numbers. That’s why we built CPA Calculator.', 'About Us');
?>
<div class="wrap content-grid"><article class="prose">
<p class="lead">Money decisions are part of everyday life — what to set aside from a 1099 check, whether a raise changes your bracket, whether an S corp is worth it. The answers usually sit behind jargon or an hourly fee. CPA Calculator bridges that gap.</p>
<h2 id="mission">Our mission</h2>
<p>To make professional-grade financial tools and explanations available to anyone, free, without the complexity. We take the calculations a CPA normally handles and turn them into tools that show their work and articles that explain the “why”.</p>
<h2 id="offer">What we offer</h2>
<h3>Smart calculators</h3>
<p><?= count(TOOLS) ?> free calculators covering <a href="/calculators/federal-income-tax/">federal income tax</a>, <a href="/calculators/1099-tax-calculator/">1099</a> and <a href="/calculators/self-employment-tax/">self-employment tax</a>, <a href="/calculators/quarterly-estimated-tax/">quarterly estimates</a>, <a href="/calculators/paycheck-calculator/">paychecks</a>, <a href="/calculators/capital-gains-tax/">capital gains</a>, <a href="/calculators/s-corp-tax-savings/">S corp savings</a>, <a href="/calculators/depreciation-calculator/">depreciation</a>, <a href="/calculators/profit-margin/">margins</a> and more. Each one is easy to use, built on current IRS figures and honest about its limits.</p>
<h3>Practical guides</h3>
<p>Our <a href="/blog/">tax guides</a> explain the rules in plain English with worked examples — what to do when you get a 1099, how quarterly taxes work, what every box on your W-2 means.</p>
<h3>CPA-level thinking, simplified</h3>
<p>We are not a replacement for a licensed CPA. Think of CPA Calculator as your first step: understand your situation, set aside the right amount and walk into your accountant’s office with better questions.</p>
<h2 id="who">Who it’s for</h2>
<ul><li>Freelancers, contractors and gig workers</li><li>Employees checking withholding or a job offer</li><li>Small-business owners and side hustlers</li><li>First-time filers</li><li>Anyone who has ever thought “I wish this were easier”</li></ul>
<h2 id="principles">What we believe</h2>
<ul class="checks">
  <li><?= icon('check') ?><span><strong>Accuracy over shortcuts.</strong> We follow the actual order of operations on the tax return. <a href="/our-methodology/">Read our methodology</a>.</span></li>
  <li><?= icon('check') ?><span><strong>Show the work.</strong> A number without an explanation isn’t much help.</span></li>
  <li><?= icon('check') ?><span><strong>Privacy first.</strong> Calculations run in your browser and we never store your inputs.</span></li>
  <li><?= icon('check') ?><span><strong>Free, for real.</strong> No account, no email gate, no paywall.</span></li>
</ul>
<h2 id="contact">Get in touch</h2>
<p>Questions, corrections or ideas for a new calculator? Email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a> or use our <a href="/contact/">contact form</a>.</p>
</article>
<aside class="aside"><div class="card"><div class="res-label" style="margin-bottom:10px">On this page</div><ul class="toc" data-toc></ul><div class="aside-cta"><strong>Start with your taxes</strong>Free estimate in under a minute.<a class="btn btn-sm" href="/calculators/">All calculators</a></div></div></aside>
</div>
