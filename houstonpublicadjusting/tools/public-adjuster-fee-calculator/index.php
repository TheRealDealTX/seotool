<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'public-adjuster-fee-calculator',
    'title' => 'Public Adjuster Fee Calculator: Is Hiring Worth It in Texas?',
    'desc' => 'Public adjuster fee calculator for Houston and Texas claims. Compare your net payout with and without a public adjuster and find your break-even settlement.',
    'h1' => 'Public Adjuster Fee Calculator',
    'lede' => 'Texas caps public adjuster fees at 10% of the settlement. Plug in the insurer&rsquo;s offer and a realistic settlement to see exactly what you would keep either way.',
    'form' => '
<form data-tool="fee" data-out="out-fee" class="tool-grid">
  <label>Insurance company&rsquo;s offer ($)<input name="offer" inputmode="decimal" value="18000"><span class="hint">Enter 0 if the claim was denied</span></label>
  <label>Expected settlement with a public adjuster ($)<input name="with_pa" inputmode="decimal" value="41000"><span class="hint">Your contractor&rsquo;s estimate is a reasonable starting point</span></label>
  <label>Public adjuster fee (%)<input name="fee_pct" inputmode="decimal" value="10"><span class="hint">Texas maximum is 10% (Ins. Code &sect;4102.104)</span></label>
  <label>Fee is charged on<select name="basis"><option value="total">The total settlement</option><option value="increase">Only the increase over the offer</option></select><span class="hint">Read your contract; terms vary</span></label>
</form>
<div class="tool-result" id="out-fee" aria-live="polite"></div>',
    'prose' => '
<h2>How public adjuster fees work in Texas</h2>
<p>A public adjuster in Houston, TX is paid on contingency: a percentage of the claim money recovered, agreed in a written contract before any work starts. Texas Insurance Code &sect;4102.104 limits that fee to <strong>10% of the settlement</strong>. There is no hourly bill and nothing upfront &mdash; if nothing is recovered, nothing is owed.</p>
<p>The question is never just &ldquo;what does the fee cost?&rdquo; It is &ldquo;what do I keep?&rdquo; If representation moves a settlement from $18,000 to $41,000, a 10% fee is $4,100 and you still keep $36,900 &mdash; more than double the original offer. If the carrier&rsquo;s offer is already fair, hiring may not make sense, and an honest adjuster will tell you that.</p>
<h2>When hiring a public adjuster usually pays off</h2>
<ul class="checklist">
  <li>The claim was denied or the offer is far below contractor bids</li>
  <li>The loss is large or complex: hurricane, fire, multi-room water, commercial</li>
  <li>The carrier keeps requesting documents, changing adjusters or delaying</li>
  <li>You don&rsquo;t have time to manage estimates, inspections and negotiations yourself</li>
</ul>
<p>Read more in <a href="/are-public-adjusters-worth-it/">Are Public Adjusters Worth It?</a></p>',
    'faqs' => [
        ['What is the maximum public adjuster fee in Texas?', 'Texas law caps a public adjuster’s compensation at 10% of the amount of the insurance settlement on the claim (Texas Insurance Code §4102.104).'],
        ['Do I pay a public adjuster if my claim gets nothing?', 'No. Public adjusters in Texas work on contingency. If no money is recovered, no fee is owed.'],
        ['Can a public adjuster take a fee on money I already received?', 'It depends on the contract. Many adjusters charge only on new money recovered after they are hired. Ask before you sign and get it in writing.'],
    ],
]);
