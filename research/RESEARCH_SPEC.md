# Research Specification — Data-Driven Reinvestment Allocation at Sands China

| Field | Value |
|---|---|
| Document type | Execution-ready research specification (**not** the research report) |
| Version / date | v1.2 — 2026-11-13 (v1.1: regulation correction from T07; v1.2: break-even formula correction from T13) |
| Author status | Independent external research using public information only. No affiliation with, access to, or endorsement by Sands China Ltd. or Las Vegas Sands Corp. |
| Latest public period in scope | Q3 2026 (quarter ended 30 Sep 2026), released by Las Vegas Sands around 21–22 Oct 2026 |
| Task registry | [`research/work.json`](work.json) (machine-readable backlog, validated by `scripts/frontier.py`) |
| Spec gate | `python3 scripts/check_research_spec.py research/RESEARCH_SPEC.md` |

### Evidence labels used throughout this spec

Every factual statement in this spec carries one of these labels. The eventual report must keep using them until a claim is upgraded.

| Label | Meaning | Allowed use in final report |
|---|---|---|
| `[PRIMARY ✔]` | Checked against the issuer's own filing / official statistic; URL, page, period recorded in the source register | Stated as fact with citation |
| `[SECONDARY ✔]` | Seen in reputable secondary reporting during spec preparation (2026-11-13); primary filing **not yet opened** | Only after upgrade to `[PRIMARY ✔]` (task T03/T04) |
| `[TO-VERIFY]` | Analyst background knowledge, not checked this session | Never, until verified |
| `[ILLUSTRATIVE]` | Hypothetical number used only to show the arithmetic of a method | Only with the label "illustrative, not a Sands figure" |
| `[DERIVED]` | Computed by us from verified inputs; formula and inputs recorded in code | Stated with method note |

Evidence-strength grades for external case studies (used in §5, §9):

| Grade | Definition |
|---|---|
| **E1** | Independent (e.g., peer-reviewed) study with a credible causal design: randomized holdout, natural experiment, well-specified DiD |
| **E2** | Independent / peer-reviewed analysis of real operator data, observational or quasi-experimental with stated limitations |
| **E3** | Company-reported result (filings, earnings calls, executive-authored articles) — not independently audited for causality |
| **E4** | Vendor case study with quantified outcome and some disclosed method |
| **E5** | Practitioner anecdote or community discussion (qualitative only) |
| **E6** | Untested hypothesis / our inference |

---

## 1. Research objective and intended audience

### 1.1 Objective

Produce an independent, evidence-graded analysis of **one concrete, financially material decision** facing Sands China. The analysis should show how a strategy team could use public financial evidence, documented practice from comparable operators, unit economics and a validation design to decide what to do next. The research must end in a recommendation that names **the action, the owning business function, the financial mechanism and the measurement method**.

### 1.2 Audience and what each needs

| Audience | What they need from the work | Implication for deliverables |
|---|---|---|
| Recruitment contact (Manian Chong) | Quick evidence of commercial judgement, initiative and professionalism | Deliverable B (2-page brief) must be readable in 5 minutes, respectful in tone, and make no claims of internal knowledge |
| Strategic analysis / business-management team | A credible Sands-specific question, correct economics (GGR vs net revenue vs EBITDA, gaming tax wedge), honest limits on causal claims | Deliverable A (8–12 pp) + Deliverable C (reproducible materials) |
| Interviewers | Ability to defend assumptions and identification strategy | Deliverable D (question bank with evidence-based answers) |

### 1.3 Success standard

An experienced casino strategy analyst reading Deliverable A should agree that: (a) the question matters to Sands now; (b) the numbers are correctly defined and sourced; (c) the method separates what public data can and cannot show; (d) the proposed internal test would actually establish incrementality.

### 1.4 Non-goals

- No claim that Sands management is under-performing or mis-allocating resources unless the evidence clearly supports it. Higher spending can be a deliberate investment, and the research is framed that way.
- No sophisticated ML used for display. A model is included only when it changes a decision or its measurement.
- No fabricated internal data, references, quotations or causal effects.

---

## 2. Candidate Sands China business decisions

Five candidates were considered. Facts cited here are `[SECONDARY ✔]` unless marked otherwise and **must be upgraded to `[PRIMARY ✔]`** in tasks T03–T05.

**Context facts behind the candidates** (all `[SECONDARY ✔]`, to be checked against the LVS Q2-2025 / Q3-2026 releases and call transcripts):

