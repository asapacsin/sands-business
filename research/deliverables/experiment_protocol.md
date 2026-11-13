# T18 — Experiment protocol: Mass reinvestment level and mix test

*Pre-registration-style protocol written by an external researcher using public information. Execution
requires Sands China internal data, approvals and systems. Numeric tolerances marked `[SET BY SANDS]` are
business decisions this document cannot make.*

## 1. Question

For rated mass players, does the current (post-2Q25) reinvestment level and mix earn positive incremental
contribution after gaming tax, and would a reduced or reallocated offer do better?

## 2. Design

| Element | Specification |
|---|---|
| Unit | Rated mass player (pseudonymised customer ID), property of record |
| Population | Rated mass players with ≥1 visit in the prior 12 months. **Excluded**: self-excluded, RG-flagged, VIP/rolling, host-managed premium players (reviewed case by case instead), employees |
| Strata | Property (5) × tier (established / lapsed-or-new / premium mass) × baseline theo decile → randomise within strata |
| Arms | **A** current offer (control, ~80–90%); **B** reduced offer, −30% free play / promotional credit (5–10%); **C** reallocated: B's saving redeployed as new/lapsed-player or non-room rewards (5–10%) |
| Room sub-test | On nights forecast ≥ 97% occupancy: randomise room comp vs equal-value non-room reward among players below a theo threshold `[SET BY SANDS]` |
| Duration | 8 weeks treatment + 4 weeks follow-up (delayed visit effects). Avoid starting within 2 weeks of Golden Week / CNY, or stratify by calendar block |
| Concealment | Hosts and floor staff are not told assignments where feasible; offer system assigns automatically |

## 3. Metrics

| Type | Metric | Definition |
|---|---|---|
| **Primary** | Incremental contribution per player | Δtheo·(1 − τ − v) − Δreinvestment cost − Δcomp-room opportunity cost (τ = 0.40 unless the tax treatment of promotional play is confirmed otherwise) |
| Secondary | Δtheo; Δvisits; Δnon-gaming spend; reinvestment cost per $ theo | Per player, test window and follow-up |
| Guardrail 1 | Visit frequency | Arm B/C vs A: decline no worse than −X% `[SET BY SANDS]` (illustrative: −10%) |
| Guardrail 2 | Mass-share trend | Portfolio mass share (company definition) not below pre-test 4-quarter low |
| Guardrail 3 | Customer experience | Complaints per 1,000 players; NPS where measured |
| Guardrail 4 | Responsible gambling | No increase in RG-indicator rates in any arm; any treated player newly flagged is removed and offered standard RG support |
| Guardrail 5 | Host attrition | Top-tier relationship losses, reviewed weekly |

## 4. Success threshold (pre-declared)

Adopt arm B or C for a cell only if **(a)** the 90% CI lower bound of the primary metric (B or C minus A) is
> 0 for that cell, **and (b)** no guardrail is breached. Otherwise keep the current offer. Cells are
pre-registered; no post-hoc cell slicing for adoption decisions.

## 5. Analysis plan

- Estimator: stratified difference in means with CUPED (pre-period theo covariate), as implemented in
  `analysis/holdout_analysis.py` (synthetic validation: 91% coverage of 90% CIs; correct adopt / do-not-adopt
  calls in both simulated cases).
- Outcome = theo, not actual win (removes hold noise); actual win reported as secondary.
- Power: MDE = (z₀.₉₅ + z₀.₈₀)·σ·√(1/n_T + 1/n_C). Example `[ILLUSTRATIVE]`: σ = US$500 contribution per player,
  2,400 treated vs 21,600 control → MDE ≈ US$27 per player. Sands should compute σ from internal history.
- Heterogeneity: report by property × tier, with a Holm correction for adoption decisions.
- Spillovers: household and group play (shared hosts) → cluster-randomise by host book if contamination
  is detected in a pilot.

## 6. Confounders and threats

| Threat | Handling |
|---|---|
| Seasonality, events, concerts | Randomisation; calendar-block stratification |
| Competitor promotions (post-satellite-closure scramble) | Affects all arms equally within the test window; external validity noted |
| Players learn of differential offers | Small arms; offers personalised already; monitor complaints |
| Hold variance | Use theo |
| Visa/travel policy shocks | Pause rule if arrivals move > 15% vs forecast `[ILLUSTRATIVE]` |
| Equilibrium (competitor response to a market-wide pull-back) | Not identified by this design; adopt gradually and monitor share |

## 7. Costs and risk cap

Maximum forgone contribution ≈ (arm B share) × (cell contribution) × (lift lost). With a 10% arm, the
exposure is bounded to ~10% of a cell's incremental theo for 8 weeks. Analyst and CRM effort is roughly
1 analyst for 3 months plus CRM configuration `[ILLUSTRATIVE]`.

## 8. Ethics and compliance

- Legal review of offer variation under DICJ rules; documented PDPA basis for processing.
- Data stays in Macau; only aggregate results leave (PDPA cross-border rules — `notes/macau_context.md`).
- RG exclusions and monitoring as in Guardrail 4; no arm ever increases incentives to at-risk players.

## 9. Where causal identification is NOT possible

- From public data alone (any level).
- For VIP/rolling and host-managed premium players (small n, negotiated terms): use case review.
- Market-level equilibrium effects of a pull-back by Sands.
