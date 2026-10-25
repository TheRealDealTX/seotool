<?php
require __DIR__ . '/../_common.php';

$slug = 'influencer-email-generator';
$name = 'Influencer Email Generator';
$desc = 'Free influencer email generator: write to an influencer as a brand, or pitch a brand as a creator. Get subject lines, an email and a short DM in seconds.';

page_start([
    'title' => 'Influencer Email Generator: Outreach & Pitch Templates',
    'description' => $desc,
    'path' => '/tools/' . $slug . '/',
    'extra_css' => ['/assets/css/tools.css'],
    'extra_js' => ['/assets/js/tools/email.js'],
    'schema' => [tool_schema($slug, $name, $desc)],
]);

page_hero(
    'Free tool · outreach templates',
    'Influencer <span class="grad-text">Email Generator</span>',
    'Not sure how to write to an influencer, or how to pitch a brand? Fill in a few details and get subject lines, a ready-to-send email and a short DM version you can copy in one click.',
    [['Free Tools', '/tools/'], [$name, '/tools/' . $slug . '/']]
);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap tool-shell">
    <form class="tool-panel" id="em-form" onsubmit="return false">
      <div class="mode-toggle" role="group" aria-label="Who is writing?">
        <button type="button" data-mode="brand" aria-pressed="true">Brand → Influencer</button>
        <button type="button" data-mode="creator" aria-pressed="false">Creator → Brand pitch</button>
      </div>

      <div id="em-brand">
        <div class="inline-pair">
          <div class="field"><label for="b-brand">Your brand name</label><input id="b-brand" type="text" value="Glow Theory"></div>
          <div class="field"><label for="b-sender">Your name</label><input id="b-sender" type="text" value="Maya"></div>
        </div>
        <div class="field"><label for="b-product">Product or campaign</label><input id="b-product" type="text" value="our new vitamin C serum"></div>
        <div class="inline-pair">
          <div class="field"><label for="b-name">Influencer first name</label><input id="b-name" type="text" value="Jess"></div>
          <div class="field"><label for="b-handle">Their handle</label><input id="b-handle" type="text" value="@jessglows"></div>
        </div>
        <div class="field"><label for="b-recent">A recent post you liked <span class="hint">(makes it personal)</span></label><input id="b-recent" type="text" value="your morning skincare routine Reel"></div>
        <div class="inline-pair">
          <div class="field"><label for="b-platform">Platform</label><select id="b-platform"><option>Instagram</option><option>TikTok</option><option>YouTube</option><option>Facebook</option><option>Pinterest</option></select></div>
          <div class="field"><label for="b-comp">Compensation</label><select id="b-comp"><option value="paid">Paid collaboration</option><option value="gifted">Gifted product</option><option value="affiliate">Affiliate / commission</option></select></div>
        </div>
      </div>

      <div id="em-creator" hidden>
        <div class="inline-pair">
          <div class="field"><label for="c-name">Your name</label><input id="c-name" type="text" value="Alex"></div>
          <div class="field"><label for="c-handle">Your handle</label><input id="c-handle" type="text" value="@alexlifts"></div>
        </div>
        <div class="inline-pair">
          <div class="field"><label for="c-niche">Your niche</label><input id="c-niche" type="text" value="home fitness"></div>
          <div class="field"><label for="c-platform">Main platform</label><select id="c-platform"><option>Instagram</option><option>TikTok</option><option>YouTube</option><option>Facebook</option><option>Pinterest</option></select></div>
        </div>
        <div class="inline-pair">
          <div class="field"><label for="c-followers">Followers</label><input id="c-followers" type="text" value="32K"></div>
          <div class="field"><label for="c-er">Engagement rate</label><input id="c-er" type="text" value="4.8%"></div>
        </div>
        <div class="inline-pair">
          <div class="field"><label for="c-brand">Brand you are pitching</label><input id="c-brand" type="text" value="FlexBand"></div>
          <div class="field"><label for="c-contact">Contact first name <span class="hint">(optional)</span></label><input id="c-contact" type="text" value=""></div>
        </div>
        <div class="field"><label for="c-idea">Your content idea</label><input id="c-idea" type="text" value="a 3-part Reel series: 10-minute resistance band workouts for small apartments"></div>
        <div class="field"><label for="c-proof">Proof point <span class="hint">(a result or audience fact)</span></label><input id="c-proof" type="text" value="68% of my audience is 25-34 and works out at home"></div>
      </div>

      <div class="field"><label for="em-tone">Tone</label><select id="em-tone"><option value="friendly">Friendly</option><option value="professional">Professional</option><option value="bold">Short &amp; bold</option></select></div>
      <div class="btn-row">
        <button type="button" class="btn btn-glow" id="em-go"><?= icon('sparkles') ?> Generate</button>
        <button type="button" class="btn btn-ghost" id="em-again">Regenerate variation</button>
      </div>
    </form>

    <div class="tool-panel tool-output gradient-border" aria-live="polite">
      <div class="out-label" style="margin-top:0">Subject lines</div>
      <ul class="subject-list" id="em-subjects"></ul>
      <div class="out-label">Email <button type="button" class="btn btn-ghost btn-sm" data-copy="#em-body"><?= icon('copy') ?> Copy</button></div>
      <div class="template-box gen-out" id="em-body"></div>
      <div class="out-label">Short DM version <button type="button" class="btn btn-ghost btn-sm" data-copy="#em-dm"><?= icon('copy') ?> Copy</button></div>
      <div class="template-box gen-out dm" id="em-dm"></div>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2 id="how-it-works">How to write to an influencer (and get a reply)</h2>
    <p>Most outreach emails fail for the same three reasons: they are generic, they hide the offer, and they ask for too much in the first message. This generator follows the structure that consistently gets replies, whether you are a brand reaching out to a creator or a creator pitching a brand.</p>
    <ol>
      <li><strong>A personal opener.</strong> Mention a specific post. It proves you are not mass-mailing, and it is the single biggest driver of reply rates.</li>
      <li><strong>Why them, in one sentence.</strong> Connect their audience to your product (or your audience to the brand's customers).</li>
      <li><strong>A clear offer.</strong> Say upfront whether it is paid, gifted or commission-based. Creators skip vague emails because they assume "unpaid".</li>
      <li><strong>One easy next step.</strong> Ask for rates, a quick call, or permission to send details. Not all three.</li>
    </ol>
    <p>The DM version compresses the same message for Instagram, TikTok or Facebook inboxes, where anything longer than a few lines gets ignored. Use it as a first touch and move to email once they reply. For a deeper walkthrough with seven more templates, read <a href="/how-to-write-to-an-influencer/">how to write to an influencer</a>.</p>

    <h2>Tips for brands contacting influencers</h2>
    <ul>
      <li><strong>Find the business email first.</strong> Check the bio, the "Email" or "Contact" button on Instagram and TikTok, the YouTube About tab, or a link-in-bio page. Email beats DMs for anything paid.</li>
      <li><strong>Lead with compensation.</strong> If the collaboration is gifted only, say so. Honesty earns more goodwill than a surprise later.</li>
      <li><strong>Follow up once, after 4-7 days.</strong> A short, polite bump often doubles response rates. Stop after two follow-ups.</li>
    </ul>

    <h2>Subject lines that get opened</h2>
    <p>Your subject line decides whether the email is read at all. The best ones are short, specific and name both parties, for example "Glow Theory x Jess: paid collab idea". Avoid all caps, emojis in professional pitches and vague lines like "Opportunity". The generator gives you three options so you can test which style your audience responds to.</p>
    <h2>Tips for creators pitching brands</h2>
    <ul>
      <li><strong>Pitch an idea, not just yourself.</strong> "A 3-part series on X" is far easier to approve than "I would love to work together".</li>
      <li><strong>Bring one proof point.</strong> An audience stat, a past result or your engagement rate (calculate it with the <a href="/tools/engagement-rate-calculator/">engagement rate calculator</a>).</li>
      <li><strong>Attach your media kit.</strong> Build one in five minutes with the <a href="/tools/media-kit-builder/">media kit builder</a>, and know your price before they ask with the <a href="/tools/influencer-earnings-calculator/">earnings calculator</a>.</li>
    </ul>
    <div class="callout"><?= icon('shield') ?><p>Everything is generated in your browser by Monetizing Influencers templates. Nothing you type is sent anywhere. Always review and personalise before you hit send.</p></div>
  </div>
</section>

<?php
faq_block([
    ['How do you write to an influencer for the first time?', '<p>Keep it under 150 words: a personal compliment on a specific post, one sentence on why they fit your brand, a clear offer (paid, gifted or affiliate) and a simple question like "Can you share your rates?". Use the Brand → Influencer mode above to draft it.</p>'],
    ['Should I contact influencers by email or DM?', '<p>Email is best for paid collaborations because it is easier to share details and contracts. DMs work for a quick first touch or for smaller creators who do not list an email. The generator gives you both versions.</p>'],
    ['How do creators pitch brands with no reply?', '<p>Send one follow-up after about a week with a new angle, such as a fresh content idea or a recent result. If there is still no reply, move on and try again next quarter.</p>'],
    ['Is it okay to use a template?', '<p>Yes, as long as you personalise it. Change the opener, the post you reference and the idea for every send. Templated structure is fine; templated wording is what gets ignored.</p>'],
]);
more_tools($slug);
cta_band('Want help landing the deal?', 'Monetizing Influencers helps creators build pitch lists, media kits and outreach sequences that turn into paid partnerships.');
page_end();
