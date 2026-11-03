<?php
defined('SCC') || (http_response_code(404) && exit);
$status = $_GET['sent'] ?? '';
$t = time();
$sig = hash_hmac('sha256', (string) $t, config('form_secret', 'scc-form-' . SITE_ORIGIN));
page_head([
    'title' => 'Contact Solar CCTV Camera',
    'description' => 'Contact the Solar CCTV Camera team with questions about solar security cameras, corrections to our guides, or partnership enquiries.',
    'path' => '/contact/',
    'schema' => [breadcrumb_schema([['Home', '/'], ['Contact', '/contact/']]), ['@type' => 'ContactPage', 'name' => 'Contact Solar CCTV Camera', 'url' => abs_url('/contact/')]],
]);
?>
<section class="page-hero"><div class="hero-sky" aria-hidden="true"><span class="hero-sun"></span></div><div class="wrap" style="position:relative">
  <?= breadcrumbs_html([['Home', '/'], ['Contact', '/contact/']]) ?>
  <h1>Contact us</h1>
  <p class="lede">Questions about a solar camera setup, a correction to one of our guides, or a partnership idea? Send us a message and we’ll reply by email, usually within two business days.</p>
</div></section>
<section class="section" style="padding-top:50px">
  <div class="wrap split" style="align-items:start">
    <div class="form-card">
<?php if ($status === '1'): ?><div class="notice ok">Thanks, your message has been sent. We’ll reply by email.</div><?php endif; ?>
<?php if ($status === '0'): ?><div class="notice err">Sorry, your message could not be sent. Please check the fields and try again, or email us directly.</div><?php endif; ?>
      <form method="post" action="/contact/send" class="contact-form">
        <div class="field"><label for="c-name">Your name</label><input id="c-name" type="text" name="name" required maxlength="80" autocomplete="name"></div>
        <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required maxlength="120" autocomplete="email"></div>
        <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>Question about a solar camera setup</option><option>Correction or update to a guide</option><option>Tool feedback</option><option>Partnership / other</option></select></div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required minlength="20" maxlength="5000"></textarea></div>
        <div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <input type="hidden" name="t" value="<?= $t ?>"><input type="hidden" name="sig" value="<?= $sig ?>"><input type="hidden" name="js" value="0">
        <button class="btn btn-sun btn-lg" type="submit"><?= icon('mail', 20) ?> Send message</button>
        <p class="tool-note">We use your details only to reply. See our <a href="/privacy-policy/">privacy policy</a>. We can’t offer paid placements or guest posts.</p>
      </form>
    </div>
    <div class="prose">
      <h2>Before you write</h2>
      <p>Many setup questions are answered faster by our tools and guides:</p>
      <ul>
        <li>Camera keeps running flat? Start with <a href="/troubleshooting/not-charging/">solar camera not charging: fixes</a> and the <a href="/tools/solar-camera-battery-calculator/">battery calculator</a>.</li>
        <li>Unsure which way to point the panel? Use the <a href="/tools/solar-panel-angle-calculator/">panel angle calculator</a>.</li>
        <li>No Wi‑Fi at the spot? Read <a href="/guides/do-solar-cameras-need-wifi/">do solar cameras need Wi‑Fi</a>.</li>
      </ul>
      <h2>Email</h2>
      <p><a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a></p>
      <p class="muted">We’re an online publication, not a retailer or installer, so we can’t process orders, returns or warranty claims. Contact the camera manufacturer for those.</p>
    </div>
  </div>
</section>
<script>document.addEventListener('DOMContentLoaded',function(){var f=document.querySelector('.contact-form');if(f){f.addEventListener('focusin',function(){f.elements.js.value='1';},{once:true});}});</script>
<?php page_foot();
