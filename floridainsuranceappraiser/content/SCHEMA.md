# Content module contract (read by build.py)

All copy is plain Python data. HTML strings may use <p>, <ul>/<ol>/<li>, <strong>, <em>,
<a href="/...">, <h3>, <table> (with <thead>/<tbody>). No <h1>/<h2> inside bodies; no inline styles,
no scripts. Use straight ASCII quotes inside Python strings carefully (prefer double-quoted
Python strings and typographic apostrophes ’ inside copy, or escape).
Import `from siteconfig import BIZ, PHONE, PHONE_LINK` if you need the phone/email.

Internal link targets that exist:
  /  /about/  /contact/  /appraisal-process/  /faq/  /claim-glossary/  /blog/
  /appraisal-services/<service-slug>/  /florida-locations/<city-slug>/  /claim-tools/<tool-slug>/
Service slugs: homeowners-claim-appraisal, hurricane-claim-appraisal, roof-claim-appraisal,
  water-damage-claim-appraisal, sinkhole-claim-appraisal, fire-smoke-claim-appraisal,
  condo-hoa-claim-appraisal, commercial-claim-appraisal, umpire-services, xactimate-estimate-review
City slugs: miami-fl, tampa-fl, orlando-fl, jacksonville-fl, fort-lauderdale-fl, west-palm-beach-fl,
  fort-myers-fl, naples-fl, sarasota-fl, st-petersburg-fl, tallahassee-fl, pensacola-fl
Tool slugs: appraisal-worth-it-calculator, hurricane-deductible-calculator, acv-depreciation-calculator,
  claim-deadline-calculator, roof-measurement-calculator, contents-inventory-builder, appraisal-readiness-quiz
Blog slugs: how-the-appraisal-clause-works-in-florida, florida-hurricane-deductible-explained,
  appraiser-vs-public-adjuster-vs-attorney-florida, what-to-do-when-a-florida-claim-is-underpaid,
  florida-roof-claims-after-the-2022-reforms

Common record fields:
  slug, title (<=60 chars, SEO <title>), description (meta, 140-158 chars), h1, kicker (3-6 word eyebrow),
  lead (1-2 sentence intro paragraph, plain text), sections: list of (h2_text, html_body),
  faqs: list of (question, answer_plain_text)  (3-5 items)
