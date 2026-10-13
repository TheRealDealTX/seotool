<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';

$path = '/contact/';
$crumbs = [['Home', '/'], ['Contact', $path]];
page_start([
    'title' => 'Contact | Sugar Land Public Adjuster | +1 (832) 503-5866',
    'description' => 'If you’re dealing with property damage, insurance questions, or a settlement that doesn’t feel right, this is the right place to start. Call or text (832) 503-5866.',
    'path' => $path,
    'page_type' => 'ContactPage',
    'breadcrumbs' => $crumbs,
    'body_class' => 'no-auto-popup',
]);
page_hero('Contact', 'Call, text or email a licensed Sugar Land public adjuster—or send the form for a free, no-obligation claim review.', $crumbs, 'Free claim review');
?>
<section class="section">
  <div class="container split">
    <div class="prose">
<?php if (isset($_GET['error'])): ?>
      <div class="callout callout-warn"><p>Sorry—your message could not be sent. Please check your name and phone number, or call/text us directly at <?= tel_link() ?>.</p></div>
<?php endif; ?>
      <p>If you’re dealing with property damage, insurance questions, or a settlement that doesn’t feel right, this is the right place to start. A short conversation can help clarify your options and prevent costly mistakes before they happen.</p>
      <p>Use the form to tell us a little about your situation. A Sugar Land public adjuster will review your information and follow up to discuss next steps—no pressure, no obligation.</p>
      <p><strong>Your claim matters. Let’s make sure it’s handled properly from the start.</strong></p>
      <div class="grid-2 mt-2">
        <div class="card"><div class="icon" aria-hidden="true">📞</div><h2 class="h3">Call</h2><p><?= tel_link() ?></p></div>
        <div class="card"><div class="icon" aria-hidden="true">💬</div><h2 class="h3">Text</h2><p><?= sms_link(SITE['phone_display']) ?><br><span class="small muted">Photos of the damage welcome.</span></p></div>
        <div class="card"><div class="icon" aria-hidden="true">✉️</div><h2 class="h3">Email</h2><p><a href="mailto:<?= e(SITE['email']) ?>"><?= e(SITE['email']) ?></a></p></div>
        <div class="card"><div class="icon" aria-hidden="true">📍</div><h2 class="h3">Service area</h2><p>Sugar Land &amp; Fort Bend County. <a href="/service-areas/">See all areas</a></p></div>
      </div>
      <h2>What to have handy</h2>
      <ul class="checklist">
        <li>Your policy number and declarations page (if available)</li>
        <li>Your claim number and the insurer’s estimate or denial letter</li>
        <li>Photos or video of the damage</li>
        <li>The date the damage happened</li>
      </ul>
      <p class="small muted">Don’t have them? That’s fine—we can help you request your full policy from the insurer.</p>
    </div>
    <div class="form-card">
      <h2>Request a free claim review</h2>
      <?php lead_form('contact', 'Contact page', true); ?>
    </div>
  </div>
</section>
<?php page_end(); ?>
