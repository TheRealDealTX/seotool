<?php
return [
    'title'       => 'Privacy Policy',
    'seo_title'   => 'Privacy Policy | San Marcos Public Adjuster',
    'description' => 'How San Marcos Public Adjuster collects, uses, and protects information from our website forms, file uploads, analytics, claim tools, and weather features.',
    'lead'        => 'What this website collects, why, and the choices you have. Effective October 20, 2026.',
    'kicker'      => 'Legal',
    'image'       => '/assets/img/featured/page-privacy-policy.webp',
    'image_alt'   => 'Padlock over a document representing website privacy',
    'faqs' => [
        ['q' => 'Do you sell my personal information?', 'a' => '<p>No. We do not sell, rent, or trade personal information, and we do not give it to third parties for their own marketing.</p>'],
        ['q' => 'Where do form submissions go?', 'a' => '<p>Every form on this website sends your submission by email to <a href="mailto:info@sanmarcospublicadjuster.com">info@sanmarcospublicadjuster.com</a>. Submissions are not saved in a website database.</p>'],
        ['q' => 'Are uploaded photos and documents stored on the website?', 'a' => '<p>No. Files you attach to a Free Claim Review request are sent as email attachments and are not kept on the web server after the request is processed.</p>'],
        ['q' => 'Does this site use cookies?', 'a' => '<p>Google Analytics sets cookies to measure how the site is used. The site also stores small values in your browser\'s local storage, for example to remember that you closed the Free Claim Review pop-up. We do not use advertising cookies.</p>'],
    ],
    'body' => <<<'HTML'
<p><strong>Effective date: October 20, 2026</strong> (this version replaces the policy dated February 6, 2026)</p>
<p>San Marcos Public Adjuster is a public adjusting service of [[company]] ("we," "our," or "us"). This Privacy Policy explains what information we collect when you visit sanmarcospublicadjuster.com, use its tools, or contact us by form, phone, or email, and how we use and protect it. We have written it to match what this website actually does. By using the site, you agree to the practices described here.</p>

<h2>Information you choose to give us</h2>
<p>When you submit the Free Claim Review form (on its own page, on the Contact page, or in the pop-up), call, or email us, you may provide:</p>
<ul>
<li>Your name, phone number, and email address</li>
<li>The property location (city, ZIP code, or address)</li>
<li>Your insurance company, claim status, type of damage, and date of loss</li>
<li>A message describing your situation</li>
<li>Photos or PDF documents you choose to upload</li>
</ul>
<p>You do not need to give us any personal information to read the website. We need contact details only to respond to a request.</p>

<h2>How form submissions and uploads are handled</h2>
<ul>
<li><strong>Delivered by email.</strong> Each submission is sent by email to [[email]]. It is not stored in a website database.</li>
<li><strong>Uploads.</strong> The form accepts up to three files (JPG, PNG, WEBP, HEIC, or PDF), up to 8 MB each and 20 MB in total. Files are checked for type and size, attached to the email, and not kept on the web server.</li>
<li><strong>Consent.</strong> The form asks you to agree that we may contact you about your request by phone, text, or email.</li>
<li><strong>No client relationship.</strong> Sending a form does not make you a client. That happens only if you sign a written public adjuster contract.</li>
</ul>

<h2>How we use your information</h2>
<ul>
<li>To respond to your questions and Free Claim Review requests</li>
<li>To evaluate and, if you hire us, work on your property insurance claim</li>
<li>To keep business records and meet legal and regulatory obligations, including those that apply to Texas public adjusters</li>
<li>To understand how the website is used and improve it</li>
</ul>

<h2>Calls, texts, and emails</h2>
<p>If you send us a request, we may contact you by phone, text, or email about that request or your claim. We do not send marketing newsletters. If you would like us to stop contacting you, tell us by replying, calling [[phone]], or emailing [[email]].</p>

<h2>Spam protection and rate limiting</h2>
<p>To block automated abuse, our forms use a hidden "honeypot" field and a signed form token. We also limit how many submissions can come from one connection in an hour. To do that, the server keeps a short-lived record of submission times tied to a one-way hashed version of your IP address, not the IP address itself.</p>

<h2>Server and security logs</h2>
<p>Like most websites, our hosting provider may record standard technical data such as IP address, browser type, pages requested, and the date and time of each request. These logs are used for security, troubleshooting, and keeping the site running. Our own application logs record operational events, such as whether an email was delivered and how many files were attached, not the content of your message.</p>

<h2>Google Analytics and cookies</h2>
<p>This website uses Google Analytics, a web analytics service provided by Google, to understand how visitors find and use the site: for example, which pages are viewed, roughly where visitors are located, what device and browser they use, and whether a form was submitted or the pop-up was shown. Google Analytics uses cookies and similar technologies, and the data it collects is processed by Google under its own privacy policy. We do not send your name, email, phone number, or message contents to Google Analytics.</p>
<p>You can block or delete cookies in your browser settings, or install Google's opt-out browser add-on, available at tools.google.com/dlpage/gaoptout. The website will still work. We do not use advertising or remarketing cookies.</p>

<h2>Local storage in your browser</h2>
<p>Some features save small pieces of information in your own browser using local storage or session storage. This information stays on your device and is not sent to us:</p>
<ul>
<li><strong>Pop-up reminder.</strong> The Free Claim Review pop-up stores a date so it does not reappear for a while after you close it (about 7 days) or submit it (about 90 days), and a session flag so it shows at most once per visit.</li>
<li><strong>Claim Documentation Checklist.</strong> The <a href="/claim-documentation-checklist/">checklist</a> saves your progress in your browser only if you choose to turn saving on. You can clear it in the tool or through your browser settings.</li>
<li><strong>Claim Calculator.</strong> The <a href="/claim-calculator/">claim calculator</a> runs in your browser. The numbers you enter are not sent to our server.</li>
</ul>

<h2>Weather, storm data, and maps</h2>
<p>Our <a href="/weather/">weather</a>, <a href="/weather-events/">weather events</a>, <a href="/storm-history/">storm history</a>, and <a href="/storm-lookup/">storm lookup</a> pages display public data from the National Weather Service (NWS) and NOAA's National Centers for Environmental Information (NCEI). Our server requests that data from government sources; your browser does not send any personal information to the NWS or NOAA when you view these pages. The storm lookup map loads map tiles from OpenStreetMap, which means your browser connects to OpenStreetMap's servers and they receive your IP address, as with any website. These pages do not ask for your device location.</p>

<h2>When we share information</h2>
<p>We share personal information only when it is needed to help you or required by law:</p>
<ul>
<li>With service providers that run the website and email (for example, hosting and email delivery), who may handle data only to provide their services</li>
<li>With your insurance company, contractors you designate, or others involved in your claim, as part of representing you under a signed contract and with your authorization</li>
<li>When required by law, regulation, subpoena, or a request from a regulator such as the Texas Department of Insurance</li>
<li>To protect the rights, property, or safety of you, us, or others</li>
</ul>

<h2>How long we keep information</h2>
<p>We keep inquiry emails and claim records as long as needed to respond, to represent you if you hire us, and to meet record-keeping requirements that apply to Texas public adjusters. Rate-limit records expire automatically after a short time. Server logs are rotated regularly.</p>

<h2>Security</h2>
<p>The website uses HTTPS encryption, and we take reasonable administrative and technical steps to protect the information you send. No website or email system is completely secure, so please do not send Social Security numbers, bank account numbers, or similar sensitive financial data through the form.</p>

<h2>Your choices and rights</h2>
<p>You may ask us to tell you what personal information we hold about you, correct it, or delete it, subject to legal and regulatory record-keeping obligations. Email [[email]] or call [[phone]], and we will respond within a reasonable time.</p>

<h2>Children's privacy</h2>
<p>This website is intended for adults and is not directed to children under 13. We do not knowingly collect personal information from children. If you believe a child has sent us information, contact us and we will delete it.</p>

<h2>Links to other websites</h2>
<p>Our articles link to outside sources such as the Texas Department of Insurance, FEMA, the National Weather Service, and NOAA. We are not responsible for their privacy practices, so please review their policies when you visit them.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy when the website or our practices change. The effective date at the top of the page shows when it was last revised. Significant changes will be reflected here before they take effect.</p>

<h2>Contact us</h2>
<p>Questions about this Privacy Policy or your information:</p>
<p><strong>San Marcos Public Adjuster</strong><br>A public adjusting service of [[company]], TDI license #[[license]]<br>Email: [[email]]<br>Phone: [[phone]]</p>
<p>See also our <a href="/terms-of-use/">Terms of Use</a>.</p>
HTML,
];
