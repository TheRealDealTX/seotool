<?php
return [
    'template'    => 'contact',
    'title'       => 'Contact San Antonio Public Adjuster',
    'seo_title'   => 'Contact a San Antonio Public Adjuster | Claim Help',
    'description' => 'Contact San Antonio Public Adjuster for insurance claim help in San Antonio and Bexar County. Call, email, or send a free claim review request.',
    'lead'        => 'Questions about property damage or a settlement that does not feel right? Reach out and a licensed Texas public adjuster will follow up.',
    'kicker'      => 'Contact',
    'image'       => '/assets/img/featured/page-contact.webp',
    'image_alt'   => 'San Antonio homeowner on the phone discussing an insurance claim',
    'faqs' => [
        ['q' => 'How quickly will you respond?', 'a' => '<p>We respond as quickly as possible. If your property needs emergency protection, such as tarping or water extraction, take reasonable steps to prevent further damage right away and keep your receipts.</p>'],
        ['q' => 'Does contacting you cost anything or obligate me?', 'a' => '<p>No. Reaching out and receiving a Free Claim Review are free and carry no obligation. A client relationship starts only if you sign a written public adjuster contract.</p>'],
        ['q' => 'Do you have an office I can visit?', 'a' => '<p>We serve San Antonio, Bexar County, and surrounding communities and typically meet clients at the damaged property. Contact us by phone, email, or the form to set up a time.</p>'],
        ['q' => 'Where does the contact form go?', 'a' => '<p>Every form submission on this website is emailed to info@publicadjustersanantonio.com and reviewed by our team. If you would rather write to Joseph Dittman personally, email jditt@risepublicadjusting.com.</p>'],
        ['q' => 'Should I call you or my insurance company first?', 'a' => '<p>Report the loss to your insurer promptly, as most policies require. You can contact us before or after reporting; we can help you understand what the insurer may ask for.</p>'],
    ],
    'body' => <<<'HTML'
<p>If you are dealing with property damage, insurance questions, or a settlement that does not feel right, this is a good place to start. A short conversation can clarify your options and help you avoid mistakes before they affect your claim. Use the form to tell us about your situation, and a San Antonio public adjuster will review it and follow up. No pressure, no obligation.</p>

<h2>Ways to reach us</h2>
<ul>
<li><strong>Phone:</strong> [[phone]]</li>
<li><strong>Email:</strong> [[email]]</li>
<li><strong>Form:</strong> the Free Claim Review form on this page. All form submissions go to info@publicadjustersanantonio.com.</li>
</ul>

<h2>Contact Joseph Dittman directly</h2>
<p>Prefer to write to the adjuster who handles claims? Email <a href="/author/joseph-dittman/">Joseph Dittman</a>, licensed Texas public adjuster, at [[joseph-email]]. Include your name, phone number, property city or ZIP code, and a short description of the damage and where the claim stands.</p>

<h2>What happens after you reach out</h2>
<ol>
<li>A licensed public adjuster reviews the details you send.</li>
<li>We contact you to talk through the damage, your policy, and where the claim stands.</li>
<li>We give you an honest view of whether a public adjuster can help, with no pressure and no obligation.</li>
<li>If you decide to move forward, we provide a written contract with fees disclosed before any work begins.</li>
</ol>

<h2>What to have ready</h2>
<ul>
<li>Your claim number and insurance company name, if a claim was filed</li>
<li>The approximate date of loss</li>
<li>Photos or video of the damage</li>
<li>Any insurer estimate, letter, or denial you have received</li>
<li>Your policy declarations page, if available</li>
</ul>
<p>Do not worry if you do not have everything. We can help you figure out what to request, and our <a href="/claim-documentation-checklist/">claim documentation checklist</a> can help you get organized.</p>

<h2>Service area</h2>
<p>We serve San Antonio, Bexar County, and <a href="/service-areas/">surrounding communities</a>. Prefer a structured request? Use our <a href="/free-claim-review/">Free Claim Review</a> page. Have a general question first? Our <a href="/faq/">San Antonio public adjuster FAQs</a> may already answer it.</p>
HTML,
];
