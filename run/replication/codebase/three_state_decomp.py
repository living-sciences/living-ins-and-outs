"""Step 6: three-state (E/U/I) decomposition -- second half of three-state.nb.

Entry point = the shipped quarterly instantaneous-rate series ei/eu/ie/iu/ue/ui
.dat (already time-aggregated lambda's; the upstream construction of lambda from
monthly CPS gross-flow probabilities needs ~42GB microdata + Stata, absent here).

Steady state (paper p.13):
  sse (e) = lam_iu lam_ue + lam_ui lam_ie + lam_ue lam_ie
  ssu (u) = lam_ei lam_iu + lam_ie lam_eu + lam_iu lam_eu
  ssi (i) = lam_eu lam_ui + lam_ue lam_ei + lam_ui lam_ei
  urate = ssu/(ssu+sse)          emp/pop = sse/(ssi+ssu+sse)
Six single-rate hypotheticals (eq. 7/8): only one lambda varies, the other five
held at their 1967-2010 means. Table 2 = OLS slope of each detrended hypothetical
on the detrended actual measured rate (footnote 20 / Table 2 note).
"""
import argparse
import json
import os
import numpy as np
import requests

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shimer_common import detrend, ols_slope, quarterly_avg

RATES = ["ei", "eu", "ie", "iu", "ue", "ui"]


def steady_state(L):
    """L: dict name->array. Returns (u,e,i) steady-state numerators (times const k)."""
    sse = L["iu"] * L["ue"] + L["ui"] * L["ie"] + L["ue"] * L["ie"]
    ssu = L["ei"] * L["iu"] + L["ie"] * L["eu"] + L["iu"] * L["eu"]
    ssi = L["eu"] * L["ui"] + L["ue"] * L["ei"] + L["ui"] * L["ei"]
    return ssu, sse, ssi


def hypothetical(lams, vary):
    """Only lambda[vary] varies; the other five fixed at their sample means."""
    L = {k: (v if k == vary else np.full_like(v, v.mean())) for k, v in lams.items()}
    ssu, sse, ssi = steady_state(L)
    return ssu / (ssu + sse), sse / (ssi + ssu + sse)  # urate, emppop hypotheticals


def fetch_fred_monthly(series_id, cache):
    if os.path.exists(cache):
        arr = []
        with open(cache) as f:
            for ln in f.read().strip().splitlines()[1:]:
                arr.append(float(ln.split(",")[1]))
        return np.array(arr)
    r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv",
                     params={"id": series_id, "cosd": "1948-01-01", "coed": "2010-12-01"},
                     timeout=60)
    r.raise_for_status()
    lines = r.text.strip().splitlines()[1:]
    with open(cache, "w") as f:
        f.write("date,value\n")
        for ln in lines:
            f.write(ln + "\n")
    return np.array([float(ln.split(",")[1]) for ln in lines])


