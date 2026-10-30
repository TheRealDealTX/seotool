<?php
$app = [
    '@context' => 'https://schema.org', '@type' => 'WebApplication',
    'name' => 'Tiny House Style Quiz', 'url' => abs_url($PATH),
    'description' => $ROUTE['description'],
    'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any',
    'browserRequirements' => 'Requires JavaScript',
    'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
    'publisher' => ['@id' => SITE_URL . '/#org'],
];
page_start([
    'breadcrumbs' => [['Home', '/'], ['Free Tools', '/tools/'], [$ROUTE['nav'], null]],
    'styles' => ['/assets/css/tools.css'],
    'schema' => [$app],
]);

// Style keys -> route slugs and one-line summaries.
$quizStyles = [
    'aframe'    => ['a-frame-house-plans', 'A steep, snow-shedding roof, a big sleeping loft and a striking look. Great as a getaway or rental cabin.'],
    'cabin'     => ['small-cabin-plans', 'Simple, sturdy and easy to heat. A small cabin suits rural land, wood stoves and owner-builders.'],
    'container' => ['shipping-container-home-plans', 'Steel boxes with a modern, industrial look that can be trucked to site and stacked or combined.'],
    'cottage'   => ['tiny-cottage-plans', 'Porches, gables and cozy rooms. A tiny cottage feels like a real house, just smaller.'],
    'thow'      => ['tiny-house-on-wheels-plans', 'A mobile home base built on a trailer, for people who want flexibility and lower land costs.'],
    'shed'      => ['shed-to-tiny-house', 'The fastest, cheapest route into a small space: convert a well-built shed into a studio, office or bunkhouse.'],
    'farm'      => ['small-farmhouse-plans', 'Board-and-batten charm with a mudroom and porch, sized for homesteads and families.'],
    'adu'       => ['adu-plans', 'A backyard cottage or granny flat on an existing lot, for family, guests or rental income.'],
    'loft'      => ['tiny-house-plans-with-loft', 'Sleeping lofts double usable space without a bigger footprint, ideal for couples and kids.'],
];
$styleOut = [];
foreach ($quizStyles as $k => [$slug, $blurb]) {
    $r = $ROUTES['/' . $slug . '/'];
    $plans = [];
    foreach (plans_for_style($slug) as $ps) $plans[] = ['name' => $PLANS[$ps]['name'], 'url' => '/plans/' . $ps . '/', 'title' => $PLANS[$ps]['title']];
    $styleOut[$k] = ['name' => $r['nav'], 'url' => '/' . $slug . '/', 'blurb' => $blurb, 'icon' => icon($r['icon']), 'plans' => $plans];
}

