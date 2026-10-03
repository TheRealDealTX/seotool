<?php /** Free Claim Review popup. Opened by site.js 4 seconds after page load. */ ?>
<dialog class="popup" id="claim-popup" aria-labelledby="claim-popup-title" aria-describedby="claim-popup-desc" data-claim-popup>
  <div class="popup-inner">
    <button class="popup-close" type="button" data-popup-close aria-label="Close"><?= icon('close', 'icon') ?></button>
    <div class="popup-head">
      <span class="popup-icon"><?= icon('clipboard', 'icon') ?></span>
      <div>
        <p class="eyebrow mb-0">Free &middot; No obligation</p>
        <h2 id="claim-popup-title">Get a Free Claim Review</h2>
      </div>
    </div>
    <p id="claim-popup-desc" class="popup-text">Hail, wind, fire, or water damage? Denied or underpaid claim? Tell us what happened and a licensed McAllen public adjuster will review your options.</p>
    <?php component('claim-form', ['context' => 'Popup form', 'compact' => true]); ?>
    <button class="popup-dismiss" type="button" data-popup-close>No thanks</button>
  </div>
</dialog>
