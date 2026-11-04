#!/usr/bin/env python3
"""Generate app/data/states.json for cpacalculator.com.
Primary compilation: Tax Foundation "State Individual Income Tax Rates and Brackets, 2026" (data as of Feb 11 2026),
updated for later 2026 legislation (GA HB 463, UT SB 60, SC H.4216, WV SB 392, AR Act 1/2 2026 special session,
HI Act 46 std deduction, AZ HB 4168 conformity, ME 2026 std, MA 2026 surtax threshold, OH R.C. 5747.02)."""
import json, sys

N = None
FED = {"single": 16100, "mfj": 32200, "hoh": 24150}  # 2026 federal standard deduction (OBBBA)

def flat(rate, zero_to=None, zero_mfj=None):
    if zero_to:
        return {"single": [[zero_to, 0], [N, rate]], "mfj": [[zero_mfj or zero_to, 0], [N, rate]]}
    return {"single": [[N, rate]]}

def none(name, slug, sales, notes, source, local="No local income taxes."):
    return dict(name=name, slug=slug, type="none", year=2026, base="none", brackets={}, std={"single": 0, "mfj": 0},
                exemption={"personal": 0, "dependent": 0}, local=local, salesTax=sales, notes=notes, source=source)

S = {}

S["AL"] = dict(name="Alabama", slug="alabama", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[500, .02], [3000, .04], [N, .05]], "mfj": [[1000, .02], [6000, .04], [N, .05]], "hoh": "single"},
  std={"single": 3000, "mfj": 8500, "hoh": 5200, "mfs": 4250},
  stdPhase={"single": [25499, 35499, 2500], "mfj": [25999, 35999, 5000], "hoh": [25999, 35999, 2500], "mfs": [12999, 17999, 2500]},
  exemption={"personal": 1500, "personalByStatus": {"single": 1500, "mfj": 3000, "hoh": 3000, "mfs": 1500}, "dependent": 1000},
  special="al", fedTaxDeduction="full",
  local="About two dozen cities and counties levy occupational license taxes on wages earned there — for example Birmingham (1%), Bessemer (1%) and Gadsden (2%).",
  salesTax=4, notes="Alabama is one of the few states that lets you deduct the federal income tax you paid, which lowers the effective rate. The standard deduction shrinks as income rises, and the dependent exemption falls from $1,000 to $500 above $50,000 of AGI and to $300 above $100,000.",
  source="https://www.revenue.alabama.gov/individual-corporate/")

S["AK"] = none("Alaska", "alaska", 0, "Alaska has no state individual income tax and no statewide sales tax, though many boroughs and cities levy local sales taxes. Permanent Fund Dividend payments are taxable on your federal return.", "https://tax.alaska.gov/")

S["AZ"] = dict(name="Arizona", slug="arizona", type="flat", year=2026, base="federal_agi",
  brackets=flat(.025), std=dict(FED), exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 0, "dependentCredit": 100},
  local="No local income taxes.", salesTax=5.6,
  notes="Arizona taxes all income at a flat 2.5%. HB 4168 (2026) re-conformed Arizona to the federal standard deduction for 2026. A $100 credit is allowed for each dependent under 17 ($25 for older dependents), phasing out above $200,000 of income ($400,000 joint).",
  source="https://azdor.gov/individuals")

S["AR"] = dict(name="Arkansas", slug="arkansas", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[4600, .02], [N, .037]]},
  lowIncome={"max": 92300, "brackets": [[5499, 0], [10899, .02], [15599, .03], [25699, .034], [N, .037]]},
  std={"single": 2470, "mfj": 4940, "hoh": 2470}, exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 29, "dependentCredit": 29},
  local="No local income taxes.", salesTax=6.5,
  notes="A May 2026 special session cut the top rate from 3.9% to 3.7%, retroactive to January 1, 2026. Filers with net income of about $92,300 or less use a separate low-income table (0% to 3.7%); thresholds shown are the latest published (2025) amounts, and the small bracket-adjustment band just above that level is simplified.",
  source="https://www.dfa.arkansas.gov/office/taxes/income-tax-administration/")

S["CA"] = dict(name="California", slug="california", type="progressive", year=2025, base="federal_agi",
  brackets={"single": [[11079, .01], [26264, .02], [41452, .04], [57542, .06], [72724, .08], [371479, .093], [445771, .103], [742953, .113], [1000000, .123], [N, .133]],
            "mfj": [[22158, .01], [52528, .02], [82904, .04], [115084, .06], [145448, .08], [742958, .093], [891542, .103], [1000000, .113], [1485906, .123], [N, .133]],
            "hoh": [[22173, .01], [52530, .02], [67716, .04], [83805, .06], [98990, .08], [505208, .093], [606251, .103], [1000000, .113], [1010417, .123], [N, .133]]},
  std={"single": 5706, "mfj": 11412, "hoh": 11412}, exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 153, "dependentCredit": 475}, special="ca",
  local="No city or county income taxes on residents (San Francisco and some cities tax businesses on payroll or gross receipts instead).", salesTax=7.25,
  notes="Brackets include the 1% Mental Health Services Tax on taxable income over $1 million, so the top rate is 13.3%. Wages are also subject to the 1.3% State Disability Insurance (SDI) payroll tax with no wage cap (not included here). Figures are the 2025 inflation-indexed amounts; California publishes 2026 indexing late in the year.",
  source="https://www.ftb.ca.gov/file/personal/tax-calculator-tables-rates.html")

