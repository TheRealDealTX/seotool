<?php
defined('HA_ROOT') || exit;
$title = 'Integrations';
$fields = $format === 'json'
    ? ['lead_id', 'name', 'first_name', 'last_name', 'email', 'phone', 'phone_e164', 'move_in', 'bedrooms', 'budget', 'message',
       'property', 'property_url', 'page_url', 'submitted_at', 'submitted_local', 'source']
    : ['First Name', 'Last Name', 'Phone', 'Email', 'Max Budget', 'How Many Bedrooms?', 'Move-in Date', 'City', 'Comments', 'Phone JS',
       'Date', 'Time', 'Page URL', 'User Agent', 'Remote IP', 'Powered by', 'form_id', 'form_name'];
?>
<div class="grid-2">
  <section class="card">
    <h2>Send leads to Integrately</h2>
    <p class="muted">Every form on the website (popup, contact page, listing “Check availability”) is sent to this webhook the moment it’s submitted. Leads are still saved under <a href="/admin/leads/">Leads</a> and emailed as before.</p>
    <form method="post">
      <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
      <label class="block">Integrately webhook URL
        <input name="webhook_url" type="url" value="<?= e($url) ?>" placeholder="https://webhooks.integrately.com/a/webhooks/…" autocomplete="off" spellcheck="false">
      </label>
      <p><button class="btn primary" type="submit">Save</button> <?php if ($url): ?><button class="btn" type="submit" name="do" value="test">Send a test lead</button><?php endif ?></p>
    </form>
    <form method="post" class="format-pick">
      <input type="hidden" name="_csrf" value="<?= e($csrf) ?>"><input type="hidden" name="do" value="format">
      <p><strong>Data format</strong></p>
      <label class="inline"><input type="radio" name="format" value="elementor"<?= $format === 'elementor' ? ' checked' : '' ?>> <span><strong>Same as riseapartments.com</strong> (Elementor webhook) – copy your Rise automation and the fields line up</span></label>
      <label class="inline"><input type="radio" name="format" value="json"<?= $format === 'json' ? ' checked' : '' ?>> <span>Simple JSON fields (name, email, move_in…)</span></label>
      <p><button class="btn small" type="submit">Save format</button></p>
    </form>
    <?php if ($last): ?>
      <p class="note"><span><strong>Last delivery:</strong> <?= $last['ok'] ? '✅ delivered' : '⚠️ failed – ' . e($last['error']) ?> ·
        <?= e($last['lead'] ?? '') ?> · <?= e(date('M j, g:i A', strtotime($last['at']))) ?> UTC</span></p>
    <?php endif ?>
  </section>
  <section class="card">
    <h2>How to connect</h2>
    <ol class="steps-list">
      <li>In Integrately, copy your riseapartments.com contact-form automation (or create one with <strong>Webhook / API → Webhook received</strong>). Copy the new automation’s webhook URL.</li>
      <li>Paste it above and click <strong>Save</strong>.</li>
      <li>Click <strong>Send a test lead</strong>, then in Integrately click to check for new data. The sample lead’s fields appear.</li>
      <li>Map the fields to your action (CRM, Google Sheets, SMS…) and turn the automation on.</li>
    </ol>
    <h3>Fields sent</h3>
    <p class="muted"><?= implode(', ', array_map(fn ($f) => '<code>' . $f . '</code>', $fields)) ?></p>
  </section>
</div>
