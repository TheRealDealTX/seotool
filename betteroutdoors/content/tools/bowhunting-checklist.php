<?php defined('BO') || exit;
$lists = [
    ['Bow & Arrows', 'fa-bullseye', [
        ['Bow, tuned and sighted in', null], ['Arrows with broadheads (sharpened, spun-tested)', 'fixed blade broadheads 100 grain'], ['Spare arrows and practice points', null],
        ['Release aid + backup release', 'index finger bow release aid'], ['Bow sling or hanger', 'compound bow sling'], ['Allen key multitool', 'archery allen wrench set bow tool'], ['Broadhead wrench', null],
    ]],
    ['Treestand & Blind', 'fa-tree', [
        ['Full-body safety harness', 'treestand safety harness'], ['Lifeline / tree strap', 'treestand lifeline rope'], ['Bow hoist rope', 'bow hoist rope'], ['Climbing sticks or ladder check', null],
        ['Seat cushion', null], ['Pruning shears / hand saw', 'folding pruning saw hunting'], ['Ground blind & stakes (if used)', null],
    ]],
    ['Clothing & Scent', 'fa-shirt', [
        ['Base layers (merino or synthetic)', null], ['Insulating mid layer', null], ['Rain / wind shell', null], ['Gloves and face mask', null],
        ['Warm hat', null], ['Scent-control spray', 'scent eliminator spray hunting'], ['Boots (rubber for scent control)', null],
    ]],
    ['Optics & Navigation', 'fa-binoculars', [
        ['Rangefinder with angle compensation', 'archery rangefinder angle compensation'], ['Binoculars', 'hunting binoculars 10x42'], ['Headlamp + spare batteries', 'red light headlamp hunting'],
        ['Phone with offline maps', null], ['Trail markers / reflective tacks', 'reflective trail markers hunting'], ['Wind checker powder', 'wind checker hunting'],
    ]],
    ['Recovery & Field Dressing', 'fa-kit-medical', [
        ['Fixed-blade or replaceable-blade knife', 'replaceable blade hunting knife'], ['Field dressing gloves', null], ['Game bags', 'game bags elk deer'], ['Drag rope or cart', null],
        ['Blood-tracking light', 'blood tracking light hunting'], ['Tags, license and zip ties', null], ['First aid kit', 'hunting first aid kit'],
    ]],
    ['Pack Essentials', 'fa-person-hiking', [
        ['Water and snacks', null], ['Hand warmers', 'hand warmers'], ['Toilet paper / wipes', null], ['Fire starter', null],
        ['Small multitool', null], ['Grunt call / rattle bag', 'deer grunt call'], ['Trash bag', null],
    ]],
];
$n = 0;
?>
<div class="panel reveal" data-tool="checklist" style="margin-top:-60px;position:relative;z-index:2">
  <div class="check-meter">
    <strong id="cl-count">0 / 0 packed</strong>
    <div class="bar" aria-hidden="true"><span id="cl-bar"></span></div>
    <div class="btn-row no-print">
      <button type="button" class="btn btn-teal" id="cl-print"><i class="fa-solid fa-print" aria-hidden="true"></i> Print</button>
      <button type="button" class="btn btn-outline" id="cl-reset"><i class="fa-solid fa-rotate-left" aria-hidden="true"></i> Reset</button>
    </div>
  </div>
  <div class="check-groups">
<?php foreach ($lists as [$title, $icon, $items]): ?>
    <div class="check-group">
      <h3><i class="fa-solid <?= e($icon) ?>" aria-hidden="true"></i> <?= e($title) ?></h3>
<?php foreach ($items as [$label, $q]): $n++; ?>
      <label><input type="checkbox" data-id="i<?= $n ?>"><span><?= e($label) ?></span><?php if ($q): ?><a class="amz-mini no-print" href="<?= e(amz_url($q)) ?>" target="_blank" rel="nofollow sponsored noopener">Shop</a><?php endif; ?></label>
<?php endforeach; ?>
    </div>
<?php endforeach; ?>
  </div>
  <p class="aff-note">Your ticks are saved in this browser only. &ldquo;Shop&rdquo; links go to Amazon; as an Amazon Associate, Better Outdoors earns from qualifying purchases.</p>
</div>

<div class="tool-content prose">
  <h2 id="how-to-use">How to Use This Bowhunting Checklist</h2>
  <p>Run through the list the night before every hunt. Ticks save automatically in your browser, so you can pack over several evenings and pick up where you left off. Hit print for a paper copy to keep in your truck. The Better Outdoors team built the list around the gear that most often gets forgotten: a backup release, a bow hoist rope, spare headlamp batteries and tracking light.</p>
  <h2 id="non-negotiables">The Non-Negotiables</h2>
  <ul class="checks">
    <li><strong>A full-body harness</strong> attached from the moment you leave the ground. Falls from treestands are among the leading causes of hunting injuries.</li>
    <li><strong>Sharp, spin-tested broadheads</strong> that fly with your field points.</li>
    <li><strong>A rangefinder</strong>: misjudged yardage is the most common reason for a miss.</li>
    <li><strong>Your license and tags</strong>, plus anything your state requires for tagging and reporting.</li>
  </ul>
  <?= callout('tip', 'Pre-season tune-up', 'Two weeks before opening day, check your draw length and sight tape, shoot your broadheads and re-wax your string. Our <a href="/2016-pse-draw-length-adjustment/">draw length guide</a> and <a href="/tools/kinetic-energy-calculator/">kinetic energy calculator</a> help you confirm your setup.') ?>
  <?= faq_block([
      'What do I need for my first bowhunt?' => 'At minimum: a tuned bow, arrows with sharp broadheads, a release aid, a rangefinder, a safety harness if you hunt from a treestand, layered clothing, a headlamp, a knife, your license and tags, water and a first aid kit.',
      'What is the most commonly forgotten bowhunting gear?' => 'Release aids, headlamp batteries, bow hoist ropes, tags and tracking lights top the list. A written checklist solves most of it.',
      'Should I carry a backup release?' => 'Yes. A release is small, easy to drop from a treestand and impossible to replace mid-hunt. A spare in your pack can save your season.',
  ], 'faq') ?>
</div>