- In the Q2 2025 earnings call, LVS management said it had under-performed in Macao partly because it had not done enough on **customer reinvestment**. It raised reinvestment and promotional activity from late April 2025 to recapture share, and said reinvestment would be market-driven rather than tied to a fixed EBITDA-margin target. ([Q2 2025 transcript](https://www.fool.com/earnings/call-transcripts/2025/07/23/las-vegas-sands-lvs-q2-2025-earnings-transcript))
- Sands China's Macao **mass-market revenue share** was 23.6% in Q1 2025, ~25.4% in Q3 2025 and **26.1% in Q3 2026**, the highest since 4Q23. Analysts cite 25.4–25.5% on a total-GGR basis, so the share definitions must be reconciled. ([focusgn](https://focusgn.com/asia-pacific/sands-china-third-quarter-revenue-rises-8-4-as-macau-market-share-grows), [Futu/CLSA](https://news.futunn.com/en/post/1001893168/major-brokerage-clsa-sands-china-01928-hk-q3-results-meet))
- Q3 2026: Macao **adjusted property EBITDA US$529m, −12.0% y/y** (US$601m in Q3 2025); margin **27.3%, −420 bps**; net revenue ~US$1.93bn, +1.4% y/y; rolling-play hold added ~US$11m. Nine-month adjusted property EBITDA US$1.59bn, −6.5%. ([Investing.com](https://ca.investing.com/news/stock-market-news/las-vegas-sands-q3-2026-slides-ebitda-falls-17-amid-premium-weakness-93CH-4894774), [Macau Business](https://macaubusiness.com/sands-chinas-earnings-down-14-pct-y-o-y-amid-opex-surge/), [BigGo](https://finance.biggo.com/news/US_LVS_2026-10-21))
- Q3 2026 by property (revenue / adjusted property EBITDA, y/y): Venetian ~$649m (−6.2%) / $205m (−15.3%); Londoner $685m (flat) / $178m (−18.7%); Parisian $231m (+6%) / $46m (−13.2%); Plaza & Four Seasons $238m (+15.5%) / $85m; Sands Macao $99m (+37.5%) / $14m (+75%). ([sigma.world](https://sigma.world/news/sands-china-q3-29-percent-191-million-cash/), [GGRAsia](https://www.ggrasia.com/?p=181096))
- Management attributed margin pressure to higher operating costs, higher promotional spend and a mix shift, and called Q3 2026 premium weakness "aberrational". The Londoner, fully available from mid-2025 after renovation, has a stated target of US$1bn+ annual EBITDA. ([Q4 2025 transcript](https://www.fool.com/earnings/call-transcripts/2026/01/28/las-vegas-sands-lvs-q4-2025-earnings-transcript/), [ASGAM 2024](https://asgam.com/2024/07/26/sands-china-expects-its-macau-margins-to-near-40-once-the-londoner-macao-fully-fitted-out/))
- Macau market GGR 2025: MOP247.4bn (~US$30.9bn), +9.1% y/y, ~84.6% of 2019. Mass ~73% of full-year GGR per a CreditSights summary. ([CDC Gaming](https://cdcgaming.com/brief/macau-ggr-up-9-1-in-2025-to-us30-9-billion-following-subdued-december-result/), [sigma.world](https://sigma.world/news/macau-2025-ggr-creditsights-report/))

| # | Candidate decision | Owner (functional) | Why it might matter |
|---|---|---|---|
| D1 | **Allocation of incremental mass-market customer reinvestment** (free play / promotional credit, rebates, comp rooms, F&B, entertainment) across the five Macao properties and customer tiers | Casino Marketing + Finance (FP&A) + Property Ops | Explicit strategy since Q2 2025; share has risen while EBITDA and margin have fallen. Is the *marginal* reinvestment dollar incremental? |
| D2 | **Hotel room allocation and pricing**: cash vs complimentary rooms vs casino-rate rooms, especially in the newly expanded Londoner inventory | Hotel Revenue Mgmt + Casino Marketing | Room nights are a reinvestment currency. Comp rooms have a real opportunity cost only on high-occupancy nights |
| D3 | **Londoner Macao ramp-up**: how to close the gap between the ~US$712m current annualised run-rate (Q3 2026 × 4) `[DERIVED]` and the US$1bn+ target | Property GM + Finance | A large capital project with a stated return target |
| D4 | **Premium vs base-mass segment mix and hold-volatility management** | Casino Ops + Finance | Q3 2026 results were hurt by premium weakness; segment mix drives margin |
| D5 | **Non-gaming investment prioritisation** (MICE, entertainment, retail, F&B) under the concession's non-gaming commitments | Strategy + Non-gaming BUs | Policy pressure to diversify; whole-resort customer value |

The user-proposed decision (allocate incremental service, marketing and operational investment across properties, segments and activities) is broad. D1 is a sharper, more measurable version of it, and D2 is a sub-component of D1.

---

## 3. Decision-selection matrix and justification

Scores are 1 (weak) to 5 (strong) and are the analyst's judgement, recorded so a reviewer can challenge them. The weights reflect the brief's priorities.

| Criterion (weight) | D1 Reinvestment allocation | D2 Room allocation | D3 Londoner ramp | D4 Segment mix / hold | D5 Non-gaming |
|---|---|---|---|---|---|
| Financial materiality (0.20) | 5 — reinvestment levels move margin by hundreds of bps on ~US$7–8bn revenue `[DERIVED]` from 9M net revenue $5.81bn | 3 | 4 | 4 | 3 |
| Relevance to current reported strategy (0.20) | 5 — explicitly named by management | 3 | 4 | 3 | 3 |
| Public-data availability (0.15) | 3 — share, margin, gaming volumes and hotel KPIs are public; promotion cost is only partly observable | 4 — occupancy, ADR, RevPAR per property `[TO-VERIFY]` | 3 | 3 | 2 |
| Comparable-operator evidence (0.15) | 5 — Harrah's/Caesars CRM, peer-reviewed free-play studies | 4 — casino-hotel RM literature | 2 | 2 | 2 |
| Quantitative feasibility (0.10) | 4 | 4 | 3 | 3 | 2 |
| Actionability of recommendation (0.10) | 5 — a holdout test and an allocation rule are directly implementable | 4 | 3 | 2 | 3 |
| Analyst-competency showcase (0.10) | 5 — economics, causal inference, experiment design | 4 | 3 | 3 | 3 |
| **Weighted score** | **4.60** | **3.60** | **3.25** | **2.95** | **2.60** |

**Selected primary decision: D1, with D2 folded in as one reinvestment channel.**

Why D1:
1. It is the decision management has visibly made and is still making. The research evaluates an active trade-off; it does not invent one.
2. Its core question, whether the *marginal* reinvestment dollar creates *incremental* profit, cannot be answered from revenue or share trends alone. That is the gap a data-driven analyst fills.
3. Comparable-operator evidence is unusually strong: there is peer-reviewed work on real casino free-play data and a well-documented control-group culture at Harrah's.
4. Public data can bound the answer at the portfolio and property level. A clear line can be drawn between public evidence and the internal test needed to settle it, which is itself a demonstration of analytical judgement.

Why the others are not primary: D3 depends heavily on internal ramp plans; D4 is dominated by hold volatility that public data cannot separate from strategy; D5 lacks comparable quantified evidence. These are used as context and as competing explanations in §12.

---

## 4. Final research question and testable hypotheses

### 4.1 Primary research question

> **How should Sands China allocate the next increment of mass-market customer reinvestment across its five Macao properties and customer tiers so that it generates positive incremental adjusted property EBITDA after gaming tax and room opportunity cost, while sustaining mass-market share near current levels? And what test would show management whether it does?**

### 4.2 Sub-questions

- SQ1. What do public results show about the relationship between Sands' mass share gains and its margin and EBITDA since Q2 2025, relative to Macao peers, after accounting for hold, premium mix and the Londoner ramp?
- SQ2. Where, by property, has margin compression been concentrated relative to revenue growth?
- SQ3. What is the break-even incremental GGR per dollar of reinvestment after Macao gaming tax, and how does it compare with documented promotional response in the literature?
- SQ4. When is a comp room economically "free", and when does it displace cash revenue?
- SQ5. Which external analytical practices transfer to Macao, and what adaptations do regulation, privacy law and customer mix require?
- SQ6. What internal experiment would identify incrementality at acceptable cost and risk?

### 4.3 Hypotheses

| ID | Hypothesis | Testable with | Falsified if |
|---|---|---|---|
| H1 | Since Q2 2025, Sands' mass-share gain relative to peers has come with a margin decline greater than peers' that is **not fully explained** by hold, premium mix or Londoner room availability | Public quarterly panel 2023Q1–2026Q3 (T08, T12) | After adjustments, Sands' margin change is within the peer range |
| H2 | The share gained per point of margin given up has **diminished** over successive quarters since 2Q25 (diminishing marginal returns) | Public panel, quarterly ratio Δshare / Δmargin (T12) | The ratio is stable or rising |
| H3 | Margin compression is **heterogeneous across properties** beyond what revenue changes imply, so allocation matters more than the total level | Public property tables (T09) | Property margins move together within ±150 bps of the portfolio |
| H4 | On high-occupancy nights at specific properties, complimentary rooms displace cash revenue, so their true cost exceeds marginal cost | Public occupancy and ADR (T10); internal night-level data for confirmation | Occupancy is well below sell-out at all properties |
| H5 | A material share of reinvestment given to established mass players is **non-incremental**, consistent with peer-reviewed findings of insensitivity to free play | **Internal only**: randomized holdout (T20) | The holdout shows incremental theo-win ≥ break-even multiple |
| H6 | Because roughly 40% of GGR goes to gaming tax `[TO-VERIFY]`, the break-even incremental GGR per $1 of reinvestment is around 1.8–2.5× (1.1–1.5× if promotional play reduces taxable GGR) `[DERIVED]`, higher than the 1.0× intuition | Arithmetic (T13); tax treatment of promotional play must be verified | Verified tax treatment changes the wedge materially |

---

## 5. External casino case-study research plan

### 5.1 Search protocol

- **Sources, in priority order**: operator 10-K/annual reports and investor presentations; peer-reviewed hospitality and gaming journals (*Cornell Hospitality Quarterly*, *UNLV Gaming Research & Review Journal*, *International Journal of Hospitality Management*, *Journal of Revenue and Pricing Management*, *Interfaces/INFORMS Journal on Applied Analytics*); HBS/Ivey cases; reputable trade press (GGRAsia, Inside Asian Gaming, CDC Gaming); vendor case studies; practitioner communities.
- **Search strings** (log every query in `research/sources/search_log.csv`): `casino free play incremental`, `casino loyalty control group`, `casino hotel revenue management total guest value`, `casino workforce scheduling forecasting`, `Marina Bay Sands analytics`, `MGM Rewards personalization results`, `Caesars Rewards analytics`, `integrated resort cross-sell`, plus Google Scholar forward citations of every E1/E2 paper found.
- **Stopping rule**: at least 12 cases across application areas A–D, with at least 3 rated E1/E2. Stop when two consecutive search rounds add no case rated ≥E3.

### 5.2 Case-extraction template (one row per case in `research/sources/case_register.csv`)

`case_id, operator, property/market, application_area(A–D), business_problem, decision_changed, data_used, method, reported_outcome(metric, magnitude, period), evidence_grade(E1–E6), control_group(Y/N/unclear), causal_design, documented_costs_limitations, transferability_to_sands(High/Med/Low), macau_adjustments, source_url, publication_date, accessed_date, verification_status`

### 5.3 Seed cases (starting points only; each must be verified and graded in T06)

| Case | Area | What to establish | Provisional grade | Status |
|---|---|---|---|---|
| Harrah's/Caesars Total Rewards: G. Loveman, "Diamonds in the Data Mine", *HBR*, May 2003 | A | Segment-level offer testing against control groups; which decision changed (offer design for regional players) | E3 (executive-authored) | `[SECONDARY ✔]` exists; control-group detail so far only from secondary sources ([O'Reilly listing](https://oreilly.com/library/view/harvard-business-review/9781422171967/chapter007.html)) |
| Lucas & Spilde (2024), *UNLV GRRJ*: free-play reductions at a Western US tribal casino | A | Insensitivity to FP reductions; ~20% visitation drop only when FP was eliminated entirely | E2 (real data; check design) | `[SECONDARY ✔]` ([UNLV news](https://unlv.edu/news/article/study-diminishing-impact-casino-free-play-promotions), [GRRJ](https://oasis.library.unlv.edu/grrj/vol28/iss1/1)) |
| Lucas & Spilde (2017), *Cornell Hospitality Quarterly*: two tribal casinos' FP campaigns | A | One campaign effective, the other (≈$15m/yr) needing a retool | E2 | `[SECONDARY ✔]` |
| Lucas, Cho & Singh (2020), *CHQ*: FP redeemers vs non-redeemers, light/medium tiers | A | No group-level spend-per-trip difference | E2 | `[SECONDARY ✔]` ([SAGE](https://journals.sagepub.com/doi/ref/10.1177/1938965520963047)) |
| Lucas: increased FP awards, *Journal of Gambling Business & Economics* | A | Large FP increases produced no significant change in own-money losses or visitation | E2 | `[SECONDARY ✔]` ([JGBE](https://www.ubplj.org/index.php/jgbe/article/view/2239)) |
| Suh (2012), *CHQ* 52(2): FP coupon value vs slot volume | A | Findings to extract | E2? | `[TO-VERIFY]` content |
| Metters et al. (2008), *Interfaces*: revenue management at Harrah's Cherokee | B | Customer-value-based room allocation; reported revenue impact | E3/E4 | `[TO-VERIFY]` |
| Kuyumcu (2002), *J. Revenue & Pricing Mgmt*: "Gaming twist in hotel revenue management" | B | Total-guest-worth room pricing | E2/E4 | `[TO-VERIFY]` |
| Norman & Mayer (1997), *Cornell HRA Quarterly*: yield management in Las Vegas casino hotels | B | Early casino-hotel RM practice | E2 | `[TO-VERIFY]` |
| Marina Bay Sands (LVS filings/calls): Sands Rewards, hotel yield, IR operating model | A, B, D | Any quantified outcomes; most comparable Asian IR | E3 | To search |
| MGM Resorts (MGM Rewards, personalization) and Wynn | A, D | Quantified outcomes in filings or credible press | E3/E4 | To search |
| Workforce / staffing forecasting in casinos (operator or vendor cases) | C | Labour cost vs service-level results | E4 | To search |
| Asian IR peers (Genting Singapore / Resorts World, Galaxy, Melco) | A–D | Disclosed analytics programmes | E3/E4 | To search |

### 5.4 Grading rules (non-negotiable)

1. Vendor-reported uplift is graded E4 even if large, and never described as "proven".
2. A before/after comparison without a control group is "consistent with" an effect, never "caused".
3. Every case states what it **does not** show: cost, durability, novelty decay, selection.
4. Las Vegas/regional US slot-heavy evidence is flagged for **segment mismatch**, because Macao mass is table-baccarat-dominated (mass baccarat ~MOP36bn of ~MOP46bn mass GGR in 4Q25 `[SECONDARY ✔]`, [AGBrief](https://agbrief.com/news/macau/17/01/2026/macau-vip-baccarat-delivers-2-53b-in-4q25-accounting-for-30-7-of-ggr/)).

### 5.5 Practitioner and research-community review (application to methodology)

| Question | Sources to mine | Lesson to extract into method (examples of the expected form) |
|---|---|---|
| Why do analytics projects create profit vs unused dashboards? | Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* (CUP, 2020) `[TO-VERIFY edition]`; HBR/MIT SMR articles on analytics adoption; r/analytics, r/datascience, r/BusinessIntelligence threads (search "dashboard nobody uses", "analytics ROI", "stakeholder adoption") | Start from a named decision and decision owner (built into §8) |
| From KPI reporting to commercial influence | Same, plus casino-industry interviews in trade press | Present a recommendation as an option with economics and a test |
| Organisational blockers | Practitioner threads; consulting surveys (treat as E5) | Include a "decision owner / incentive" column in the matrix (§9) |
| Estimating ROI of analytics | Experimentation literature; finance practice | Define the success threshold before testing (§8.6) |
| Incremental vs would-have-happened-anyway revenue | Lucas papers; uplift-modelling literature; holdout practice | Use holdouts and theoretical win; never attribute total redeemer spend to offers |

Rule: community content is coded as **qualitative practitioner evidence (E5)**. Record thread URL, date, and the specific lesson. Quote no more than one sentence, and never treat it as representative.

---

## 6. Macau / Sands competitive and financial research plan

### 6.1 Entities and filings

| Entity | Listing / reporting | Primary documents to collect (period: FY2023 → Q3 2026) | Key definitional caveat |
|---|---|---|---|
| Sands China Ltd. (1928.HK) | HKEX; IFRS; interim + annual reports | Annual Report 2024, 2025; Interim Report 2025, 2026; HKEX announcements | IFRS vs LVS's US GAAP segment numbers can differ; reconcile |
| Las Vegas Sands Corp. (LVS) | NYSE; US GAAP; quarterly 10-Q/10-K, earnings releases with Macao property tables | Q1 2023 – Q3 2026 earnings releases, supplemental tables, call transcripts | "Adjusted property EBITDA" is LVS-defined; hold-adjusted figures are company estimates |
| Galaxy Entertainment (27.HK) | HKEX; quarterly unaudited updates | Quarterly results Q1 2023 – Q3 2026 | "Adjusted EBITDA" definition differs; reports "normalized for luck" |
| Wynn Macau (1128.HK) / Wynn Resorts | HKEX + Wynn Resorts 10-Q segment data | Wynn Resorts quarterly releases (Macau operations) | Segment basis differs between parent and HK filings |
| Melco Resorts & Entertainment (MLCO) | Nasdaq; quarterly 6-K | Quarterly releases (City of Dreams, Studio City, Altira) | Property mix includes Cyprus/Manila; isolate Macau |
| MGM China (2282.HK) / MGM Resorts | HKEX + MGM Resorts 10-Q | MGM Resorts quarterly releases (MGM China segment) | Different EBITDA definitions |
| SJM Holdings (880.HK) | HKEX; interim/annual + quarterly updates | Results incl. satellite-casino disclosures | Satellite casino closures (end-2025 `[TO-VERIFY]`) shift share |

### 6.2 Market and government data

| Data | Publisher | Frequency | Use |
|---|---|---|---|
| Monthly GGR; quarterly GGR by game (VIP baccarat, mass baccarat, slots) | DICJ (Gaming Inspection and Coordination Bureau) — exact statistics URL to be confirmed (the URL tried on 2026-11-13 returned 404) | Monthly / quarterly | Market totals, mass share denominator |
| Visitor arrivals by origin, length of stay, per-capita spending | DSEC (dsec.gov.mo, reachable 2026-11-13) | Monthly / quarterly | Demand drivers; confounders |
| Hotel occupancy, guests, room supply | DSEC / MGTO Data+ (dataplus.macaotourism.gov.mo, reachable) | Monthly | Market occupancy for H4 |
| Gaming tax receipts | DSF / press summaries ([AGBrief](https://agbrief.com/news/macau/11/03/2026/macau-gaming-tax-climbs-7-63-to-11-9b-in-2025/)) | Annual | Cross-check effective tax rate |
| Regulation | Law 16/2022 (gaming law amendments, concessions from 2023) `[TO-VERIFY]`; Law 7/2024 (gaming credit regime) and Law 20/2024 (illegal gambling) `[SECONDARY ✔]` — corrected in v1.1, see notes/macau_context.md; Personal Data Protection Act (Law 8/2005) `[TO-VERIFY]`; DICJ instructions on promotions, credit and responsible gambling | — | Constraints in §9 |

### 6.3 Metrics to compile (comparable-definition register)

For each operator and property, quarterly: net revenue (total and by category: casino, rooms, F&B, mall, convention/retail/other); adjusted (property) EBITDA and margin; hold-normalised EBITDA where disclosed; rolling chip volume and win %; non-rolling (mass) table drop and win %; slot handle and hold; hotel occupancy, ADR, RevPAR; mall revenue; mass GGR share and total GGR share.

Each metric records its definition, currency (US$/HK$/MOP), accounting basis (US GAAP/IFRS), period end, publication date and URL in `research/data/metric_dictionary.csv`. **Do not compare across operators unless the definitions match**, or the mismatch is documented and the comparison is marked "directional".

### 6.4 Investigation topics (from the brief), mapped to tasks

| Topic | Task |
|---|---|
| Revenue growth vs EBITDA growth | T08, T09 |
| Property-level performance | T09 |
| Gaming activity and market share | T08, T12 |
| Hotel utilisation, pricing, demand | T10 |
| Customer acquisition and retention | Public data is not observable; report as an internal-data requirement (T19) |
| Non-gaming revenue, cross-sell | T09 (category mix), T11 |
| Service investment and operating costs | T09 (only opex disclosed in filings; Sands China interim/annual notes) |
| Tourism patterns and competition | T07 |
| Regulation and data privacy | T07, §9 |

**Principle for interpretation**: a rise in promotional or operating expense is classified as *strategic investment* when it is linked to a stated objective with an observable return path (share, visitation, ramp). It is classified as *possible inefficiency* only when costs rise with no offsetting revenue, share or strategic rationale **and** peers facing the same market did not show the same pattern. Most findings are expected to be "undetermined from public data", and the report should say so.

---

## 7. Public datasets and source-verification strategy

### 7.1 Source register

`research/sources/source_register.csv` columns: `source_id, title, publisher, url, document_type, reporting_period, currency, accounting_basis, publication_date, accessed_date, sha256_of_downloaded_file, pages_used, evidence_label, verified_by, notes`.

- Raw downloaded filings go in `research/data/raw/` (gitignored if licensing is unclear). Their SHA-256 and URL are committed so another analyst can re-obtain the identical file.
- Every number in `research/data/processed/*.csv` carries `source_id` + page/table reference.

### 7.2 Verification protocol

1. **Primary first**: a secondary figure (press, broker note) is only a pointer; record the primary-source value. If they differ, use the primary value and log the discrepancy.
2. **Two-person rule substitute**: a second automated pass re-extracts 100% of headline figures and a random 20% of the rest from the primary PDF. Any mismatch blocks the deliverable (T22).
3. **Period alignment**: label every quarter by period-end date; note restatements.
4. **Currency**: convert to US$ only with a documented rate source and date (HKD and MOP are pegged/quasi-pegged; still record the rate used).
5. **Unreachable sources**: some hosts were unreachable from the preparation environment on 2026-11-13 (investor.sands.com returned 403, the DICJ statistics URL 404, mgmchinaholdings.com timed out). Fetch them via HKEXnews (reachable) or an alternative mirror, or mark them `UNVERIFIED — access`. Never fill the gap with recalled numbers.

### 7.3 Known public sources to verify (seed list)

| Purpose | Source | Status |
|---|---|---|
| Sands China filings | HKEXnews (hkexnews.hk, reachable) and investor.sandschina.com ([example PDF](https://investor.sandschina.com/static-files/d335806d-be20-484d-b72b-2cacf47f9528)) | Seen in search; content not opened |
| LVS releases and transcripts | investor.sands.com (403 from environment); transcripts via [Motley Fool Q2 2025](https://www.fool.com/earnings/call-transcripts/2025/07/23/las-vegas-sands-lvs-q2-2025-earnings-transcript) and [Q4 2025](https://www.fool.com/earnings/call-transcripts/2026/01/28/las-vegas-sands-lvs-q4-2025-earnings-transcript/) | Transcripts are secondary copies; prefer the official webcast/8-K exhibit |
| Q3 2026 LVS presentation | [MarketScreener copy](https://www.marketscreener.com/news/las-vegas-sands-third-quarter-2026-presentation-ce785cd9dc88f226) | Secondary copy; obtain the 8-K exhibit |
| Market GGR | DICJ; [CDC Gaming summary](https://cdcgaming.com/brief/macau-ggr-up-9-1-in-2025-to-us30-9-billion-following-subdued-december-result/) | Secondary; get DICJ tables |

---

## 8. Analytical methods, metrics, equations and model requirements

### 8.1 Metric definitions (must appear in the report glossary)

| Metric | Definition | Public? |
|---|---|---|
| GGR (gross gaming revenue) | Win from wagering before deductions; the basis for Macao gaming tax | Market: yes (DICJ). Operator: partly derivable |
| Net casino revenue | GGR less commissions, rebates, discounts and incentives, and the standalone value of comps allocated to other departments (ASC 606 / IFRS 15) `[TO-VERIFY exact LVS policy]` | Yes (filings) |
| Net revenue | Net casino + rooms + F&B + mall + convention/retail/other | Yes |
| Contribution profit (of a decision) | Incremental net revenue − gaming tax on incremental GGR − variable costs − promotional cost − opportunity cost | No (internal) |
| Adjusted property EBITDA | LVS-defined non-GAAP property earnings before D&A, corporate expense, etc. | Yes, by property |
| EBITDA margin | Adjusted property EBITDA / net revenue | Yes |
| Free cash flow / economic return | EBITDA − capex − tax − Δworking capital; return vs cost of capital | Group level only |
| Theoretical win ("theo") | Handle × house edge; used to measure play without hold noise | No (internal) |
| Reinvestment rate | Total reinvestment cost / GGR (or / theo) | No (internal); public proxy only via net/gross gap (T11) |

### 8.2 Method A — Financial performance decomposition (PUBLIC)

1. **Y/y and q/q bridges** of net revenue and adjusted property EBITDA by property, from LVS property tables, Q1 2023 – Q3 2026.
2. **Revenue decomposition by category** (casino, rooms, F&B, mall, other) and by property.
3. **Volume / win-rate / mix decomposition of casino revenue** (per segment: rolling, non-rolling, slots):
   `ΔRev_casino = Σ_g [ ΔVolume_g · WinRate_g,t−1 + Volume_g,t · ΔWinRate_g ]  (+ residual = net-to-gross deductions, interaction)`
   where volume is rolling chip volume, non-rolling drop or slot handle `[TO-VERIFY these are still disclosed per property]`.
   The residual between implied gross win and reported net casino revenue is a **noisy proxy for deductions, including promotions** (T11).
4. **Hotel**: `ΔRooms revenue ≈ ΔOcc · ADR · Rooms + Occ · ΔADR · Rooms + Occ · ADR · ΔRooms_available` (Londoner inventory change).
5. **Margin bridge**: ΔEBITDA = ΔNet revenue × prior margin + Net revenue × Δmargin; flag hold-normalised vs reported.
6. **Peer comparison**: same bridges for Galaxy, Wynn Macau, Melco Macau, MGM China and SJM where definitions allow.

**Observable**: revenue by category and property, EBITDA by property, gaming volumes and win rates, hotel KPIs, market share.
**Not observable**: promotional cost by channel, customer-level response, comp-room counts, variable cost by department, labour cost by property (beyond aggregate disclosures).

### 8.3 Method B — Unit economics of the reinvestment decision

For a reinvestment offer *o* to customer segment *s* at property *p*:

```
ΔΠ(o,s,p) = ΔGGR · (1 − τ)                      # incremental gaming win after gaming tax
          − ΔRebates_and_commissions
          + ΔNG · m_NG                          # incremental non-gaming spend × contribution margin
          − C_promo(o)                          # cash cost of reinvestment (FP redeemed, rebates)
          − OC_room(o)                          # opportunity cost of comp rooms (below)
          − ΔVariableCost                       # service, labour attributable to incremental play
```

- Measure ΔGGR as **incremental theoretical win**, not actual win, to remove hold noise. It is estimated against a counterfactual: holdout group or forecast.
- τ = effective gaming tax rate on GGR (35% special tax + ~4–5% levies ≈ 39–40% `[TO-VERIFY under Law 16/2022]`). Whether and how promotional play reduces taxable GGR must be verified; it changes the wedge.
- **Break-even multiple** (H6): incremental GGR required per $1 of reinvestment
  `k* = c_promo / (1 − τ − v)`, where v = variable cost as a share of incremental GGR and c_promo = 1 (or 1 − τ if promotional play reduces taxable GGR).
  `[ILLUSTRATIVE]` τ = 0.40, v = 0.10 → k* = 2.0 (1.2 if promotional play is tax-deductible). A $1 promotion breaks even only if it creates ≈ $2 of *incremental* GGR. (v1.2 correction: v1.0 applied v multiplicatively and stated 1.85.)
- **Comp room opportunity cost** for room-night r:
  `OC_room = P(sellout_r) · (ADR_cash,r − c_var) + (1 − P(sellout_r)) · c_var`
  where c_var is the marginal cost of an occupied room. When the hotel is full, the cost is close to lost cash ADR; when it is not, the cost is near housekeeping and amenities.
- **Marginal ROI**: `mROI = ΔΠ / C_promo`; allocate while mROI > hurdle h (e.g., 0, or the cost-of-capital-adjusted threshold).

### 8.4 Method C — Decision simulation / scenario model (PUBLIC + ILLUSTRATIVE)

**Model**: property × segment response curves with diminishing returns
`ΔTheo_s,p(x) = a_s,p · (1 − e^(−b_s,p · x))`, where x is incremental reinvestment.
Objective: maximise `Σ_s,p ΔΠ_s,p(x_s,p)` subject to `Σ x_s,p ≤ B` and the guardrail `MassShare ≥ S_min`.
The optimum satisfies the **equimarginal rule**: shift budget until marginal ΔΠ per $ is equal across cells (or zero).

**Calibration from public data**: only at portfolio and property level. Response parameters cannot be estimated from public data. They will be set as `[ILLUSTRATIVE]` ranges that bracket the literature (e.g., Lucas' near-zero effects for established players vs positive effects for lapsed or new players) and anchored to observed share and margin movements (T12).

**Public anchor, "implied cost per share point"** `[DERIVED, method]`:
```
Value of 1 pt mass share ≈ Market mass GGR × 1% × (1 − τ) × (1 − v)
Observed cost ≈ Δ(adjusted EBITDA vs peer-implied counterfactual) between periods
Implied payback = observed cost / value of share points gained
```
`[ILLUSTRATIVE]`: if mass GGR ≈ 73% × US$30.9bn ≈ US$22.6bn/yr, 1 pt ≈ US$226m GGR, ≈ US$113m after τ = 0.40 and v = 0.10 (additive), before reinvestment cost. The final model must recompute this from verified inputs.

**Scenarios** (all labelled illustrative, not Sands forecasts):

| Scenario | Definition |
|---|---|
| Baseline / BAU | Current reinvestment level and mix continue; share and margin held at the latest verified quarter |
| Conservative improvement | Reallocate 10% of reinvestment from low-response to higher-response cells; response gap at the low end of literature ranges |
| Expected improvement | Reallocate 20%; mid-range response gap |
| Optimistic improvement | Reallocate 30%, plus comp rooms re-priced on high-occupancy nights; upper-range response gap |

**Sensitivity**: tornado chart and two-way grids over τ, v, response elasticity, the share of non-incremental reinvestment (0–60%), the comp-room P(sellout) and the share guardrail. Report which assumptions flip the sign of the recommendation.

**Model requirements**: pure Python (pandas, numpy, scipy, matplotlib); deterministic seed; all parameters in `research/model/assumptions.yaml` with source or `ILLUSTRATIVE` tag; unit tests covering the break-even formula, the scenario totals and the equimarginal property.

### 8.5 Method D — Public-data quasi-experimental analysis (PUBLIC, weak identification)

- **Difference-in-differences / synthetic control**: treated = Sands China; donors = the 5 Macao peers; treatment = 2Q25 reinvestment shift; outcomes = mass share and EBITDA margin; quarterly 2023Q1–2026Q3.
- **Why identification is weak, stated up front**: n = 6 operators; the treatment coincides with the **Londoner room-inventory return** (mid-2025) and later with **satellite casino closures** (end-2025, `[TO-VERIFY]`); hold volatility; and peers changed their own promotional intensity. The result is reported as **descriptive evidence consistent or inconsistent with H1/H2, not a causal estimate**.
- Robustness: hold-normalised EBITDA where available; excluding the Londoner; placebo treatment dates; leave-one-out donors.

### 8.6 Method E — Validation and experimentation design (INTERNAL; for management)

**Primary design: randomised holdout within segment**
- Unit: rated mass player (customer ID), stratified by property of record, tier, recency/frequency and baseline theo decile.
- Arms: (A) current offer; (B) reduced offer, e.g., −30% free play; (C) reallocated offer, e.g., shifted to lapsed or new segment cells. Holdout share 5–10% per stratum to cap revenue risk.
- Duration: ≥ 8 weeks plus 4-week post-period to catch delayed visitation effects. Pre-registered.
- **Primary metric**: incremental contribution per player (§8.3) using theo.
- **Guardrails**: visitation frequency, share of wallet proxies (in-market visits), mass-share trend, complaints/NPS, host-relationship attrition for top tiers, responsible-gambling indicators (no increased intensity for at-risk flags).
- **Success threshold (pre-declared)**: the 90% CI lower bound of incremental contribution per $ of reinvestment is > 0 for the reallocated arm vs current, and no guardrail is breached beyond its pre-set tolerance.
- **Power**: compute the minimum detectable effect from historical variance of theo per player (internal); theo, not actual win, as the outcome to reduce variance; CUPED-style pre-period covariate adjustment.
- **Confounders and controls**: holidays (Golden Week, CNY), concerts and events, competitor promotions, visa and travel policy changes, hold. Randomisation handles most of these; property-level events need stratified timing.
- **Alternatives where randomisation is infeasible**: geo/property stepped-wedge rollout with DiD; matched comparison (propensity on pre-period theo); interrupted time series with forecast counterfactual; uplift modelling **only after** an RCT produces labels.
- **Comp-room test**: randomise the comp-room vs alternative-reward choice on forecast high-occupancy nights; measure displaced cash revenue (from RM system) and gaming response.
- **Costs**: forgone revenue in reduced arms (bounded by the holdout share), analyst and CRM time, host-communication risk.
- **Where causal identification is impossible**: from public data alone, at any level; for VIP and premium players with very small n, use case-based judgement.

### 8.7 Forecast evaluation (supporting)

Any forecast used as a counterfactual (e.g., property-level visitation) is evaluated out-of-sample with rolling origin; report MAPE/MASE against a seasonal-naive benchmark. If it does not beat seasonal-naive, it is not used.

---

## 9. Framework for transferring external case-study lessons to Sands

### 9.1 Reasoning chain (one per transferable approach)

```
External operator's problem → Analytical method → Decision changed → Measured outcome (+ evidence grade)
→ Relevant Sands problem → Macau-specific adaptation → Proposed Sands decision
→ Expected economic mechanism → Validation requirement
```

Worked skeleton (to be completed with verified facts in T14):

| Link | Content (draft) |
|---|---|
| External problem | Harrah's: offers to regional players were not tied to measured response (`[SECONDARY ✔]` via Loveman 2003) |
| Method | Segment-level offers tested against control groups |
| Decision changed | Offer value and design by segment |
| Outcome | Company-reported improvements (E3); magnitude to verify |
| Peer-reviewed counterweight | Lucas et al.: established players are often insensitive to free play (E2) |
| Sands problem | Increased reinvestment since 2Q25; share up, margin down (`[SECONDARY ✔]`) |
| Macau adaptation | Table-dominated mass, host-driven relationships, PDPA data limits, inbound mainland visitors with travel constraints, RG obligations |
| Proposed decision | Randomised reinvestment holdout and reallocation pilot at 1–2 properties |
| Mechanism | Remove non-incremental reinvestment; redeploy to cells with positive mROI |
| Validation | §8.6 |

### 9.2 Decision matrix columns (Deliverable A, Table 5)

`approach | external evidence & source | evidence grade | relevant Sands property/segment | decision owner | required data | business KPI | financial mechanism | implementation complexity (L/M/H) | key risks & regulatory constraints | public-data feasibility | potential for measurable incremental value | transferable? (Yes / With adaptation / No) + reason`

Rows at minimum: (1) control-group offer testing; (2) free-play right-sizing; (3) lapsed/new-player targeted reactivation; (4) total-guest-value room allocation; (5) dynamic cash room pricing; (6) demand-based labour scheduling; (7) cross-property itinerary offers (shows, F&B); (8) non-gaming cross-sell personalisation.

### 9.3 Macau transfer filters (each approach must pass or be adapted)

1. **Game mix**: US evidence is slot-heavy; Macao mass is baccarat-heavy. Rated table play needs card-in rates; how much play is unrated is a key uncertainty.
2. **Customer origin**: mostly mainland visitors with travel-permit constraints; visitation is less elastic to offers than for local regional players.
3. **Distribution**: post-junket environment; role of hosts and premium-mass agents (legal status under current law `[TO-VERIFY]`).
4. **Data privacy**: Macau PDPA (Law 8/2005) consent, purpose limitation and cross-border transfer rules govern customer analytics and data shared with a US parent `[TO-VERIFY]`.
5. **Regulatory**: DICJ rules on promotions, credit and responsible gambling; experiments must not increase harm for at-risk players (ethics review).
6. **Concession obligations**: non-gaming investment commitments; government sensitivity to "pure gaming" promotional competition.
7. **Competitive response**: Cotai's six concessionaires react to each other's reinvestment, so an RCT measures customer response, not the market equilibrium. Note this explicitly.

---

## 10. Proposed report outline and principal figures/tables

### 10.1 Deliverable A — Independent Research Report (8–12 pages)

| § | Section | Pages | Principal figures / tables |
|---|---|---|---|
| 1 | Executive summary | 1 | Box: decision, evidence, recommendation, test |
| 2 | The decision and why now | 0.75 | F1: Sands mass share vs adjusted property EBITDA margin, quarterly 2023–3Q26 |
| 3 | Macau competitive environment | 1 | F2: GGR by segment 2023–2026; T1: operator comparison (comparable definitions only) |
| 4 | What comparable operators teach | 1.5 | T2: case register summary with evidence grades |
| 5 | Sands financial analysis | 2 | F3: property EBITDA bridges; F4: revenue-category mix by property; F5: hotel occupancy/ADR by property; T3: decomposition (observable vs unobservable) |
| 6 | Transferability assessment | 1 | T4: reasoning chains; T5: decision matrix |
| 7 | Quantitative decision framework | 1.5 | F6: break-even multiple vs τ and v; F7: scenario comparison; F8: tornado sensitivity |
| 8 | Recommended next action | 0.75 | T6: action / owner / mechanism / metric / threshold / timeline |
| 9 | Risks, limitations, what cannot be concluded | 0.75 | T7: competing explanations and status |
| 10 | References | 1 | Full source register extract |

### 10.2 Deliverable B — Two-page executive brief

Page 1: the question, why it matters now (3 verified facts), what the public evidence shows (2–3 findings with explicit limits). Page 2: the proposed reallocation pilot and test design (one diagram), expected value range (illustrative, labelled), the internal data needed, and a 2-line author note about independent research using public information.
**Tone rules**: "an option management could evaluate", never "Sands should have…"; no assertion of poor management; no internal knowledge implied; no logos or brand impersonation.

### 10.3 Deliverable C — Reproducible materials (see §11)

### 10.4 Deliverable D — Interview preparation

8 questions, each with a 120–200-word evidence-based answer and its source IDs. Required topics:
1. "Couldn't the margin decline simply be the Londoner ramp or bad hold?"
2. "Why theo instead of actual win?"
3. "How do you know free play isn't incremental at Sands specifically?"
4. "Walk me through why break-even is ~2× and not 1×."
5. "How would you size the holdout without hurting revenue?"
6. "What if competitors respond to a pull-back?"
7. "What does Macau privacy law change about your plan?"
8. "What would make you change your recommendation?"

---

## 11. Implementation and reproducibility plan

### 11.1 Repository layout

```
research/
  RESEARCH_SPEC.md              # this file
  work.json                     # task registry (frontier)
  requirements.json             # independent acceptance requirements
  sources/source_register.csv   # every source, verified status
  sources/case_register.csv     # §5.2 template
  sources/search_log.csv
  data/raw/                     # downloaded filings (gitignored if licence unclear; hashes committed)
  data/processed/               # tidy CSVs: operator_quarter.csv, property_quarter.csv, market_quarter.csv
  data/metric_dictionary.csv
  model/assumptions.yaml        # every parameter with source or ILLUSTRATIVE tag
  analysis/                     # Python scripts (extract, decompose, scenario, figures)
  tests/                        # unit tests for formulas and data integrity
  outputs/figures/, outputs/tables/
  deliverables/A_report.md, B_brief.md, D_interview.md (+ PDF exports)
```

### 11.2 Engineering rules

- Python ≥ 3.11; pinned `requirements.txt`; one command (`make all` or `python -m research.analysis.run_all`) regenerates every figure and table from `data/processed`.
- Every processed number traces to `source_id` + page. Tests fail if any processed row lacks `source_id`.
- Illustrative parameters cannot leak into "actual" tables: tests assert that `ILLUSTRATIVE` values appear only in scenario outputs.
- Work runs under the repository's AI-native workflow: a task contract per backlog item, deterministic gates, and independent review before any task is marked PASS (see `AGENTS.md`).

---

## 12. Potential findings, competing explanations and limitations

### 12.1 Plausible findings (to be confirmed or rejected, not presumed)

| Possible finding | What would support it | What would contradict it |
|---|---|---|
| F-a: Share gains are being "bought" at a declining marginal return | H2 ratio falling; peer margins stable | Ratio stable; peers' margins fell similarly |
| F-b: Margin pressure is concentrated at specific properties | H3 heterogeneity | Uniform compression |
| F-c: Reinvestment is a rational strategic investment with long-term value (share, Londoner ramp, customer base) | Rising visitation and share while EBITDA recovers q/q (e.g., 2Q26 $430m → 3Q26 $529m `[SECONDARY ✔]`) | Persistent EBITDA decline with flat share |
| F-d: Public data cannot distinguish F-a from F-c | Likely outcome for parts of the analysis | — |

### 12.2 Competing explanations for margin decline (each must be addressed)

1. Hold variance (rolling and premium mass) — use hold-normalised figures.
2. Premium-segment weakness (management's Q3 2026 explanation) — segment mix decomposition.
3. Londoner ramp-up costs and room inventory return.
4. Labour and opex inflation (reported "opex surge" `[SECONDARY ✔]`).
5. Competitor promotional intensity (market-wide reinvestment war).
6. Satellite casino closures and redistribution of mass play `[TO-VERIFY timing]`.
7. Visitor-mix changes (origin, length of stay, per-capita spend).
8. Accounting changes or reclassification between categories.

### 12.3 Limitations (stated in the report)

- No customer-level, offer-level or cost-by-channel data. Incrementality cannot be estimated from public data.
- Few operators (n = 6) and short post-period (~6 quarters).
- Definition differences across operators and between IFRS and US GAAP.
- External evidence is largely US and slot-based; transfer uncertainty is high.
- Management commentary is self-reported (E3).

---

## 13. Quality assurance and evidence-verification checklist

- [ ] Every number in A, B and D has a `source_id`, page/table reference and evidence label.
- [ ] No `[SECONDARY ✔]` or `[TO-VERIFY]` claim remains in A or B; all upgraded to `[PRIMARY ✔]` or removed.
- [ ] Every illustrative number is labelled "illustrative, not a Sands figure".
- [ ] GGR, net revenue, contribution, EBITDA and cash flow are never conflated; glossary present.
- [ ] Periods, currencies and accounting bases are stated on every table and figure.
- [ ] Cross-operator comparisons use matched definitions or are labelled "directional".
- [ ] No causal language ("caused", "drove", "proved") without an E1 design. Public-data DiD is described as "consistent with".
- [ ] Every case study has an evidence grade and a "what it does not show" note.
- [ ] Competing explanations in §12.2 are each addressed explicitly.
- [ ] Tone check on B: no accusation, no lecturing, no implied internal access, no Sands branding.
- [ ] `make all` regenerates all figures from a clean clone; tests pass.
- [ ] 100% of headline figures and a random 20% of others re-extracted from primary sources with zero unresolved mismatches.
- [ ] Recommendation names action, owner, mechanism, metric, threshold and timeline.
- [ ] Internal-data requirements are listed separately from public findings.

---

## 14. Milestones and step-by-step execution tasks

Data class: **PUB** = completable from public data; **INT** = requires Sands internal data (specified, not executed); **HUM** = requires a human decision or action.

### Milestones

| Milestone | Tasks | Exit condition |
|---|---|---|
| M1 Sources and data foundation | T01–T07 | Source register complete; primary filings collected; regulation brief done |
| M2 Public financial analysis | T08–T12 | Processed datasets + decomposition + share/margin panel, all tests passing |
| M3 Economics, scenarios, transfer | T13–T17 | Model with sensitivity; reasoning chains; decision matrix |
| M4 Validation design and internal-data spec | T18–T20 | Experiment protocol and data request |
| M5 Deliverables and QA | T21–T26 | A, B, C, D complete; QA checklist passed; human sign-off |

### Task cards

**T01 — Set up research workspace** (PUB)
- Inputs: §11 layout.
- Procedure: create directories, CSV templates (source, case, search log, metric dictionary), `assumptions.yaml` skeleton, pinned requirements, test scaffold.
- Output: committed skeleton; `pytest`/unittest runs green on empty data.
- Dependencies: none.
- Completion: templates match §5.2, §6.3 and §7.1 column specs exactly; tests run.

**T02 — Source acquisition: Sands China and LVS filings** (PUB)
- Inputs: §6.1; HKEXnews; LVS 8-K exhibits.
- Procedure: download LVS quarterly earnings releases Q1 2023–Q3 2026 and Sands China annual/interim reports 2024–2026; hash; register.
- Output: `data/raw/*` hashes + `source_register.csv` rows.
- Dependencies: T01.
- Completion: every quarter Q1 2023–Q3 2026 has a primary LVS release registered; gaps logged with reason.

**T03 — Upgrade spec facts to primary** (PUB)
- Inputs: all `[SECONDARY ✔]` facts in §2, §12.
- Procedure: locate each in a primary document; record value, page and discrepancies.
- Output: `sources/fact_verification.csv` (claim, secondary value, primary value, source_id, page, status).
- Dependencies: T02.
- Completion: 100% of §2 facts resolved to PRIMARY ✔, CORRECTED or UNVERIFIABLE.

**T04 — Peer filings acquisition** (PUB)
- Inputs: §6.1 peers.
- Procedure: collect quarterly releases for Galaxy, Wynn Macau/Wynn Resorts, Melco, MGM China/MGM Resorts and SJM, Q1 2023–Q3 2026.
- Output: registered sources; definition notes per operator.
- Dependencies: T01.
- Completion: each operator has quarterly revenue and EBITDA sources or a documented gap.

**T05 — Market statistics acquisition** (PUB)
- Inputs: DICJ, DSEC, MGTO.
- Procedure: download monthly/quarterly GGR by game, visitor arrivals, hotel occupancy 2019, 2023–2026.
- Output: `data/processed/market_quarter.csv`, `market_month.csv`.
- Dependencies: T01.
- Completion: totals reconcile to DICJ annual figures within rounding.

**T06 — External case-study review** (PUB)
- Inputs: §5 protocol and seed list.
- Procedure: search, extract to the case template, grade, write a "does not show" note.
- Output: `case_register.csv` (≥ 12 cases, ≥ 3 E1/E2), `search_log.csv`.
- Dependencies: T01.
- Completion: stopping rule met; every case has all 10 brief questions answered or marked unknown.

**T07 — Macau context and regulation brief** (PUB)
- Inputs: §6.2 regulations, tourism data, trade press.
- Procedure: summarise gaming tax structure (verify τ and promotional-play tax treatment), concession commitments, PDPA rules on customer analytics and cross-border transfer, promotion and RG rules, satellite closure timing.
- Output: `research/notes/macau_context.md` with citations.
- Dependencies: T05.
- Completion: τ verified with primary legal source or explicitly marked unverified; each constraint linked to a §9.3 filter.

**T08 — Operator-quarter panel** (PUB)
- Inputs: T02, T04, T05.
- Procedure: extract net revenue, EBITDA, margin, hold-normalised figures, mass/VIP GGR where disclosed; compute market shares with documented denominators.
- Output: `data/processed/operator_quarter.csv` + metric dictionary entries.
- Dependencies: T02, T04, T05.
- Completion: data-integrity tests pass (source IDs present, sums reconcile, no duplicate keys).

**T09 — Sands property-level decomposition** (PUB)
- Inputs: LVS property tables.
- Procedure: Method A steps 1–5 per property; flag unobservable components.
- Output: `property_quarter.csv`; bridge tables; figures F3, F4.
- Dependencies: T02, T03.
- Completion: bridges sum to reported totals; observable/unobservable table produced.

**T10 — Hotel KPI analysis and comp-room opportunity frame** (PUB)
- Inputs: property occupancy, ADR, RevPAR (if disclosed); market occupancy.
- Procedure: occupancy and ADR trends by property; identify high-occupancy periods; parameterise P(sellout) ranges for §8.3.
- Output: figure F5; assumption entries for OC_room.
- Dependencies: T09, T05.
- Completion: P(sellout) ranges documented with source or ILLUSTRATIVE label.

**T11 — Net-to-gross proxy for deductions** (PUB)
- Inputs: gaming volumes and win rates, net casino revenue.
- Procedure: compute implied gross win vs reported net casino revenue per property-quarter; analyse the gap trend before and after 2Q25.
- Output: proxy series + caveat note (it contains commissions, discounts and comps allocation, not just promotions).
- Dependencies: T09.
- Completion: method validated on at least one period where the company disclosed deductions, or labelled unvalidated.

**T12 — Share–margin trade-off and quasi-experimental analysis** (PUB)
- Inputs: T08.
- Procedure: H1/H2 tests; DiD and synthetic control per §8.5 with robustness and placebo checks.
- Output: figure F1, regression/synthetic-control tables, written interpretation stating identification limits.
- Dependencies: T08, T07.
- Completion: every competing explanation in §12.2 is addressed in the write-up; no causal language.

**T13 — Unit-economics model** (PUB + ILLUSTRATIVE)
- Inputs: §8.3; τ from T07; T10 parameters.
- Procedure: implement ΔΠ, k*, OC_room and mROI functions with unit tests.
- Output: `analysis/economics.py`, tests, figure F6.
- Dependencies: T07, T10.
- Completion: tests cover edge cases (τ = 0, full occupancy, zero response); k* matches the closed form.

**T14 — Transfer reasoning chains** (PUB)
- Inputs: T06, T07, T09.
- Procedure: complete the §9.1 chain for each candidate approach; apply §9.3 filters.
- Output: table T4.
- Dependencies: T06, T07, T09.
- Completion: ≥ 6 chains; each has evidence grade, Macau adaptation and verdict.

**T15 — Decision matrix** (PUB)
- Inputs: T14.
- Procedure: fill §9.2 columns; score transparently.
- Output: table T5.
- Dependencies: T14.
- Completion: every row has all columns; "not transferable" rows are explained.

**T16 — Scenario and sensitivity model** (PUB + ILLUSTRATIVE)
- Inputs: T13, T12 anchors.
- Procedure: implement §8.4 response curves, equimarginal allocation, four scenarios, tornado chart and two-way grids.
- Output: F7, F8; `scenario_results.csv` marked ILLUSTRATIVE.
- Dependencies: T13, T12.
- Completion: sign-flip assumptions identified; tests confirm the equimarginal property and that no illustrative value is in actual tables.

**T17 — Recommendation drafting** (PUB)
- Inputs: T12, T15, T16.
- Procedure: write the action / owner / mechanism / metric / threshold / timeline table and alternatives.
- Output: table T6.
- Dependencies: T12, T15, T16.
- Completion: passes the §13 recommendation-specificity check.

**T18 — Experiment protocol** (PUB design, INT execution)
- Inputs: §8.6.
- Procedure: write the pre-registration-style protocol: arms, strata, metrics, guardrails, threshold, power method, ethics/RG safeguards, analysis plan.
- Output: `research/deliverables/experiment_protocol.md`.
- Dependencies: T13, T07.
- Completion: an independent reviewer can compute the MDE given variance inputs; all guardrails have numeric tolerances or explicit placeholders.

**T19 — Internal-data requirements specification** (INT)
- Inputs: T13, T18.
- Procedure: list required internal tables (player-trip theo, offers issued/redeemed, comp rooms by night, RM forecasts, labour by outlet, host assignments), grain, history and privacy handling.
- Output: `research/deliverables/internal_data_request.md`.
- Dependencies: T18.
- Completion: each item maps to a hypothesis or metric; PDPA handling noted.

**T20 — Holdout analysis code on synthetic data** (PUB, synthetic)
- Inputs: T18.
- Procedure: simulate player-level data **clearly labelled synthetic**; implement the analysis pipeline (CUPED, stratified estimate, guardrails, CI) so it is ready for internal data.
- Output: `analysis/holdout_analysis.py` + tests; demo output labelled SYNTHETIC.
- Dependencies: T18.
- Completion: the pipeline recovers the known simulated effect within its CI in ≥ 90% of simulation runs.

**T21 — Deliverable A draft** (PUB)
- Inputs: T09–T19.
- Procedure: write per §10.1.
- Output: `deliverables/A_report.md` + PDF.
- Dependencies: T17, T18, T19.
- Completion: 8–12 pages; all figures F1–F8 and tables T1–T7 present.

**T22 — Evidence QA pass** (PUB)
- Inputs: A draft, source register.
- Procedure: run the §13 checklist; automated re-extraction of headline figures; scan for prohibited causal and accusatory language.
- Output: `qa/qa_report.md`.
- Dependencies: T21.
- Completion: zero unresolved checklist items.

**T23 — Deliverable B brief** (PUB)
- Inputs: final A.
- Procedure: write per §10.2.
- Output: `deliverables/B_brief.md` + PDF (2 pages).
- Dependencies: T22.
- Completion: ≤ 2 pages; tone rules pass; all numbers trace to A.

**T24 — Deliverable D interview prep** (PUB)
- Inputs: A, model.
- Procedure: answer the §10.4 questions with source IDs.
- Output: `deliverables/D_interview.md`.
- Dependencies: T22.
- Completion: 8 Q&As; each cites ≥ 1 source or model output.

**T25 — Reproducibility check** (PUB)
- Inputs: repository.
- Procedure: fresh clone → one command → compare outputs by hash.
- Output: reproducibility log.
- Dependencies: T21.
- Completion: identical figures and tables; tests green in CI.

**T26 — Human review and send decision** (HUM)
- Inputs: B, A, QA report.
- Procedure: the author reviews tone and accuracy and decides whether, when and how to share with the recruitment contact.
- Output: decision record.
- Dependencies: T22, T23, T24, T25.
- Completion: explicit human approval; nothing is sent automatically.

---

## 15. Acceptance criteria for the completed research

The research is complete only when **all** of the following hold:

1. **Decision clarity**: Deliverable A answers the nine management questions of the brief (§8 of the brief), each in an identifiable subsection.
2. **Evidence integrity**: the §13 checklist passes with zero open items; every significant claim is `[PRIMARY ✔]` or explicitly marked as unverifiable.
3. **Economic correctness**: the report computes break-even and contribution after gaming tax and opportunity cost, using the glossary definitions consistently.
4. **Honest identification**: public-data analyses are described as descriptive or quasi-experimental with stated limits; causal claims rest only on E1 evidence or on the proposed internal test.
5. **Actionability**: the recommendation specifies action, owner, mechanism, metric, success threshold and timeline. It survives the "what would change your mind" test (§10.4 Q8).
6. **Transfer discipline**: each external approach carries an evidence grade, a Macau adaptation and a transferable / adapt / not-transferable verdict.
7. **Reproducibility**: one command regenerates all quantitative outputs from committed processed data; CI passes.
8. **Tone and boundaries**: Deliverable B passes the tone rules; no implied affiliation, internal access or endorsement.
9. **Separation of public and internal**: internal-data needs appear only in the data request and the experiment protocol, never as findings.

---

## Prioritized execution backlog

Ordered for an AI research or coding assistant to start immediately. Machine-readable version: [`research/work.json`](work.json).

| Priority | Task | Class | Depends on | Why now |
|---|---|---|---|---|
| 1 | T01 Workspace setup | PUB | — | Unblocks everything |
| 2 | T02 Sands/LVS filings | PUB | T01 | All findings rest on these |
| 3 | T03 Upgrade spec facts to primary | PUB | T02 | De-risks the selected decision itself |
| 4 | T05 Market statistics | PUB | T01 | Share denominators |
| 5 | T04 Peer filings | PUB | T01 | Peer counterfactual |
| 6 | T07 Macau context and tax verification | PUB | T05 | τ drives the economics |
| 7 | T06 Case-study review | PUB | T01 | Can run in parallel with T02–T05 |
| 8 | T08 Operator-quarter panel | PUB | T02, T04, T05 | |
| 9 | T09 Property decomposition | PUB | T02, T03 | |
| 10 | T10 Hotel KPIs / comp-room frame | PUB | T09, T05 | |
| 11 | T11 Net-to-gross proxy | PUB | T09 | |
| 12 | T12 Share–margin analysis | PUB | T08, T07 | Tests H1/H2 |
| 13 | T13 Unit economics | PUB | T07, T10 | |
| 14 | T14 Transfer chains | PUB | T06, T07, T09 | |
| 15 | T15 Decision matrix | PUB | T14 | |
| 16 | T16 Scenarios and sensitivity | PUB | T13, T12 | |
| 17 | T18 Experiment protocol | PUB/INT | T13, T07 | |
| 18 | T17 Recommendation | PUB | T12, T15, T16 | |
| 19 | T19 Internal data request | INT | T18 | |
| 20 | T20 Holdout code (synthetic) | PUB | T18 | |
| 21 | T21 Report A | PUB | T17, T18, T19 | |
| 22 | T22 Evidence QA | PUB | T21 | |
| 23 | T23 Brief B | PUB | T22 | |
| 24 | T24 Interview prep D | PUB | T22 | |
| 25 | T25 Reproducibility check | PUB | T21 | |
| 26 | T26 Human review and send decision | HUM | T22–T25 | Outward-facing; human only |
