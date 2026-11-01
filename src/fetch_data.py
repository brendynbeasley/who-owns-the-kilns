"""Download the public data this repository uses into data/raw/.

Everything fetched here is already committed, so the analysis runs offline. Run this only to refresh
or to check the files against their sources. Sources:

  EPA Greenhouse Gas Reporting Program (Envirofacts API, data.epa.gov/efservice):
    every US cement kiln plant (subpart H), its parent companies with ownership shares, and its
    subpart H carbon dioxide, 2010-2023.
  USGS Minerals Yearbook, cement chapter tables, 2002-2023 (one spreadsheet per year).
  BLS producer price indexes via FRED: cement manufacturing (PCU327310327310) and ready-mix
    concrete manufacturing (PCU327320327320), monthly from 1965.

Usage (from the repository root):
    python src/fetch_data.py
"""

import io
import json
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
UA = {"User-Agent": "Brendyn Beasley research 83249437+brendynbeasley@users.noreply.github.com"}

EF = "https://data.epa.gov/efservice"
H_SUBPART_ID = 6          # GHGRP subpart H = cement production (PUB_DIM_SUBPART)
YEARS = range(2010, 2024)  # GHGRP reporting years published for cement as of November 2026

S3 = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production"
USGS_MYB = {
    2002: f"{S3}/mineral-pubs/cement/cememyb02.xls",
    2003: f"{S3}/mineral-pubs/cement/cemenmyb03.xls",
    2004: f"{S3}/mineral-pubs/cement/cemenmyb04.xls",
    2005: f"{S3}/mineral-pubs/cement/cemenmyb05.xls",
    2006: f"{S3}/atoms/files/myb1-2006-cemen.xls",
    2007: f"{S3}/atoms/files/myb1-2007-cemen.xls",
    2008: f"{S3}/atoms/files/myb1-2008-cemen.xls",
    2009: f"{S3}/atoms/files/myb1-2009-cemen.xls",
    2010: f"{S3}/atoms/files/myb1-2010-cemen.xls",
    2011: f"{S3}/atoms/files/myb1-2011-cemen.xls",
    2012: f"{S3}/atoms/files/myb1-2012-cemen.xls",
    2013: f"{S3}/atoms/files/myb1-2013-cemen.xlsx",
    2014: f"{S3}/atoms/files/myb1-2014-cemen.xlsx",
    2015: "https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/atoms/files/myb1-2015-cemen.xlsx",
    2016: "https://d9-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/atoms/files/myb1-2016-cement.xls",
    2017: f"{S3}/atoms/files/myb1-2017-cemen.xls",
    2018: "https://pubs.usgs.gov/myb/vol1/2018/myb1-2018-cement.xlsx",
    2019: "https://pubs.usgs.gov/myb/vol1/2019/myb1-2019-cement.xlsx",
    2020: f"{S3}/s3fs-public/media/files/myb1-2020-cemen-adv2.xlsx",
    2021: f"{S3}/s3fs-public/media/files/myb1-2021-cemen-ert.xlsx",
    2022: f"{S3}/s3fs-public/media/files/myb1-2022-cemen-ert.xlsx",
    2023: f"{S3}/s3fs-public/media/files/myb1-2023-cemen-ERT.xlsx",
}
FRED = {"cement": "PCU327310327310", "readymix": "PCU327320327320"}


def get(url, tries=4):
    for k in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=180)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            print(f"  retry {k + 1} after error: {e}")
            time.sleep(3 * (k + 1))
    raise RuntimeError(f"could not fetch {url}")


def envirofacts(path, page=5000):
    """Page through an Envirofacts table query and return all rows."""
    rows, start = [], 0
    while True:
        batch = get(f"{EF}/{path}/ROWS/{start}:{start + page - 1}/JSON").json()
        rows += batch
        if len(batch) < page:
            return rows
        start += page


def fetch_ghgrp():
    emis = pd.DataFrame(envirofacts(f"PUB_FACTS_SUBP_GHG_EMISSION/SUB_PART_ID/=/{H_SUBPART_ID}"))
    emis = emis[emis.year.isin(YEARS)]
    print(f"GHGRP subpart H emission rows: {len(emis)} ({emis.facility_id.nunique()} plants)")
    emis.to_csv(RAW / "ghgrp_subpart_h_emissions.csv", index=False)

    fac = pd.DataFrame(envirofacts("PUB_DIM_FACILITY/NAICS_CODE/=/327310"))
    missing = sorted(set(emis.facility_id) - set(fac.facility_id))
    for fid in missing:  # a few kiln plants report a different primary NAICS code
        fac = pd.concat([fac, pd.DataFrame(envirofacts(f"PUB_DIM_FACILITY/FACILITY_ID/=/{fid}"))])
        time.sleep(0.3)
    keep = ["facility_id", "year", "facility_name", "parent_company", "city", "state", "county",
            "county_fips", "latitude", "longitude", "naics_code", "reported_subparts"]
    fac = fac[fac.facility_id.isin(emis.facility_id) & fac.year.isin(YEARS)][keep]
    print(f"GHGRP facility-year rows for those plants: {len(fac)} ({len(missing)} looked up by id)")
    fac.sort_values(["facility_id", "year"]).to_csv(RAW / "ghgrp_cement_facilities.csv", index=False)


def fetch_usgs():
    out = RAW / "usgs_myb"
    out.mkdir(exist_ok=True)
    for year, url in USGS_MYB.items():
        ext = url.rsplit(".", 1)[1]
        (out / f"cement_myb_{year}.{ext}").write_bytes(get(url).content)
    print(f"USGS: {len(USGS_MYB)} yearbook files")


def fetch_fred():
    for name, sid in FRED.items():
        df = pd.read_csv(io.StringIO(get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}").text))
        df.to_csv(RAW / f"fred_{sid}.csv", index=False)
        print(f"FRED {sid} ({name}): {len(df)} months, {df.iloc[0, 0]} to {df.iloc[-1, 0]}")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    fetch_ghgrp()
    fetch_usgs()
    fetch_fred()
    (RAW / "SOURCES.json").write_text(json.dumps({
        "downloaded": time.strftime("%Y-%m-%d"),
        "ghgrp": EF, "usgs_yearbook": USGS_MYB,
        "fred": {k: f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={v}" for k, v in FRED.items()},
    }, indent=1))


if __name__ == "__main__":
    main()
