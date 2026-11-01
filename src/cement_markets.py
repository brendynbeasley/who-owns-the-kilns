"""Hart and Tirole (1990) on today's US cement industry: the model's numbers, who owns the kilns,
and whether slack kilns move the margin to the concrete trucks.

Three parts, all written to results/:
  1. The linear-demand example of the paper (Propositions 1 and 2, footnote 24): output and profit
     when an upstream monopolist sells to rival downstream firms by secret contract, versus after it
     merges with one of them.                                               -> model_linear.csv
  2. Market structure, the precondition for foreclosure (Williamson's objection). Every US clinker
     plant from the EPA Greenhouse Gas Reporting Program, grouped by owner, 2010-2023. The paper's
     benchmark (FTC 1966) is that the top four suppliers held under half of the market in only 6% of
     states.                    -> state_concentration.csv, owners_2023.csv, plant_rivals.csv
  3. Capacity and the bottleneck (the paper's "scarce needs" story for cement). National and district
     clinker utilization from the USGS Minerals Yearbook against cement prices, the cement/ready-mix
     price ratio (BLS PPI), and the share of cement sold to ready-mix producers.
                                     -> capacity_prices.csv, district_capacity_prices.csv, tests.csv

Usage (from the repository root, after the data in data/raw/ is present):
    python src/cement_markets.py
"""

import re
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

RADIUS_MILES = 160          # FTC (1966) via Hart-Tirole p. 249: 90% of cement shipped 160 miles or less
CR4_LINE = 50               # the paper's state benchmark: top-4 share below 50% in only 6% of states
PAPER_SHARE_BELOW = 6       # percent of states, 1960s (quoted, Hart and Tirole 1990, p. 249)
EXCLUDE_STATES = {"PR"}     # Puerto Rico is outside the USGS US totals
# Owner names that change with an acquisition: legacy name -> (acquirer, first year the plants' own
# GHGRP filings name the acquirer). Dates come from the filings, not from press releases.
LEGACY = {
    "LAFARGE": ("Holcim", 2017),
    "ESSROC|ITALCEMENTI": ("Heidelberg Materials", 2017),
    "ASH GROVE": ("CRH", 2018),
    "TEXAS INDUSTRIES|TXI": ("Martin Marietta", 2014),
}
OWNER_RULES = [  # regex on the reported parent name -> owner group
    ("HOLCIM", "Holcim"), ("HEIDELBERG|HANSON|LEHIGH", "Heidelberg Materials"),
    ("CRH|OLDCASTLE", "CRH"), ("MARTIN MARIETTA", "Martin Marietta"), ("CEMEX", "Cemex"),
    ("BUZZI|RC LONESTAR|HERCULES", "Buzzi"), ("VOTORANTIM|BARBARA", "Votorantim (St Marys)"),
    ("TAIHEIYO", "Taiheiyo (CalPortland)"), ("GCC", "GCC"),
    ("EAGLE|CENTRAL PLAINS|TULSA CEMENT", "Eagle Materials"),
    ("SUMMIT|CONTINENTAL CEMENT", "Summit Materials"), ("ARGOS", "Argos"), ("GIANT", "Giant Cement"),
    ("TITAN", "Titan America"), ("NATIONAL CEMENT", "National Cement"), ("MITSUBISHI", "Mitsubishi Cement"),
    ("CAPITOL|ZACHRY", "Capitol Aggregates (Zachry)"), ("MONARCH", "Monarch Cement"), ("DRAKE", "Drake Cement"),
    ("PHOENIX", "Phoenix Cement"), ("ALAMO", "Alamo Cement"), ("SNYDER", "Snyder Associated"),
    ("SKANON", "Skanon Investments"), ("VULCAN", "Vulcan Materials"), ("ANDERSON COLUMBIA", "Anderson Columbia"),
    ("NATURAL RESOURCES OF CENTRAL FLORIDA", "Natural Resources of Central Florida"), ("CJM OF FLORIDA", "CJM of Florida"),
]
TX_NORTH_COUNTIES = {"MCLENNAN", "ECTOR", "NOLAN", "ELLIS"}      # USGS Table 2: Texas, northern
PA_WEST_COUNTIES = {"BUTLER", "LAWRENCE"}                        # USGS Table 2: Pennsylvania, western
STATES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
          "Colorado": "CO", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
          "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Maine": "ME", "Maryland": "MD",
          "Michigan": "MI", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
          "Nevada": "NV", "New Mexico": "NM", "New York": "NY", "Ohio": "OH", "Oklahoma": "OK",
          "Oregon": "OR", "Pennsylvania": "PA", "South Carolina": "SC", "South Dakota": "SD",
          "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Virginia": "VA", "Washington": "WA",
          "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}