S["CO"] = dict(name="Colorado", slug="colorado", type="flat", year=2026, base="federal_taxable",
  brackets=flat(.044), std=dict(FED), exemption={"personal": 0, "dependent": 0},
  local="Denver, Aurora, Greenwood Village, Glendale and Sheridan charge small monthly occupational privilege taxes (Denver: $5.75 a month for employees).", salesTax=2.9,
  notes="Colorado starts from federal taxable income, so the federal standard deduction is built in, and taxes it at a flat 4.4%. TABOR surplus refunds and temporary rate reductions can change the effective rate in high-revenue years.",
  source="https://tax.colorado.gov/individual-income-tax")

S["CT"] = dict(name="Connecticut", slug="connecticut", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[10000, .02], [50000, .045], [100000, .055], [200000, .06], [250000, .065], [500000, .069], [N, .0699]],
            "mfj": [[20000, .02], [100000, .045], [200000, .055], [400000, .06], [500000, .065], [1000000, .069], [N, .0699]],
            "hoh": [[16000, .02], [80000, .045], [160000, .055], [320000, .06], [400000, .065], [800000, .069], [N, .0699]]},
  std={"single": 0, "mfj": 0}, exemption={"personal": 15000, "personalByStatus": {"single": 15000, "mfj": 24000, "hoh": 19000, "mfs": 12000}, "dependent": 0},
  exemptionPhase={"single": [30000, 45000], "mfj": [48000, 72000], "hoh": [38000, 57000], "mfs": [24000, 36000]},
  special="ct",
  local="No local income taxes.", salesTax=6.35,
  notes="Connecticut has no standard deduction; its personal exemption phases out completely by $45,000 of AGI for single filers ($72,000 joint). Higher earners lose the benefit of the 2% bracket and pay “benefit recapture” amounts, so many high-income taxpayers effectively pay their top rate on all income. The low-income personal tax credit (1%–75%) is not modeled.",
  source="https://portal.ct.gov/drs")

S["DE"] = dict(name="Delaware", slug="delaware", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[2000, 0], [5000, .022], [10000, .039], [20000, .048], [25000, .052], [60000, .0555], [N, .066]]},
  std={"single": 3250, "mfj": 6500, "hoh": 3250}, exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 110, "dependentCredit": 110},
  local="Wilmington levies a 1.25% earned income tax on residents and on non-residents who work in the city.", salesTax=0,
  notes="Delaware has no sales tax but a graduated income tax that reaches 6.6% above $60,000. Brackets are the same for every filing status, so married couples don’t get wider brackets. Each personal exemption is a $110 credit.",
  source="https://revenue.delaware.gov/")

S["FL"] = none("Florida", "florida", 6, "Florida has no state personal income tax — the state constitution prohibits one. Revenue comes mainly from the 6% sales tax plus local discretionary surtaxes, and from property taxes.", "https://floridarevenue.com/")

S["GA"] = dict(name="Georgia", slug="georgia", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0499), std={"single": 15000, "mfj": 30000, "hoh": 15000}, exemption={"personal": 0, "dependent": 5000},
  local="No local income taxes.", salesTax=4,
  notes="HB 463 (signed May 2026) cut the flat rate from 5.19% to 4.99% retroactive to January 1, 2026, raised the standard deduction to $15,000 ($30,000 joint) and the dependent exemption to $5,000. Further 0.125-point annual cuts toward 3.99% depend on revenue triggers.",
  source="https://dor.georgia.gov/taxes/individual-taxes")

S["HI"] = dict(name="Hawaii", slug="hawaii", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[9600, .014], [14400, .032], [19200, .055], [24000, .064], [36000, .068], [48000, .072], [125000, .076], [175000, .079], [225000, .0825], [275000, .09], [325000, .10], [N, .11]],
            "mfj": [[19200, .014], [28800, .032], [38400, .055], [48000, .064], [72000, .068], [96000, .072], [250000, .076], [350000, .079], [450000, .0825], [550000, .09], [650000, .10], [N, .11]],
            "hoh": [[14400, .014], [21600, .032], [28800, .055], [36000, .064], [54000, .068], [72000, .072], [187500, .076], [262500, .079], [337500, .0825], [412500, .09], [487500, .10], [N, .11]]},
  std={"single": 8000, "mfj": 16000, "hoh": 12000}, exemption={"personal": 1144, "dependent": 1144},
  local="No local income taxes (counties add a 0.5% surcharge to the 4% general excise tax).", salesTax=4,
  notes="Hawaii has 12 brackets, the most of any state, topping out at 11%. Act 46 roughly doubled the standard deduction for 2026 to $8,000 single / $16,000 joint, with more increases through 2031. Act 24 (2026) adds a 13% rate on income over $1 million starting in 2027.",
  source="https://tax.hawaii.gov/")

