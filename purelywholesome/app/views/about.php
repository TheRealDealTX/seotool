<?php /** @var array $crumbs */
$heroTitle = 'About Purely Wholesome Farm'; $heroEyebrow = 'Our story';
$heroLede = 'Farming is a journey, and we’re here for every step: from the first brood of chicks to the hundredth jar of pickles.';
include __DIR__ . '/partials/page-hero.php';
$counts = array_count_values(array_column(live_posts(), 'topic')); ?>
<section class="section section--tight">
  <div class="wrap about">
    <div class="prose about__copy">
      <p class="dropcap">At Purely Wholesome Farm, we believe farming is more than planting seeds or raising animals. It is about nurturing the land, respecting nature’s cycles and putting good food on the table. We are blessed to live in a supportive farming community where pride in land stewardship is a way of life, and when the rest of the world seems chaotic, it’s nice to know we have a little piece of heaven.</p>
      <p>This site is where we share what that life actually looks like: the brine ratio that finally gave us juicy chicken every time, the sides we serve with lamb chops when company is coming, how we keep the water trough open in January, and everything we have learned (sometimes the hard way) about goats, hens and a well-stocked pantry.</p>
      <h2>What you’ll find here</h2>
      <ul>
        <li><strong>Farm kitchen recipes</strong> for lamb, brined poultry, pumpkin pie, sourdough and scratch baking.</li>
        <li><strong>Livestock guides</strong> for raising dairy goats and backyard chickens, from kidding season to winter care.</li>
        <li><strong>Canning and preserving</strong> walkthroughs built on tested, safe methods.</li>
        <li><strong>Free interactive tools</strong> that handle the math: <a href="/tools/brine-calculator/">brine ratios</a>, <a href="/tools/lamb-cooking-calculator/">lamb temperatures</a>, <a href="/tools/goat-gestation-calculator/">goat due dates</a> and more.</li>
      </ul>
      <h2>What we stand for</h2>
      <p><strong>Practicality over theory.</strong> Every guide should leave you with something you can do today. <strong>Accuracy.</strong> Food safety and animal health details are checked against USDA, extension and veterinary references, and we say so when something is our experience rather than settled science. <strong>Readers first.</strong> We no longer accept paid guest posts; the archive’s older partner articles are clearly labeled.</p>
      <p>Read more about how we write and update articles in our <a href="/editorial-policy/">editorial policy</a>, or <a href="/contact-us/">drop us a line</a>. We read every message.</p>
    </div>
    <aside class="about__aside">
      <div class="about__card">
        <h2>Purely Wholesome Farm at a glance</h2>
        <ul class="about__list">
          <?php foreach (TOPICS as $k => [$label]): if (empty($counts[$k])) continue; ?><li><a href="/topics/<?= $k ?>/"><?= e($label) ?></a><span><?= (int)$counts[$k] ?></span></li><?php endforeach ?>
        </ul>
        <a class="btn btn--primary" href="/blog/">Start reading <?= icon('arrow') ?></a>
      </div>
    </aside>
  </div>
</section>
