<?php
require __DIR__ . '/../_common.php';

$slug = 'monetization-readiness-quiz';
$name = 'Monetization Readiness Quiz';
$desc = 'Take the free influencer monetization quiz: 10 quick questions reveal your readiness score and the two income streams you should start with right now.';

page_start([
    'title' => 'Influencer Monetization Quiz: Are You Ready?',
    'description' => $desc,
    'path' => '/tools/' . $slug . '/',
    'extra_css' => ['/assets/css/tools.css'],
    'extra_js' => ['/assets/js/tools/quiz.js'],
    'schema' => [tool_schema($slug, $name, $desc)],
]);

page_hero(
    'Free tool · 2-minute quiz',
    'Monetization <span class="grad-text">Readiness Quiz</span>',
    'Ten quick questions about your audience, content and goals. Get a readiness score out of 100 and the two income streams that fit you best, with clear next steps for each.',
    [['Free Tools', '/tools/'], [$name, '/tools/' . $slug . '/']]
);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap">
    <div class="quiz-card gradient-border" id="quiz" aria-live="polite">
      <noscript><p>This quiz needs JavaScript. You can still read the guide below.</p></noscript>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow prose">
    <h2 id="how-it-works">How the quiz scores you</h2>
    <p>Every answer does two things. First, it adds to your <strong>readiness score</strong>, a 0-100 measure of how prepared you are to earn consistently today. It rewards the things brands and customers actually respond to: an engaged audience, consistent posting, a professional media kit, owned channels like a website or email list, and time to run the business side.</p>
    <p>Second, each answer adds points to six income streams: brand deals, affiliate marketing, ad revenue, digital products, memberships and UGC (user-generated content made for brands without posting it). Your two highest-scoring streams become your recommendations. For example, if your audience keeps asking "where did you get that?", affiliate marketing scores highly; if they ask "how do you do that?", a digital product or course is a natural fit.</p>

    <h2>What your readiness score means</h2>
    <ul>
      <li><strong>0-39: Foundation stage.</strong> Focus on consistency and a clear niche. Start with streams that have no follower minimum, like UGC and affiliate links, so you earn while you grow.</li>
      <li><strong>40-69: Ready to earn.</strong> You have enough to start pitching. Build a media kit, set your rates and send five tailored pitches a week.</li>
      <li><strong>70-100: Ready to scale.</strong> You are leaving money on the table if you rely on one stream. Add an owned product or membership and negotiate longer brand partnerships.</li>
    </ul>

    <h2>Turn your result into action</h2>
    <p>Every recommendation links to the relevant section of the Monetizing Influencers <a href="/monetization/">influencer monetization guide</a> and the tool that helps you start. If brand deals are in your top two, get your rate from the <a href="/tools/influencer-earnings-calculator/">earnings calculator</a> and build a <a href="/tools/media-kit-builder/">media kit</a>. If you want to see how your streams add up, plug them into the <a href="/tools/income-stream-simulator/">income stream simulator</a>.</p>
    <p>Retake the quiz every few months. As your audience grows and you add owned channels, your score and your best-fit streams will change.</p>
  </div>
</section>

<?php
faq_block([
    ['How long does the monetization quiz take?', '<p>About two minutes. There are 10 multiple-choice questions and you get your results instantly. Nothing is stored or sent anywhere.</p>'],
    ['Can I monetize with a small following?', '<p>Yes. UGC, affiliate links and small paid collaborations work with a few hundred to a few thousand engaged followers. The quiz will point you toward the streams that do not need a big audience.</p>'],
    ['Is the readiness score accurate?', '<p>It is a structured self-assessment, not a guarantee. It highlights the gaps (like a missing media kit or no owned audience) that most often hold creators back from earning.</p>'],
]);
more_tools($slug);
cta_band('Want a personal monetization plan?', 'Share your quiz result with Monetizing Influencers and we will outline the income streams and first steps that fit your channel.');
page_end();