S["ID"] = dict(name="Idaho", slug="idaho", type="flat", year=2026, base="federal_taxable",
  brackets={"single": [[4811, 0], [N, .053]], "mfj": [[9622, 0], [N, .053]], "hoh": "mfj"},
  std=dict(FED), exemption={"personal": 0, "dependent": 0},
  local="No local income taxes.", salesTax=6,
  notes="Idaho taxes income above a small zero bracket at a flat 5.3% (cut from 5.695% by HB 40, retroactive to 2025). It starts from federal taxable income, so the federal standard deduction applies. The zero-bracket amount shown is the latest published (2025) figure.",
  source="https://tax.idaho.gov/taxes/income-tax/individual-income/")

S["IL"] = dict(name="Illinois", slug="illinois", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0495), std={"single": 0, "mfj": 0}, exemption={"personal": 2925, "dependent": 2925},
  exemptionCliff={"single": 250000, "mfj": 500000, "hoh": 250000, "mfs": 250000},
  local="No local income taxes — Chicago does not tax wages.", salesTax=6.25,
  notes="Illinois taxes all net income at a flat 4.95% after a $2,925 exemption per person (2026). The exemption is lost entirely once AGI exceeds $250,000 ($500,000 joint). Retirement income such as Social Security, pensions and IRA distributions is exempt.",
  source="https://tax.illinois.gov/individuals.html")

S["IN"] = dict(name="Indiana", slug="indiana", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0295), std={"single": 0, "mfj": 0}, exemption={"personal": 1000, "dependent": 2500}, localBase="taxable",
  local="Every county levies a local income tax on residents, roughly 0.5% to 3% depending on the county (Marion County/Indianapolis is 2.02%). Enter your county rate in the local tax box.", salesTax=7,
  notes="Indiana’s flat rate fell to 2.95% for 2026 and is scheduled to reach 2.9%. Each taxpayer gets a $1,000 exemption and each qualifying dependent child an extra $1,500. County income taxes add significantly to the total.",
  source="https://www.in.gov/dor/individual-income-taxes/")

S["IA"] = dict(name="Iowa", slug="iowa", type="flat", year=2026, base="federal_taxable",
  brackets=flat(.038), std=dict(FED), exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 40, "dependentCredit": 40},
  local="Many school districts add an income surtax calculated as a percentage of your Iowa tax.", salesTax=6,
  notes="Iowa completed its move to a flat 3.8% tax in 2025 and starts from federal taxable income. Retirement income is fully exempt for those 55 and older. Each person and dependent gets a $40 credit.",
  source="https://revenue.iowa.gov/taxes/tax-guidance/individual-income-tax")

S["KS"] = dict(name="Kansas", slug="kansas", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[23000, .052], [N, .0558]], "mfj": [[46000, .052], [N, .0558]], "hoh": "single"},
  std={"single": 3605, "mfj": 8240, "hoh": 6180}, exemption={"personal": 9160, "personalByStatus": {"single": 9160, "mfj": 18320, "hoh": 9160, "mfs": 9160}, "dependent": 2320},
  local="No local taxes on wages.", salesTax=6.5,
  notes="Kansas moved to two brackets (5.2% and 5.58%) in 2024 with a large $9,160 personal exemption ($18,320 joint). Social Security benefits are fully exempt from Kansas tax.",
  source="https://www.ksrevenue.gov/perstaxtypesii.html")

S["KY"] = dict(name="Kentucky", slug="kentucky", type="flat", year=2026, base="federal_agi",
  brackets=flat(.035), std={"single": 3360, "mfj": 3360, "hoh": 3360}, exemption={"personal": 0, "dependent": 0},
  local="Most cities and counties levy occupational license taxes on wages — e.g. Louisville Metro about 2.2% and Lexington-Fayette 2.25%.", salesTax=6,
  notes="Kentucky’s flat rate dropped to 3.5% for 2026 under revenue-triggered cuts, with further cuts possible. The $3,360 standard deduction is not doubled on a joint return, so many couples file separately on the same form.",
  source="https://revenue.ky.gov/Individual/Pages/default.aspx")

S["LA"] = dict(name="Louisiana", slug="louisiana", type="flat", year=2026, base="federal_agi",
  brackets=flat(.03), std={"single": 12875, "mfj": 25750, "hoh": 25750}, exemption={"personal": 0, "dependent": 0},
  local="No local income taxes.", salesTax=5,
  notes="Louisiana replaced its graduated brackets with a flat 3% rate and a much larger standard deduction starting in 2025, and repealed personal exemptions. The state sales tax rate rose to 5% in 2025.",
  source="https://revenue.louisiana.gov/individual-income-tax/")

S["ME"] = dict(name="Maine", slug="maine", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[27399, .058], [64849, .0675], [N, .0715]], "mfj": [[54849, .058], [129749, .0675], [N, .0715]],
            "hoh": [[41100, .058], [97300, .0675], [N, .0715]]},
  std={"single": 15700, "mfj": 31400, "hoh": 23550}, stdPhase={"single": [100000, 175000, 0], "mfj": [200050, 350050, 0], "hoh": [150000, 262500, 0]},
  exemption={"personal": 5300, "dependent": 0}, credits={"personalCredit": 0, "dependentCredit": 305},
  local="No local income taxes.", salesTax=5.5,
  notes="Maine phases in conformity with the new federal standard deduction: $15,700 single / $31,400 joint for 2026, phasing out at higher incomes. The refundable dependent credit is $305 per dependent ($610 for children five and under). Head-of-household brackets here are approximate.",
  source="https://www.maine.gov/revenue/taxes/income-estate-tax/individual-income-tax")

