# Texas Public Adjuster Compliance Research — SmokeDamage.com

Prepared: 2026-09-28. All sources below were fetched on **2026-09-28** unless noted.
Every legal statement here is tied to a verbatim quote from an official source.
If something is not in this file, do not state it on the site.

Primary sources used:

| Source | URL | Notes |
|---|---|---|
| Texas Insurance Code ch. 4102 (Texas Legislature, Texas Constitution and Statutes) | https://statutes.capitol.texas.gov/Docs/IN/htm/IN.4102.htm | The public URL renders via JavaScript; the same official text was retrieved from the Legislature's resource server at https://tcss.legis.texas.gov/resources/IN/htm/IN.4102.htm |
| 28 TAC Chapter 19, Subchapter J (§§19.701–19.713) | https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-701 (and -702 … -713) | Cornell LII reproduces the official Texas Administrative Code text with Texas Register history notes. The Texas SOS TAC viewer (linked from TDI) is a JavaScript app and was not scraped. |
| TDI consumer tip: "Public adjusters: What to know before you hire one to help with your claim" | https://www.tdi.texas.gov/tips/public-adjusters.html | Page shows "Last updated: 3/25/2025" |
| TDI FIN535 Public Insurance Adjuster Contract (form version FIN535 \| 0824) | https://www.tdi.texas.gov/forms/finagentlicense/FIN535.pdf | TDI-prescribed standard contract |
| TDI licensee lookup (official) | https://appscenter.tdi.texas.gov/reports/p/sirconReport | Queried its JSON endpoints by license number |
| TDI open data: "Insurance agencies and businesses approved to manage insurance-related products" (dataset 3yqc-fcdt) | https://data.texas.gov/dataset/3yqc-fcdt | Attribution: Texas Department of Insurance; data updated 2026-09-28 |

---

## LICENSE VERIFICATION RESULT

**Status: VERIFIED** against two official TDI sources on 2026-09-28.

### Source 1 — TDI licensee lookup (appscenter.tdi.texas.gov, "Look up Texas-licensed insurance agents, adjusters, businesses")

Queried `searchReportFirmInfoByLicNo`, `searchFirmLicenseInfoByLicNo`, `searchFirmAddressInfoByLicNo`, `searchFirmAddressHistoryInfoByLicNo`, `searchFirmAliasesInfoByLicNo`, `searchFirmIndvAssnInfoByLicNo`, `searchFirmBondsInfoByLicNo` with license number 3356839.

| Field | Value on TDI record |
|---|---|
| Licensed name | **RISE PUBLIC ADJUSTING LLC** |
| License number | **3356839** |
| License type | **Public Insurance Adjuster** |
| Status | **Active** (status date 07-02-2025) |
| Original issue date | 07-02-2025 |
| Expiration date | **07-02-2027** |
| Resident | Yes (resident state: Texas) |
| NPN | 21642765 |
| **Mailing address** (effective 07-02-2025) | **2140 E SOUTHLAKE BLVD STE L, SOUTHLAKE, TX 76092-6537** |
| **Business location address** (effective 01-28-2026) | **5514 IMOGEN DR., BELTON, TX 76513** |
| Prior business location (07-02-2025 to 01-28-2026) | 2140 E SOUTHLAKE BLVD STE L302, SOUTHLAKE, TX 76092 |
| Phone on record | 832-503-5866 (fax 254-346-2782) |
| Assumed names / aliases on record | **None** (empty result) |
| Designated responsible licensed person | DITTMAN, JOSEPH RAY (association begin 07-02-2025) |
| Bond on record | Surety bond, Texas Bonding Company, $10,000, effective 06-30-2025, no termination date |
| Problem reports | None returned |

Related individual record (same lookup, license 3341461): **DITTMAN, JOSEPH RAY**, license type Public Insurance Adjuster, status **Active**, issued 05-29-2025, expires **05-31-2028**, resident Texas.

### Source 2 — TDI open dataset on data.texas.gov (3yqc-fcdt)

