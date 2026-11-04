"""Search snippets: <title> and meta description overrides, kept in one place so lengths stay in range
(titles <= 65 characters, descriptions 70-160). build.py applies these after the pages are assembled."""
import lib

F = lib.FLOAT_RATE_S

TITLES = {
    "/texas-judgment-interest-rate/": f"Texas Judgment Interest Rate: {lib.JUDG_RATE_S} ({lib.RATE_MONTH[:3]} {lib.RATE_Y}) | Enforce Interest",
    "/hail-wind-claims/": "Texas Hail & Wind Claims Paid Late | Enforce Interest",
    "/hurricane-claims/": "Texas Hurricane Claims: Deadlines & Interest | Enforce Interest",
}

DESC = {
    "/": "Enforce Interest helps Texans recover statutory interest when insurers pay property claims late: 18% "
         "a year under §542.060. Free claim review.",
    "/fire-smoke-damage/": "Texas fire and smoke damage claims paid late: the 18% interest rate, arson timing, smoke "
                           "damage investigations, ACV holdbacks and contents.",
    "/texas-judgment-interest-rate/": f"The Texas postjudgment interest rate for {lib.RATE_MONTH} is {lib.JUDG_RATE_S} (Fin. "
                                      f"Code §304.003). Full OCCC history plus the {F} weather-claim rate.",
    "/texas-prompt-payment-act/": "The Texas Prompt Payment Act (Ins. Code ch. 542) section by section: 15-day, 15-business-day, "
                                  "5-day and 60-day deadlines, interest and key cases.",
    "/blog/": "Guides to Texas prompt-payment interest: the 18% and floating rates, Hinojos, 542A notice, freeze and smoke "
              "claims, deadlines and cancellation rules.",
    "/blog/how-long-to-file-a-freeze-claim-in-texas/": "How long you have to report and sue on a Texas freeze or burst-pipe "
                                                        "claim, freeze exclusions, catastrophe extensions and interest.",
    "/blog/act-of-god-floating-rate/": f"The Texas 'Act of God' floating rate on weather claims: §542.060(c), {lib.JUDG_RATE_S} + "
                                       f"5% = {F}, which claims it covers and the 2017 cutoff.",
    "/blog/18-standard-rate-explained/": "How the 18% prompt-payment interest rate in Texas Insurance Code §542.060(a) works: "
                                         "when it applies and starts, the math and partial payments.",
    "/blog/texas-homeowners-insurance-cancellation-rules/": "How long must a Texas homeowners policy be in force? The 60-day "
                                                            "cancellation rule in §551.104, notice periods and nonrenewal.",
    "/blog/542a-pre-suit-notice-explained/": "What Texas Insurance Code Chapter 542A requires before a weather-claim lawsuit: "
                                             "61-day notice, contents, inspection and the fee formula.",
    "/blog/texas-insurance-claim-deadlines/": "Every Texas insurance claim deadline in one place: reporting, Chapter 542's "
                                              "15/15/5/60-day rules, TWIA, 542A notice and limitations.",
    "/blog/smoke-damage-claim-texas/": "How Texas smoke damage claims work: smoke damage investigations, disputed scope, "
                                       "wildfire smoke, HVAC and contents, deadlines and interest.",
    "/blog/hinojos-v-state-farm-lloyds-explained/": "What the Texas Supreme Court decided in Hinojos v. State Farm Lloyds "
                                                    "(2021) and what it means for appraisal and partial payments.",
    "/texas-prejudgment-interest/": f"Texas prejudgment interest explained: the 180-day accrual rule, the {lib.JUDG_RATE_S} rate, "
                                    "settlement offers and §542.060 claims. Free calculator.",
    "/water-plumbing-damage/": "Texas water and plumbing damage claims paid late: sudden vs. seepage, mold, freeze, the 18% "
                               "interest rate and how to document a water claim.",
    "/statutory-damages-calculator/": f"Free Texas §542.060 statutory interest calculator: 18% or {F} floating rate, partial "
                                      "payments, supplements and a printable memo.",
    "/does-my-claim-qualify/": "Free two-minute check: does your Texas insurance claim qualify for prompt-payment interest "
                               "under §542.060? Find out where you stand.",
    "/about-us/": f"Enforce Interest is a {lib.FIRM} service (TDI license #{lib.LICENSE}) focused on Texas prompt-payment "
                  "interest on late-paid property claims.",
    "/contact/": "Send your Texas insurance claim to Enforce Interest for a free review. We rebuild the timeline and "
                 "calculate statutory interest. No upfront cost.",
    "/tools/": "Free Texas insurance claim tools: statutory interest, Chapter 542 deadlines, appraisal interest, judgment "
               "rates, prejudgment interest and more.",
    "/tools/appraisal-interest-calculator/": "Calculate Texas prompt-payment interest on the gap between pre-appraisal "
                                             "payments and the award (Hinojos), and check for shortfalls.",
    "/tools/public-adjuster-fee-calculator/": "Texas public adjuster fee calculator: the 10% cap in Insurance Code "
                                              "§4102.104, what you net and your break-even settlement.",
    "/tools/depreciation-calculator/": "Calculate depreciation, actual cash value and recoverable depreciation on an "
                                       "insurance claim, with typical lifespans for roofs and more.",
    "/tools/542a-notice-calculator/": "Texas Chapter 542A calculator: 61-day pre-suit notice dates, the 30-day inspection "
                                      "window and the §542A.007 attorney-fee ratio.",
    "/tools/claim-timeline-builder/": "Log Texas insurance claim events, see the Chapter 542 deadlines they trigger, flag "
                                      "late payments and print a status-request letter.",
    "/tools/claim-deadline-calculator/": "Calculate every Texas Chapter 542 claim deadline from your notice date: 15 days, "
                                         "15 business days, 5 business days, 60 days and more.",
    "/hail-wind-claims/": f"Texas hail and wind claims paid late: deadlines, the 61-day 542A notice, the {F} floating "
                          "interest rate, roof supplements and evidence.",
    "/tools/wind-hail-deductible-calculator/": "Convert a percentage wind/hail or named-storm deductible into dollars "
                                               "and see what a Texas storm claim pays after it.",
    "/disclaimer/": "Enforce Interest is a public adjusting service, not a law firm. What to know about our content, "
                    "calculators, fees and licensing.",
    "/faq/": "Answers on the Texas 60-day rule, 18% and floating-rate interest, appraisal, supplements, deadlines to sue and "
             "how our free review works.",
    "/long-term-claim-supplements/": "How Texas prompt-payment deadlines and interest apply to claim supplements: hidden "
                                     "damage, code upgrades and stacking interest.",
    "/post-appraisal-interest-recovery/": "Insurer paid the appraisal award but not the interest? How Hinojos and Rodriguez "
                                          "apply in Texas and how post-appraisal interest works.",
    "/hurricane-claims/": "Texas hurricane claims: private insurer deadlines and floating interest, TWIA's one-year, 60-day "
                          "and 10-day rules, deductibles and wind vs. flood.",
}