S["MD"] = dict(name="Maryland", slug="maryland", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[1000, .02], [2000, .03], [3000, .04], [100000, .0475], [125000, .05], [150000, .0525], [250000, .055], [500000, .0575], [1000000, .0625], [N, .065]],
            "mfj": [[1000, .02], [2000, .03], [3000, .04], [150000, .0475], [175000, .05], [225000, .0525], [300000, .055], [600000, .0575], [1200000, .0625], [N, .065]], "hoh": "mfj"},
  std={"single": 3350, "mfj": 6700, "hoh": 6700}, exemption={"personal": 3200, "dependent": 3200}, special="md", localBase="taxable",
  local="All 23 counties and Baltimore City levy a local income tax of 2.25% to 3.3% of Maryland taxable income — this often adds more than half again to the state tax. Enter your county rate in the local tax box.", salesTax=6,
  notes="The 2025 Budget Reconciliation Act added 6.25% and 6.5% brackets above $500,000 and $1 million, replaced the percentage standard deduction with a flat $3,350 ($6,700 joint), and added a 2% surtax on capital gains for AGI over $350,000. Personal exemptions phase out above $100,000 of AGI ($150,000 joint).",
  source="https://www.marylandcomptroller.gov/individuals/taxes/income-tax.html")

S["MA"] = dict(name="Massachusetts", slug="massachusetts", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[1107750, .05], [N, .09]]},
  std={"single": 0, "mfj": 0}, exemption={"personal": 4400, "personalByStatus": {"single": 4400, "mfj": 8800, "hoh": 6800, "mfs": 4400}, "dependent": 1000},
  local="No local income taxes.", salesTax=6.25,
  notes="Massachusetts taxes most income at a flat 5%, plus the 4% “millionaires’ tax” surtax on taxable income over $1,107,750 for 2026 (indexed each year), for a 9% top rate. Short-term capital gains are taxed at 8.5%. Paid Family and Medical Leave payroll contributions are separate.",
  source="https://www.mass.gov/info-details/massachusetts-tax-rates")

S["MI"] = dict(name="Michigan", slug="michigan", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0425), std={"single": 0, "mfj": 0}, exemption={"personal": 5900, "dependent": 5900},
  local="24 cities levy an income tax: Detroit 2.4% for residents (1.2% non-residents), Grand Rapids 1.5%, Saginaw 1.5%, Highland Park 2%, and most others 1%.", salesTax=6,
  notes="Michigan’s flat rate is 4.25%, with a personal exemption of $5,900 per person and dependent for 2026. Retirement income exemptions are being phased back in through 2026.",
  source="https://www.michigan.gov/taxes/iit")

S["MN"] = dict(name="Minnesota", slug="minnesota", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[33310, .0535], [109430, .068], [203150, .0785], [N, .0985]], "mfj": [[48700, .0535], [193480, .068], [337930, .0785], [N, .0985]], "hoh": "single"},
  std={"single": 15300, "mfj": 30600, "hoh": 23000}, exemption={"personal": 0, "dependent": 5300}, special="mn",
  local="No local income taxes.", salesTax=6.875,
  notes="Minnesota has four brackets topping out at 9.85%, plus a 1% surtax on net investment income over $1 million. The standard deduction is reduced for AGI above about $244,400. Head-of-household filers use the single brackets in this estimate, which slightly overstates their tax.",
  source="https://www.revenue.state.mn.us/minnesota-income-tax-rates-and-brackets")

S["MS"] = dict(name="Mississippi", slug="mississippi", type="flat", year=2026, base="federal_agi",
  brackets={"single": [[10000, 0], [N, .04]]},
  std={"single": 2300, "mfj": 4600, "hoh": 3400}, exemption={"personal": 6000, "personalByStatus": {"single": 6000, "mfj": 12000, "hoh": 8000, "mfs": 6000}, "dependent": 1500},
  local="No local income taxes.", salesTax=7,
  notes="Mississippi exempts the first $10,000 of taxable income and taxes the rest at 4% for 2026, down from 4.4%. The Build Up Mississippi Act phases the rate down to 3% by 2030, with further cuts possible.",
  source="https://www.dor.ms.gov/individual")

S["MO"] = dict(name="Missouri", slug="missouri", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[1348, 0], [2696, .02], [4044, .025], [5392, .03], [6740, .035], [8088, .04], [9436, .045], [N, .047]]},
  std=dict(FED), exemption={"personal": 0, "dependent": 0}, fedTaxDeduction="mo",
  local="Kansas City and St. Louis levy a 1% earnings tax on residents and on non-residents who work in the city.", salesTax=4.225,
  notes="Missouri’s top rate is 4.7% and applies above just $9,436 of taxable income, so most workers effectively pay a near-flat rate. You can deduct part of your federal income tax (35% down to 0% depending on AGI, capped at $5,000 / $10,000 joint). Capital gains are exempt starting in 2025.",
  source="https://dor.mo.gov/taxation/individual/")

S["MT"] = dict(name="Montana", slug="montana", type="progressive", year=2026, base="federal_taxable",
  brackets={"single": [[47500, .047], [N, .0565]], "mfj": [[95000, .047], [N, .0565]], "hoh": [[71250, .047], [N, .0565]]},
  std=dict(FED), exemption={"personal": 0, "dependent": 0},
  local="No local income taxes.", salesTax=0,
  notes="Montana starts from federal taxable income and has two rates; the top rate fell to 5.65% for 2026 and is scheduled to drop to 5.4% in 2027. Montana has no general sales tax.",
  source="https://mtrevenue.gov/taxes/individual-income-tax/")

