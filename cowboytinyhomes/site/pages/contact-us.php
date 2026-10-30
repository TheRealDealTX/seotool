<?php
require_once __DIR__ . '/../inc/contact.php';

$result = null;
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    $result = handle_contact($_POST);
    if ($result['ok']) {
        header('Location: /contact-us/?sent=1#form', true, 303);
        exit;
    }
}
$sent = isset($_GET['sent']);
$v = $result['values'] ?? [];
$val = fn(string $k) => e($v[$k] ?? '');

// Calculator links pass ?project=&size=&budget=&note= to prefill the message.
$prefill = '';
if (!$v && (isset($_GET['project']) || isset($_GET['budget']) || isset($_GET['note']))) {
    $bits = [];
    if (!empty($_GET['project'])) $bits[] = 'Project: ' . contact_clean((string)$_GET['project'], 80);
    if (!empty($_GET['size']))    $bits[] = 'Size: ' . contact_clean((string)$_GET['size'], 40) . ' sq ft';
    if (!empty($_GET['budget']))  $bits[] = 'Estimated budget: ' . contact_clean((string)$_GET['budget'], 80);
    if (!empty($_GET['note']))    $bits[] = contact_clean((string)$_GET['note'], 300);
    $prefill = "From the website planning tools —\n" . implode("\n", $bits) . "\n\nMy goals: ";
}
$activeRemodel = ($v['form'] ?? '') === 'remodel' || (($_GET['project'] ?? '') === 'remodel');
// Plan pages pass ?ptype= to preselect the project type.
$preType = $v ? '' : contact_clean((string)($_GET['ptype'] ?? ''), 80);

$cityOptions = function (string $sel) {
    $out = '<option value="">- Select City -</option>';
    foreach (array_merge(array_values(SERVICE_CITIES), ['Other']) as $c) {
        $out .= '<option' . ($sel === $c ? ' selected' : '') . '>' . e($c) . '</option>';
    }
    return $out;
};
$radio = function (string $name, array $opts, string $sel) {
    $out = '<div class="radio-row">';
    foreach ($opts as $o) {
        $out .= '<label><input type="radio" name="' . $name . '" value="' . e($o) . '"' . ($sel === $o ? ' checked' : '') . '> ' . e($o) . '</label>';
    }
    return $out . '</div>';
};
$hidden = '<input type="hidden" name="ts" value="' . time() . '"><div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>';

hero([
    'eyebrow' => 'Free Design Consultation',
    'h1' => 'Contact Cowboy Tiny Homes',
    'lead' => 'Tell us what you want to build or remodel. We will review your goals, your property and your budget, then follow up with honest next steps — no pressure and no obligation.',
    'image' => 'Design-and-build-contact.webp',
    'cta' => false,
]);
?>
<section class="section" id="form">
  <div class="wrap contact-grid">
    <div class="tool-panel">
<?php if ($sent): ?>
      <div class="alert alert--ok" role="status"><strong>Thank you — your project details are on their way.</strong> The Cowboy Tiny Homes team will contact you soon. Need us sooner? Call <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a>.</div>
<?php elseif ($result && $result['errors']): ?>
      <div class="alert alert--err" role="alert"><strong>Please check the form:</strong><ul><?php foreach ($result['errors'] as $er) echo '<li>' . e($er) . '</li>'; ?></ul></div>
<?php endif; ?>
      <h2>Tell Us About Your Project</h2>
      <div class="tabs" role="tablist">
        <button class="tab" role="tab" type="button" data-panel="panel-build" aria-selected="<?= $activeRemodel ? 'false' : 'true' ?>">Design / Build</button>
        <button class="tab" role="tab" type="button" data-panel="panel-remodel" aria-selected="<?= $activeRemodel ? 'true' : 'false' ?>">Remodel</button>
      </div>

      <form id="panel-build" class="form" method="post" action="/contact-us/#form" <?= $activeRemodel ? 'hidden' : '' ?>>
        <input type="hidden" name="form" value="design-build"><?= $hidden ?>
        <div><label for="b-first">First name *</label><input id="b-first" type="text" name="first_name" value="<?= $val('first_name') ?>" autocomplete="given-name" required></div>
        <div><label for="b-last">Last name</label><input id="b-last" type="text" name="last_name" value="<?= $val('last_name') ?>" autocomplete="family-name"></div>
        <div><label for="b-phone">Phone *</label><input id="b-phone" type="tel" name="phone" value="<?= $val('phone') ?>" autocomplete="tel" required></div>
        <div><label for="b-email">Email *</label><input id="b-email" type="email" name="email" value="<?= $val('email') ?>" autocomplete="email" required></div>
        <div><label for="b-type">What do you want to build?</label>
          <select id="b-type" name="project_type">
<?php foreach (['', 'Custom tiny home', 'ADU / casita / guest house', 'Tiny home on wheels', 'Park model home', 'Small single-family home', 'Design / plans only', 'Not sure yet'] as $o): ?>
            <option value="<?= e($o) ?>"<?= ($v['project_type'] ?? $preType) === $o && $o !== '' ? ' selected' : '' ?>><?= $o === '' ? '- Select -' : e($o) ?></option>
