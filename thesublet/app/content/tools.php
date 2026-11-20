<?php defined('APP') || exit;

return [
'cost-calculator' => [
    'lead' => 'See what a sublet really costs — upfront and over the whole stay — including a prorated first month, deposit, fees and utilities.',
    'meta' => 'Free sublet cost calculator: add rent, deposit, fees and utilities, prorate a mid-month move-in, and see your upfront and total cost.',
    'widget' => <<<'HTML'
<form class="calc" data-calc="cost" onsubmit="return false">
  <div class="row3">
    <label>Monthly rent ($)<input type="number" name="rent" value="1400" min="0" step="10"></label>
    <label>Move-in date<input type="date" name="start"></label>
    <label>Move-out date<input type="date" name="end"></label>
  </div>
  <div class="row3">
    <label>Security deposit ($)<input type="number" name="deposit" value="1400" min="0" step="10"></label>
    <label>Utilities / month ($) <small>0 if included</small><input type="number" name="util" value="0" min="0" step="5"></label>
    <label>One-time fees ($) <small>cleaning, application, keys</small><input type="number" name="fees" value="0" min="0" step="5"></label>
  </div>
  <div class="row3">
    <label>Other monthly costs ($) <small>parking, internet</small><input type="number" name="other" value="0" min="0" step="5"></label>
    <label>Proration method<select name="method"><option value="days">Actual days in month</option><option value="30">30-day month</option><option value="365">Daily rate (365-day year)</option></select></label>
    <label class="chk"><input type="checkbox" name="refund" checked> Expect deposit back</label>
  </div>
</form>
<div class="calc-out" data-out="cost" aria-live="polite"></div>
HTML,
    'body' => <<<'HTML'
<h2>How the calculator works</h2>
<p>Sublets rarely start on the first of the month, so the first and last months are usually partial. The calculator splits your stay into calendar months, charges full rent for every complete month and prorates the partial ones using the method you choose. It then adds utilities and other monthly costs for the same period, plus one-time fees.</p>
<p><strong>Upfront cost</strong> is what you typically hand over before you get the keys: the first (possibly prorated) month plus the deposit and one-time fees. <strong>Total cost of the stay</strong> is everything you will spend; if you expect your deposit back, it is excluded from the total, but you still need the cash on day one.</p>
<h2>Tips to keep the cost down</h2>
<ul><li>Ask whether utilities and Wi-Fi are included — it is common in furnished sublets and simplifies budgeting.</li><li>Agree in writing how the deposit is held and when it is returned. See our guide to <a href="/blog/security-deposits-for-sublets/">security deposits for sublets</a>.</li><li>Never pay a deposit before you have toured (in person or by live video) and signed a written sublease.</li></ul>
HTML,
    'faqs' => [
        ['q' => 'What is a typical security deposit for a sublet?', 'a' => 'It varies by host, city and state law. Many hosts ask for something in the range of half a month to one month of rent; some states cap deposits. Always get the deposit terms in writing.'],
        ['q' => 'Which proration method is correct?', 'a' => 'Whichever your sublease says. Many landlords use the actual number of days in the month; others use a 30-day month or a daily rate based on a 365-day year. The differences are usually small, but agree on one up front.'],
        ['q' => 'Does the calculator store my numbers?', 'a' => 'No. All calculations run in your browser and nothing is sent to The Sublet.'],
    ],
    'amazon' => [['label' => 'Packing cubes', 'query' => 'packing cubes set', 'icon' => '🧳'], ['label' => 'Luggage scale', 'query' => 'digital luggage scale', 'icon' => '⚖️'], ['label' => 'Bill organizer folder', 'query' => 'accordion file organizer bills', 'icon' => '🗂️']],
],

'compare' => [
    'lead' => 'Put a sublet, a short-term lease and an extended-stay hotel side by side for the length of your stay — including the costs people forget.',
    'meta' => 'Compare the total cost of a sublet, a short-term lease and an extended-stay hotel for your stay length, with fees, utilities and furniture included.',
    'widget' => <<<'HTML'
<form class="calc" data-calc="compare" onsubmit="return false">
  <label>Length of stay (months)<input type="number" name="months" value="3" min="1" max="12" step="1"></label>
  <div class="cmp3">
    <fieldset><legend>Sublet</legend>
      <label>Monthly rent ($)<input type="number" name="s_rent" value="1500" min="0" step="10"></label>
      <label>Utilities / month ($)<input type="number" name="s_util" value="0" min="0" step="5"></label>
      <label>One-time fees ($)<input type="number" name="s_fees" value="0" min="0" step="10"></label>
    </fieldset>
    <fieldset><legend>Short-term lease</legend>
      <label>Monthly rent ($)<input type="number" name="l_rent" value="1700" min="0" step="10"></label>
      <label>Utilities + internet / month ($)<input type="number" name="l_util" value="180" min="0" step="5"></label>
      <label>Furniture rental / month ($)<input type="number" name="l_furn" value="150" min="0" step="10"></label>
      <label>Application, broker &amp; setup fees ($)<input type="number" name="l_fees" value="300" min="0" step="10"></label>
    </fieldset>
    <fieldset><legend>Extended-stay hotel</legend>
      <label>Nightly rate ($)<input type="number" name="h_rate" value="95" min="0" step="1"></label>
      <label>Taxes &amp; fees (%)<input type="number" name="h_tax" value="12" min="0" max="40" step="0.5"></label>
      <label>Extra food cost / month ($) <small>small kitchenette</small><input type="number" name="h_food" value="100" min="0" step="10"></label>
    </fieldset>
  </div>
</form>
<div class="calc-out" data-out="compare" aria-live="polite"></div>
HTML,
    'body' => <<<'HTML'
<h2>What each option usually looks like</h2>
<p><strong>Sublets</strong> are usually furnished, often include utilities, and can match odd dates — but you depend on the original tenant’s lease and landlord, so confirm subletting is allowed. <strong>Short-term leases</strong> (often 3–6 months) come straight from a landlord and are usually unfurnished, with premium rent for the short term, setup costs and utilities in your name. <strong>Extended-stay hotels</strong> are the most flexible — no lease, housekeeping, easy cancellation — but nightly rates add up and lodging taxes may apply (some places exempt longer stays; check locally).</p>
<p>The defaults above are placeholders, not market data. Replace them with real quotes for your city. For a deeper look, read <a href="/blog/sublet-vs-extended-stay-hotel/">sublet vs. extended-stay hotel</a>.</p>
HTML,
    'faqs' => [
        ['q' => 'Is a sublet always cheaper than a hotel?', 'a' => 'Not always, but for stays of a month or more a furnished sublet is often cheaper per month than paying nightly. Hotels win on flexibility and services, so compare real quotes for your dates.'],
        ['q' => 'Why include furniture rental for a lease?', 'a' => 'Most short-term leases are unfurnished. If you would need to rent or buy furniture for a few months, that cost belongs in the comparison.'],
        ['q' => 'Do hotels charge tax on long stays?', 'a' => 'Lodging taxes and exemptions for longer stays vary by state and city. Ask the hotel how taxes apply to your full stay.'],
    ],
],

'proration' => [
    'lead' => 'Moving in mid-month? Calculate the prorated rent for a partial first or last month using three common methods.',
    'meta' => 'Free rent proration calculator for move-in or move-out dates: compare actual-days, 30-day and 365-day daily-rate methods instantly.',
    'widget' => <<<'HTML'
<form class="calc" data-calc="proration" onsubmit="return false">
  <div class="row3">
    <label>Monthly rent ($)<input type="number" name="rent" value="1500" min="0" step="10"></label>
    <label>Date<input type="date" name="date"></label>
    <label>This is my<select name="kind"><option value="in">Move-in date (pay to month end)</option><option value="out">Move-out date (pay from month start)</option></select></label>
  </div>
</form>
<div class="calc-out" data-out="proration" aria-live="polite"></div>
HTML,
    'body' => <<<'HTML'
<h2>Three ways to prorate rent</h2>
<ol><li><strong>Actual days in the month:</strong> monthly rent ÷ days in that month × days you occupy. February days cost more than July days.</li><li><strong>30-day month (banker’s month):</strong> monthly rent ÷ 30 × days occupied, regardless of the month.</li><li><strong>Daily rate from a 365-day year:</strong> monthly rent × 12 ÷ 365 × days occupied.</li></ol>
<p>The move-in day and move-out day are both counted here as occupied days. Put whichever method you agree on into your <a href="/blog/sublease-agreement-what-to-include/">sublease agreement</a> so nobody is surprised.</p>
HTML,
    'faqs' => [
        ['q' => 'Is the move-in day counted?', 'a' => 'In this calculator, yes — the day you get the keys counts as a paid day. Some agreements differ, so check yours.'],
        ['q' => 'Which method do landlords use most?', 'a' => 'It varies. The actual-days method is very common, but the agreement is what matters.'],
    ],
],

'packing-checklist' => [
    'lead' => 'Tick items off as you pack for a furnished sublet. Your list saves automatically on this device, so you can come back to it.',
    'meta' => 'Free packing checklist for a furnished sublet or short-term rental. Tick items, add your own, and it saves on your device automatically.',
    'widget' => <<<'HTML'
<div class="checklist" data-checklist>
  <div class="cl-bar"><span data-cl-progress>0 of 0 packed</span><span><button type="button" class="btn btn-sm btn-ghost" data-cl-print>Print</button> <button type="button" class="btn btn-sm btn-ghost" data-cl-reset>Reset</button></span></div>
  <div class="cl-groups" data-cl-groups></div>
  <form class="cl-add" data-cl-add><label>Add your own item<input type="text" name="item" maxlength="80" placeholder="e.g. Hospital badge holder"></label><button class="btn btn-sm" type="submit">Add</button></form>
</div>
HTML,
    'body' => <<<'HTML'
<h2>Packing for a furnished place</h2>
<p>“Furnished” usually means bed, dresser, table and basic kitchen gear — but it varies. Before you pack, ask the host exactly what is included: sheets and towels, pots and pans, a desk, hangers, a vacuum. Bring the small things that make a borrowed space feel like yours, and leave bulky items that are easy to borrow or buy locally.</p>
<p>Read our full guide on <a href="/blog/what-to-pack-for-a-sublet/">what to pack for a sublet</a>.</p>
HTML,
    'faqs' => [
        ['q' => 'Where is my checklist saved?', 'a' => 'In your browser’s local storage on this device. It is not sent to The Sublet, and clearing your browser data will erase it.'],
        ['q' => 'Should I bring my own sheets?', 'a' => 'Ask your host. Many furnished sublets include linens, but bringing one set of sheets and a towel you like is a low-effort comfort upgrade.'],
    ],
    'amazon' => [['label' => 'Compression packing cubes', 'query' => 'compression packing cubes', 'icon' => '🧳'], ['label' => 'Travel-size toiletry bottles', 'query' => 'travel size toiletry bottles tsa', 'icon' => '🧴'], ['label' => 'Collapsible laundry hamper', 'query' => 'collapsible laundry hamper', 'icon' => '🧺'], ['label' => 'Velvet hangers (pack)', 'query' => 'velvet hangers 30 pack', 'icon' => '👔']],
],

'room-planner' => [
    'lead' => 'Enter your room size, drop in furniture and drag things around to see what fits before you move in. Your layout saves on this device.',
    'meta' => 'Free room planner: draw a room to scale, add a bed, desk and dresser, drag and rotate furniture, and see what fits in your sublet.',
    'widget' => <<<'HTML'
<div class="planner" data-planner>
  <div class="pl-controls">
    <label>Room width (ft)<input type="number" name="w" value="12" min="5" max="40" step="0.5"></label>
    <label>Room length (ft)<input type="number" name="l" value="11" min="5" max="40" step="0.5"></label>
    <label>Add furniture<select name="add">
      <option value="">Choose…</option>
      <option value="Twin bed|3.25|6.25">Twin bed (39×75 in)</option><option value="Full bed|4.5|6.25">Full bed (54×75 in)</option>
      <option value="Queen bed|5|6.67">Queen bed (60×80 in)</option><option value="Desk|4|2">Desk (48×24 in)</option>
      <option value="Dresser|5|1.5">Dresser (60×18 in)</option><option value="Nightstand|1.5|1.5">Nightstand</option>
      <option value="Chair|2|2">Chair</option><option value="Bookshelf|3|1">Bookshelf</option><option value="Suitcase|2.25|1.25">Suitcase</option>
      <option value="Rug|5|7">Rug (5×7 ft)</option><option value="Loveseat|5|2.75">Loveseat</option>
    </select></label>
    <button type="button" class="btn btn-sm btn-ghost" data-pl-rotate>Rotate selected</button>
    <button type="button" class="btn btn-sm btn-ghost" data-pl-delete>Delete selected</button>
    <button type="button" class="btn btn-sm btn-ghost" data-pl-reset>Clear room</button>
  </div>
  <svg class="pl-svg" data-pl-svg role="img" aria-label="Room layout"></svg>
  <p class="small muted" data-pl-info>Drag pieces to move them. Grid squares are 1 ft.</p>
</div>
HTML,
    'body' => <<<'HTML'
<h2>Why plan a room you are only staying in for a few months?</h2>
<p>Because a few months is long enough to be annoyed by a desk that blocks the closet. Ask your host for the room’s measurements (or measure on your video tour), sketch it here, and you will know whether your standing desk, keyboard or second suitcase will fit. Leave about 30 inches of walking space along main paths.</p>
HTML,
    'faqs' => [
        ['q' => 'How accurate are the furniture sizes?', 'a' => 'They are common standard sizes. Real pieces vary, so edit the room size and measure the actual furniture if fit is tight.'],
        ['q' => 'Is my layout saved?', 'a' => 'Yes, in your browser on this device only.'],
    ],
],

'city-quiz' => [
    'lead' => 'Answer six quick questions and we’ll suggest US cities that could suit a short-term stay — then you can browse sublets and read each city guide.',
    'meta' => 'Take The Sublet’s free city match quiz: six questions about budget, transit, climate and lifestyle to find a city for your next short-term stay.',
    'widget' => <<<'HTML'
<form class="quiz" data-quiz onsubmit="return false">
  <fieldset><legend>1. Why are you moving for a few months?</legend>
    <label class="chk"><input type="radio" name="why" value="tech" checked> Tech or startup job/internship</label>
    <label class="chk"><input type="radio" name="why" value="health"> Healthcare / travel nursing</label>
    <label class="chk"><input type="radio" name="why" value="gov"> Government, policy or nonprofit</label>
    <label class="chk"><input type="radio" name="why" value="finance"> Finance, media or consulting</label>
    <label class="chk"><input type="radio" name="why" value="study"> School, research or a semester</label>
    <label class="chk"><input type="radio" name="why" value="explore"> Just exploring / remote work</label>
  </fieldset>
  <fieldset><legend>2. Monthly housing budget</legend>
    <label class="chk"><input type="radio" name="budget" value="1"> Under $1,000</label>
    <label class="chk"><input type="radio" name="budget" value="2" checked> $1,000–$1,800</label>
    <label class="chk"><input type="radio" name="budget" value="3"> $1,800+</label>
  </fieldset>
  <fieldset><legend>3. Do you want to live without a car?</legend>
    <label class="chk"><input type="radio" name="car" value="yes" checked> Yes — transit and walking</label>
    <label class="chk"><input type="radio" name="car" value="no"> I’ll have a car</label>
  </fieldset>
  <fieldset><legend>4. Preferred weather</legend>
    <label class="chk"><input type="radio" name="climate" value="warm"> Warm most of the year</label>
    <label class="chk"><input type="radio" name="climate" value="mild" checked> Mild / I don’t mind</label>
    <label class="chk"><input type="radio" name="climate" value="seasons"> Real seasons, snow is fine</label>
  </fieldset>
  <fieldset><legend>5. City size</legend>
    <label class="chk"><input type="radio" name="size" value="big" checked> Big city energy</label>
    <label class="chk"><input type="radio" name="size" value="mid"> Mid-size, easier pace</label>
    <label class="chk"><input type="radio" name="size" value="college"> College town</label>
  </fieldset>
  <fieldset><legend>6. Weekend priority</legend>
    <label class="chk"><input type="radio" name="weekend" value="culture" checked> Food, museums, nightlife</label>
    <label class="chk"><input type="radio" name="weekend" value="outdoors"> Hiking, water, outdoors</label>
    <label class="chk"><input type="radio" name="weekend" value="calm"> Quiet and affordable</label>
  </fieldset>
  <button class="btn" type="submit" data-quiz-go>Show my matches</button>
</form>
<div class="calc-out" data-out="quiz" aria-live="polite"></div>
HTML,
    'body' => <<<'HTML'
<h2>How the matching works</h2>
<p>Each city gets broad, general tags — rough cost level, how practical it is without a car, climate, size and what people commonly go there for. Your answers are scored against those tags. It is a starting point for research, not a ranking: every city has affordable corners, car-free neighborhoods and exceptions to its stereotype. Read each <a href="/sublets/">city guide</a> and compare real listings before deciding.</p>
HTML,
    'faqs' => [
        ['q' => 'Why didn’t my city show up?', 'a' => 'The quiz covers a selection of cities with guides on The Sublet. Browse all cities from the Sublets page.'],
        ['q' => 'Are the cost levels based on listings?', 'a' => 'No — they are broad, general impressions of relative housing costs, not data from The Sublet listings. Always compare current prices.'],
    ],
],
];
