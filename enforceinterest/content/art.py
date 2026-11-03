"""Decorative inline SVG art for claim-type cards (no external images)."""


def hail():
    dots = "".join(
        f'<circle cx="{(i * 53) % 400 + 10}" cy="{(i * 37) % 120 + 6}" r="{2 + i % 3}" fill="#fff" opacity="{0.25 + (i % 4) * .15}">'
        f'<animate attributeName="cy" from="{(i * 37) % 120 - 30}" to="{(i * 37) % 120 + 140}" dur="{1.6 + (i % 5) * .3}s" repeatCount="indefinite"/></circle>'
        for i in range(34))
    return (f'<svg class="art" viewBox="0 0 400 132" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<defs><linearGradient id="gh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3a4a"/><stop offset="1" stop-color="#170d0c"/></linearGradient></defs>'
            f'<rect width="400" height="132" fill="url(#gh)"/>{dots}'
            f'<path d="M0 118 L60 96 L120 118 L180 92 L240 118 L300 98 L360 118 L400 104 V132 H0z" fill="#6f1818" opacity=".9"/></svg>')


def hurricane():
    return ('<svg class="art" viewBox="0 0 400 132" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<defs><radialGradient id="gu" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#3b5566"/><stop offset="1" stop-color="#170d0c"/></radialGradient></defs>'
            '<rect width="400" height="132" fill="url(#gu)"/>'
            '<g transform="translate(200 66)" fill="none" stroke="#c9a24f" stroke-width="2" opacity=".75">'
            '<g><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="14s" repeatCount="indefinite"/>'
            '<path d="M0 0 C 30 -10 50 -40 20 -70 M0 0 C -30 10 -50 40 -20 70 M0 0 C 10 30 40 50 70 20 M0 0 C -10 -30 -40 -50 -70 -20"/>'
            '<circle r="9" stroke="#fff"/><circle r="40" stroke-dasharray="4 8" opacity=".5"/><circle r="64" stroke-dasharray="2 10" opacity=".35"/></g></g></svg>')


def fire():
    return ('<svg class="art" viewBox="0 0 400 132" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<defs><linearGradient id="gf" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#b33a2e"/><stop offset=".55" stop-color="#4a0f0f"/><stop offset="1" stop-color="#170d0c"/></linearGradient></defs>'
            '<rect width="400" height="132" fill="url(#gf)"/>'
            '<g fill="none" stroke="#fff" stroke-linecap="round" opacity=".18" stroke-width="10">'
            '<path d="M40 140 C 60 90 20 70 60 30"><animate attributeName="d" values="M40 140 C 60 90 20 70 60 30;M40 140 C 20 90 70 70 40 20;M40 140 C 60 90 20 70 60 30" dur="4s" repeatCount="indefinite"/></path>'
            '<path d="M160 140 C 190 100 140 60 180 20"><animate attributeName="d" values="M160 140 C 190 100 140 60 180 20;M160 140 C 140 100 200 60 160 10;M160 140 C 190 100 140 60 180 20" dur="5s" repeatCount="indefinite"/></path>'
            '<path d="M300 140 C 330 90 280 70 320 30"><animate attributeName="d" values="M300 140 C 330 90 280 70 320 30;M300 140 C 280 90 340 60 300 20;M300 140 C 330 90 280 70 320 30" dur="4.5s" repeatCount="indefinite"/></path></g>'
            '<path d="M0 132 H400 V120 Q350 110 300 120 T200 116 T100 122 T0 116z" fill="#170d0c"/></svg>')


def water():
    return ('<svg class="art" viewBox="0 0 400 132" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<defs><linearGradient id="gw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#170d0c"/><stop offset="1" stop-color="#1f4253"/></linearGradient></defs>'
            '<rect width="400" height="132" fill="url(#gw)"/>'
            '<g fill="none" stroke="#9fd0e0" stroke-width="2">'
            '<path opacity=".55" d="M0 80 Q 50 64 100 80 T 200 80 T 300 80 T 400 80 T 500 80"><animateTransform attributeName="transform" type="translate" from="0 0" to="-200 0" dur="6s" repeatCount="indefinite"/></path>'
            '<path opacity=".35" d="M0 96 Q 50 82 100 96 T 200 96 T 300 96 T 400 96 T 500 96 T 600 96"><animateTransform attributeName="transform" type="translate" from="-200 0" to="0 0" dur="8s" repeatCount="indefinite"/></path>'
            '<path opacity=".2" d="M0 112 Q 50 100 100 112 T 200 112 T 300 112 T 400 112 T 500 112"><animateTransform attributeName="transform" type="translate" from="0 0" to="-200 0" dur="10s" repeatCount="indefinite"/></path></g>'
            '<path d="M200 18 c 10 14 18 24 18 33 a18 18 0 0 1 -36 0 c0 -9 8 -19 18 -33z" fill="#9fd0e0" opacity=".5"/></svg>')
