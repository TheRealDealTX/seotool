<?php
// Gonzales Modern Living: the original featured design, now a full catalog plan. It keeps
// its URL, H1 and story from the WordPress-era page; everything else comes from pages/plan.php.
$GLOBALS['plan_h1'] = 'Gonzales Modern Living: 2-Bedroom Small House Plan';
$GLOBALS['plan_story'] = function () { ?>
<section class="section section--alt">
  <div class="wrap content-grid">
    <article class="prose">
      <h2>A Small House That Lives Large</h2>
      <p>The Gonzales Modern Living (Number Two) is designed for people who want to experience a cozy, modern contemporary interior without paying for space they will never use. Its carefully planned layout maximizes every inch and keeps day-to-day living functional and comfortable.</p>
      <p>Wood-textured flooring and stair treads give the home a natural feel, while earth-tone hues create a warm, inviting atmosphere. It is a great home for couples, small families, downsizers or anyone who values quality living in a modest space.</p>
      <h3>Ground floor</h3>
      <ul>
        <li><strong>Kitchen with a two-seat mini bar</strong> at the island — perfect for breakfast or a quick snack, with ample storage for everything you cook.</li>
        <li><strong>Open living area</strong> that flows from the kitchen, with room for a sofa, media wall and gallery-style stair display.</li>
        <li><strong>Powder room</strong> on the main level for guests and everyday convenience, next to a utility room for the washer, dryer and water heater.</li>
        <li><strong>Covered patio</strong> to extend living outdoors — a must in the Texas shoulder seasons.</li>
      </ul>
      <h3>Upper floor</h3>
      <ul>
        <li><strong>Two bedrooms</strong> upstairs for privacy and a quiet night's rest.</li>
        <li><strong>Walk-in closet</strong> off the primary bedroom for serious storage.</li>
        <li><strong>Study / home office</strong> — a separate room for remote work, school or hobbies.</li>
        <li><strong>Full bathroom</strong> serving both bedrooms, stacked over the utility room to keep the plumbing short.</li>
      </ul>
      <h2>Why It Works</h2>
      <p>Stacking the bedrooms over the living space keeps the footprint small, which lowers foundation and roofing costs and leaves more of your lot for yard, parking or a garden. Putting the powder room downstairs means guests never wander through private space, and giving the office its own room upstairs separates work from home in a way a corner desk never can.</p>
      <p>The Gonzales plan is a strong fit as a primary small home on an infill lot, a second home on rural land, or — where local rules allow a two-story accessory unit — a roomy backyard ADU for family or long-term renters.</p>
      <h2>Make It Yours</h2>
      <p>Like every Cowboy Tiny Homes design, the Gonzales Modern Living can be adapted. Common changes include a main-floor bedroom for aging in place, a larger covered porch, a metal roof and stone wainscot for a Hill Country look, or added insulation and shading for west-facing lots. Our team makes sure your home is not only beautiful, but designed for function and comfort.</p>
      <p>Ready to discover the joys of small house living? Cowboy Tiny Homes is here to help you turn that dream into a reality — whether you want the full design-build service or just the plans.</p>
    </article>
    <aside class="sidebar">
      <figure class="img-frame"><img src="<?= img_url('3.webp') ?>" alt="Gonzales Modern Living living room with the stair and gallery wall" width="500" height="333" loading="lazy"></figure>
      <figure class="img-frame" style="margin-top:18px"><img src="<?= img_url('4.webp') ?>" alt="Gonzales Modern Living kitchen with the two-seat mini bar" width="500" height="333" loading="lazy"></figure>
      <p class="form-note">Interior renderings of the Gonzales Modern Living finishes.</p>
    </aside>
  </div>
</section>
<?php };
require __DIR__ . '/plan.php';
