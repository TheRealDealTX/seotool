<?php
$GLOBALS['schema'][] = [
    '@type' => 'Product', '@id' => abs_url('/gonzales-modern-living/') . '#plan',
    'name' => 'Gonzales Modern Living — 2 Bedroom Small House Plan',
    'description' => 'Two-story, two-bedroom small house plan with a powder room downstairs, full bath upstairs, study/home office, mini bar kitchen, walk-in closet and patio.',
    'image' => [abs_url(img_url('3.webp')), abs_url(img_url('4.webp'))],
    'brand' => ['@id' => SITE_URL . '/#business'],
    'offers' => ['@type' => 'Offer', 'price' => '1000', 'priceCurrency' => 'USD', 'availability' => 'https://schema.org/InStock',
                 'url' => abs_url('/gonzales-modern-living/'), 'seller' => ['@id' => SITE_URL . '/#business']],
];
hero([
    'eyebrow' => 'Featured House Design',
    'h1' => 'Gonzales Modern Living: 2-Bedroom Small House Plan',
    'lead' => 'A cozy, modern contemporary small home that makes every inch count — two bedrooms, a study, a mini bar kitchen and warm natural finishes in a compact two-story footprint.',
    'image' => '3.webp',
    'cta' => false,
]);
?>
<section class="section">
  <div class="wrap content-grid">
    <article class="prose">
      <div class="gallery-2">
        <img src="/assets/img/3.webp" alt="Living room in the Gonzales Modern Living plan with wood-look floors and staircase gallery wall" width="500" height="333">
        <img src="/assets/img/4.webp" alt="Kitchen with two-seat mini bar and stair treads in the Gonzales Modern Living plan" width="500" height="333">
      </div>
      <h2>A Small House That Lives Large</h2>
      <p>The Gonzales Modern Living (Number Two) is designed for people who want to experience a cozy, modern contemporary interior without paying for space they will never use. Its carefully planned layout maximizes every inch and keeps day-to-day living functional and comfortable.</p>
      <p>Wood-textured flooring and stair treads give the home a natural feel, while earth-tone hues create a warm, inviting atmosphere. It is a great home for couples, small families, downsizers or anyone who values quality living in a modest space.</p>

      <h2>Floor Plan Highlights</h2>
      <h3>Ground floor</h3>
      <ul class="checklist">
        <li><strong>Kitchen with a two-seat mini bar</strong> — perfect for breakfast or a quick snack, with ample storage for everything you cook.</li>
        <li><strong>Open living area</strong> that flows from the kitchen, with room for a sofa, media wall and gallery-style stair display.</li>
        <li><strong>Powder room</strong> on the main level for guests and everyday convenience.</li>
        <li><strong>Patio</strong> to extend living outdoors — a must in the Texas shoulder seasons.</li>
      </ul>
      <h3>Upper floor</h3>
      <ul class="checklist">
        <li><strong>Two bedrooms</strong> upstairs for privacy and a quiet night's rest, each with its own closet space.</li>
        <li><strong>Walk-in closet</strong> for serious storage.</li>
        <li><strong>Study / home office</strong> — a separate space for remote work, school or hobbies.</li>
        <li><strong>Full bathroom</strong> serving both bedrooms.</li>
      </ul>

      <h2>Why It Works</h2>
      <p>Stacking the bedrooms over the living space keeps the footprint small, which lowers foundation and roofing costs and leaves more of your lot for yard, parking or a garden. Putting the powder room downstairs means guests never wander through private space, and giving the office its own room upstairs separates work from home in a way a corner desk never can.</p>
      <p>The Gonzales plan is a strong fit as a primary small home on an infill lot, a second home on rural land, or — where local rules allow a two-story accessory unit — a roomy backyard ADU for family or long-term renters.</p>

      <h2>Make It Yours</h2>
      <p>Like every Cowboy Tiny Homes design, the Gonzales Modern Living can be adapted. Common changes include a main-floor bedroom for aging in place, a larger covered porch, a metal roof and stone wainscot for a Hill Country look, or added insulation and shading for west-facing lots. Our team makes sure your home is not only beautiful, but designed for function and comfort.</p>
      <p>Ready to discover the joys of small house living? Cowboy Tiny Homes is here to help you turn that dream into a reality — whether you want the full design-build service or just the plans.</p>
    </article>
    <aside class="sidebar">
      <div class="side-box">
        <h2>Plan Details</h2>
        <ul>
          <li class="kv">Price starts at <strong>$1,000</strong></li>
          <li class="kv">Bedrooms: <strong>2</strong></li>
          <li class="kv">Bathrooms: <strong>1 full + powder room</strong></li>
          <li class="kv">Floors: <strong>2</strong></li>
          <li class="kv">Extras: <strong>walk-in closet, office, patio</strong></li>
        </ul>
      </div>
      <div class="side-box side-box--cta">
        <h2>Interested in This Plan?</h2>
        <p>Choose full design &amp; build, or just a remodel inspired by it.</p>
        <a class="btn btn--gold" href="/contact-us/?project=Gonzales+Modern+Living&amp;note=Interested+in+the+Gonzales+Modern+Living+plan">Design &amp; Build</a>
        <a class="btn btn--ghost" href="/contact-us/?project=remodel">Remodel</a>
      </div>
      <div class="side-box">
        <h2>Price It Out</h2>
        <ul>
          <li><a href="/tools/tiny-home-cost-calculator/?type=custom&amp;size=900&amp;finish=standard">Estimate build cost</a></li>
          <li><a href="/tools/tiny-home-loan-calculator/">Estimate monthly payment</a></li>
          <li><a href="/home-designs/">See all house designs</a></li>
        </ul>
      </div>
    </aside>
  </div>
</section>
<?php
faq_section([
    ['How many bedrooms does the Gonzales Modern Living have?', '<p>Two bedrooms, both on the upper floor, plus a separate study or home office.</p>'],
    ['How many bathrooms are in the Gonzales plan?', '<p>A full bathroom upstairs that serves both bedrooms, and a powder room on the ground floor.</p>'],
    ['Can the Gonzales Modern Living be built as an ADU?', '<p>Often, yes, where your city allows two-story accessory dwellings of this size. Some cities limit ADU height or square footage, so we confirm the rules for your lot in the feasibility study.</p>'],
    ['What does "price starts at $1,000" include?', '<p>It is the starting price for the plan. Construction is quoted separately based on your site, finishes and location. Contact us for a full design-build estimate.</p>'],
], 'Gonzales Modern Living FAQs');
related(['/home-designs/', '/custom-tiny-homes-texas/', '/adu-builders-texas/'], 'More Designs & Home Types');
cta_band('Build the Gonzales in Texas', 'Talk with Cowboy Tiny Homes about building this plan on your land, or customizing it to fit.');
