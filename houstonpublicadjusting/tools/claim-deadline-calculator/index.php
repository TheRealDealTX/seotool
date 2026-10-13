<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'claim-deadline-calculator',
    'title' => 'Texas Insurance Claim Deadline Calculator (Prompt Payment Act)',
    'desc' => 'Map your Texas insurance claim deadlines: Prompt Payment Act acknowledgment, decision and payment dates plus key policy deadlines. Free from Houston Public Adjusters.',
    'h1' => 'Texas Insurance Claim Deadline Calculator',
    'lede' => 'Chapter 542 of the Texas Insurance Code sets deadlines your insurer must meet. Enter your dates to see what should have happened by when &mdash; and which deadlines are yours.',
    'form' => '
<form data-tool="deadline" data-out="out-deadline" class="tool-grid">
  <label>Date of loss<input name="loss" type="date"><span class="hint">The day the storm, fire or leak happened</span></label>
  <label>Date you reported the claim<input name="notice" type="date"></label>
  <label>Date you sent everything the insurer requested<input name="docs" type="date"><span class="hint">Optional</span></label>
  <label style="display:flex;gap:10px;align-items:center;margin-top:26px"><input name="cat" type="checkbox" style="width:auto;margin:0"> Declared weather catastrophe <span class="hint" style="margin:0">(adds 15 days)</span></label>
</form>
<div class="tool-result" id="out-deadline" aria-live="polite"></div>',
    'prose' => '
<h2>The Texas Prompt Payment of Claims Act</h2>
<p>Texas Insurance Code Chapter 542, Subchapter B, puts first-party property insurers on a clock:</p>
<ul class="checklist">
  <li><strong>15 days</strong> after notice of the claim to acknowledge it, begin the investigation and request what it needs from you (&sect;542.055)</li>
  <li><strong>15 business days</strong> after receiving everything it requested to accept or reject the claim in writing, with up to <strong>45 more days</strong> if it explains why it needs them (&sect;542.056)</li>
  <li><strong>5 business days</strong> after accepting the claim to pay it (&sect;542.057)</li>
  <li>An extra <strong>15 days</strong> on these deadlines after a weather catastrophe or major natural disaster (&sect;542.059)</li>
</ul>
<p>An insurer that violates these deadlines can owe statutory interest on the amount of the claim plus reasonable attorney&rsquo;s fees (&sect;542.060). These are general rules; surplus lines carriers, TWIA and some policy types follow different timelines.</p>
<h2>Deadlines that belong to you</h2>
<p>Policies require prompt notice, and many Texas homeowners policies require wind and hail damage to be reported within one year of the storm. TWIA policies require it by statute. Most policies also limit how long you have to sue, often two years. And before suing over a weather-related claim, Texas generally requires 61 days&rsquo; written pre-suit notice (Chapter 542A). Don&rsquo;t let a deadline make the decision for you &mdash; see <a href="/when-waiting-to-hire-a-public-adjuster-can-cost-you/">when waiting can cost you</a>.</p>',
    'faqs' => [
        ['How long does an insurance company have to pay a claim in Texas?', 'Generally 5 business days after it notifies you that the claim is accepted. Acceptance itself must come within 15 business days after the insurer receives all items it requested, or up to 45 days later if it gives written reasons.'],
        ['How long do I have to file a hail or wind claim in Texas?', 'It depends on your policy. Many Texas homeowners policies and all TWIA policies require wind and hail claims to be filed within one year of the date of loss. Report damage as soon as you find it.'],
    ],
]);
