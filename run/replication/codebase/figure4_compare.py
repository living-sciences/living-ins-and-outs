"""Step 7: Figure 4 cross-check -- two-state probabilities vs three-state
transition probabilities on the overlapping quarterly sample.

Convert the shipped quarterly UE/EU instantaneous rates to full-month
transition probabilities  Lambda^AB = 1 - exp(-lambda^AB)  and compare:
  Lambda^UE  vs  two-state job-finding probability F_t
  Lambda^EU  vs  two-state employment-exit probability X_t
"""
import argparse
import json
import os
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load(path):
    d = np.loadtxt(path)
    return {round(x, 2): y for x, y in zip(d[:, 0], d[:, 1])}


def align(a, b):
    keys = sorted(set(a) & set(b))
    return np.array(keys), np.array([a[k] for k in keys]), np.array([b[k] for k in keys])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--two_state", required=True, help="dir with find_prob.q.dat / sep_prob.q.dat")
    ap.add_argument("--rates", required=True, help="dir with ue.dat / eu.dat")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    F = load(os.path.join(args.two_state, "find_prob.q.dat"))   # two-state F_t (prob)
    X = load(os.path.join(args.two_state, "sep_prob.q.dat"))    # two-state X_t (prob)
    lam_ue = np.loadtxt(os.path.join(args.rates, "ue.dat"))
    lam_eu = np.loadtxt(os.path.join(args.rates, "eu.dat"))
    LUE = {round(x, 2): 1 - np.exp(-y) for x, y in zip(lam_ue[:, 0], lam_ue[:, 1])}
    LEU = {round(x, 2): 1 - np.exp(-y) for x, y in zip(lam_eu[:, 0], lam_eu[:, 1])}

    d1, f, ue = align(F, LUE)
    d2, x, eu = align(X, LEU)

    out = {
        "corr_F_UE": float(np.corrcoef(f, ue)[0, 1]),
        "mean_logdiff_F_UE": float(np.mean(np.log(f) - np.log(ue))),
        "corr_X_EU": float(np.corrcoef(x, eu)[0, 1]),
        "mean_logdiff_X_EU": float(np.mean(np.log(x) - np.log(eu))),
        "overlap_sample": f"{d1[0]:.2f}-{d1[-1]:.2f}",
        "n_quarters": int(len(d1)),
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=2)
    print("[fig4]", json.dumps(out, indent=2))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
    ax1.plot(d1, f, color="C0", label="two-state F (job finding prob.)")
    ax1.plot(d1, ue, color="C1", ls="--", label=r"$\Lambda^{UE}=1-e^{-\lambda^{UE}}$")
    ax1.set_ylabel("job finding probability")
    ax1.legend()
    ax1.set_title("Figure 4: two-state vs three-state transition probabilities")
    ax2.plot(d2, x, color="C3", label="two-state X (employment exit prob.)")
    ax2.plot(d2, eu, color="C2", ls="--", label=r"$\Lambda^{EU}=1-e^{-\lambda^{EU}}$")
    ax2.set_ylabel("employment exit probability")
    ax2.set_xlabel("year")
    ax2.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(args.out) or ".", "figure4.pdf"))
    plt.close(fig)
    print("[fig4] wrote figure4.pdf")


if __name__ == "__main__":
    main()
