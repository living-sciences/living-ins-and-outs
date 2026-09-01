# Follow-up study: Living update of Shimer (2012) through 2026

## Question

Shimer (2012), "Reassessing the Ins and Outs of Unemployment" (RED 15(2)),
estimated on 1948–2010 (two-state) and 1967–2010 (three-state) CPS data that
fluctuations in the **job-finding rate** account for roughly three-quarters of
U.S. unemployment-rate fluctuations, a share that **rises over time** to ~0.90 in
the most recent decades, while the **employment-exit (separation) rate** is much
less cyclical and declines secularly after the mid-1980s. This follow-up
re-estimates the paper's headline claims (C1 job-finding share; C2 the level/
cyclicality of F and X; C3 the three-state gross-flows decomposition) on data
**through mid-2026** and produces an over-time visualization of how the findings
evolved. Claim C4 (demographic heterogeneity) is explicitly out of scope — it
requires matched CPS microdata.

## Approach

**Reused from the seeded replication** (`/workspace/eval/replication/codebase/`):
the eq.(5) employment-exit root-finder (`solve_exit_rate`), the HP-detrend
convention, and the cofactor steady-state formulas for the three-state
decomposition. The seeded code's eq.(4)/(5) construction was validated there
against the shipped Mathematica notebooks to machine precision, so I built on it
rather than re-deriving.

**New / changed for the update:**
1. `fetch_all.py` — pulls all 13 FRED series (3 stocks + mean-duration check + 9
   gross-flows) via the keyless `fredgraph.csv` endpoint, preserving missing
   months as NaN (no interpolation).
2. `two_state.py` — re-implements the Part-1 pipeline to the follow-up spec,
   which differs from the replication in three ways the spec dictates:
   (a) the **1.1 CPS-redesign factor** on `UEMPLT5` from 1994-01 (the replication
   used shipped microdata shares 1976–2005 + published levels 2005–2010);
   (b) **within-window** HP detrending (the notebook detrended once on the full
   sample then subset); (c) **Newey–West(8)** standard errors. Adds the 2020-03
   clip rule and NaN-quarter dropping for the 2025 shutdown gap.
3. `three_state.py` — builds monthly 3×3 transition matrices from the live BLS
   flows and applies the eigenvalue time-aggregation correction (the microdata
   step the replication could not run; it had used the shipped 1967–2004 λ files).
4. Windows: the paper's four anchor columns (→2010), the same four extended to
   2026, pre-COVID (1987–2019), fully-post-paper (2010–2026), 1948–2019, each
   2020-spanning window computed both incl- and excl-2020; plus 20-year rolling
   windows stepped one quarter (1948Q1–1967Q4 … ending 2026Q2).

The 1948–2010 and 1987–2010 anchors were run and checked **first**; they passed
(below) before any extension.

## Results

### Anchor replication (gate) — passed, and closer to the paper than the seeded run

| Window | paper β_F/β_X | this study β_F/β_X | seeded replication β_F/β_X |
|---|---|---|---|
| 1948–2010 | 0.77 / 0.24 | **0.769 / 0.238** | 0.763 / 0.245 |
| 1967–2010 | 0.83 / 0.17 | **0.831 / 0.173** | 0.807 / 0.198 |
| 1976–2010 | 0.85 / 0.15 | **0.847 / 0.155** | 0.838 / 0.166 |
| 1987–2010 | 0.90 / 0.10 | **0.898 / 0.107** | 0.858 / 0.144 |

All four within ±0.01 of the paper. Mean F 1948–2010 = 0.4395 (paper 0.44;
matches the spec dry-run of 0.440); mean X = 0.0334 (paper 0.034). Seeded values
from `output/table1_1948_2010.json`; the 1.1-factor spec reproduces the paper's
later columns more tightly than the replication's published-tail splice did.

### C1 — job-finding share through 2026

