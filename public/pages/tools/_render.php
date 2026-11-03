<?php
defined('SCC') || exit;

function render_tool(string $path, string $id): void
{
    $t = tools_meta()[$id];
    $a = article("tool-$id");
    render_article($path, "tool-$id", 'tools', [
        'tool' => $id,
        'schema' => [[
            '@type' => 'WebApplication',
            'name' => $t['name'],
            'url' => abs_url($path),
            'applicationCategory' => 'UtilitiesApplication',
            'operatingSystem' => 'Any (runs in the browser)',
            'description' => $a['description'] ?? $t['blurb'],
            'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
            'publisher' => ['@id' => SITE_ORIGIN . '/#organization'],
        ]],
    ]);
}
