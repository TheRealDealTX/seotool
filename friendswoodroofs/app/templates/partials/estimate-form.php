<?php
/**
 * Estimate request form. Works as a normal POST without JavaScript; site.js
 * enhances it with inline validation and an in-page submit.
 *
 * @var string $returnTo  page path the form lives on (must be in FORM_PAGES)
 * @var string $heading   visible heading text
 * @var string $headingLevel  'h2' or 'h3'
 * @var string $intro     optional intro sentence
 */
$flash   = form_flash();
$errors  = $flash['errors'];
$old     = $flash['old'];
$val     = fn (string $k) => e(is_string($old[$k] ?? null) ? $old[$k] : '');
$msgValue = is_string($old['message'] ?? null) ? $old['message'] : ($prefillMessage ?? '');
$prefill = isset($_GET['service']) && is_string($_GET['service']) && array_key_exists($_GET['service'], service_options()) ? $_GET['service'] : '';
$prefillService ??= '';
$prefillMessage ??= '';
$selected = is_string($old['service'] ?? null) ? $old['service'] : ($prefill !== '' ? $prefill : $prefillService);
$headingLevel ??= 'h2';
$intro ??= '';
$err = function (string $field) use ($errors): string {
    return isset($errors[$field])
        ? '<p class="field-error" id="err-' . $field . '">' . icon('alert', 'icon icon-sm') . '<span>' . e($errors[$field]) . '</span></p>'
        : '<p class="field-error" id="err-' . $field . '" hidden></p>';
};
$invalid = fn (string $f) => isset($errors[$f]) ? ' aria-invalid="true"' : '';
$fieldLabels = ['name' => 'Name', 'phone' => 'Phone', 'email' => 'Email', 'location' => 'Property address or ZIP code', 'service' => 'Service needed', 'message' => 'Message', 'consent' => 'Consent'];
?>
<div class="estimate-card" id="estimate-form">
  <<?= $headingLevel ?> class="estimate-title" id="estimate-heading" tabindex="-1"><?= e($heading) ?></<?= $headingLevel ?>>
  <?php if ($intro): ?><p class="estimate-intro"><?= e($intro) ?></p><?php endif; ?>
  <p class="form-note">Fields marked <span class="req" aria-hidden="true">*</span><span class="sr-only">with an asterisk</span> are required. Prefer to talk? Call <a href="<?= e(phone_href()) ?>"><?= e(phone_display()) ?></a>.</p>

  <div class="form-status" data-form-status role="alert" aria-live="assertive"<?= $flash['message'] ? '' : ' hidden' ?>>
    <?php if ($flash['message']): ?>
      <p class="form-status-title"><?= icon('alert', 'icon icon-sm') ?> <span><?= e($flash['message']) ?></span></p>
      <?php if ($errors): ?>
      <ul>
        <?php foreach ($errors as $f => $msg): ?>
        <li><a href="#f-<?= e($f) ?>"><?= e($fieldLabels[$f] ?? $f) ?>: <?= e($msg) ?></a></li>
        <?php endforeach; ?>
      </ul>
      <?php endif; ?>
    <?php endif; ?>
  </div>

  <form class="estimate-form" method="post" action="/submit-estimate/" novalidate data-estimate-form aria-labelledby="estimate-heading">
    <input type="hidden" name="csrf" value="<?= e(csrf_token()) ?>">
    <input type="hidden" name="ts" value="<?= e(form_timestamp_token()) ?>">
    <input type="hidden" name="return_to" value="<?= e($returnTo) ?>">
    <div class="hp-field" aria-hidden="true">
      <label for="f-website">Leave this field empty</label>
      <input type="text" id="f-website" name="website" tabindex="-1" autocomplete="off">
    </div>

    <div class="form-grid">
      <div class="field">
        <label for="f-name">Name <span class="req" aria-hidden="true">*</span></label>
        <input type="text" id="f-name" name="name" required maxlength="100" autocomplete="name" value="<?= $val('name') ?>" aria-describedby="err-name"<?= $invalid('name') ?>>
        <?= $err('name') ?>
      </div>
      <div class="field">
        <label for="f-phone">Phone <span class="req" aria-hidden="true">*</span></label>
        <input type="tel" id="f-phone" name="phone" required maxlength="40" autocomplete="tel" inputmode="tel" value="<?= $val('phone') ?>" aria-describedby="hint-phone err-phone"<?= $invalid('phone') ?>>
        <p class="field-hint" id="hint-phone">Include area code.</p>
        <?= $err('phone') ?>
      </div>
      <div class="field">
        <label for="f-email">Email <span class="optional">(optional)</span></label>
        <input type="email" id="f-email" name="email" maxlength="254" autocomplete="email" value="<?= $val('email') ?>" aria-describedby="hint-email err-email"<?= $invalid('email') ?>>
        <p class="field-hint" id="hint-email">Leave blank if you prefer a phone call.</p>
        <?= $err('email') ?>
      </div>
      <div class="field">
        <label for="f-location">Property address or ZIP code <span class="req" aria-hidden="true">*</span></label>
        <input type="text" id="f-location" name="location" required maxlength="200" autocomplete="street-address" value="<?= $val('location') ?>" aria-describedby="err-location"<?= $invalid('location') ?>>
        <?= $err('location') ?>
      </div>
      <div class="field field-full">
        <label for="f-service">Service needed <span class="req" aria-hidden="true">*</span></label>
        <select id="f-service" name="service" required aria-describedby="err-service"<?= $invalid('service') ?>>
          <option value="">Choose a service</option>
          <?php foreach (service_options() as $value => $label): ?>
          <option value="<?= e($value) ?>"<?= $selected === $value ? ' selected' : '' ?>><?= e($label) ?></option>
          <?php endforeach; ?>
        </select>
        <?= $err('service') ?>
      </div>
      <div class="field field-full">
        <label for="f-message">Describe your roofing concern <span class="optional">(optional)</span></label>
        <textarea id="f-message" name="message" rows="5" maxlength="4000" aria-describedby="hint-message err-message" data-message-field><?= e($msgValue) ?></textarea>
        <p class="field-hint" id="hint-message">What are you seeing, where, and since when? Is water coming inside? Roof age and material help if you know them.</p>
        <?= $err('message') ?>
      </div>
      <div class="field field-full field-check">
        <input type="checkbox" id="f-consent" name="consent" value="1" required<?= !empty($old['consent']) ? ' checked' : '' ?> aria-describedby="err-consent"<?= $invalid('consent') ?>>
        <label for="f-consent">I agree that Friendswood Roofers may contact me by phone, text or email about this request. <span class="req" aria-hidden="true">*</span> <a href="/privacy-policy/">Privacy Policy</a></label>
        <?= $err('consent') ?>
      </div>
    </div>

    <div class="form-actions">
      <button class="btn btn-accent btn-lg" type="submit" data-submit><span data-submit-label>Send Estimate Request</span></button>
      <p class="form-fineprint">Submitting this form sends your request to our team. It does not schedule an appointment or create a binding quote.</p>
    </div>
  </form>
</div>
