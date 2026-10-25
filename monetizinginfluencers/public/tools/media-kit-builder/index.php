<?php
require __DIR__ . '/../_common.php';

$slug = 'media-kit-builder';
$name = 'Media Kit Builder';
$desc = 'Free influencer media kit builder: enter your stats, audience, services and rates and get a polished one-page media kit to print or save as a PDF.';

page_start([
    'title' => 'Free Influencer Media Kit Builder (Print to PDF)',
    'description' => $desc,
    'path' => '/tools/' . $slug . '/',
    'extra_css' => ['/assets/css/tools.css'],
    'extra_js' => ['/assets/js/tools/media-kit.js'],
    'schema' => [tool_schema($slug, $name, $desc)],
]);

page_hero(
    'Free tool · live preview',
    'Influencer <span class="grad-text">Media Kit Builder</span>',
    'Type your details on the left and watch a clean, brand-ready media kit build itself on the right. When it looks right, print it or save it as a PDF and attach it to your next pitch.',
    [['Free Tools', '/tools/'], [$name, '/tools/' . $slug . '/']]
);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap tool-shell mk-shell">
    <form class="tool-panel" id="mk-form" onsubmit="return false">
      <fieldset class="mk-fieldset"><legend>About you</legend>
        <div class="inline-pair">
          <div class="field"><label for="mk-name">Name</label><input id="mk-name" name="name" type="text" value="Sofia Reyes"></div>
          <div class="field"><label for="mk-handle">Handle</label><input id="mk-handle" name="handle" type="text" value="@sofiaeatsgreen"></div>
        </div>
        <div class="inline-pair">
          <div class="field"><label for="mk-niche">Niche</label><input id="mk-niche" name="niche" type="text" value="Plant-based food &amp; wellness"></div>
          <div class="field"><label for="mk-location">Location</label><input id="mk-location" name="location" type="text" value="Austin, TX"></div>
        </div>
        <div class="field"><label for="mk-bio">Short bio</label><textarea id="mk-bio" name="bio" rows="3" style="min-height:90px">I share quick, budget-friendly plant-based recipes for busy people. My community comes for 15-minute meals and stays for honest product reviews.</textarea></div>
      </fieldset>

      <fieldset class="mk-fieldset"><legend>Platforms</legend>
        <div class="mk-plat-row">
          <div class="field"><label for="mk-ig">Instagram followers</label><input id="mk-ig" name="ig" type="text" value="42K"></div>
          <div class="field"><label for="mk-tt">TikTok followers</label><input id="mk-tt" name="tt" type="text" value="88K"></div>
          <div class="field"><label for="mk-yt">YouTube subscribers</label><input id="mk-yt" name="yt" type="text" value="12K"></div>
          <div class="field"><label for="mk-pin">Pinterest / other</label><input id="mk-pin" name="pin" type="text" value=""></div>
        </div>
        <div class="inline-pair">
          <div class="field"><label for="mk-er">Avg engagement rate</label><input id="mk-er" name="er" type="text" value="5.2%"></div>
          <div class="field"><label for="mk-views">Avg monthly views / reach</label><input id="mk-views" name="views" type="text" value="1.4M"></div>
        </div>
      </fieldset>

      <fieldset class="mk-fieldset"><legend>Audience</legend>
        <div class="inline-three">
          <div class="field"><label for="mk-age">Top age group</label><input id="mk-age" name="age" type="text" value="25-34 (54%)"></div>
          <div class="field"><label for="mk-gender">Gender split</label><input id="mk-gender" name="gender" type="text" value="78% women"></div>
          <div class="field"><label for="mk-countries">Top countries</label><input id="mk-countries" name="countries" type="text" value="US, CA, UK"></div>
        </div>
      </fieldset>

      <fieldset class="mk-fieldset"><legend>Services &amp; rates</legend>
        <div class="field"><label for="mk-services">One per line: service = price</label><textarea id="mk-services" name="services" rows="4" style="min-height:110px">Instagram Reel = $650
