<?php defined('BO') || exit; ?>
<div class="key-takeaways reveal">
  <h2>Key Takeaways</h2>
  <ul>
    <li>Before you learn <strong>how to adjust draw length</strong>, measure yours: <strong>wingspan &divide; 2.5</strong> is the starting point, shooting confirms it.</li>
    <li>Compound bows use one of three systems: <strong>rotating modules</strong>, <strong>swappable modules (mods)</strong>, or <strong>cam-specific draw lengths</strong> that need a new cam.</li>
    <li>Always follow the <strong>draw length chart for your exact cam</strong>, and set both cams the same on dual or hybrid systems.</li>
    <li>If a module is under string or cable tension, <strong>use a bow press</strong> or let a pro shop do it.</li>
    <li>After any change, <strong>re-check draw stops, peep height, D-loop, rest and sight</strong>. Draw length changes ripple through the whole setup.</li>
  </ul>
</div>

<p class="lead">Knowing how to adjust draw length is one of the most useful skills a compound shooter can have. Draw length decides where your anchor lands, how your bow arm sets up and whether your peep lines up without straining. When it is right, the bow feels like it was built for you. When it is wrong, you fight it on every shot.</p>

<p>The good news: on most modern bows, adjusting draw length is a simple, repeatable job once you understand which cam system you have. This Better Outdoors guide is brand-neutral. It covers how to measure, how to identify rotating modules versus module swaps versus cam-specific draw lengths, a step-by-step process, how draw stops and let-off fit in, and what to re-tune afterward. If you own a PSE, our <?= post_link('2016-pse-draw-length-adjustment', 'PSE draw length adjustment guide') ?> covers PSE charts and models in detail.</p>

<?= tool_cta('draw-length-calculator') ?>

<h2 id="h-step-zero-measure-before-adjusting-draw-length">Step Zero: Measure Before Adjusting Draw Length</h2>
<p>Adjusting draw length without a target number turns into endless guesswork. Draw length is measured from the nocking point on the string to the pivot point of the grip, plus 1.75 inches (the ATA standard). You don&rsquo;t need to measure the bow to start, though. You need to measure you.</p>
<ol class="steps">
  <li><strong>Stand against a wall</strong> with your arms straight out to the sides, palms forward, without stretching.</li>
  <li><strong>Have a helper measure</strong> from middle fingertip to middle fingertip in inches.</li>
  <li><strong>Divide by 2.5.</strong> A 71-inch wingspan gives a starting point of about 28.5 inches.</li>
</ol>
<p>That number is a baseline. Release style shifts it: shooters using a wrist-strap index release often end up a little shorter than the formula, while some handheld release shooters settle slightly longer. A <?= amz('archery draw length arrow measuring', 'draw check arrow') ?> at a pro shop gives you a second opinion, and real shooting gives you the final answer.</p>

<h3 id="h-signs-your-draw-length-is-right">Signs Your Draw Length Is Right</h3>
<ul class="checks">
  <li>The string touches your nose and the corner of your mouth without you reaching for it</li>
  <li>Your bow arm has a slight, relaxed bend at the elbow</li>
  <li>Your front shoulder stays down and relaxed at full draw</li>
  <li>Your peep lines up with your eye at a natural head position</li>
  <li>You can hold steady on target for several seconds</li>
</ul>
<p>Too long, and you&rsquo;ll feel stretched, the string may slap your forearm and your shoulder creeps up. Too short, and your anchor floats, your posture collapses and you lose back tension.</p>

<h2 id="h-identify-your-cam-system">Identify Your Cam System First</h2>
<p>This is the step most people skip, and it decides everything else. Look closely at your cams. You&rsquo;ll find a cam name or code stamped or printed on them, and usually small numbers or letters next to module holes. That cam name is what you&rsquo;ll look up on the manufacturer&rsquo;s chart.</p>
<?= data_table(
    ['Cam system', 'How draw length changes', 'Typical adjustment range', 'Press usually needed?'],
    [
        ['Rotating module', 'One module with numbered or lettered holes; you rotate it to a new position', 'Wide, often several inches in ½-inch steps', 'Usually no'],
        ['Swappable module (mod)', 'Remove the module and install a different size mod for each draw length', 'Wide, but you need the right mod for each length', 'Often yes'],
        ['Cam-specific draw length', 'The cam itself is cut for one draw length; changing it means a new cam', 'Little or none without new parts', 'Yes'],
        ['Module plus string post', 'Module sets the inch, a post or peg adds a ½-inch step', 'Varies by cam', 'Often yes for post changes'],
    ],
    'Common compound bow draw length systems'
) ?>