# ---------------------------------------------------------------- 1. the model

def model_linear():
    """Linear demand p = a - Q, upstream cost c, a - c = 1 (so quantities are shares of (a-c)/b)."""
    rows = []
    for n in [1, 2, 3, 4, 6, 10]:
        q_ni = n / (n + 1)                  # secret contracts: each downstream firm gets its Cournot quantity
        profit_ni = n / (n + 1) ** 2        # upstream captures Cournot industry profit (Prop. 1, c2 infinite)
        rows.append(dict(downstream_firms=n, output_nonintegrated=q_ni, output_integrated=0.5,
                         upstream_profit_nonintegrated=profit_ni, monopoly_profit=0.25,
                         share_of_monopoly_profit=profit_ni / 0.25, output_cut_by_integration=1 - 0.5 / q_ni,
                         markup_nonintegrated=1 - q_ni, markup_integrated=0.5,
                         total_surplus_nonintegrated=q_ni - q_ni ** 2 / 2, total_surplus_integrated=0.375))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- 2. who owns the kilns

def owner_group(name, year):
    name = name.upper()
    for pat, (acq, since) in LEGACY.items():
        if re.search(pat, name):
            return acq if year >= since else {"LAFARGE": "Lafarge", "ASH GROVE": "Ash Grove",
                                               "TEXAS INDUSTRIES|TXI": "TXI"}.get(pat, "Essroc (Italcementi)")
    for pat, grp in OWNER_RULES:
        if re.search(pat, name):
            return grp
    return name.strip().title()


def split_owners(parent, facility, year):
    """'A (50%); B (50%)' -> [(group, 0.5), ...]; blank or 'None' parents fall back to the facility name.
    When the reported percentages sum to less than 100% and no owner is left without a share (two 2010
    filings list only a 51% holder), the named owners are scaled up to 100%, so no kiln output is lost."""
    if "TEXAS LEHIGH" in str(parent).upper() + str(facility).upper():
        return [("Eagle Materials", 0.5), ("Heidelberg Materials", 0.5)]  # the plant's 2021-23 filings: 50/50
    blank = not isinstance(parent, str) or re.sub(r"\(.*?\)", "", parent).strip().upper() in ("", "NONE")
    parts = [p.strip() for p in str(facility if blank else parent).split(";") if p.strip()]
    out = []
    for p in parts:
        m = re.search(r"\((\d+(?:\.\d+)?)%\)", p)
        out.append([owner_group(re.sub(r"\(.*?\)", "", p), year), float(m.group(1)) / 100 if m else None])
    known = sum(s for _, s in out if s is not None)
    blanks = [o for o in out if o[1] is None]
    for o in blanks:
        o[1] = max(1 - known, 0) / len(blanks) if known < 1 else 0
    total = sum(s for _, s in out)
    return [(g, s / total) for g, s in out if s > 0]


def load_plants():
    emis = pd.read_csv(RAW / "ghgrp_subpart_h_emissions.csv")
    fac = pd.read_csv(RAW / "ghgrp_cement_facilities.csv")
    co2 = emis[emis.gas_id == 1].groupby(["facility_id", "year"]).co2e_emission.sum().rename("co2").reset_index()
    p = fac.merge(co2, on=["facility_id", "year"], how="inner")
    n0 = len(p)
    p = p[~p.state.isin(EXCLUDE_STATES)]
    white = p.facility_name.str.upper().str.contains("WHITE") | p.parent_company.fillna("").str.upper().str.contains("WHITE")
    p = p[~white & (p.co2 > 0)].copy()
    print(f"GHGRP plant-years with kiln CO2: {n0}; kept {len(p)} after dropping Puerto Rico, "
          f"white-cement plants and zero-emission years ({p.facility_id.nunique()} plants, "
          f"{p.year.min()}-{p.year.max()})")
    p["county_u"] = p.county.fillna("").str.upper().str.replace(" COUNTY", "", regex=False).str.strip()
    p["subregion"] = p.state
    p.loc[(p.state == "TX"), "subregion"] = np.where(p.loc[p.state == "TX", "county_u"].isin(TX_NORTH_COUNTIES), "TX-N", "TX-S")
    p.loc[(p.state == "PA"), "subregion"] = np.where(p.loc[p.state == "PA", "county_u"].isin(PA_WEST_COUNTIES), "PA-W", "PA-E")
    rows = []
    for r in p.itertuples():
        for g, s in split_owners(r.parent_company, r.facility_name, r.year):
            rows.append(dict(facility_id=r.facility_id, year=r.year, facility_name=r.facility_name, city=r.city, state=r.state,
                             subregion=r.subregion, lat=r.latitude, lon=r.longitude, owner=g, co2=r.co2 * s))
    return pd.DataFrame(rows)


