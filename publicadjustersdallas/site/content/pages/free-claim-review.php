<?php
return [
    'template'    => 'contact',
    'title'       => 'Request a Free Claim Review',
    'seo_title'   => 'Free Claim Review | Dallas Public Adjuster',
    'description' => 'Request a free claim review from a Dallas Public Adjuster. We look at your damage, policy, and insurer estimate and explain your options. No obligation.',
    'lead'        => 'Tell us about your property damage and your claim. A licensed Texas public adjuster will review it and give you a straight answer about your options.',
    'kicker'      => 'Free Claim Review',
    'image'       => '/assets/img/featured/page-free-claim-review.webp',
    'image_alt'   => 'Public adjuster reviewing an insurance estimate and policy documents for a Dallas claim',
    'faqs' => [
        ['q' => 'Is the claim review really free?', 'a' => '<p>Yes. The Free Claim Review has no cost. If you later decide to hire us, fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement.</p>'],
        ['q' => 'Do I have to hire you after the review?', 'a' => '<p>No. There is no obligation. Plenty of people just want a second opinion on the insurer\'s estimate or decision, and that is fine with us.</p>'],
        ['q' => 'What if my claim is already closed or paid?', 'a' => '<p>Send it anyway. Depending on your policy and the timing, a claim may be supplemented or reopened when damage was missed or the estimate was incomplete. We will tell you honestly whether that looks possible.</p>'],
        ['q' => 'Can I upload photos and documents?', 'a' => '<p>Yes. The form accepts photos and PDF files, such as damage photos, your declarations page, or the insurer\'s estimate and letters. They are emailed to info@publicadjustersdallas.com and are not stored on the web server.</p>'],
        ['q' => 'I have not filed a claim yet. Can I still request a review?', 'a' => '<p>Yes. We can talk through the damage and what your policy may cover before you file. Most policies require prompt notice to the insurer, though, so do not wait long to report the loss.</p>'],
    ],
    'body' => <<<'HTML'
<p>Wondering whether your insurance claim is being handled fairly? A Free Claim Review is a simple way to find out. A licensed Texas public adjuster looks at what happened to your Dallas-area property, what your policy says, and how the insurer has responded so far, then explains your options in plain English.</p>

<h2>What the Free Claim Review covers</h2>
<ul>
<li>Your situation: the type of damage, when it happened, and where the claim stands</li>
<li>Your policy: deductibles (including any separate wind/hail deductible), coverages, and exclusions that may matter</li>
<li>The insurer's estimate, letters, or denial, if you have them</li>
<li>Possible next steps, such as a supplement, additional documentation, or appraisal</li>
<li>An honest answer about whether a public adjuster is likely to help, even if that answer is no</li>
</ul>
<p>There is no cost and no obligation. Sending the form does not make you a client; that only happens if you sign a written public adjuster contract, which Texas law lets you rescind within 72 hours.</p>

<h2>What to have ready</h2>
<ul>
<li>Insurance company and claim number, if a claim was filed</li>
<li>Date of loss, even if approximate</li>
<li>Photos or video of the damage</li>
<li>The insurer's estimate, letters, or denial</li>
<li>Your declarations page, if you have it</li>
</ul>
<p>Do not have all of it? Send what you have. The <a href="/claim-documentation-checklist/">claim documentation checklist</a> can help you gather the rest, and the <a href="/storm-lookup/">storm lookup tool</a> shows reported hail and wind events near your address in Dallas County.</p>

<h2>What happens next</h2>
<p>Your request is emailed to us at info@publicadjustersdallas.com. We review it and contact you by phone or email as soon as we can. If it looks like we can help, we will explain how representation works and share a written contract with fees disclosed before any work begins. If your claim looks like it is being handled fairly, we will tell you that too.</p>
<p>Prefer to talk first? Call or text [[phone]], email [[email]], or write to Joseph Dittman directly at [[joseph-email]].</p>
HTML,
];
