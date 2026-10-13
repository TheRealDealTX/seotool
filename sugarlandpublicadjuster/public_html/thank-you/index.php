<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
page_start([
    'title' => 'Thank You | Sugar Land Public Adjuster',
    'description' => 'Thanks for contacting Sugar Land Public Adjuster. We will be in touch shortly.',
    'path' => '/thank-you/',
    'robots' => 'noindex, follow',
    'body_class' => 'no-auto-popup',
]);
page_hero('Thank you—we received your request', 'A Sugar Land public adjuster will contact you shortly. If your situation is urgent, call or text ' . tel_link() . '.', [['Home', '/'], ['Thank You', '/thank-you/']]);
?>
<script>try{localStorage.setItem('slpa_lead_sent','1')}catch(e){}</script>
<section class="section">
  <div class="container narrow prose">
    <h2>While you wait</h2>
    <ul class="checklist">
      <li>Photograph and video all damage before cleanup or repairs.</li>
      <li>Make temporary repairs to prevent further damage and keep every receipt.</li>
      <li>Avoid giving a recorded statement until you’ve talked with us.</li>
      <li>Start your contents list with the <a href="/tools/home-inventory-checklist/">home inventory builder</a>.</li>
    </ul>
    <p><a class="btn btn-primary" href="/blog/">Read our claim guides</a></p>
  </div>
</section>
<?php page_end(['no_popup' => true]); ?>