S["NE"] = dict(name="Nebraska", slug="nebraska", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[4130, .0246], [24760, .0351], [N, .0455]], "mfj": [[8250, .0246], [49530, .0351], [N, .0455]], "hoh": "single"},
  std={"single": 8850, "mfj": 17700, "hoh": 13000}, exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 176, "dependentCredit": 176},
  local="No local income taxes.", salesTax=5.5,
  notes="Nebraska’s top rate dropped to 4.55% for 2026 and is scheduled to reach 3.99% in 2027. Each personal and dependent exemption is a $176 credit. Social Security benefits are fully exempt. Head-of-household brackets are approximated with the single schedule.",
  source="https://revenue.nebraska.gov/individuals")

S["NV"] = none("Nevada", "nevada", 6.85, "Nevada has no personal income tax. It relies on sales taxes (6.85% state rate plus local add-ons), gaming taxes and a payroll-based Modified Business Tax paid by employers.", "https://tax.nv.gov/")

S["NH"] = none("New Hampshire", "new-hampshire", 0, "New Hampshire has never taxed wages, and its 3% Interest & Dividends Tax was repealed for tax periods beginning on or after January 1, 2025, so it now has no individual income tax at all. There is also no general sales tax.", "https://www.revenue.nh.gov/")

S["NJ"] = dict(name="New Jersey", slug="new-jersey", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[20000, .014], [35000, .0175], [40000, .035], [75000, .05525], [500000, .0637], [1000000, .0897], [N, .1075]],
            "mfj": [[20000, .014], [50000, .0175], [70000, .0245], [80000, .035], [150000, .05525], [500000, .0637], [1000000, .0897], [N, .1075]], "hoh": "mfj"},
  std={"single": 0, "mfj": 0}, exemption={"personal": 1000, "dependent": 1500},
  local="No local income taxes on residents (Newark levies a 1% payroll tax on employers).", salesTax=6.625,
  notes="New Jersey has no standard deduction, only $1,000 personal and $1,500 dependent exemptions, and its 10.75% top rate on income over $1 million is among the highest in the nation. NJ’s gross-income tax uses its own definitions (for example, 401(k) deferrals are excluded but some other pre-tax items are not).",
  source="https://www.nj.gov/treasury/taxation/")

S["NM"] = dict(name="New Mexico", slug="new-mexico", type="progressive", year=2026, base="federal_taxable",
  brackets={"single": [[5500, .015], [16500, .032], [33500, .043], [66500, .047], [210000, .049], [N, .059]],
            "mfj": [[8000, .015], [25000, .032], [50000, .043], [100000, .047], [315000, .049], [N, .059]], "hoh": "mfj"},
  std=dict(FED), exemption={"personal": 0, "dependent": 4000}, special="nm",
  local="No local income taxes.", salesTax=4.875,
  notes="New Mexico restructured its brackets in 2025, adding a 1.5% bottom rate; the top rate is 5.9%. It uses the federal standard deduction and allows a $4,000 deduction for each dependent after the first. The 4.875% gross receipts tax applies to most services as well as goods.",
  source="https://www.tax.newmexico.gov/individuals/")

S["NY"] = dict(name="New York", slug="new-york", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[8500, .039], [11700, .044], [13900, .0515], [80650, .054], [215400, .059], [1077550, .0685], [5000000, .0965], [25000000, .103], [N, .109]],
            "mfj": [[17150, .039], [23600, .044], [27900, .0515], [161550, .054], [323200, .059], [2155350, .0685], [5000000, .0965], [25000000, .103], [N, .109]],
            "hoh": [[12800, .039], [17650, .044], [20900, .0515], [107650, .054], [269300, .059], [1616450, .0685], [5000000, .0965], [25000000, .103], [N, .109]]},
  std={"single": 8000, "mfj": 16050, "hoh": 11200}, exemption={"personal": 0, "dependent": 1000},
  recapture={"start": 107650, "span": 50000},
  localTax={"nyc": {"label": "New York City resident tax", "brackets": {
      "single": [[12000, .03078], [25000, .03762], [50000, .03819], [N, .03876]],
      "mfj": [[21600, .03078], [45000, .03762], [90000, .03819], [N, .03876]],
      "hoh": [[14400, .03078], [30000, .03762], [60000, .03819], [N, .03876]]}},
    "yonkers": {"label": "Yonkers resident surcharge", "pctOfState": .1675}},
  local="New York City residents pay an additional city income tax of 3.078% to 3.876% of NY taxable income, and Yonkers residents pay a surcharge of 16.75% of their net state tax. Non-residents who work in NYC do not pay the city tax. The MCTMT applies to self-employment income in the metro area.", salesTax=4,
  notes="The FY2026 budget cut the five lowest rates (now 3.9% to 5.9%) starting in 2026. Above $107,650 of AGI, New York “recaptures” the benefit of its lower brackets, so high earners pay a flat rate on all income; this calculator applies a simplified version of that recapture.",
  source="https://www.tax.ny.gov/pit/file/tax_tables.htm")

