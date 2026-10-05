<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Terms of Service', '/terms-of-service/']];
$page = [
    'title' => 'Terms of Service | Austin Landscape Lighting',
    'description' => 'Terms governing use of austinlandscapelighting.com and the planning tools, estimates and content provided by Austin Landscape Lighting.',
    'path' => '/terms-of-service/',
    'robots' => 'noindex, follow',
    'schema' => [schema_webpage(['title' => 'Terms of Service', 'description' => 'Terms of service.', 'path' => '/terms-of-service/']), schema_breadcrumb($crumbs)],
];
ob_start();
echo sub_hero(['eyebrow' => 'Legal', 'h1' => 'Terms of Service', 'intro' => 'Last updated October 5, 2026. By using austinlandscapelighting.com you agree to these terms.', 'crumbs' => $crumbs, 'cta' => false]);
?>
<section class="section">
  <div class="container container--narrow prose" data-reveal>
    <h2>Use of this website</h2>
    <p>This website is provided by Austin Landscape Lighting for informational purposes and to let you request services. You agree to use it lawfully and not to interfere with its operation, attempt to gain unauthorized access, scrape content in bulk or submit false or abusive information through our forms.</p>
    <h2>Estimates, tools and content</h2>
    <p>The calculators, visualizer, articles and price ranges on this site are planning aids and general information only. They are not quotes, engineering advice or guarantees of results. Fixture counts, costs, energy savings, transformer sizing and sunset times are estimates and may differ from your actual project. A binding price is provided only in a written estimate signed by Austin Landscape Lighting.</p>
    <h2>Services and warranty</h2>
    <p>Lighting design, installation, maintenance and repair services are governed by the written estimate or agreement for each project. Our two-year workmanship warranty and any manufacturer fixture warranties are described in that agreement. Nothing on this website expands or replaces those terms.</p>
    <h2>Intellectual property</h2>
    <p>The text, photographs, illustrations, tools, code and design of this website are owned by or licensed to Austin Landscape Lighting and protected by copyright. You may view and print pages for personal, non-commercial use. Any other use requires our written permission.</p>
    <h2>Testimonials</h2>
    <p>Reviews on this site reflect the experience of individual clients. Results vary with property, design and conditions.</p>
    <h2>Disclaimer and limitation of liability</h2>
    <p>This website is provided "as is" without warranties of any kind, express or implied, including accuracy, availability or fitness for a particular purpose. To the fullest extent permitted by law, Austin Landscape Lighting is not liable for any indirect, incidental or consequential damages arising from your use of the website or reliance on its content.</p>
    <h2>Third-party links</h2>
    <p>Links to other websites are provided for convenience. We are not responsible for their content or practices.</p>
    <h2>Governing law</h2>
    <p>These terms are governed by the laws of the State of Texas. Any dispute relating to this website will be resolved in the state or federal courts located in Travis County, Texas.</p>
    <h2>Changes</h2>
    <p>We may revise these terms at any time by posting an updated version here. Your continued use of the site constitutes acceptance of the revised terms.</p>
    <h2>Contact</h2>
    <p>Questions about these terms: <a href="mailto:<?= e(BIZ['email']) ?>"><?= e(BIZ['email']) ?></a> or <a href="<?= BIZ['phone_href'] ?>"><?= e(BIZ['phone_display']) ?></a>.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
