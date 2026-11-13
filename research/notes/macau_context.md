# T07 — Macau context and regulation brief

Status labels as in the spec. Accessed 2026-11-13. Legal texts were **not** read in the original
(Chinese/Portuguese gazette); legal points are `[SECONDARY ✔]` from law-firm guides and trade press
and must be confirmed with counsel before any operational use.

## 1. Gaming tax (drives the break-even multiple, §8.3)

| Item | Finding | Label | Source |
|---|---|---|---|
| Special gaming tax | 35% of GGR | `[SECONDARY ✔]` (multiple outlets agree) | [GGRAsia 2022](https://www.ggrasia.com/macau-40pct-ggr-tax-in-new-law-ce-can-cut-up-to-5-points/), [AGBrief 2022](https://agbrief.com/intelligence/16/06/2022/macau-1-percentage-point-gaming-tax-hike-last-minute-sting-in-the-tail-for-operators/) |
| Levies | Amended law made the 2% (Macao Foundation) and 3% (urban development, tourism, social security) levies fixed rather than "up to", so the total is ~40% of GGR (previously ~39%) | `[SECONDARY ✔]` — trade press only; statute not read (deliverables tag it `[U PR-TAX-2022]`) | [ASGAM 2022](https://asgam.com/2022/06/16/macau-concessionaires-facing-1-effective-ggr-tax-hike-under-new-gaming-law/) |
| Reductions | The Chief Executive may reduce the burden by up to 5 points, e.g. for GGR from foreign players | `[SECONDARY ✔]` | [Macau Business](https://www.macaubusiness.com/gaming-tax-rebates-on-foreign-bets-rise-in-2024-govt/) |
| Tax treatment of promotional / free play | **Not verified.** Whether promotional chips reduce taxable GGR determines whether reinvestment is "pre-tax" or "post-tax" money | `[TO-VERIFY]` | — |

**Model choice**: base τ = 0.40; sensitivity τ ∈ {0.35, 0.40} (economics.json) and the 0.35–0.40 grid in F6. Promotional-cost tax treatment
is run as a scenario switch (`promo_reduces_taxable_ggr` = False/True).

## 2. Market structure events that confound 2025–2026 comparisons

| Event | Timing | Why it matters | Label | Source |
|---|---|---|---|---|
| Satellite casino closures (SJM-operated, 8 of 9 closed; L'Arc converted) | Final closures 30–31 Dec 2025 | 2025 satellite GGR ≈ HK$9.77bn (~US$1.25bn) up for grabs in 2026; SJM share 13.1% (2024) → 11.9% (2025). All six concessionaires competed for it, partly via lower minimum bets | `[SECONDARY ✔]` | [focusgn](https://focusgn.com/asia-pacific/sjm-posts-2025-loss-as-satellite-casino-closures-impact-results), [Macau Daily Times](https://macaudailytimes.com.mo/casinos-slash-mass-bets-to-capture-business-from-closed-satellite-venues.html), [AGBrief](https://agbrief.com/news/macau/10/03/2026/sjm-faces-perfect-storm-as-satellite-closures-and-costs-hit-results-clsa/) |
| Londoner Grand room inventory return | Fully available from ~May–Jun 2025 (management commentary) | Coincides with the 2Q25 reinvestment push; raises Londoner revenue and opex | `[SECONDARY ✔]` | Q2 2025 call transcript |
| Venetian renovation | ~500 rooms out of service on average through 4Q27 | Venetian room revenue down y/y in 3Q26 | `[PRIMARY ✔]` | LVS-ER-2026-10-21, Venetian table footnote |
| Rolling-play hold | 2Q26 hold unusually low (+US$87m hold-adjusted) | Single-quarter margin distortion; use hold-adjusted series | `[PRIMARY ✔]` | LVS-ER-2026-07-22 |

## 3. Regulation relevant to customer analytics and reinvestment tests

| Rule | Relevance | Label | Source |
|---|---|---|---|
| Gaming law amendments and 10-year concessions from 2023 (Law 16/2022) | Non-gaming investment commitments; government preference for diversification over "pure gaming" promotion | `[TO-VERIFY]` (law number) | Chambers Gaming Law 2025 guide |
| Law 7/2024 — gaming credit regime (effective 1 Aug 2024) | Credit only by concessionaires; affects premium-segment reinvestment levers (credit is not an available "promotion" tool for third parties) | `[SECONDARY ✔]` | [Chambers 2024](https://practiceguides.chambers.com/practice-guides/gaming-law-2024/macau-sar-china) |
| Law 20/2024 — illegal gambling (enacted 28 Oct 2024) | Rules out informal agent-driven incentives; reinforces compliance review of any offer channel | `[SECONDARY ✔]` | [GGRAsia](https://www.GGRAsia.com/?p=157179), Chambers 2025 |
| Personal Data Protection Act (Law 8/2005); regulator = Personal Data Protection Bureau from 1 Feb 2024 | Processing needs a legal basis (unambiguous consent or statutory ground). Transfers outside Macau only to adequate jurisdictions, with consent, or with notification/authorisation. Customer-level analysis should be done **in Macau** on pseudonymised data; only aggregates should leave | `[SECONDARY ✔]` | [DLA Piper](https://www.dlapiperdataprotection.com/?c=MO&t=law), [IFLR](https://www.iflr.com/article/2gp8mhgk8fgpqy2c0asqo/sponsored/cross-border-data-transfers-essential-compliance-steps-for-multinational-corporations-in-macau), [FPF](https://fpf.org/blog/new-report-on-limits-of-consent-in-macaus-data-protection-law) |
| Responsible gambling (DICJ guidelines) | Randomised offer tests must exclude self-excluded and at-risk-flagged players and must never *increase* incentives to them | `[TO-VERIFY]` specific instrument | DICJ site (RG section) |

Correction to spec v1.0: §6.2 cited "Law 7/2024 on illegal gambling". Law 7/2024 is the credit
regime; illegal gambling is Law 20/2024. The spec has been corrected.

## 4. Market data facts used downstream (all `[PRIMARY ✔]` from DICJ XML)

- 2025 games-of-fortune GGR: MOP247,404m (DICJ-Q-2026 report 1).
- 3Q26 games-of-fortune GGR: MOP60,215m; VIP baccarat MOP16,906m; mass baccarat MOP33,612m.
- Mass (all games ex-VIP baccarat) ≈ US$5.39bn in 3Q26 at MOP 8.034/US$.

## 5. Mapping to transfer filters (spec §9.3)

| Filter | Constraint established here |
|---|---|
| 1 Game mix | Mass baccarat ≈ 56% of 3Q26 GGR; slots ≈ 7% (MOP4,091m/60,215m) → slot-based US evidence transfers weakly |
| 4 Privacy | In-Macau processing, pseudonymisation, aggregate-only transfer to the US parent |
| 5 Regulation | RG exclusion rules; no third-party credit; compliance review of offers |
| 6 Concession | Non-gaming commitments favour reinvestment that shifts value into non-gaming spend |
| 7 Competition | 2026 satellite-closure scramble means all operators were raising mass incentives at once |
