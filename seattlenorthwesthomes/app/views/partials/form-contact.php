<?php defined('SNW') || (http_response_code(404) && exit); ?>
<form class="lead-form" id="form" method="post" action="/submit/">
  <?= form_guard('contact') ?>
  <?= form_flash() ?>
  <?php partial('form-fields') ?>
  <label>What can we help with?<select name="interest"><option value="">Select</option><option>Buying a home</option><option>Selling a home</option><option>Buying and selling</option><option>A specific listing</option><option>Something else</option></select></label>
  <label>Message<textarea name="message" rows="5" required></textarea></label>
  <button class="btn btn-accent btn-lg" type="submit">Send Message</button>
</form>
