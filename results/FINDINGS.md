# Hart and Tirole (1990) on today's cement industry: findings

## In plain English

In 1990 Oliver Hart and Jean Tirole showed that a supplier with market power can gain by buying one of its
customers, because owning the customer lets it credibly hold back supply from the customer's rivals. They used the
1960s wave of cement makers buying ready-mix concrete companies as their main example. This repository checks
their cement story against 2002–2023 data.

- **Local cement markets are concentrated, more than in the 1960s by this measure.** In every one of the 34 states
  with kilns, the top four owners hold at least half of kiln output, against all but 6% of states in the FTC's
  1960s count of shipments. In 30 of the 34 states four or fewer companies own every kiln. Holcim, CRH, Heidelberg
  Materials, Cemex, Buzzi and Eagle Materials own most of the kilns, and within 160 miles of the typical plant there
  are only three separate owners.
- **Idle kilns cheapened cement relative to concrete.** Utilization fell from 88% in 2006 to 49% in 2009, and
  cement's price relative to ready-mixed concrete fell 14% from 2007 to 2012, the pattern Hart and Tirole's "scarce needs"
  story relies on. The link holds nationally, not district by district.
- **Consolidation did not raise prices.** Where ownership of the kilns became more concentrated between 2010 and
  2023, such as Maine and New York (Lafarge's plants to Holcim) or Oregon and Washington (Ash Grove's to CRH),
  cement prices rose no faster than elsewhere once the size of the change is taken into account, which matches Hortaçsu and Syverson's (2007) finding of efficiency
  rather than foreclosure in cement.

A friendlier tour is in the [README](../README.md); methods are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels.** *Kiln output* = subpart H carbon dioxide reported to the EPA, used as a proxy for clinker
output. *HHI* = sum of squared percentage shares. *CR4* = share of the four largest owners. *Utilization* = clinker
produced ÷ clinker capacity (USGS). *Relative price* = cement PPI ÷ ready-mix PPI, 2002 = 1. *District* = USGS cement
district (a state, a group of states, or half of Texas or Pennsylvania). *Within 160 miles* = all kilns within 160
miles of a given plant, the FTC's 90% shipping distance. Owner names are as reported to the EPA after merging
spelling variants (see TECHNICAL.md).

## 1. The model (`model_linear.csv`)

Linear demand, a − c = 1, b = 1. "Secret contracts" = the supplier sells to n downstream firms by private contract;
"integrated" = the supplier owns one of them.

| Downstream firms | Output, secret contracts | Output, integrated | Supplier profit, secret | Share of monopoly profit | Output cut by integration |
|---|---|---|---|---|---|
| 1 | 0.500 | 0.500 | 0.250 | 1.000 | 0.000 |
| 2 | 0.667 | 0.500 | 0.222 | 0.889 | 0.250 |
| 3 | 0.750 | 0.500 | 0.188 | 0.750 | 0.333 |
| 4 | 0.800 | 0.500 | 0.160 | 0.640 | 0.375 |
| 6 | 0.857 | 0.500 | 0.122 | 0.490 | 0.417 |
| 10 | 0.909 | 0.500 | 0.083 | 0.331 | 0.450 |

Total surplus with two downstream firms is 0.444 under secret contracts and 0.375 after integration, the 4/9 and 3/8
of the paper's footnote 24.

## 2. Concentration by state, 2023 (`state_concentration.csv`, `state_owner_shares_2023.csv`)

| State | Owners | CR4 (%) | HHI | Largest owner | Its share (%) | Kiln CO2 (Mt) |
|---|---|---|---|---|---|---|
| TX | 10 | 66.5 | 1,570 | Martin Marietta | 30.3 | 8.6 |
| CA | 5 | 92.7 | 2,709 | Taiheiyo (CalPortland) | 40.0 | 6.9 |
| MO | 4 | 100.0 | 3,480 | Holcim | 44.4 | 6.7 |
| FL | 6 | 93.0 | 2,343 | Cemex | 32.2 | 4.0 |
| AL | 5 | 85.6 | 2,180 | Argos | 29.3 | 3.6 |
| MI | 2 | 100.0 | 5,059 | Holcim | 55.4 | 3.2 |
| PA | 4 | 100.0 | 3,396 | Heidelberg Materials | 47.8 | 2.5 |
| SC | 3 | 100.0 | 3,864 | Holcim | 51.9 | 2.3 |
| MD | 2 | 100.0 | 6,854 | Heidelberg Materials | 80.4 | 2.3 |
| IN | 2 | 100.0 | 5,054 | Heidelberg Materials | 55.2 | 2.3 |
| KS | 2 | 100.0 | 5,128 | CRH | 58.0 | 2.2 |
| AZ | 3 | 100.0 | 3,472 | Taiheiyo (CalPortland) | 38.6 | 2.0 |
| CO | 3 | 100.0 | 3,865 | Holcim | 46.5 | 1.6 |
| KY | 1 | 100.0 | 10,000 | Eagle Materials | 100.0 | 1.3 |
| IA | 2 | 100.0 | 5,483 | Summit Materials | 65.6 | 1.3 |
| TN | 2 | 100.0 | 5,443 | Buzzi | 64.9 | 1.2 |
| NY | 2 | 100.0 | 9,041 | Holcim | 95.0 | 1.2 |
| OK | 3 | 100.0 | 3,546 | Eagle Materials | 41.6 | 1.2 |
| IL | 2 | 100.0 | 5,564 | Eagle Materials | 66.8 | 1.1 |
| UT | 2 | 100.0 | 5,003 | Holcim | 51.3 | 1.1 |
| OH | 2 | 100.0 | 5,103 | Eagle Materials | 57.2 | 0.8 |
| MT | 2 | 100.0 | 5,079 | CRH | 56.3 | 0.6 |
| AR, GA, ME, NE, NM, NV, OR, SD, VA, WA, WV, WY | 1 each | 100.0 | 10,000 | CRH (AR, NE, OR, WA), Eagle (NV, WY), GCC (NM, SD), Argos (WV), Cemex (GA), Giant (ME), Titan (VA) | 100.0 | 0.2–0.9 |

