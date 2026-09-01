# Theory, updated to 2026 — the ins and outs of unemployment

*A living-paper theory section for Shimer (2012), "Reassessing the Ins and Outs
of Unemployment" (RED 15(2)). Calibrated on FRED CPS data through 2026-07,
reusing the series built in `followup/001-living-update`. Every quantitative
claim is labelled [ESTIMATED] (from data), [CALIBRATED] (parameter set to match
a moment), or [PROPOSED] (theoretical suggestion, not itself tested).*

---

## 1. The original model, in one paragraph

Workers flow between employment and unemployment. Let `F_t` be the monthly
probability an unemployed worker finds a job and `X_t` the monthly probability an
employed worker exits to unemployment, both corrected for within-month time
aggregation (paper eqs. 4–5). The unemployment rate obeys the exact law of motion
`u_{t+1} = u_t + X_t(1−u_t) − F_t u_t`, whose fixed point is the steady-state
approximation

> **u\*_t = X_t / (X_t + F_t).**   *(eq. 5 in steady state)*

Shimer's two findings: (i) u\*_t tracks actual u_t almost perfectly (paper reports
corr ≈ 0.99 monthly), so the *cyclicality* of unemployment can be decomposed into
a **job-finding** contribution and an **employment-exit** contribution; and
(ii) that decomposition is lopsided — regressing the detrended finding-only
hypothetical `x̄/(x̄+f_t)` on detrended actual u gives β_F ≈ 0.75 over 1948–2010,
rising to ≈ 0.90 since 1987, while separations (β_X) explain the rest and have
*declined secularly* since the mid-1980s. Shimer, quoting Hall (2004), framed
separation-driven recessions as a dismissed relic: *"in the modern U.S. economy,
recessions are not times of unusual job loss … a burst is quickly reabsorbed."*
The model's own escape hatch — separations can dominate "in times of unusual job
loss" — was left as a footnote because no such episode was in the 1948–2010 data.

## 2. What the 2010–2026 evidence demands

Follow-up 001 re-estimated the paper on data through 2026 and found two things the
original framework does not, on its own, organize:

**(a) One episode breaks the constant-β decomposition.** Excluding 2020, the
job-finding story *holds and strengthens*: β_F = 0.89 for 1987–2026 and 0.84 for
the fully-post-paper 2010–2026 window [ESTIMATED, 001 `estimates_by_window.csv`].
But **2020 was the "burst of job loss" the new view dismissed, realized at
20-sigma scale.** Including 2020, the 2010–2026 two-state β_F collapses to 0.54
and β_X rises to 0.38 — the largest separation contribution of any window in 78
years; the three-state separation contribution `λ^EU` jumps from 0.16 (1990–2019)
to 0.55 (2010–2026 incl-2020) while the finding contribution `λ^UE` falls from
0.50 to 0.15 [ESTIMATED, 001]. A single β cannot be simultaneously 0.89 (the
normal regime, 60+ years) and 0.54 (the pooled recent window): the covariance
structure itself changes state. 001 handled this by *dropping* 2020 — defensible
for "did the claim hold," but a 2026 theory needs to *model* the exception, not
delete it.

**(b) The flows have slowed secularly, and that has a dynamic consequence the
original left implicit.** Mean `X̄` fell from 0.033 (1948–2010) to 0.021
(2010–2026) and mean `F̄` from 0.44 to 0.32 [ESTIMATED]. Their sum — the monthly
speed at which u converges to u\* — fell from **ω = 0.47 to 0.34**. Because
deviations of u from u\* decay at rate ω, the monthly persistence ρ = 1 − ω *rose
from 0.53 to 0.66* and the half-life of an unemployment deviation *rose 53%, from
1.08 to 1.66 months* [CALIBRATED]. The steady-state approximation that anchors the
whole method is therefore a weaker approximation now than in 1948, and it breaks
outright in fast-moving episodes: in 2020 (excluding the clipped March point)
corr(u, u\*) fell to 0.75 and u overshot u\* by 5.2 pp [ESTIMATED].

## 3. The updated model — one added state, one recalibrated trend

I keep Shimer's flow accounting *exactly* and add the **smallest** structure that
reconciles both eras: **a rare, state-dependent layoff regime layered on the
existing decomposition, plus a recalibration of the (already-present) secular
flow trend into its dynamic implication.**

**The state-dependence (the one structural amendment).** Let a latent regime
`s_t ∈ {N, L}` govern the *relative variance* of the two flow shocks:

