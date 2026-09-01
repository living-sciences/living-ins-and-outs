# Living update spec — Shimer (2012), "Reassessing the Ins and Outs of Unemployment" (RED 15(2))

You are the followup agent. You are seeded from a completed replication of Shimer (2012).
The paper's original sample is **1948–2010** (two-state analysis) and **1967–2010** (three-state
gross-flows analysis). Your job: re-estimate the paper's main claims on data through **2026**
and produce an over-time visualization showing how the findings evolved. Everything below has
been **pre-verified against live endpoints on 2026-08-23** (series IDs, coverage dates, and a
dry-run of the core computation — mean job-finding probability 1948–2010 computed from the
sources below came out 0.440, exactly matching the paper's reported 44%).

No Stata/MATLAB/Mathematica needed: the paper's package ships Mathematica notebooks
(`findsep/u-v-f-s.nb`, `grossflows/three-state.nb`), but every computation is simple time-series
arithmetic. Implement in Python (numpy/pandas/scipy/statsmodels). If the replication codebase
already contains a working Python port of equations (4)–(5), reuse it; otherwise implement from
this spec — it is fully self-contained.

---

## The claims being updated

**C1 (headline, Table 1).** Fluctuations in the job finding rate account for ~three-quarters of
fluctuations in the U.S. unemployment rate, and the share **rises over time**:
- beta_F = **0.77** (1948–2010), **0.83** (1967–2010), **0.85** (1976–2010), **0.90** (1987–2010)
- beta_X (employment exit contribution) = **0.24**, 0.17, 0.15, **0.10** over the same windows.
Method: construct hypothetical unemployment rates from job-finding/exit rates, HP-detrend
(lambda = 1e5) quarterly averages, regress each hypothetical on the actual detrended
unemployment rate. beta_F + beta_X ≈ 1 (0.99–1.01, not exact).

**C2 (Figure 1 facts).** The job finding probability F_t averages **44%** post-war and is strongly
procyclical (falls ~40 log points peak-to-trough); the employment exit probability X_t averages
**3.4%**, is much less cyclical, and **declines secularly from the mid-1980s** ("quantitatively
irrelevant during the last two decades").

**C3 (Table 2, three-state).** Using gross worker flows between Employment/Unemployment/
Inactivity with an eigenvalue time-aggregation correction, the UE transition rate accounts for
~half of unemployment-rate fluctuations, EU less than a quarter, UI ~0.17:
- 1967–2010: UE **0.49**, EU **0.22**, UI 0.17, IU 0.12, IE 0.08, EI −0.05
- 1987–2010: UE **0.51**, EU **0.17**, UI 0.16, IU 0.13, IE 0.09, EI −0.05.

**C4 (Section 4 heterogeneity) — NOT updated here.** Requires matched CPS monthly microdata
by demographic group (42+ GB, month-to-month record linkage). Infeasible in one session and the
IPUMS-CPS application is still pending. Listed for a human in the caveats section; do not build on it.

---

## Data sources (all verified 2026-08-23)

All monthly, seasonally adjusted, from FRED. The **keyless** CSV endpoint works and is the
primary path:

```
https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES_ID>
```

| Variable | FRED ID | Verified coverage |
|---|---|---|
| Unemployment level u_t (thousands) | `UNEMPLOY` | 1948-01 → 2026-07 |
| Unemployed < 5 weeks u^s_t | `UEMPLT5` | 1948-01 → 2026-07 |
| Civilian employment e_t | `CE16OV` | 1948-01 → 2026-07 |
| Mean unemployment duration (weeks, optional check) | `UEMPMEAN` | 1948-01 → 2026-07 |
| Flow E→E | `LNS17000000` | 1990-02 → 2026-07 |
| Flow U→E | `LNS17100000` | 1990-02 → 2026-07 |
| Flow N→E | `LNS17200000` | 1990-02 → 2026-07 |
| Flow E→U | `LNS17400000` | 1990-02 → 2026-07 |
| Flow U→U | `LNS17500000` | 1990-02 → 2026-07 |
| Flow N→U | `LNS17600000` | 1990-02 → 2026-07 |
| Flow E→N | `LNS17800000` | 1990-02 → 2026-07 |
| Flow U→N | `LNS17900000` | 1990-02 → 2026-07 |
| Flow N→N | `LNS18000000` | 1990-02 → 2026-07 |

("N" in the flows series = Not in labor force = Shimer's state I.)

**Known data quirks (already confirmed on the live data):**
1. **2020-03 pathology**: F_t computed from eq (4) is −0.026 in March 2020 (the COVID
   layoff wave made short-term unemployment exceed the model's bounds). This is the ONLY
   out-of-range month in 1948–2026. Handling rule below.
2. **Flows gap 2025-10 and 2025-11**: the labor-force-flows series (all LNS17xxx/LNS18000000)
   have no observations for these two months (2025 government shutdown; no CPS collected).
   Stock series (UNEMPLOY etc.) are also worth checking for the same gap — if a month is
   missing, carry NaN through and drop incomplete quarters from the detrending/regression
   sample (do NOT interpolate across the shutdown; note the dropped quarters in findings).
3. **1994 CPS redesign**: the raw `UEMPLT5` short-term unemployment series drops
   discontinuously in 1994-01. Per the paper's Appendix A, footnote 38: **multiply UEMPLT5
   by 1.1 for all observations ≥ 1994-01** ("delivers very similar results" to Shimer's
   incoming-rotation-group microdata adjustment, and is the adjustment Elsby–Michaels–Solon
   (2009) also use). Apply the same 1.1 factor through 2026 — state this as a maintained
   assumption in the findings note.

**Fallbacks if fredgraph.csv is blocked:**
- FRED API with the available key: `https://api.stlouisfed.org/fred/series/observations?series_id=<ID>&api_key=$FRED_API_KEY&file_type=json`
- BLS public API v2 (no key, rate-limited): `https://api.bls.gov/publicAPI/v2/timeseries/data/<BLS_ID>?startyear=YYYY&endyear=YYYY` with BLS IDs `LNS13000000` (=UNEMPLOY), `LNS13008396` (=UEMPLT5), `LNS12000000` (=CE16OV), and the LNS17xxx IDs as-is. Note: BLS caps 20 years per request and blocks non-browser user agents on download.bls.gov — use the API, not the flat files.
- Do NOT rely on Shimer's website (sites.google.com/site/robertshimer/research/flows) for updated data; it responds (HTTP 200) but its series end around 2010.

**Historical splice for C3 (in the seeded codebase, no download needed):** the package files
`ue.dat, eu.dat, ei.dat, ie.dat, ui.dat, iu.dat` are quarterly full-month transition
probabilities Λ^AB (already time-aggregation corrected), covering **1967Q2–2004Q4** (an older
vintage than the published paper — expect small differences from Table 2). `find.dat`/`sep.dat`
are quarterly F and X, 1951–2004.

---

## Part 1 — Two-state update (C1 + C2). This is the flagship.

### Construction (monthly, then quarterly averages)
1. Download UNEMPLOY, UEMPLT5, CE16OV. Apply the ×1.1 redesign factor to UEMPLT5 from 1994-01 on.
2. Job finding probability, eq (4): `F_t = 1 − (u_{t+1} − u^s_{t+1}) / u_t`; rate `f_t = −ln(1−F_t)`.
3. **2020-03 rule**: where F_t ∉ (0,1) (only 2020-03), set F_t = 0.01 (f_t = −ln 0.99), flag the
   month, and run every 2020-inclusive window twice — once as-is, once excluding 2020Q1–2020Q4 —
   reporting both (`excl_2020` column).
4. Employment exit rate x_t, eq (5): with l_t = u_t + e_t, solve for x_t > 0 in
   `u_{t+1} = (1 − e^{−f_t−x_t}) x_t / (f_t + x_t) · l_t + e^{−f_t−x_t} u_t`
   (monotone increasing in x_t; bisection or scipy.optimize.brentq on [1e-6, 1] works;
   dry-run check: mean X_t = 1−e^{−x_t} over 2008–2010 ≈ 0.026, and paper's post-war mean is 0.034).
5. Aggregate f_t, x_t, and the next-month unemployment rate `urate_{t} ≡ u_{t+1}/l_{t+1}` to
   **quarterly means** (drop quarters with any missing month).

### Estimation per window
For a window [start, end]:
- f̄, x̄ = within-window means of quarterly f_t, x_t.
- Hypothetical rates: `hypF_t = x̄/(x̄ + f_t)` (job-finding-only variation) and
  `hypX_t = x_t/(x_t + f̄)` (exit-only variation).
- HP-filter (lambda = **1e5**, statsmodels `hpfilter`) each of hypF, hypX, urate **within the window**;
  take cyclical components.
- `beta_F` = OLS coefficient of cyclical hypF on cyclical urate (no constant needed beyond demeaning;
  include a constant, it's harmless). Same for `beta_X`. SEs: **Newey–West, 8 lags**.
- Sanity: beta_F + beta_X ∈ [0.97, 1.03] in normal windows.

### Windows
1. **Replication anchors** (must come first — if these fail, stop and debug before extending):
   1948–2010 → expect beta_F ≈ 0.77, beta_X ≈ 0.24 (tolerance ±0.03); 1987–2010 → ≈ 0.90 / 0.10.
2. **Paper's column windows, extended**: 1948–2026, 1967–2026, 1976–2026, 1987–2026.
3. **Out-of-sample and subperiods**: 1987–2019 (pre-COVID check), 2010–2026 (fully post-paper),
   2010–2026 excl. 2020, 1948–2019.
4. **Rolling**: 20-year (80-quarter) windows, stepped 1 quarter, from 1948Q1–1967Q4 through the
   last full window ending 2026Q2. Recompute f̄, x̄, the HP trend, and the regression inside each
   window. Also produce each rolling estimate excluding 2020 quarters where the window overlaps 2020.
   This is cheap (< a minute total).

### C2 update (descriptive, same constructed series)
Report post-1948 and post-2010 means of F_t and X_t, and the 2010–2026 trend in X_t (has the
secular decline in the exit probability continued, flattened, or reversed after COVID?). Note
the paper's caveat (Elsby–Hobijn–Şahin–Valletta 2011) that growing misreporting of duration may
bias the level of F_t downward in recent decades — levels are less trustworthy than cyclicality.

## Part 2 — Three-state update (C3). Secondary; do after Part 1 works.

1. Download the 9 flow series. For each month, form the 3×3 discrete transition matrix
   `n_t[A→B] = flow(A→B)_t / Σ_B' flow(A→B')_t` for A,B ∈ {E,U,I} (columns-from-A sum to 1;
   orient the matrix the way your eigendecomposition code expects).
2. Time-aggregation correction (Section 3.1): eigendecompose n_t = P M P^{-1}; verify eigenvalues
   are real, positive, distinct (Shimer found they always are; if a month fails, flag it and skip
   that month rather than forcing a complex log). Continuous-time generator λ_t = P log(M) P^{-1};
   off-diagonals λ^AB_t are the instantaneous rates. Full-month probabilities Λ^AB_t = 1 − exp(−λ^AB_t).
3. Decomposition, eq (7): with window-mean rates λ̄^AB, for each of the six rates construct the
   hypothetical steady-state unemployment rate letting only that rate vary
   (e.g. for UE: e^UE_t, u^UE_t, i^UE_t from the cofactor formulas with λ^UE_t time-varying and the
   other five at λ̄; hypothetical u-rate = u^UE_t/(u^UE_t + e^UE_t)). Quarterly-average, HP(1e5) detrend,
   regress on the detrended actual unemployment rate (from the same flows-implied stocks or from
   urate as in Part 1 — use the actual CPS unemployment rate u/(u+e); Shimer's regressand is the
   actual detrended unemployment rate).
4. Windows: **1990–2010** (overlap anchor — compare against Table 2's 1987–2010 column: expect
   UE ≈ 0.5, EU ≈ 0.17, same ordering; exact match not expected since BLS's official matched flows
   ≠ Shimer's own matching and margin-error treatment), 1990–2026, 1990–2019, 2010–2026,
   and 2010–2026 excl. 2020. Remember the 2025-10/11 gap: drop 2025Q4.
5. Optional if time permits: reproduce the 1967–2004 decomposition from the package `*.dat` files
   (λ^AB = −ln(1−Λ^AB)) as a historical anchor, noting the vintage difference.

**Caveat to state**: BLS published flows begin 1990-02, so the three-state update cannot extend the
paper's 1967 start; the update tests whether the paper's *recent-decades* three-state conclusion
holds through 2026. The published flows are NOT adjusted for margin error (Abowd–Zellner); neither
was Shimer's baseline, and Fujita–Ramey (2009) found the adjustment changes little.

## Part 3 — Deliverables

Write everything to an `outputs/` directory:

1. **`estimates_by_window.csv`** — tidy: `part` (two_state | three_state), `window_start`,
   `window_end`, `excl_2020` (bool), `parameter` (beta_F, beta_X, beta_UE, beta_EU, beta_UI,
   beta_IU, beta_IE, beta_EI), `estimate`, `se_nw8`, `n_quarters`, `is_paper_anchor` (bool),
   `paper_value` (where applicable, else empty).
2. **`rolling_estimates.csv`** — `window_start`, `window_end`, `beta_F`, `se_F`, `beta_X`, `se_X`,
   `excl_2020`.
3. **`series_monthly.csv`** — date, u, us_adj, e, F, f, X, x, plus the six Λ^AB from Part 2 (NaN pre-1990).
4. **The flagship figure** (`living_update.png` + `.pdf`), two panels sharing the x-axis (calendar time):
   - **Panel A**: rolling 20-year beta_F (solid line) with 95% Newey–West CI band, and beta_X
     (second line, its own band), x = window END date. Horizontal dashed reference lines at
     **0.77** ("paper, 1948–2010") and **0.90** ("paper, 1987–2010"), labeled. Shade the paper's
     original sample (1948–2010) in light grey with a vertical line + label "paper's data end
     (Dec 2010)". Add NBER recession bars (hardcode the standard dates through 2020; if any
     recession was dated after 2020, only include it if you can confirm dates from FRED series
     `USREC`). Annotate the windows overlapping 2020 (e.g. a lighter line for the incl-2020
     variant where it diverges from excl-2020).
   - **Panel B**: quarterly F_t and X_t (X on a secondary axis or ×10 scale, labeled), 1948–2026,
     same original-sample shading. This is the paper's Figure 1 extended 16 years.
   - Title the figure so it reads standalone; axis labels with units; source line
     "CPS via FRED, Shimer (2012) methodology, redesign factor 1.1 post-1994".
5. **`findings.md`** (~1 page): the anchor replication result vs. paper values; how beta_F evolved
   (did the post-1987 "job finding explains ~all of it" claim strengthen, hold, or weaken through
   2026?); what including vs. excluding 2020 does — the COVID recession was a *layoff* (separation)
   shock, the one recent episode where "the ins won", so expect the incl-2020 windows to show a
   larger beta_X and say so plainly; whether the post-2021 period reverts to job-finding dominance;
   the three-state confirmation; and the caveat list (1.1 factor maintained post-2010; duration
   misreporting; flows start 1990; 2025 shutdown gap; C4 not updated).

## Failure handling
- Anchor replication off by > 0.05 on beta_F for 1948–2010: debug (most likely suspects: HP lambda,
  quarterly timing of urate = u_{t+1}/l_{t+1}, the 1.1 factor start date, or F/X monthly-vs-quarterly
  construction order — rates are computed monthly FIRST, then quarterly-averaged) before proceeding.
- FRED unreachable: fall back per the data-sources section (FRED API key, then BLS API).
- Part 2 blocked for any reason: ship Part 1 alone — it is the paper's headline — and record why.
- Never silently interpolate over the 2025 shutdown gap or the 2020-03 clip; every such touch is
  flagged in findings.md.

## For the human (not you)
- **C4 heterogeneity update**: needs IPUMS-CPS basic monthly extracts (application pending) or the
  NBER/Census CPS microdata with month-to-month matching — tens of GB and a full pipeline; a
  separate project.
- If exactness on the redesign adjustment ever matters: recompute the incoming-rotation-group
  short-term-unemployment share 1994–2026 from CPS microdata instead of the 1.1 factor.