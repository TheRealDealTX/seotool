<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Saffron for eye health is one of the most interesting areas of saffron research. Small trials in early age-related macular degeneration (AMD) found that 20 mg a day improved how well the retina responds to light. Here\'s what that means, and how saffron fits alongside AREDS2 vitamins.', 'Benefits &middot; Eye Health');
?>
<div class="wrap layout">
  <article class="prose">
    <div class="keyfacts">
      <h2>Key takeaways</h2>
      <ul>
        <li>Trials used <strong>20 mg of saffron a day</strong> for about 3 months.</li>
        <li>Saffron improved <strong>retinal flicker sensitivity</strong> in early AMD; one trial also found small gains in visual acuity.</li>
        <li>Saffron <strong>does not replace AREDS2</strong>, which has the strongest evidence for slowing AMD.</li>
        <li>Always discuss supplements with your eye doctor.</li>
      </ul>
    </div>
    <?= toc(['what' => 'What is AMD?', 'research' => 'The saffron eye research', 'areds' => 'Saffron vs AREDS2', 'take' => 'How to take it', 'picks' => 'Best saffron for eyes', 'faq' => 'FAQ']) ?>

    <h2 id="what">What Is Age-Related Macular Degeneration?</h2>
    <p>AMD damages the macula, the small central part of the retina responsible for sharp, detailed vision. It is a leading cause of vision loss in people over 50. "Dry" AMD progresses slowly; "wet" AMD involves abnormal blood vessels and needs urgent treatment. Saffron has only been studied in early and mild-to-moderate <em>dry</em> AMD.</p>

    <h2 id="research">What the Saffron Eye Research Shows</h2>
    <ul>
      <li><strong>Falsini et al. (2010):</strong> 25 people with early AMD took 20 mg saffron or placebo for 3 months each in a crossover design. Saffron improved retinal flicker sensitivity, a measure of macular function.</li>
      <li><strong>Piccardi et al. (2012):</strong> 29 patients took 20 mg/day for an average of 14 months. Improvements in retinal sensitivity and visual acuity appeared after 3 months and were maintained.</li>
      <li><strong>Broadhead et al. (2019):</strong> an Australian crossover trial of 100 people with mild/moderate AMD found modest improvements in visual function with 20 mg/day, including in people already taking AREDS supplements.</li>
    </ul>
    <p>Researchers suggest saffron's crocin and crocetin protect light-sensing cells from oxidative stress and help regulate how they respond to light damage.</p>

    <h2 id="areds">Saffron vs AREDS2: Which Should You Take?</h2>
    <div class="table-wrap"><table>
      <thead><tr><th></th><th>AREDS2 formula</th><th>Saffron 20 mg</th></tr></thead>
      <tbody>
        <tr><td>Evidence</td><td>Large NIH trials (4,000+ people)</td><td>Small trials (25–100 people)</td></tr>
        <tr><td>Proven outcome</td><td>Slows progression to advanced AMD</td><td>Improves retinal function measures</td></tr>
        <tr><td>Who it's for</td><td>Intermediate AMD or advanced AMD in one eye</td><td>Early to mild/moderate dry AMD (studied)</td></tr>
        <tr><td>Can combine?</td><td colspan="2">Broadhead 2019 included participants taking both. Ask your ophthalmologist.</td></tr>
      </tbody>
    </table></div>
    <p>AREDS2 is the standard of care for intermediate AMD. Saffron is best viewed as a possible add-on, not a replacement. Browse <?= amz('areds 2 eye vitamins lutein zeaxanthin', 'AREDS2 lutein &amp; zeaxanthin formulas on Amazon') ?>.</p>

    <h2 id="take">How to Take Saffron for Eye Health</h2>
    <ol class="steps">
      <li><strong>Dose:</strong> 20 mg of saffron extract once daily, the dose used in all three trials.</li>
      <li><strong>With a meal</strong> to reduce stomach upset.</li>
      <li><strong>Be patient:</strong> trials measured changes after about 3 months.</li>
      <li><strong>Keep your eye exams:</strong> regular checks (including an Amsler grid at home) matter far more than any supplement.</li>
    </ol>
    <p class="note">Few saffron supplements come in exactly 20 mg. Most are 28–30 mg, slightly above the eye-trial dose but within the range used safely in mood research. Ask your eye doctor what is reasonable for you, and use our <a href="/tools/saffron-dosage-calculator/">dosage calculator</a> to work out capsule counts.</p>

    <h2 id="picks">Best Saffron Supplements for Eye Health</h2>
    <?= aff_note() ?>
    <?= product_card('now-foods') ?>
    <?= product_inline('nootropics-depot', 'Crocin-standardized 30 mg extract. Crocin is the compound linked to retinal protection.') ?>
    <?= product_inline('source-naturals', '15 mg tablets let you get closer to the studied 20 mg dose.') ?>

    <?= faq_block([
      ['Can saffron reverse macular degeneration?', '<p>No. Saffron improved retinal function measures in small trials but has not been shown to reverse AMD or prevent progression to advanced disease.</p>'],
      ['How much saffron is good for eyes?', '<p>All the main AMD trials used 20 mg of saffron a day.</p>'],
      ['Can I take saffron with AREDS2?', '<p>One trial included people taking AREDS supplements and saffron together without problems. Check with your ophthalmologist before combining them.</p>'],
      ['Does saffron help with glaucoma or dry eye?', '<p>There is very early research on glaucoma, but not enough to recommend saffron for it. Keep using the treatments your eye doctor prescribes.</p>'],
    ]) ?>
    <?= sources([
      'Falsini B, et al. Influence of saffron supplementation on retinal flicker sensitivity in early age-related macular degeneration. <em>Invest Ophthalmol Vis Sci.</em> 2010;51(12):6118-6124.',
      'Piccardi M, et al. A longitudinal follow-up study of saffron supplementation in early age-related macular degeneration. <em>Evid Based Complement Alternat Med.</em> 2012;2012:429124.',
      'Broadhead GK, et al. Saffron therapy for the treatment of mild/moderate age-related macular degeneration: a randomised clinical trial. <em>Graefes Arch Clin Exp Ophthalmol.</em> 2019;257(1):31-40.',
      'Age-Related Eye Disease Study 2 Research Group. Lutein + zeaxanthin and omega-3 fatty acids for age-related macular degeneration. <em>JAMA.</em> 2013;309(19):2005-2015.',
    ]) ?>
    <?= med_note() ?>
  </article>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
