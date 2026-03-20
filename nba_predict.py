"""
nba_predict.py
─────────────────────────────────────────────────────────────────────────────
Standalone NBA Linear-Regression predictor.

How it works:
Looks up pre-computed win probabilities from predict.json.
─────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations
import json
import os

_PROBS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nba_predict.json")
_probs: dict | None = None

def _load_probs() -> dict:
    global _probs
    if _probs is None:
        if not os.path.exists(_PROBS_PATH):
            raise FileNotFoundError(
                f"Probability matrix not found: {_PROBS_PATH}\n"
                "Run the matrix generator in the main file to create nba_predict.json."
            )
        with open(_PROBS_PATH, "r") as f:
            _probs = json.load(f)
    return _probs

def nba_predict(home: str, away: str) -> float:
    """
    Return the probability that the home team wins.
    """
    home = home.upper()
    away = away.upper()

    if home == away:
        raise ValueError("Home and away teams must be different")

    matrix = _load_probs()

    if home not in matrix:
        raise ValueError(f'Unknown team "{home}". Valid: {sorted(matrix.keys())}')
    if away not in matrix[home]:
        raise ValueError(f'Unknown team "{away}".')

    return matrix[home][away]


''' Example usage:
from nba_predict import nba_predict
print(nba_predict("LAL", "BOS"))  # Probability that LAL beats BOS at home
'''