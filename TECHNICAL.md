# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, every test statistic
and how to reproduce the results. All tables are in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Oliver Hart and Jean Tirole, "Vertical Integration and Market Foreclosure," *Brookings Papers on Economic Activity:
Microeconomics* 1990, pp. 205–286 (article pp. 205–276, comments by Dennis W. Carlton and Oliver E. Williamson and
general discussion pp. 277–284). A theory paper with two upstream and two downstream firms, secret bilateral
contracts and incomplete contracts in the sense of Grossman and Hart (1986). Its headline results are qualitative
(Table 1, p. 212), with one worked linear example (footnote 24, p. 239). The application to cement (pp. 249–252)
rests on figures from the FTC's 1966 *Economic Report on Mergers and Vertical Integration in the Cement Industry*.

| Quantity in the paper | Value | Location |
|---|---|---|
| Output, secret contracts vs. merged (linear demand) | 2(a−c)/3b vs. (a−c)/2b | Prop. 1–2; fn. 24 |
| Total surplus, duopoly vs. merger with exit (gross of investment) | 4/9 vs. 3/8 of (a−c)²/b | fn. 24, p. 239 |
| Cement utilization, 1955 and 1960 | 94% and 74% | p. 250 |
| States where top four cement suppliers held < 50% | 6% | p. 249 |
| Cement shipped 160 miles or less | 90% | p. 249 |
| Acquisitions in markets with above-average excess capacity | 37 of 55 | p. 250 |
| Acquired ready-mix firms' purchases from parent | 37% → 69% | p. 251 |

## Headline results

| Test | Estimate | Uncertainty | N |
|---|---|---|---|
| States with top-4 owners below 50%, 2023 (paper: 6%) | 0% | 30 states have four or fewer owners | 34 states |
| States with HHI above 1,800, 2023 | 97.1% | | 34 states |
| Median owners within 160 miles of a kiln, 2010 → 2023 | 4 → 3 | | 91 → 87 plants |
| Median HHI within 160 miles, 2010 → 2023 | 3,558 → 3,770 | | 91 → 87 plants |
| National top-4 share and HHI, 2023 | 45.0%, 831 | | 25 owners |
| Δ relative price on Δ utilization, per 10 points | +0.0118 | SE 0.0039, p = 0.002 | 21 |
| Relative price on utilization (levels), per 10 points | +0.0271 | SE 0.0107, p = 0.011 | 22 |
| District log price on utilization, per 10 points (FE) | −0.0062 | SE 0.0070, p = 0.37 | 438 |
| District log price on HHI, per 1,000 (FE) | −0.0141 | SE 0.0190, CI [−0.051, 0.023] | 287 |
| Same, controlling for utilization | −0.0255 | SE 0.0228, p = 0.26 | 252 |
| Long difference 2010–2023, per 1,000 | +0.0056 | SE 0.0152, CI [−0.024, 0.035] | 16 |

## Data

All files are committed in `data/raw/` and were downloaded on 2026-11-01 by `src/fetch_data.py`.

- `ghgrp_cement_facilities.csv` and `ghgrp_subpart_h_emissions.csv`: EPA Greenhouse Gas Reporting Program,
  Envirofacts tables `PUB_DIM_FACILITY` (NAICS 327310 plus one kiln plant filed under another code) and
  `PUB_FACTS_SUBP_GHG_EMISSION` for subpart H (cement production), 2010–2023. 100 plants, 1,386 plant-years.
- `usgs_myb/cement_myb_YYYY.xls(x)`: USGS Minerals Yearbook cement tables, 2002–2023. Used: Table 5 (clinker
  capacity and production by district), Table 9 (shipments by destination and origin), Table 11 or 12 (portland
  cement shipped by district, with value), Table 14 or 15 (shipments by type of customer).
- `fred_PCU327310327310.csv`, `fred_PCU327320327320.csv`: BLS producer price indexes for cement manufacturing and
  ready-mix concrete manufacturing, monthly from 1965, via FRED.

## Method

Rules fixed before looking at outcomes:

- **Market share.** Each owner's share of subpart H carbon dioxide (gas 1), the kiln process and fuel emissions
  that scale with clinker output. Plant-years with zero kiln CO2, Puerto Rico and the two white-cement plants
  (Lehigh White Cement) are dropped, leaving 1,237 plant-years and 96 plants.
- **Owners.** Parent names as reported, split by reported percentages; spelling variants merged. A parent field
  that is blank or reads "None" falls back to the facility name. Where the reported percentages sum to less than
  100% (two 2010 filings, Continental Cement and Cemex Demopolis, list only a 51% holder), the named owners are
  scaled up to 100% so that no kiln output drops out of the market totals. Legacy names are
  assigned to the acquirer from the first year any of the legacy plants report the acquirer: Lafarge → Holcim (2017),
  Essroc → Heidelberg Materials (2017), Ash Grove → CRH (2018), TXI → Martin Marietta (2014). Texas Lehigh is
  split 50/50 between Eagle Materials and Heidelberg Materials, as its 2021–2023 filings report.
