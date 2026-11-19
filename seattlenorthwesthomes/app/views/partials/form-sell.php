<?php defined('SNW') || (http_response_code(404) && exit); ?>
<form class="lead-form" id="form" method="post" action="/submit/">
  <?= form_guard('sell') ?>
  <?= form_flash() ?>
  <?php partial('form-fields') ?>
  <label>Property address<input type="text" name="address" autocomplete="street-address" required></label>
  <div class="grid-2">
    <label>Neighborhood<select name="neighborhood"><option value="">Select</option>
<?php foreach (neighborhoods() as $h): ?><option><?= e($h['name']) ?></option><?php endforeach ?>
      <option>Other Seattle area</option></select></label>
    <label>ZIP code<input type="text" name="zip" inputmode="numeric" maxlength="10" autocomplete="postal-code"></label>
    <label>Property type<select name="property_type"><option value="">Select</option><option>Single Family</option><option>Condo</option><option>Townhome</option><option>Multi-Family</option><option>Land</option></select></label>
    <label>Estimated value<input type="text" name="estimated_price" placeholder="Your best guess is fine"></label>
    <label>Bedrooms<input type="number" name="beds" min="0" max="20"></label>
    <label>Bathrooms<input type="number" name="baths" min="0" max="20" step="0.25"></label>
  </div>
  <label>When would you like to sell?<select name="timeline"><option value="">Select</option><option>Within 30 days</option><option>1–3 months</option><option>3–6 months</option><option>Just curious about my home's value</option></select></label>
  <label>Anything else we should know?<textarea name="message" rows="4" placeholder="Recent updates, condition, questions about timing…"></textarea></label>
  <button class="btn btn-accent btn-lg" type="submit">Request My Free Home Value Review</button>
  <p class="fine">No obligation. We'll review recent comparable sales and reply with next steps.</p>
</form>
