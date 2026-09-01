"""Step 4: download the paper's documented monthly BLS series from FRED and
write them in the findsep-style .txt format consumed by run_two_state.py.

Series (seasonally adjusted, thousands):
  UNEMPLOY (LNS13000000) unemployment level     -> unemp.txt
  CE16OV   (LNS12000000) civilian employment    -> emp.txt
  UEMPLT5  (LNS13008396) unemployed < 5 weeks    -> short.txt
"""
import argparse
import os
import datetime
import requests

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv"
NAMEMAP = {
    "UNEMPLOY": ("unemp.txt", "LNS13000000 Seas Adj Unemployment Level (Thousands)"),
    "CE16OV":   ("emp.txt",   "LNS12000000 Seas Adj Employment Level (Thousands)"),
    "UEMPLT5":  ("short.txt", "LNS13008396 Seas Adj Unemployed < 5 Weeks (Thousands)"),
}


def fetch(series_id, start, end):
    cosd = start + "-01"
    coed = end + "-01"
    r = requests.get(FRED, params={"id": series_id, "cosd": cosd, "coed": coed}, timeout=60)
    r.raise_for_status()
    rows = []
    for line in r.text.strip().splitlines()[1:]:
        date, val = line.split(",")
        rows.append((date, val))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default="UNEMPLOY,CE16OV,UEMPLT5")
    ap.add_argument("--start", default="1948-01")
    ap.add_argument("--end", default="2010-12")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    vintage = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    for sid in args.series.split(","):
        sid = sid.strip()
        rows = fetch(sid, args.start, args.end)
        fname, desc = NAMEMAP[sid]
        # raw CSV copy with recorded vintage
        with open(os.path.join(args.out, sid + ".csv"), "w") as f:
            f.write(f"# {sid} downloaded from FRED {vintage}, {args.start}..{args.end}\n")
            f.write("date,value\n")
            for d, v in rows:
                f.write(f"{d},{v}\n")
        # findsep-style: header line then one value per month
        vals = [v for _, v in rows]
        header = (f"{desc}, 16 years and over, {args.start}--{args.end}, "
                  f"Downloaded from FRED {vintage}")
        with open(os.path.join(args.out, fname), "w") as f:
            f.write(header + "\n")
            for v in vals:
                f.write(v + "\n")
        print(f"[fred] {sid}: {len(vals)} months {rows[0][0]}..{rows[-1][0]} -> {fname}")

    print(f"[fred] vintage {vintage}; wrote to {args.out}")


if __name__ == "__main__":
    main()
