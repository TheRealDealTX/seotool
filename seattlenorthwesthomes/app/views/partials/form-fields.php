<?php defined('SNW') || (http_response_code(404) && exit);
/* Shared name/email/phone block. */ ?>
  <div class="grid-2">
    <label>First name<input type="text" name="first_name" autocomplete="given-name" required></label>
    <label>Last name<input type="text" name="last_name" autocomplete="family-name"></label>
    <label>Email<input type="email" name="email" autocomplete="email" required></label>
    <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
  </div>
