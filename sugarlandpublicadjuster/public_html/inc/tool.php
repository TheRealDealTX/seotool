<?php
/** Shared wrapper for the /tools/ pages. */
require_once __DIR__ . '/layout.php';

function tool_start(string $slug, string $name, string $title, string $desc, string $h1, string $lead, array $faqs = []): void
{
    $path = '/tools/' . $slug . '/';
    $crumbs = [['Home', '/'], ['Tools', '/tools/'], [$name, $path]];
    $schema = [[
        '@type' => 'WebApplication',
        '@id' => SITE['origin'] . $path . '#app',
        'name' => $name,
        'url' => SITE['origin'] . $path,
        'description' => $desc,
        'applicationCategory' => 'FinanceApplication',
        'operatingSystem' => 'Any (web browser)',
        'isAccessibleForFree' => true,
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'provider' => ['@id' => SITE['origin'] . '/#business'],
    ]];
    if ($faqs) {
        $schema[] = faq_schema($faqs, $path);
    }
    page_start([
        'title' => $title,
        'description' => $desc,
        'path' => $path,
        'breadcrumbs' => $crumbs,
        'schema' => $schema,
    ]);
    page_hero($h1, $lead, $crumbs, 'Free tool · Sugar Land Public Adjuster');
    echo '<div class="container content-layout"><div class="tool-main">';
}

function tool_end(array $faqs = []): void
{
    if ($faqs) {
        echo '<section class="prose mt-2"><h2>Frequently asked questions</h2>';
        faq_list($faqs);
        echo '</section>';
    }
    echo '<p class="tool-note">These tools give planning estimates only. They are not legal advice, an appraisal or a guarantee of what any insurer will pay. Your policy language controls. For a free review of your actual claim, call or text ' . tel_link() . '.</p>';
    echo '</div>';
    sidebar_cta();
    echo '</div>';
    page_end(['scripts' => '<script src="/assets/js/tools.js?v=' . ASSET_VER . '" defer></script>']);
}
