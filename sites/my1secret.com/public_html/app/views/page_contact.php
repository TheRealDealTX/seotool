<?php defined('M1S') || exit; ?>
<article class="narrow prose">
  <h1>Contact Us</h1>
  <?php if (cfg('contact_email')): ?>
    <p>Email the My 1 Secret team at <a href="mailto:<?= e(cfg('contact_email')) ?>"><?= e(cfg('contact_email')) ?></a>. We read every message.</p>
  <?php endif; ?>
  <ul>
    <li><strong>Questions about renting, insurance claims or home life?</strong> You'll get faster, better answers by <a href="/submit/">posting in the community</a>.</li>
    <li><strong>Something breaks the rules?</strong> Use the <em>Report</em> link under the post or comment so a moderator sees it right away.</li>
    <li><strong>Account or privacy requests?</strong> <?= cfg('contact_email') ? 'Email us from the address on your account.' : 'Post in the community and a team member will follow up.' ?></li>
  </ul>
</article>
