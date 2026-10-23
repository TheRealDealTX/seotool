<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Short, evidence-based answers to the questions we get asked most about saffron supplements. Each answer links to a deeper guide.', 'FAQ');
?>
<div class="wrap layout">
  <div class="prose">
    <?= faq_block([
      ['What is a saffron supplement?', '<p>A capsule, tablet or softgel containing a concentrated extract of saffron (<em>Crocus sativus</em>) stigmas, standardized for active compounds such as crocins and safranal.</p>'],
      ['What are the main benefits of saffron?', '<p>The strongest evidence is for mild-to-moderate low mood. Moderate evidence supports stress and anxiety, sleep quality and early macular degeneration; smaller studies cover PMS, sexual function and appetite. <a href="/saffron-benefits/">See all benefits</a>.</p>'],
    ], 'Basics') ?>
    <?= faq_block([
      ['How much saffron should I take per day?', '<p>Usually 28–30 mg of extract. Use 20 mg for eye health and 176.5 mg of Satiereal® for appetite. <a href="/saffron-dosage/">Dosage guide</a>.</p>'],
      ['When is the best time to take saffron?', '<p>Split morning and evening with food for mood; evening for sleep; before meals for appetite.</p>'],
      ['How long does saffron take to work?', '<p>2–4 weeks for sleep, 4–8 weeks for mood, about 3 months for eye measures.</p>'],
      ['Can I take saffron every day long-term?', '<p>Trials have lasted up to about 14 months at 20 mg/day. Review long-term use with your doctor and consider periodic breaks.</p>'],
      ['Should I cycle saffron?', '<p>There\'s no evidence that cycling is needed. Some people take a short break every few months to check whether they still benefit.</p>'],
    ], 'Dosage & Timing') ?>
    <?= faq_block([
      ['Is saffron safe?', '<p>At 20–30 mg/day it is well tolerated in trials. Side effects are uncommon and mild. <a href="/saffron-side-effects/">Safety guide</a>.</p>'],
      ['Can I take saffron while pregnant?', '<p>Avoid saffron supplements during pregnancy unless your obstetrician approves. High doses may stimulate the uterus.</p>'],
      ['Does saffron interact with medications?', '<p>Possibly with antidepressants, blood thinners, blood-pressure and diabetes medicines, and sedatives. Try the <a href="/tools/saffron-safety-checker/">safety checker</a>.</p>'],
      ['Can saffron cause weight gain?', '<p>Not that we know of. If anything, saffron tends to reduce appetite slightly.</p>'],
      ['Is saffron addictive?', '<p>No. There is no evidence of dependence or withdrawal.</p>'],
    ], 'Safety') ?>
    <?= faq_block([
      ['What is the best saffron supplement?', '<p>A research-dose, standardized extract from a tested brand. Our top pick is ' . amz('B0B69MGMFW', 'Nootropics Depot Saffron 30 mg') . '. <a href="/best-saffron-supplements/">See all 12 reviews</a>.</p>'],
      ['What\'s the difference between affron and Satiereal?', '<p>affron® is studied for mood, stress and sleep at 28 mg; Satiereal® for appetite at 176.5 mg. <a href="/affron-vs-satiereal/">Full comparison</a>.</p>'],
      ['How can I tell if a saffron supplement is real?', '<p>Look for a branded extract or stated crocin/safranal percentages, third-party testing and a realistic price. <a href="/how-to-choose-a-saffron-supplement/">Buying checklist</a>.</p>'],
      ['Are saffron gummies effective?', '<p>They can contain saffron, but dosing is usually less precise and they often add sugar and other herbs. Capsules are closer to the research.</p>'],
      ['Can I just eat saffron instead of taking a supplement?', '<p>Culinary saffron is healthy and delicious, but its active-compound content varies, so it\'s hard to match trial doses. Browse ' . amz('grade 1 saffron threads', 'quality saffron threads') . ' for cooking.</p>'],
    ], 'Buying') ?>
    <?= faq_block([
      ['Does saffron help with anxiety?', '<p>A 2019 meta-analysis found saffron reduced anxiety symptoms vs placebo. <a href="/saffron-for-depression-and-mood/#anxiety">Read more</a>.</p>'],
      ['Does saffron increase libido?', '<p>Small trials found saffron improved antidepressant-related sexual side effects in men and women. Evidence in other groups is limited.</p>'],
      ['Does saffron help with ADHD?', '<p>A small trial in children compared saffron with methylphenidate, but evidence is very limited. Don\'t use saffron in place of ADHD treatment.</p>'],
    ], 'Specific Uses') ?>
    <?= med_note() ?>
  </div>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