Query `agency_license_number=3356839` returned:
`org_name: RISE PUBLIC ADJUSTING LLC; agency_type: Limited Liability Company; license_type: Public Insurance Adjuster; license_issue_date: 2025-07-02; expiration_date: 2027-07-02; city: SOUTHLAKE; state: TX; pstl_cd: 760926537`.
(This dataset shows city/ZIP only, not street address, and has no status column. It matches the mailing address city/ZIP.)

### Not reached / not used
- https://apps.tdi.state.tx.us/pcci/pcci_search.jsp — blocked by the network proxy (CONNECT 502).
- https://www.tdi.texas.gov/agent/agentlookup.html — returned 404.
- No secondary (non-government) sources were used for license facts.

### Issues the owner must resolve before launch
1. **Which address to display.** TDI shows two current addresses: a mailing address in Southlake and a business-location address in Belton (updated 01-28-2026). §4102.113 requires "address … as they appear in the records of the commissioner" but does not say which address type. §4102.106(b) says "The address of the place of business must appear on the face of the license," which points to the **business location** address. Confirm with TDI or counsel, and confirm the Belton address is current and correct before publishing it. Do not publish an address that is not on the TDI record.
2. **Brand name "Smoke Damage Public Adjuster".** TDI shows **no alias/assumed name** on the firm record. §4102.162 prohibits using a name other than the licensed name in an advertisement "unless the name is used under a valid assumed name certificate as provided by Chapter 71, Business & Commerce Code." The owner should confirm an assumed name certificate exists for "Smoke Damage Public Adjuster" (and consider adding it to the TDI record). Until confirmed, every page should clearly show the licensed name "Rise Public Adjusting LLC" next to the brand.
3. The phone on the TDI record (832-503-5866) differs from the site phone (+1 844-537-1427). Phone is not listed in the §4102.113 advertising requirement, but the owner may want TDI records updated.

---

## ADVERTISING REQUIREMENTS FOR THE WEBSITE

### The rule
**Texas Insurance Code §4102.113 (ADVERTISEMENTS):**
> "Each advertisement by a license holder soliciting or advertising business must display the license holder's name, address, and license number as they appear in the records of the commissioner."

**28 TAC §19.712(a)(1)** — websites are advertisements:
> "As used in Insurance Code Chapter 4102, concerning Public Insurance Adjusters, "advertisement" includes: (1) printed and published material, audiovisual material and descriptive literature of a public insurance adjuster used in direct mail, newspapers, magazines, radio, telephone and television scripts, websites, billboards, and similar displays;"

§19.712(a)(6)–(7) also cover lead-generation forms ("lead card solicitations") and "any other communication directly or indirectly related to a public insurance adjuster contract, and intended to result in the eventual execution of such a contract."

### What must be displayed on SmokeDamage.com (every page that solicits or advertises business — practically, the site-wide footer, and any landing page/ad)
1. **Licensed name exactly as on TDI record:** `Rise Public Adjusting LLC` (TDI shows "RISE PUBLIC ADJUSTING LLC").
2. **License number exactly as on TDI record:** `3356839` (e.g., "Texas Department of Insurance Public Insurance Adjuster License #3356839").
3. **Address exactly as on TDI record** — one of the addresses in the verification table above (see Issue 1; the business-location address is the likelier match to "place of business"). Owner must confirm which.