<h3 id="h-rotating-module-vs-module-swap">Rotating Module vs. Module Swap</h3>
<p>The rotating module vs. module swap question comes up constantly. A <strong>rotating module</strong> is a single piece bolted to the cam with several holes. You remove a screw or two, rotate it to the position your chart lists, and reinstall. Beginner, youth and many hunting bows use this design because it gives a wide range and is often press-free.</p>
<p>A <strong>module swap</strong> uses separate mods, each sized for a specific draw length (or a small range). You buy or borrow the correct mod, remove the old one and bolt in the new one. Swappable mods are common on flagship and target-oriented bows because a dedicated mod can be optimized for one draw length. The trade-off: you need the right part, and the swap often requires a press.</p>

<h3 id="h-cam-specific-draw-lengths">Cam-Specific Draw Lengths</h3>
<p>Some bows, especially older single-cam designs and certain performance cams, have a draw length that is built into the cam itself. If there is no module, or the module only fine-tunes within a narrow window, a bigger change means ordering a new cam from a dealer. Give the dealer the bow model and serial number, because cams are model-specific.</p>

<h3 id="h-brand-notes-mathews-bear-pse">Brand Notes: Mathews, Bear and PSE</h3>
<p>Every brand does it a little differently, and systems change from model to model, so treat these as orientation rather than instructions:</p>
<ul>
  <li><strong>Mathews draw length mods:</strong> Mathews uses mods to set draw length, and depending on the model that can mean a rotating mod or a separate mod for each draw length. Because Mathews sells through dealers, your pro shop can confirm which mod your bow needs. Our guide to <?= post_link('understanding-mathews-compound-bow-packages', 'Mathews compound bow packages') ?> explains how that dealer setup works.</li>
  <li><strong>Bear draw length adjustment:</strong> Bear bows use module systems that vary by cam. Many hunting and RTH models are designed for owner adjustment, but check the owner&rsquo;s manual or Bear&rsquo;s support pages for the chart that matches the cam on your bow.</li>
  <li><strong>PSE draw length chart:</strong> PSE publishes a chart for each cam system. There is no single chart for every PSE bow. See our <?= post_link('2016-pse-draw-length-adjustment', 'PSE-specific guide') ?> for how to read one.</li>
</ul>
<?= callout('note', 'Use the chart, not a forum post', 'Module positions differ between cams, even within one brand and one model year. The only reliable source for your settings is the manufacturer chart for the cam named on your bow, or an authorized dealer.') ?>

<h2 id="h-how-to-change-draw-length-on-a-compound-bow">How to Change Draw Length on a Compound Bow: Step by Step</h2>
<p>Here is the general process for how to change draw length on a compound bow with a module system. Work slowly, and photograph everything before you touch it.</p>

<h3 id="h-what-you-ll-need">What You&rsquo;ll Need</h3>
<ul>
  <li>Correct-size hex keys; a <?= amz('archery allen wrench set bow tool', 'dedicated archery hex key set') ?> helps prevent stripped screws</li>
  <li>The manufacturer chart for your cam</li>
  <li>A towel or padded work surface</li>
  <li>A phone to photograph current settings</li>
  <li>A bow press, if your system needs one</li>
  <li>A draw weight scale to check the result</li>
</ul>

<h3 id="h-step-1-record-your-current-settings">Step 1: Record Your Current Settings</h3>
<p>Write down the current module position (and draw stop and string post position, if your cam has them) on every cam. Take close-up photos of both cams. If anything goes wrong, you can return to a known starting point.</p>

<h3 id="h-step-2-find-the-target-position-on-the-chart">Step 2: Find the Target Position on the Chart</h3>
<p>Look up your target draw length on the chart for your cam. Note the module position or mod size, any string post setting and any draw stop position listed. Move ½ inch at a time if you&rsquo;re fine-tuning; bigger jumps are fine when you know the target from a fitting.</p>

<h3 id="h-step-3-check-whether-the-module-is-loaded">Step 3: Check Whether the Module Is Loaded</h3>
<p>Try loosening a module screw a quarter turn. If it turns freely and the string and cables stay seated, the module isn&rsquo;t carrying load. If the screw binds or the module wants to shift under tension, stop. You need a bow press.</p>
<?= callout('warn', 'Never force a loaded module', 'Removing a load-bearing module without a press can let the string or cables jump the track, damage the cam or cause injury. When in doubt, treat the change as press-required.') ?>

