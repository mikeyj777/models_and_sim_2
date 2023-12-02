import numpy as np
import pandas as pd
from random import shuffle
import copy

from card_games.blackjack.blackjack import Blackjack

bj = Blackjack()

num_players = 5
max_iters = 1000
bankroll = 10000

# suits are 2 thru Ace (0 to 12)
# simulating two tens of different suits to one player.  6 as dealer's up card.


# get shuffled deck 
game = Blackjack(num_players=num_players, bankroll=bankroll)

cards_to_specify = [8, 8+13, 4]
specified_card_locations = [0,num_players + 1, (num_players + 1) * 2 - 1]
game.position_cards_for_analysis(cards_to_specify=cards_to_specify, specified_card_locations=specified_card_locations)
game.deal_hands()
game.set_score_dealer()

results = []
for i in range(max_iters):
    deck_original_position = game.deck_position
    original_hands = copy.deepcopy(game.hands)
    # split
    bj.play_hand(id=0, action = 'split')
    for n in range(1,len(game.hands)):
        bj.play_hand(id=n)
    
    # optimal strategy
    game.deck_position = deck_original_position
    game.hands = copy.deepcopy(original_hands)
    for n in range(len(game.hands)):
        bj.play_hand(id=n)
    
    game.deck_position = deck_original_position
    game.hands = copy.deepcopy(original_hands)
    

apple = 1
