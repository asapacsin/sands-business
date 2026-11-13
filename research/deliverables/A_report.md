---
title: "Measuring the Return on Mass-Market Reinvestment at Sands China"
subtitle: "An independent analysis of public information, with a proposed test design"
date: "13 November 2026"
---

> **Independence statement.** This is independent research by an external analyst, using only public
> information. The author has no affiliation with, internal access to, or endorsement from Sands China Ltd.
> or Las Vegas Sands Corp.
>
> **Evidence tags.** **[P id]** primary filing or official statistic (source ID and table);
> **[D file]** derived by the author from primary data (file in `research/outputs/`);
> **[I]** illustrative, not a Sands figure or forecast; **[U id]** unverified: earnings-call transcript copy,
> broker note, press, or published research seen only as abstract/metadata (graded in `case_register.csv`).
> Source IDs resolve in `research/sources/source_register.csv` (URL, date, SHA-256).
> "LVS-ER" = Las Vegas Sands earnings release (8-K Ex.99.1), Macao property tables; "DICJ-Q" = DICJ
> quarterly statistics, report 1 (totals) and report 3 (by game).

## 1. Executive summary

**The decision.** According to the Q2 2025 earnings call, Sands China raised mass-market customer
reinvestment from late April 2025 to recover share, with reinvestment applied "across the board" and the level to be "market sensitive" (management, verbatim)
**[U TR-LVS-2025Q2]**. The decision this report addresses is how to
size and allocate the *next* increment across the five Macao properties and customer tiers so that it earns
positive incremental profit after Macao's ~40% gaming tax **[U PR-TAX-2022]**.

**What the public evidence shows** (2Q25–3Q26 against 3Q23–1Q25):

1. **Share has recovered.** Sands' derived share of Macao total GGR rose from 22.4% (1Q25) to 25.4%
   (3Q26), and the derived mass-win index rose 4.5 points **[D results.json; from P LVS-ER, DICJ-Q]**.
2. **More of gross win is being reinvested.** The gap between implied gross win and booked casino revenue
   rose from 20.5% to 23.5% of gross win, about **US$226m a year** of additional rebates, discounts, comps
   and commissions **[D results.json net_to_gross]**. This is a proxy, not a promotional ledger.
3. **Margins fell, partly market-wide.** Sands' five-property adjusted property EBITDA margin fell
   4.2 points; peers moved by −2.6 to +0.3 points on a *directional* comparison (EBITDA vs EBITDAR definitions)
   **[D results.json margin_did]**. The difference of about −2.8 points (−2.1 excluding the low-hold 2Q26)
   is consistent with reinvestment costs, but it also spans the Londoner ramp and the satellite-casino
   closures. Sands' 3Q26 margin (27.8% for five properties; 27.3% including ferry and other
   **[P LVS-ER-2026-10-21]**) remains at or above the three SEC-filing peers (23.2–27.8%)
   **[P WYNN/MGM/MELCO-ER 3Q26]**.
4. **Whether the increment pays cannot be determined from public data.** Implied *average* returns range
   from 0.4× to 2.1× of cost, depending on how much of the share gain is attributed to reinvestment
   **[D economics.json + I attribution]**. Break-even is 1.0× on this measure.
5. **Hotels are effectively full.** Mean occupancy since 2Q25 was 98.5% at The Venetian, 98.3% at The
   Parisian and 99.1% at Sands Macao **[P LVS-ER hotel statistics]**. On those nights a complimentary room
   displaces a paying guest, so its true cost is closer to the cash rate than to housekeeping cost (about
   US$94–211 a night under illustrative sell-out probabilities, against roughly US$40 when not full **[I]**).

**Recommendation.** Management could consider a 12-week randomised reinvestment holdout across all
properties to measure the *marginal* return of the post-2Q25 increment by tier, paired with a room-comp
substitution test on forecast sell-out nights. Casino Marketing would own it with FP&A. At most 5–10% of
each mass cell would receive a changed offer **[I: design proposal]**. A change is adopted only if the
90% confidence lower bound on incremental contribution per player is above zero and no guardrail is
breached (visits, share, customer experience, responsible gambling).

## 2. The decision and why it matters now

Five candidate decisions were scored on materiality, strategic relevance, data availability, external
evidence, feasibility and actionability. The reinvestment decision scored highest (4.60/5); hotel room
allocation (3.60) was folded into it as a reinvestment channel **[D RESEARCH_SPEC.md §3, analyst scores]**.