<h3 id="h-step-4-move-or-swap-the-module">Step 4: Move or Swap the Module</h3>
<p>For a rotating module, remove the screws, rotate the module so the chart&rsquo;s position lines up with the mounting hole, and reinstall. For a module swap, press the bow if required, remove the old mod and install the new one in the orientation the manual shows.</p>

<h3 id="h-step-5-match-every-cam">Step 5: Match Every Cam</h3>
<p>On dual-cam, hybrid and binary systems, set both cams to the same position. A mismatch throws off cam timing, which shows up as a lumpy draw cycle, a soft or uneven back wall and inconsistent arrow flight. Single-cam bows only have one module to move, but check the idler for any matching setting the manual lists.</p>

<h3 id="h-step-6-tighten-and-test-draw">Step 6: Tighten and Test-Draw</h3>
<p>Tighten screws snug, not cranked; aluminum threads strip easily. Use thread locker only if the manufacturer allows it. Draw the bow slowly several times, listening for clicks or creaks and watching that the string and cables track cleanly.</p>

<h2 id="h-draw-stops-and-let-off">Draw Stops, Let-Off and Draw Length</h2>
<p>Draw stops are small pegs or adjustable posts that set where the cam stops rotating. On many cams they are tied to draw length, and on some they also set let-off. That means a draw length change can quietly change how your back wall feels.</p>
<ul>
  <li><strong>Draw stops tied to modules:</strong> Some modules carry the draw stop, so moving the module moves the stop. Others have a separate stop that must be moved to a matching position.</li>
  <li><strong>Adjustable let-off:</strong> Cams with let-off settings often use the draw stop position to control it. Moving the stop can change both let-off and the effective draw length slightly.</li>
  <li><strong>Timing the stops:</strong> On dual-stop systems, both stops should hit the cables or limbs at the same moment at full draw. A pro shop can check this with a draw board.</li>
</ul>
<p>Change one variable at a time: set draw length first, shoot it, then adjust let-off if you need to.</p>

<h2 id="h-adjusting-draw-length-then-re-tuning">After Adjusting Draw Length: Re-Tune the Bow</h2>
<p>Adjusting draw length changes where your eye, anchor and arrow sit. Plan to re-tune these items afterward:</p>
<?= data_table(
    ['Item', 'Why it changes', 'What to do'],
    [
        ['Peep sight', 'Your anchor moves, so the peep no longer meets your eye', 'Move the peep up or down the string until it lines up at a natural head position'],
        ['D-loop', 'Loop length acts like a tiny draw length change', 'Retie or adjust so your release hand anchors comfortably'],
        ['Draw weight', 'Some cams change peak or holding weight with draw length', 'Check with a scale and adjust limb bolts equally'],
        ['Cam timing', 'Module changes can expose a timing issue', 'Check both cams roll over together; a shop can fix with cable twists'],
        ['Arrow rest', 'Nock travel can shift slightly', 'Re-check center shot and paper tune'],
        ['Sight', 'Arrow speed changes, roughly 10 fps per inch of draw by common rule of thumb', 'Re-sight every pin or re-calibrate your slider tape'],
    ],
    'What to re-check after a draw length change'
) ?>
<p>Your arrows may also be affected. A longer draw length stores more energy, which can call for a stiffer spine. Use our <a href="/tools/arrow-speed-calculator/">arrow speed calculator</a> to estimate the speed change at your new setting.</p>

<?= product_grid([
    ['name' => 'Portable Bow Press', 'q' => 'portable bow press compound', 'icon' => 'fa-screwdriver-wrench', 'badge' => 'Most useful', 'blurb' => 'Relieves limb tension so you can swap loaded modules, move peeps and change strings safely.', 'pros' => ['Fits most modern split-limb bows', 'Portable for camp or the truck']],
    ['name' => 'Bow Draw Weight Scale', 'q' => 'bow draw weight scale digital', 'icon' => 'fa-weight-hanging', 'blurb' => 'Confirms peak draw weight after a draw length change so you know exactly what you&rsquo;re pulling.', 'pros' => ['Catches uneven limb bolt settings', 'Quick check before hunting season']],
    ['name' => 'D-Loop Pliers and Loop Material', 'q' => 'd loop pliers bow string loop material', 'icon' => 'fa-link', 'blurb' => 'Tie a new D-loop at the right length to fine-tune fit after you change draw length.', 'pros' => ['Inexpensive', 'Fine adjustments in minutes']],
], 'Tools for adjusting draw length at home') ?>

