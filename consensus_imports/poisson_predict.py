import pandas as pd
import numpy as np
from scipy.stats import norm

def win_prob(lambda_home, lambda_away):
    mu = lambda_home - lambda_away
    sigma = np.sqrt(lambda_home + lambda_away)
    prob = 1 - norm.cdf(0, loc=mu, scale=sigma)
    return float(prob)

def poisson_predict(home_abbr, away_abbr):
    try:
        df_latest = pd.read_csv("../latest_matchups_only.csv")
        match = df_latest[
            (df_latest['team_abbreviation_home'] == home_abbr.upper()) & 
            (df_latest['team_abbreviation_away'] == away_abbr.upper())
        ]
        
        row = match.iloc[0]
        lh, la = row['lambda_h'], row['lambda_a']
        prob_home = win_prob(lh, la)

        return float(prob_home)

    except FileNotFoundError:
        print("Error: latest_matchups_only.csv not found. Run the creation script first.")