The timing matters for three reasons:

- **It is an active choice.** On the Q2 2025 call management said: "around late April, we started to implement
  a more aggressive customer reinvestment program" and "We will, however, be market sensitive" **[U TR-LVS-2025Q2]**.
- **The competitive context changed again in 2026.** SJM's satellite casinos closed on 30–31 December 2025;
  in 2025 they generated about HK$9.77bn (~US$1.25bn) of GGR, which every concessionaire competed for
  **[U PR-SATELLITE-2026]**.
- **The economics are unforgiving.** With ~40% of GGR paid in gaming tax and levies, a dollar of
  reinvestment must generate about two dollars of *incremental* GGR to break even **[I τ = 0.40, v = 0.10; Section 7]**.

![F1. Sands share (derived from LVS volumes and DICJ) vs operator margins. [D results.json; P LVS-ER, DICJ-Q, peer ERs]](../outputs/figures/F1_share_vs_margin.png)

## 3. The Macao competitive environment

| Metric (MOP m) **[P DICJ-Q-2024/2025/2026, reports 1 and 3]** | 2024 | 2025 | 3Q26 |
|---|---|---|---|
| Games of fortune GGR | 226,782 | 247,404 (+9.1%) | 60,215 |
| Mass share of GGR (ex-VIP baccarat) | — | 72.5% | 71.9% |

**Peer margins** (directional only: definitions differ):

| Operator (Macau) **[P LVS/WYNN/MGM/MELCO-ER; D operator_quarter.csv]** | 1Q25 | 3Q25 | 1Q26 | 3Q26 | Mean change, post vs pre |
|---|---|---|---|---|---|
| Sands China (5 properties, adj. property EBITDA) | 31.5% | 31.8% | 30.4% | 27.8% | −4.2 pts |
| Wynn Macau + Wynn Palace (adj. property EBITDAR) | 29.1% | 30.8% | 28.2% | 27.8% | −2.6 pts |
| MGM China (segment adj. EBITDAR) | 27.8% | 26.1% | 24.4% | 23.2% | −2.0 pts |
| Melco Macau properties (adj. EBITDA) | 28.1% | 29.0% | 28.4% | 23.4% | +0.3 pts |

Galaxy Entertainment and SJM do not file with the SEC and were not included (documented gap). MGM China
reported a record 17.1% market share in 3Q26, which shows rivals were also competing for share
**[P MGM-ER-2026-10-28]**. EBITDAR excludes rent, so Wynn and MGM margins are not strictly comparable.

## 4. What comparable operators teach

Sixteen cases were reviewed and graded (`sources/case_register.csv`). Three lessons matter:

1. **Control groups, not intuition.** Harrah's (now Caesars) is the best-known example of offer decisions
   tested against control groups **[U LIT-LOVEMAN-2003, grade E3]**: persuasive on method, not proof of
   effect size.
2. **Established players often do not respond to free play.** Abstracts of peer-reviewed studies using real casino data report
   little response to free-play *reductions*; visitation fell about 20% only where free play was
   eliminated entirely **[U LIT-LUCAS-2024, LIT-LUCAS-2020, grade E2]**. These are US
   slot-player studies, so effect sizes do **not** transfer to Macao's baccarat-led mass market; the
   hypothesis and test design do.
3. **Rooms are a reinvestment currency.** Harrah's Cherokee priced rooms by total guest value and reported
   ~15% revenue gains against 3–7% for typical installations **[U LIT-METTERS-2008, grade E3, vendor co-authors]**.

Vendor case studies (workforce scheduling, AI personalisation) report large gains without counterfactuals;
they are graded E4 and used only to generate test ideas.

## 5. Sands China financial analysis

### 5.1 Portfolio trend

| Quarter **[P LVS-ER; D sands_portfolio_quarterly.csv]** | Net revenue (US$m) | Adj. property EBITDA (US$m) | Margin | Hold-adjusted margin | Net-to-gross gap |
|---|---|---|---|---|---|
| 1Q25 | 1,677 | 528 | 31.5% | 32.1% | 21.1% |
| 3Q25 | 1,874 | 596 | 31.8% | 31.7% | 22.2% |
| 1Q26 | 2,076 | 630 | 30.4% | 29.6% | 23.5% |
| 2Q26 | 1,751 | 426 | 24.3% | 29.3% | 26.4% |
| 3Q26 | 1,902 | 528 | 27.8% | 27.2% | 23.5% |