// Questions: [question, hint, [[label, sub, scores], ...]]
$questions = [
    ['What is your total budget, including land prep?', 'Rough is fine.', [
        ['Under $40,000', 'Mostly DIY, simple finishes', ['shed' => 3, 'thow' => 2, 'container' => 2, 'aframe' => 2, 'loft' => 1]],
        ['$40,000 to $80,000', 'A solid owner-built home', ['thow' => 3, 'aframe' => 2, 'container' => 2, 'loft' => 2, 'cabin' => 2, 'shed' => 1]],
        ['$80,000 to $150,000', 'Some hired help or a builder', ['cabin' => 3, 'cottage' => 3, 'loft' => 2, 'adu' => 2, 'container' => 1, 'aframe' => 1]],
        ['More than $150,000', 'Builder-built, more space', ['adu' => 3, 'farm' => 3, 'cottage' => 2, 'cabin' => 2]],
    ]],
    ['Where will your tiny house go?', 'Your land situation shapes everything else.', [
        ['I do not have land yet', 'Or I want to move around', ['thow' => 3, 'loft' => 2, 'container' => 1]],
        ['On rural land I own', 'Acreage, woods or a homestead', ['cabin' => 3, 'farm' => 3, 'aframe' => 3, 'shed' => 2, 'container' => 1]],
        ['In the backyard of an existing home', 'Mine or a family member\'s', ['adu' => 3, 'shed' => 2, 'cottage' => 2]],
        ['On a small lot in town', 'Or in a tiny house community', ['cottage' => 3, 'thow' => 2, 'loft' => 2, 'container' => 1]],
    ]],
    ['Do you need to be able to move it?', '', [
        ['Yes, mobility is a must', 'I plan to relocate', ['thow' => 3, 'loft' => 2, 'container' => 1]],
        ['Maybe someday', 'Nice to have, not essential', ['container' => 2, 'shed' => 2, 'thow' => 1]],
        ['No, it is staying put', 'Permanent foundation', ['cabin' => 2, 'cottage' => 2, 'adu' => 2, 'farm' => 2, 'aframe' => 2]],
    ]],
    ['What is the climate like?', '', [
        ['Cold with heavy snow', 'Long winters', ['aframe' => 3, 'cabin' => 3, 'farm' => 1]],
        ['Hot and sunny', 'Long summers, strong sun', ['container' => 2, 'cottage' => 1, 'adu' => 1, 'farm' => 1]],
        ['Mild most of the year', 'Moderate seasons', ['cottage' => 2, 'thow' => 2, 'loft' => 1, 'adu' => 1, 'shed' => 1]],
        ['Rainy or coastal', 'Wet, windy or humid', ['cottage' => 2, 'aframe' => 2, 'cabin' => 1, 'loft' => 1]],
    ]],
    ['Who will live or stay there?', '', [
        ['Just me', 'Solo living or a personal retreat', ['shed' => 3, 'thow' => 2, 'container' => 2, 'aframe' => 1]],
        ['Two of us', 'A couple or two friends', ['thow' => 2, 'aframe' => 2, 'loft' => 2, 'cabin' => 1, 'cottage' => 1]],
        ['A family with kids', 'Separate sleeping spaces matter', ['loft' => 3, 'farm' => 3, 'cabin' => 2, 'adu' => 1]],
        ['Extended family or frequent guests', 'Room for more people', ['adu' => 3, 'farm' => 2, 'cottage' => 2]],
    ]],
    ['How much of the building will you do yourself?', '', [
        ['None, I will hire it out', 'A builder handles it', ['adu' => 2, 'cottage' => 2, 'farm' => 1, 'container' => 1]],
        ['Finish work and painting', 'Not framing or systems', ['container' => 2, 'thow' => 1, 'loft' => 1, 'cottage' => 1]],
        ['I can frame walls and a roof', 'Comfortable with power tools', ['cabin' => 2, 'aframe' => 2, 'shed' => 2, 'thow' => 2, 'loft' => 1]],
        ['Pretty much everything', 'Experienced builder', ['aframe' => 2, 'cabin' => 2, 'farm' => 1, 'thow' => 1, 'shed' => 1]],
    ]],
    ['Which look do you love most?', '', [
        ['Modern and industrial', 'Clean lines, steel, big glass', ['container' => 3, 'thow' => 1, 'adu' => 1]],
        ['Rustic and woodsy', 'Logs, timber and stone', ['cabin' => 3, 'aframe' => 2]],
        ['Classic and cozy', 'Porches, gables, window boxes', ['cottage' => 3, 'loft' => 1]],
        ['Farmhouse', 'Board-and-batten and metal roofs', ['farm' => 3, 'loft' => 1, 'thow' => 1]],
        ['Bold and architectural', 'A shape people notice', ['aframe' => 3, 'container' => 1]],
    ]],
    ['How will you mainly use it?', '', [
        ['Full-time home', 'Where I live every day', ['cottage' => 2, 'farm' => 2, 'loft' => 2, 'thow' => 1, 'cabin' => 1]],
        ['Rental income', 'Short- or long-term rental', ['adu' => 3, 'aframe' => 2, 'container' => 1]],
        ['Vacation or weekend getaway', 'A place to escape to', ['aframe' => 3, 'cabin' => 3, 'shed' => 1]],
        ['Office, guest room or family member', 'Extra space near the main house', ['shed' => 3, 'adu' => 2, 'cottage' => 1]],
    ]],
];
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free tool</p>
    <h1>Tiny House Style Quiz</h1>
    <p class="lead">Not sure whether you are an A-frame person, a tiny house on wheels person or an ADU person? Answer eight quick questions about your budget, land, climate and lifestyle, and this tiny house style quiz will match you with the styles that fit best.</p>
    <ul class="hero-facts">
      <li>8 questions, about 2 minutes</li>
      <li>9 tiny house styles</li>
      <li>No email required</li>
    </ul>
  </div>
</section>

