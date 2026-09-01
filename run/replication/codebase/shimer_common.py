"""Shared helpers for the Shimer 'Ins and Outs of Unemployment' replication.

Ports the HP filter, detrending, and IO conventions from the shipped
Mathematica notebooks (findsep/u-v-f-s.nb and grossflows/three-state.nb).
"""
import numpy as np


def hp_trend(vec, smooth):
    """HP-filter trend of *log(vec)*, returned in levels (exp of the log trend).

    Exact port of the notebook's Trend[vec, smooth]:
        A = -(D'D)   (D = second-difference operator, standard HP penalty)
        B = Inverse[I - smooth * A] = Inverse[I + smooth * D'D]
        Trend = Exp[B . Log[vec]]
    """
    vec = np.asarray(vec, dtype=float)
    T = len(vec)
    logv = np.log(vec)
    # Standard HP penalty matrix K = D'D where D is (T-2) x T second differences.
    D = np.zeros((T - 2, T))
    for i in range(T - 2):
        D[i, i] = 1.0
        D[i, i + 1] = -2.0
        D[i, i + 2] = 1.0
    K = D.T @ D
    B_inv = np.eye(T) + float(smooth) * K
    log_trend = np.linalg.solve(B_inv, logv)
    return np.exp(log_trend)


def detrend(vec, smooth):
    """Detrend[vec, smooth] = Log[vec] - Log[Trend[vec, smooth]]."""
    vec = np.asarray(vec, dtype=float)
    return np.log(vec) - np.log(hp_trend(vec, smooth))


def quarterly_avg(monthly):
    """(1/3) * sum of each consecutive block of 3 (drops incomplete tail block).

    Mirrors Mathematica's  1/3 Plus @@ Transpose[Partition[x, 3]]."""
    m = np.asarray(monthly, dtype=float)
    n = (len(m) // 3) * 3
    return m[:n].reshape(-1, 3).mean(axis=1)


def quarterly_sum(monthly):
    """sum of each consecutive block of 3 (Plus @@ Transpose[Partition[x,3]])."""
    m = np.asarray(monthly, dtype=float)
    n = (len(m) // 3) * 3
    return m[:n].reshape(-1, 3).sum(axis=1)


def date_q(series, start):
    """Return (date, value) rows with date = start + (i-1)/4, i=1..len."""
    series = np.asarray(series, dtype=float)
    dates = start + np.arange(len(series)) / 4.0
    return np.column_stack([dates, series])


def date_m(series, start):
    series = np.asarray(series, dtype=float)
    dates = start + np.arange(len(series)) / 12.0
    return np.column_stack([dates, series])


def write_dat(path, rows):
    """Write a two-column .dat like Mathematica's Export (whitespace separated)."""
    with open(path, "w") as f:
        for d, v in rows:
            # Mathematica prints the decimal quarter with trailing .25/.5/.75 and
            # full-precision value; format similarly.
            if abs(d - round(d)) < 1e-9:
                ds = str(int(round(d)))
            else:
                ds = ("%g" % d)
            f.write("%s   %r\n" % (ds, float(v)))


def ols_slope(y, x):
    """Slope of a simple regression of y on x (with intercept)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[1]), float(beta[0])


def read_header_series(path):
    """Read a findsep-style file: first line = header, remaining = numeric values."""
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip() != ""]
    header = lines[0]
    values = np.array([float(x) for x in lines[1:]], dtype=float)
    return header, values