### Related advertising rules
- **§4102.162 (USE OF DIFFERENT NAME PROHIBITED):** "A license holder may not use a name different from the name under which the license holder is currently licensed in an advertisement, solicitation, or contract for business unless the name is used under a valid assumed name certificate as provided by Chapter 71, Business & Commerce Code." → See Issue 2.
- **§4102.161 (CERTAIN REPRESENTATIONS PROHIBITED):** "A license holder may not use any letterhead, advertisement, or other printed matter, or use any other means, to represent that the license holder is an instrumentality of the federal government, of a state, or of a political subdivision of a state." → Don't use TDI/state seals or imply government affiliation.
- **§4102.159 (MISREPRESENTATION PROHIBITED):** "A license holder may not use any misrepresentation to solicit a contract or agreement to adjust a claim."
- **§4102.155 (CERTAIN DELEGATION PROHIBITED):** "A license holder may not permit an employee or agent, in the employee's or agent's own name, to advertise, solicit or engage clients … or in any manner conduct business for which a license is required under this chapter."
- **28 TAC §19.713(b)(9):** "Licensees must not disseminate or use any form of agreement, advertising, or other communication, regardless of format or medium, in this state that is harmful to the profession of public insurance adjusting and that does not comply with Insurance Code Chapter 4102, this subchapter, or other provisions of the Insurance Code."
- **§4102.160(2)** bars paying non-licensees for referrals (relevant to any paid lead/referral arrangements).

---

## 1. License requirement and who public adjusters represent

**Plain English:** In Texas you must hold a TDI license to act as, or hold yourself out as, a public insurance adjuster. A public adjuster works for the insured (the policyholder) on property claims — not for the insurance company — and only when the client is an insured under the policy.

- **§4102.051(a):** "A person may not act as a public insurance adjuster in this state or hold himself or herself out to be a public insurance adjuster in this state unless the person holds a license issued by the commissioner under Section 4102.053 or 4102.054."
- **§4102.001(3)(A)(i)** (definition): a person who, for compensation, "acts on behalf of an insured in negotiating for or effecting the settlement of a claim or claims for loss or damage under any policy of insurance covering real or personal property".
- **§4102.101(a):** "A license issued under this chapter authorizes the adjusting of claims on behalf of insureds for fire and allied coverages, burglary, flood, and all other property claims, both real and personal, including loss of income, but only when the client is an insured under the insurance policy."
- **§4102.157:** a license holder may not act "on a bodily injury loss covered by a life, health, or accident insurance policy or on any claim for which the client is not an insured under the insurance policy."
- **§4102.158(c):** "A license holder may not represent an insured on a claim or charge a fee to an insured while representing the insurance carrier against which the claim is made."
- **28 TAC §19.704(c)(3)** (business entities): "at least one officer of the corporation or one active partner of the partnership and all other persons performing any acts of a public insurance adjuster on behalf of the corporation or partnership in this state are individually licensed by the department".
- **§4102.207(a) (unlicensed adjusters):** "Any contract for services regulated by this chapter that is entered into by an insured with a person who is in violation of Section 4102.051 may be voided at the option of the insured." (b): "the insured is not liable for the payment of any past services rendered, or future services to be rendered, by the violating person under that contract or otherwise."
- **§4102.108:** "A license issued under this chapter must at all times be posted in a conspicuous place in the principal place of business of the license holder."
- **Financial responsibility — 28 TAC §19.705:** "Each public insurance adjuster, as a condition for being licensed, must maintain proof of financial responsibility by obtaining a surety bond in the principal sum of not less than $10,000 …" (§19.707(3): the bond is "payable to the Texas Department of Insurance for the use and benefit of an insured, conditioned that the public insurance adjuster shall pay any final judgment recovered against it by an insured").
- **TDI consumer guidance:** "You can hire a public insurance adjuster to negotiate with your insurance company to settle your claim. Public insurance adjusters understand the claims process and are licensed by TDI." To check a license, complaints, and disciplinary actions: "Call our Help Line at 800-252-3439".

Sources: https://statutes.capitol.texas.gov/Docs/IN/htm/IN.4102.htm ; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-704 ; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-705 ; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-707 ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 2. Contract requirements (TDI-approved / prescribed form)

**Plain English:** A public adjuster must have a signed written contract before doing any work, and it must be either TDI's standard contract (FIN535) or a contract TDI approved before use. The contract must include specific notices, contact information, the fee method, and a date and time of signing.

