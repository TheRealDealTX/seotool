"""Form-building helpers for the calculator pages.

Every tool's `form` HTML is assembled from these so the markup matches what
assets/js/tools-core.js reads: inputs carry `name` (or `data-k` inside a
dynamic row), numeric selects carry `data-num`, ranges get an <output>.
"""


def _e(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _label(fid, label, tip=None):
    t = f' <span class="tip" tabindex="0" data-tip="{_e(tip)}" aria-label="{_e(tip)}">?</span>' if tip else ""
    return f'<label class="lbl" for="{fid}">{label}{t}</label>'


def _show(show):
    """data-show="field=value|value2" — tools-core hides the field unless it matches."""
    return f' data-show="{_e(show)}"' if show else ""


def _help(h):
    return f'<div class="help">{h}</div>' if h else ""


def num(name, label, value, unit=None, pre=None, step="any", min=None, max=None,
        help=None, tip=None, cls="", row=False, show=None):
    """Number input with optional prefix ($) and unit suffix."""
    fid = f"f-{name}" if not row else ""
    key = f'data-k="{name}"' if row else f'name="{name}" id="{fid}"'
    attrs = f' step="{step}"'
    if min is not None:
        attrs += f' min="{min}"'
    if max is not None:
        attrs += f' max="{max}"'
    p = f'<span class="pre">{pre}</span>' if pre else ""
    u = f'<span class="unit">{unit}</span>' if unit else ""
    lab = _label(fid, label, tip) if not row else f'<span class="lbl">{label}</span>'
    return (f'<div class="field {cls}"{_show(show)}>{lab}<div class="inp">{p}'
            f'<input type="number" inputmode="decimal" {key} value="{value}"{attrs}>{u}</div>{_help(help)}</div>')


def text(name, label, value="", placeholder="", cls="", row=False, autoname=None, show=None):
    fid = f"f-{name}" if not row else ""
    key = f'data-k="{name}"' if row else f'name="{name}" id="{fid}"'
    an = f' data-autoname="{_e(autoname)}"' if autoname else ""
    lab = _label(fid, label) if not row else f'<span class="lbl">{label}</span>'
    return (f'<div class="field {cls}"{_show(show)}>{lab}<div class="inp"><input type="text" {key} '
            f'value="{_e(value)}" placeholder="{_e(placeholder)}"{an}></div></div>')


def select(name, label, options, value=None, help=None, tip=None, numeric=False, cls="", row=False, show=None):
    """options: list of (value, label) or plain strings."""
    fid = f"f-{name}" if not row else ""
    key = f'data-k="{name}"' if row else f'name="{name}" id="{fid}"'
    opts = []
    for o in options:
        v, l = (o, o) if isinstance(o, str) else o
        sel = " selected" if str(v) == str(value) else ""
        opts.append(f'<option value="{_e(v)}"{sel}>{_e(l)}</option>')
    dn = " data-num" if numeric else ""
    lab = _label(fid, label, tip) if not row else f'<span class="lbl">{label}</span>'
    return (f'<div class="field {cls}"{_show(show)}>{lab}<div class="inp"><select {key}{dn}>'
            f'{"".join(opts)}</select></div>{_help(help)}</div>')


def seg(name, label, options, value, cls="full", numeric=False, tip=None, show=None):
    """Segmented radio control."""
    dn = " data-num" if numeric else ""
    items = []
    for o in options:
        v, l = (o, o) if isinstance(o, str) else o
        chk = " checked" if str(v) == str(value) else ""
        items.append(f'<label><input type="radio" name="{name}" value="{_e(v)}"{chk}{dn}><span>{_e(l)}</span></label>')
    t = f' <span class="tip" tabindex="0" data-tip="{_e(tip)}" aria-label="{_e(tip)}">?</span>' if tip else ""
    return (f'<div class="field {cls}"{_show(show)} role="radiogroup" aria-label="{_e(label)}"><span class="lbl">{label}{t}</span>'
            f'<div class="seg">{"".join(items)}</div></div>')


def switch(name, label, checked=False, cls="full", row=False, show=None):
    key = f'data-k="{name}"' if row else f'name="{name}"'
    c = " checked" if checked else ""
    return f'<label class="switch {cls}"{_show(show)}><span>{label}</span><input type="checkbox" {key}{c}></label>'


def rng(name, label, value, min, max, step=1, suffix="", cls="full", help=None, show=None):
    fid = f"f-{name}"
    return (f'<div class="field range-field {cls}"{_show(show)}><label class="lbl" for="{fid}">{label}'
            f'<output for="{fid}">{value}{suffix}</output></label>'
            f'<input type="range" name="{name}" id="{fid}" value="{value}" min="{min}" max="{max}" step="{step}" '
            f'data-suffix="{_e(suffix)}">{_help(help)}</div>')


def group(legend, *fields, cols=2):
    c = " fields--3" if cols == 3 else ""
    return f'<fieldset class="fieldset"><legend>{legend}</legend><div class="fields{c}">{"".join(fields)}</div></fieldset>'


def prices(title, *fields, note=None, cols=2):
    """Collapsible 'edit unit prices' panel. Inputs inside are ordinary fields."""
    c = " fields--3" if cols == 3 else ""
    n = f'<p class="help" style="margin:12px 0 0">{note}</p>' if note else ""
    return ('<details class="price-panel"><summary>'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>'
            f'{title}<small>Texas 2026 defaults · editable</small></summary>'
            f'<div class="pp-body"><div class="fields{c}">{"".join(fields)}</div>{n}</div></details>')


DEL = ('<button type="button" class="row-del" aria-label="Remove row"><svg viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18"/>'
       '<path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/></svg></button>')


def rows(name, fields_html, start=1, min=1, add_label="Add another", legend=None):
    """Repeatable rows. fields_html is built with row=True helpers."""
    lg = f'<legend>{legend}</legend>' if legend else ""
    return (f'<fieldset class="fieldset">{lg}<div class="rows" data-rows="{name}" data-template="tpl-{name}" '
            f'data-start="{start}" data-min="{min}"></div>'
            f'<template id="tpl-{name}"><div class="row-item">{fields_html}{DEL}</div></template>'
            f'<button type="button" class="btn btn--ghost btn--sm add-row" data-add-row="{name}">+ {add_label}</button></fieldset>')


def panel(title, inner, n=None):
    badge = f'<span class="num">{n}</span>' if n else ""
    return f'<div class="panel-title"><h2>{badge}{title}</h2></div>{inner}'
