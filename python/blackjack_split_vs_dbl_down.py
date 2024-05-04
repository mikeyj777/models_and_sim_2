import numpy as np
import pandas as pd
from random import shuffle
import copy

from card_games.blackjack.blackjack import Blackjack

num_players = 1
max_iters = 1000
bankroll = 10000
debug = True

# suits are 2 thru Ace (0 to 12)
# simulating two tens of different suits to one player.  6 as dealer's up card.
def get_bj_game(num_players, bankroll):
    game = Blackjack(num_players=num_players, bankroll=bankroll, debug=debug)

    cards_to_specify = [8, 8+13, 4]
    specified_card_locations = [0,num_players + 1, (num_players + 1) * 2 - 1]
    game.position_cards_for_analysis(cards_to_specify=cards_to_specify, specified_card_locations=specified_card_locations)
    game.deal_hands()

    return game


# get shuffled deck 
    

results = []
for i in range(max_iters):
    # first player will split 10s
    game = get_bj_game(num_players=num_players, bankroll=bankroll)
    game.modified = True
    game.modification_target = 4
    game.play_hand(id=0, action = 'split')
    
    # get the original number of hands, as split hands will be added to the array of dealt hands
    num_hands = len(game.hands)
    game.modified = False
    for n in range(1,num_hands):
        game.play_hand(id=n)
    game.payouts_for_stayed_hands()
    ans = {}
    ans['split'] = game.bankrolls[0] - bankroll
    
    # optimal strategy
    game = get_bj_game(num_players=num_players, bankroll=bankroll)
    num_hands = len(game.hands)
    for n in range(num_hands):
        game.play_hand(id=n)
    game.payouts_for_stayed_hands()
    ans['optimal'] = game.bankrolls[0] - bankroll
    results.append(ans)

res_df = pd.DataFrame(results)
res_df.to_csv('split_vs_optimal.csv')


apple = 1
