"""Flat SVG motifs (100x100 viewBox) used for generated cover art and decor.

Each motif is a fragment of SVG drawn with `currentColor` for the main shape
and `var(--m2, ...)` style is avoided so the fragments also work in standalone
SVG files: callers wrap them in a <g> that sets `color` and `fill`.
`A` is the accent fill passed in by the caller (string substituted).
"""

MOTIFS = {
    "frame": '<rect x="18" y="14" width="64" height="72" rx="4" fill="currentColor"/><rect x="28" y="24" width="44" height="52" rx="2" fill="{A}"/><path d="M30 70l12-16 9 10 7-8 12 14z" fill="currentColor" opacity=".55"/><circle cx="60" cy="36" r="5" fill="currentColor" opacity=".55"/>',
    "jar": '<rect x="34" y="10" width="32" height="10" rx="3" fill="{A}"/><path d="M30 24h40c4 0 6 3 6 7v50c0 5-4 9-9 9H33c-5 0-9-4-9-9V31c0-4 2-7 6-7z" fill="currentColor"/><path d="M50 44c6 7 8 12 8 17a8 8 0 01-16 0c0-5 2-10 8-17z" fill="{A}"/>',
    "plant": '<path d="M30 62h40l-6 28H36z" fill="{A}"/><path d="M50 62V36" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><path d="M50 44c-4-16-16-22-26-20 0 12 10 22 26 20zM50 38c4-16 16-24 28-22 0 14-12 24-28 22z" fill="currentColor"/>',
    "candle": '<path d="M50 10c8 10 9 16 9 20a9 9 0 01-18 0c0-4 1-10 9-20z" fill="{A}"/><rect x="35" y="42" width="30" height="48" rx="4" fill="currentColor"/><path d="M50 36v8" stroke="currentColor" stroke-width="3"/>',
    "pillow": '<path d="M16 26c12 4 56 4 68 0-4 16-4 32 0 48-12-4-56-4-68 0 4-16 4-32 0-48z" fill="currentColor"/><path d="M28 50h44M50 34v32" stroke="{A}" stroke-width="5" stroke-linecap="round"/>',
    "flower": '<g fill="currentColor"><circle cx="50" cy="28" r="16"/><circle cx="72" cy="44" r="16"/><circle cx="64" cy="70" r="16"/><circle cx="36" cy="70" r="16"/><circle cx="28" cy="44" r="16"/></g><circle cx="50" cy="52" r="12" fill="{A}"/>',
    "scissors": '<circle cx="30" cy="72" r="12" fill="none" stroke="currentColor" stroke-width="7"/><circle cx="70" cy="72" r="12" fill="none" stroke="currentColor" stroke-width="7"/><path d="M38 62L72 12M62 62L28 12" stroke="currentColor" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="37" r="4" fill="{A}"/>',
    "yarn": '<circle cx="48" cy="50" r="32" fill="currentColor"/><path d="M22 36c16 4 36 22 42 44M30 24c20 6 38 28 44 44M18 54c14 2 30 14 34 28" stroke="{A}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M78 62c10 6 8 20-6 24" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round"/>',
    "brush": '<rect x="44" y="40" width="12" height="52" rx="6" fill="currentColor"/><rect x="40" y="30" width="20" height="14" rx="2" fill="{A}"/><path d="M40 30c0-12 4-20 10-24 6 4 10 12 10 24z" fill="currentColor"/>',
    "ornament": '<rect x="42" y="12" width="16" height="10" rx="2" fill="{A}"/><circle cx="50" cy="56" r="34" fill="currentColor"/><path d="M18 50c20 8 44 8 64 0M20 66c20 6 40 6 60 0" stroke="{A}" stroke-width="5" fill="none"/>',
    "tree": '<path d="M50 8l22 30H60l18 24H62l20 22H18l20-22H22l18-24H28z" fill="currentColor"/><rect x="44" y="84" width="12" height="10" fill="{A}"/><circle cx="44" cy="44" r="4" fill="{A}"/><circle cx="58" cy="62" r="4" fill="{A}"/><circle cx="40" cy="74" r="4" fill="{A}"/>',
    "snowflake": '<g stroke="currentColor" stroke-width="6" stroke-linecap="round"><path d="M50 10v80M15 30l70 40M15 70l70-40"/><path d="M40 16l10 10 10-10M40 84l10-10 10 10" fill="none"/></g><circle cx="50" cy="50" r="7" fill="{A}"/>',
    "wreath": '<circle cx="50" cy="50" r="30" fill="none" stroke="currentColor" stroke-width="16" stroke-dasharray="10 4"/><path d="M42 80l8-8 8 8-8 12z" fill="{A}"/><circle cx="50" cy="74" r="6" fill="{A}"/>',
    "gift": '<rect x="16" y="40" width="68" height="50" rx="4" fill="currentColor"/><rect x="12" y="30" width="76" height="14" rx="3" fill="currentColor"/><rect x="45" y="30" width="10" height="60" fill="{A}"/><path d="M50 30c-6-14-22-18-22-8 0 6 10 8 22 8zM50 30c6-14 22-18 22-8 0 6-10 8-22 8z" fill="{A}"/>',
    "pumpkin": '<path d="M48 22c0-8 4-12 10-14" stroke="{A}" stroke-width="6" fill="none" stroke-linecap="round"/><ellipse cx="34" cy="58" rx="20" ry="30" fill="currentColor"/><ellipse cx="66" cy="58" rx="20" ry="30" fill="currentColor"/><ellipse cx="50" cy="58" rx="18" ry="32" fill="currentColor" stroke="{A}" stroke-width="3"/>',
    "ghost": '<path d="M22 90V44a28 28 0 0156 0v46l-9-8-9 8-10-8-10 8-9-8z" fill="currentColor"/><ellipse cx="40" cy="46" rx="5" ry="7" fill="{A}"/><ellipse cx="60" cy="46" rx="5" ry="7" fill="{A}"/>',
    "web": '<g stroke="currentColor" stroke-width="3" fill="none"><path d="M50 8v84M8 50h84M20 20l60 60M80 20L20 80"/><path d="M50 22l20 8 8 20-8 20-20 8-20-8-8-20 8-20z"/><path d="M50 36l10 4 4 10-4 10-10 4-10-4-4-10 4-10z"/></g><circle cx="70" cy="70" r="7" fill="{A}"/>',
    "bat": '<path d="M50 40c-4-8-10-8-10-8s2 6 0 10c-10-8-26-8-34 2 8 0 12 6 12 12 6-4 14-2 16 6 4-6 10-6 16 0 6-6 12-6 16 0 2-8 10-10 16-6 0-6 4-12 12-12-8-10-24-10-34-2-2-4 0-10 0-10s-6 0-10 8z" fill="currentColor"/><circle cx="46" cy="44" r="2" fill="{A}"/><circle cx="54" cy="44" r="2" fill="{A}"/>',
    "leaf": '<path d="M18 82C14 40 44 14 86 14c0 42-26 72-68 68z" fill="currentColor"/><path d="M22 78L70 30M40 60h16M52 48h14M36 50v14" stroke="{A}" stroke-width="4" stroke-linecap="round"/>',
    "acorn": '<path d="M24 44h52c0 26-10 44-26 48-16-4-26-22-26-48z" fill="currentColor"/><path d="M20 44c0-14 14-24 30-24s30 10 30 24z" fill="{A}"/><path d="M50 20v-10" stroke="{A}" stroke-width="6" stroke-linecap="round"/>',
    "heart": '<path d="M50 88L16 54C4 42 8 18 28 16c10-1 18 6 22 14 4-8 12-15 22-14 20 2 24 26 12 38z" fill="currentColor"/><path d="M30 32c-6 2-8 8-6 14" stroke="{A}" stroke-width="5" fill="none" stroke-linecap="round"/>',
    "envelope": '<rect x="12" y="24" width="76" height="54" rx="5" fill="currentColor"/><path d="M14 28l36 28 36-28" stroke="{A}" stroke-width="5" fill="none"/><path d="M50 70l-9-9c-4-4-1-11 4-11 2 0 4 1 5 3 1-2 3-3 5-3 5 0 8 7 4 11z" fill="{A}"/>',
    "shamrock": '<g fill="currentColor"><circle cx="38" cy="34" r="15"/><circle cx="62" cy="34" r="15"/><circle cx="38" cy="54" r="15"/><circle cx="62" cy="54" r="15"/><circle cx="50" cy="22" r="6"/></g><circle cx="50" cy="44" r="7" fill="{A}"/><path d="M50 56c0 16 6 26 14 34" stroke="currentColor" stroke-width="6" fill="none" stroke-linecap="round"/>',
    "rainbow": '<g fill="none" stroke-width="9"><path d="M10 80a40 40 0 0180 0" stroke="currentColor"/><path d="M21 80a29 29 0 0158 0" stroke="{A}"/><path d="M32 80a18 18 0 0136 0" stroke="currentColor" opacity=".6"/></g><circle cx="16" cy="84" r="9" fill="currentColor" opacity=".8"/><circle cx="84" cy="84" r="9" fill="currentColor" opacity=".8"/>',
    "star": '<path d="M50 8l12 28 30 3-23 20 7 30-26-16-26 16 7-30L8 39l30-3z" fill="currentColor"/><circle cx="50" cy="52" r="8" fill="{A}"/>',
}


def motif(name, accent="#fff"):
    return MOTIFS[name].replace("{A}", accent)
