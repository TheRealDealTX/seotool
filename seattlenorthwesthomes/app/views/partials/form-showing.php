<?php defined('SNW') || (http_response_code(404) && exit); ?>
<form class="lead-form compact" id="form" method="post" action="/submit/">
  <?= form_guard('showing') ?>
  <?= form_flash() ?>
  <input type="hidden" name="listing" value="<?= e($l['title'] . ' — ' . abs_url('/homes-for-sale/' . $l['slug'] . '/')) ?>">
  <label>Name<input type="text" name="first_name" autocomplete="name" required></label>
  <label>Email<input type="email" name="email" autocomplete="email" required></label>
  <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
  <label>Preferred time<select name="preferred_time"><option value="">Flexible</option><option>Weekday morning</option><option>Weekday afternoon</option><option>Weekday evening</option><option>Weekend</option><option>Virtual tour</option></select></label>
  <label>Message<textarea name="message" rows="3"><?= $l['status'] === 'Sold' ? 'I\'m interested in homes like this one.' : 'I\'d like more information about this home.' ?></textarea></label>
  <button class="btn btn-accent btn-block" type="submit"><?= $l['status'] === 'Sold' ? 'Find Me a Similar Home' : 'Request a Showing' ?></button>
</form>