def concentration(df, by):
    """CR4, HHI and owner count from CO2 shares within each group of `by`."""
    o = df.groupby(by + ["owner"]).co2.sum().reset_index()
    o["share"] = o.co2 / o.groupby(by).co2.transform("sum") * 100
    o = o.sort_values(by + ["share"], ascending=[True] * len(by) + [False])
    g = o.groupby(by)
    res = pd.DataFrame({"owners": g.size(), "cr4": g.share.apply(lambda s: s.head(4).sum()),
                        "hhi": g.share.apply(lambda s: (s ** 2).sum()), "top_owner": g.owner.first(),
                        "top_share": g.share.first(), "co2_tonnes": g.co2.sum()})
    return res.reset_index()


def plant_rivals(plants, year):
    """For each plant, owners and owner HHI among all kilns within RADIUS_MILES."""
    d = plants[plants.year == year]
    loc = d.groupby("facility_id")[["lat", "lon", "facility_name", "state"]].first()
    lat, lon = np.radians(loc.lat.values), np.radians(loc.lon.values)
    dist = 3958.8 * 2 * np.arcsin(np.sqrt(np.sin((lat[:, None] - lat) / 2) ** 2 +
                                          np.cos(lat[:, None]) * np.cos(lat) * np.sin((lon[:, None] - lon) / 2) ** 2))
    rows = []
    for i, fid in enumerate(loc.index):
        near = d[d.facility_id.isin(loc.index[dist[i] <= RADIUS_MILES])]
        sh = (near.groupby("owner").co2.sum() / near.co2.sum() * 100).sort_values(ascending=False)
        rows.append(dict(year=year, facility_id=fid, facility_name=loc.facility_name.iloc[i], state=loc.state.iloc[i],
                         owners_within_radius=len(sh), cr4_within_radius=sh.head(4).sum(),
                         hhi_within_radius=(sh ** 2).sum()))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- 3. USGS tables

def usgs_sheets(year):
    f = next((RAW / "usgs_myb").glob(f"cement_myb_{year}.*"))
    return pd.read_excel(f, sheet_name=None, header=None)


def find_table(xl, *keys):
    for df in xl.values():
        title = " ".join(str(x) for x in df.iloc[:3].values.ravel() if pd.notna(x)).upper()
        if all(k in title for k in keys):
            return df
    raise KeyError(keys)


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return np.nan


def table_rows(df):
    """Return (header text per column, data rows) for a USGS district table. Footnote-marker columns
    have no header text and are ignored by callers that select columns by header."""
    start = next(i for i in range(len(df)) if str(df.iat[i, 0]).strip().startswith(("District", "Destination")))
    hdr = {j: " ".join(str(df.iat[i, j]) for i in range(3, start + 1) if pd.notna(df.iat[i, j])) for j in range(1, df.shape[1])}
    rows = df.iloc[start + 1:].copy()
    rows[0] = rows[0].astype(str).str.strip().str.replace(r"[\d,\s]+$", "", regex=True)
    return hdr, rows


def col(hdr, pattern, which=0):
    cols = [j for j, h in hdr.items() if re.search(pattern, h, re.I)]
    return cols[which]


