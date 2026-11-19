<?php defined('SNW') || (http_response_code(404) && exit); ?>
<form class="lead-form" id="form" method="post" action="/submit/">
  <?= form_guard('buy') ?>
  <?= form_flash() ?>
  <?php partial('form-fields') ?>
  <div class="grid-2">
    <label>Property type<select name="property_type"><option value="">Any</option><option>Single Family</option><option>Condo</option><option>Townhome</option><option>Multi-Family</option><option>Land</option></select></label>
    <label>Preferred neighborhood<select name="neighborhood"><option value="">Anywhere in Seattle</option>
<?php foreach (neighborhoods() as $h): ?><option><?= e($h['name']) ?></option><?php endforeach ?>
      <option>Seattle suburbs (Eastside / North / South)</option></select></label>
    <label>Budget<select name="budget"><option value="">Select a range</option><option>Under $600,000</option><option>$600,000 – $900,000</option><option>$900,000 – $1.3M</option><option>$1.3M – $2M</option><option>$2M+</option></select></label>
    <label>Timeline<select name="timeline"><option value="">When are you hoping to buy?</option><option>As soon as possible</option><option>1–3 months</option><option>3–6 months</option><option>6+ months / just exploring</option></select></label>
    <label>Bedrooms<select name="beds"><option value="">Any</option><option>1+</option><option>2+</option><option>3+</option><option>4+</option></select></label>
    <label>Bathrooms<select name="baths"><option value="">Any</option><option>1+</option><option>2+</option><option>3+</option></select></label>
  </div>
  <label>Tell us about your dream home<textarea name="message" rows="4" placeholder="Must-haves, commute, schools, yard, parking…"></textarea></label>
  <button class="btn btn-accent btn-lg" type="submit">Send My Home Wish List</button>
  <p class="fine">We'll reply by email, usually within one business day. No spam, ever.</p>
</form>
