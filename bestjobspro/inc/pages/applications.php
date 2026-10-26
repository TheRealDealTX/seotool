<?php
$err = [];
$v = [];
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    [$err, $v] = handle_application_form();
}
$sent = isset($_GET['sent']);
page_start([
    'title'       => 'Apply for Jobs in Texas | Online Application | Best Jobs Pro',
    'description' => 'Apply online with Best Jobs Pro in about 5 minutes. Upload your résumé, pick a job and a Texas recruiter will match you with employers. No fees.',
    'path'        => '/applications/',
    'crumbs'      => [['Applications', '/applications/']],
    'robots'      => $err ? 'noindex, follow' : null,
]);
page_hero('Apply for a Job with Best Jobs Pro', 'Send us your application and a recruiter will review it, call you, and start building a career plan around your goals. Then we match you with openings across Texas.', [['Applications', '/applications/']], '/assets/img/site/applications-bg-2.webp', 'Free application');
$jobs = array_merge(array_column(JOBS, 0), ['Other']);
?>
<section class="section">
  <div class="wrap split split--wide" style="align-items:start">
    <div class="form-card reveal in" id="apply-form">
<?php if ($sent): ?>
      <div class="alert alert--ok" role="status"><?= icon('check') ?><p><strong>Thank you, your application was sent.</strong> A Best Jobs Pro recruiter will review it and contact you soon. For anything urgent, call <?= SITE_PHONE ?>.</p></div>
<?php endif; ?>
<?php if (isset($err['form'])): ?>
      <div class="alert alert--err" role="alert"><p><?= e($err['form']) ?></p></div>
<?php elseif ($err): ?>
      <div class="alert alert--err" role="alert"><p>Please fix the highlighted fields below.</p></div>
<?php endif; ?>
      <h2 style="font-size:1.6rem">Job application</h2>
      <p>Fields marked <span class="req" style="color:var(--brand-ink)">*</span> are required. It takes about five minutes.</p>
      <form method="post" action="/applications/#apply-form" enctype="multipart/form-data" novalidate>
        <?= form_guard_fields() ?>
        <input type="hidden" name="MAX_FILE_SIZE" value="<?= RESUME_MAX_BYTES ?>">
        <div class="form-grid form-grid--3">
          <div class="field"><label for="f-first">First name <span class="req">*</span></label><input id="f-first" name="first" autocomplete="given-name" required value="<?= old($v, 'first') ?>"<?= aria_err($err, 'first') ?>><?= field_error($err, 'first') ?></div>
          <div class="field"><label for="f-middle">Middle name</label><input id="f-middle" name="middle" autocomplete="additional-name" value="<?= old($v, 'middle') ?>"></div>
          <div class="field"><label for="f-last">Last name <span class="req">*</span></label><input id="f-last" name="last" autocomplete="family-name" required value="<?= old($v, 'last') ?>"<?= aria_err($err, 'last') ?>><?= field_error($err, 'last') ?></div>
        </div>
        <div class="form-grid" style="margin-top:18px">
          <div class="field"><label for="f-phone">Phone number <span class="req">*</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required value="<?= old($v, 'phone') ?>"<?= aria_err($err, 'phone') ?>><?= field_error($err, 'phone') ?></div>
          <div class="field"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required value="<?= old($v, 'email') ?>"<?= aria_err($err, 'email') ?>><?= field_error($err, 'email') ?></div>
          <div class="field"><label for="f-job">Which job are you applying for? <span class="req">*</span></label>
            <select id="f-job" name="job" required<?= aria_err($err, 'job') ?>>
              <option value="">Select a job</option>
<?php foreach ($jobs as $j): ?>
              <option<?= ($v['job'] ?? '') === $j ? ' selected' : '' ?>><?= e($j) ?></option>
<?php endforeach; ?>
            </select><?= field_error($err, 'job') ?></div>
          <div class="field" id="f-other-wrap"><label for="f-other">If other, please specify</label><input id="f-other" name="other" value="<?= old($v, 'other') ?>"<?= aria_err($err, 'other') ?>><?= field_error($err, 'other') ?></div>
          <div class="field field--full"><span class="label">Upload your résumé or CV</span>
            <label class="file"><input type="file" name="resume" accept=".pdf,.doc,.docx,.rtf,.txt"><span class="file__btn"><?= icon('upload') ?> Choose file</span><span class="file__name">No file chosen</span></label>
            <p class="field__hint">PDF, Word, RTF or TXT, up to 10 MB. No résumé yet? You can still apply.</p><?= field_error($err, 'resume') ?></div>
          <div class="field field--full"><label for="f-source">How did you hear about Best Jobs Pro?</label>
            <select id="f-source" name="source">
<?php foreach (['', 'Search engine (Google, Bing, etc.)', 'Recommended by a friend or colleague', 'Social media', 'Blog or publication', 'Other'] as $s): ?>
              <option value="<?= e($s) ?>"<?= ($v['source'] ?? '') === $s ? ' selected' : '' ?>><?= $s === '' ? 'Select one' : e($s) ?></option>
<?php endforeach; ?>
            </select></div>
          <div class="field field--full"><label for="f-message">Skills or anything you want us to know</label><textarea id="f-message" name="message" rows="5" placeholder="Certifications, availability, shifts you prefer, pay you are looking for…"><?= old($v, 'message') ?></textarea></div>
        </div>
        <div class="form-foot"><button class="btn" type="submit"><?= icon('send') ?> Submit application</button><small>By applying you agree to our <a href="/privacy-policy/">privacy policy</a>. We never charge job seekers.</small></div>
      </form>
    </div>
    <aside class="reveal">
      <h2 style="font-size:1.5rem">What happens next</h2>
      <ol class="steps prose" style="font-size:1rem">
        <li><strong>We review your details.</strong> A recruiter reads your application and résumé.</li>
        <li><strong>We call you.</strong> Be ready to talk about your goals, interests, skills and work history.</li>
        <li><strong>We match you.</strong> Your profile is compared against openings with employers across Texas.</li>
        <li><strong>You interview and start.</strong> We prep you, set up the interview and follow up after you start.</li>
      </ol>
      <div class="card" style="margin-top:20px">
        <h3>Make your résumé stronger first</h3>
        <p>Paste a job post and your résumé into our free checker to see which keywords you are missing.</p>
        <a class="card__link" href="/career-tools/resume-keyword-checker/">Résumé Keyword Checker <?= icon('arrow') ?></a>
      </div>
      <div class="tiles" style="margin-top:20px">
        <a class="tile" href="tel:<?= SITE_TEL ?>"><span class="tile__ico"><?= icon('phone') ?></span><span><small>Prefer to talk? Call 24/7</small><b><?= SITE_PHONE ?></b></span></a>
      </div>
    </aside>
  </div>
</section>
<?php page_end();
