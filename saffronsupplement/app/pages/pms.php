<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Saffron for PMS is backed by a small but well-designed trial: 15 mg twice daily reduced both physical and emotional premenstrual symptoms over two cycles. Here\'s how to use it, and when to see a doctor instead.', 'Benefits &middot; PMS');
?>
<div class="wrap layout">
  <article class="prose">
    <div class="keyfacts">
      <h2>Key takeaways</h2>
      <ul>
        <li><strong>15 mg twice daily</strong> (30 mg/day) reduced PMS symptom scores vs placebo.</li>
        <li>Results appeared over <strong>two menstrual cycles</strong>.</li>
        <li>Saffron helped with <strong>mood symptoms</strong> (irritability, low mood) as well as overall symptom totals.</li>
        <li>Avoid high-dose saffron if you are pregnant or trying to conceive.</li>
      </ul>
    </div>
    <?= toc(['research' => 'The PMS research', 'symptoms' => 'Which symptoms improved', 'take' => 'How to take it', 'pmdd' => 'PMS vs PMDD', 'picks' => 'Best saffron for PMS', 'faq' => 'FAQ']) ?>

    <h2 id="research">What the PMS Research Shows</h2>
    <p>In a double-blind trial, 50 women aged 20–45 with regular cycles and PMS took either 15 mg of saffron twice daily or a placebo for two menstrual cycles (Agha-Hosseini 2008). The saffron group showed significantly greater reductions in total PMS symptom scores and in depression scores. Around three-quarters of the saffron group had at least a 50% reduction in symptoms, compared with very few in the placebo group.</p>
    <p>A later review of herbal treatments for PMS listed saffron among the herbs with promising evidence, while calling for larger trials.</p>

    <h2 id="symptoms">Which Symptoms Improved?</h2>
    <ul>
      <li>Irritability and mood swings</li>
      <li>Low mood and tearfulness</li>
      <li>Overall total symptom scores, which included physical symptoms</li>
    </ul>

    <h2 id="take">How to Take Saffron for PMS</h2>
    <ol class="steps">
      <li><strong>Dose:</strong> 15 mg twice daily (morning and evening) with food.</li>
      <li><strong>Duration:</strong> the trial gave saffron continuously through two full cycles, not just the week before your period.</li>
      <li><strong>Track symptoms:</strong> record mood and symptoms daily across cycles. Our <a href="/tools/saffron-mood-sleep-tracker/">mood tracker</a> works well for this.</li>
      <li><strong>Pause if pregnant:</strong> stop saffron supplements if you become pregnant, and tell your doctor.</li>
    </ol>
    <?= product_inline('source-naturals', '15 mg tablets match the twice-daily PMS trial protocol exactly.') ?>

    <h2 id="pmdd">PMS vs PMDD</h2>
    <p>Premenstrual dysphoric disorder (PMDD) is a severe form of PMS with intense mood symptoms that disrupt daily life. If your symptoms include severe depression, anxiety, rage or thoughts of self-harm in the days before your period, please see a doctor. Effective treatments exist, and saffron has not been tested specifically for PMDD.</p>

    <h2 id="picks">Best Saffron Supplements for PMS</h2>
    <?= aff_note() ?>
    <?= product_card('pink-stork') ?>
    <?= product_card('source-naturals') ?>

    <?= faq_block([
      ['How much saffron should I take for PMS?', '<p>The PMS trial used 15 mg of saffron twice daily (30 mg/day) throughout the menstrual cycle.</p>'],
      ['When should I start taking saffron for PMS?', '<p>In the trial, women took saffron every day across two complete cycles. Starting at the beginning of a cycle and taking it daily is the closest match.</p>'],
      ['Can saffron help with period cramps?', '<p>One small trial of a herbal combination that included saffron reported less period pain, but there is no strong evidence for saffron alone and cramps.</p>'],
      ['Is saffron safe with birth control?', '<p>No interaction between saffron and hormonal contraception is known. Confirm with your pharmacist if you take other medicines.</p>'],
    ]) ?>
    <?= sources([
      'Agha-Hosseini M, et al. Crocus sativus L. (saffron) in the treatment of premenstrual syndrome: a double-blind, randomised and placebo-controlled trial. <em>BJOG.</em> 2008;115(4):515-519.',
      'Hausenblas HA, et al. Saffron (Crocus sativus L.) and major depressive disorder: a meta-analysis. <em>J Integr Med.</em> 2013;11(6):377-383.',
    ]) ?>
    <?= med_note() ?>
  </article>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
