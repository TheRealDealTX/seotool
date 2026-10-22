<?php
return [
    'template'    => 'deadline-calculator',
    'title'       => 'Texas Claim Deadline Calculator',
    'seo_title'   => 'Texas Claim Deadline Calculator | TWIA & Prompt Payment Dates',
    'description' => 'Texas claim deadline calculator for Corpus Christi property owners: map Prompt Payment Act and TWIA deadlines for filing, decisions, and appraisal.',
    'lead'        => 'Enter your date of loss and claim dates to map the deadlines Texas law sets for your insurer, or for TWIA, on a property insurance claim.',
    'kicker'      => 'Interactive Tool',
    'image'       => '/assets/img/featured/page-claim-deadline-calculator.webp',
    'image_alt'   => 'Calendar with insurance claim deadlines marked next to a policy',
    'faqs' => [
        ['q' => 'How long does my insurance company have to respond to a claim in Texas?', 'a' => '<p>Under the Prompt Payment of Claims Act, most insurers must acknowledge the claim, begin the investigation, and request what they need within 15 days of notice. They must accept or reject in writing within 15 business days after receiving all requested items, or notify you that they need more time and then decide within 45 days. Payment on an accepted claim is due within 5 business days. Surplus lines insurers have longer periods for some steps.</p>'],
        ['q' => 'What changes after a declared weather catastrophe?', 'a' => '<p>When the Texas insurance commissioner declares a weather-related catastrophe or major natural disaster, the Prompt Payment Act deadlines are extended by 15 days (Texas Insurance Code §542.059). Check the box in the calculator to add that time.</p>'],
        ['q' => 'How long do I have to file a TWIA claim?', 'a' => '<p>No later than one year after the date the damage occurred. The commissioner may extend that by up to 180 days if you show good cause. File as soon as you can; evidence is easier to gather soon after a storm.</p>'],
        ['q' => 'How long do I have to demand appraisal on a TWIA claim?', 'a' => '<p>Within 60 days after receiving TWIA\'s notice accepting or partly accepting the claim. TWIA may grant 30 more days if you ask in writing, with good cause, within 15 days after the 60-day period ends. You and TWIA split appraisal costs equally.</p>'],
        ['q' => 'Does the 61-day pre-suit notice apply to TWIA?', 'a' => '<p>No. Chapter 542A, which generally requires written notice at least 61 days before suing an insurer, does not apply to actions against TWIA. TWIA disputes over denied coverage follow their own process in Chapter 2210, including a notice of intent to sue and possible alternative dispute resolution. Talk to a Texas attorney about any lawsuit deadline.</p>'],
        ['q' => 'Is this calculator legal advice?', 'a' => '<p>No. It applies general statutory deadlines to the dates you enter. Deadlines have exceptions, business-day counts can shift with holidays, and your policy may set its own deadlines, such as for recoverable depreciation. Deadlines to sue are legal questions for a Texas attorney.</p>'],
    ],
    'body' => <<<'HTML'
<h2>Why claim deadlines matter</h2>
<p>Texas law sets deadlines for insurers to respond to and pay property claims, and it sets deadlines for policyholders too. Coastal Bend owners often deal with two systems at once: the <strong>Prompt Payment of Claims Act</strong> (Texas Insurance Code Chapter 542) for private homeowners and commercial insurers, and the separate <strong>TWIA claim rules</strong> in Chapter 2210 for windstorm claims. This Texas claim deadline calculator turns those rules into dates so you can see whether your claim is on schedule and which of your own deadlines are coming up.</p>

<h2>Private insurers: Prompt Payment of Claims Act</h2>
<table>
<thead><tr><th>Step</th><th>Deadline</th><th>Statute</th></tr></thead>
<tbody>
<tr><td>Acknowledge the claim, begin investigating, request needed items</td><td>15 days after notice of the claim (30 business days for eligible surplus lines insurers)</td><td>§542.055</td></tr>
<tr><td>Accept or reject the claim in writing</td><td>15 business days after receiving all requested items (30 days if arson is suspected)</td><td>§542.056</td></tr>
<tr><td>If the insurer says it needs more time</td><td>It must explain why within that period, then decide within 45 days of its notice</td><td>§542.056</td></tr>
<tr><td>Pay an accepted claim</td><td>5 business days after notice of acceptance (20 business days for surplus lines)</td><td>§542.057</td></tr>
<tr><td>Declared weather catastrophe</td><td>The deadlines above are extended by 15 days</td><td>§542.059(b)</td></tr>
</tbody>
</table>
<p>If payment is delayed beyond the statutory period, or more than 60 days when no other statute sets a period, the statute provides for delay damages (§542.058). Separately, before suing a private insurer on a property claim, Chapter 542A generally requires written notice at least 61 days before filing. Statute text is on the <a href="https://tcss.legis.texas.gov/resources/IN/htm/IN.542.htm" target="_blank" rel="noopener">Texas Legislature statutes site</a>.</p>

<h2>TWIA windstorm claims: Chapter 2210</h2>
<table>
<thead><tr><th>Step</th><th>Deadline</th><th>Statute</th></tr></thead>
<tbody>
<tr><td>File the claim</td><td>No later than one year after the damage occurs; the commissioner may extend up to 180 days for good cause</td><td>§2210.573(a), §2210.205</td></tr>
<tr><td>TWIA requests missing information</td><td>Within 30 days after the claim is filed</td><td>§2210.573(b)</td></tr>
<tr><td>TWIA accepts, partly accepts, or denies in writing</td><td>60 days after receiving the claim or requested information, whichever is later; the commissioner may extend it</td><td>§2210.573(d), §2210.581</td></tr>
<tr><td>TWIA pays the accepted amount</td><td>10 days after the acceptance notice (or after an act required of the claimant)</td><td>§2210.5731</td></tr>
<tr><td>Demand appraisal of the amount of loss</td><td>60 days after receiving an acceptance or partial-acceptance notice; 30 more days possible on a written good-cause request made within 15 days after that period</td><td>§2210.574</td></tr>
<tr><td>Dispute a denial of coverage</td><td>Notice of intent to sue before limitations runs; TWIA may request mediation or a moderated settlement conference within 60 days, to be completed within 60 days of the request</td><td>§2210.575</td></tr>
<tr><td>Outside deadline to sue</td><td>Two years after receiving a partial or full denial (statute of repose)</td><td>§2210.577</td></tr>
</tbody>
</table>
<p>Chapter 542A's pre-suit notice does not apply to TWIA, and the Chapter 2210 rules control where they conflict with other law. TDI also runs an ombudsman program to help TWIA policyholders. Statute text: <a href="https://tcss.legis.texas.gov/resources/IN/htm/IN.2210.htm" target="_blank" rel="noopener">Texas Insurance Code Chapter 2210</a>. For the full process, read the <a href="/twia-claim-process-corpus-christi/">TWIA claim process in Corpus Christi</a>.</p>

<h2>Tips for using the calculator</h2>
<ul>
<li><strong>Use written dates.</strong> Keep the date you reported the claim, the date the insurer confirmed it had everything it asked for, and the date on any decision letter.</li>
<li><strong>Keep proof of delivery.</strong> Email confirmations and certified mail receipts show when items were sent and received.</li>
<li><strong>Check your policy too.</strong> Policies set their own deadlines, such as the time to complete repairs and claim recoverable depreciation, or to submit a proof of loss.</li>
<li><strong>Do not wait on legal deadlines.</strong> If a deadline to sue may be approaching, talk to a Texas attorney promptly.</li>
</ul>
<p>If your insurer is missing its deadlines, see our <a href="/services/delayed-insurance-claims/">delayed insurance claims</a> page or read <a href="/why-property-insurance-claims-are-delayed-texas/">why property insurance claims are delayed in Texas</a>. A Corpus Christi Public Adjuster can review where your claim stands.</p>
HTML,
];
