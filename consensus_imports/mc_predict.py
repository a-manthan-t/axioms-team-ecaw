"""
mc_predict.py
─────────────────────────────────────────────────────────────────────────────
Standalone Monte Carlo game predictor.

Public interface (mirrors elo_predict.py):

    from mc_predict import mc_predict

    prob = mc_predict("LAL", "BOS")   # -> float, P(home wins)

How it works
─────────────────────────────────────────────────────────────────────────────
Instead of pickling model objects (which causes class-resolution errors),
the notebook pre-computes a full 30x30 matrix of win probabilities for every
possible home/away matchup and saves it to mc_probs.json.

mc_predict() simply looks up the value in that matrix - instant, no model
dependencies, no nba_api calls at runtime.

Setup (one time only)
─────────────────────────────────────────────────────────────────────────────
1.  Train the notebook fully (Sections 1-4).
2.  Run Section 12 in the notebook - this calls build_prob_matrix() and
    saves mc_probs.json to your working directory.
3.  Place mc_probs.json and mc_predict.py in the same folder.
4.  Import and call mc_predict() as shown above.

Refreshing probabilities
─────────────────────────────────────────────────────────────────────────────
Re-run Section 12 whenever you want fresh probabilities (e.g. once a week).
"""

from __future__ import annotations
import json
import os

___PROBS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mc_probs.json")
___probs: dict | None = None


def ___load_probs() -> dict:
    global ___probs
    if ___probs is None:
        if not os.path.exists(___PROBS_PATH):
            raise FileNotFoundError(
                f"Probability matrix not found: {___PROBS_PATH}\n"
                "Run Section 12 in the notebook to generate mc_probs.json."
            )
        with open(___PROBS_PATH, "r") as f:
            ___probs = json.load(f)
    return ___probs


def mc_predict(home: str, away: str) -> float:
    """
    Return the probability that the home team wins.

    Parameters
    ----------
    home : 3-letter team abbreviation, e.g. "LAL"
    away : 3-letter team abbreviation, e.g. "BOS"

    Returns
    -------
    float : P(home wins), in range (0, 1)

    Example
    -------
        from mc_predict import mc_predict
        p = mc_predict("LAL", "BOS")
    """
    home = home.upper()
    away = away.upper()

    if home == away:
        raise ValueError("home and away teams must be different")

    matrix = ___load_probs()

    if home not in matrix:
        raise ValueError(f'Unknown team "{home}". Valid: {sorted(matrix.keys())}')
    if away not in matrix[home]:
        raise ValueError(f'Unknown team "{away}". Valid: {sorted(matrix.keys())}')

    return matrix[home][away]

"""
Example Use case:

from mc_predict import mc_predict
p = mc_predict("LAL", "ATL")   # Prediction
print(p)

"""