S["NC"] = dict(name="North Carolina", slug="north-carolina", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0399), std={"single": 12750, "mfj": 25500, "hoh": 19125}, exemption={"personal": 0, "dependent": 0},
  local="No local income taxes.", salesTax=4.75,
  notes="North Carolina’s flat rate reached 3.99% for 2026, the last scheduled step of the 2023 phase-down; further cuts toward 2.49% depend on revenue triggers. The state has its own standard deduction of $12,750 ($25,500 joint).",
  source="https://www.ncdor.gov/taxes-forms/individual-income-tax")

S["ND"] = dict(name="North Dakota", slug="north-dakota", type="progressive", year=2025, base="federal_taxable",
  brackets={"single": [[48475, 0], [244825, .0195], [N, .025]], "mfj": [[80975, 0], [298075, .0195], [N, .025]], "hoh": [[64950, 0], [271450, .0195], [N, .025]]},
  std=dict(FED), exemption={"personal": 0, "dependent": 0},
  local="No local income taxes.", salesTax=5,
  notes="North Dakota has one of the lowest income taxes in the country: 0% on the first $48,475 of federal taxable income (single), 1.95% above that and 2.5% at the top. Bracket thresholds are the latest published (2025) amounts.",
  source="https://www.tax.nd.gov/individual")

S["OH"] = dict(name="Ohio", slug="ohio", type="flat", year=2026, base="federal_agi",
  brackets={"single": [[26050, 0], [N, .0275]]}, addOver=[26050, 332],
  std={"single": 0, "mfj": 0}, exemption={"personal": 2400, "dependent": 2400}, special="oh",
  local="Most Ohio cities and villages levy a municipal income tax of about 1% to 3% on wages (Columbus 2.5%, Cleveland 2.5%, Cincinnati 1.8%), and many school districts add their own income tax.", salesTax=5.75,
  notes="Starting in 2026 Ohio has a single 2.75% rate: no tax on the first $26,050, then $332 plus 2.75% of the excess (Ohio Rev. Code 5747.02). Business income is taxed separately at 3% after a $250,000 deduction. Exemptions shrink as income rises and disappear above $500,000.",
  source="https://tax.ohio.gov/individual")

S["OK"] = dict(name="Oklahoma", slug="oklahoma", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[3750, 0], [4900, .025], [7200, .035], [N, .045]], "mfj": [[7500, 0], [9800, .025], [14400, .035], [N, .045]], "hoh": "mfj"},
  std={"single": 6350, "mfj": 12700, "hoh": 9350}, exemption={"personal": 1000, "dependent": 1000},
  local="No local income taxes.", salesTax=4.5,
  notes="HB 2764 collapsed Oklahoma’s six brackets into three for 2026 and cut the top rate from 4.75% to 4.5%, with further cuts toward 3.5% tied to revenue triggers.",
  source="https://oklahoma.gov/tax/individuals.html")

S["OR"] = dict(name="Oregon", slug="oregon", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[4550, .0475], [11400, .0675], [125000, .0875], [N, .099]], "mfj": [[9100, .0475], [22800, .0675], [250000, .0875], [N, .099]], "hoh": "mfj"},
  std={"single": 2910, "mfj": 5820, "hoh": 4690}, exemption={"personal": 0, "dependent": 0},
  credits={"personalCredit": 256, "dependentCredit": 256}, creditCliff={"single": 100000, "mfj": 200000, "hoh": 200000, "mfs": 100000},
  fedTaxDeduction="or",
  local="Portland-area residents with taxable income over $125,000 ($200,000 joint) owe the Metro Supportive Housing Services tax (1%) and, in Multnomah County, the Preschool for All tax (1.5%, rising to 3% over $250,000/$400,000). TriMet and Lane Transit payroll taxes and the 0.1% statewide transit tax are withheld from wages.", salesTax=0,
  notes="Oregon has no sales tax but one of the highest income taxes, reaching 9.9% above $125,000. You can subtract part of your federal income tax (about $8,500, phased out between $125,000 and $145,000 of AGI). The $256 personal exemption credit is not allowed above $100,000 of AGI ($200,000 joint).",
  source="https://www.oregon.gov/dor/programs/individuals/pages/default.aspx")

S["PA"] = dict(name="Pennsylvania", slug="pennsylvania", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0307), std={"single": 0, "mfj": 0}, exemption={"personal": 0, "dependent": 0}, pretaxDeductible=False,
  local="Nearly every municipality and school district levies an earned income tax (EIT), usually 1% to 2% combined; Philadelphia’s resident wage tax is about 3.74% and Pittsburgh’s is 3%. Many areas also charge a $52 local services tax.", salesTax=6,
  notes="Pennsylvania taxes income at a flat 3.07% with no standard deduction or personal exemptions. Employee 401(k) and 403(b) contributions are not deductible for PA tax, though retirement distributions are generally exempt. Tax forgiveness credits can eliminate the tax for low-income households.",
  source="https://www.revenue.pa.gov/TaxTypes/PIT/Pages/default.aspx")