Summary (`tests.csv`): states with CR4 below 50%, 0 of 34 in both 2010 and 2023 (paper, 1960s: 6% of states).
States with HHI above 1,800, 33 of 34 in both years. States with a single owner, 11 (2010) and 13 (2023). States
with four or fewer owners, where CR4 is 100% by definition, 30 of 34 in both years.

## 3. Owners nationally (`owners_2023.csv`)

| Owner, 2023 | Plants | States | Share of US kiln CO2 (%) | States where largest |
|---|---|---|---|---|
| Holcim | 12 | 12 | 18.3 | 6 |
| CRH | 10 | 9 | 9.1 | 6 |
| Heidelberg Materials | 10 | 7 | 8.9 | 3 |
| Cemex | 8 | 7 | 8.8 | 2 |
| Buzzi | 7 | 6 | 8.6 | 1 |
| Eagle Materials | 8 | 8 | 7.8 | 6 |
| Taiheiyo (CalPortland) | 4 | 2 | 5.5 | 2 |
| Argos | 4 | 4 | 5.1 | 2 |
| Martin Marietta | 2 | 1 | 4.0 | 1 |
| GCC | 5 | 5 | 3.5 | 2 |

Fifteen smaller owners make up the rest; every row, for 2010 and 2023, is in the CSV. In 2010 the top six were
Cemex 15.4%, Heidelberg Materials 10.7%, Holcim 10.4%, Lafarge 9.4%, Ash Grove 9.2% and Buzzi 9.0%. National CR4
was 45.9% (2010) and 45.0% (2023); national HHI 832 and 831; owners 27 and 25. A jointly owned plant counts once
for each of its owners in the plant column.

## 4. Rivals within 160 miles (`plant_rivals.csv`)

| | 2010 | 2023 |
|---|---|---|
| Plants | 91 | 87 |
| Median owners within 160 miles | 4 | 3 |
| Median HHI within 160 miles | 3,558 | 3,770 |
| Plants with three or fewer owners within 160 miles | 48.4% | 57.5% |
| Plants whose 160-mile CR4 is below 50% | 0% | 0% |

## 5. Capacity and prices (`capacity_prices.csv`)

| Year | Capacity (kt) | Clinker (kt) | Utilization (%) | Mill price ($/t) | Relative price | Ready-mix share (%) | Import share (%) |
|---|---|---|---|---|---|---|---|
| 2002 | 99,000 | 81,517 | 82.3 | 74.5 | 1.000 | 74.9 | 18.1 |
| 2004 | 103,000 | 86,658 | 84.1 | 78.0 | 0.971 | 72.9 | 19.2 |
| 2006 | 101,000 | 88,555 | 87.7 | 99.5 | 0.989 | 73.4 | 24.8 |
| 2007 | 101,000 | 86,130 | 85.3 | 101.5 | 1.004 | 73.9 | 18.2 |
| 2008 | 107,000 | 78,382 | 73.3 | 102.0 | 0.971 | 72.0 | 11.7 |
| 2009 | 114,000 | 56,116 | 49.2 | 97.5 | 0.931 | 71.2 | 8.5 |
| 2010 | 109,000 | 59,802 | 54.9 | 91.0 | 0.901 | 69.2 | 8.1 |
| 2011 | 106,000 | 61,241 | 57.8 | 88.0 | 0.875 | 69.8 | 8.0 |
| 2012 | 106,000 | 67,173 | 63.4 | 88.5 | 0.864 | 70.3 | 8.0 |
| 2014 | 105,000 | 74,372 | 70.8 | 99.5 | 0.881 | 71.4 | 8.3 |
| 2016 | 105,000 | 75,633 | 72.0 | 110.0 | 0.920 | 73.1 | 11.3 |
| 2018 | 102,000 | 77,112 | 75.6 | 119.5 | 0.914 | 71.1 | 12.8 |
| 2020 | 102,000 | 78,951 | 77.4 | 124.0 | 0.899 | 72.6 | 13.6 |
| 2022 | 103,000 | 79,489 | 77.2 | 138.0 | 0.894 | 72.4 | 17.6 |
| 2023 | 104,000 | 76,789 | 73.8 | 151.0 | 0.904 | 72.2 | 19.0 |