- **Normal regime N** (probability 1 − π_L): finding-shock variance dominates,
  so the decomposition delivers **β_F^N ≈ 0.89** [ESTIMATED]. Separations are the
  "side issue" of the new view.
- **Layoff regime L** (probability π_L): a large common separation shock hits, so
  the separation margin dominates: **β_F^L ≈ 0.2–0.5**, `λ^EU` ≈ 0.55
  [ESTIMATED]. This is Shimer's own "times of unusual job loss," now populated by
  a data point.

The regime is *observable through the separation deviation* `x̂_t` (HP-log
deviation of X_t). Identifying L as months whose `x̂_t` exceeds the entire
pre-2015 historical maximum (0.393, Sept 1949), the **extreme layoff regime has
unconditional probability π_L = 0.0021** — 2 months in 940 (March–April 2020)
[ESTIMATED]. The pooled decomposition is then a mixture,
`β_F ≈ (1−π_L)·β_F^N + π_L·β_F^L`, which reconciles the "holds" (normal) and
"flips" (2020-inclusive) readings without discarding either. A broader,
lower-threshold "separation-elevated" regime (top-decile x̂, π ≈ 0.10) already
pulls β_F from 0.80 to 0.61 [ESTIMATED]; the *dominance* flip requires the extreme
tail.

**The recalibrated trend (no new mechanism, a drawn-out implication).** The
secular decline in ω is not a new parameter — it is Shimer's own falling X̄ (plus
a falling F̄) — but its consequence for *dynamics* was implicit. I make it
explicit: ρ_t = 1 − (X̄_t + F̄_t) is a slow-moving structural object, rising from
0.53 to 0.66, so unemployment is now intrinsically more persistent and the
steady-state approximation degrades over time.

**Why this and not the alternatives.** I considered and rejected three:

1. *A smooth time-varying β_F(t) drift.* Rejected: β_F is flat at ≈ 0.90 for
   every 20-year window ending after 2000 (001 rolling estimates) and jumps only
   across 2020. A smooth drift would misfit both the stable plateau and the sharp
   spike; the data want a **discrete rare state**, not a trend in β.
