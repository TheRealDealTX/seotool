<?php partial('page-hero', [
    'title'   => 'Privacy Policy',
    'lead'    => 'How the Friendswood Roofers website handles the information you share with us.',
    'actions' => false,
]); ?>
<section class="section section--first">
  <div class="container narrow prose legal">
    <p class="small">Effective date: <?= e(display_date((string) config('launch_date'))) ?></p>

    <p>This policy explains what information the Friendswood Roofers website at friendswoodroofs.com collects, how it is used and the choices you have. It covers this website only.</p>

    <h2>Information you choose to send us</h2>
    <p>When you submit the estimate request form, we receive:</p>
    <ul>
      <li>Your name and phone number (required)</li>
      <li>Your email address, if you choose to give it</li>
      <li>Your property address or ZIP code (required)</li>
      <li>The service you are interested in (required)</li>
      <li>Your message, if you write one, which may include a summary from the Roofing Project Planner</li>
      <li>Your confirmation that we may contact you about the request</li>
    </ul>
    <p>We use this information only to respond to your request, discuss your roofing project, prepare an estimate and keep a record of our communication with you. Please don't include sensitive information, such as financial account numbers, in the message field.</p>

    <h2>How form submissions are delivered and stored</h2>
    <p>The website does not keep your submission in a database. When you press Send, our server delivers the details as an email through our authenticated business email service to the Friendswood Roofers team inbox, which is hosted by a third-party email provider. If you give an email address, it is set as the reply-to address so we can answer you.</p>
    <p>Emails are kept in our inbox for as long as reasonably needed to handle your request and any resulting work, and for ordinary business records. You can ask us to delete your request (see "Your choices" below).</p>

    <h2>Information collected automatically</h2>
    <ul>
      <li><strong>Security cookie.</strong> Pages that contain the estimate form, and the confirmation page, set one session cookie named <code>fr_sess</code>. It protects the form against forged submissions and lets us show you any form errors after a page reload. It contains a random identifier only and expires when you close your browser.</li>
      <li><strong>Spam and abuse protection.</strong> To limit repeated or automated submissions, the server temporarily records a one-way, salted hash of your IP address and the time of each submission. The hash cannot be read back as an IP address, and these records are deleted automatically, generally within about a day.</li>
      <li><strong>Server logs.</strong> Like most websites, our hosting provider automatically records standard request information, such as IP address, browser type, the page requested and the time, for security and operation of the service. Our own error logs record technical errors only, not the content of form submissions.</li>
    </ul>
    <p>This website does not use analytics tools, advertising cookies or tracking pixels, and we do not sell or rent your personal information.</p>

    <h2>Roofing Project Planner</h2>
    <p>The Roofing Project Planner runs in your web browser. Your answers are not sent to us unless you choose to include the summary in an estimate request. If JavaScript is turned off in your browser, the planner instead sends your answers to our server in the page address so it can build the summary. In that case, the answers may appear in the hosting provider's standard server logs, but they are not otherwise stored.</p>

    <h2>Live weather map (third-party embed)</h2>
    <p>The homepage includes a live radar map embedded from RainViewer. When that part of the page loads, your browser connects directly to RainViewer's servers, which receive standard technical information such as your IP address and browser details, and RainViewer may use cookies, analytics tools (such as Google Tag Manager) or similar technologies under its own policies. We do not control that data. See <a href="https://www.rainviewer.com/privacy.html" rel="noopener">RainViewer's privacy policy</a>. The map loads only when you scroll near it, and the rest of the site works without it.</p>

    <h2>Links to other websites</h2>
    <p>We link to other sites, such as the National Weather Service and the Texas Department of Insurance. Their privacy practices are governed by their own policies.</p>

    <h2>How we share information</h2>
    <p>We share your information only as needed to respond to your request and provide our services, with service providers that operate this website and our email (such as our web host and email provider), or when required by law. We do not share your information with third parties for their own marketing.</p>

    <h2>Security</h2>
    <p>The site uses HTTPS encryption, authenticated email delivery, server-side validation and protections against spam and forged submissions. No method of transmission or storage is completely secure, but we take reasonable steps to protect the information you send.</p>

    <h2>Your choices</h2>
    <ul>
      <li>Email is optional. You can contact us by phone only.</li>
      <li>You can ask what information we have from your request, ask us to correct it, or ask us to delete it, subject to any records we must keep.</li>
      <li>You can tell us at any time to stop contacting you about a request.</li>
      <li>You can block or delete cookies in your browser settings. The estimate form needs its security cookie to work, but you can always call us instead.</li>
    </ul>
    <p>To make a request, call us at <a href="<?= e(phone_href()) ?>"><?= e(phone_display()) ?></a>.</p>

    <h2>Children</h2>
    <p>This website is intended for adults arranging roofing services. We do not knowingly collect information from children under 13.</p>

    <h2>Changes to this policy</h2>
    <p>If our practices change, for example if we add analytics or a new form, we will update this page and its effective date.</p>
    <p>Related: <a href="/terms-of-use/">Terms of Use</a> &middot; <a href="/contact/">Contact Us</a></p>
  </div>
</section>