- **§4102.103(a):** "A license holder may not, directly or indirectly, act within this state as a public insurance adjuster without having first entered into a contract, in writing, on a form approved by the commissioner, executed in duplicate by the license holder and the insured or the insured's duly authorized representative. A license holder may not use any form of contract that is not approved by the commissioner."
- **§4102.103(b):** the contract "must include a prominently displayed notice in 12-point boldface type that states "WE REPRESENT THE INSURED ONLY.""
- **§4102.103(d):** "A license holder may not enter into a contract with an insured and collect a commission … without the intent to actually perform the services customarily provided by a licensed public insurance adjuster for the insured."
- **28 TAC §19.708(d):** "All public insurance adjusters in Texas must use a written contract that is in the form prescribed by the department … Public insurance adjusters must select from the following contract form options: (1) a standard language contract developed by the department, identified by FIN 535; or (2) a contract filed and approved by the department before use."
- **§19.708(b)** required contents include (quoted in part): "(1) the name, address, and license number of the public insurance adjuster … with each page of the contract prominently displaying the license number(s); (2) the public insurance adjuster's telephone and fax number …; (3) the mailing and physical addresses to which notice of cancellation and all communications … may be delivered; (4) if any part of the contract or solicitation is made via the Internet, the email and website address …; (5) the date and time the contract was signed".
- **§19.708(b)(7)** three statements in 12-point bold on the signature page: "(A) "NOTICE: The insured may cancel this contract by written notice to the public insurance adjuster within 72 hours of signature for any reason."; (B) "We represent the insured only."; and (C) "You are entering into a service contract. You are being charged a fee for this service. You do not have to enter into this contract to make a claim for loss or damage on a policy of insurance.""
- **§19.708(b)(10)** English and Spanish notice on page 1 or 2 with TDI's number: "IMPORTANT NOTICE: You may contact the Texas Department of Insurance to get information about public insurance adjusters, your rights as a consumer, or information about how to file a complaint by calling 1-800-252-3439; or you may write the Texas Department of Insurance, at MC: CO-CP, P.O. Box 12030, Austin, Texas 78711-2030."
- **§19.708(b)(13)** "a clear and prominent statement of the public insurance adjuster's commission including: (A) the method of calculating the commission …; (B) a general description of services …; (C) a description of the claim and property damage, location, and event date".
- **§19.708(c):** "The contract must not contain any terms or conditions that have the effect of limiting or nullifying any requirements of the Insurance Code, this subchapter, or other rules of the department."
- **FIN535** states: "This contract form (FIN535 - Public Insurance Adjuster Contract) is prescribed by the Texas Department of Insurance … and must not be edited or modified."
- **TDI consumer guidance:** "Ask the public insurance adjuster how much they charge. You can try to negotiate a lower fee." and "See a sample contract (PDF)" (links FIN535).

Sources: statute URL above; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-708 ; https://www.tdi.texas.gov/forms/finagentlicense/FIN535.pdf ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 3. Compensation limits (10% cap)

**Plain English:** A Texas public adjuster's total fee can't be more than 10% of the insurance settlement on the claim, and under TDI's rule that 10% includes the adjuster's expenses and costs. Fees can be hourly, flat, a percentage, or another method. If the insurer pays (or commits in writing to pay) policy limits within 72 hours after the loss is reported, the adjuster can't take a percentage fee — only reasonable compensation for time and expenses. TDI notes the fee can be based on the whole settlement, not just the disputed amount, and a fee may still be owed if the offer doesn't go up.

