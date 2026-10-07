<?php
defined('GAP') || exit;
$meta = ['title' => 'Your Cart & Saved Gear', 'desc' => 'Your gear list: items in your cart and gear you saved for later.', 'canonical' => '/cart/', 'noindex' => true, 'body_class' => 'is-cart', 'scripts' => ['/assets/js/cart.js']];
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Cart', '/cart/']]) ?>
  <h1>Your gear list</h1>
  <p class="lede">Everything you've added, with typical prices. When you're ready, check each item's current price and buy it from the retailer.</p>
</div></section>
<section class="wrap cart-page">
  <div class="tabs cart-tabs" data-tabs>
    <div class="tab-list" role="tablist">
      <button role="tab" aria-selected="true" aria-controls="c-cart" id="tc-cart">Cart <span data-cart-count-inline>0</span></button>
      <button role="tab" aria-selected="false" aria-controls="c-saved" id="tc-saved">Saved <span data-saved-count-inline>0</span></button>
      <span class="tab-ink" aria-hidden="true"></span>
    </div>
    <div class="tab-panel" role="tabpanel" id="c-cart" aria-labelledby="tc-cart">
      <div class="cart-layout">
        <ul class="cart-lines" data-cart-lines></ul>
        <aside class="cart-summary">
          <h2>Summary</h2>
          <dl><dt>Items</dt><dd data-sum-items>0</dd><dt>Typical subtotal</dt><dd data-sum-total>$0</dd></dl>
          <p class="fine">Typical prices only. The retailer sets the final price, shipping and tax at checkout.</p>
          <button class="btn btn-chain full" type="button" data-checkout>Check prices &amp; buy</button>
          <button class="btn btn-outline full" type="button" data-share>Copy a shareable list link</button>
          <button class="btn btn-ghost full" type="button" data-print>Print as a checklist</button>
        </aside>
      </div>
      <div class="empty-cart" data-cart-empty hidden>
        <img src="/assets/img/kinds/case-bag.svg" alt="" width="120" height="120">
        <h2>Your cart is empty</h2>
        <p>Start with the <a href="/tools/climbing-kit-builder/">climbing kit builder</a> or <a href="/shop-all/">browse all gear</a>.</p>
      </div>
    </div>
    <div class="tab-panel" role="tabpanel" id="c-saved" aria-labelledby="tc-saved" hidden>
      <div class="grid products-grid" data-saved-grid></div>
      <p class="empty-note" data-saved-empty hidden>Nothing saved yet. Tap the heart on any product to keep it here.</p>
    </div>
  </div>
</section>
<dialog class="checkout-dialog"><form method="dialog"><button class="dialog-x" aria-label="Close">×</button></form>
  <h2>Buy from the retailer</h2>
  <p>Each item opens the retailer's page in a new tab, where you'll see today's price and can check out.</p>
  <ul class="checkout-links" data-checkout-links></ul>
</dialog>
