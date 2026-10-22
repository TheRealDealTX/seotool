<?php
defined('CCPA_ROOT') || exit;
/** Texas claim deadline calculator (Prompt Payment of Claims Act + TWIA timelines). */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
// Rules: from = which date it counts from; unit = days | biz | years; cat = extra days after a declared catastrophe.
$rules = [
    // Texas Prompt Payment of Claims Act (Tex. Ins. Code ch. 542, subch. B)
    ['applies' => ['private'], 'from' => 'notice', 'fromLabel' => 'date you reported the claim', 'n' => 15, 'unit' => 'days', 'cat' => 15,
     'label' => 'Insurer must acknowledge the claim, begin its investigation, and request what it needs', 'note' => 'Tex. Ins. Code §542.055 — 15 days after notice (extended 15 days after a declared weather catastrophe, §542.059).'],
    ['applies' => ['private'], 'from' => 'docs', 'fromLabel' => 'date the insurer received all requested items', 'n' => 15, 'unit' => 'biz', 'cat' => 15,
     'label' => 'Insurer must accept or reject the claim in writing', 'note' => 'Tex. Ins. Code §542.056 — 15 business days after receiving everything it requested. If it notifies you it needs more time, it then has up to 45 days.'],
    ['applies' => ['private'], 'from' => 'docs', 'fromLabel' => 'date the insurer received all requested items', 'n' => 15, 'unit' => 'biz', 'plus' => 45, 'cat' => 15,
     'label' => 'Outside date if the insurer gave notice it needed more time', 'note' => 'Tex. Ins. Code §542.056(d) — up to 45 days after its notice; shown here counted from the 15-business-day mark.'],
    ['applies' => ['private'], 'from' => 'decision', 'fromLabel' => 'date of the written decision', 'n' => 5, 'unit' => 'biz', 'cat' => 15,
     'label' => 'Payment due on an accepted claim', 'note' => 'Tex. Ins. Code §542.057 — 5 business days after notifying you of acceptance (surplus lines insurers have longer).'],
    // TWIA (Tex. Ins. Code ch. 2210, subch. L-1)
    ['applies' => ['twia'], 'from' => 'loss', 'fromLabel' => 'date of loss', 'n' => 1, 'unit' => 'years',
     'label' => 'Last day to file a TWIA claim', 'note' => 'Tex. Ins. Code §2210.573(a) — one year after the damage occurs; the commissioner may extend up to 180 days for good cause (§2210.205(b)).'],
    ['applies' => ['twia'], 'from' => 'notice', 'fromLabel' => 'date you reported the claim', 'n' => 30, 'unit' => 'days',
     'label' => 'TWIA may request missing information', 'note' => 'Tex. Ins. Code §2210.573(b) — within 30 days after the claim is filed.'],
    ['applies' => ['twia'], 'from' => 'docs', 'fromLabel' => 'date TWIA received the claim or requested information', 'n' => 60, 'unit' => 'days',
     'label' => 'TWIA must accept, partly accept, or deny in writing', 'note' => 'Tex. Ins. Code §2210.573(d) — 60 days after receiving the claim or requested information, whichever is later; the commissioner may extend it (§2210.581).'],
    ['applies' => ['twia'], 'from' => 'decision', 'fromLabel' => 'date of TWIA\'s written decision', 'n' => 10, 'unit' => 'days',
     'label' => 'TWIA payment due on the accepted amount', 'note' => 'Tex. Ins. Code §2210.5731 — 10 days after the acceptance notice.'],
    ['applies' => ['twia'], 'from' => 'decision', 'fromLabel' => 'date of TWIA\'s written decision', 'n' => 60, 'unit' => 'days',
     'label' => 'Last day to demand appraisal of the amount of loss', 'note' => 'Tex. Ins. Code §2210.574(b) — 60 days after receiving an acceptance or partial-acceptance notice.'],
    ['applies' => ['twia'], 'from' => 'decision', 'fromLabel' => 'date of TWIA\'s written decision', 'n' => 2, 'unit' => 'years',
     'label' => 'Outside deadline to sue over a TWIA denial', 'note' => 'Tex. Ins. Code §2210.577 — two years after receiving a partial or full denial (statute of repose). A notice of intent to sue and possible ADR come first (§2210.575). Talk to a Texas attorney.'],
];
?>
<section class="section section-alt" aria-labelledby="dl-h">
  <div class="container">
    <div class="tool-layout" data-deadline-calc data-rules="<?= e(json_encode($rules)) ?>">
      <form class="tool-panel" novalidate onsubmit="return false">
        <h2 id="dl-h">Your claim dates</h2>
        <p class="small muted">Enter the dates you know. Everything runs in your browser&mdash;nothing is sent to us.</p>
        <div class="form-grid">
          <div class="field field-full"><label for="dl-kind">Who insures the damage?</label>
            <select id="dl-kind" name="kind">
              <option value="private">Homeowners or commercial insurer (Texas Insurance Code ch. 542)</option>
              <option value="twia">TWIA windstorm policy (Texas Insurance Code ch. 2210)</option>
            </select></div>
          <div class="field"><label for="dl-loss">Date of loss</label><input id="dl-loss" name="loss" type="date"></div>
          <div class="field"><label for="dl-notice">Date you reported the claim</label><input id="dl-notice" name="notice" type="date"></div>
          <div class="field"><label for="dl-docs">Date insurer received all items it requested <span class="opt">(optional)</span></label><input id="dl-docs" name="docs" type="date"></div>
          <div class="field"><label for="dl-decision">Date of the insurer's written decision <span class="opt">(optional)</span></label><input id="dl-decision" name="decision" type="date"></div>
          <div class="field field-full field-check"><input id="dl-cat" name="cat" type="checkbox"><label for="dl-cat">The loss was part of a <strong>weather-related catastrophe or major natural disaster</strong> declared by the Texas insurance commissioner (adds time to some deadlines).</label></div>
        </div>
      </form>
      <div class="tool-panel results" aria-live="polite">
        <h2>Your timeline</h2>
        <ul class="deadline-list" data-deadlines></ul>
        <div class="tool-actions no-print"><button class="btn btn-gold btn-sm" type="button" onclick="window.print()"><?= icon('printer', 'icon icon-sm') ?> Print timeline</button></div>
      </div>
    </div>
    <div class="tool-panel explain" style="margin-top:28px">
      <p class="disclaimer-box mb-0"><strong>Educational estimate only&mdash;not legal advice.</strong> Statutory deadlines have exceptions (for example, an insurer may notify you it needs more time, surplus lines insurers follow different rules, and holidays can shift business-day counts). Policy deadlines and deadlines to file suit vary; consult a Texas attorney about legal deadlines. Sources are listed below.</p>
    </div>
    <?php component('cta-band', ['heading' => 'Is your insurer missing its deadlines?']); ?>
  </div>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
    </article>
    <aside class="sidebar"><?php include CCPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
