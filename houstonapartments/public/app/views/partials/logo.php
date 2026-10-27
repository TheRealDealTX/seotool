<?php
// Brand mark: teal map pin with a coral roofline + "Houston Apartments" wordmark.
defined('HA_ROOT') || exit;
$logoClass = $logoClass ?? '';
?>
<span class="logo <?= e($logoClass) ?>">
  <svg class="logo-mark" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true">
    <rect width="40" height="40" rx="12" fill="#0f766e"/>
    <path d="M20 7.5c-5.6 0-10 4.3-10 9.8C10 24.6 20 33 20 33s10-8.4 10-15.7c0-5.5-4.4-9.8-10-9.8z" fill="#fff"/>
    <path d="M14.6 18.6 20 13.9l5.4 4.7" fill="none" stroke="#ff6b4a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="16.6" y="18.3" width="6.8" height="6.2" rx="1" fill="#0f766e"/>
    <rect x="19" y="21" width="2" height="3.5" fill="#fff"/>
  </svg>
  <span class="logo-word"><b>Houston</b><i>Apartments</i></span>
</span>