Five Macao properties, excluding ferry and other operations. The hold adjustment uses LVS's disclosed
impact of normalising rolling-chip win to 3.3%; 2Q26 included unusually low rolling hold worth about
US$87m of EBITDA **[P LVS-ER-2026-07-22]**. Hold-adjusted, the margin drifted down steadily from 32.1% to
27.2% **[D]**: not a single-quarter shock.

### 5.2 Property bridge, 3Q26 vs 3Q25

| Property (US$m) **[P LVS-ER-2026-10-21; D T3_property_bridge csv]** | Δ Net revenue | Δ EBITDA | Δ Margin | EBITDA effect of margin change |
|---|---|---|---|---|
| The Venetian Macao | −43 | −37 | −3.4 pts | −22 |
| The Londoner Macao | −1 | −41 | −5.9 pts | −41 |
| The Parisian Macao | +13 | −7 | −4.4 pts | −10 |
| The Plaza & Four Seasons | +32 | +11 | −0.2 pts | −1 |
| Sands Macao | +27 | +6 | +3.0 pts | +3 |

Compression is concentrated at The Londoner and The Venetian, where about 500 rooms are out of service
for renovation through 4Q27 **[P LVS-ER-2026-10-21, Venetian footnote]**. Over the full post-period,
property margins moved very differently: Parisian −9.4 pts, Sands Macao −6.9, Venetian −5.9,
Plaza/Four Seasons −3.1, Londoner +0.3 **[D results.json property_margin_pre_post]**. The Londoner's stability
masks the return of its rooms during the ramp.

![F3. Property EBITDA margins. [P LVS-ER; D]](../outputs/figures/F3_property_margins.png)

### 5.3 The reinvestment proxy

LVS discloses, per property, mass table drop and win rate, slot handle and hold, and rolling volume and win
rate **[P LVS-ER gaming statistics]**. From these, gross gaming win is reconstructed and compared with
booked casino revenue. The difference (the "net-to-gross gap") contains rebates, commissions, discounts,
loyalty deferrals and comps allocated to rooms and F&B: not a promotional ledger, but its change is
informative.

| Property **[D net_to_gross_gap_pct.csv]** | Gap, 3Q23–1Q25 | Gap, 2Q25–3Q26 |
|---|---|---|
| The Venetian | 15.0% | 17.5% |
| The Londoner | 23.9% | 26.7% |
| The Parisian | 18.5% | 21.4% |
| The Plaza & Four Seasons | 36.9% | 36.5% |
| Sands Macao | 13.5% | 16.9% |
| **Portfolio** | **20.5%** | **23.5%** |

The step-up appears at every property except The Plaza & Four Seasons (premium clientele), consistent with
a broad-based mass reinvestment programme.

![F2. Net-to-gross gap. [D]](../outputs/figures/F2_net_to_gross_gap.png)

### 5.4 Hotels and revenue mix

Revenue mix in 3Q26: casino 78/75/77/69/93% and rooms 7/15/14/13/4% of net revenue for
Venetian/Londoner/Parisian/Plaza & Four Seasons/Sands Macao **[P LVS-ER-2026-10-21; D F4 table]**. Average
occupancy since 2Q25: Venetian 98.5%, Parisian 98.3%, Sands Macao 99.1%, Londoner 96.6%, Plaza/Four
Seasons 94.4%, with ADRs of US$147–507 **[P LVS-ER hotel statistics; D]**. Hotels this full make the
opportunity cost of complimentary rooms material.

![F5. Hotel KPIs. [P LVS-ER]](../outputs/figures/F5_hotel_kpis.png)

### 5.5 Comparison with peers (quasi-experimental, weak identification)

A difference-in-differences comparison of mean margins (post 2Q25–3Q26 vs pre 3Q23–1Q25) gives Sands
**−2.8 points** relative to the peer average **[D results.json margin_did]**. Robustness checks, all **[D]**:

- Hold-adjusting Sands: −2.8.
- Excluding 2Q26: −2.1.
- Leaving out one peer at a time: −1.9 to −3.4.
- Placebo start dates in 2024: −0.3 to −0.8.

The post-2Q25 divergence is therefore larger than in earlier periods. It cannot be attributed to
reinvestment alone: three peers is a small sample, their EBITDA definitions differ, and the treatment
coincides with the Londoner ramp and the satellite closures.

## 6. Transferability

Of eight candidate approaches (`deliverables/transfer_analysis.md`), two transfer with adaptation and one
does not transfer at all:

- **Transfer with adaptation:** control-group offer testing, and total-guest-value room allocation.
- **Hypotheses to test, not results:** free-play right-sizing for established players, and reactivation of
  new or lapsed players.
- **Not prioritised:** labour scheduling (vendor evidence only).
- **Not transferable:** online ML bonus personalisation (online gaming is illegal in Macau).

The Macau-specific adaptations are: process customer data in Macau on pseudonymised IDs
**[U LAW-PDPA]**; exclude players flagged for responsible gambling; review host-managed premium players case
by case rather than randomising them; and allow for the 2026 competitive scramble.

## 7. Quantitative decision framework

**Break-even.** The incremental GGR needed per $1 of reinvestment is k* = c / (1 − τ − v), where τ is the
gaming tax rate (~40% **[U PR-TAX-2022]**), v is variable cost as a share of GGR (10% **[I]**) and c is 1,
or 1 − τ if promotional play reduces taxable GGR (unverified). k* = **2.0×**, or 1.2× if promotional
play is tax-deductible **[D economics.json + I]**.

![F6. Break-even multiple. [D formula; I parameters]](../outputs/figures/F6_break_even.png)

**Public-data anchor** (average, not marginal; not causal):

| Share gain used **[D economics.json; I attribution]** | Share of gain attributed to reinvestment | Incremental GGR (US$m/yr) | Contribution before reinvestment (US$m/yr) | Incremental deductions (US$m/yr) | Return multiple |
|---|---|---|---|---|---|
| Company definition +2.5 pts (23.6% → 26.1%) **[U TR-LVS-2025Q3, PR-SCL-3Q26]** | 100% | 539 | 270 | 226 | 1.19× |
| Company definition +2.5 pts | 50% | 270 | 135 | 226 | 0.60× |
| Derived index +4.5 pts | 100% | 968 | 484 | 226 | 2.14× |
| Derived index +4.5 pts | 50% | 484 | 242 | 226 | 1.07× |

**Scenario model** (`analysis/scenarios.py`; all response curves illustrative). The incremental pool is
split into property × tier cells with diminishing-returns response curves, ordered by the literature
(established players respond least) and calibrated so the pool breaks even on average **[I]**. Findings:

- **Reallocation across cells adds little:** US$0.4m, US$2.6m and US$8.1m a year in the conservative,
  expected and optimistic cases, with the share guardrail met in every scenario **[I scenario_results.json]**.
- **The level of the increment matters more.** With diminishing returns, an increment that breaks even on
  average has marginal dollars *below* break-even; in the base case the best-performing pool size is 25–50%
  of the current increment **[I]**.
- **The sign depends on unknown inputs.** The pool's net contribution flips sign with the true response
  level, v, τ and the tax treatment of promotional play **[I sensitivity]**. Public data identifies none of
  these, so the conclusion rests on a test rather than on the model.

![F7. Scenarios. [I]](../outputs/figures/F7_scenarios.png)
![F8. Sensitivity. [I]](../outputs/figures/F8_tornado.png)

## 8. Recommended next action

| Element **[I: design proposal; parameters set by Sands]** | Recommendation |
|---|---|
| Action | 12-week randomised reinvestment holdout (8 weeks of treatment plus 4 of follow-up) in every property × mass tier. Arms: current offer; −30% offer; reallocated offer. Plus a room-comp vs non-room-reward test on nights forecast at ≥97% occupancy |
| Owner | Casino Marketing (design and offers), with FP&A (measurement) and Hotel Revenue Management (room test); Compliance sign-off |
| Financial mechanism | Remove reinvestment that does not change behaviour; recover cash room revenue on sell-out nights; redeploy savings to cells with measured positive return |
| Metric | Incremental contribution per player = Δtheo·(1−τ−v) − Δreinvestment − Δroom opportunity cost |
| Threshold | Adopt a change in a cell only if the 90% CI lower bound is > 0 and no guardrail is breached (visits, share, complaints, responsible gambling, host attrition) |
| Timeline | 4 weeks of design and compliance; 12 weeks in market; a decision at week 17 |
| Exposure | At most 5–10% of each cell receives a changed offer (size *illustrative*; Sands would set it from its own variance data) |

**What would change this recommendation:** internal or test evidence that the marginal return in most cells
exceeds 2× (or 1.2× if promotional play is tax-deductible) **[D economics.json + I]**. In that case the
increment should be kept or raised. The full protocol is in `deliverables/experiment_protocol.md`; the internal data it needs is listed
in `deliverables/internal_data_request.md`.