<h2 id="h-bow-press-for-draw-length">Do You Need a Bow Press for Draw Length?</h2>
<p>It depends on your cam. Many rotating-module bows are designed for press-free changes because the module isn&rsquo;t carrying load. Swappable mods, string post changes and new cams usually need a press. A quick rule: if your manual says press-free, and the screw turns freely, you&rsquo;re fine. If not, press it.</p>
<p>A <?= amz('portable bow press compound', 'portable bow press') ?> is worth owning if you work on your own bows often. If you only adjust once, a pro shop will usually do it quickly.</p>

<h2 id="h-when-to-use-a-pro-shop">When to Use a Pro Shop</h2>
<p>At Better Outdoors we recommend a pro shop when:</p>
<ul>
  <li>Your bow needs a press you don&rsquo;t have, or a new mod or cam</li>
  <li>You can&rsquo;t find the chart for your cam</li>
  <li>Cam timing or draw stops look uneven after the change</li>
  <li>The draw cycle feels rough, noisy or inconsistent</li>
  <li>You want your draw length verified on a draw board with a coach watching your form</li>
</ul>
<p>A good shop can measure your draw length, set the bow, re-time the cams, move the peep and paper tune in one visit.</p>

<h2 id="h-common-mistakes">Common Mistakes When You Adjust Draw Length</h2>
<ul>
  <li><strong>Adjusting only one cam</strong> on a dual or hybrid system</li>
  <li><strong>Forgetting the draw stops</strong>, leaving a soft or uneven wall</li>
  <li><strong>Judging by feel in the living room</strong> instead of shooting groups</li>
  <li><strong>Leaving the peep where it was</strong> and craning your neck to find it</li>
  <li><strong>Guessing module positions</strong> instead of using the chart</li>
</ul>
<p>Shoot at least 30 arrows at a new setting before you decide. Compare groups at 20 yards and pay attention to how fast you can settle the pin.</p>

<h2 id="h-final-thoughts">Final Thoughts on How to Adjust Draw Length</h2>
<p>Learning how to adjust draw length comes down to three habits: measure honestly, follow the chart for your exact cam, and re-tune everything the change touches. Do that, and a quick module move turns into better posture, a steadier hold and tighter groups.</p>

<?= faq_block([
    'How do I adjust draw length on a compound bow?' => 'Identify your cam system, find your target draw length on the manufacturer chart for that cam, then move or swap the module on every cam to the listed position. Re-check draw stops, peep height, D-loop and sight afterward.',
    'How do I know what draw length I need?' => 'Measure your wingspan fingertip to fingertip and divide by 2.5 for a starting point, then confirm by shooting. Correct draw length lets you anchor naturally with a slight bend in your bow arm.',
    'What is the difference between a rotating module and a module swap?' => 'A rotating module is one piece with several positions that you rotate to change draw length. A module swap means removing the module and installing a different-size mod for each draw length.',
    'Do I need a bow press to adjust draw length?' => 'Not always. Many rotating-module bows can be adjusted press-free. If the module is under string or cable tension, or you are swapping mods or cams, use a bow press.',
    'How do Mathews draw length mods work?' => 'Mathews bows set draw length with mods. Depending on the model, that may be a rotating mod or a separate mod for each draw length. Your Mathews dealer can confirm which mod your bow needs.',
    'Does adjusting draw length change draw weight?' => 'It can. Some cams change peak or holding weight when draw length changes. Check with a draw weight scale and adjust both limb bolts equally if needed.',
    'Where do I find a PSE draw length chart?' => 'PSE publishes a chart for each cam system on its website and in the owner&rsquo;s manual. Our PSE draw length adjustment guide explains how to read one.',
    'How much does draw length affect arrow speed?' => 'A common rule of thumb is about 10 fps per inch of draw length. Re-sight your pins after any change.',
    'Can every compound bow change draw length?' => 'No. Some bows have cam-specific draw lengths, so a large change requires a new cam. Most modern hunting and beginner bows use modules that allow a range of adjustment.',
]) ?>
