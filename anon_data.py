
# Author: Shuyi Wu
# Date: 17 October 2026
# Description: Pseudonymisation of Data

"""script to anonymise data"""

import pandas as pd
import random

df = pd.read_csv("VAoT.csv")


def randomise(n):
    rng = random.Random(str(n))
    return rng.randint(1, len(df))

df["Hospital Number"] = [randomise(n) for n in df["Hospital Number"]]
df["NHS Number"] = [randomise(n) for n in df["NHS Number"]]

"""prints out df to csv file"""
df.to_csv("VAoT_anon.csv")