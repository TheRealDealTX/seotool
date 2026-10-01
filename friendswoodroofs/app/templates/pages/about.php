<?php defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
partial('page-hero', [
    'eyebrow' => 'About us',
    'title'   => 'About Friendswood Roofers',
    'lead'    => 'Friendswood Roofers is a roofing company focused on one thing: helping Friendswood homeowners make sound, well-informed decisions about their roofs.',
]); ?>

<section class="section">
  <div class="container split">
    <div class="prose" data-reveal>
      <h2>Focused on Friendswood homes</h2>
      <p>A roof is easy to ignore until something goes wrong, and then it suddenly needs a decision. Friendswood Roofers was set up to make that moment less stressful. We serve homeowners in Friendswood, Texas, and we keep our attention on the kinds of roofs, weather and questions that come up here.</p>
      <p>Friendswood homes face long, hot summers, high humidity, heavy downpours and the June-to-November Atlantic hurricane season. Those conditions shape how roofs wear, where leaks start and which details matter most, such as flashing, ventilation and how a roof is protected if a storm arrives in the middle of a project.</p>
      <p>Our <a href="/services/">roofing services</a> cover the full life of a residential roof: <a href="/services/roof-inspections/">inspections</a>, <a href="/services/roof-repair/">repairs</a>, <a href="/services/roof-maintenance/">maintenance</a>, <a href="/services/storm-damage-roof-repair/">storm damage repair</a> and <a href="/services/roof-replacement/">replacement</a> with <a href="/services/asphalt-shingle-roofing/">asphalt shingles</a> or <a href="/services/metal-roofing/">metal roofing</a>.</p>
    </div>
    <figure class="split-media" data-reveal>
      <?= photo('roofing-crew-trucks', '(min-width: 900px) 45vw, 100vw') ?>
      <figcaption><?= photo_credit('roofing-crew-trucks') ?></figcaption>
    </figure>
  </div>
</section>

<section class="section section--tint" aria-labelledby="approach-heading">
  <div class="container">
    <div class="section-head" data-reveal>
      <p class="eyebrow">Our approach</p>
      <h2 id="approach-heading">A practical way to assess your roof</h2>
      <p>Every recommendation should be something you can see and understand. Here is how we work through a roofing concern.</p>
    </div>
    <ol class="approach-list">
      <li data-reveal>
        <h3>Listen first</h3>
        <p>We start with what you have noticed: where, when and how often. Details like "only during heavy rain from the south" can point straight to the cause.</p>
      </li>
      <li data-reveal>
        <h3>Look at the whole roof</h3>
        <p>A visible problem is not always the source. We check the roof surface, flashing, vents, edges and, when accessible, the attic, because leaks often start somewhere other than where they show up.</p>
      </li>
      <li data-reveal>
        <h3>Show you what we see</h3>
        <p>Photos let you see conditions on a roof you should not climb yourself. We explain what is normal wear, what needs attention now and what can wait.</p>
      </li>
      <li data-reveal>
        <h3>Recommend only what the roof needs</h3>
        <p>If a repair will do the job, we say so. If replacement makes more sense, we explain why with evidence. When it is a close call, we can price both options so you can compare.</p>
      </li>
      <li data-reveal>
        <h3>Put it in writing</h3>
        <p>Your estimate lists the scope, materials and price, and explains how anything that cannot be seen until work begins, such as damaged decking, would be handled.</p>
      </li>
      <li data-reveal>
        <h3>Respect your time and home</h3>
        <p>We confirm schedules, keep you informed when weather causes changes, protect your property during work and clean up when the job is done.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container narrow prose" data-reveal>
    <h2>What we will not do</h2>
    <p>Trust is easier to build when expectations are clear. We will not:</p>
    <ul>
      <li>Pressure you to sign on the spot. A good estimate is still good after you compare it.</li>
      <li>Promise insurance outcomes. Coverage decisions belong to your insurance company.</li>
      <li>Offer to pay or waive your insurance deductible, which Texas law prohibits.</li>
      <li>Ask you to climb onto your roof. Ground-level observations and photos from inside your home are enough to get started.</li>
    </ul>
    <h2>Learn before you call</h2>
    <p>If you are still gathering information, our blog covers <a href="/blog/how-to-choose-a-roofing-contractor-friendswood/">how to choose a roofing contractor</a>, <a href="/blog/roof-repair-or-replacement-friendswood/">repair versus replacement</a> and <a href="/blog/roof-inspection-what-to-expect-friendswood/">what happens during a roof inspection</a>. The <a href="/faqs/">FAQs page</a> answers common questions, and the <a href="/roofing-project-planner/">Roofing Project Planner</a> helps you organize your concern before you reach out.</p>
  </div>
</section>

<?php partial('cta-band', ['title' => 'Have a question about your roof?', 'text' => 'Call or send an estimate request. We will listen, take a look and explain your options clearly.']); ?>