def usgs_year(year):
    xl = usgs_sheets(year)
    hdr, rows = table_rows(find_table(xl, "CLINKER CAPACITY"))
    c_cap, c_prod = col(hdr, "annual"), col(hdr, r"produc")
    cap = rows[[0, c_cap, c_prod]].rename(columns={0: "district", c_cap: "capacity_kt", c_prod: "clinker_kt"})
    hdr, rows = table_rows(find_table(xl, "PORTLAND", "SHIPPED", "DISTRICT"))
    c_q, c_v = col(hdr, r"^(?!.*per).*metric tons", -1), col(hdr, r"Average|per", -1)  # rightmost = current year
    val = rows[[0, c_q, c_v]].rename(columns={0: "district", c_q: "shipments_kt", c_v: "price_per_t"})
    hdr, rows = table_rows(find_table(xl, "TYPE OF CUSTOMER"))
    c_rm, c_tot = col(hdr, r"Ready"), col(hdr, r"Total")
    cust = rows[[0, c_rm, c_tot]].rename(columns={0: "district", c_rm: "readymix_kt", c_tot: "cust_total_kt"})
    out = []
    for t in (cap, val, cust):
        t = t[~t.district.str.match(r"^(--|W |nan|r[A-Z]|e[A-Z]|See|TABLE)") & (t.district.str.len() < 60)].copy()
        for c in t.columns[1:]:
            t[c] = t[c].map(num)
        t["year"] = year
        out.append(t.dropna(subset=t.columns[1:2]))
    return out


def import_share(year):
    """Share of cement sold to US final customers that originated abroad (USGS Table 9, portland, current year)."""
    hdr, rows = table_rows(find_table(usgs_sheets(year), "DESTINATION AND ORIGIN"))
    c = col(hdr, str(year))
    foreign = rows[rows[0].str.startswith("Foreign")][c].map(num).iloc[-1]   # last one is under "Origin:"
    total = rows[rows[0].str.startswith("Total shipments")][c].map(num).iloc[-1]
    return foreign / total * 100


def load_usgs(years=range(2002, 2024)):
    cap, val, cust = [], [], []
    for y in years:
        a, b, c = usgs_year(y)
        cap.append(a), val.append(b), cust.append(c)
    cap, val, cust = pd.concat(cap), pd.concat(val), pd.concat(cust)
    print(f"USGS yearbooks {min(years)}-{max(years)}: {len(cap)} capacity rows, {len(val)} value rows, "
          f"{len(cust)} customer rows")
    return cap, val, cust


def district_states(name):
    """'Georgia, Maryland, Virginia, West Virginia' -> {'GA','MD','VA','WV'}; Texas/Pennsylvania halves -> subregions."""
    if name.startswith("Texas, "):
        return {"TX-N"} if "northern" in name else {"TX-S"}
    if name.startswith("Pennsylvania, "):
        return {"PA-W"} if "western" in name else {"PA-E"}
    parts = re.split(r",\s*|\s+and\s+", name)
    codes = {STATES.get(p.strip()) for p in parts}
    if None in codes:
        return None
    return {s for c in codes for s in ({"TX-N", "TX-S"} if c == "TX" else {"PA-E", "PA-W"} if c == "PA" else {c})}


def ppi_annual():
    out = []
    for sid, name in [("PCU327310327310", "ppi_cement"), ("PCU327320327320", "ppi_readymix")]:
        d = pd.read_csv(RAW / f"fred_{sid}.csv")
        d.columns = ["date", name]
        d["year"] = d.date.str[:4].astype(int)
        out.append(d.groupby("year")[name].mean())
    return pd.concat(out, axis=1)


# ---------------------------------------------------------------- main