- **§4102.104(a):** "a license holder may receive a commission for service provided under this chapter consisting of an hourly fee, a flat rate, a percentage of the total amount paid by an insurer to resolve a claim, or another method of compensation. The total commission received may not exceed 10 percent of the amount of the insurance settlement on the claim."
- **§4102.104(b):** "A license holder may not receive a commission consisting of a percentage of the total amount paid by an insurer to resolve a claim on a claim on which the insurer, not later than 72 hours after the date on which the loss is reported to the insurer, either pays or commits in writing to pay to the insured the policy limit of the insurance policy in accordance with Section 862.053. The license holder is entitled to reasonable compensation from the insured for services provided … based on the time spent on a claim that is subject to this subsection and expenses incurred by the license holder …"
- **28 TAC §19.701(b)(1)** (definition of Commission): "… not to exceed 10 percent of the amount of the insurance settlement on the claim, including expenses, direct costs, or any other costs accrued by the public insurance adjuster."
- **§19.708(b)(11):** contract must state "that under any method of compensation, the total commission payable to the public insurance adjuster, including expenses, direct costs, or any other costs accrued by the public insurance adjuster, must not exceed 10% of the amount of the insurance settlement".
- **§19.708(b)(12):** "if applicable, a statement disclosing how payments issued before the effective date of the contract will be used in determining compensation to the public insurance adjuster".
- **§4102.160(1):** a license holder may not "advance money to any potential client or insured".
- **TDI consumer guidance (verbatim):** "Public adjusters can charge up to 10% of the total amount the company will pay for your claim. The fee can be based on the total amount of the claim settlement, not just the amount you're disputing." / "For example: If the company wants to pay $100,000 for your claim and you're disputing $20,000, the public adjuster could charge $10,000." / "You can ask the public adjuster to put their fee in a dollar amount, instead of a percentage, in the contract." / "If your insurance company doesn't increase its offer after you hire the public adjuster, you might still have to pay the public adjuster. And you still have to pay your deductible."

Sources: statute URL; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-701 ; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-708 ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 4. No legal advice / not acting as an attorney

**Plain English:** A public adjuster can't practice law or give legal advice. They also can't solicit clients for a lawyer, sign someone up mainly to send them to a lawyer, or have a client sign a lawyer's representation agreement. They may recommend a particular attorney.

- **§4102.156:** "A license holder may not render services or perform acts that constitute the practice of law, including the giving of legal advice to any person in the license holder's capacity as a public insurance adjuster."
- **§4102.003:** "This chapter may not be construed as entitling a person who is not licensed by the Supreme Court of Texas to practice law in this state."
- **§4102.158(d):** "A license holder may not directly or indirectly solicit, as described by Chapter 38, Penal Code, employment for an attorney or enter into a contract with an insured for the primary purpose of referring an insured to an attorney and without the intent to actually perform the services customarily provided by a licensed public insurance adjuster. This section may not be construed to prohibit a license holder from recommending a particular attorney to an insured."
- **§4102.158(e):** "A license holder may not act on behalf of an attorney in having an insured sign an attorney representation agreement."
- **28 TAC §19.713(b)(7):** "Licensees must not engage in the unauthorized practice of law."
- **TDI:** public adjusters can't "Practice law or provide legal advice."

Sources: statute URL; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-713 ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 5. No participation in repair/reconstruction; conflicts of interest; referral fees

**Plain English:** A public adjuster can't take part, directly or indirectly, in rebuilding, repairing, or restoring the property on a claim they're adjusting, and can't have financial ties to or take money from salvage, repair, or construction firms that get business from that claim. They can't take referral fees from anyone (attorneys, appraisers, umpires, contractors, salvage companies), and can't pay non-licensees for referrals. Contractors, for their part, can't act as public adjusters or advertise to adjust claims on property they work on.

