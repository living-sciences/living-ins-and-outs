"""Step 3 / Step 5: Table 1 job-finding vs. employment-exit decomposition.

Footnote 11 of the paper: construct the two hypothetical unemployment rates
    u^f_t = xbar / (xbar + f_t)      (only the job-finding rate varies)
    u^x_t = x_t  / (x_t  + fbar)     (only the exit rate varies)
using full-sample means xbar, fbar of the quarterly rate series; HP-detrend
each and the actual unemployment rate in logs (smoothing 1e5); the slope of a
regression of each detrended hypothetical on the detrended actual rate is the
job-finding / exit-rate contribution.

Mirrors u-v-f-s.nb, which detrends the full series once and then subsets
(Drop[..., z]) for a later-start sub-sample.
"""
import argparse
import json
import os
import numpy as np

from shimer_common import detrend, ols_slope

# Table 1 columns use progressively later start dates. Aliases map the plan's
# labels to (start_year, end_year_inclusive).
ALIASES = {
    "full": None,
    "1948": (1948, 2010),
    "1948b": (1967, 2010),
    "1948c": (1976, 2010),
    "1987": (1987, 2010),
}


def parse_sample(token, dates):
    """Return a boolean mask over `dates` for a sample token."""
    if token in ALIASES:
        spec = ALIASES[token]
    elif "-" in token:
        a, b = token.split("-")
        spec = (int(a), int(b))
    else:
        spec = (int(token), 9999)
    if spec is None:
        return np.ones(len(dates), dtype=bool)
    lo, hi = spec
    return (dates >= lo) & (dates < hi + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", required=True, help="dir with find.dat/sep.dat/urate.q.dat")
    ap.add_argument("--samples", default="full,1987")
    ap.add_argument("--hp", type=float, default=1e5)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    find = np.loadtxt(os.path.join(args.series, "find.dat"))   # rate f_t (quarterly)
    sep = np.loadtxt(os.path.join(args.series, "sep.dat"))     # rate x_t (quarterly)
    urate = np.loadtxt(os.path.join(args.series, "urate.q.dat"))
    dates = find[:, 0]
    fQ, xQ, uQ = find[:, 1], sep[:, 1], urate[:, 1]

    fbar, xbar = fQ.mean(), xQ.mean()
    # hypothetical steady-state unemployment rates
    u_f = xbar / (xbar + fQ)      # only finding varies
    u_x = xQ / (xQ + fbar)        # only exit varies

    d_urate = detrend(uQ, args.hp)
    d_uf = detrend(u_f, args.hp)
    d_ux = detrend(u_x, args.hp)

    out = {}
    for token in [s.strip() for s in args.samples.split(",") if s.strip()]:
        mask = parse_sample(token, dates)
        finding, _ = ols_slope(d_uf[mask], d_urate[mask])
        exit_, _ = ols_slope(d_ux[mask], d_urate[mask])
        out[token] = {
            "finding_contribution": finding,
            "exit_contribution": exit_,
            "sum": finding + exit_,
            "n_quarters": int(mask.sum()),
            "period": f"{dates[mask][0]:.2f}-{dates[mask][-1]:.2f}",
        }
        print(f"[table1] {token}: finding={finding:.4f} exit={exit_:.4f} "
              f"sum={finding+exit_:.4f} n={int(mask.sum())} "
              f"({dates[mask][0]:.2f}-{dates[mask][-1]:.2f})")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print("[table1] wrote", args.out)


if __name__ == "__main__":
    main()
