# T14–T15 — Transferring external evidence to Sands China

Evidence grades and case IDs refer to `sources/case_register.csv`. Sands facts are `[PRIMARY ✔]`
(LVS releases, DICJ) unless labelled. Economic values are `[ILLUSTRATIVE]` unless labelled `[DERIVED]`.

## T4 — Reasoning chains

### Chain 1 — Control-group offer testing (C01, E3; methodological support C02–C05, E2)

| Link | Content |
|---|---|
| External problem | Harrah's could not tell which offers changed customer behaviour |
| Method | Hypothesis → offer to segment → compare with a control group that did not get the offer |
| Decision changed | Offer value and design by segment |
| Outcome | Company-reported gains (E3); no independent effect size |
| Sands problem | Since 2Q25, more of gross win is not booked as casino revenue: the net-to-gross gap rose from 20.5% (3Q23–1Q25 mean) to 23.5% (2Q25–3Q26 mean), ≈ US$226m/yr `[DERIVED]`. Mass-share index +4.5 pts by 3Q26 `[DERIVED]` |
| Macau adaptation | Customer-level randomisation done inside Macau on pseudonymised IDs (PDPA); exclude RG-flagged players; host-managed premium players are handled by case review, not randomised |
| Proposed Sands decision | A standing 5–10% randomised holdout in each mass tier at every property, with the offer level as the treatment |
| Mechanism | Measures incremental theo per $ of reinvestment, cell by cell |
| Validation | Spec §8.6; pipeline in `analysis/holdout_analysis.py` (synthetic demo: 91% CI coverage) |
| Verdict | **Transferable with adaptation** |

### Chain 2 — Right-sizing free play for established players (C02–C05, E2)

| Link | Content |
|---|---|
| External problem | Large FP budgets with unclear incrementality |
| Method | Compare play and visitation across groups whose FP was cut, kept or removed |
| Decision changed | FP reduced for groups insensitive to it |
| Outcome | Little response to FP reductions; ~20% visitation loss only when FP was eliminated (C02) |
| Sands problem | The post-2Q25 increase may include FP to players who would have visited anyway |
| Macau adaptation | Evidence is from US slot players; Macau mass is baccarat-led (mass baccarat ≈ 56% of 3Q26 GGR `[PRIMARY ✔]`) and visits are travel-constrained. **Effect sizes do not transfer**; the hypothesis and test design do |
| Proposed Sands decision | Test a –30% offer arm for established rated-mass players (largest pool share) |
| Mechanism | Saves reinvestment cost if theo loss < saving/(1 − τ − v) |
| Validation | Holdout; guardrails on visits and share |
| Verdict | **Hypothesis to test**, not a result |

### Chain 3 — Total-guest-value room allocation (C07, E3)

| Link | Content |
|---|---|
| External problem | Rooms given to casino guests displaced cash guests |
| Method | Revenue management pricing rooms by expected total guest value (room + gaming) |
| Decision changed | Room availability and price by customer value |
| Outcome | Chain-wide ~15% revenue improvement reported (vs 3–7% typical RM) — practitioner/vendor co-authored |
| Sands problem | Hotels ran near full: 2Q25–3Q26 mean occupancy Venetian 98.5%, Parisian 98.3%, Sands Macao 99.1%, Londoner 96.6%, Plaza/Four Seasons 94.4% `[PRIMARY ✔]` |
| Macau adaptation | Room comps are a core mass-reinvestment currency; total-value logic applies directly, but weekday/weekend and holiday patterns are Macau-specific |
| Proposed Sands decision | On forecast sell-out nights, swap room comps for non-room rewards for players below a theo threshold |
| Mechanism | Comp room opportunity cost ≈ US$94–211/night under illustrative P(sellout) `[ILLUSTRATIVE]` vs ≈ US$40 when not full |
| Validation | Randomise reward type on forecast high-occupancy nights; measure displaced cash revenue and gaming response |
| Verdict | **Transferable with adaptation** (strongest operational fit) |

### Chain 4 — Reactivation of lapsed / new players (C10, E4)

| Link | Content |
|---|---|
| External problem | Promotional spend concentrated on existing players |
| Method | Vendor player-valuation model |
| Outcome | Vendor claims: -18% promo expense, 75% reactivation (no counterfactual) |
| Sands problem | 2026 satellite closures put ~US$1.25bn of 2025 GGR up for grabs `[SECONDARY ✔]` — many new-to-Sands mass players |
| Proposed Sands decision | Shift part of the reinvestment increment from established to new/lapsed cells |
| Verdict | **Hypothesis to test** (evidence weak, E4) — include only as a test arm |

### Chain 5 — Demand-based labour scheduling (C12–C13, E4)

| Link | Content |
|---|---|
| Outcome | No quantified independent results found |
| Macau adaptation | Labour import quotas and local-employment rules limit flexing |
| Verdict | **Not prioritised**: weak evidence, and Sands' 3Q26 commentary frames higher service spend as deliberate investment ("enhanced service and hospitality offerings") `[PRIMARY ✔]` |

### Chain 6 — Real-time ML bonus personalisation (C11, E4)

| Verdict | **Not transferable**: online setting (illegal in Macau); vendor claim only |
|---|---|

## T5 — Decision matrix

| Approach | External evidence (grade) | Sands property / segment | Decision owner | Required data | Business KPI | Financial mechanism | Complexity | Key risks & constraints | Public-data feasibility | Measurable incremental value | Transferable? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Control-group offer testing | C01 (E3), C02–C05 (E2) | All, rated mass | VP Casino Marketing + FP&A | Player-trip theo, offers, redemptions | Incremental contribution per $ | Cut non-incremental spend; fund responsive cells | M | Host pushback; RG exclusions; PDPA | Low (design only) | **High** | Yes, with adaptation |
| 2 FP right-sizing, established players | C02–C05 (E2) | Venetian, Londoner, Parisian (largest mass pools) | Casino Marketing | Same + tier history | Theo per $ FP; visits | Lower cost at constant theo | L | Competitor scramble 2026; share loss | Low | High | Hypothesis to test |
| 3 Total-guest-value room allocation | C07 (E3) | Venetian, Parisian, Sands Macao (≥98% occupancy) | Hotel RM + Casino Marketing | Night-level occupancy, comp vs cash, guest theo | Displaced cash revenue; RevPAR + theo | Recover cash ADR on sell-out nights | M | Guest experience for downgraded players | Medium (occupancy/ADR public) | Medium–High | Yes, with adaptation |
| 4 Dynamic cash room pricing | C07 (E3); a further RM citation was not retrieved | Londoner (new inventory), Plaza/Four Seasons | Hotel RM | Booking curves | ADR, RevPAR | Price to demand | M | Brand positioning | Medium | Medium | Yes |
| 5 New/lapsed reactivation | C10 (E4) | Cotai mass | Casino Marketing | Acquisition source, first-visit theo | Second-visit rate, theo | Grow base at lower cost | M | Weak evidence | Low | Uncertain | Hypothesis to test |
| 6 Labour scheduling | C12–C13 (E4) | Table games, F&B | Operations | Hourly demand, rosters | Labour cost per table hour, service levels | Lower overtime | H | Labour quotas; service strategy | Low | Uncertain | Not prioritised |
| 7 Cross-property itinerary offers | — (no case found) | Cotai (connected properties) | Marketing + Entertainment | Cross-property spend | Non-gaming spend per guest | Shift value to non-gaming (concession goals) | M | Attribution | Low | Uncertain | Hypothesis to test |
| 8 ML real-time bonuses | C11 (E4, online) | — | — | — | — | — | H | Online gaming illegal | — | — | **No** |