- **§4102.158(a):** "A license holder may not: (1) participate directly or indirectly in the reconstruction, repair, or restoration of damaged property that is the subject of a claim adjusted by the license holder; or (2) engage in any other activities that may reasonably be construed as presenting a conflict of interest, including soliciting or accepting any remuneration from, having a financial interest in, or deriving any direct or indirect financial benefit from, any salvage firm, repair firm, construction firm, or other firm that obtains business in connection with any claim the license holder has a contract or agreement to adjust."
- **§4102.158(b):** "A license holder may not, without the knowledge and consent of the insured in writing, acquire an interest in salvaged property that is the subject of a claim adjusted by the license holder."
- **§4102.163(a):** "A contractor may not act as a public adjuster or advertise to adjust claims for any property for which the contractor is providing or may provide contracting services, regardless of whether the contractor: (1) holds a license under this chapter; or (2) is authorized to act on behalf of the insured under a power of attorney or other agreement."
- **§4102.164(a):** "A licensed public insurance adjuster may not accept a fee, commission, or other valuable consideration of any nature, regardless of form or amount, in exchange for the referral by a licensed public insurance adjuster of an insured to any third-party individual or firm, including an attorney, appraiser, umpire, construction company, contractor, or salvage company."
- **§4102.160(2):** may not "pay, allow, or give, or offer to pay, allow, or give, directly or indirectly, to a person who is not a licensed public insurance adjuster a fee, commission, or other valuable consideration for the referral of an insured to the public insurance adjuster …"
- **28 TAC §19.708(b)(9)** requires this contract notice: "NOTICE: A public insurance adjuster may not participate directly or indirectly in the reconstruction, repair, or restoration of damaged property that is the subject of a claim adjusted by the public insurance adjuster or engage in any other activities that may reasonably be construed as presenting a conflict of interest …"
- **TDI:** "Under Texas law, public insurance adjusters who work on your claim can't act as your contractor. Likewise, contractors can't advertise that they'll handle your insurance claim." Also can't "Get referral fees from attorneys, contractors, or anyone else involved in your claim."

Sources: statute URL; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-708 ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 6. Right to cancel (72 hours)

**Plain English:** The insured can cancel a public adjuster contract for any reason by written notice within 72 hours of signing. TDI's form says notice goes by registered or certified mail (return receipt requested) to the address on the contract, or by personal service. TDI's consumer page says you can't get out of the contract after 72 hours. Separately, a contract with an unlicensed adjuster can be voided by the insured (§4102.207).

- **§4102.103(b):** "The contract must contain a provision allowing the client to rescind the contract by written notice to the license holder within 72 hours of signature".
- **28 TAC §19.708(b)(7)(A):** ""NOTICE: The insured may cancel this contract by written notice to the public insurance adjuster within 72 hours of signature for any reason.""
- **FIN535:** "At the option of the Insured, this contract may/must be voidable for 72 hours after signing. The Insured may void the contract by notifying the Public Insurance Adjuster in writing, by either registered or certified mail, return receipt requested, to the address shown on this contract or by personally serving notice on the Public Insurance Adjuster."
- **TDI consumer guidance:** "If you change your mind, you have 72 hours after you've signed a contract to cancel it. You can't get out of the contract after 72 hours."

Sources: statute URL; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-708 ; https://www.tdi.texas.gov/forms/finagentlicense/FIN535.pdf ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 7. Solicitation restrictions

**Plain English:** No soliciting during a natural disaster while it's still happening. Solicitation (in person, by phone, or otherwise) is only allowed 9 a.m.–9 p.m. Monday–Saturday and noon–9 p.m. Sunday — but an adjuster may take calls or visits the insured starts at any hour. No badges, no misrepresentation, no posing as a government body.

- **§4102.151 (SOLICITATION PROHIBITED DURING NATURAL DISASTER):** "A license holder may not solicit or attempt to solicit a client for employment during the progress of a loss-producing natural disaster occurrence."
- **§4102.152(a):** "A license holder may not solicit or attempt to solicit business on a loss or a claim in person, by telephone, or in any other manner at any time except between the hours of 9 a.m. and 9 p.m. on a weekday or a Saturday and between noon and 9 p.m. on a Sunday."
- **§4102.152(b):** "This section does not prohibit a license holder from accepting phone calls or personal visits during the prohibited hours from an insured on the insured's initiation."
- **§4102.154:** "A license holder may not use a badge in connection with the official activities of the license holder's business."
- **§4102.159:** "A license holder may not use any misrepresentation to solicit a contract or agreement to adjust a claim."
- **28 TAC §19.713(b)(2):** "Licensees must not employ any improper solicitation that would violate Insurance Code Chapter 4102 and applicable rules."
- **TDI:** public adjusters can't "Knock on your door asking for business during a natural disaster or after 9 p.m." and can't "Wear a badge while they're working as a public insurance adjuster."