S["RI"] = dict(name="Rhode Island", slug="rhode-island", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[82050, .0375], [186450, .0475], [N, .0599]]},
  std={"single": 11200, "mfj": 22400, "hoh": 16800}, exemption={"personal": 5250, "dependent": 5250},
  allowancePhase=[261000, 290800],
  local="No local income taxes.", salesTax=7,
  notes="Rhode Island uses the same three brackets (3.75%, 4.75%, 5.99%) for every filing status. The standard deduction and exemptions phase out between about $261,000 and $290,800 of income. A surtax on very high incomes begins in 2027.",
  source="https://tax.ri.gov/tax-sections/personal-income-tax")

S["SC"] = dict(name="South Carolina", slug="south-carolina", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[30000, .0199], [N, .0521]]},
  std={"single": 15000, "mfj": 30000, "hoh": 22500}, stdPhase={"single": [40000, 95000, 0], "mfj": [80000, 190000, 0], "hoh": [60000, 142500, 0], "mfs": [40000, 95000, 0]},
  exemption={"personal": 0, "dependent": 4930},
  local="No local income taxes.", salesTax=6,
  notes="H. 4216 (Act 110, signed March 2026) replaced the 0%/3%/6% schedule with two rates — 1.99% up to $30,000 and 5.21% above — retroactive to January 1, 2026. South Carolina now starts from federal AGI and allows its own income-adjusted deduction ($15,000 single, $22,500 head of household, $30,000 joint) that phases out as income rises.",
  source="https://dor.sc.gov/news/information-about-h-4216")

S["SD"] = none("South Dakota", "south-dakota", 4.2, "South Dakota has no personal or corporate income tax. The state sales tax rate is 4.2% (temporarily reduced from 4.5% through mid-2027), plus municipal sales taxes.", "https://dor.sd.gov/")

S["TN"] = none("Tennessee", "tennessee", 7, "Tennessee taxes no wages or salaries, and its Hall tax on interest and dividends was fully repealed in 2021. Its 7% state sales tax plus local rates gives it one of the highest combined sales tax rates in the country.", "https://www.tn.gov/revenue.html")

S["TX"] = none("Texas", "texas", 6.25, "Texas has no personal income tax, and the state constitution requires voter approval to create one. The state relies on a 6.25% sales tax (up to 8.25% with local taxes), the franchise (margin) tax on businesses and relatively high local property taxes.", "https://comptroller.texas.gov/taxes/")

S["UT"] = dict(name="Utah", slug="utah", type="flat", year=2026, base="federal_agi",
  brackets=flat(.0445), std={"single": 0, "mfj": 0}, exemption={"personal": 0, "dependent": 0}, special="ut",
  utCredit={"rate": .06, "fedStd": dict(FED), "depExemption": 2111, "phaseRate": .013, "phaseStart": {"single": 18213, "mfj": 36426, "hoh": 27320, "mfs": 18213}},
  local="No local income taxes.", salesTax=4.85,
  notes="SB 60 (2026) cut Utah’s flat rate from 4.5% to 4.45%, retroactive to January 1, 2026. Instead of a standard deduction, Utah gives a taxpayer credit of 6% of the federal standard deduction plus $2,111 per dependent, phased out at 1.3% of income above about $18,213 ($36,426 joint).",
  source="https://tax.utah.gov/income")

S["VT"] = dict(name="Vermont", slug="vermont", type="progressive", year=2025, base="federal_agi",
  brackets={"single": [[49400, .0335], [119700, .066], [249700, .076], [N, .0875]], "mfj": [[82500, .0335], [199450, .066], [304000, .076], [N, .0875]],
            "hoh": [[66200, .0335], [170550, .066], [276200, .076], [N, .0875]]},
  std={"single": 7650, "mfj": 15300, "hoh": 11450}, exemption={"personal": 5300, "dependent": 5300}, special="vt",
  local="No local income taxes.", salesTax=6,
  notes="Vermont’s four rates run from 3.35% to 8.75%. Taxpayers with federal AGI over $150,000 pay the greater of the regular tax or 3% of AGI. Brackets and deductions are the latest published (2025) amounts.",
  source="https://tax.vermont.gov/individuals/personal-income-tax")

S["VA"] = dict(name="Virginia", slug="virginia", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[3000, .02], [5000, .03], [17000, .05], [N, .0575]]},
  std={"single": 8750, "mfj": 17500, "hoh": 8750}, exemption={"personal": 930, "dependent": 930},
  local="No local income taxes.", salesTax=5.3,
  notes="Virginia’s top 5.75% rate starts at just $17,000 of taxable income for every filing status, so most workers effectively pay close to 5.75% on the margin. The standard deduction is $8,750 ($17,500 joint). Sales tax is 5.3% statewide (4.3% state plus 1% local), higher in some regions.",
  source="https://www.tax.virginia.gov/individual-income-tax")

S["WA"] = none("Washington", "washington", 6.5, "Washington has no tax on wages or salaries. It does tax long-term capital gains: 7% on gains above a standard deduction of about $278,000, plus an extra 2.9% (9% total) on gains over $1 million starting in 2025. Wages are subject to the WA Cares long-term-care premium (0.58%) and paid-leave premiums.", "https://dor.wa.gov/taxes-rates/other-taxes/capital-gains-tax",
  local="No local income taxes (Seattle’s 2017 income tax was struck down).")

