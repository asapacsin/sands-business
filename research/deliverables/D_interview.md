# Deliverable D — Interview preparation

Source IDs refer to `sources/source_register.csv`, `sources/case_register.csv` and `outputs/*.json`.
Tags: [P id] primary; [D] derived; [I] illustrative, not a Sands figure; [U id] unverified secondary (incl. research seen only as abstract).

**1. "Couldn't the margin decline just be the Londoner ramp or bad hold?"**
Partly, yes, and I tried to separate the two. Hold first: LVS discloses the EBITDA effect of normalising
rolling win to 3.3%. On that basis the Macao margin still declined steadily, from 32.1% (1Q25) to 27.2%
(3Q26), so hold explains the 2Q26 spike but not the trend (LVS-ER-2026-07-22, -10-21). The Londoner is
harder. Its room inventory returned in mid-2025, exactly when reinvestment rose, and its margin is roughly
flat across the periods while Venetian, Parisian and Sands Macao fell 6–9 points. That is why I don't call
the −2.8-point gap to peers a reinvestment effect: it is consistent with one, but it is not identified.
The net-to-gross gap rising at four of five properties is the more direct signal (outputs/results.json). [P LVS-ER-2026-07-22, LVS-ER-2026-10-21; D results.json]

**2. "Why use theoretical win instead of actual win?"**
Actual win includes luck. A baccarat player's results over a few weeks can swing far more than any offer
effect. Theo, which is handle times house edge, measures the play the offer is meant to change. In a
holdout with thousands of players per cell, theo shrinks variance enough to detect effects of tens of
dollars per player; actual win often would not. CUPED with pre-period theo shrinks variance further
(analysis/holdout_analysis.py). [D holdout_synthetic_demo.json; I]

**3. "How do you know free play isn't incremental at Sands specifically?"**
I don't, and the report says so. The peer-reviewed evidence (C02–C05) shows that established US slot
players often don't respond to free-play changes. That justifies testing the hypothesis, not assuming it.
Macao is different: baccarat-led, visits constrained by travel, and a 2026 market where every operator was
competing for displaced satellite-casino players. The public data gives an average return range of
0.4–2.1×, which straddles break-even. That is exactly why the recommendation is a test. [U LIT-LUCAS-2024, LIT-LUCAS-2020; D economics.json; U PR-SATELLITE-2026]

**4. "Walk me through why break-even is about 2× and not 1×."**
Gaming tax and levies take about 40% of GGR; assume another ~10% in variable costs such as service, F&B
and labour. Each incremental dollar of GGR therefore leaves about 50 cents of contribution. A $1 promotion
needs $2 of incremental GGR to pay for itself: k* = 1/(1 − 0.40 − 0.10). If promotional play turns out to
reduce taxable GGR, the promotion's net cost is only 60 cents and k* drops to 1.2×. That tax-treatment
question is the first thing I would ask Sands to confirm, if given the opportunity (notes/macau_context.md). [U PR-TAX-2022; I v = 0.10; D economics.json]

**5. "How would you size the holdout without hurting revenue?"**
Cap exposure at 5–10% of each cell for 8 weeks, so at worst you lose part of the incremental theo of a
small fraction of players for two months. Then size by minimum detectable effect, MDE = 2.49·σ·√(1/n_T +
1/n_C). With an illustrative σ of US$500 per player and 2,400 vs 21,600 players, the MDE is about US$27
per player. Sands would plug in its own σ. If a cell is too small, pool similar cells or extend the
duration rather than raise the treated share. [I MDE example; D holdout_analysis.py]

**6. "What if competitors respond to a pull-back?"**
The randomised test measures customer response with competitor behaviour held fixed. It can't measure a
market-wide equilibrium if Sands cut across the board and rivals reacted. I'd handle that by adopting
changes gradually by cell, keeping the share guardrail (company-defined mass share not below its recent
low), and watching peer share each month from DICJ data and peer releases. MGM China's record 17.1% share
in 3Q26 shows rivals were actively competing (C15). [P MGM-ER-2026-10-28; P DICJ-Q]

**7. "What does Macau privacy law change about your plan?"**
Under the Personal Data Protection Act (Law 8/2005), processing needs a clear legal basis, and transfers
outside Macau are restricted. So the customer-level analysis runs in Macao on pseudonymised IDs, and only
aggregate results leave. Responsible-gambling flags are used only to exclude players. Compliance signs off
the offer variation under DICJ rules before anything goes live (deliverables/experiment_protocol.md §8). [U LAW-PDPA]

**8. "What would make you change your recommendation?"**
Three things. If internal data showed the marginal return already above ~2× in most cells, I would
recommend keeping or raising the increment. If promotional play is tax-deductible, break-even is 1.2× and
the current level is more likely profitable. And if the test couldn't be run for compliance or host-relationship
reasons, I would fall back to a staggered property-level rollout analysed with difference-in-differences,
and say clearly that the evidence would be weaker. [D economics.json; I]