TikTok video = $800
Story set (3 frames) = $250
UGC video (no posting) = $350</textarea></div>
        <div class="field"><label for="mk-brands">Past brands <span class="hint">(comma separated)</span></label><input id="mk-brands" name="brands" type="text" value="Oatly, Thrive Market, Vitamix, Daily Harvest"></div>
      </fieldset>

      <fieldset class="mk-fieldset"><legend>Contact &amp; style</legend>
        <div class="inline-pair">
          <div class="field"><label for="mk-email">Contact email</label><input id="mk-email" name="email" type="email" value="hello@sofiaeatsgreen.com"></div>
          <div class="field"><label for="mk-color">Accent colour</label><input id="mk-color" name="color" type="color" value="#8b5cf6"></div>
        </div>
      </fieldset>
      <p class="small" id="mk-saved" aria-live="polite">Your draft saves automatically in this browser.</p>
    </form>

    <div class="tool-output">
      <article class="kit" id="kit" aria-label="Media kit preview">
        <div class="kit-top">
          <div class="kit-avatar" id="k-initials">SR</div>
          <h2 id="k-name">Sofia Reyes</h2>
          <div class="kit-handle"><span id="k-handle"></span> · <span id="k-location"></span></div>
          <span class="kit-niche" id="k-niche"></span>
        </div>
        <div class="kit-body">
          <h3>About</h3>
          <p id="k-bio"></p>
          <h3>Reach</h3>
          <div class="kit-stats" id="k-stats"></div>
          <div class="kit-two">
            <div><h3>Audience</h3><ul class="kit-list" id="k-aud"></ul></div>
            <div><h3>Rates</h3><ul class="kit-list" id="k-rates"></ul></div>
          </div>
          <h3>Brands I have worked with</h3>
          <div class="kit-brands" id="k-brands"></div>
        </div>
        <div class="kit-foot"><span id="k-email"></span><em style="font-style:normal">Let's create something great together</em></div>
      </article>
      <div class="kit-actions">
        <button type="button" class="btn btn-glow" id="mk-print"><?= icon('printer') ?> Print / Save as PDF</button>
        <button type="button" class="btn btn-ghost" id="mk-reset">Reset example</button>
      </div>
      <p class="disclaimer">Tip: in the print dialog choose "Save as PDF" and turn on "Background graphics" to keep the colours.</p>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2 id="how-it-works">What to put in an influencer media kit</h2>
    <p>A media kit is your creator resume: one page that tells a brand who you are, who listens to you and what it costs to work together. Brand managers often review dozens of creators for a single campaign, so the best kits answer the obvious questions in under 30 seconds. This builder includes every section brands look for:</p>
    <ul>
      <li><strong>Who you are.</strong> Name, handle, niche and a two-sentence bio focused on what your audience gets from you.</li>
      <li><strong>Reach.</strong> Followers per platform, average engagement rate and monthly views or reach. Use real, recent numbers; brands check.</li>
      <li><strong>Audience.</strong> Top age group, gender split and top countries. This is often the deciding factor, because brands buy audiences, not follower counts.</li>
      <li><strong>Services and rates.</strong> A short menu of deliverables with starting prices. Listing rates filters out low-budget enquiries and speeds up deals.</li>
      <li><strong>Social proof.</strong> Brands you have worked with, even gifted collaborations.</li>
      <li><strong>Contact.</strong> One clear email address.</li>
    </ul>

    <h2>How to use the builder</h2>
    <p>Start with the example and overwrite it with your own details. The preview updates on every keystroke, and your draft is saved in this browser, so you can close the tab and come back later. Pick an accent colour that matches your profile aesthetic. When you are happy, click <strong>Print / Save as PDF</strong>: only the kit is printed, at full width, ready to attach to an email.</p>
    <p>Not sure what to charge? Get a starting range from the <a href="/tools/influencer-earnings-calculator/">influencer earnings calculator</a>, and calculate your exact engagement with the <a href="/tools/engagement-rate-calculator/">engagement rate calculator</a>. For a deeper guide, including design tips and what to leave out, read <a href="/influencer-media-kit/">how to make an influencer media kit</a>.</p>

    <h2>Media kit tips that win more deals</h2>
    <ul>
      <li><strong>Update it monthly.</strong> Stale numbers are the most common media kit mistake.</li>
      <li><strong>Lead with your strongest stat.</strong> If your engagement is high, put it first. If your audience is unusually targeted, lead with that.</li>
      <li><strong>Tailor for big pitches.</strong> Duplicate the kit and swap in the most relevant past brands and services for each campaign.</li>
      <li><strong>Send it with a pitch, not instead of one.</strong> Pair it with a personalised email from the <a href="/tools/influencer-email-generator/">influencer email generator</a>.</li>
    </ul>
    <div class="callout"><?= icon('shield') ?><p>Your media kit data never leaves your device. Monetizing Influencers does not see or store anything you type here.</p></div>
  </div>
</section>

<?php
faq_block([
    ['What is an influencer media kit?', '<p>A one-page document that summarises your channels, audience demographics, engagement, services, rates and past brand partners. Brands use it to decide quickly whether you fit a campaign.</p>'],
    ['Should I put my rates in my media kit?', '<p>Starting rates help: they save time and set expectations. If you prefer to negotiate case by case, write "rates from $X" or "rates on request" instead.</p>'],
    ['How do I save my media kit as a PDF?', '<p>Click "Print / Save as PDF", choose "Save as PDF" as the destination and enable background graphics so the colour header prints.</p>'],
    ['Do I need a media kit with a small following?', '<p>Yes. Nano and micro creators benefit most, because a professional kit makes a small, engaged audience look like the opportunity it is.</p>'],
]);
more_tools($slug);
cta_band('Want a media kit page on your own website?', 'Monetizing Influencers builds money sites for creators with a live media kit page, email capture and SEO built in.', 'See web design for influencers', '/website-design/');
page_end();
