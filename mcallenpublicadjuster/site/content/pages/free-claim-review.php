<?php
return [
    'template'    => 'contact',
    'title'       => 'Request a Free Claim Review',
    'seo_title'   => 'Free Claim Review | McAllen Public Adjuster',
    'description' => 'Request a free claim review from a McAllen public adjuster. We look at your policy, damage, and insurer estimate and explain options. No obligation.',
    'lead'        => 'Tell us about your property damage and claim. A licensed Texas public adjuster will review it and give you an honest answer about your options.',
    'kicker'      => 'Free Claim Review',
    'image'       => '/assets/img/featured/page-free-claim-review.webp',
    'image_alt'   => 'Public adjuster reviewing an insurance estimate and policy documents',
    'faqs' => [
        ['q' => 'Is the claim review really free?', 'a' => '<p>Yes. The Free Claim Review has no cost. If you later choose to hire us, fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement.</p>'],
        ['q' => 'Do I have to hire you after the review?', 'a' => '<p>No. There is no obligation. Many people simply want a second opinion on their insurer\'s estimate or decision, and that is fine.</p>'],
        ['q' => 'What if my claim is already closed or paid?', 'a' => '<p>Send it anyway. Depending on your policy and timing, a claim may be supplemented or reopened when damage was missed or the estimate was incomplete. We will tell you honestly whether that looks possible.</p>'],
        ['q' => 'Can I upload photos and documents?', 'a' => '<p>Yes. The form accepts photos and PDF files, such as damage photos, your declarations page, or the insurer\'s estimate and letters. They are emailed to our team and are not stored on the web server.</p>'],
    ],
    'body' => <<<'HTML'
<p>Not sure whether your insurance claim is being handled fairly? A Free Claim Review is a simple way to find out. A licensed Texas public adjuster looks at what happened to your property, what your policy says, and how your insurer has responded so far, then explains your options in plain English.</p>

<h2>What the Free Claim Review includes</h2>
<ul>
<li>A review of your situation: the type of damage, when it happened, and where the claim stands</li>
<li>A look at your policy, including deductibles, coverages, and exclusions that may matter</li>
<li>A review of the insurer's estimate, letters, or denial, if you have them</li>
<li>An explanation of possible next steps, such as a supplement, appraisal, or additional documentation</li>
<li>An honest answer about whether a public adjuster is likely to help, even if the answer is no</li>
</ul>
<p>There is no cost and no obligation. Submitting the form does not create a client relationship; that only happens if you sign a written public adjuster contract, which Texas law lets you rescind within 72 hours.</p>

<h2>What to have ready</h2>
<ul>
<li>Claim number and insurance company, if a claim was filed</li>
<li>Date of loss, even if approximate</li>
<li>Photos or video of the damage</li>
<li>The insurer's estimate, letters, or denial</li>
<li>Your declarations page, if you have it</li>
</ul>
<p>Missing something? Submit what you have. Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> can help you organize the rest.</p>

<h2>What happens next</h2>
<p>We review your information and contact you by phone or email as quickly as possible. If it looks like we can help, we will walk you through how representation works and share a written contract with fees disclosed before any work begins. If it looks like your claim is being handled fairly, we will tell you that too. Prefer to talk first? Call [[phone]] or email [[email]].</p>
HTML,
];
