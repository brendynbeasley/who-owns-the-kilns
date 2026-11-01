"""The extension: when ownership of a region's kilns consolidated, did its cement get dearer?

Hortacsu and Syverson (2007) used confidential Census plant data to show that, in cement and
ready-mixed concrete markets, prices fell rather than rose as markets became more integrated. Public
data cannot see who owns the ready-mix trucks, but they can see who owns the kilns. Between 2010 and
2023 the owners of US cement plants changed hands in a series of large deals, so the concentration of
each USGS cement district moved for reasons that had little to do with that district's demand.
If those changes conferred the kind of market power the foreclosure story needs, prices should have
risen where concentration rose.

Data: plant ownership and kiln CO2 from the EPA GHGRP (via src/cement_markets.py); district average
mill prices and clinker utilization from the USGS Minerals Yearbook, 2010-2023.
Writes results/district_hhi_prices.csv, district_changes.csv, consolidation_tests.csv and
results/consolidation_scatter.png.

Usage (from the repository root):
    python src/consolidation_prices.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cement_markets as cm  # noqa: E402

YEARS = range(2010, 2024)    # years covered by both GHGRP and the USGS yearbooks
DROP = r"^(Total|Grand|Puerto|Importers|Independent|Alaska)"   # rows that are not districts with kilns


def district_panel(plants, val, cap):
    rows, unmatched, no_kilns = [], set(), 0
    for r in val.itertuples():
        members = cm.district_states(r.district)
        if members is None:
            unmatched.add(r.district)
            continue
        d = plants[(plants.year == r.year) & plants.subregion.isin(members)]
        if d.empty:
            no_kilns += 1
            continue
        sh = (d.groupby("owner").co2.sum() / d.co2.sum() * 100).sort_values(ascending=False)
        rows.append(dict(district=r.district, year=r.year, price_per_t=r.price_per_t, shipments_kt=r.shipments_kt,
                         plants=d.facility_id.nunique(), owners=len(sh), hhi=(sh ** 2).sum(), cr4=sh.head(4).sum(),
                         top_owner=sh.index[0], top_share=sh.iloc[0]))
    if unmatched:
        print(f"District names not mapped to states (dropped): {sorted(unmatched)}")
    print(f"District price rows with no reporting kiln plant in their states that year (dropped): {no_kilns}")
    p = pd.DataFrame(rows)
    u = cap.assign(utilization=cap.clinker_kt / cap.capacity_kt * 100)[["district", "year", "utilization"]]
    return p.merge(u, on=["district", "year"], how="left")


def owners_text(plants, members, year, k=3):
    d = plants[(plants.year == year) & plants.subregion.isin(members)]
    sh = (d.groupby("owner").co2.sum() / d.co2.sum() * 100).sort_values(ascending=False)
    return "; ".join(f"{o} {s:.0f}%" for o, s in sh.head(k).items())


def main():
    plants = cm.load_plants()
    cap, val, _ = cm.load_usgs(YEARS)
    val = val[~val.district.str.match(DROP)].dropna(subset=["price_per_t"])
    cap = cap[~cap.district.str.match(DROP)]
    p = district_panel(plants, val, cap)
    p["log_price"] = np.log(p.price_per_t)
    p["hhi_k"] = p.hhi / 1000
    print(f"District-years with prices and kilns: {len(p)} ({p.district.nunique()} district definitions); "
          f"{p.utilization.notna().sum()} also have a matching capacity row")
    p.round(3).to_csv(cm.OUT / "district_hhi_prices.csv", index=False)

    tests = []
    specs = [("log_price ~ hhi_k + C(district) + C(year)", p, "district and year fixed effects"),
             ("log_price ~ hhi_k + utilization + C(district) + C(year)", p.dropna(subset=["utilization"]),
              "plus district utilization"),
             ("log_price ~ hhi_k + C(year)", p, "year effects only (cross-section)")]
    for f, data, label in specs:
        r = smf.ols(f, data=data).fit(cov_type="cluster", cov_kwds={"groups": data.district})
        b, se, pv = r.params["hhi_k"], r.bse["hhi_k"], r.pvalues["hhi_k"]
        lo, hi = b - 1.96 * se, b + 1.96 * se
        print(f"log price on HHI/1000, {label}: {b:+.4f} (SE {se:.4f}, p={pv:.2f}), n={int(r.nobs)}")
        tests.append(dict(test=f"log price on HHI (per 1,000 points), {label}", value=b, se=se, p=pv,
                          ci_low=lo, ci_high=hi, n=int(r.nobs), clusters=data.district.nunique()))

    first, last = p[p.year == min(YEARS)].set_index("district"), p[p.year == max(YEARS)].set_index("district")
    common = first.index.intersection(last.index)
    ch = pd.DataFrame({"hhi_2010": first.loc[common, "hhi"], "hhi_2023": last.loc[common, "hhi"],
                       "owners_2010": first.loc[common, "owners"], "owners_2023": last.loc[common, "owners"],
                       "price_2010": first.loc[common, "price_per_t"], "price_2023": last.loc[common, "price_per_t"]})
    ch["d_hhi"] = ch.hhi_2023 - ch.hhi_2010
    ch["price_growth_pct"] = (ch.price_2023 / ch.price_2010 - 1) * 100
    ch["owners_2010_names"] = [owners_text(plants, cm.district_states(d), min(YEARS)) for d in ch.index]
    ch["owners_2023_names"] = [owners_text(plants, cm.district_states(d), max(YEARS)) for d in ch.index]
    ch = ch.sort_values("d_hhi", ascending=False)
    ch.round(1).to_csv(cm.OUT / "district_changes.csv")
    print(f"Districts with the same definition in 2010 and 2023: {len(ch)} (dropped "
          f"{first.index.difference(common).size} 2010 and {last.index.difference(common).size} 2023 definitions)")
    r = smf.ols("np.log(price_2023 / price_2010) ~ I(d_hhi / 1000)", data=ch).fit(cov_type="HC1")
    b, se = r.params.iloc[1], r.bse.iloc[1]
    print(f"Long difference 2010-2023: log price growth on change in HHI/1000 = {b:+.4f} (SE {se:.4f}), n={len(ch)}")
    tests.append(dict(test="long difference 2010-2023: log price growth on change in HHI (per 1,000)",
                      value=b, se=se, p=r.pvalues.iloc[1], ci_low=b - 1.96 * se, ci_high=b + 1.96 * se,
                      n=len(ch), clusters=np.nan))
    up, down = ch[ch.d_hhi > 0], ch[ch.d_hhi <= 0]
    tests.append(dict(test="median price growth 2010-2023, districts where HHI rose (percent)",
                      value=up.price_growth_pct.median(), n=len(up)))
    tests.append(dict(test="median price growth 2010-2023, districts where HHI fell or held (percent)",
                      value=down.price_growth_pct.median(), n=len(down)))
    pd.DataFrame(tests).to_csv(cm.OUT / "consolidation_tests.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axvline(0, color="#999", lw=0.8)
    ax.scatter(ch.d_hhi, ch.price_growth_pct, s=40, color="#1f4e79")
    for d, r_ in ch.iterrows():
        ax.annotate(d, (r_.d_hhi, r_.price_growth_pct), fontsize=7, xytext=(4, 3),
                    textcoords="offset points")
    xs = np.linspace(ch.d_hhi.min(), ch.d_hhi.max(), 20)
    ax.plot(xs, (np.exp(r.params.iloc[0] + b * xs / 1000) - 1) * 100, color="#c55a11", lw=1.2, ls="--")
    ax.set_xlabel("Change in owner HHI of the district's kilns, 2010 to 2023")
    ax.set_ylabel("Change in average mill price, 2010 to 2023 (%)")
    ax.set_title("Where kiln ownership consolidated, cement prices did not rise faster", fontsize=11)
    fig.text(0.01, 0.01, "Sources: EPA GHGRP (owners, kiln CO2), USGS Minerals Yearbook (district prices).", fontsize=7)
    fig.tight_layout()
    fig.savefig(cm.OUT / "consolidation_scatter.png", dpi=150)
    print("Wrote results/district_hhi_prices.csv, district_changes.csv, consolidation_tests.csv, consolidation_scatter.png")


if __name__ == "__main__":
    main()
