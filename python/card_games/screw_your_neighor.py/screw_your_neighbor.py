import copy
import numpy as np
import pandas as pd

from card_games.card_deck.card_game import Card_Game

class Screw_Your_Neighbor(Card_Game):

    def __init__(self, num_players = 0, bankroll = 10000, bet = 5, debug=False) -> None:
        self.syn_optimal_df = pd.read_csv('python/card_games/screw_your_neighbor/screw_your_neighbor_optimal_strategy.csv')