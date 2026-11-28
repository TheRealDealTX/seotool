<?php
// Shared widget markup helpers
function w_head(string $title, string $ic, string $sub = '', bool $reset = true, string $tag = 'h2'): string {
    return '<div class="calc-head"><span class="calc-ic">' . icon($ic) . '</span><div><' . $tag . ' class="calc-title">' . e($title) . '</' . $tag . '>' . ($sub ? '<p>' . e($sub) . '</p>' : '') . '</div>'
        . ($reset ? '<button type="button" class="btn btn-ghost btn-sm calc-reset" data-reset>' . icon('reset', 'ic ic-xs') . ' Reset</button>' : '') . '</div>';
}
function w_ring(string $key = 'ring', string $sub = ''): string {
    return '<div class="ring" data-ring="' . $key . '"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="ring-bg" cx="60" cy="60" r="52"/><circle class="ring-fg" cx="60" cy="60" r="52" stroke-dasharray="326.73" stroke-dashoffset="326.73"/></svg><div class="ring-val"><span><span data-out="' . $key . '">--</span>' . ($sub ? '<small>' . e($sub) . '</small>' : '') . '</span></div></div>';
}
function w_field(string $name, string $label, string $ph = '', string $suffix = '', string $mode = 'decimal', string $val = '', string $extra = ''): string {
    $type = $mode === 'text' ? 'text' : 'text';
    return '<div class="field"><label for="f-' . $name . '">' . e($label) . '</label><div class="input-wrap"><input class="input" id="f-' . $name . '" name="' . $name . '" type="' . $type . '" inputmode="' . $mode . '" placeholder="' . e($ph) . '" value="' . e($val) . '" autocomplete="off"' . $extra . '>' . ($suffix ? '<span class="suffix">' . e($suffix) . '</span>' : '') . '</div></div>';
}
function w_letter_select(string $name, string $sel = 'A', string $cls = 'select'): string {
    $h = '<select class="' . $cls . '" name="' . $name . '" aria-label="Letter grade">';
    foreach (['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F'] as $l) $h .= '<option' . ($l === $sel ? ' selected' : '') . '>' . $l . '</option>';
    return $h . '</select>';
}
function w_rm(): string { return '<button type="button" class="rm" data-rm aria-label="Remove row">' . icon('trash', 'ic ic-xs') . '</button>'; }
function w_actions(string $label = 'Calculate'): string {
    return '<div class="calc-actions"><button type="submit" class="btn btn-primary">' . icon('zap', 'ic') . ' ' . e($label) . '</button></div>';
}
