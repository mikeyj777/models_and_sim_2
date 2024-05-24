import math
import numpy as np
import pandas as pd

from random import random

starting_rad = 10

num_trials = 10000

trial = 0
rad = starting_rad
ans = []
while trial <= num_trials:
    trial += 1
    shots = 0
    rad = starting_rad
    while True:
        shots += 1
        x = starting_rad * random()
        y = starting_rad * random()
        d = math.sqrt(x**2 + y **2)
        if d == rad:
            continue
        if d > rad:
            break
        chord_len = 2 * math.sqrt(rad**2 - d**2)
        rad = chord_len / 2
    ans.append(shots)

ans_df = pd.DataFrame(ans)

print(ans_df.describe())
