import copy
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
        self.stayed_hands = []
        

        super().__init__(num_players = num_players, include_dealer = True, cards_per_hand = 2, bankroll = bankroll, bet = bet)

    def get_hand_total(self, id):
        tot = 0
        hand = copy.deepcopy(self.hands[id])
        # reduce cards to the equivalent value in lowest suit
        hand = [x % 13 for x in hand]
        
        # sort cards in hand.  This will put aces at end.  The Ace will be counted as 11 unless it forces hand over 21.
        hand.sort()
        for i in range(len(hand)):
            card = hand[i]
            # 12 is Ace (0 - 12)
            if card < 12:
                # 8 is the rank asociated with a '10'.  below here, all hand values are card value (plus 2 here).
                # above this, values are handled differently
                if card > 8:
                    tot += 10
                else:
                    tot += (card + 2)
            if card == 12:
                tot += 11
                if tot > self.target:
                    tot -= 10
        if id == self.dealer_id:
            self.dealer_total = tot
        return tot

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
                action = 'stand'
            if tot > self.target:
                action = 'busted'
            if tot < self.dealer_target:
                action = 'hit'
            return action
        tot = self.get_hand_total(id)
        if tot == self.target:
            # I'm at 21.  Time to chill
            action = 'stand'
        if tot < self.target:
            # check the strategy to determine next action
            action = None
        if tot > self.target:
            action = 'busted'
        return action

    def play_hand(self, id, action = None):
        
        if self.dealer_id is None:
            self.set_dealer_showing_card_and_dealer_total_score()

        if action is not None:
            func = getattr(self, action)
            func(id)
            return

        if id == self.dealer_id:
            action = self.get_action(is_dealer=True)
            func = getattr(self, action)
            func(id)
            return

        paired = False
        hand = copy.deepcopy(self.hands[id])

        hand = [x % 13 for x in hand]
        if len(hand) == 2:
            if len(set(hand)) == 1:
                paired = True

        hard = True
        for card in hand:
            if card == 12:
                hard = False
                break

        score = self.get_hand_total(id)
        bjo = self.bj_optimal_df
        hard_or_soft_df = bjo[bjo['hard'] == hard]
        scores_df = hard_or_soft_df[hard_or_soft_df['score_dealer'] == self.dealer_showing_card]
        score_df = scores_df[scores_df['score'] == score]
        action = score_df['decision'].values[0]
        if paired:
            should_split_val = score_df['should_split'].values[0]
            if not pd.isna(should_split_val):
                if should_split_val:
                    action = 'split'
        
        func = getattr(self, action)
        func(id)

    def split(self, id):
        card1a = self.hands[id][0]
        card1b = self.get_next_card()
        self.hands.append([card1a, card1b])
        id_to_play = len(self.hands) - 1
        self.play_hand(id_to_play)
        self.hands = self.hands[:-1]
        card2a = self.hands[id][1]
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
        self.bets[id] *= 2
        self.play_hand(id, action = 'stand')

    def stand(self, id):
        self.stayed_hands.append(id)

    def payouts_for_stayed_hands(self):
        for id in self.stayed_hands:
            tot = self.get_hand_total(id)
            if tot == self.dealer_total:
                continue
            if tot < self.dealer_total or tot > self.target:
                self.bankrolls[id] -= self.bets[id]
            else:
                self.bankrolls[id] += self.bets[id]

    def busted(self, id):
        self.bankrolls[id] -= self.bets[id]