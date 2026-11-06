# Lighthouse results: live site

URL: https://sandybrown-bear-867005.hostingersite.com · Lighthouse 12 · run November 6, 2026

The SEO score caps at about 66 because the demo is deliberately `noindex` (meta tag plus `X-Robots-Tag` header). "SEO without noindex" re-weights the SEO category with the `is-crawlable` audit excluded.

| Page | Device | Performance | Accessibility | Best practices | SEO | SEO without noindex | LCP | CLS |
|---|---|---|---|---|---|---|---|---|
| Home | Mobile | 99 | 100 | 100 | 66 | 100 | 2.0 s | 0 |
| Home | Desktop | 100 | 100 | 100 | 66 | 100 | 0.6 s | 0 |
| The Studios | Mobile | 100 | 100 | 100 | 66 | 100 | 1.7 s | 0 |
| The Studios | Desktop | 100 | 100 | 100 | 66 | 100 | 0.4 s | 0.001 |
| Gallery | Mobile | 97 | 100 | 100 | 66 | 100 | 2.5 s | 0 |
| Gallery | Desktop | 100 | 100 | 100 | 66 | 100 | 0.4 s | 0 |
| Neighborhood | Mobile | 99 | 100 | 100 | 66 | 100 | 2.0 s | 0 |
| Neighborhood | Desktop | 91–98 | 100 | 100 | 66 | 100 | 1.0–1.6 s | 0.013 |
| Amenities | Mobile | 100 | 100 | 100 | 66 | 100 | 1.4 s | 0 |
| Amenities | Desktop | 100 | 100 | 100 | 66 | 100 | 0.4 s | 0.001 |
| Contact | Mobile | 100 | 100 | 100 | 63 | 100 | 1.6 s | 0 |
| Contact | Desktop | 100 | 100 | 100 | 63 | 100 | 0.4 s | 0 |

Neighborhood desktop varies between runs with server response time (about 0.5 s TTFB through the test network). Contact's raw SEO is 63 instead of 66 only because fewer SEO audits apply to that page.
