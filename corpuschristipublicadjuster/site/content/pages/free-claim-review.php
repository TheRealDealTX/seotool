<?php
return [
    'template'    => 'contact',
    'title'       => 'Request a Free Claim Review',
    'seo_title'   => 'Free Claim Review | Corpus Christi Public Adjuster',
    'description' => 'Request a free claim review from Corpus Christi Public Adjuster. We look at your policy, damage, and insurer estimate and explain your options. No obligation.',
    'lead'        => 'Tell us about your property damage and claim. A licensed Texas public adjuster will review it and give you an honest answer about your options.',
    'kicker'      => 'Free Claim Review',
    'image'       => '/assets/img/featured/page-free-claim-review.webp',
    'image_alt'   => 'Public adjuster reviewing an insurance estimate and policy documents',
    'faqs' => [
        ['q' => 'Is the claim review really free?', 'a' => '<p>Yes. The Free Claim Review has no cost. If you later choose to hire us, fees are disclosed in a written contract before any work begins; Texas law caps public adjuster compensation at 10% of the insurance settlement.</p>'],
        ['q' => 'Do I have to hire you after the review?', 'a' => '<p>No. There is no obligation. Many people simply want a second opinion on their insurer\'s estimate or decision, and that is fine.</p>'],
        ['q' => 'Can you review a TWIA or flood claim?', 'a' => '<p>Yes. Send what you have from each insurer involved, whether that is TWIA, your homeowners or commercial carrier, or a flood insurer. After a hurricane, the split between wind and water damage often matters as much as the totals, and TWIA has its own deadlines for filing, appraisal, and disputes.</p>'],
        ['q' => 'What if my claim is already closed or paid?', 'a' => '<p>Send it anyway. Depending on your policy and timing, a claim may be supplemented or reopened when damage was missed or the estimate was incomplete. We will tell you honestly whether that looks possible.</p>'],
        ['q' => 'Can I upload photos and documents?', 'a' => '<p>Yes. The form accepts photos and PDF files, such as damage photos, your declarations page, or the insurer\'s estimate and letters. They are attached to the email sent to info@corpuschristipublicadjuster.com and are not kept on the web server.</p>'],
    ],
    'body' => <<<'HTML'
<p>Not sure whether your insurance claim is being handled fairly? A Free Claim Review is a simple way to find out. A licensed Texas public adjuster looks at what happened to your property, what your policy says, and how your insurer has responded so far, then explains your options in plain English. It is open to property owners in Corpus Christi, Nueces County, and the surrounding Coastal Bend.</p>

<h2>What the Free Claim Review includes</h2>
<ul>
<li>A review of your situation: the type of damage, when it happened, and where the claim stands</li>
<li>A look at your policy, including wind/hail or named-storm deductibles, coverages, and exclusions that may matter</li>
<li>A review of the insurer's estimate, letters, or denial, if you have them</li>
<li>A check of the deadlines that may apply, such as TWIA's one-year filing period and 60-day appraisal window</li>
<li>An explanation of possible next steps, such as a supplement, appraisal, or more documentation</li>
<li>An honest answer about whether a public adjuster is likely to help, even if the answer is no</li>
</ul>
<p>There is no cost and no obligation. Submitting the form does not create a client relationship; that happens only if you sign a written public adjuster contract, which Texas law lets you rescind within 72 hours.</p>

<h2>What to have ready</h2>
<ul>
<li>Claim number and insurance company, if a claim was filed</li>
<li>Date of loss, even if approximate</li>
<li>Photos or video of the damage</li>
<li>The insurer's estimate, letters, or denial</li>
<li>Your declarations page, if you have it</li>
</ul>
<p>Missing something? Submit what you have. Our <a href="/claim-documentation-checklist/">claim documentation checklist</a> can help you organize the rest, and the <a href="/claim-deadline-calculator/">claim deadline calculator</a> maps out the Texas timelines from your own dates.</p>

<h2>What happens next</h2>
<p>Your request is emailed to [[email]] and reviewed by a licensed public adjuster. We contact you by phone or email as quickly as we can. If it looks like we can help, we will explain how representation works and share a written contract with fees disclosed before any work begins. If your claim looks like it is being handled fairly, we will tell you that too. Prefer to talk first? Call or text [[phone]].</p>
HTML,
];
