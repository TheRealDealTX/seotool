<section class="hero">
  <div class="hero-inner">
    <div class="hero-copy">
      <span class="pill"><?= icon('sparkle') ?> Free for renters</span>
      <h1>Find a roommate who wants <em>the same apartment</em> you do.</h1>
      <p class="lead">Pick the properties you love, and we'll match you with renters interested in the same place — scored on budget, move-in date and lifestyle. Then add them as friends and start chatting.</p>
      <div class="hero-cta">
        <a class="btn btn-primary btn-lg" href="/register">Create your free profile</a>
        <a class="btn btn-ghost btn-lg" href="/login">I already have an account</a>
      </div>
      <div class="hero-stats">
        <div><strong><?= number_format($stats['members']) ?></strong><span>renters</span></div>
        <div><strong><?= number_format($stats['properties']) ?></strong><span>properties</span></div>
        <div><strong>100%</strong><span>free</span></div>
      </div>
    </div>
    <div class="hero-art" aria-hidden="true">
      <div class="mock-card m1"><span class="avatar avatar-md avatar-initials" style="--h:250">JM</span><div><strong>Jordan, 26</strong><small>Night owl · Tidy · $900–1,200</small></div><span class="score great">92%</span></div>
      <div class="mock-card m2"><span class="avatar avatar-md avatar-initials" style="--h:340">AR</span><div><strong>Alex, 24</strong><small>Same apartment property</small></div><span class="score great">87%</span></div>
      <div class="mock-card m3"><span class="avatar avatar-md avatar-initials" style="--h:150">SK</span><div><strong>Sam, 29</strong><small>Non-smoker · Pet friendly</small></div><span class="score good">71%</span></div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-title">How it works</h2>
  <div class="steps">
    <div class="step card"><span class="step-n">1</span><h3>Build your profile</h3><p>Budget, move-in date, sleep schedule, cleanliness, pets — the things that actually matter when you share a home.</p></div>
    <div class="step card"><span class="step-n">2</span><h3>Pick your properties</h3><p>Choose the apartment communities you're interested in, or add one. You'll see everyone else eyeing the same place.</p></div>
    <div class="step card"><span class="step-n">3</span><h3>Match, friend &amp; chat</h3><p>Browse compatibility scores, send friend requests, message each other and post in the community feed.</p></div>
  </div>
</section>

<?php if ($featured): ?>
<section class="section">
  <h2 class="section-title">Popular properties</h2>
  <div class="grid grid-3">
    <?php foreach ($featured as $p): partial('partials/property_card', ['p' => $p, 'guest' => true]); endforeach; ?>
  </div>
</section>
<?php endif; ?>

<section class="section">
  <div class="cta-band card">
    <div><h2>Your next roommate is already looking.</h2><p>It takes two minutes to set up a profile.</p></div>
    <a class="btn btn-light btn-lg" href="/register">Get started</a>
  </div>
</section>