def main():
    OUT.mkdir(exist_ok=True)
    tests = []

    m = model_linear()
    m.round(4).to_csv(OUT / "model_linear.csv", index=False)
    two = m[m.downstream_firms == 2].iloc[0]
    print(f"Model, two downstream firms: output {two.output_nonintegrated:.3f} -> {two.output_integrated:.3f} "
          f"after integration; supplier profit {two.share_of_monopoly_profit:.1%} of monopoly before")

    plants = load_plants()
    st = concentration(plants, ["year", "state"])
    st.round(2).to_csv(OUT / "state_concentration.csv", index=False)
    (plants[plants.year == 2023][["facility_name", "city", "state", "subregion", "owner", "co2"]]
     .sort_values(["state", "city"]).round(0).to_csv(OUT / "plants_2023.csv", index=False))
    so = plants[plants.year == 2023].groupby(["state", "owner"]).co2.sum().reset_index()
    so["share"] = so.co2 / so.groupby("state").co2.transform("sum") * 100
    so.sort_values(["state", "share"], ascending=[True, False]).round(2).to_csv(OUT / "state_owner_shares_2023.csv", index=False)
    for y in (2010, 2023):
        s = st[st.year == y]
        below = (s.cr4 < CR4_LINE).mean() * 100
        print(f"{y}: {len(s)} states with kilns; top-4 owners under {CR4_LINE}% in {below:.1f}% of them "
              f"(paper, 1960s: {PAPER_SHARE_BELOW}%); median HHI {s.hhi.median():.0f}")
        tests.append(dict(test=f"states with CR4 < {CR4_LINE}%, {y}", value=below, n=len(s),
                          note=f"paper (FTC 1966): {PAPER_SHARE_BELOW}% of states"))
        tests.append(dict(test=f"states with HHI > 1800, {y}", value=(s.hhi > 1800).mean() * 100, n=len(s), note="percent"))
        tests.append(dict(test=f"states with one owner, {y}", value=(s.owners == 1).sum(), n=len(s), note="count"))
        tests.append(dict(test=f"states with four or fewer owners (CR4 = 100%), {y}", value=(s.owners <= 4).sum(),
                          n=len(s), note="count"))

    nat = concentration(plants.assign(us="US"), ["year", "us"])
    own = plants[plants.year.isin([2010, 2023])].groupby(["year", "owner"]).agg(
        co2=("co2", "sum"), plants=("facility_id", "nunique"), states=("state", "nunique")).reset_index()
    own["share"] = own.co2 / own.groupby("year").co2.transform("sum") * 100
    lead = st[st.year.isin([2010, 2023])].groupby(["year", "top_owner"]).size().rename("states_led")
    own = own.merge(lead, left_on=["year", "owner"], right_index=True, how="left").fillna({"states_led": 0})
    own.sort_values(["year", "share"], ascending=[True, False]).round(2).to_csv(OUT / "owners_2023.csv", index=False)
    for y in (2010, 2023):
        n = nat[nat.year == y].iloc[0]
        print(f"{y} national: {n.owners} owners, top-4 share {n.cr4:.1f}%, HHI {n.hhi:.0f}")
        tests.append(dict(test=f"national CR4 of kiln CO2, {y}", value=n.cr4, n=n.owners, note="owners"))
        tests.append(dict(test=f"national HHI of kiln CO2, {y}", value=n.hhi, n=n.owners, note="owners"))

    pr = pd.concat([plant_rivals(plants, y) for y in (2010, 2023)])
    pr.round(1).to_csv(OUT / "plant_rivals.csv", index=False)
    for y in (2010, 2023):
        s = pr[pr.year == y]
        print(f"{y}: plants have a median of {s.owners_within_radius.median():.0f} owners within {RADIUS_MILES} "
              f"miles; median HHI there {s.hhi_within_radius.median():.0f}")
        tests.append(dict(test=f"median owners within {RADIUS_MILES} miles of a plant, {y}",
                          value=s.owners_within_radius.median(), n=len(s), note="plants"))
        tests.append(dict(test=f"median HHI within {RADIUS_MILES} miles of a plant, {y}",
                          value=s.hhi_within_radius.median(), n=len(s), note="plants"))
        tests.append(dict(test=f"plants with 3 or fewer owners within {RADIUS_MILES} miles, {y}",
                          value=(s.owners_within_radius <= 3).mean() * 100, n=len(s), note="percent"))
        tests.append(dict(test=f"plants whose {RADIUS_MILES}-mile top-4 share is under {CR4_LINE}%, {y}",
                          value=(s.cr4_within_radius < CR4_LINE).mean() * 100, n=len(s),
                          note=f"paper (FTC 1966): {PAPER_SHARE_BELOW}% of states"))

    cap, val, cust = load_usgs()
    us = (cap[cap.district.str.match("^Total")].set_index("year")[["capacity_kt", "clinker_kt"]]
          .join(val[val.district.str.match("^Total")].set_index("year")[["shipments_kt", "price_per_t"]])
          .join(cust[cust.district.str.match("^Total")].set_index("year")[["readymix_kt", "cust_total_kt"]]))
    us["utilization"] = us.clinker_kt / us.capacity_kt * 100
    us["readymix_share"] = us.readymix_kt / us.cust_total_kt * 100
    us["import_share"] = [import_share(y) for y in us.index]
    us = us.join(ppi_annual(), how="left")
    us["cement_to_readymix"] = us.ppi_cement / us.ppi_readymix
    us["cement_to_readymix_2002"] = us.cement_to_readymix / us.cement_to_readymix.loc[2002]
    us.index.name = "year"
    us.round(4).to_csv(OUT / "capacity_prices.csv")
    lo, hi = us.utilization.idxmin(), us.utilization.loc[:2008].idxmax()
    print(f"Utilization peaked at {us.utilization[hi]:.1f}% in {hi} and fell to {us.utilization[lo]:.1f}% in {lo}")
    tests.append(dict(test="clinker utilization peak (2002-2008)", value=us.utilization[hi], n=hi, note="year in n"))
    tests.append(dict(test="clinker utilization trough", value=us.utilization[lo], n=lo, note="year in n"))
    tests.append(dict(test="ready-mix share of portland cement shipments, 2023", value=us.readymix_share.loc[2023],
                      n=2023, note="percent"))
    tests.append(dict(test="imported share of cement sold to US customers, 2023", value=us.import_share.loc[2023],
                      n=2023, note="percent, USGS Table 9"))
    for a, b, c_ in [(2010, 2023, "price_per_t"), (2008, 2011, "price_per_t"), (2007, 2012, "cement_to_readymix")]:
        tests.append(dict(test=f"change in {c_}, {a}-{b} (percent)", value=(us.loc[b, c_] / us.loc[a, c_] - 1) * 100,
                          n=b - a, note="national"))

    d = us.reset_index()
    for f, label in [("cement_to_readymix_2002 ~ utilization", "levels"),
                     ("cement_to_readymix_2002.diff() ~ utilization.diff()", "first differences")]:
        dd = d.copy()
        dd["dr"], dd["du"] = dd.cement_to_readymix_2002.diff(), dd.utilization.diff()
        ff = f if label == "levels" else "dr ~ du"
        r = smf.ols(ff, data=dd).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
        b, se = r.params.iloc[1], r.bse.iloc[1]
        print(f"Cement/ready-mix price ratio on utilization ({label}): {b * 10:.4f} per 10 points (SE {se * 10:.4f}), n={int(r.nobs)}")
        tests.append(dict(test=f"price ratio on utilization, {label} (per 10 points)", value=b * 10, se=se * 10,
                          p=r.pvalues.iloc[1], n=int(r.nobs), note="2002-2023, Newey-West SE"))

    dist = cap.merge(val, on=["district", "year"])
    print(f"District capacity rows matched to a price row by exact name and year: {len(dist)} of {len(cap)} "
          f"(unmatched rows are totals or districts defined differently in the two tables)")
    dist = dist[~dist.district.str.match("^(Total|Grand|Puerto|Importers|Independent|Alaska)")].copy()
    dist["utilization"] = dist.clinker_kt / dist.capacity_kt * 100
    dist = dist.dropna(subset=["utilization", "price_per_t"])
    dist.round(3).to_csv(OUT / "district_capacity_prices.csv", index=False)
    r = smf.ols("np.log(price_per_t) ~ utilization + C(district) + C(year)", data=dist).fit(
        cov_type="cluster", cov_kwds={"groups": dist.district})
    print(f"District panel: log price on utilization = {r.params['utilization'] * 10:.4f} per 10 points "
          f"(SE {r.bse['utilization'] * 10:.4f}), {len(dist)} district-years, {dist.district.nunique()} districts")
    tests.append(dict(test="district log cement price on utilization, district+year FE (per 10 points)",
                      value=r.params["utilization"] * 10, se=r.bse["utilization"] * 10, p=r.pvalues["utilization"],
                      n=len(dist), note=f"{dist.district.nunique()} districts, clustered SE"))
    pd.DataFrame(tests).to_csv(OUT / "tests.csv", index=False)

    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.plot(us.index, us.utilization, color="#1f4e79", lw=2, label="Clinker capacity utilized (%, left)")
    ax1.set_ylabel("Percent of kiln capacity used")
    ax1.set_ylim(40, 100)
    ax2 = ax1.twinx()
    ax2.plot(us.index, us.cement_to_readymix_2002, color="#c55a11", lw=2, ls="--",
             label="Cement price ÷ ready-mix price, 2002 = 1 (right)")
    ax2.set_ylabel("Relative price index")
    ax2.set_ylim(0.8, 1.05)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="lower left", frameon=False, fontsize=9)
    ax1.set_title("When US kilns sat idle, cement got cheaper relative to concrete", fontsize=11)
    fig.text(0.01, 0.01, "Sources: USGS Minerals Yearbook (cement), BLS producer price indexes via FRED.", fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "capacity_and_prices.png", dpi=150)
    print("Wrote results/model_linear.csv, plants_2023.csv, state_concentration.csv, state_owner_shares_2023.csv, owners_2023.csv, plant_rivals.csv, "
          "capacity_prices.csv, district_capacity_prices.csv, tests.csv, capacity_and_prices.png")


if __name__ == "__main__":
    main()