Sources: statute URL; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-713 ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## 8. Claim funds, payments, and records (fiduciary duty)

**Plain English:** Claim money a public adjuster receives is held as a fiduciary and can't be diverted. Insurance payments must name the insured as a payee and require the insured's own signature/endorsement; the adjuster can't endorse checks for the insured even with authorization. The adjuster must keep detailed records of each claim (including fees and disbursements) in Texas for at least five years. No statute or rule found requiring a specific escrow/trust *account* by name — so don't claim one.

- **§4102.111(a):** "All funds received as claim proceeds by a license holder acting as a public insurance adjuster are received and held by the license holder in a fiduciary capacity. A license holder may not divert or appropriate fiduciary funds received or held."
- **§4102.104(c):** "Except for the payment of a commission by the insured, all persons paying any proceeds of a policy of insurance or making any payment affecting an insured's rights under a policy of insurance must: (1) include the insured as a payee on the payment draft or check; and (2) require the written signature and endorsement of the insured on the payment draft or check."
- **§4102.104(e):** "Notwithstanding any authorization the insured may have given to a public insurance adjuster, a public insurance adjuster may not sign and endorse any payment draft or check on behalf of an insured."
- **§4102.110(a)** records must include, among others, "(6) the total compensation received for the adjustment; and (7) an itemized statement of disbursements made by the license holder from recoveries received on behalf of the insured." **(b)** kept "in this state for at least five years after the termination of a transaction with the insured".
- **§4102.153 (confidentiality):** "A license holder may not knowingly make any false report to the license holder's employer or client and may not divulge to any other person, except as the law may require, any information obtained except at the direction of the employer or the client for whom the information is obtained."

Source: statute URL — accessed 2026-09-28.

## 9. Other consumer-facing points

- **Ethics (28 TAC §19.713(b)):** "(1) Licensees must conduct business fairly with their clients, insurance companies, and the public." … "(6) Licensees must have appropriate knowledge and experience for the work they undertake and should obtain competent technical assistance, when necessary, to help handle claims and losses outside their area of expertise."
- **TDI:** public adjusters can't "Keep you from talking with your insurance company."
- **TDI:** "Hiring a public adjuster is one of your options if your homeowners claim is denied or you think your insurance company should pay more for repairs."
- **TDI (complaints):** "To report a public adjuster, call the Texas Department of Insurance at 800-252-3439 or file a complaint." and "If you're having issues with your public insurance adjuster, you have the right to sue."
- **TDI (questions to ask before signing):** "Will you inspect my damaged property? Will you talk to my insurance company and ask for a larger amount? How long will it take you to settle my claim?"
- **Exemption from license:** §4102.051(b) — no PA license required for a Texas-licensed attorney who has complied with §4102.053(a)(6), or a licensed P&C agent "while acting for an insured concerning a loss under a policy issued by that agent."
- **Technical experts:** §4102.002(6) exempts "a photographer, estimator, appraiser, engineer, or arbitrator employed by a public insurance adjuster exclusively for the purpose of furnishing technical assistance to the licensed public insurance adjuster".

Sources: statute URL; https://www.law.cornell.edu/regulations/texas/28-Tex-Admin-Code-SS-19-713 ; https://www.tdi.texas.gov/tips/public-adjusters.html — accessed 2026-09-28.

## Not verified / do not state
- Any specific claim-filing deadlines, statute-of-limitations periods, or prompt-payment deadlines (not researched here).
- Any escrow/trust-account requirement beyond the §4102.111 fiduciary duty.
- Continuing-education hours, exam details, license fees.
- Anything about whether TDI has approved a custom Rise Public Adjusting contract (unknown; the firm may use FIN535).
