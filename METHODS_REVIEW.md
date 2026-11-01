# Methods review: Hart and Tirole (1990)

- **Paper.** Oliver Hart and Jean Tirole, "Vertical Integration and Market Foreclosure," *Brookings Papers on
  Economic Activity: Microeconomics* 1990, pp. 205–286. The article runs pp. 205–276 (including Appendixes A to F);
  comments by Dennis W. Carlton (pp. 277–280) and Oliver E. Williamson (pp. 280–283) and a general discussion
  (pp. 283–284) follow, with references on pp. 285–286.
- **Statistical focus.** (1) The ex post monopolization result of Propositions 1 and 2 (pp. 221–224), that
  integration lets a low-cost supplier restrict output it could not restrict under secret contracts, with the
  linear example in footnote 24 (p. 239); and (2) the cement application (pp. 249–252), whose descriptive figures,
  drawn from a 1966 FTC report and from Allen (1971), are used to argue that the "scarce needs" variant fits the
  1960s merger wave.
- **Review standard.** For the formal part, internal consistency, how explicitly the assumptions are stated, and
  whether the predictions can be tested. For the applications, standard reporting of sources, sample construction
  and uncertainty for the descriptive statistics quoted.
- **What was read.** The full published text, including comments and discussion, from the PDF posted by the
  Brookings Institution (brookings.edu, file `1990_bpeamicro_hart.pdf`, a scanned and text-extracted copy). Some
  displayed equations did not survive text extraction, so equation-level details are reported only where the
  surrounding prose or a legible line states them. The FTC report and Allen (1971) were not read; figures from them
  are recorded as the paper reports them. Author background comes from the authors' pages at nobelprize.org.

## Methods summary

The paper is a deductive model of a vertical chain with two upstream suppliers (U1, U2) and two downstream firms
(D1, D2) that sell perfect substitutes. Upstream firms produce at constant marginal cost c_i; downstream firms
transform the input one-for-one at zero cost and, given the quantities they hold, end up at the Cournot outcome.
Contracts between upstream and downstream firms are bilateral and secret, and may be general (two-part tariffs
and conditional contracts are allowed). Following Grossman and Hart (1986), vertical integration is modeled as
profit sharing between the merged units (Assumption 1), at a fixed cost E (Assumption 2); only U_i can merge with
D_i (Assumption 3); integration is irreversible (Assumption 4); and rivals can respond immediately (Assumption 5).
The game has an ex ante stage (integration, then industry-specific investment or exit) and an ex post stage (costs
revealed, contract offers, acceptance, production, product-market competition).

Three variants are solved. In ex post monopolization (Bertrand competition upstream), nonintegration yields
Cournot output 2q*(c1) and integration of the low-cost pair yields lower output with a partial foreclosure of D2,
which is still supplied at the rival's cost c2 (Proposition 2, "price squeeze"). Extensions add cost uncertainty
and investment (Propositions 5 to 10), giving the prediction that the more efficient upstream firm integrates and
that bandwagoning can follow. In scarce needs and scarce supplies (bargaining between stages, Propositions 11 to
20), integration redirects trade to the merging partner and can induce exit of a rival (ex ante monopolization).
Table 1 (p. 212) summarizes the variants. A section on applications discusses cement and ready-mixed concrete in
the 1960s, airline computer reservation systems, and the St. Louis Terminal Railroad case.

## Research design

Theoretical, with illustrative case discussions. The formal results are equilibrium characterizations; the case
studies are narrative and rely on secondary sources. The paper says plainly (p. 249) that the case discussion "is
only meant to suggest" how the industries might be analyzed and that the evidence was not collected with the model
in mind. There is no hypothesis test.

## Sampling strategy

Does not apply to the formal results. For the applications, the three industries are chosen for illustration; no
selection rule is stated, and the cement figures are those reported in the FTC inquiry and in Allen (1971) and
Wilk (1968), which the paper did not re-collect.

## Sample size

Does not apply to the model (two firms per stage; the text notes, footnote 7, that the model could be generalized).
For cement, the counts reported are 55 vertical acquisitions (p. 250) and 22 metropolitan areas with ready-mix
concentration data (p. 249). Neither sample is described beyond its count.

## Inclusion and exclusion criteria

For the model, the scope conditions do this work, and they are stated: homogeneous downstream products, constant
returns upstream in the first two variants and capacity constraints in the third, no contingent forward contracts,
secret offers, no horizontal mergers, and upstream costs high enough that downstream firms end at the Cournot
outcome. For the cement figures, the criteria by which the FTC counted acquisitions, markets or "above-average
excess capacity" are not reported in the paper.

