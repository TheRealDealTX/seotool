<?php
/** Inline stroke icons (24x24, currentColor). */
function icon(string $name, string $class = 'icon'): string
{
    static $p = [
        'roof'     => '<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v9.5h14V10"/><path d="M9.5 19.5v-5h5v5"/>',
        'hail'     => '<path d="M7 15a4.5 4.5 0 1 1 1.2-8.85A5.5 5.5 0 0 1 18.5 9 3.5 3.5 0 0 1 18 15.9"/><circle cx="8" cy="19" r="1"/><circle cx="12" cy="21" r="1"/><circle cx="16" cy="19" r="1"/>',
        'water'    => '<path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0c0-4.1 6-10.5 6-10.5Z"/><path d="M9 14.5a3 3 0 0 0 3 3"/>',
        'fire'     => '<path d="M12 21a6.5 6.5 0 0 0 6.5-6.5c0-4-3.5-6-4-10.5-2.5 1.5-4 4-4 6.5-1-1-1.5-2-1.5-3C7.5 9.5 5.5 12 5.5 14.5A6.5 6.5 0 0 0 12 21Z"/><path d="M12 21a2.5 2.5 0 0 1-2.5-2.5c0-1.6 1.5-2.4 2.5-4 1 1.6 2.5 2.4 2.5 4A2.5 2.5 0 0 1 12 21Z"/>',
        'wind'     => '<path d="M3 8h11a3 3 0 1 0-3-3"/><path d="M3 12h16a3 3 0 1 1-3 3"/><path d="M3 16h7"/>',
        'shield'   => '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
        'building' => '<path d="M4 21V5.5L12 3v18"/><path d="M12 8.5 20 11v10"/><path d="M2.5 21h19"/><path d="M7 8h2M7 11.5h2M7 15h2M15 13.5h2M15 17h2"/>',
        'phone'    => '<path d="M5 3.5h3.5l1.8 4.6-2.3 1.4a11 11 0 0 0 6.5 6.5l1.4-2.3 4.6 1.8V19a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 3.5 5.1 1.5 1.5 0 0 1 5 3.5Z"/>',
        'message'  => '<path d="M4 5h16v11H9l-5 4V5Z"/><path d="M8 9.5h8M8 12.5h5"/>',
        'check'    => '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        'arrow'    => '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
        'calc'     => '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01M8.5 14.5h.01M12 14.5h.01M15.5 14.5v3M8.5 18h.01M12 18h.01"/>',
        'calendar' => '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/><path d="M8 13.5h3v3H8z"/>',
        'clipboard'=> '<rect x="5" y="4.5" width="14" height="16.5" rx="2"/><path d="M9 4.5V3h6v1.5"/><path d="m8.5 12 2 2 4-4"/><path d="M8.5 17h7"/>',
        'list'     => '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
        'radar'    => '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12 18 6"/><circle cx="12" cy="12" r="1"/>',
        'quiz'     => '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6"/><path d="M12 17h.01"/>',
        'pin'      => '<path d="M12 21s7-6.1 7-11.5a7 7 0 1 0-14 0C5 14.9 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
        'doc'      => '<path d="M6 3h8.5L19 7.5V21H6V3Z"/><path d="M14 3v5h5"/><path d="M9 12.5h7M9 16h7"/>',
        'search'   => '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
        'scale'    => '<path d="M12 4v16M7 20h10"/><path d="M5 8h14"/><path d="m5 8-2.5 6a3 3 0 0 0 5 0L5 8ZM19 8l-2.5 6a3 3 0 0 0 5 0L19 8Z"/>',
        'camera'   => '<path d="M4 8h3l1.5-2.5h7L17 8h3v11H4V8Z"/><circle cx="12" cy="13" r="3.5"/>',
        'license'  => '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16.2a3.4 3.4 0 0 1 6.4 0M14.5 10h4M14.5 13.5h3"/>',
        'clock'    => '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'dollar'   => '<path d="M12 3v18"/><path d="M16.5 7.5c0-1.7-2-3-4.5-3s-4.5 1.3-4.5 3S9.5 10.5 12 11s4.5 1.3 4.5 3.5-2 3-4.5 3-4.5-1.3-4.5-3"/>',
        'menu'     => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'close'    => '<path d="m6 6 12 12M18 6 6 18"/>',
        'chevron'  => '<path d="m6 9 6 6 6-6"/>',
        'up'       => '<path d="m6 15 6-6 6 6"/>',
        'star'     => '<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8L12 3.5Z"/>',
        'print'    => '<path d="M7 9V3.5h10V9"/><rect x="3.5" y="9" width="17" height="8" rx="1.5"/><path d="M7 14h10v6.5H7z"/>',
        'download' => '<path d="M12 4v11"/><path d="m7 10.5 5 5 5-5"/><path d="M4.5 19.5h15"/>',
        'external' => '<path d="M14 4h6v6"/><path d="M20 4 11 13"/><path d="M18 14v5.5H4.5V6H10"/>',
    ];
    $d = $p[$name] ?? $p['check'];
    return '<svg class="' . h($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $d . '</svg>';
}