- **Markets.** State of the plant (the FTC instead counted shipments into each state, which public data do not
  record); a 160-mile great-circle radius around each plant; and USGS districts, mapped to
  states, with Texas and Pennsylvania split by county as in USGS Table 2.
- **Concentration.** With shares $`s_{im}`$ in percent for owner $`i`$ in market $`m`$,

```math
\text{HHI}_{m} = \sum_{i} s_{im}^{2}, \qquad \text{CR4}_{m} = \sum_{i \in \text{top 4}} s_{im}
```

- **Utilization and relative price.** National utilization from the USGS "Total" row; the relative price is the
  annual mean of the cement PPI over the annual mean of the ready-mix PPI, normalized to 2002.

```math
u_t = \frac{\text{clinker}_t}{\text{capacity}_t}, \qquad r_t = \frac{\text{PPI}^{\text{cement}}_t / \text{PPI}^{\text{ready-mix}}_t}{\text{PPI}^{\text{cement}}_{2002} / \text{PPI}^{\text{ready-mix}}_{2002}}
```

- **Estimating equations.** Newey-West standard errors (2 lags) for the national series; district-clustered
  errors for panels; HC1 for the long difference. Districts are matched by exact name across tables and years;
  a change in a district's definition creates a new fixed-effect unit.

```math
\begin{aligned}
\Delta r_t &= \alpha + \beta\,\Delta u_t + \varepsilon_t \\
\ln p_{dt} &= \gamma\,u_{dt} + \delta_d + \tau_t + \varepsilon_{dt} \\
\ln p_{dt} &= \theta\,\text{HHI}_{dt}/1000 + \delta_d + \tau_t + \varepsilon_{dt} \\
\ln p_{d,2023} - \ln p_{d,2010} &= \alpha + \varepsilon_d \\
&\quad + \theta\,(\text{HHI}_{d,2023} - \text{HHI}_{d,2010})/1000
\end{aligned}
```

- **Model.** Linear inverse demand with $`a - c = 1`$, $`b = 1`$. With $`n`$ downstream firms and secret
  contracts, output is $`n/(n+1)`$ and the supplier's profit is $`n/(n+1)^2`$, against $`1/2`$ and $`1/4`$ after
  integration (`results/model_linear.csv`).

## Full test statistics

`results/tests.csv` and `results/consolidation_tests.csv` hold every statistic. Additional ones not in the table
above: states with a single kiln owner, 11 (2010) and 13 (2023); plants with three or fewer owners within 160 miles,
48.4% (2010) and 57.5% (2023); share of plants whose 160-mile top four is below 50%, 0% in both years; national HHI
832 (2010) and 831 (2023), top-4 share 45.9% and 45.0%; states with four or fewer owners, 30 of 34 in both years; utilization peak 87.7% (2006) and trough 49.2% (2009);
relative price −13.9% from 2007 to 2012; mill price −13.7% from 2008 to 2011 and +65.9% from 2010 to 2023;
ready-mix share of portland shipments 72.2% (2023, range 69.2% to 74.9% over 2002–2023); import share 19.0% (2023),
8.1% (2010), 24.8% (2006); cross-sectional price on HHI with year effects only, +0.0036 (SE 0.0056); median price
growth 67.1% where HHI rose (9 districts, one of them Missouri at +6 points) and 56.2% where it fell (7).

## Reproducing the results

```bash
pip install -r requirements.txt
python src/fetch_data.py            # optional: refreshes data/raw/ from the sources
python src/cement_markets.py        # model, concentration, capacity and prices
python src/consolidation_prices.py  # the extension: concentration changes and prices
```

## Repository layout

| Path | What it is |
|---|---|
| [src/fetch_data.py](src/fetch_data.py) | Downloads EPA, USGS and FRED files into `data/raw/` |
| [src/cement_markets.py](src/cement_markets.py) | Model table, owner grouping, concentration, capacity and price tests |
| [src/consolidation_prices.py](src/consolidation_prices.py) | District HHI against district prices, 2010–2023 |
| `results/*.csv`, `results/*.png` | Every number and figure in the README |

## References

- Federal Trade Commission (1966). *Economic Report on Mergers and Vertical Integration in the Cement Industry.*
  Cited through Hart and Tirole (1990).
- Grossman, S. & Hart, O. (1986). The costs and benefits of ownership. *Journal of Political Economy* 94(4).
- Hart, O. & Tirole, J. (1990). Vertical integration and market foreclosure. *Brookings Papers on Economic
  Activity: Microeconomics* 1990, 205–286.
- Hortaçsu, A. & Syverson, C. (2007). Cementing relationships: vertical integration, foreclosure, productivity, and
  prices. *Journal of Political Economy* 115, 250–301.
- Rey, P. & Tirole, J. (2007). A primer on foreclosure. *Handbook of Industrial Organization*, Vol. 3.
- US Department of Justice & Federal Trade Commission (2023). *Merger Guidelines*, December 18, 2023.