2. *Dropping 2020 as an outlier* (001's operating choice). Rejected for the
   theory: it discards the single episode that *identifies* separation dynamics
   and yields no recurrence probability — the very thing a forward-looking model
   needs.
3. *Constant β with fatter-tailed shocks.* Rejected: fattening the shock
   distribution raises the *size* of u moves but leaves the finding/separation
   *covariance ratio* — hence β — unchanged, so it cannot produce a separation
   share of 0.81. What changes in 2020 is the mix, not just the magnitude.

## 4. Calibration: paper-era vs 2026

| Parameter | Symbol | 1948–2010 | 2026 | Label |
|---|---|---|---|---|
| Mean job-finding prob. | F̄ | 0.44 | 0.32 | ESTIMATED |
| Mean employment-exit prob. | X̄ | 0.033 | 0.021 | ESTIMATED |
| Adjustment speed | ω = F̄+X̄ | 0.47 | 0.34 | ESTIMATED |
| Persistence of u deviations | ρ = 1−ω | 0.53 | 0.66 | CALIBRATED |
| Half-life of u deviation (mo.) | t½ | 1.08 | 1.66 | CALIBRATED |
| Implied steady-state u | u\* | 0.071 | 0.062 | ESTIMATED |
| Steady-state approx. corr | corr(u,u\*) | 0.945 | 0.924 | ESTIMATED |
| β_F, normal regime | β_F^N | 0.77 → 0.90¹ | 0.84² | ESTIMATED |
| β_F, layoff-inclusive | β_F | n/a | 0.54³ | ESTIMATED |
| 3-state separation contrib. | λ^EU | 0.16 | 0.55³ | ESTIMATED |
| Extreme layoff-regime prob. | π_L | 0 (in sample) | 0.0021 | ESTIMATED |
| 2020 separation share | — | n/a | 0.81 | ESTIMATED |

¹ 1948–2010 → 1987–2010. ² 2010–2026 *excluding* 2020. ³ 2010–2026 *including*
2020. Full table with moments/sources: `calibration_table.csv`. Normal/layoff
β's and λ's read from 001 `estimates_by_window.csv`; levels/ω/ρ re-estimated here
on 001's monthly series (`era_calibration_full.csv`).

## 5. Validation

**(i) Out-of-sample regime classifier.** Calibrating the extreme-regime threshold
on **pre-2015 data only** (largest monthly separation deviation ever seen:
x̂ = 0.393), the rule flags **exactly March–April 2020 and nothing else** in
2015–2026 [ESTIMATED]. The classifier identifies the layoff regime out of sample
with no false positives across the 2015–2019 expansion or the 2021–2026 recovery.

**(ii) The updated model explains an episode the original cannot.** A per-episode
monthly decomposition of every postwar recession (`episode_decomposition.csv`)
puts the **separation share of the unemployment surge at 0.81 in 2020** versus a
median of 0.36 pre-1985, 0.17 in 2008, and ≤ 0.27 in every recession since 1990
[ESTIMATED]. The separation-*only* hypothetical unemployment rate (clip-immune —
it uses the real X_t and a constant f̄) peaked at **0.164 in 2020 versus ≤ 0.084
in every other postwar recession** — a doubling with no precedent. The
constant-β / normal-regime model predicts a separation share of ≈ 0.16 for *any*
unemployment surge; it is structurally incapable of generating 2020. The regime
model, by switching to state L, matches it. (Figure, Panel A.)

**(iii) The recalibration is itself validated by 2008 and by the steady-state
break.** The same episode metric returns 0.17 for 2008–09 — the paper's
job-finding story, confirmed on an out-of-sample recession — so the amendment adds
a *rare* regime without disturbing the original's fit elsewhere. And the
steady-state correlation degrades exactly where the model says it should: with ω
falling, corr(u,u\*) slips 0.945 → 0.924 across eras and to 0.75 within 2020.

## 6. What the update implies going forward [PROPOSED]

- **A lower but stickier natural rate.** Falling X̄ and F̄ push the implied
  steady-state rate down (u\* 0.071 → 0.062) but push persistence up (ρ 0.53 →
  0.66). The 2026 labor market settles at lower unemployment yet takes ~50% longer
  to get there — expect flatter, more drawn-out unemployment cycles and recoveries
  that "feel" slow even when the level is low. [PROPOSED]
- **The steady-state approximation is aging.** Any analysis (including this
  paper's own decomposition) that assumes near-instant convergence to u\* is a
  worse approximation each decade; in fast shocks it fails. Living updates should
  monitor corr(u, u\*) as a health check, not assume the 0.99 of the 2000s.
  [PROPOSED]
- **Separation tail-risk is under-insured.** π_L is tiny, but 2020 showed the
  layoff shock can exceed the entire historical record by 4×. A model calibrated
  only to Great-Moderation second moments — as most DSGE labor blocks are —
  systematically understates the probability *and severity* of a separation-driven
  recession. The 2026 model should carry an explicit, fat-tailed layoff regime
  even though it activates rarely. [PROPOSED]

---

### Deviations, assumptions, honesty notes

- The 2020 layoff is a **monthly (sub-quarterly) event**: the March separation
  spike (X = 0.103, a ~20σ deviation) is largely washed out by the quarterly
  averaging the paper's decomposition uses, which is *why* the quarterly β_X for
  2010–2026 is "only" 0.38 rather than dominant. The episode/regime evidence here
  is deliberately monthly. [documented]
- The March-2020 point has F clipped to 0.01 by 001 (eq. 4 went out of bounds);
  the clip is on the *finding* side. Steady-state correlations drop it (with it,
  recent corr spuriously collapses to 0.24 — a known data artifact); the
  separation-only hypothetical is constructed to be clip-immune. [documented]
- **β_F^L is not identified from pre-2015 data**: 2020 is the only extreme layoff
  episode on record, so its *magnitude* is calibrated to the 2020-inclusive
  windows themselves, not predicted from history. The honest content of the OOS
  test is the *classifier* (which regime) and the *qualitative flip*, not a
  point-predicted β_F^L. This is itself the tail-risk finding of §6. [limitation]
- No genuine structural (likelihood) estimation of a Markov-switching model was
  run; regime probabilities are frequencies and β's are the paper's own OLS
  decomposition on regime subsamples/windows — calibration to moments 001 already
  produced, per the follow-up's compute-modest instruction. [scope]
- Levels of F̄, X̄ carry the Elsby–Hobijn–Şahin–Valletta duration-misreporting
  caveat (biases F̄ down in recent decades); cyclicality and the *ratio-based* ω,
  ρ objects are more robust than the levels. [caveat, inherited from 001]