Every year from 2002 to 2023 is in the CSV.

| Test (`tests.csv`) | Estimate | SE | p | N |
|---|---|---|---|---|
| Relative price on utilization, levels, per 10 points | +0.0271 | 0.0107 | 0.011 | 22 |
| Relative price on utilization, first differences, per 10 points | +0.0118 | 0.0039 | 0.002 | 21 |
| District log price on utilization, district and year effects, per 10 points | −0.0062 | 0.0070 | 0.37 | 438 (31 districts) |

Changes: relative price −13.9% (2007 to 2012); mill price −13.7% (2008 to 2011) and +65.9% (2010 to 2023).
`district_capacity_prices.csv` holds the 438 district-years.

## 6. Extension: concentration changes and prices (`consolidation_tests.csv`, `district_changes.csv`)

| Test | Estimate | SE | 95% CI | N |
|---|---|---|---|---|
| Log price on HHI/1000, district and year effects | −0.0141 | 0.0190 | [−0.051, 0.023] | 287 (27 units) |
| Same, plus district utilization | −0.0255 | 0.0228 | [−0.070, 0.019] | 252 (25 units) |
| Log price on HHI/1000, year effects only | +0.0036 | 0.0056 | [−0.007, 0.015] | 287 |
| Long difference 2010–2023, log price growth on ΔHHI/1000 | +0.0056 | 0.0152 | [−0.024, 0.035] | 16 |

Median price growth 2010–2023: 67.1% in the 9 districts where HHI rose (Missouri, at +6 points, among them), 56.2%
in the 7 where it fell.

| District | Owners 2010 → 2023 | HHI 2010 | HHI 2023 | ΔHHI | Price 2010 ($/t) | Price 2023 ($/t) | Growth (%) |
|---|---|---|---|---|---|---|---|
| Maine and New York | 4 → 3 | 2,956 | 6,563 | +3,607 | 91.7 | 148.4 | 61.8 |
| Oregon and Washington | 2 → 1 | 7,781 | 10,000 | +2,219 | 90.0 | 150.5 | 67.1 |
| Kansas | 3 → 2 | 4,424 | 5,128 | +704 | 97.7 | 110.9 | 13.5 |
| California | 6 → 5 | 2,163 | 2,709 | +546 | 79.0 | 134.0 | 69.6 |
| Illinois | 2 → 2 | 5,124 | 5,564 | +440 | 89.1 | 138.0 | 54.9 |
| Colorado and Wyoming | 4 → 4 | 2,608 | 2,801 | +193 | 93.0 | 187.5 | 101.6 |
| South Carolina | 3 → 3 | 3,724 | 3,864 | +140 | 86.8 | 146.0 | 68.2 |
| Iowa, Nebraska, South Dakota | 4 → 4 | 2,603 | 2,644 | +41 | 103.1 | 170.0 | 64.8 |
| Missouri | 4 → 4 | 3,473 | 3,480 | +6 | 82.5 | 149.0 | 80.6 |
| Texas, southern | 6 → 6 | 2,040 | 2,017 | −23 | 86.0 | 162.5 | 88.9 |
| Georgia, Maryland, Virginia, West Virginia | 5 → 5 | 2,854 | 2,762 | −91 | 84.2 | 156.0 | 85.4 |
| Texas, northern | 5 → 5 | 2,693 | 2,447 | −246 | 91.0 | 159.5 | 75.3 |
| Michigan | 2 → 2 | 5,412 | 5,059 | −352 | 100.5 | 157.0 | 56.2 |
| Arkansas and Oklahoma | 4 → 4 | 3,485 | 3,003 | −482 | 97.4 | 135.0 | 38.6 |
| Florida | 8 → 6 | 3,175 | 2,343 | −831 | 90.5 | 129.5 | 43.1 |
| Arizona and New Mexico | 3 → 4 | 3,979 | 2,797 | −1,181 | 102.2 | 152.5 | 49.2 |

The owner names behind each district, for both years, are in `district_changes.csv`; the full panel is
`district_hhi_prices.csv`; every plant and owner in 2023 is in `plants_2023.csv`.

## Figures

- `capacity_and_prices.png`: national clinker utilization and the relative price of cement, 2002–2023.
- `consolidation_scatter.png`: change in district HHI against change in mill price, 2010–2023.