## Independent and dependent variables

In the model, the exogenous elements are the cost distributions F_i, investment costs I and J, the integration cost
E, the bargaining shares, and capacities; the outcomes are industry structure (NI, PI, FI or exit), output, prices,
and profits. In the cement application, the implied explanatory variable is excess cement capacity (utilization
94% in 1955, 74% in 1960) and the outcome is the timing and direction of vertical acquisitions.

## Statistical methods

None in the empirical sense. The formal methods are equilibrium analysis of a multi-stage game with proofs in
Appendixes A to F, including a uniqueness argument for the first variant (Appendix B), an analysis of exclusive
dealing (Appendix C) and a war-of-attrition and preemption model (Appendix E). The applications use descriptive
percentages and counts quoted from other sources.

## Reported effect sizes

The formal results are mostly signs and orderings (for example, q1* + q2* < 2q*(c1) when c1 < c2). The one
numerical illustration is footnote 24: with p = a − bQ, monopoly output (a − c)/2b and duopoly output (a − c)/3b per
firm, total surplus 3/8 (a − c)²/b − I1 − E after merger and exit against 4/9 (a − c)²/b − I1 − I2 under duopoly.
For cement, the reported magnitudes are descriptive (listed in the table below).

## Confidence intervals

None are reported, and none would apply to the formal results. The cement statistics are reported without any
indication of sampling or measurement error.

## P-values, if applicable

Not applicable. No hypothesis is tested statistically.

## Missing data treatment

Not discussed. For cement, the paper reports state-level concentration as a share of states and ready-mix
concentration for the 22 metropolitan areas "for which the FTC had data" (p. 249), which implies other areas were
missing, without saying how many or why.

## Stated limitations

The authors state that the costs of integration are represented only by a fixed amount E rather than modeled
(p. 207); that Assumption 1 is "extreme" (footnote 13); that Assumption 3 rules out extortion (footnote 15); that
irreversibility (Assumption 4) is restrictive where conditions change and that cyclical integration is left for
future work (p. 219); that the simplifying condition 5 in the scarce supplies variant "will fail to be satisfied in
many markets" (p. 240); that clear-cut antitrust prescriptions are hard to deliver (p. 213); and that the
applications are only suggestive (p. 249). In the cement case they note that one prediction of the scarce needs
model, all supplies coming from the internal supplier, is not borne out, since acquired firms still bought from
other cement producers (p. 251), and that holdup-based efficiency motives were not ruled out (p. 252).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Output under nonintegration | 2q*(c1), Cournot output at cost c1 | Proposition 1, pp. 221–222 | Total input sold when a low-cost supplier contracts secretly with both downstream firms | That real contracts are secret or that firms play Cournot downstream |
| Output under partial integration | q1* + q2* < 2q*(c1) when c1 < c2 | Proposition 2 and Figure 1, pp. 222–224 | The output contraction (ex post monopolization) from integration by the low-cost pair | The size of the contraction in any industry |
| Transfer to the foreclosed rival | t2* = c2 q2* | Proposition 2, equation 2, p. 222 | The price squeeze: D2 is still supplied, at the rival supplier's cost | That integrated firms actually sell to rivals at such prices |
| Linear example, outputs | q^m = (a − c)/2b; q* = (a − c)/3b per firm | Footnote 24, p. 239 | Monopoly versus duopoly output with linear demand | Welfare in other demand systems |
| Linear example, total surplus | 3/8 (a − c)²/b − I1 − E (merger with exit) vs. 4/9 (a − c)²/b − I1 − I2 (duopoly) | Footnote 24, p. 239 | That merger with exit can raise total surplus when I2 is large and E small | That such mergers are common or that investment costs are of that size |
| Efficient firm's integration incentive | G(F1, F2) > G(F2, F1) | Proposition 5, pp. 226–227 | The more efficient supplier (first-order stochastic dominance) gains more from integrating | A measured cost ranking of real merging firms |
| Cement shipping distance | 90% shipped 160 miles or less | p. 249, citing FTC Report p. 7 | The geographic reach of cement markets in the 1960s | Today's market boundaries |
| State cement concentration | Top four held < 50% in only 6% of states | p. 249 | Upstream concentration at the state level | Concentration in the true (sub-state or multi-state) markets |
| Ready-mix concentration | Top four ≥ 50% in 17 of 22 metro areas; ≥ 75% in 8 | pp. 249–250, citing FTC Report p. 3 | Downstream concentration in areas with FTC data | Concentration in the areas without data |
| Cement utilization | 94% (1955); 74% (1960) | p. 250, citing FTC Report table III-3 | The swing from tight to slack upstream capacity | That excess capacity caused the mergers |
| Capacity growth | +60% from 1955 to 1965, twice the growth of shipments | p. 250, citing the Wall Street Journal, March 29, 1965 | Scale of the capacity build-up | Plant-level costs or efficiency |
| Timing of acquisitions | 80% in weak market conditions; 37 of 55 in markets with above-average excess capacity | p. 250, citing FTC Report p. 100 and Allen (1971) | Coincidence of acquisitions with slack capacity | A causal effect, or what share of non-acquiring markets also had slack |
| Acquired ready-mix firms' market shares | 19% to 45% of sales in their market areas | p. 250, citing FTC Report p. 14 | That targets were large downstream firms | That the acquisitions raised concrete prices |
| Purchases from parent | 37% before, 69% after acquisition | p. 251, citing FTC Report p. 14 | Redirection of input purchases toward the integrated supplier | Whether rivals were harmed or exited |
| CRS booking fees, 1981–82 | $0.24 (Eastern), $1.32 (Delta), $2.00 (New York Air) per Sabre booking | p. 253, citing CCH Trade Regulation Reports | Price discrimination by an integrated reservation system | Effects on fares or on rival airlines' traffic |