<section class="section tool-sec">
  <div class="wrap tool-shell" id="qz">
    <div class="panel quiz-panel">
      <div id="qz-quiz">
        <div class="quiz-top"><span id="qz-count">Question 1 of <?= count($questions) ?></span><span id="qz-pct">0% done</span></div>
        <div class="quiz-progress" role="progressbar" aria-label="Quiz progress" aria-valuemin="0" aria-valuemax="<?= count($questions) ?>" aria-valuenow="0" id="qz-bar"><i style="width:0%"></i></div>
        <?php foreach ($questions as $qi => [$q, $hint, $opts]): ?>
        <div class="quiz-q<?= $qi === 0 ? ' active' : '' ?>" data-q="<?= $qi ?>" role="group" aria-labelledby="qz-h<?= $qi ?>">
          <h2 id="qz-h<?= $qi ?>" tabindex="-1"><?= e($q) ?></h2>
          <?php if ($hint): ?><p class="muted" style="margin:0"><?= e($hint) ?></p><?php endif; ?>
          <div class="quiz-opts">
            <?php foreach ($opts as $oi => [$label, $sub, $scores]): ?>
            <button type="button" data-o="<?= $oi ?>" data-label="<?= e($label) ?>" data-s="<?= e(json_encode($scores)) ?>"><span class="k" aria-hidden="true"><?= chr(65 + $oi) ?></span><span><?= e($label) ?><small><?= e($sub) ?></small></span></button>
            <?php endforeach; ?>
          </div>
        </div>
        <?php endforeach; ?>
        <div class="quiz-nav">
          <button type="button" class="btn btn-outline btn-sm" id="qz-back" disabled>&larr; Back</button>
          <button type="button" class="btn btn-outline btn-sm" id="qz-restart-top">Start over</button>
        </div>
      </div>
      <div class="quiz-result" id="qz-result" hidden tabindex="-1" aria-labelledby="qz-res-h"></div>
    </div>

    <div class="panel result-panel">
      <p class="result-label" id="qz-label">Your matches so far</p>
      <div aria-live="polite">
        <p class="result-big sm" id="qz-lead">Answer to begin</p>
        <p class="result-sub" id="qz-lead-sub">Your top styles update after every answer.</p>
      </div>
      <ul class="live-list" id="qz-live"></ul>
      <p class="result-note">Match strength compares your answers with what each style does best. It is a starting point, not a verdict: zoning and site conditions matter too.</p>
    </div>
  </div>
</section>
<script type="application/json" id="qz-data"><?= json_encode($styleOut, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) ?></script>

