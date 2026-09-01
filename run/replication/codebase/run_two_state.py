"""Step 2 / Step 4: two-state job-finding & employment-exit construction.

Python port of the computational path in findsep/u-v-f-s.nb (no Wolfram kernel
available in this environment). Follows the notebook exactly:

  F_t (eq. 4)  = 1 - (u_{t+1} - u^s_{t+1}) / u_t
  f_t          = -log(1 - F_t)
  x_t (eq. 5)  : root of  u_{t+1} = (1-e^{-f_t-x}) x (u_t+e_t)/(f_t+x) + e^{-f_t-x} u_t
  X_t          = 1 - e^{-x_t}
  X~_t (eq. 6) = u^s_{t+1} / e_t          (time-aggregation-ignoring exit prob)
then 3-month quarterly averages.
"""
import argparse
import json
import os
import numpy as np
from scipy.optimize import brentq

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shimer_common import (
    detrend, quarterly_avg, quarterly_sum, date_q, write_dat,
    read_header_series,
)


def load_inputs(data_dir, start, shortadj_path=None, splice_tail=False):
    """Load monthly series and build the CPS-redesign-adjusted short-term series.

    splice_tail=True: after the microdata-share window ends, continue the
    short-term-unemployment series with the *published* level (used for
    2005M2-2010M12 in step 4, where CPS-microdata shares are unavailable).
    """
    def find(name):
        p = os.path.join(data_dir, name)
        return p if os.path.exists(p) else None

    _, unemp = read_header_series(find("unemp.txt"))
    _, emp = read_header_series(find("emp.txt"))
    _, short = read_header_series(find("short.txt"))
    help_path = find("helpwant.txt")
    if help_path is not None:
        _, helpw = read_header_series(help_path)
    else:
        helpw = None

    if shortadj_path is None:
        shortadj_path = find("shortadj.txt")
    _, shares = read_header_series(shortadj_path)

    # Appendix-A adjustment: published short-term for months before 1976M1,
    # microdata share * unemployment level from 1976M1 on.
    off = 12 * (1976 - start)  # index of 1976M1 (0-based)
    prefix = short[:off]
    adj = shares * unemp[off:off + len(shares)]
    if splice_tail:
        tail = short[off + len(shares):]  # published level for months past the share window
        shortadj = np.concatenate([prefix, adj, tail])
    else:
        shortadj = np.concatenate([prefix, adj])

    # longest common available sample
    lengths = [len(unemp), len(emp), len(shortadj)]
    if helpw is not None:
        lengths.append(len(helpw))
    available = min(lengths)
    unemp = unemp[:available]
    emp = emp[:available]
    shortadj = shortadj[:available]
    if helpw is not None:
        helpw = helpw[:available]
    yrs = (available - 1) // 12
    stop_year = start + yrs
    stop_month = available - 12 * yrs
    return dict(unemp=unemp, emp=emp, shortadj=shortadj, help=helpw,
                available=available, stop=(stop_year, stop_month))


def solve_exit_rate(u_t, u_next, e_t, f_t, guess=0.03):
    """Root of eq. (5) for the monthly exit rate x."""
    def g(s):
        return ((1 - np.exp(-f_t - s)) * s * (u_t + e_t) / (f_t + s)
                + np.exp(-f_t - s) * u_t - u_next)
    lo, hi = 1e-12, 10.0
    glo, ghi = g(lo), g(hi)
    if glo * ghi < 0:
        return brentq(g, lo, hi, xtol=1e-12, rtol=1e-12)
    # fallback: Newton from the notebook's 0.03 guess
    from scipy.optimize import newton
    return float(newton(g, guess))


