"""Privacy policy (carried over from the WordPress site, with the contact
placeholders filled in) and a new terms-of-use page."""

from siteconfig import BIZ

PRIVACY = {
    "path": "/privacy-policy/",
    "title": "Privacy Policy | Christina Dittman Creations",
    "description": "How Christina Dittman Creations (Belton Banners) collects, uses and protects the information you share when you request a custom hand-painted banner.",
    "h1": "Privacy Policy",
    "effective": "Effective Date: March 2026",
    "body": f"""
<p>Christina Dittman Creations (“we,” “our,” or “us”) respects your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, and safeguard your information when you visit our website or submit a request for custom hand-painted banners.</p>
<h2>Information We Collect</h2>
<p>When you interact with our website, we may collect the following information:</p>
<h3>Personal Information You Provide</h3>
<ul><li>Name</li><li>Email address</li><li>Phone number</li><li>Event details (such as type of event, date, and design preferences)</li><li>Any additional information you submit through our contact or order forms</li></ul>
<h3>Automatically Collected Information</h3>
<ul><li>IP address</li><li>Browser type and device information</li><li>Pages visited and time spent on the site</li></ul>
<p>This information helps us improve your experience and better understand how our website is used.</p>
<h2>How We Use Your Information</h2>
<p>We use your information to:</p>
<ul><li>Respond to inquiries and provide quotes</li><li>Communicate with you about your custom banner order</li><li>Process and manage orders</li><li>Improve our website and services</li><li>Send updates related to your request or order</li></ul>
<p>We do not sell or rent your personal information to third parties.</p>
<h2>How We Protect Your Information</h2>
<p>We take reasonable measures to protect your personal information from unauthorized access, misuse, or disclosure. While no method of transmission over the internet is 100% secure, we strive to use commercially acceptable means to safeguard your data.</p>
<h2>Sharing Your Information</h2>
<p>We may share your information only in the following situations:</p>
<ul><li>With trusted service providers who help us operate our website or fulfill orders</li><li>When required by law or to comply with legal obligations</li></ul>
<p>We only share the minimum necessary information and ensure appropriate safeguards are in place.</p>
<h2>Cookies and Tracking Technologies</h2>
<p>Our website may use cookies and similar technologies to enhance your browsing experience. Cookies help us understand how visitors use our site and allow us to improve functionality.</p>
<p>You can choose to disable cookies through your browser settings.</p>
<h2>Your Choices and Rights</h2>
<p>You have the right to:</p>
<ul><li>Request access to the personal information we hold about you</li><li>Request corrections or updates to your information</li><li>Request deletion of your personal data</li></ul>
<p>To make any of these requests, please contact us using the information below.</p>
<h2>Third-Party Links</h2>
<p>Our website may contain links to third-party websites. We are not responsible for the privacy practices or content of those websites.</p>
<h2>Children’s Privacy</h2>
<p>Our services are not directed toward individuals under the age of 13. We do not knowingly collect personal information from children.</p>
<h2>Changes to This Privacy Policy</h2>
<p>We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated effective date.</p>
<h2>Contact Us</h2>
<p>If you have any questions about this Privacy Policy or how your information is handled, please contact us:</p>
<p><strong>Christina Dittman Creations</strong><br>
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a><br>
<a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></p>
""",
}

TERMS = {
    "path": "/terms-of-use/",
    "title": "Terms of Use | Christina Dittman Creations",
    "description": "Terms of use for beltonbanners.com and for ordering custom hand-painted banners from Christina Dittman Creations in Belton, TX.",
    "h1": "Terms of Use",
    "effective": "Effective Date: October 2026",
    "body": f"""
<p>These terms apply to your use of beltonbanners.com (the “Site”) and to custom banner orders placed with Christina Dittman Creations (“we,” “our,” or “us”). By using the Site or placing an order you agree to them.</p>
<h2>Custom Orders</h2>
<ul>
<li>Every banner is made to order. A quote is confirmed with you before painting begins, and a sketch or design description is shared for approval.</li>
<li>Because each banner is painted by hand, small variations in lettering, color and texture are part of the work and are not defects.</li>
<li>Changes requested after painting has started may change the price or the completion date.</li>
<li>Turnaround times are estimates. Rush requests are accommodated when the schedule allows.</li>
</ul>
<h2>Payment, Cancellation and Refunds</h2>
<ul>
<li>Payment terms are confirmed with your quote. Custom work that has already been started is not refundable.</li>
<li>If you need to cancel before painting begins, let us know as soon as possible.</li>
</ul>
<h2>Artwork and Copyright</h2>
<ul>
<li>Designs, sketches and photographs created by Christina Dittman Creations remain our copyright. You receive the physical banner for personal, non-commercial display.</li>
<li>We may photograph finished banners and show them on this Site and on social media. Tell us at the time of ordering if you would prefer that a banner is not shown.</li>
<li>Please only request wording, logos or artwork you have the right to use.</li>
</ul>
<h2>Care and Use</h2>
<p>Banners are painted on paper or canvas and are intended for indoor or covered display. Guidance on hanging and storage is provided on the <a href="/faq/">FAQ</a> page. We are not responsible for damage caused by weather, improper hanging or storage.</p>
<h2>Website Content</h2>
<p>Content on this Site is provided for general information and may change without notice. We make reasonable efforts to keep it accurate but do not guarantee that it is complete or current.</p>
<h2>Limitation of Liability</h2>
<p>To the extent permitted by law, our liability for any order is limited to the amount paid for that order.</p>
<h2>Contact</h2>
<p><strong>Christina Dittman Creations</strong><br>
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a><br>
<a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></p>
""",
}
