import pandas as pd
import numpy as np
from scipy.stats import norm

__df_latest = pd.read_csv("consensus_imports/poisson_lambdas.csv")

def win_prob(lambda_home, lambda_away):
    mu = lambda_home - lambda_away
    sigma = np.sqrt(lambda_home + lambda_away)
    prob = 1 - norm.cdf(0, loc=mu, scale=sigma)
    return float(prob)

def poisson_predict(home_abbr, away_abbr):
    match = __df_latest[
        (__df_latest['team_abbreviation_home'] == home_abbr.upper()) &
        (__df_latest['team_abbreviation_away'] == away_abbr.upper())
    ]

    row = match.iloc[0]
    lh, la = row['lambda_h'], row['lambda_a']
    prob_home = win_prob(lh, la)

    return prob_home
