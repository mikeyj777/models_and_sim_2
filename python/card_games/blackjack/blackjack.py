import numpy as np
import pandas as pd

from card_games.card_deck.card_game import Card_Game

class Blackjack(Card_Game):

    def __init__(self, num_players = 0, bankroll = 10000, bet = 5) -> None:
        self.bj_optimal_df = pd.read_csv('python/card_games/blackjack/blackjack_optimal_strategy.csv')
        self.dealer_showing_card = None
        self.target = 21
        self.dealer_target = 17
        self.dealer_stays_at_soft_17 = True
        self.dealer_id = None

        super().__init__(num_players = num_players, include_dealer = True, cards_per_hand = 2, bankroll = bankroll, bet = bet)

    def get_hand_total(self, id):
        tot = 0
        for i in len(self.hands[id]):
            card = self.hands[id][i]
            card_val = card % 13
            if card_val == 12:
                tot += 11
                if tot > self.target:
                    tot -= 10
            if card_val < 12:
                if card_val > 8:
                    tot += 10
                else:
                    tot += (card_val + 2)

    def set_dealer_showing_card_and_dealer_total_score(self):
        self.dealer_id = len(self.hands) - 1
        dealer_hand = self.hands[len(self.hands) - 1]
        self.dealer_showing_card = dealer_hand[1]
        self.dealer_total = self.get_hand_total(len(self.hands) - 1)
    
    def get_action(self, id = None, is_dealer=False):
        # id not included when hand is for dealer.

        if id is None:
            id = self.dealer_id
        if is_dealer:
            tot = self.dealer_total
            if tot >= self.dealer_target:
                action = 'stay'
            if tot > self.target:
                action = 'busted'
            if tot < self.dealer_target:
                action = 'hit'
            return action
        tot = self.get_hand_total(id)
        if tot == self.target:
            # I'm at 21.  Time to chill
            action = 'stay'
        if tot < self.target:
            # check the strategy to determine next action
            action = None
        if tot > self.target:
            action = 'busted'
        return action

    def play_hand(self, id, action = None):
        
        if self.dealer_showing_card is None:
            self.set_dealer_showing_card_and_dealer_total_score()

        if action is not None:
            func = getattr(self, action)
            func(id)
            return

        if id == len(self.hands) - 1:
            self.get_action(is_dealer=True)
            func = getattr(self, action)
            func(id)
            return

        hand = self.hands[id]

        hard = True
        for card in hand:
            if card % 13 == 12:
                hard = False
                break

        score = sum(hand)
        bjo = self.bj_optimal_df
        hard_or_soft_df = bjo[bjo['hard'] == hard]
        scores_df = hard_or_soft_df[hard_or_soft_df['score_dealer'] == self.dealer_showing_card]
        score_df = hard_or_soft_df[scores_df['score'] == score]
        action = score_df['decision']
        if not pd.isna(score_df['should_split']):
            if score_df['should_split']:
                action = 'split'
        
        func = getattr(self, action)
        func(id)

    def split(self, id):
        card1a = self.hands[id,0]
        card1b = self.get_next_card()
        self.hands.append([card1a, card1b])
        id_to_play = len(self.hands) - 1
        self.play_hand(id_to_play)
        self.hands = self.hands[:-1]
        card2a = self.hands[id,1]
        card2b = self.get_next_card()
        self.hands.append([card2a, card2b])
        self.play_hand(id_to_play)
        self.hands = self.hands[:-1]


    def hit(self, id):

        self.hands[id].append(self.get_next_card())
        action = self.get_action(id)
        self.play_hand(id, action=action)


    def double(self, id):
        self.hands[id].append(self.get_next_card())
        self.bet *= 2
        tot = sum(self.hands[id])
        
        self.play_hand(id, action = 'stay')

    def stay(self, id):
        tot = sum(self.hands[id])
        # this condition should not exist here.  but, adding it for debug
        if tot > self.target:
            self.bankroll -= self.bet
        if tot < self.dealer_total:
            self.bankroll -= self.bet
        if tot > self.dealer_total:
            self.bankroll += self.dealer_total


    def busted(self, id):
        self.bankroll -= self.bet