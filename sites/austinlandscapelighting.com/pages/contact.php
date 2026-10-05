<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Contact', '/contact/']];
$page = [
    'title' => 'Contact Austin Landscape Lighting | Free Estimate',
    'description' => 'Request a free landscape lighting consultation from Austin Landscape Lighting. Call +1 (281) 704-7210 or send the form; a designer replies within one business day.',
    'path' => '/contact/',
    'active' => '/contact/',
    'schema' => [schema_webpage(['title' => 'Contact', 'description' => 'Contact Austin Landscape Lighting.', 'path' => '/contact/'], 'ContactPage'), schema_breadcrumb($crumbs)],
];
ob_start();
echo sub_hero(['eyebrow' => 'Get in touch', 'h1' => 'Let\'s Talk About Your Project', 'intro' => 'Fill out the form and a lighting designer from Austin Landscape Lighting will reach out within one business day to schedule your free on-site consultation. Prefer to talk now? Call or text ' . BIZ['phone_display'] . '.', 'crumbs' => $crumbs, 'cta' => false]);
echo contact_section('Free estimate', 'Tell us about your property');
?>
<section class="section section--alt">
  <div class="container">
    <?= section_head('What happens next', 'From form to first glow') ?>
    <?= process_steps() ?>
  </div>
</section>
<section class="section">
  <div class="container container--narrow">
    <?= section_head('Before you call', 'Common questions') ?>
    <?= faq_list(array_slice(site_faqs(), 0, 4), 'contact-faq') ?>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