def construct(inp, smooth):
    unemp, emp, shortadj = inp["unemp"], inp["emp"], inp["shortadj"]
    n = len(unemp)

    # unemployment rate led one period: u_{t+1}/l_{t+1}
    UrateM = (unemp / (unemp + emp))[1:]

    # eq (4): job finding probability and rate
    FindM = 1.0 - (unemp[1:] - shortadj[1:]) / unemp[:-1]
    findM = -np.log(1.0 - FindM)

    # eq (5): exit rate by root finding, then exit probability
    sepM = np.array([solve_exit_rate(unemp[t], unemp[t + 1], emp[t], findM[t])
                     for t in range(n - 1)])
    SepM = 1.0 - np.exp(-sepM)

    # eq (6) naive (time-aggregation-ignoring) exit probability: u^s_{t+1}/e_t
    XtildeM = shortadj[1:] / emp[:-1]

    # quarterly aggregates
    findQ = quarterly_avg(findM)       # rate  -> find.dat (matches shipped)
    sepQ = quarterly_avg(sepM)         # rate  -> sep.dat
    UrateQ = quarterly_avg(UrateM)
    FindQp = quarterly_avg(FindM)      # probability
    SepQp = quarterly_avg(SepM)        # probability
    XtildeQ = quarterly_avg(XtildeM)
    UnempQ = quarterly_sum(unemp)

    return dict(FindM=FindM, findM=findM, sepM=sepM, SepM=SepM, XtildeM=XtildeM,
                UrateM=UrateM, findQ=findQ, sepQ=sepQ, UrateQ=UrateQ,
                FindQp=FindQp, SepQp=SepQp, XtildeQ=XtildeQ, UnempQ=UnempQ)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--shortadj", default=None)
    ap.add_argument("--start", type=int, default=1951)
    ap.add_argument("--hp", type=float, default=1e5)
    ap.add_argument("--out", required=True)
    ap.add_argument("--splice_tail", action="store_true",
                    help="continue short-term series with published level past the share window")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    inp = load_inputs(args.data, args.start, args.shortadj, splice_tail=args.splice_tail)
    print("[two_state] Python port of u-v-f-s.nb (no Wolfram kernel).")
    print("[two_state] available months=%d, sample %d:M1 -> %d:M%d"
          % (inp["available"], args.start, inp["stop"][0], inp["stop"][1]))

    r = construct(inp, args.hp)
    start = args.start

    write_dat(os.path.join(args.out, "find.dat"), date_q(r["findQ"], start))
    write_dat(os.path.join(args.out, "sep.dat"), date_q(r["sepQ"], start))
    write_dat(os.path.join(args.out, "xtilde.q.dat"), date_q(r["XtildeQ"], start))
    write_dat(os.path.join(args.out, "urate.q.dat"), date_q(r["UrateQ"], start))
    # probability versions (used by figures / downstream figure4 comparison)
    write_dat(os.path.join(args.out, "find_prob.q.dat"), date_q(r["FindQp"], start))
    write_dat(os.path.join(args.out, "sep_prob.q.dat"), date_q(r["SepQp"], start))

    # ---- summary statistics ----
    ss_month = r["sepM"] / (r["sepM"] + r["findM"])
    corr_urate_ss = float(np.corrcoef(r["UrateM"], ss_month)[0, 1])

    summary = dict(
        mean_F=float(np.mean(r["FindM"])),
        mean_X=float(np.mean(r["SepM"])),
        F_peak_to_trough_logpoints=float(np.log(r["FindQp"].max())
                                          - np.log(r["FindQp"].min())),
        sd_detrended_X=float(np.std(detrend(r["SepQp"], args.hp), ddof=0)),
        sd_detrended_Xtilde=float(np.std(detrend(r["XtildeQ"], args.hp), ddof=0)),
        corr_urate_ss=corr_urate_ss,
        # validation extras vs. notebook printed values
        corr_findQ_urateQ=float(np.corrcoef(detrend(r["findQ"], args.hp),
                                            detrend(r["UrateQ"], args.hp))[0, 1]),
        corr_sepQ_urateQ=float(np.corrcoef(detrend(r["sepQ"], args.hp),
                                           detrend(r["UrateQ"], args.hp))[0, 1]),
        n_quarters=int(len(r["findQ"])),
        sample=f"{start}:M1-{inp['stop'][0]}:M{inp['stop'][1]}",
        engine="python-port-of-u-v-f-s.nb",
    )
    with open(os.path.join(args.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("[two_state] summary:", json.dumps(summary, indent=2))

    # ---- Figure 1: F (top); X and X~ (bottom) ----
    dates = start + np.arange(len(r["findQ"])) / 4.0
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    ax1.plot(dates, r["FindQp"], color="C0")
    ax1.set_ylabel("F  (job finding prob.)")
    ax1.set_title("Figure 1: job finding probability F (top); exit probabilities X, X~ (bottom)")
    ax2.plot(dates, r["SepQp"], color="C3", label="X (exit prob.)")
    ax2.plot(dates, r["XtildeQ"], color="C2", ls="--", label="X~ (naive, u^s/e)")
    ax2.set_ylabel("employment exit prob.")
    ax2.set_xlabel("year")
    ax2.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "figure1.pdf"))
    plt.close(fig)

    # ---- Figure 2: F and X against the unemployment rate ----
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(11, 4.5))
    axa.scatter(r["UrateQ"], r["FindQp"], s=12, color="C0")
    axa.set_xlabel("unemployment rate")
    axa.set_ylabel("F (job finding prob.)")
    axa.set_title("F vs. unemployment rate")
    axb.scatter(r["UrateQ"], r["SepQp"], s=12, color="C3")
    axb.set_xlabel("unemployment rate")
    axb.set_ylabel("X (exit prob.)")
    axb.set_title("X vs. unemployment rate")
    fig.tight_layout()
    fig.savefig(os.path.join(args.out, "figure2.pdf"))
    plt.close(fig)
    print("[two_state] wrote figures + dat files to", args.out)


if __name__ == "__main__":
    main()
