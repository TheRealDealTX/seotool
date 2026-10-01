<?php defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
partial('page-hero', [
    'title'   => 'Terms of Use',
    'lead'    => 'The terms that apply when you use the Friendswood Roofers website.',
    'actions' => false,
]); ?>
<section class="section section--first">
  <div class="container narrow prose legal">
    <p class="small">Effective date: <?= e(display_date((string) config('launch_date'))) ?></p>

    <p>By using friendswoodroofs.com (the "website"), you agree to these terms. If you do not agree, please do not use the website.</p>

    <h2>General information only</h2>
    <p>The articles, FAQs, service descriptions and other content on this website are general information for homeowners. They are not an inspection of your roof and are not legal, insurance, engineering or financial advice. Roofing needs depend on the specific condition of your roof, which can only be confirmed by an inspection. Insurance questions should be directed to your insurance company or agent.</p>

    <h2>Estimates and requests</h2>
    <p>Submitting the estimate request form or calling us does not create a contract, schedule an appointment or guarantee availability. Any price or scope of work is provided only in a written estimate after we have assessed your roof, and roofing work proceeds only under a separate written agreement. Scheduling depends on the work involved, material availability and weather.</p>

    <h2>Roofing Project Planner</h2>
    <p>The Roofing Project Planner is a note-taking aid that helps you organize your observations. It does not diagnose roof problems, inspect your roof, provide a quote or make a definitive recommendation. Do not climb onto your roof to answer its questions.</p>

    <h2>Weather information</h2>
    <p>The live radar map on the homepage is provided by a third party, RainViewer, under its own terms. Radar imagery may be delayed, incomplete or unavailable. It is not an official source of weather warnings. For watches, warnings and emergency information, rely on the National Weather Service and local authorities.</p>

    <h2>Acceptable use</h2>
    <p>Please use the website lawfully. Do not submit false information, attempt to interfere with the website's operation or security, send automated or bulk submissions, or use the forms to send unsolicited messages.</p>

    <h2>Website content</h2>
    <p>The content and design of this website belong to Friendswood Roofers unless otherwise noted. Please do not copy or republish them without permission.</p>

    <h2>Links to other websites</h2>
    <p>Links to other websites, such as government weather and insurance resources, are provided for convenience. We are not responsible for their content, availability or practices.</p>

    <h2>No warranties</h2>
    <p>We work to keep the website accurate and available, but it is provided "as is" without warranties of any kind, to the extent permitted by law. Content may change without notice.</p>

    <h2>Limitation of liability</h2>
    <p>To the extent permitted by law, Friendswood Roofers is not liable for any loss or damage arising from your use of, or reliance on, the website's general information. This does not limit any rights you have under a written agreement for roofing work or under applicable law.</p>

    <h2>Governing law</h2>
    <p>These terms are governed by the laws of the State of Texas.</p>

    <h2>Changes</h2>
    <p>We may update these terms from time to time. The effective date above shows when they were last changed.</p>

    <h2>Questions</h2>
    <p>Call us at <a href="<?= e(phone_href()) ?>"><?= e(phone_display()) ?></a>. See also our <a href="/privacy-policy/">Privacy Policy</a>.</p>
  </div>
</section>