<section class="section tool-prose">
  <div class="narrow prose">
    <h2>Which tiny house style is right for you?</h2>
    <p>&ldquo;Tiny house&rdquo; covers a lot of ground: a 160 sq ft house on a trailer, a steep A-frame in the snow, a steel shipping container and a 700 sq ft backyard cottage all count. Each one solves a different problem. The best style for you depends less on looks than on where it will sit, whether it has to move, what the weather does and how much of the work you will take on. This quiz from Tiny Homes Blueprint weighs those factors for you and points you to the styles worth a closer look.</p>

    <h2>How the style quiz works</h2>
    <p>Each answer adds points to the styles it suits. For example, &ldquo;I need to be able to move it&rdquo; scores heavily for a tiny house on wheels, while &ldquo;cold with heavy snow&rdquo; favors A-frames and cabins. Your match strength for each style is the share of the maximum points that style could have earned from your answers, so a 100% match means every answer pointed its way.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Style</th><th>Usually best when</th><th>Watch out for</th></tr></thead>
      <tbody>
        <tr><td><a href="/tiny-house-on-wheels-plans/">Tiny house on wheels</a></td><td>You have no land yet or need to move</td><td>Parking and zoning, weight limits</td></tr>
        <tr><td><a href="/a-frame-house-plans/">A-frame</a></td><td>Snowy sites, vacation rentals</td><td>Sloped walls reduce usable floor area</td></tr>
        <tr><td><a href="/small-cabin-plans/">Small cabin</a></td><td>Rural land, owner-builders, wood heat</td><td>Well, septic and access costs</td></tr>
        <tr><td><a href="/tiny-cottage-plans/">Tiny cottage</a></td><td>Town lots, full-time living</td><td>Minimum house size rules in some areas</td></tr>
        <tr><td><a href="/adu-plans/">ADU</a></td><td>Backyards, family or rental income</td><td>Local size caps, setbacks and fees</td></tr>
        <tr><td><a href="/shipping-container-home-plans/">Shipping container</a></td><td>Modern look, quick shell, hot climates with good insulation</td><td>Insulation, condensation and cutting steel</td></tr>
        <tr><td><a href="/shed-to-tiny-house/">Shed conversion</a></td><td>Small budgets, offices, guest space</td><td>Insulation, plumbing and permit rules</td></tr>
        <tr><td><a href="/small-farmhouse-plans/">Small farmhouse</a></td><td>Homesteads and families</td><td>Usually larger and costlier to build</td></tr>
        <tr><td><a href="/tiny-house-plans-with-loft/">Loft plans</a></td><td>Couples and kids who need sleeping space</td><td>Headroom, stairs and summer heat</td></tr>
      </tbody>
    </table></div>

    <h2>Why your style choice matters</h2>
    <p>Style is not just about looks. It decides how a building department classifies your home, which affects where you can put it and how you can pay for it. A tiny house on wheels is often treated like an RV, which can make it hard to live in full-time in some places, while a cottage or ADU on a foundation is a house in the eyes of the law and can usually be financed with a construction loan or mortgage. Style also drives cost: an A-frame's steep roof is simple to frame but wastes floor area at the edges, and a container gives you a quick steel shell that still needs insulation and framing inside.</p>

    <h3>Questions to answer before you commit</h3>
    <ul class="check-list">
      <li><strong>Can I legally live in it where I want to put it?</strong> Ask your planning office about minimum house sizes, ADU rules and whether they have adopted IRC Appendix AQ.</li>
      <li><strong>How will I pay for it?</strong> Foundation homes open the door to conventional loans; tiny houses on wheels usually rely on savings, RV loans or personal loans.</li>
      <li><strong>Who will build it?</strong> Simple shapes like cabins and sheds suit first-time builders. Containers need welding and steel cutting, and complex rooflines need more skill.</li>
      <li><strong>What will the weather do to it?</strong> Snow load, wind, humidity and heat all favor some styles over others, and affect insulation and roofing choices.</li>
      <li><strong>Will it still fit my life in five years?</strong> Children, aging parents, remote work or a future rental plan can all change what you need.</li>
    </ul>

    <h2>What to do with your result</h2>
    <ol>
      <li><strong>Read up on your top match.</strong> Each style page covers sizes, costs, pros and cons and layout ideas.</li>
      <li><strong>Check the rules for your land.</strong> A great style is no use if your county will not allow it. Start with our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a>.</li>
      <li><strong>Size and price it.</strong> Use the <a href="/tools/how-big-should-my-tiny-house-be/">size calculator</a> to find your square footage and the <a href="/tools/tiny-house-cost-calculator/">cost calculator</a> to set a budget.</li>
      <li><strong>Sketch a layout.</strong> Try your ideas in the <a href="/tools/tiny-house-layout-planner/">layout planner</a> before you commit to a plan.</li>
    </ol>
    <p>If your top two matches are close, that is useful information too. Many good tiny houses blend styles, like a cottage with a sleeping loft or a cabin built as a backyard ADU. Tiny Homes Blueprint plans are designed to adapt in exactly that way.</p>
    <p>It is also worth retaking the quiz with one answer changed. Switching from &ldquo;I need to move it&rdquo; to &ldquo;it is staying put,&rdquo; or from a solo household to a couple, shows you which of your assumptions is really driving the result, and that is often the decision to settle first.</p>

    <?php faq_block([
        ['What is the most popular tiny house style?', '<p>Tiny houses on wheels are the best-known style, but foundation-built cottages, cabins and backyard ADUs are often easier to permit and finance. The most popular choice in your area depends heavily on local zoning.</p>'],
        ['Which tiny house style is cheapest to build?', '<p>Shed conversions and simple owner-built cabins or tiny houses on wheels are usually the cheapest. Containers can look cheap but often need significant insulation, framing and steel work. See the <a href="/blog/how-much-does-a-tiny-house-cost/">tiny house cost guide</a> for details.</p>'],
        ['What tiny house style is best for a family?', '<p>Families usually do best with plans that include lofts or separate bedrooms, such as loft plans, small farmhouses or a 2 to 3 bedroom cabin. Our <a href="/plans/plan-12-2418/">Plan 12-2418</a> is a 700 sq ft, 3-bedroom option.</p>'],
        ['Can I combine tiny house styles?', '<p>Yes. Many of the best tiny houses mix ideas, like a farmhouse-style tiny house on wheels or a cabin designed as an ADU. Use your top matches as a guide to the features you want.</p>'],
        ['Is the quiz result final?', '<p>No. It is a starting point based on eight answers. Your land, local rules and budget details should drive the final decision, and you can retake the quiz with different answers anytime.</p>'],
    ]); ?>

    <h2>Related tools and guides</h2>
    <ul class="related-links">
      <li><a href="/tools/how-big-should-my-tiny-house-be/"><?= icon('size') ?> Tiny house size calculator</a></li>
      <li><a href="/tools/tiny-house-cost-calculator/"><?= icon('cost') ?> Cost calculator</a></li>
      <li><a href="/tools/tiny-house-layout-planner/"><?= icon('layout') ?> Layout planner</a></li>
      <li><a href="/tiny-house-plans/"><?= icon('file') ?> Browse all tiny house plans</a></li>
      <li><a href="/blog/tiny-house-kits-vs-plans/"><?= icon('book') ?> Tiny house kits vs plans</a></li>
      <li><a href="/blog/free-tiny-house-plans/"><?= icon('book') ?> Free vs paid tiny house plans</a></li>
      <li><a href="/blog/how-to-build-a-tiny-house/"><?= icon('book') ?> How to build a tiny house</a></li>
      <li><a href="/embracing-tiny-homes-unlocking-the-advantages-of-compact-living/"><?= icon('leaf') ?> Advantages of compact living</a></li>
    </ul>
  </div>
</section>

<?php cta_band('Found your style?', 'Browse Tiny Homes Blueprint plans, or tell us your top match and we will suggest a plan or a modification that fits.'); ?>
<?php page_end(['scripts' => ['/assets/js/tools/style-quiz.js']]); ?>