S["WV"] = dict(name="West Virginia", slug="west-virginia", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[10000, .0211], [25000, .0281], [40000, .0316], [60000, .0422], [N, .0458]],
            "mfs": [[5000, .0211], [12500, .0281], [20000, .0316], [30000, .0422], [N, .0458]]},
  std={"single": 0, "mfj": 0}, exemption={"personal": 2000, "dependent": 2000},
  local="No local income taxes (some cities such as Charleston and Huntington charge flat weekly user fees on people who work there).", salesTax=6,
  notes="SB 392 cut every West Virginia rate by 5% retroactive to January 1, 2026; the top rate is now 4.58% (from 4.82%). The same brackets apply to single and joint filers, which creates a marriage penalty. Social Security benefits are fully exempt starting in 2026.",
  source="https://tax.wv.gov/Individuals/Pages/PersonalIncomeTaxReductionBill.aspx")

S["WI"] = dict(name="Wisconsin", slug="wisconsin", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[15110, .035], [51950, .044], [332720, .053], [N, .0765]], "mfj": [[20150, .035], [69260, .044], [443630, .053], [N, .0765]], "hoh": "single"},
  std={"single": 13960, "mfj": 25840, "hoh": 13960}, stdPhase={"single": [20119, 136453, 0], "mfj": [29039, 159690, 0], "hoh": [20119, 136453, 0]},
  exemption={"personal": 700, "dependent": 700},
  local="No local income taxes.", salesTax=5,
  notes="Wisconsin’s sliding-scale standard deduction is largest at low incomes and phases out completely by about $136,000 ($160,000 joint). Rates run from 3.5% to 7.65%. Head-of-household filers use the single schedule in this estimate.",
  source="https://www.revenue.wi.gov/Pages/Individuals/home.aspx")

S["WY"] = none("Wyoming", "wyoming", 4, "Wyoming has no personal or corporate income tax. Mineral severance taxes and a 4% state sales tax (plus local option taxes) fund most state spending.", "https://revenue.wyo.gov/")

S["DC"] = dict(name="District of Columbia", slug="district-of-columbia", type="progressive", year=2026, base="federal_agi",
  brackets={"single": [[10000, .04], [40000, .06], [60000, .065], [250000, .085], [500000, .0925], [1000000, .0975], [N, .1075]]},
  std=dict(FED), exemption={"personal": 0, "dependent": 0},
  local="DC is a single taxing jurisdiction — there is no separate city or county income tax. Non-residents who work in DC do not pay DC income tax.", salesTax=6,
  notes="DC uses the same seven brackets for all filing statuses, from 4% to 10.75% on income over $1 million, and matches the federal standard deduction. The general sales tax is 6%, scheduled to rise to 7% in October 2027.",
  source="https://otr.dc.gov/page/individual-income-tax-forms-and-instructions")

NEIGHBORS = {
 "AL": "FL GA MS TN", "AK": "WA TX FL", "AZ": "CA NV UT NM CO", "AR": "MO TN MS LA TX OK", "CA": "OR NV AZ",
 "CO": "WY NE KS OK NM UT AZ", "CT": "NY MA RI", "DE": "MD PA NJ", "FL": "GA AL", "GA": "FL AL TN NC SC",
 "HI": "CA WA OR", "ID": "WA OR NV UT WY MT", "IL": "WI IA MO KY IN", "IN": "IL MI OH KY", "IA": "MN WI IL MO NE SD",
 "KS": "NE MO OK CO", "KY": "IL IN OH WV VA TN MO", "LA": "TX AR MS", "ME": "NH MA VT", "MD": "PA DE VA WV DC",
 "MA": "NH VT NY CT RI", "MI": "OH IN WI", "MN": "WI IA SD ND", "MS": "LA AR TN AL", "MO": "IA IL KY TN AR OK KS NE",
 "MT": "ID WY SD ND", "NE": "SD IA MO KS CO WY", "NV": "CA OR ID UT AZ", "NH": "ME VT MA", "NJ": "NY PA DE",
 "NM": "AZ UT CO OK TX", "NY": "VT MA CT NJ PA", "NC": "VA TN GA SC", "ND": "MN SD MT", "OH": "PA WV KY IN MI",
 "OK": "KS MO AR TX NM CO", "OR": "WA ID NV CA", "PA": "NY NJ DE MD WV OH", "RI": "MA CT", "SC": "NC GA",
 "SD": "ND MN IA NE WY MT", "TN": "KY VA NC GA AL MS AR MO", "TX": "NM OK AR LA", "UT": "ID WY CO NM AZ NV",
 "VT": "NH MA NY", "VA": "MD DC WV KY TN NC", "WA": "OR ID", "WV": "OH PA MD VA KY", "WI": "MN IA IL MI",
 "WY": "MT SD NE CO UT ID", "DC": "MD VA",
}
for c, n in NEIGHBORS.items():
    S[c]["neighbors"] = n.split()

assert len(S) == 51, len(S)
for c, s in S.items():
    assert c in NEIGHBORS
    for n in s["neighbors"]:
        assert n in S, (c, n)

order = sorted(S, key=lambda c: S[c]["name"])
out = {"updated": "2026-11-04",
       "compiledFrom": "Tax Foundation, State Individual Income Tax Rates and Brackets 2026 (as of Feb. 11, 2026), updated for 2026 legislation and checked against state revenue department publications.",
       "states": {c: S[c] for c in order}}
json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print("wrote", len(S))
