<?php
return [
    'title'       => 'Texas Insurance Claim Deadline Calculator (Ch. 542)',
    'description' => 'Enter your claim dates to see the Texas prompt payment deadlines your insurer must meet to acknowledge, accept or reject, and pay your claim. Exports to calendar.',
    'h1'          => 'Texas claim deadline calculator',
    'lead'        => 'Texas Insurance Code Chapter 542 puts your insurer on a clock. Enter the dates you know to see each deadline, check whether it has passed, and add them all to your calendar.',
    'updated'     => '2026-10-13',
    'script'      => '/assets/js/tools/deadlines.js',
    'app'         => <<<'HTML'
<div class="tcols tcols--wide" data-dl>
  <div>
    <fieldset class="tgroup">
      <legend>Who insures the property?</legend>
      <div class="seg" data-seg="ins">
        <button type="button" class="is-on" data-v="std">Standard insurer</button>
        <button type="button" data-v="sl">Surplus lines insurer</button>
        <button type="button" data-v="twia">TWIA (windstorm)</button>
      </div>
    </fieldset>
    <fieldset class="tgroup">
      <legend>Your dates</legend>
      <div class="tf-row">
        <label class="tf">Date of loss (storm, leak, fire)<input type="date" data-in="loss"></label>
        <label class="tf">Date you reported the claim<input type="date" data-in="notice"></label>
      </div>
      <div class="tf-row">
        <label class="tf">Date the insurer had everything it asked for<small>Optional: the last document, photo or statement you sent</small><input type="date" data-in="items"></label>
        <label class="tf">Date the insurer said it will pay<small>Optional: the acceptance letter or email</small><input type="date" data-in="accept"></label>
      </div>
      <label class="tcheck"><input type="checkbox" data-in="cat"><span>The commissioner declared a <strong>weather-related catastrophe or major natural disaster</strong> for this event (adds 15 days, §542.059)</span></label>
      <label class="tcheck"><input type="checkbox" data-in="more"><span>The insurer notified me it needs <strong>more time</strong> to decide</span></label>
      <label class="tf" data-more hidden>Date of that notice<input type="date" data-in="moredate"></label>
      <label class="tcheck"><input type="checkbox" data-in="arson"><span>The insurer has said it suspects <strong>arson</strong></span></label>
    </fieldset>
  </div>
  <div>
    <div class="cl-head"><p class="tlabel" style="margin:0">Your deadlines</p><span class="badge badge--info" data-out="today"></span></div>
    <ol class="vt" data-out="list"><li><p class="vt__what">Enter the date you reported the claim to see the timeline.</p></li></ol>
    <div class="tbtns">
      <button type="button" class="btn btn--primary btn--sm" data-act="ics">Add to calendar (.ics)</button>
      <button type="button" class="btn btn--ghost btn--sm" data-act="copy">Copy summary</button>
      <button type="button" class="btn btn--ghost btn--sm" data-act="print">Print</button>
    </div>
    <p class="muted" style="margin-top:1rem">Business days skip weekends and Texas state holidays. Your insurer's count may differ by a day. Deadlines restart when the insurer makes a new, reasonable request for information.</p>
  </div>
</div>
HTML,
    'body'        => <<<'HTML'
<h2>The deadlines this calculator uses</h2>
<p>Chapter 542, Subchapter B of the Texas Insurance Code (the "prompt payment of claims" rules) applies to most first-party property claims. Here is what each step means:</p>
<div class="table-wrap"><table>
<thead><tr><th>Step</th><th>Deadline</th><th>Section</th></tr></thead>
<tbody>
<tr><td>Acknowledge the claim, begin the investigation, request the items it needs</td><td>15 days after notice (surplus lines: 30 business days)</td><td>§542.055</td></tr>
<tr><td>Accept or reject in writing</td><td>15 business days after receiving all requested items (30 days if arson is suspected)</td><td>§542.056(a)–(b)</td></tr>
<tr><td>If it needs more time</td><td>It must say why within that period, then decide within 45 days of that notice</td><td>§542.056(d)</td></tr>
<tr><td>Pay</td><td>5 business days after notifying acceptance (surplus lines: 20 business days)</td><td>§542.057</td></tr>
<tr><td>Weather catastrophe or major disaster</td><td>Each deadline extended 15 days</td><td>§542.059(b)</td></tr>
</tbody></table></div>
<p>If an insurer that owes the claim misses these deadlines, it can owe interest as damages plus reasonable attorney's fees (§542.060). For weather-related claims covered by Chapter 542A, the interest rate is set differently, and you must give written notice at least 61 days before filing suit (§542A.003).</p>

<h2>TWIA claims follow different rules</h2>
<p>If your windstorm coverage is with the Texas Windstorm Insurance Association, the calculator switches to TWIA's statute (Insurance Code Chapter 2210): the claim must be filed within one year of the date of damage, TWIA may request more information within 30 days of the claim being filed, and it generally must accept or deny within 60 days of receiving the claim or the information it asked for (§2210.573).</p>

<h2>How to use these dates</h2>
<ul class="checklist">
  <li>Send every document in writing and keep proof of the date. The clock for the decision starts when the insurer has <em>everything</em> it asked for.</li>
  <li>If a deadline passes, ask the adjuster in writing for the status and cite the section. That alone often moves a stalled claim.</li>
  <li>Keep a claim diary: who you spoke to, when, and what was promised. See our guide on <a href="/post/how-long-does-an-insurance-adjuster-have-to-contact-you/">how long an adjuster has to contact you</a>.</li>
</ul>
[[cta]]
HTML,
    'faqs' => [
        ['q' => 'Do these deadlines apply to my policy?', 'a' => 'They apply to most property insurers doing business in Texas. Surplus lines insurers have longer periods, and TWIA follows Chapter 2210. Some government risk pools may not be covered. Check with an attorney if you are unsure.'],
        ['q' => 'What counts as receiving "all items"?', 'a' => 'The 15-business-day decision period starts once the insurer has every item, statement and form it reasonably requested to secure final proof of loss. A new, reasonable request can reset that date, so keep sending documents promptly and in writing.'],
        ['q' => 'What if my insurer misses a deadline?', 'a' => 'Put a written status request on record citing the section. If the claim is owed and payment is late, Chapter 542 allows interest as damages plus attorney\'s fees. Talk to a Texas attorney about remedies.'],
        ['q' => 'How long do I have to file a claim?', 'a' => 'That depends on your policy. TWIA requires filing within one year of the date of damage. Many private policies also set a reporting window for wind and hail. Read the "duties after loss" section of your policy. <a href="/post/how-long-do-you-have-to-file-a-hail-claim-in-texas/">More on filing deadlines</a>.'],
    ],
    'related' => ['/post/how-long-does-an-insurance-adjuster-have-to-contact-you/', '/services/denied-underpaid-claims/', '/post/how-long-do-you-have-to-file-a-hail-claim-in-texas/'],
];
