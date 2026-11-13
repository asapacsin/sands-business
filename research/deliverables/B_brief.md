---
title: "Measuring the Return on Mass-Market Reinvestment in Macao"
subtitle: "Two-page research brief — independent analysis of public information"
date: "November 2026"
---

**About this brief.** I prepared this independently, using only public sources. I have no internal
information and no affiliation with Sands China. It is offered as an example of how I would approach a
commercial question; it does not assess management. The full report, data and code are available on request.
*Evidence tags:* **[P id]** primary filing or statistic; **[D]** derived by me from primary data;
**[I]** illustrative, not a Sands figure; **[U id]** unverified (call transcript, press, or research seen only as
abstract/metadata). IDs refer to the project's source register.

### The question

According to its Q2 2025 earnings call, Sands China raised mass-market customer reinvestment from late
April 2025 to rebuild share, with the level to be "market sensitive" (management, verbatim) **[U TR-LVS-2025Q2]**. The open
question for any operator in that position is a **marginal** one: does the next dollar of reinvestment
create more than it costs once Macao's ~40% gaming tax is paid **[U PR-TAX-2022]**? And which properties
and customer groups should receive it?

### What the public data shows (2Q25–3Q26 vs 3Q23–1Q25)

- **Share recovered.** Sands' share of Macao GGR rose from 22.4% (1Q25) to 25.4% (3Q26) **[D from P LVS-ER, DICJ-Q]**.
  A broker note cites 25.4% for 3Q26 **[U BRK-CLSA-2026Q3]**.
- **Reinvestment rose.** The share of gross gaming win not booked as casino revenue (rebates, discounts,
  comps and commissions) rose from 20.5% to 23.5%, roughly US$226m a year **[D]**. This is a proxy, not
  an internal ledger.
- **Margins compressed, partly across the market.** On a *directional* comparison (peer definitions
  differ: EBITDA vs EBITDAR), Sands' five-property margin fell 4.2 points while Wynn, MGM and Melco moved
  by −2.6 to +0.2 points **[D from P LVS-ER, WYNN/MGM/MELCO-ER]**. Sands' 3Q26 five-property margin of 27.8%
  (27.3% including ferry and other operations **[P LVS-ER-2026-10-21]**) is at or above those peers. The
  relative gap of about −2.8 points **[D]** coincides with the Londoner ramp, room renovations and the
  closure of SJM's satellite casinos **[U PR-SATELLITE-2026]**; how much each contributed is my
  inference and cannot be separated with public data.
- **Hotels are full.** Occupancy averaged 98–99% at The Venetian, The Parisian and Sands Macao since 2Q25
  **[P LVS-ER hotel statistics]**, so a complimentary room there usually displaces a paying guest.

### Why the answer needs a test, not a model

Assuming a 40% gaming tax and 10% variable cost, a dollar of reinvestment must create about **$2 of
incremental GGR** to break even, or about $1.2 if promotional play reduces taxable GGR, which needs
confirming **[I]**. Depending on how much of the share gain can be attributed to reinvestment, public data
implies an *average* (not marginal) return between 0.4× and 2.1× of cost **[D + I]**. That range straddles
break-even, so the public numbers cannot settle the question.

Abstracts of peer-reviewed studies on real US casino data report that established players often respond little to changes
in free play **[U LIT-LUCAS-2024, LIT-LUCAS-2020]**, and Harrah's built its marketing around control-group
testing **[U LIT-LOVEMAN-2003]**. Those results come from slot-based US markets and do not transfer
directly to Macao's baccarat-led market, but the testing discipline does.

### A practical next step management could evaluate

| Element **[I: design proposal]** | |
|---|---|
| **Action** | A 12-week randomised holdout: 5–10% of players in each property × mass-tier cell receive a −30% or a reallocated offer, plus a room-comp vs non-room-reward test on forecast sell-out nights |
| **Owners** | Casino Marketing and FP&A; Hotel Revenue Management for the room test; Compliance sign-off |
| **Measure** | Incremental contribution per player = Δtheoretical win × (1 − tax − variable cost) − Δreinvestment − Δroom opportunity cost |
| **Decision rule** | Change a cell's offer only if the 90% confidence lower bound is above zero and guardrails hold: visits, share, complaints, responsible-gambling indicators |
| **Safeguards** | Data processed in Macao on pseudonymised IDs; at-risk players excluded; host-managed premium players reviewed case by case |

If the test shows marginal returns above break-even in most cells, the case for keeping or expanding the
increment becomes evidence-based. If not, the savings can be redirected to the cells that respond.

### What I would need to go further

Player-trip theoretical win, offers issued and redeemed, night-level comp and cash room data, and a
breakdown of net-to-gross deductions. With those, the analysis pipeline, already built and validated on
synthetic data, could produce cell-level estimates within weeks.
