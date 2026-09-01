# Replication Report

**Generated:** 2026-08-24 21:50:53

---

## Executive Summary

**Mode:** full

**Replication Score: 63.2%** (25/27 claims counted)

*Coverage: scored over 25 attempted/blocked claim(s); 2 out-of-scope (not targeted by the plan — excluded, not counted as failures).*

## Tier Breakdown

| Tier | Match | Partial | No match | Not attempted | n/a | Missing | Total |
|---|---|---|---|---|---|---|---|
| Headline | 2 | 1 | 0 | 0 | 0 | 0 | 3 |
| Supporting | 11 | 4 | 1 | 6 | 0 | 0 | 24 |

## Per-Claim Verdicts

| ID | Tier | Type | Status | Rationale | Evidence |
|---|---|---|---|---|---|
| C1 | headline | scalar | match | The reproduced Table 1 decomposition is in output/table1_1948_2010.json. The column-1 case (all workers, period '1948.00-2010.50') reports finding_contribution=0.7632 and exit_c... | 3 file(s) |
| C2 | headline | scalar | partial | Step 5 (which verifies C2) produced output/table1_1948_2010.json, whose '1987' entry covers period 1987.00-2010.50 (95 quarters) — the paper's exact Table 1 column 4 sample — an... | 4 file(s) |
| C3 | headline | qualitative | match | Step 2 output output/two_state/summary.json reports corr_findQ_urateQ = -0.9652 versus corr_sepQ_urateQ = 0.6493, and the 1948-2010 reconstruction (output/two_state_1948_2010/su... | 7 file(s) |
| C4 | supporting | table | partial | The run produced output/table1_1948_2010.json (in the codebase output/ dir) with four of Table 1's five columns, computed on the reconstructed 1948-2010 series via the footnote-... | 4 file(s) |
| C5 | supporting | scalar | match | The claim is about the job finding probability F_t averaging 44% over the post-war period (1948-2010). find.dat stores the instantaneous job finding rate f_t, and the verificati... | 4 file(s) |
| C6 | supporting | scalar | match | The claim is a windowed, single-business-cycle amplitude: the job-finding probability F_t falls by about forty log points from a cyclical peak to the following trough 'during re... | 5 file(s) |
| C7 | supporting | scalar | match | The claim asks for the post-war (1948-2010) mean of the employment exit probability X_t constructed via eq. (5), expected ~0.034. The run produced output/two_state_1948_2010/sep... | 3 file(s) |
| C8 | supporting | scalar | match | The pipeline detrended both the exit-probability series X_t (eq. 5) and the time-aggregation-ignoring X-tilde_t (eq. 6 with F-tilde=F) with an HP filter (smoothing 1e5) and repo... | 5 file(s) |
| C9 | supporting | scalar | match | The plan's step 2 (targeting this claim) ran the two-state construction on the shipped 1951:M1-2005:M1 aggregate data and produced corr_urate_ss=0.9872 (output/two_state/summary... | 5 file(s) |
| C10 | supporting | figure | match | The claim's Figure 1 was reproduced at output/replication/codebase/output/two_state_1948_2010/figure1.pdf, which matches the claim's exact 1948Q1-2010Q4 span (step 2/step 4 of t... | 3 file(s) |
| C11 | supporting | figure | no match | The claim describes the paper's Figure 2 as a two-panel time series in which a hypothetical unemployment rate driven only by job-finding fluctuations (x-bar/(x-bar+f_t), top pan... | 6 file(s) |
| C12 | supporting | figure | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Figure 3 (prime-age men 25-54) requires CPS microdata restricted to that demog... | 0 file(s) |
| C13 | supporting | scalar | match | Plan step 7 (figure4_compare.py) reproduced the Figure 4 cross-check and wrote output/figure4.json, which reports corr_F_UE = 0.9474 and mean_logdiff_F_UE = 0.32046 (log units) ... | 3 file(s) |
| C14 | supporting | scalar | match | Plan step 7 (figure4_compare.py, verifies C14) produced output/figure4.json with corr_X_EU=0.8503 and mean_logdiff_X_EU=0.5862 (i.e. X_t averages ~58.6 log points above Lambda^E... | 4 file(s) |
| C15 | supporting | figure | partial | output/figure4.pdf was produced and is the correct figure: two stacked panels, the top comparing the two-state job-finding probability F_t with the three-state UE transition pro... | 4 file(s) |
| C16 | supporting | scalar | match | Plan step 6 ran three_state_decomp.py on the shipped six instantaneous transition-rate series (ei/eu/ie/iu/ue/ui .dat, 151 quarters 1967Q2-2004Q4) — the notebook's already-time-... | 3 file(s) |
| C17 | supporting | table | partial | The run produced output/table2.json (the expected output/table2.csv was not written, but an equivalent JSON table exists), giving the six-transition-rate decomposition for the u... | 2 file(s) |
| C18 | supporting | qualitative | match | The three quantitative sub-claims of the decomposition are unambiguously demonstrated by the produced output/table2.json. In the full-sample unemployment-rate column, lambda^UE=... | 5 file(s) |
| C19 | supporting | scalar | partial | The run produced all four three-state coefficients for the employment-population ratio (full sample) in output/table2.json under emp_pop_ratio.full: UE=1.0397, IE=0.6435, EU=0.4... | 3 file(s) |
| C20 | supporting | scalar | out of scope | No plan step targeted this claim; treated as out_of_scope (excluded from the score, not a failure): Alternative job-finding measures M_t (medium-term-unemployment based) and D_t... | 0 file(s) |
| C21 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Job-loser-share and reason-for-unemployment job-finding rates and the F^comp/F... | 0 file(s) |
| C22 | supporting | figure | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Figure 9 (real vs compositional job finding across seven observable dimensions... | 0 file(s) |
| C23 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Three-state EU+EI sums, employer-to-employer transitions, and the quarterly jo... | 0 file(s) |
| C24 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Short-term-unemployment shares in the full CPS vs incoming rotation groups (19... | 0 file(s) |
| C25 | supporting | scalar | not attempted | No plan step targeted this claim; the planner marked it BLOCKED (counts as a reproducibility gap): Comparison against Bleakley's independent gross-flow estimates requires Bleakl... | 0 file(s) |
| C26 | supporting | figure | out of scope | No plan step targeted this claim; treated as out_of_scope (excluded from the score, not a failure): Figure 7 (three alternative job-finding measures F_t, D_t, M_t) is reconstruc... | 0 file(s) |
| C27 | supporting | qualitative | match | The reproduced X_t series produced by the step-2 two-state construction (output/two_state/sep.dat, the Figure 1 bottom-panel series) shows an unmistakable secular decline: annua... | 5 file(s) |

## Flags

- 2 claim(s) marked out_of_scope (planner did not target them) — excluded from the score, not counted as failures. Score is over the 25 attempted/blocked claim(s).

## Replication Attempt

**Environment:** Python 3.12.8, GPU: NVIDIA RTX A6000 (x4, 49140 MiB each), Packages: numpy 2.5.2, scipy 1.18.1, pandas 3.0.5, matplotlib 3.11.1, requests 2.34.2
**Duration:** 0s
**Steps completed:** 7/7

| Step | Description | Result | Duration |
|------|-------------|--------|----------|
| 1 | Prepare working copy, unzip inputs, install deps, check for Wolfram kernel, inventory inputs. | Success | 0s |
| 2 | Two-state job-finding (F, eq.4) and employment-exit (X, eq.5) construction on shipped 1951-2005 aggregate data; quarterly averages; Figures 1-2 and summary stats. | Success | 0s |
| 3 | Table 1 decomposition on shipped-vintage series: hypothetical unemployment rates (only f varies / only x varies), HP-detrended, regressed on detrended actual urate; full and 1987 samples. | Success | 0s |
| 4 | Reconstruct two-state inputs at full 1948-2010 scale from public FRED data (UNEMPLOY, CE16OV, UEMPLT5); apply Appendix-A short-term correction with shipped shortadj shares for 1976M1-2005M1, splice published UEMPLT5 for 2005M2-2010M12; re-run two-state construction. | Success | 0s |
| 5 | Headline Table 1 decomposition at the paper's exact samples on the 1948-2010 reconstructed series: full 1948-2010, 1967-2010, 1976-2010, 1987-2010 (the four whole-population-aggregate columns). | Success | 0s |
| 6 | Three-state (E/U/I) decomposition -- second half of three-state.nb on shipped quarterly lambda series. Steady-state urate & emp-pop measures, six single-rate hypotheticals (eq.7/8), Table 2 OLS slopes on detrended measured actual rates, steady-state/actual correlation, Figure 5. | Success | 0s |
| 7 | Figure 4 cross-check: convert shipped quarterly UE/EU instantaneous rates to full-month probabilities Lambda=1-exp(-lambda), compare Lambda^UE vs two-state F and Lambda^EU vs two-state X on the overlapping quarterly sample; report correlations and mean log-level differences; emit two-panel Figure 4. | Success | 0s |


## Limitations & Code Quality

**Fixes the replication agent applied to make the work run:** 1 (0 minor, 1 major, 0 critical). These are evidence about the provided code/paper, not the replication.

Only one fix was required, and it is a single localized data-handling gap rather than a fundamental methodological failure. The core two-state estimation algorithm was intact and the fix defaults to off so step-2 behavior matches the notebook exactly. The issue is that the published code only ran cleanly up to the 2005M1 end of the microdata-share window, while the paper's headline sample runs through 2010M12; bridging that gap required understanding the truncation logic and adding a deliberate tail-splice using the published level. This raises it above trivial maintenance to major, and signals that the shipped pipeline was incomplete for reproducing the full-sample results even though the estimation methodology itself is sound and implementable.

| # | Description | Severity | Impact |
|---|-------------|----------|--------|
| 1 | Added an opt-in --splice_tail flag so the short-term series continues with the published level past the 2005M1 end of the microdata-share window, allowing the sample to extend to 2010M12. | major | Indicates the provided notebook/code as shipped only reproduced results up to the microdata-share window (2005M1) and did not itself extend the series to the full 1948-2010 sample the paper reports. The share-based adjustment window and the full analysis window are mismatched, and the code that bridged them was missing. This is a genuine incompleteness in the published pipeline for the full-sample results, though the fix is conservative (default off preserves notebook behavior) and the extension method is a plausible, documented reconstruction rather than a fabrication. |


---

*Report generated by Veritas Replication Agent*
