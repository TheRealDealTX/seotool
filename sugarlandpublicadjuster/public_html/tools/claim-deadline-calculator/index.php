<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/tool.php';
$faqs = [
    ['What is the Texas Prompt Payment of Claims Act?', '<p>Chapter 542, Subchapter B of the Texas Insurance Code sets deadlines for insurers handling first-party claims. In general, an insurer must acknowledge the claim, begin its investigation and request what it needs within 15 days of notice; accept or reject the claim within 15 business days after receiving everything it requested (it may extend this by up to 45 days if it notifies you why it needs more time); and pay within 5 business days after notifying you it will pay.</p>'],
    ['Can these deadlines be extended after a hurricane?', '<p>Yes. After a weather-related catastrophe or major natural disaster, Texas law allows the claim-handling deadlines to be extended by an additional 15 days. Tick the catastrophe box to see the effect.</p>'],
    ['What happens if the insurer misses a deadline?', '<p>Texas law can allow statutory interest and attorney’s fees when an insurer violates the prompt-payment rules, but whether that applies depends on the facts. Keep a dated log of every communication, and talk with an attorney about legal remedies.</p>'],
    ['How long do I have to report a storm claim?', '<p>Check your policy. Many Texas homeowners policies require weather-related claims to be reported within one year of the date of loss, and every policy requires prompt notice.</p>'],
];
tool_start('claim-deadline-calculator', 'Texas Claim Deadline Calculator',
    'Texas Insurance Claim Deadline Calculator (Prompt Payment Act) | Sugar Land Public Adjuster',
    'Calculate the Texas Prompt Payment Act deadlines on your insurance claim: acknowledgment, accept/reject and payment dates. Free tool from a Sugar Land public adjuster.',
    'Texas Insurance Claim Deadline Calculator',
    'Enter a few dates and see when your insurer’s Texas Prompt Payment deadlines fall—and which ones may already have passed.', $faqs);
?>
<form class="tool" id="deadline" onsubmit="return false">
  <h2>Your claim dates</h2>
  <div class="tool-grid">
    <label>Date of loss <span class="hint">When the damage happened</span><input type="date" name="loss"></label>
    <label>Date the insurer received notice <span class="hint">When you reported the claim</span><input type="date" name="notice"></label>
    <label>Date insurer received all requested items <span class="hint">Optional — last documents you sent</span><input type="date" name="items"></label>
    <label>Date insurer said it would pay <span class="hint">Optional — acceptance letter date</span><input type="date" name="accept"></label>
  </div>
  <p class="mt-2"><label class="consent" style="font-size:.95rem;color:var(--text)"><input type="checkbox" name="cat"> Weather catastrophe declared (adds 15 days)</label>
  <label class="consent" style="font-size:.95rem;color:var(--text)"><input type="checkbox" name="flood"> This is an NFIP flood claim</label></p>
  <div class="tool-results" aria-live="polite">
    <h3 class="mt-0">Your timeline</h3>
    <ol class="timeline-out" data-out="timeline"><li><strong>—</strong><span>Enter the date the insurer received notice to begin.</span></li></ol>
  </div>
  <div class="tool-actions"><button type="button" class="btn btn-primary" data-open-popup>Insurer missing deadlines? Get a free review</button><button type="button" class="btn btn-outline" onclick="window.print()">Print timeline</button></div>
</form>
<section class="prose mt-2">
  <h2>How the deadlines are counted</h2>
  <p>“Days” are calendar days; “business days” skip weekends and holidays. This calculator skips weekends and major federal holidays, so treat the dates as close approximations. Surplus lines insurers and some policy types have different rules, and flood claims under the National Flood Insurance Program follow federal deadlines instead.</p>
  <p>If your insurer is stalling, keep every letter and email, write down every call, and respond to document requests promptly—the clock on the accept/reject decision generally starts when the insurer has everything it reasonably asked for. A <a href="/services/denied-underpaid-claims/">Sugar Land public adjuster</a> can take over that communication for you.</p>
</section>
<?php tool_end($faqs); ?>