Excluding the 2020 COVID quarters, the paper's finding **holds and slightly
strengthens**. β_F extended to 2026-Q2 (excl-2020): 0.79 (1948–), 0.85 (1967–),
0.86 (1976–), **0.89 (1987–)**. The fully-post-paper 2010–2026 window gives
β_F = 0.84 (excl-2020). Rolling 20-year β_F sits at ~0.90 for every window ending
after ~2000 and stays there through 2026 (figure, Panel A).

### C1/COVID — including 2020 flips the result to separations

The 2020 recession was a layoff shock. Incl-2020, the **2010–2026** window flips
to β_F = 0.54 / β_X = **0.38** — the one recent episode where "the ins won."
Every 2020-spanning window shows a lower β_F / higher β_X when 2020 is kept.
Post-2021 reverts to job-finding dominance (excl-2020 keeps 2021–2026 and returns
to β_F ≈ 0.84–0.89).

### C2 — levels and the secular exit-rate decline

Mean F fell from 0.440 (1948–2010) to 0.328 (2011–2026); mean X from 0.0334 to
0.0205. Levels carry the duration-misreporting caveat. The secular decline in the
exit probability **continued** post-COVID (linear trend 2010–2026 = −0.00035/yr,
p < 1e-20); outside the 2020 spike, X_t remains quantitatively irrelevant.

### C3 — three-state confirmation

1990–2010 overlap matches Table 2's 1987–2010 column: UE **0.52** (paper 0.51),
EU **0.168** (0.17), UI 0.152 (0.16), IU 0.115 (0.13), IE 0.079 (0.09),
EI −0.034 (−0.05); UE ≈ half, EU < a quarter. Same COVID flip as two-state:
2010–2026 UE 0.42→0.15, EU 0.17→0.55 when 2020 is included. All months passed the
real/positive/distinct-eigenvalue check.

### Comparison table (original vs. update)

| Quantity | Original (source) | This study | Note |
|---|---|---|---|
| β_F 1948–2010 | 0.763 (`table1_1948_2010.json`) | 0.769 | anchor; both ≈ paper 0.77 |
| β_F 1987–2010 | 0.858 (`table1_1948_2010.json`) | 0.898 | 1.1-factor closer to paper 0.90 |
| β_F 1987–2026 excl-2020 | — (post-paper) | 0.892 | claim holds to 2026 |
| β_F 2010–2026 incl-2020 | — | 0.538 | COVID = separation shock |
| 3-state UE 1990–2010 | 0.504 for 1967–2004 (`table2.json`) | 0.520 | ≈ paper 0.49–0.51 |

## Deviations & limitations

- **Redesign adjustment differs from the seeded replication by design:** the spec
  mandates the ×1.1 factor from 1994-01 (Appendix-A fn 38); the replication used
  microdata shares + a published-level tail. This is the intended method for a
  living update and reproduces the anchors better. Maintained as an assumption
  post-2010.
- **Within-window detrending & Newey–West(8) SEs** replace the replication's
  detrend-once-then-subset + plain OLS, per the spec. For the full-sample anchor
  the two detrend approaches coincide.
- **Three-state cannot extend before 1990** (BLS flows start 1990-02); it tests
  the recent-decades conclusion only. Flows are not margin-error adjusted.
- **2025 shutdown gap** (stocks miss 2025-10; flows miss 2025-10/11) and the
  **2020-03 clip** are flagged, never interpolated; affected quarters dropped.
- **C4 not updated** — needs matched CPS microdata (tens of GB); left for a human.

## Artifacts (`results/`)

`living_update.png`/`.pdf` (flagship two-panel figure), `fig2_window_comparison.png`,
`estimates_by_window.csv` (68 rows, two- and three-state), `rolling_estimates.csv`
(261 rows), `series_monthly.csv` (943 months, incl. six Λ^AB), `findings.md`
(one-page write-up), plus `c2_descriptive.json`, `three_state_estimates.csv`,
`quarterly_series.csv`.