def measured_series(fred_dir):
    """Return dict date->urate and date->emppop, quarterly-averaged (calendar Q from 1948M1)."""
    def load_txt(name):
        with open(os.path.join(fred_dir, name)) as f:
            lines = f.read().strip().splitlines()[1:]
        return np.array([float(x) for x in lines])
    unemp = load_txt("unemp.txt")
    emp = load_txt("emp.txt")
    urate_m = unemp / (unemp + emp)
    emratio_m = fetch_fred_monthly("EMRATIO", os.path.join(fred_dir, "EMRATIO.csv")) / 100.0
    urate_q = quarterly_avg(urate_m)
    emppop_q = quarterly_avg(emratio_m)
    dates = 1948.0 + np.arange(len(urate_q)) / 4.0
    ur = {round(d, 2): v for d, v in zip(dates, urate_q)}
    ep = {round(d, 2): v for d, v in zip(dates, emppop_q)}
    return ur, ep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rates", required=True, help="dir with ei/eu/ie/iu/ue/ui .dat")
    ap.add_argument("--fred", default="output/fred", help="dir with unemp.txt/emp.txt for measured refs")
    ap.add_argument("--hp", type=float, default=1e5)
    ap.add_argument("--samples", default="full,1987")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    lams = {}
    dates = None
    for name in RATES:
        d = np.loadtxt(os.path.join(args.rates, name + ".dat"))
        lams[name] = d[:, 1]
        if dates is None:
            dates = d[:, 0]
    print(f"[3state] loaded lambda's, {len(dates)} quarters {dates[0]}-{dates[-1]}")

    # baseline steady-state (all rates vary)
    ssu, sse, ssi = steady_state(lams)
    ss_urate = ssu / (ssu + sse)
    ss_emppop = sse / (ssi + ssu + sse)

    # six single-rate hypotheticals
    hyp_urate = {}
    hyp_emppop = {}
    for r in RATES:
        hu, he = hypothetical(lams, r)
        hyp_urate[r] = hu
        hyp_emppop[r] = he

    # measured actual references, aligned by quarterly date
    ur_map, ep_map = measured_series(args.fred)
    keys = [round(d, 2) for d in dates]
    act_urate = np.array([ur_map[k] for k in keys])
    act_emppop = np.array([ep_map[k] for k in keys])

    corr_ss_urate = float(np.corrcoef(ss_urate, act_urate)[0, 1])
    print(f"[3state] corr(steady-state urate, measured urate) = {corr_ss_urate:.4f}")

    # detrend everything once on the full sample
    d_act_u = detrend(act_urate, args.hp)
    d_act_e = detrend(act_emppop, args.hp)
    d_hyp_u = {r: detrend(hyp_urate[r], args.hp) for r in RATES}
    d_hyp_e = {r: detrend(hyp_emppop[r], args.hp) for r in RATES}

    def sample_mask(token):
        if token == "full":
            return np.ones(len(dates), dtype=bool)
        yr = int(token)
        return dates >= yr

    result = {"urate": {}, "emp_pop_ratio": {}, "corr_ss_urate": corr_ss_urate,
              "sample_span": f"{dates[0]:.2f}-{dates[-1]:.2f}",
              "reference": "measured u/(u+e) and EMRATIO from FRED, quarterly-averaged",
              "engine": "python-port-of-three-state.nb (2nd half); lambda entry point = shipped .dat"}

    for token in [s.strip() for s in args.samples.split(",") if s.strip()]:
        m = sample_mask(token)
        uslopes, eslopes = {}, {}
        for r in RATES:
            su, _ = ols_slope(d_hyp_u[r][m], d_act_u[m])
            se, _ = ols_slope(d_hyp_e[r][m], d_act_e[m])
            uslopes[r.upper()] = su
            eslopes[r.upper()] = se
        result["urate"][token] = uslopes
        result["emp_pop_ratio"][token] = eslopes
        print(f"[3state] sample {token} (n={int(m.sum())}):")
        print("   urate:  ", {k: round(v, 3) for k, v in uslopes.items()},
              " sum=", round(sum(uslopes.values()), 3))
        print("   emppop: ", {k: round(v, 3) for k, v in eslopes.items()},
              " sum=", round(sum(eslopes.values()), 3))

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print("[3state] wrote", args.out)

    # ---- Figure 5: six hypothetical urate series vs actual measured urate ----
    labels = {"ei": "EI", "eu": "EU", "ie": "IE", "iu": "IU", "ue": "UE", "ui": "UI"}
    fig, axes = plt.subplots(3, 2, figsize=(11, 11), sharex=True)
    order = ["ue", "eu", "ui", "iu", "ie", "ei"]
    for ax, r in zip(axes.flat, order):
        ax.plot(dates, act_urate, color="0.5", lw=1.2, label="actual urate")
        ax.plot(dates, hyp_urate[r], color="C3", lw=1.2, label=f"only {labels[r]} varies")
        ax.set_title(f"{labels[r]} transition rate")
        ax.legend(fontsize=8)
        ax.set_ylabel("unemployment rate")
    for ax in axes[-1]:
        ax.set_xlabel("year")
    fig.suptitle("Figure 5: single-transition-rate hypothetical unemployment rates vs actual")
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(args.out) or ".", "figure5.pdf"))
    plt.close(fig)
    print("[3state] wrote figure5.pdf")


if __name__ == "__main__":
    main()
