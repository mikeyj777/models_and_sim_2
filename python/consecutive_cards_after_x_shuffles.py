import numpy as np
import pandas as pd

from card_games.card_deck.standard_deck import Standard_Deck

num_trials = 10000
max_shuffles = 100

ans = []

for shuffles in range(1, max_shuffles + 1):
    count_diff_1 = 0
    for _ in range(num_trials):
        sd = Standard_Deck(shuffle_it=False)
        sd.shuffle(num_shuffles=shuffles)
        deck = sd.deck
        deck_shift = np.concatenate((deck[1:], [np.inf]))
        diff = np.abs(deck_shift - deck)
        unique, counts = np.unique(diff, return_counts = True)
        count_dict = dict(zip(unique, counts))
        diff_1 = 0
        if 1 in count_dict:
            diff_1 = count_dict[1]
        count_diff_1 += diff_1
    ans.append({shuffles: count_diff_1 / num_trials})

ans_df = pd.DataFrame(ans)

ans_df.to_csv('shuffles_vs_consec_cards_2.csv')

apple = 1