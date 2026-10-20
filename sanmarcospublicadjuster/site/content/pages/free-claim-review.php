<?php
return [
    'template'    => 'contact',
    'title'       => 'Request a Free Claim Review',
    'seo_title'   => 'Free Claim Review | San Marcos Public Adjuster',
    'description' => 'Request a free claim review from a San Marcos public adjuster. We look at your damage, policy, and insurer estimate and explain your options. No obligation.',
    'lead'        => 'Share what happened to your property and where your claim stands. A licensed Texas public adjuster will review it and give you an honest read on your options.',
    'kicker'      => 'Free Claim Review',
    'image'       => '/assets/img/featured/page-free-claim-review.webp',
    'image_alt'   => 'Public adjuster reviewing an insurance estimate and policy documents',
    'faqs' => [
        ['q' => 'Is the review actually free?', 'a' => '<p>Yes. There is no charge for the Free Claim Review. If you later decide to hire us, fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement.</p>'],
        ['q' => 'Am I committing to anything by submitting the form?', 'a' => '<p>No. Many people only want a second opinion on an estimate or a denial letter. A client relationship starts only if you sign a written contract, and Texas law lets you rescind it within 72 hours.</p>'],
        ['q' => 'My claim was already paid or closed. Should I still send it?', 'a' => '<p>Yes. Depending on the policy and the timing, a claim may be supplemented or reopened when damage was missed or the estimate was incomplete. We will tell you honestly if that does not look possible.</p>'],
        ['q' => 'What files can I upload?', 'a' => '<p>You can attach up to three photos (JPG, PNG, WEBP, or HEIC) or PDF files, such as damage photos, the declarations page, or the insurer\'s estimate. They are emailed to <a href="mailto:info@sanmarcospublicadjuster.com">info@sanmarcospublicadjuster.com</a> with your request and are not stored on the web server. If you have more, we can collect them after we talk.</p>'],
        ['q' => 'I have not filed a claim yet. Can you still review it?', 'a' => '<p>Yes. We can talk through the damage and what your policy may cover before you file. Most policies require prompt notice of a loss, though, so report the damage to your insurer without long delays.</p>'],
    ],
    'body' => <<<'HTML'
<p>Wondering whether your insurance claim is being handled fairly? A Free Claim Review is the simplest way to find out. A licensed Texas public adjuster looks at what happened to your San Marcos-area property, what your policy says, and how the insurer has responded, then explains your options in plain English.</p>

<h2>What we look at</h2>
<ul>
<li>The type of damage, when it occurred, and the current status of the claim</li>
<li>Your coverages, deductibles (including any separate wind/hail deductible), endorsements, and exclusions</li>
<li>The insurer's estimate, letters, or denial, if you have received them</li>
<li>Possible next steps, such as additional documentation, a supplement, or appraisal</li>
<li>Whether a public adjuster is likely to help, including when the honest answer is no</li>
</ul>

<h2>Gather these if you can</h2>
<ul>
<li>Insurance company and claim number</li>
<li>Date of loss</li>
<li>Photos or video of the damage</li>
<li>The insurer's estimate and any letters</li>
<li>Your declarations page</li>
</ul>
<p>Do not hold off because something is missing. Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> can help you organize the rest, and the <a href="/storm-lookup/">storm lookup tool</a> shows reported hail and wind events near San Marcos and Hays County.</p>

<h2>What happens next</h2>
<p>Your request is emailed to our team. We review it and reach out by phone or email as soon as we can. If it looks like we can help, we explain how representation works and share a written contract with fees disclosed before any work begins. If your claim appears to be on track, we will tell you that too.</p>
<p>Prefer to talk first? Call [[phone]] or email [[email]]. To reach Joseph Dittman, licensed public adjuster, directly, email [[joseph-email]]. You can also learn more <a href="/about-us/">about San Marcos Public Adjuster</a> or see the <a href="/services/">claims we handle</a>.</p>
HTML,
];
