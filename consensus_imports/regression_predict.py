"""
regression_predict.py
─────────────────────────────────────────────────────────────────────────────
Standalone NBA Linear-Regression predictor.

How it works:
Looks up pre-computed win probabilities from predict.json.
─────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations
import json
import os

__PROBS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regression_probs.json")
__probs: dict | None = None

def __load_probs() -> dict:
    global __probs
    if __probs is None:
        if not os.path.exists(__PROBS_PATH):
            raise FileNotFoundError(
                f"Probability matrix not found: {__PROBS_PATH}\n"
                "Run the matrix generator in the main file to create regression_probs.json."
            )
        with open(__PROBS_PATH, "r") as f:
            __probs = json.load(f)
    return __probs

def regression_predict(home: str, away: str) -> float:
    """
    Return the probability that the home team wins.
    """
    home = home.upper()
    away = away.upper()

    if home == away:
        raise ValueError("Home and away teams must be different")

    matrix = __load_probs()

    if home not in matrix:
        raise ValueError(f'Unknown team "{home}". Valid: {sorted(matrix.keys())}')
    if away not in matrix[home]:
        raise ValueError(f'Unknown team "{away}".')

    return matrix[home][away]


''' Example usage:
from nba_predict import nba_predict
print(nba_predict("LAL", "BOS"))  # Probability that LAL beats BOS at home
'''