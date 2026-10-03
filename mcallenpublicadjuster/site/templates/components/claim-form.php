<?php
$context = $context ?? '';
$compact = !empty($compact);
$fid = 'cf' . substr(md5(($context ?: 'form') . mt_rand()), 0, 6);
$claimTypes = ['Hail damage', 'Wind / storm damage', 'Hurricane / tropical storm', 'Roof damage', 'Fire damage', 'Smoke damage', 'Water damage', 'Flood-related', 'Commercial property', 'Other'];
$statuses = ['Not filed yet', 'Filed - waiting on insurer', 'Inspection completed', 'Claim denied', 'Claim underpaid / low offer', 'Claim delayed', 'Claim closed / settled', 'Other'];
?>
<form class="claim-form<?= $compact ? ' claim-form-compact' : '' ?>" action="/api/claim-review.php" method="post" enctype="multipart/form-data" novalidate data-claim-form>
  <input type="hidden" name="csrf_token" value="<?= e(form_token()) ?>">
  <input type="hidden" name="page_context" value="<?= e($context) ?>">
  <div class="hp-field" aria-hidden="true">
    <label for="<?= $fid ?>-website">Leave this field empty</label>
    <input type="text" id="<?= $fid ?>-website" name="website" tabindex="-1" autocomplete="off">
  </div>
  <div class="form-grid">
    <div class="field">
      <label for="<?= $fid ?>-name">Full name <span class="req" aria-hidden="true">*</span></label>
      <input id="<?= $fid ?>-name" name="full_name" type="text" autocomplete="name" required maxlength="100">
    </div>
    <div class="field">
      <label for="<?= $fid ?>-phone">Phone <span class="req" aria-hidden="true">*</span></label>
      <input id="<?= $fid ?>-phone" name="phone" type="tel" autocomplete="tel" required maxlength="30" inputmode="tel">
    </div>
    <div class="field">
      <label for="<?= $fid ?>-email">Email <span class="req" aria-hidden="true">*</span></label>
      <input id="<?= $fid ?>-email" name="email" type="email" autocomplete="email" required maxlength="150">
    </div>
    <div class="field">
      <label for="<?= $fid ?>-loc">Property city or ZIP code <span class="req" aria-hidden="true">*</span></label>
      <input id="<?= $fid ?>-loc" name="location" type="text" autocomplete="postal-code" required maxlength="80" placeholder="e.g. McAllen or 78504">
    </div>
    <div class="field">
      <label for="<?= $fid ?>-type">Claim type <span class="req" aria-hidden="true">*</span></label>
      <select id="<?= $fid ?>-type" name="claim_type" required>
        <option value="">Select one</option>
        <?php foreach ($claimTypes as $t): ?><option><?= e($t) ?></option><?php endforeach; ?>
      </select>
    </div>
    <div class="field">
      <label for="<?= $fid ?>-status">Claim status <span class="req" aria-hidden="true">*</span></label>
      <select id="<?= $fid ?>-status" name="claim_status" required>
        <option value="">Select one</option>
        <?php foreach ($statuses as $s): ?><option><?= e($s) ?></option><?php endforeach; ?>
      </select>
    </div>
    <?php if (!$compact): ?>
    <div class="field">
      <label for="<?= $fid ?>-ins">Insurance company <span class="opt">(optional)</span></label>
      <input id="<?= $fid ?>-ins" name="insurer" type="text" maxlength="100">
    </div>
    <div class="field">
      <label for="<?= $fid ?>-dol">Date of loss <span class="opt">(optional)</span></label>
      <input id="<?= $fid ?>-dol" name="date_of_loss" type="date" max="<?= date('Y-m-d') ?>">
    </div>
    <?php endif; ?>
    <div class="field field-full">
      <label for="<?= $fid ?>-msg">Briefly, what happened? <span class="req" aria-hidden="true">*</span></label>
      <textarea id="<?= $fid ?>-msg" name="message" rows="<?= $compact ? 3 : 4 ?>" required maxlength="4000"></textarea>
    </div>
    <?php if (!$compact && cfg('uploads_enabled')): ?>
    <div class="field field-full">
      <label for="<?= $fid ?>-files">Photos or documents <span class="opt">(optional &middot; up to <?= (int) cfg('upload_max_files') ?> files, <?= (int) (cfg('upload_max_bytes') / 1048576) ?> MB each &middot; JPG, PNG, WEBP, HEIC, PDF)</span></label>
      <input id="<?= $fid ?>-files" name="attachments[]" type="file" multiple accept=".jpg,.jpeg,.png,.webp,.heic,.heif,.pdf,image/jpeg,image/png,image/webp,image/heic,application/pdf">
    </div>
    <?php endif; ?>
    <div class="field field-full field-check">
      <input id="<?= $fid ?>-privacy" name="privacy_ack" type="checkbox" value="1" required>
      <label for="<?= $fid ?>-privacy">I agree that McAllen Public Adjuster may contact me about my request by phone, text, or email, and I have read the <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a>. <span class="req" aria-hidden="true">*</span></label>
    </div>
  </div>
  <div class="form-status" role="status" aria-live="polite" tabindex="-1"></div>
  <button class="btn btn-gold btn-lg btn-block" type="submit"><span class="btn-label">Request My Free Claim Review</span></button>
  <p class="form-note"><?= icon('shield', 'icon icon-sm') ?> <span>Your information is sent securely and used only to respond to your request. Prefer to talk? Call <a href="<?= e(tel_link()) ?>"><?= e(cfg('phone_short')) ?></a>.</span></p>
</form>
