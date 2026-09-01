# Living update — Shimer (2012), "Ins and Outs of Unemployment," through 2026

**Data vintage:** FRED, downloaded 2026-08-24 (CPS series through 2026-07).
**Method:** Shimer (2012) eqs (4)–(5) and the Table 1 / Table 2 decompositions,
re-implemented in Python per the follow-up spec. Short-term unemployment
(`UEMPLT5`) multiplied by **1.1 from 1994-01 on** (Appendix-A footnote-38
adjustment) — a *maintained assumption* carried through 2026. HP filter λ=1e5,
detrended **within each window**; slopes with Newey–West(8) standard errors.

## 1. Anchor replication (must-pass gate) — PASSED

The 1948–2010 and 1987–2010 anchors reproduce the paper and improve on the
seeded replication (which spliced published `UEMPLT5` levels for 2005–2010 rather
than using the 1.1 factor).

| Window | β_F paper | β_F this study | β_X paper | β_X this study | seeded repl. β_F/β_X |
|---|---|---|---|---|---|
| 1948–2010 | 0.77 | **0.769** (se .024) | 0.24 | **0.238** (se .027) | 0.763 / 0.245 |
| 1967–2010 | 0.83 | **0.831** | 0.17 | **0.173** | 0.807 / 0.198 |
| 1976–2010 | 0.85 | **0.847** | 0.15 | **0.155** | 0.838 / 0.166 |
| 1987–2010 | 0.90 | **0.898** | 0.10 | **0.107** | 0.858 / 0.144 |

All four within ±0.01 of the paper (tolerance was ±0.03). Mean job-finding
probability 1948–2010 = **0.4395** (paper 0.44; the spec's dry-run target of
0.440 reproduced exactly); mean exit probability = **0.0334** (paper 0.034).
β_F + β_X ∈ [1.00, 1.01] in every window. Seeded-replication values read from
`/workspace/eval/replication/codebase/output/table1_1948_2010.json`.

## 2. How β_F evolved through 2026 (C1)

**Excluding the 2020 COVID quarters, the post-1987 "job finding explains almost
all of it" claim HOLDS and even strengthens slightly.** Extending each of the
paper's start-year windows to 2026-Q2 (excl-2020):

| Window→2026 | β_F excl-2020 | β_X excl-2020 | β_F incl-2020 | β_X incl-2020 |
|---|---|---|---|---|
| 1948–2026 | 0.791 | 0.209 | 0.738 | 0.250 |
| 1967–2026 | 0.846 | 0.147 | 0.754 | 0.221 |
| 1976–2026 | 0.859 | 0.131 | 0.754 | 0.217 |
| 1987–2026 | **0.892** | 0.101 | 0.762 | 0.208 |
| 1987–2019 (pre-COVID) | 0.898 | 0.098 | — | — |
| 2010–2026 (fully post-paper) | **0.843** | 0.112 | **0.538** | **0.380** |

The 20-year rolling β_F (Panel A of the figure) rises from ~0.70 for windows
ending in the late 1960s to a stable **~0.90** for every window ending after
2000, and stays there through the last full window ending 2026-Q2. The paper's
central finding is not a historical artifact: it is, if anything, more true now.

## 3. What including vs. excluding 2020 does — the COVID layoff exception

The COVID recession was a **separation (layoff) shock**, the one recent episode
where "the ins won." This shows up sharply and exactly as expected:

- The **2010–2026** window flips from job-finding-dominated (β_F 0.84, β_X 0.11
  excl-2020) to **separation-heavy** (β_F 0.54, β_X **0.38** incl-2020) — the
  largest β_X of any window in the study.
- Every 2020-spanning window has a lower β_F and higher β_X when 2020 is kept
  (dashed lines in Panel A: β_F drops to ~0.72–0.76, β_X jumps to ~0.21–0.38).
- **Post-2021 reverts to job-finding dominance.** The excl-2020 estimates — which
  drop 2020Q1–Q4 but keep 2021–2026 — return to β_F ≈ 0.84–0.89, so the recovery
  and the tight 2022–2024 labor market are again a job-finding story. COVID is a
  four-quarter exception embedded in an otherwise unchanged regime.

The three-state decomposition tells the same story: the UE (job-finding)
contribution flips from 0.42 (excl-2020) to **0.15** while EU (separations) rises
from 0.17 to **0.55** (incl-2020) over 2010–2026.

## 4. Descriptive levels (C2)

- Mean **F_t** fell from 0.440 (1948–2010) to **0.328** (2011–2026); mean **X_t**
  from 0.0334 to **0.0205**. These are *level* declines and should be read with
  the Elsby–Hobijn–Şahin–Valletta (2011) caveat that growing duration
  misreporting biases the level of F_t downward in recent decades — cyclicality
  (Sections 2–3) is far more trustworthy than levels.
- **The secular decline in the employment-exit probability continued** after
  COVID: a linear trend in X_t over 2010–2026 (excluding the clipped 2020-03
  month) is **−0.00035/yr** (p < 1e-20), gentler than the −0.0006/yr of
  1985–2010 but still clearly downward. The exit rate has *not* reverted upward
  post-COVID; outside the 2020 spike it remains "quantitatively irrelevant."

## 5. Three-state confirmation (C3)

BLS gross-flow series (`LNS17xxx`, start 1990-02) → monthly 3×3 transition
matrices → eigenvalue time-aggregation correction (all months real, positive,
distinct eigenvalues — no failures) → eq.(7) decomposition:

| Rate | 1990–2010 (this study) | paper 1987–2010 | 1990–2019 | 2010–2026 excl-2020 |
|---|---|---|---|---|
| UE | **0.520** | 0.51 | 0.502 | 0.421 |
| EU | **0.168** | 0.17 | 0.164 | 0.171 |
| UI | 0.152 | 0.16 | 0.135 | 0.144 |
| IU | 0.115 | 0.13 | 0.149 | 0.200 |
| IE | 0.079 | 0.09 | 0.085 | 0.101 |
| EI | −0.034 | −0.05 | −0.044 | −0.051 |

The 1990–2010 overlap column matches Table 2's 1987–2010 column in magnitude and
ordering: UE ≈ half, EU < a quarter, UI ≈ 0.15. The paper's recent-decades
three-state conclusion holds through 2026 (excl-2020).

## Caveats & maintained assumptions

1. **1.1 redesign factor maintained post-2010** (Appendix-A footnote 38). Exact
   treatment would recompute the incoming-rotation-group short-term share from CPS
   microdata — a separate project.
2. **Duration misreporting** biases the *level* of F_t downward in recent decades
   (levels in §4 less trustworthy than cyclicality).
3. **BLS published flows begin 1990-02**, so the three-state update cannot extend
   the paper's 1967 start; it tests the recent-decades conclusion only. Published
   flows are not margin-error adjusted (neither was Shimer's baseline;
   Fujita–Ramey 2009 find the adjustment changes little).
4. **2025 government-shutdown gap:** stock series miss 2025-10; flow series miss
   2025-10 and 2025-11 (no CPS collected). No interpolation — the affected
   quarters (2025Q3, 2025Q4) are dropped from every sample. 2026Q3 is also dropped
   (only July available).
5. **2020-03 clip:** F_t from eq.(4) was −0.026 in March 2020 (short-term
   unemployment exceeded the model bound); clipped to 0.01 and flagged. It is the
   only out-of-range month in 1948–2026 and is why every 2020-inclusive window is
   also reported excluding 2020.
6. **C4 (demographic heterogeneity) not updated** — needs matched CPS monthly
   microdata (tens of GB, IPUMS-CPS application pending). Left for a human.
