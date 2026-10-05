<?php
/**
 * Inline SVG icons (24x24, stroke-based). icon('name') returns markup.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

function icon(string $name, string $class = 'ico'): string
{
    static $paths = [
        'uplight'  => '<path d="M12 3v4"/><path d="M8 7h8l-2 7h-4z"/><path d="M12 14v7"/><path d="M8 21h8"/><path d="M5 10 3 8"/><path d="m19 10 2-2"/>',
        'path'     => '<path d="M4 21c4-6 4-10 8-10s4 4 8 10"/><circle cx="7" cy="9" r="1.5"/><circle cx="17" cy="9" r="1.5"/><path d="M7 10.5V14"/><path d="M17 10.5V14"/>',
        'tree'     => '<path d="M12 3 7 10h3l-4 6h5v5h2v-5h5l-4-6h3z"/>',
        'deck'     => '<path d="M3 11h18"/><path d="M5 11v9"/><path d="M19 11v9"/><path d="M8 11V7h8v4"/><path d="M12 3v4"/><path d="M8 20h8"/>',
        'pool'     => '<path d="M3 15c2 0 2 1.5 4 1.5S9 15 11 15s2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M3 19c2 0 2 1.5 4 1.5S9 19 11 19s2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M7 11V5a2 2 0 0 1 4 0"/><path d="M15 11V5a2 2 0 0 1 4 0"/>',
        'wifi'     => '<path d="M2 9a16 16 0 0 1 20 0"/><path d="M5 12.5a11 11 0 0 1 14 0"/><path d="M8.5 16a6 6 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>',
        'bulb'     => '<path d="M9 18h6"/><path d="M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
        'shield'   => '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
        'building' => '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2"/><path d="M10 21v-3h4v3"/>',
        'wrench'   => '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 10l-2.5 2.5a1 1 0 0 1-1.4 0L10 5.4a1 1 0 0 1 0-1.4L12.5 1.5l-1.3 1.3a4 4 0 0 0 3.5 3.5z"/><path d="m3 21 8-8"/>',
        'pencil'   => '<path d="M4 20h4l10-10-4-4L4 16z"/><path d="m12.5 7.5 4 4"/>',
        'bolt'     => '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
        'calc'     => '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8 11h2M12 11h2M16 11h0M8 15h2M12 15h2M16 15v3"/>',
        'dollar'   => '<path d="M12 2v20"/><path d="M17 6.5c-1-1.5-2.5-2-5-2-3 0-4.5 1.5-4.5 3.5C7.5 11 10 11.5 12 12s4.5 1 4.5 3.5c0 2-1.5 3.5-4.5 3.5-2.5 0-4-.5-5-2"/>',
        'sparkle'  => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><path d="m12 7 1.5 3.5L17 12l-3.5 1.5L12 17l-1.5-3.5L7 12l3.5-1.5z"/>',
        'thermo'   => '<path d="M10 4a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 9v6"/>',
        'sun'      => '<circle cx="12" cy="13" r="4"/><path d="M12 3v2M4.2 6.2l1.4 1.4M3 13h2M19 13h2M18.4 6.2 17 7.6"/><path d="M3 21h18"/><path d="M6 17.5h12"/>',
        'quiz'     => '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7"/><circle cx="12" cy="17" r=".6"/>',
        'phone'    => '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
        'mail'     => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'clock'    => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'pin'      => '<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'star'     => '<path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.4l-5.6 2.9 1.1-6.2L3 9.7l6.2-.9z"/>',
        'check'    => '<path d="m5 12 5 5L20 7"/>',
        'arrow'    => '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
        'quote'    => '<path d="M7 7h4v6H7a3 3 0 0 0-3 3v1h3"/><path d="M15 7h4v6h-4a3 3 0 0 0-3 3v1h3"/>',
        'moon'     => '<path d="M20 14.5A8 8 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>',
        'menu'     => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'close'    => '<path d="m6 6 12 12M18 6 6 18"/>',
        'switch'   => '<rect x="3" y="8" width="18" height="8" rx="4"/><circle cx="16" cy="12" r="2.5"/>',
        'camera'   => '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
        'warranty' => '<circle cx="12" cy="10" r="6"/><path d="m9 16-1 5 4-2 4 2-1-5"/><path d="m9.5 10 1.8 1.8L14.5 8"/>',
        'leaf'     => '<path d="M20 4c-8 0-14 4-14 11a5 5 0 0 0 5 5c7 0 9-8 9-16z"/><path d="M6 20c3-5 6-8 10-11"/>',
        'home'     => '<path d="m3 11 9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        'chevron'  => '<path d="m6 9 6 6 6-6"/>',
        'drag'     => '<path d="M8 12H3m0 0 3-3m-3 3 3 3"/><path d="M16 12h5m0 0-3-3m3 3-3 3"/>',
    ];
    $p = $paths[$name] ?? $paths['sparkle'];
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $p . '</svg>';
}
