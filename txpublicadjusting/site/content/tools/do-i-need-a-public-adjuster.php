<?php
return [
    'title'       => 'Do I Need a Public Adjuster? Free 2-Minute Quiz',
    'description' => 'Seven honest questions that show whether your Texas property claim needs a public adjuster, or whether you can handle it yourself. Free, instant result.',
    'h1'          => 'Do I need a public adjuster?',
    'lead'        => 'Not every claim needs one. Answer seven quick questions for an honest read on whether outside help is likely to pay for itself, and what to do next either way.',
    'updated'     => '2026-10-13',
    'script'      => '/assets/js/tools/quiz.js',
    'app'         => <<<'HTML'
<div data-quiz>
  <div class="quiz-progress"><span data-out="bar"></span></div>
  <p class="muted" data-out="step">Question 1 of 7</p>
  <div data-out="qs"></div>
  <div class="quiz-result" data-out="result"></div>
  <div class="tbtns"><button type="button" class="btn btn--ghost btn--sm" data-act="back" hidden>Back</button><button type="button" class="btn btn--ghost btn--sm" data-act="restart" hidden>Start over</button></div>
</div>
HTML,
    'body'        => <<<'HTML'
<h2>How the quiz scores your claim</h2>
<p>The questions weigh the factors that most often decide whether a public adjuster adds value: the size and complexity of the loss, how far the insurer's number is from the real repair cost, whether the claim is stuck or denied, and how much time you have to manage it. Small claims that were paid correctly score low, and that's the honest answer.</p>
<div class="compare">
  <div>
    <h3>Usually fine to handle yourself</h3>
    <ul>
      <li>Small, clear damage that the insurer scoped correctly</li>
      <li>The estimate matches your contractor's within a small margin</li>
      <li>Communication is prompt and the deadlines are being met</li>
    </ul>
  </div>
  <div>
    <h3>Worth a professional look</h3>
    <ul>
      <li>Large losses: fire, major water, whole-roof or commercial</li>
      <li>Denials, partial denials or "wear and tear" findings you disagree with</li>
      <li>Big gaps between the insurer's estimate and real repair bids</li>
      <li>Contents inventories, business income or multiple buildings</li>
    </ul>
  </div>
</div>
<p>Whatever your result, the free review is a no-pressure way to get a licensed adjuster's opinion. If your claim doesn't need us, we'll say so. Read more in <a href="/post/should-i-use-a-public-adjuster/">Should I use a public adjuster?</a></p>
HTML,
    'faqs' => [
        ['q' => 'Is this quiz a substitute for a claim review?', 'a' => 'No. It\'s a quick screening based on common patterns. A licensed adjuster reviewing your policy and estimate can give you a real answer.'],
        ['q' => 'Do you save my answers?', 'a' => 'No. The quiz runs entirely in your browser and nothing is sent to us.'],
    ],
    'related' => ['/post/should-i-use-a-public-adjuster/', '/post/the-truth-about-public-adjuster-fees/', '/post/when-is-it-too-late-to-hire-a-public-adjuster/'],
];
