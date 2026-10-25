<?php
/**
 * Shared helpers for the /tools/ section (tool list + "More free tools" cards).
 * Included by every tool page; returns 404 if requested directly.
 */
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === realpath(__FILE__)) {
    http_response_code(404);
    exit;
}
require_once __DIR__ . '/../inc/layout.php';

function tool_list(): array
{
    return [
        'influencer-earnings-calculator' => ['calc', 'Influencer Earnings Calculator', 'Estimate your sponsored post rate, monthly and yearly income by platform, niche, engagement and content type.'],
        'engagement-rate-calculator'     => ['heart', 'Engagement Rate Calculator', 'Average up to 10 posts, calculate engagement by followers or by reach, and benchmark it against your platform and tier.'],
        'influencer-email-generator'     => ['mail', 'Influencer Email Generator', 'Write an outreach email to an influencer, or a creator pitch to a brand, with subject lines and a short DM version.'],
        'media-kit-builder'              => ['file', 'Media Kit Builder', 'Fill in your stats and get a polished one-page media kit you can print or save as a PDF in minutes.'],
        'income-stream-simulator'        => ['pie', 'Income Stream Simulator', 'Mix brand deals, affiliate, ads, products, memberships and UGC to see your monthly income and diversification score.'],
        'monetization-readiness-quiz'    => ['quiz', 'Monetization Readiness Quiz', 'Answer 10 quick questions and get your readiness score plus the two income streams to start with right now.'],
    ];
}

/** Schema node for a tool page. */
function tool_schema(string $slug, string $name, string $desc): array
{
    return [
        '@type' => 'WebApplication',
        'name' => $name,
        'url' => SITE_URL . '/tools/' . $slug . '/',
        'description' => $desc,
        'applicationCategory' => 'BusinessApplication',
        'operatingSystem' => 'Any (web browser)',
        'isAccessibleForFree' => true,
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'publisher' => ['@id' => SITE_URL . '/#org'],
    ];
}

function more_tools(string $exclude): void
{
    ?>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker reveal">Keep going</span>
      <h2 class="reveal">More free creator tools</h2>
    </div>
    <div class="card-grid cols-3">
<?php $n = 0; foreach (tool_list() as $slug => [$ic, $name, $txt]):
        if ($slug === $exclude || ++$n > 3) { continue; } ?>
      <article class="card tool-card tilt reveal"><a href="/tools/<?= $slug ?>/"><span class="ico-badge"><?= icon($ic) ?></span><h3><?= e($name) ?></h3><p><?= e($txt) ?></p><span class="more">Try it free <?= icon('arrow') ?></span></a></article>
<?php endforeach; ?>
    </div>
    <p style="text-align:center;margin-top:30px"><a class="btn btn-ghost" href="/tools/">All free tools <?= icon('arrow') ?></a></p>
  </div>
</section>
<?php
}