## 9. Risks, competing explanations and limitations

| Competing explanation for lower margins **[evidence as tagged per row]** | Status |
|---|---|
| Rolling hold variance | Addressed with LVS's own hold adjustment **[P LVS-ER]** |
| Premium-segment weakness (management's 3Q26 explanation) | Partly visible: Venetian rolling win 3.97% vs 5.87% **[P LVS-ER-2026-10-21]**; not separable from mass economics |
| Londoner ramp and Venetian room renovation | Present; cannot be separated with public data |
| Opex inflation and deliberate service investment | Management cites "investments in enhanced service and hospitality offerings" **[P LVS-ER-2026-10-21]**; costs not disclosed by property |
| Competitor incentives after satellite closures | Market-wide **[U PR-SATELLITE-2026]**; partly netted by the peer comparison |
| Accounting reclassification | No restatement detected (comparatives match prior releases in integrity tests) **[D tests]** |

**Limitations:** no customer-level or offer-level data; the net-to-gross gap mixes several deduction types;
the share index differs from the company's definition (the derived total GGR share of 25.4% for 3Q26
matches a broker figure **[U BRK-CLSA-2026Q3]**); only three peers, with mixed EBITDA definitions; external
studies are US- and slot-based; the tax treatment of promotional play is unverified.

**What cannot be concluded:** whether the current reinvestment level is profitable at the margin, or which
property or tier has the highest return.

## 10. References

Primary data (66 registered sources with URLs and SHA-256 hashes in `sources/source_register.csv`):

- **[P LVS-ER-*]** Las Vegas Sands Corp., quarterly earnings releases (Form 8-K Ex.99.1), 25 Jan 2023 – 21 Oct
  2026, SEC EDGAR, e.g. https://www.sec.gov/Archives/edgar/data/1300514/000130051426000099/lvs_ex991x09302026.htm
- **[P DICJ-Q-*]** DICJ, Gaming Statistics, quarterly, 2023–2026:
  https://www.dicj.gov.mo/web/en/information/DadosEstat/2026/report_en.xml
- **[P WYNN-ER-*, MGM-ER-*, MELCO-ER-*]** Wynn Resorts, MGM Resorts International and Melco Resorts &
  Entertainment earnings releases, 2023–2026, SEC EDGAR.

Research and secondary sources (registered; tags as used above). Research items were read as abstracts or metadata only:

- **[U LIT-LOVEMAN-2003]** Loveman, G. (2003). Diamonds in the Data Mine. *Harvard Business Review*, May.
- **[U LIT-LUCAS-2024]** Lucas, A. F., & Spilde, K. (2024). Measuring the Impact of Reduced Free-play Offers on Casino Loyalty Behavior. *UNLV Gaming Research & Review Journal* 28(1). Abstract only. https://oasis.library.unlv.edu/grrj/vol28/iss1/1
- **[U LIT-LUCAS-2020]** Lucas, A. F., Cho, S. R., & Singh, A. K. (2020). Impact of Casino Free Play on the Wagering Behavior of Light- and Medium-User Groups. *Cornell Hospitality Quarterly*. Abstract only. https://oasis.library.unlv.edu/hotel_fac_articles/368
- **[U LIT-METTERS-2008]** Metters, R. et al. (2008). The "Killer Application" of Revenue Management: Harrah's Cherokee Casino & Hotel. *Interfaces* 38(3), 161–175.
- **[U TR-LVS-2025Q2]** LVS Q2 2025 earnings call transcript (third-party copy). https://www.fool.com/earnings/call-transcripts/2025/07/23/las-vegas-sands-lvs-q2-2025-earnings-transcript
- **[U BRK-CLSA-2026Q3]** CLSA note on Sands China 3Q26 via Futu News. https://news.futunn.com/en/post/1001893168/major-brokerage-clsa-sands-china-01928-hk-q3-results-meet
- **[U PR-TAX-2022]** GGRAsia (2022). https://www.ggrasia.com/macau-40pct-ggr-tax-in-new-law-ce-can-cut-up-to-5-points/
- **[U PR-SATELLITE-2026]** focusgn (2026). https://focusgn.com/asia-pacific/sjm-posts-2025-loss-as-satellite-casino-closures-impact-results
- **[U LAW-PDPA]** DLA Piper, Data Protection in Macau SAR. https://www.dlapiperdataprotection.com/?c=MO&t=law
