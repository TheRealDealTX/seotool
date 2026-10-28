<?php
defined('HA_ROOT') || exit;
$title = 'Integrations';
$fields = ['lead_id', 'name', 'first_name', 'last_name', 'email', 'phone', 'phone_e164', 'move_in', 'bedrooms', 'budget', 'message',
           'property', 'property_url', 'page_url', 'submitted_at', 'submitted_local', 'source'];
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
    <?php if ($last): ?>
      <p class="note"><span><strong>Last delivery:</strong> <?= $last['ok'] ? '✅ delivered' : '⚠️ failed – ' . e($last['error']) ?> ·
        <?= e($last['lead'] ?? '') ?> · <?= e(date('M j, g:i A', strtotime($last['at']))) ?> UTC</span></p>
    <?php endif ?>
  </section>
  <section class="card">
    <h2>How to connect</h2>
    <ol class="steps-list">
      <li>In Integrately, create an automation and choose <strong>Webhook / API</strong> as the trigger (“Webhook received”). Copy the webhook URL it gives you.</li>
      <li>Paste it above and click <strong>Save</strong>.</li>
      <li>Click <strong>Send a test lead</strong>, then in Integrately click to check for new data. The sample lead’s fields appear.</li>
      <li>Map the fields to your action (CRM, Google Sheets, SMS…) and turn the automation on.</li>
    </ol>
    <h3>Fields sent</h3>
    <p class="muted"><?= implode(', ', array_map(fn ($f) => '<code>' . $f . '</code>', $fields)) ?></p>
  </section>
</div>
