# T19 — Internal data that would be needed (not requested, not held)

This list shows what an internal team would need to replace this project's public-data proxies.
The author does **not** have, and has not requested, any of this data.

| # | Table (grain) | History | Key fields | Used for | Hypothesis / metric | Privacy handling (PDPA) |
|---|---|---|---|---|---|---|
| 1 | Player-trip (player × trip) | 24 months | pseudonymised ID, property, tier, dates, rated drop, theo, actual win, game type | Baseline theo, outcome, CUPED covariate | H5, primary metric | Pseudonymised in Macau; no names |
| 2 | Offers issued / redeemed (offer × player) | 24 months | offer type (FP, rebate, room, F&B, show), face value, cost basis, issue/redeem dates, channel (host / CRM) | Reinvestment cost by cell | H5; cost side of §8.3 | Same |
| 3 | Comp room nights (night × room) | 24 months | comp vs cash vs casino rate, guest theo, rate code | Comp-room opportunity cost | H4 | Aggregate to night × property for analysis |
| 4 | RM forecasts and actuals (night × property × room type) | 24 months | forecast occupancy, final occupancy, ADR by segment, denials | P(sellout) | H4 | Non-personal |
| 5 | Net-to-gross reconciliation (property × month) | 36 months | gross win, commissions, rebates, discounts, loyalty deferral, comp allocation | Replace public "gap" proxy with actual components | T11 validation | Non-personal |
| 6 | Host assignments (player × host) | 12 months | host ID, tier | Cluster design, exclusions | Experiment design | Pseudonymised |
| 7 | RG flags and exclusions | Current | flag type, date | Exclusions and guardrail | Guardrail 4 | Strictly restricted; used only to exclude |
| 8 | Labour by outlet (outlet × hour) | 12 months | hours, staff count, covers/tables open | Variable cost v | §8.3 parameter v | Aggregated |
| 9 | Gaming tax treatment memo | — | treatment of promotional play in taxable GGR | τ treatment switch | k* (2.0× vs 1.2×) | Non-personal |
