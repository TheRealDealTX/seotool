<?php
defined('CCPA_ROOT') || exit;
return [
    'template'    => 'contact',
    'title'       => 'Contact Corpus Christi Public Adjuster',
    'seo_title'   => 'Contact a Corpus Christi Public Adjuster | Call or Text',
    'description' => 'Contact Corpus Christi Public Adjuster about a hurricane, TWIA, hail, water, or fire claim. Call or text, email, or send a free claim review request.',
    'lead'        => 'Questions about property damage or a settlement that does not feel right? Reach out and a licensed Texas public adjuster will follow up.',
    'kicker'      => 'Contact',
    'image'       => '/assets/img/featured/page-contact.webp',
    'image_alt'   => 'Corpus Christi homeowner on the phone discussing an insurance claim',
    'faqs' => [
        ['q' => 'How quickly will you respond?', 'a' => '<p>We respond as quickly as we can. If your property needs emergency protection, such as tarping a roof or extracting water, take reasonable steps to prevent further damage right away and keep your receipts. If anyone is in danger, call 911.</p>'],
        ['q' => 'Does contacting you cost anything or obligate me?', 'a' => '<p>No. Reaching out and receiving a Free Claim Review are free and carry no obligation. A client relationship starts only if you sign a written public adjuster contract, which Texas law lets you rescind within 72 hours.</p>'],
        ['q' => 'Do you have an office I can visit?', 'a' => '<p>We serve Corpus Christi, Nueces County, and surrounding Coastal Bend communities and usually meet clients at the damaged property. Contact us by phone, text, email, or the form to set up a time.</p>'],
        ['q' => 'Should I call you or my insurance company first?', 'a' => '<p>Report the loss to your insurer promptly, as most policies require. TWIA claims generally must be filed within one year of the date of loss. You can contact us before or after reporting; we can explain what the insurer is likely to ask for.</p>'],
    ],
    'body' => <<<'HTML'
<p>If you are dealing with property damage, insurance questions, or a settlement that does not feel right, this is a good place to start. A short conversation can clarify your options and help you avoid mistakes before they affect your claim. Use the form to tell us about your situation, call or text [[phone]], or email [[email]]. Every form submission goes to that same inbox.</p>
<p>If you would rather reach Joseph Dittman, our licensed public adjuster, directly, email him at [[author-email]].</p>

<h2>What happens after you reach out</h2>
<ol>
<li>A licensed public adjuster reviews the details you send.</li>
<li>We contact you to talk through the damage, your policy, and where the claim stands.</li>
<li>We give you an honest view of whether a public adjuster can help, with no pressure.</li>
<li>If you decide to move forward, we provide a written contract with fees disclosed before any work begins.</li>
</ol>

<h2>What to have ready</h2>
<ul>
<li>Your claim number and insurance company, if a claim was filed (including TWIA or a flood insurer)</li>
<li>The approximate date of loss</li>
<li>Photos or video of the damage</li>
<li>Any insurer estimate, letter, or denial</li>
<li>Your policy declarations page, if available</li>
</ul>
<p>Do not worry if you do not have everything. We can help you work out what to request.</p>

<h2>Service area</h2>
<p>We serve Corpus Christi, Nueces County, and surrounding <a href="/service-areas/">Coastal Bend communities</a>. Prefer a structured request? Use the <a href="/free-claim-review/">Free Claim Review</a> page. Have a general question first? Our <a href="/faq/">public adjuster FAQ</a> may answer it.</p>
HTML,
];
