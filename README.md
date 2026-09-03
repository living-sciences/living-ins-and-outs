# Reassessing the Ins and Outs of Unemployment (Shimer, RED 2012)

This repository holds the working directory of an automated replication and
extension of the paper, produced by [SAI](https://sai.science) agents. It is
the same file tree a signed-in user can browse in the run's workspace, and it
backs the public living-paper page:

**https://sai.science/econ/living-ins-and-outs**

## What is here

- `run/` — the replication working directory: `analyze/` (extracted claims),
  `replication/` (the ported and executed codebase), `verify/` (per-claim
  verdicts and the replication score), `report/` (the run's own report), and
  `followup/` (the extension studies: a re-estimation of the paper's main
  claims on data through 2024-2026, and a refit of the paper's model to the
  combined evidence, each with its report, result card, and figures).
- `referee_report.md` — the referee-style report synthesized from the run.
- Some large input data files are omitted; where that happened,
  `run/LARGE_FILES_OMITTED.md` lists them.

## The paper

Shimer, R. (2012). Reassessing the ins and outs of unemployment. Review of Economic Dynamics 15(2), 127-148.

Replication materials from the author's website. Files under `run/replication/codebase/` derive from those materials
(possibly modified by the replication agent) and remain under their original
authors' terms. Everything else in this repository is generated output from
the SAI pipeline.

## Caveats

Replication scores measure whether claims reproduce under our agents' effort,
not whether authors did anything wrong. Read the referee report's Notes and
the per-claim verdicts in `run/verify/verdicts.json` before quoting any
number.

## Data sources for the extension studies

The extension studies pulled fresh public data on August 24, 2026, all of it from FRED (Federal Reserve Bank of St. Louis). In full:

- U.S. Bureau of Labor Statistics, Current Population Survey: Unemployment Level (UNEMPLOY), Number Unemployed for Less Than 5 Weeks (UEMPLT5), Employment Level (CE16OV), and Average Weeks Unemployed (UEMPMEAN), monthly, seasonally adjusted, January 1948 to July 2026, retrieved from FRED.
- U.S. Bureau of Labor Statistics, Current Population Survey, Labor Force Flows (series LNS17000000, LNS17100000, LNS17200000, LNS17400000, LNS17500000, LNS17600000, LNS17800000, LNS17900000, LNS18000000), monthly, seasonally adjusted, February 1990 to July 2026, retrieved from FRED.
- National Bureau of Economic Research, US Business Cycle Expansions and Contractions (recession chronology), used for figure shading.
- Shimer's original replication materials (the Mathematica notebooks shipped with the paper), reused for the detrending and steady-state code conventions only; no original data files were reused.

The theory update fetched no new data; it works entirely from the living update's constructed series.