## Interpretation notes

- The central formal claim, that secret bilateral contracting prevents an upstream monopolist from committing to
  the monopoly output, is clearly stated and proved under explicit assumptions. Its reach depends on two of them:
  that offers are secret, and that integration means full profit sharing. Both are acknowledged in the text.
- The paper's three variants make different predictions about who is harmed (Table 1). The cement discussion
  selects the scarce needs variant mainly because the complaining firms were cement producers and capacity was
  slack. The authors themselves describe the evidence against ex post monopolization as "circumstantial"
  (footnote 39). The variant choice is an interpretation, not a test.
- The cement figures are secondary and descriptive. They establish that acquisitions coincided with slack capacity
  and that acquired firms bought more from their parents. They do not establish that foreclosure raised prices or
  reduced output, which is the welfare-relevant question.
- Williamson's comment (pp. 281–282) questions whether cement met the model's concentration and entry conditions
  and whether the downstream bottleneck was binding; Carlton (p. 280) asks whether two-part tariffs and the cost
  asymmetries central to the model were present in any of the cases. These are published objections in the same
  volume, not documented errors.
- Reporting issues are separate from analytical ones. No analytical error in the formal results is documented in
  the sources read here. The reporting gaps are in the applications: sample definitions, the denominator behind
  "6 percent of the states," and the classification behind "above-average excess capacity" are not given.
- The modern rerun in this repository uses public 2002–2023 data on kiln ownership, utilization and prices. It
  checks the conditions and timing the cement discussion relies on and tests whether consolidation of kiln
  ownership moved prices; it does not reproduce the paper's figures and cannot observe vertical integration.

## Unanswered questions

- How large is the output effect of integration outside the linear Cournot case, and how sensitive is it to
  observable (public) contract terms?
- How did the FTC define cement markets and "above-average excess capacity," and how many markets without
  acquisitions also had slack capacity?
- Did the 1960s acquisitions change concrete or cement prices, quantities or entry? (Hortaçsu and Syverson, 2007,
  later addressed this with Census plant data and found prices fell and quantities rose as markets became more
  integrated.)
- Were two-part tariffs and secret discounts actually used in cement supply contracts of the period?
- Did the reluctant bandwagoning described in executives' statements lead to full integration in any market, and
  did non-integrated cement producers exit?

## Items requiring expert verification

- The exact statements of Propositions 2, 5 and 13 to 20, whose displayed equations were partly lost in text
  extraction from the scanned copy; an expert should confirm the conditions against a clean printed copy.
- The FTC Report (1966) page and table references (p. 3, p. 7, p. 14, p. 100, table III-3) as cited by the paper,
  which were not checked against the report.
- Whether later work (for example, the published comments on the secret-contracting assumption by subsequent
  authors) identifies conditions under which Proposition 1's Cournot outcome fails, such as alternative beliefs
  of downstream firms about rivals' contracts.
- The characterization of the St. Louis Terminal Railroad case (224 U.S. 383, 1912) as quoted from Areeda and
  Hovenkamp (1987).