<?php endforeach; ?>
          </select></div>
        <div><label for="b-city">City you are building in or near</label><select id="b-city" name="city"><?= $cityOptions($v['city'] ?? '') ?></select></div>
        <div class="full"><label for="b-cityo">If other, which city or county?</label><input id="b-cityo" type="text" name="city_other" value="<?= $val('city_other') ?>"></div>
        <div class="full"><label for="b-addr">Project address (include city and zip code)</label><input id="b-addr" type="text" name="address" value="<?= $val('address') ?>" autocomplete="street-address"></div>
        <div class="full"><label>Do you own the property you wish to build on?</label><?= $radio('own_property', ['Yes', 'No', 'Still looking for land'], $v['own_property'] ?? '') ?></div>
        <div class="full"><label>How do you prefer to be contacted?</label><?= $radio('contact_pref', ['Phone', 'Email', 'Either'], $v['contact_pref'] ?? '') ?></div>
        <div class="full"><label for="b-msg">What are your goals for this project?</label><textarea id="b-msg" name="message" placeholder="Size, bedrooms, budget, timeline, how you will use it..."><?= $v ? $val('message') : e($prefill) ?></textarea></div>
        <div class="full"><button class="btn btn--gold" type="submit">Send My Project Details</button></div>
        <p class="form-note full">By submitting, you agree to be contacted about your project. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </form>

      <form id="panel-remodel" class="form" method="post" action="/contact-us/#form" <?= $activeRemodel ? '' : 'hidden' ?>>
        <input type="hidden" name="form" value="remodel"><input type="hidden" name="project_type" value="Home remodel"><?= $hidden ?>
        <div><label for="r-first">First name *</label><input id="r-first" type="text" name="first_name" value="<?= $val('first_name') ?>" autocomplete="given-name" required></div>
        <div><label for="r-last">Last name</label><input id="r-last" type="text" name="last_name" value="<?= $val('last_name') ?>" autocomplete="family-name"></div>
        <div><label for="r-phone">Phone *</label><input id="r-phone" type="tel" name="phone" value="<?= $val('phone') ?>" autocomplete="tel" required></div>
        <div><label for="r-email">Email *</label><input id="r-email" type="email" name="email" value="<?= $val('email') ?>" autocomplete="email" required></div>
        <div><label for="r-area">Which part of the house is being remodeled?</label>
          <select id="r-area" name="remodel_area">
<?php foreach (['', 'Living area', 'Kitchen', 'Bedroom', 'Bathroom', 'Whole house', 'Others'] as $o): ?>
            <option value="<?= e($o) ?>"<?= ($v['remodel_area'] ?? '') === $o && $o !== '' ? ' selected' : '' ?>><?= $o === '' ? '- Select -' : e($o) ?></option>
<?php endforeach; ?>
          </select></div>
        <div><label for="r-other">If others, please describe</label><input id="r-other" type="text" name="remodel_other" value="<?= $val('remodel_other') ?>"></div>
        <div class="full"><label for="r-addr">Project address (include city and zip code)</label><input id="r-addr" type="text" name="address" value="<?= $val('address') ?>" autocomplete="street-address"></div>
        <div class="full"><label>How do you prefer to be contacted?</label><?= $radio('contact_pref', ['Phone', 'Email', 'Either'], $v['contact_pref'] ?? '') ?></div>
        <div class="full"><label for="r-msg">What are your goals for this project?</label><textarea id="r-msg" name="message"><?= $val('message') ?></textarea></div>
        <div class="full"><button class="btn btn--gold" type="submit">Send My Remodel Details</button></div>
        <p class="form-note full">By submitting, you agree to be contacted about your project. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </form>
    </div>

    <aside class="sidebar">
      <div class="side-box side-box--cta">
        <h2>Talk to a Designer</h2>
        <p>Prefer the phone? Call or text and tell us what you have in mind.</p>
        <a class="btn btn--gold" href="<?= PHONE_HREF ?>"><?= PHONE ?></a>
        <a class="btn btn--ghost" href="mailto:<?= EMAIL ?>">Email Us</a>
      </div>
      <div class="side-box">
        <h2>What Happens Next</h2>
        <ol class="toc" style="padding-left:1.2em">
          <li>We review your goals, budget and location.</li>
          <li>We call to talk through options and answer questions.</li>
          <li>If it is a fit, we scope a feasibility study and design.</li>
        </ol>
      </div>
      <div class="side-box">
        <h2>Before You Call</h2>
        <ul>
          <li><a href="/tools/tiny-home-cost-calculator/">Estimate your budget</a></li>
          <li><a href="/tools/which-tiny-home-is-right-for-me/">Find your home type</a></li>
          <li><a href="/guides/tiny-house-laws-texas/">Check Texas tiny house laws</a></li>
          <li><a href="/faqs/">Read the FAQs</a></li>
        </ul>
      </div>
    </aside>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><h2>Where We Build</h2><p class="section-intro">Cowboy Tiny Homes designs and builds across Texas, including these metro areas and the rural land around them.</p></div>
    <div class="cards cards--links">
<?php foreach (SERVICE_CITIES as $slug => $city): ?>
      <a class="card card--link" href="/tiny-home-builders-<?= $slug ?>/"><span class="card-kicker">Service Area</span><strong><?= $city ?></strong><span>Tiny homes, ADUs and park models in and around <?= $city ?>.</span></a>
<?php endforeach; ?>
    </div>
  </div>
</section>
