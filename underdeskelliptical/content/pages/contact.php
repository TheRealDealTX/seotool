<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// The form posts back to /contact/; handling is in contact_handle() (inc/contact.php).
$status = contact_handle();
$form = $status === 'sent'
    ? '<div class="callout"><p><strong>Thanks, your message is on its way.</strong> We usually reply within one to two business days.</p></div>'
    : ($status === 'error' ? '<div class="callout warn"><p>Please fill in your name, a valid email and a message.</p></div>' : '') . '
<form class="contact-form tool" method="post" action="/contact/">
  <div class="tool-form">
    <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required maxlength="100" autocomplete="name"></div>
    <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required maxlength="150" autocomplete="email"></div>
    <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>Help choosing a product</option><option>Question about an article</option><option>Report an error</option><option>Business or partnership</option><option>Other</option></select></div>
    <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required maxlength="5000"></textarea></div>
    <div class="hp" aria-hidden="true"><label>Leave this empty <input name="website" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="t" value="' . time() . '">
    <button class="btn" type="submit">Send message</button>
  </div>
</form>';
return [
    'title' => 'Contact Under Desk Elliptical',
    'description' => 'Questions about choosing or using an under desk elliptical? Contact the Under Desk Elliptical team. We reply within one to two business days.',
    'h1' => 'Contact Us',
    'lead' => 'Questions about choosing or using an under desk elliptical? We\'re happy to help.',
    'schema' => [['@type' => 'ContactPage', 'name' => 'Contact Under Desk Elliptical', 'url' => SITE_URL . '/contact/']],
    'body' => <<<HTML
<p>Tell us about your desk, your budget and what you want from an under desk elliptical, and we'll point you in the right direction. You can also send feedback on our guides or report anything that looks out of date.</p>
<p>Want an instant answer? Try the <a href="/tools/which-under-desk-elliptical-quiz/">60-second quiz</a> or check whether a machine will fit with the <a href="/tools/desk-clearance-checker/">desk clearance checker</a>.</p>
{$form}
<p class="small">We use your details only to reply. See our <a href="/privacy-policy/">privacy policy</a>.</p>
HTML,
];
