# Follow-up 002 — Calibrated theory update for Shimer (2012), to 2026

## Question

Seeded from the completed replication and from follow-up 001 (which re-estimated
Shimer's "Ins and Outs of Unemployment" through 2026), produce a **calibrated,
updated theory** a 2026 version of the paper would carry: recalibrate the paper's
own flow model on the latest data, make the **smallest** amendment that reconciles
the original findings with the new evidence (notably the 2020 separation shock and
the secular decline of the flows), validate it out-of-sample, and label every
claim by its epistemic status. Deliver a written theory section, a paper-era-vs-
2026 calibration table, a figure, and the result card.

## Approach

**Reused (no re-fetching, no re-running the original pipeline):** 001's monthly
and quarterly constructed series (`series_monthly.csv`, `quarterly_series.csv` —
F_t, X_t, f_t, x_t, the six three-state Λ's, FRED vintage 2026-08-24), 001's
window decomposition estimates (`estimates_by_window.csv`, Newey–West), and the
seeded replication's exact HP-filter port (`shimer_common.hp_trend`). I ran only
new **estimation + calibration** on those series (`workspace/analyze.py`,
`workspace/finalize.py`).

**New work.** (1) Re-estimated the paper's *central* parameters by era — mean F̄,
X̄, the adjustment speed ω = F̄+X̄, the implied persistence ρ = 1−ω and half-life,
the implied steady-state u\*, and the steady-state-approximation quality corr(u,u\*).
(2) Formalized a **regime-switching amendment**: a rare layoff regime identified
from the separation-rate deviation x̂_t, with an estimated regime probability π_L
and regime-conditional β_F anchored on 001's robust windows. (3) Validated it:
an out-of-sample regime classifier (calibrate pre-2015, test 2015–2026) and a
per-recession monthly finding-vs-separation decomposition showing 2020 is the lone
episode the constant-β model cannot produce. (4) Wrote the theory section
(`results/theory_update.md`) with [ESTIMATED]/[CALIBRATED]/[PROPOSED] labels.

## Results

**Recalibration (paper-era → 2026), all [ESTIMATED] unless noted, from 001's
monthly series:**

| Parameter | 1948–2010 | 2026 | Source |
|---|---|---|---|
| Mean F̄ | 0.440 | 0.321 | `era_calibration_full.csv` |
| Mean X̄ | 0.033 | 0.021 | `era_calibration_full.csv` |
| Adjustment speed ω=F̄+X̄ | 0.473 | 0.342 | this study |
| Persistence ρ=1−ω [CALIBRATED] | 0.527 | 0.658 | this study |
| Half-life (months) [CALIBRATED] | 1.08 | 1.66 | this study |
| Implied steady-state u\* | 0.071 | 0.062 | this study |
| corr(u, u\*) | 0.945 | 0.924 | this study |

The secular decline Shimer flagged in X̄ *continued* (and F̄ fell too); their sum,
the monthly convergence speed, fell 28%, so unemployment is now materially more
persistent (half-life +53%) and the steady-state approximation weaker — degrading
to corr 0.75 within the 2020 episode. With the clipped March-2020 point kept, the
recent-era corr spuriously collapses to 0.24 (known data artifact; dropped).

**The regime amendment (the intellectual step):**

| Regime | β_F | 3-state λ^EU (separations) | Source |
|---|---|---|---|
| Normal (1987–2019) | **0.90** | 0.16 | 001 `estimates_by_window.csv` |
| Normal, recent (2010–2026 excl-2020) | **0.84** | 0.17 | 001 |
| Layoff-inclusive (2010–2026 incl-2020) | **0.54** | **0.55** | 001 |

The extreme layoff regime has **π_L = 0.0021** (2 months in 940: March–April
2020) [ESTIMATED]. 2020's monthly separation deviation peaked at **4.2× the entire
pre-2015 record** (x̂ = 1.66 vs 0.39). A mixture
`β_F ≈ (1−π_L)β_F^N + π_L β_F^L` reconciles the "holds" and "flips" readings
without deleting 2020.

**Validation.**
- *OOS classifier:* trained on pre-2015 (threshold = the pre-2015 separation-
  deviation maximum), it flags **exactly March–April 2020** in 2015–2026 and
  nothing else — no false positives in the 2015–19 expansion or 2021–26 recovery.
- *Episode decomposition (monthly):* the separation share of the unemployment
  surge is **0.81 in 2020** vs **0.17 in 2008** and ≤ 0.27 in every recession
  since 1990; the separation-only hypothetical u peaked at **0.164 in 2020 vs
  ≤ 0.084 in every other postwar recession**. The constant model predicts ≈ 0.16
  everywhere and cannot generate 2020; 2008's 0.17 confirms the original story
  out of sample, so the amendment adds a *rare* regime without disturbing the fit
  elsewhere. (Figure Panel A.)

**Comparison to the original / replication baseline** (original values read from
disk, cited below):

| Quantity | Original | This study | Source of original |
|---|---|---|---|
| β_F headline (1948–2010) | 0.763 | recalibrated context, unchanged | `replication/codebase/output/table1_1948_2010.json` (via 001) |
| Mean X̄ (secular level) | 0.0334 (1948–2010) | 0.0211 (2010–2026) | 001 `c2_descriptive.json` / this study |
| β_F 2010–2026 incl-2020 | 0.538 | used as layoff anchor | 001 `estimates_by_window.csv` |
| 3-state λ^EU normal→2020 | 0.164 → 0.551 | used as regime anchor | 001 `estimates_by_window.csv` |
| Steady-state corr (paper) | ≈0.99 monthly (paper §2) | 0.945 (1948–2010 qtrly-avg), 0.75 in 2020 | paper text / this study |

## Deviations & limitations

- **No likelihood-based Markov-switching estimation** was run (compute-modest
  instruction). π_L is a frequency and the regime β's are the paper's own OLS
  decomposition on regime subsamples/001 windows — calibration to moments 001 had
  already produced. Stated plainly per the instruction's fallback clause.
- **β_F^L magnitude is calibrated, not predicted OOS.** 2020 is the only extreme
  layoff episode on record, so its *size* is fit to the 2020-inclusive windows.
  The out-of-sample content is the *classifier* (which months are the regime) and
  the *qualitative flip*; the un-predictability of the magnitude is itself the
  tail-risk finding. My initial naïve quarterly mixture under-predicted the
  2015–26 β_F flip for exactly this reason — reported honestly, not hidden.
- **2020 is a sub-quarterly event**; the analysis is deliberately monthly, and the
  clipped March F-point is handled with a clip-immune separation hypothetical (per
  the noted data artifact).
- **Levels of F̄, X̄** carry the duration-misreporting caveat inherited from 001;
  the ratio-based ω, ρ, u\* objects are more robust than the levels.
- **C4-style demographic heterogeneity** is untouched (needs CPS microdata; out of
  scope, as in 001).

## Artifacts (`results/`)

`theory_update.md` (the written section), `calibration_table.csv`,
`episode_decomposition.csv`, `regime_estimates.csv`, `era_calibration_full.csv`,
`fig1_theory_update.png` / `.pdf`. Reproduce with
`workspace/analyze.py` then `workspace/finalize.py`.
