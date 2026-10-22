<?php
defined('CCPA_ROOT') || exit;
return [
    'title'       => 'Privacy Policy',
    'seo_title'   => 'Privacy Policy | Corpus Christi Public Adjuster Website',
    'title_short' => 'Privacy Policy | Corpus Christi PA',   // shown before the phone number in <title>
    'description' => 'How Corpus Christi Public Adjuster collects, uses, and protects information sent through our website, claim review form, uploads, tools, and weather pages.',
    'lead'        => 'What information this website collects, how we use it, and the choices you have. Last updated October 22, 2026.',
    'kicker'      => 'Legal',
    'image'       => '/assets/img/featured/page-privacy-policy.webp',
    'image_alt'   => 'Padlock over a document representing website privacy',
    'faqs' => [
        ['q' => 'Where do my form submissions go?', 'a' => '<p>Every Free Claim Review and contact form submission is emailed to info@corpuschristipublicadjuster.com. Submissions are not stored in a website database.</p>'],
        ['q' => 'Are my uploaded photos stored on the website?', 'a' => '<p>No. Files you upload with a request are attached to the email sent to info@corpuschristipublicadjuster.com and are not kept on the web server after the message is sent.</p>'],
        ['q' => 'Do you sell my personal information?', 'a' => '<p>No. We do not sell or rent personal information, and we do not share it with third parties for their own marketing.</p>'],
        ['q' => 'Does this website use tracking cookies?', 'a' => '<p>The website uses Google Analytics, which sets first-party cookies to count visits and see how pages are used. The site\'s own code sets no cookies; it uses your browser\'s local storage only for a few convenience features, such as remembering that you closed the claim review pop-up. We use no advertising cookies or ad retargeting.</p>'],
    ],
    'body' => <<<'HTML'
<p><strong>Last updated: October 22, 2026</strong></p>
<p>This Privacy Policy explains how Corpus Christi Public Adjuster, a public adjusting service of [[company]] ("we," "our," or "us"), handles information when you visit corpuschristipublicadjuster.com, use its tools, or contact us. It is written to describe what this website actually does.</p>

<h2>Information you give us</h2>
<p>When you submit a Free Claim Review or contact form, we collect the information you enter, which may include:</p>
<ul>
<li>Name, email address, and phone number</li>
<li>Property city and ZIP code</li>
<li>Claim type and claim status</li>
<li>Your insurance company (optional)</li>
<li>Date of loss (optional)</li>
<li>Your message</li>
<li>File uploads such as photos or PDFs (optional)</li>
</ul>
<p>You do not have to provide personal information to browse the site. Please share only what is needed to describe your situation, and do not send Social Security numbers, bank account details, or similar sensitive data through the form.</p>

<h2>How form submissions and uploads are handled</h2>
<p>Every form submission is emailed to <strong>info@corpuschristipublicadjuster.com</strong>. Submissions are <strong>not stored in a website database</strong>. Files you upload are attached to that email and are <strong>not kept on the web server</strong> after the message is sent. The form accepts a limited number of image and PDF files of limited size. After delivery, your submission is kept in our business email system as described under Data retention.</p>
<p>If you email Joseph Dittman directly at [[author-email]], that message is handled in the same way as other business email.</p>

<h2>How we use your information</h2>
<ul>
<li>To review your claim situation and respond to your request</li>
<li>To communicate with you about your property damage, claim, or our services</li>
<li>To prepare and handle a claim if you become a client under a written contract</li>
<li>To meet legal and regulatory obligations, including Texas Department of Insurance requirements</li>
<li>To protect the website from spam and abuse</li>
</ul>

<h2>Calls and text messages</h2>
<p>We call or text you only in response to a request you made, such as a Free Claim Review, or in connection with a claim we are handling for you. We do not send marketing text messages. You can ask us to stop contacting you at any time.</p>

<h2>Spam protection and rate limiting</h2>
<p>To limit spam and automated abuse of our forms, the website stores a one-way hash of the visitor's IP address with submission timestamps. The hash is not readily reversible into the original IP address. These records are deleted after about 3 days.</p>

<h2>Server and security logs</h2>
<p>Like most websites, our hosting provider may keep server and security logs that include IP addresses, browser information, requested pages, and timestamps. These logs are used to operate and secure the service. The website's own error logs record technical problems, not the content of your messages.</p>

<h2>Cookies, local storage, and analytics</h2>
<ul>
<li><strong>Cookies.</strong> The website\'s own code does not set cookies. Google Analytics (below) sets first-party analytics cookies. We use no advertising cookies or ad retargeting.</li>
<li><strong>Pop-up preference.</strong> The Free Claim Review pop-up uses your browser's local storage and session storage to remember that it was shown, closed, or submitted, so it does not keep reappearing. This stays on your device and is not sent to us.</li>
<li><strong>Analytics.</strong> We use Google Analytics 4 to understand how visitors use the site (pages viewed, approximate location, device and browser type, and how you arrived). Google processes this data under its own <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">privacy policy</a>. We do not send form contents to Google Analytics. You can block analytics cookies in your browser settings or with Google\'s <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">opt-out add-on</a>.</li>
</ul>
<p>You can clear local storage at any time through your browser settings.</p>

<h2>Claim tools that run in your browser</h2>
<p>The <a href="/claim-calculator/">claim settlement calculator</a>, <a href="/hurricane-deductible-calculator/">hurricane deductible calculator</a>, and <a href="/claim-deadline-calculator/">claim deadline calculator</a> run entirely in your browser. The numbers and dates you enter are not sent to our server.</p>
<p>The <a href="/claim-documentation-checklist/">claim documentation checklist</a> can save your progress in your browser's local storage, but only if you choose to. That information stays on your device and is never sent to us. You can clear it through the tool or your browser settings.</p>
<p>The <a href="/storm-lookup/">storm event lookup</a> asks for a city or ZIP code, not a street address.</p>

<h2>Weather, storm data, and maps</h2>
<p>Our server requests weather, alert, and forecast data from the National Weather Service (api.weather.gov), tide data from NOAA CO-OPS (Tides and Currents), tropical storm data from the National Hurricane Center, and storm records from the NOAA National Centers for Environmental Information and the Iowa Environmental Mesonet (IEM). Because our server makes those requests, <strong>your IP address is not shared with those providers</strong> for that data.</p>
<p>Some content loads directly in your browser from third parties:</p>
<ul>
<li><strong>Radar loop.</strong> NEXRAD radar image tiles load from the Iowa Environmental Mesonet.</li>
<li><strong>Base maps.</strong> Map tiles load from OpenStreetMap tile servers (storm maps) and from Esri ArcGIS Online (the radar base map).</li>
</ul>
<p>When those maps are displayed, your browser connects to those servers, and they receive your IP address and standard browser information under their own privacy and usage policies.</p>

<h2>Sharing of information</h2>
<p>We do not sell your personal information. We share it only:</p>
<ul>
<li>With service providers that help us operate the website and email, under confidentiality obligations</li>
<li>With your insurer or others involved in your claim, when you are a client and the sharing is needed to handle the claim</li>
<li>When required by law, regulation, subpoena, or a request from the Texas Department of Insurance</li>
<li>To protect our rights, safety, or property, or those of others</li>
</ul>

<h2>Data retention</h2>
<p>Because submissions are delivered by email, they are kept in our email system as long as needed to respond to you, handle any resulting claim, and meet legal and regulatory record-keeping requirements. Inquiries that do not lead to representation may be deleted when no longer needed. You may ask us to delete your information, subject to those obligations.</p>

<h2>Security</h2>
<p>We use reasonable administrative and technical safeguards, including encrypted HTTPS connections, authenticated email delivery, and limited access to submissions. No website or email system is completely secure, so we cannot guarantee absolute security.</p>

<h2>Children's privacy</h2>
<p>This website is not intended for children under 13, and we do not knowingly collect their personal information. If you believe a child has submitted information, contact us and we will delete it.</p>

<h2>Your choices</h2>
<p>You may contact us to ask what personal information we hold about you, to correct it, or to request deletion, and we will respond within a reasonable time as required by applicable law. We do not sell personal data or use it for targeted advertising.</p>

<h2>Third-party links</h2>
<p>This website links to outside sites such as government agencies. We are not responsible for their privacy practices; please review their policies.</p>

<h2>How to contact us</h2>
<p>For privacy questions or requests, contact Corpus Christi Public Adjuster ([[company]]) by email at [[email]] or by phone or text at [[phone]].</p>

<h2>Changes to this policy</h2>
<p>We may update this Privacy Policy when the website or our practices change. The date at the top of this page shows when it was last revised.</p>
HTML,
];
