<?php defined('BO') || exit; ?>
<div class="tool-wrap" data-tool="bow-finder">
  <div class="panel reveal" id="bf-panel">
    <div class="quiz-progress" aria-hidden="true"><span id="bf-bar"></span></div>
    <div id="bf-q"></div>
    <p class="hint" style="margin-top:18px;font-size:.85rem;color:var(--muted)">Question <span id="bf-n">1</span> of 6 &middot; <button type="button" id="bf-back" class="icon-btn" style="width:auto;height:auto;font-size:.85rem;color:var(--teal)" hidden>&larr; Back</button></p>
  </div>
  <div class="result reveal reveal-d2" aria-live="polite">
    <h2 style="font-size:1.3rem">Your best matches</h2>
    <p id="bf-intro">Answer the questions and the Better Outdoors bow finder will rank the compound bows we&rsquo;ve reviewed for you.</p>
    <div id="bf-results"></div>
    <button type="button" class="btn btn-orange" id="bf-restart" hidden style="margin-top:18px"><i class="fa-solid fa-rotate-left" aria-hidden="true"></i> Start Over</button>
  </div>
</div>
<script type="application/json" id="bf-data"><?= json_encode([
    ['slug' => 'mathews-lift-29-5', 'name' => 'Mathews Lift 29.5', 'img' => img_url($POSTS['mathews-lift-29-5']['thumb']), 'dl' => [24.5, 30], 'tags' => ['premium', 'compact', 'quiet', 'speed', 'stand', 'spot', 'experienced', 'bare'], 'note' => '29.5" ATA, up to 348 fps, 55–80 lb'],
    ['slug' => 'mathews-prima-level-1-package', 'name' => 'Mathews Prima', 'img' => img_url($POSTS['mathews-prima-level-1-package']['thumb']), 'dl' => [21.5, 27.5], 'tags' => ['premium', 'compact', 'light', 'smaller', 'short', 'quiet', 'stand', 'package', 'beginner'], 'note' => '30" ATA, 21.5–27.5" draw, 40–60 lb'],
    ['slug' => 'bear-archery-alaskan-xt-rth-compound-bow', 'name' => 'Bear Alaskan XT RTH', 'img' => img_url($POSTS['bear-archery-alaskan-xt-rth-compound-bow']['thumb']), 'dl' => [25, 30], 'tags' => ['value', 'package', 'forgiving', 'stable', 'spot', 'target', 'light', 'beginner'], 'note' => '33" ATA, 335 fps, ready to hunt'],
    ['slug' => 'bear-archery-whitetail-maxx-rth-compound-bow', 'name' => 'Bear Whitetail Maxx RTH', 'img' => img_url($POSTS['bear-archery-whitetail-maxx-rth-compound-bow']['thumb']), 'dl' => [26, 30], 'tags' => ['value', 'package', 'stand', 'speed', 'beginner', 'compact'], 'note' => '31" ATA, up to 339 fps, ready to hunt'],
    ['slug' => 'bear-archery-persist-compound-bow', 'name' => 'Bear Persist', 'img' => img_url($POSTS['bear-archery-persist-compound-bow']['thumb']), 'dl' => [25, 30.5], 'tags' => ['mid', 'speed', 'adjustable', 'stand', 'spot', 'experienced', 'bare', 'forgiving'], 'note' => '31" or 33" ATA, 340 fps, 75–90% let-off'],
    ['slug' => '2018-pse-evolve-28', 'name' => 'PSE Evolve 28 (used)', 'img' => img_url($POSTS['2018-pse-evolve-28']['thumb']), 'dl' => [24.5, 30], 'tags' => ['value', 'compact', 'blind', 'stand', 'forgiving', 'used', 'experienced'], 'note' => '28" ATA, 7" brace height, 335 fps'],
], JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) ?></script>

<div class="tool-content prose">
  <h2 id="how-we-match">How the Bow Finder Matches You</h2>
  <p>The Better Outdoors bow finder scores every compound bow we have reviewed against your answers. Draw length is a hard filter: a bow that can&rsquo;t reach your draw length is ruled out no matter how good it is. After that, points go to bows that fit your budget, hunting style, build and priorities. Short axle-to-axle bows score higher for treestands and ground blinds, longer bows for open-country stability, and ready-to-hunt packages for first-time buyers.</p>
  <?= data_table(['If you value…', 'Look for…'], [
      ['Forgiveness', 'Longer axle-to-axle (32"+) and a brace height of 6.5" or more'],
      ['Maneuverability in a blind', 'Axle-to-axle of 28–31"'],
      ['Flat trajectory', 'Higher IBO rating and the longest draw length that still fits you'],
      ['Simple setup', 'An RTH (ready-to-hunt) package with sight, rest and quiver installed'],
      ['A light carry', 'Mass weight under about 4 lb'],
  ], 'What bow specs mean for you') ?>
  <p>Not sure of your draw length? Start with the <a href="/tools/draw-length-calculator/">draw length calculator</a>. Weighing a package against a bare bow? Read <?= post_link('understanding-mathews-compound-bow-packages', 'our guide to Mathews bow packages') ?>.</p>
  <?= faq_block([
      'What compound bow should a beginner buy?' => 'Most beginners do best with a ready-to-hunt package that fits their draw length, with an adjustable draw weight they can pull comfortably. A forgiving axle-to-axle length of 31 to 33 inches and a brace height near 6.5 inches help consistency.',
      'Is a shorter or longer bow better for hunting?' => 'Shorter bows (28 to 31 inches) are easier to handle in treestands and blinds. Longer bows (32 inches and up) tend to hold steadier and be more forgiving at long range.',
      'How important is draw length when choosing a bow?' => 'It is the most important fit factor. A bow must be able to adjust to your draw length, so check the draw length range before anything else.',
  ], 'faq') ?>
</div>
