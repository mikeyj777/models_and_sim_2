import numpy as np
import pandas as pd
from random import shuffle
import copy

from card_games.card_deck.dealt_cards import Dealt_Cards
from card_games.blackjack import black_jack_optimal_strategy as bjo

num_players = 5
max_iters = 1000

# suits are 2 thru Ace (0 to 12)
# simulating two tens of different suits to one player.  6 as dealer's up card.


# get shuffled deck 
game = Dealt_Cards(num_players=num_players, include_dealer=True, cards_per_hand=2)

cards_to_specify = [8, 8+13, 4]
specified_card_locations = [0,num_players + 1, (num_players + 1) * 2 - 1]
game.position_cards_for_analysis(cards_to_specify=cards_to_specify, specified_card_locations=specified_card_locations)
game.deal_hands()

results = []
for i in range(max_iters):
    deck_original_position = game.deck_position
    deck_original_length = len(game.deck)
    # split
    card1a = game.hands[0,0]
    card1b = game.get_next_card()
    game.hands.append([card1a, card1b])
    card2a = card1a
    card2b = game.get_next_card()
    game.hands.append([card2a, card2b])
    

apple = 1
