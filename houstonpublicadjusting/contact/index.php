<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Contact', '/contact/']];
page_start([
    'title' => 'Contact Houston Public Adjusters | Free Claim Review (832) 503-5866',
    'desc' => 'Contact Houston Public Adjusters for a free insurance claim review. Call or text (832) 503-5866 or email jditt@risepublicadjusting.com. No pressure, no obligation.',
    'path' => '/contact/',
    'crumbs' => $crumbs,
    'no_popup' => true,
    'schema' => [['@type' => 'ContactPage', 'name' => 'Contact Houston Public Adjusters', 'url' => SITE_URL . '/contact/', 'mainEntity' => ['@id' => SITE_URL . '/#business']]],
]);
echo page_hero('Contact Houston Public Adjusters', 'If you&rsquo;re dealing with property damage, insurance questions or a settlement that doesn&rsquo;t feel right, this is the right place to start. A short conversation can help clarify your options and prevent costly mistakes before they happen.', $crumbs);
?>
<section class="section">
  <div class="wrap two-col">
    <div>
<?php if (!empty($_GET['error'])): ?>
      <p class="notice">Your message could not be sent. Please check the form and try again, or call or text <?= PHONE_DISPLAY ?>.</p>
<?php endif; ?>
      <div class="tool"><?= lead_form('lead-contact', 'Tell us about your claim', 'Use the form below to tell us a little about your situation. A Houston public adjuster will review your information and follow up to discuss next steps &mdash; no pressure, no obligation.') ?></div>
    </div>
    <div>
      <h2>Reach us directly</h2>
      <ul class="checklist">
        <li><strong>Call:</strong> <a href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a></li>
        <li><strong>Text:</strong> <a href="sms:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a> &mdash; send photos of the damage</li>
        <li><strong>Email:</strong> <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a></li>
        <li><strong>Hours:</strong> <?= HOURS_TEXT ?></li>
        <li><strong>Service area:</strong> Houston and surrounding cities &mdash; <a href="/service-areas/">see all areas</a></li>
        <li><strong>License:</strong> <?= LEGAL_NAME ?>, Texas public adjuster license #<?= LICENSE_NO ?></li>
      </ul>
      <h3>What to have ready</h3>
      <p>Helpful, but not required: photos or video of the damage, your claim number, the insurer&rsquo;s estimate or denial letter, any contractor estimates, and your policy declarations page.</p>
      <p>Your claim matters. Let&rsquo;s make sure it&rsquo;s handled properly from the start.</p>
      <div class="author-box"><img src="<?= AUTHOR['photo'] ?>" alt="Joseph Dittman" width="96" height="96" loading="lazy"><div><p class="author-name">Joseph Dittman</p><p>Licensed Texas public adjuster. Joseph or a member of our team will personally review your submission.</p></div></div>
    </div>
  </div>
</section>
<?php
page_end();
