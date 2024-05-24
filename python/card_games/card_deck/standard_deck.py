import numpy as np

class Standard_Deck:

    def __init__(self, shuffle_it = True, cards_to_specify = [], specified_card_locations = [], debug = False, num_shuffles = 7) -> None:
        self.deck = np.arange(52)
        self.debug = debug
        self.num_shuffles = num_shuffles
        if shuffle_it:
            self.shuffle(self.num_shuffles)
        self.cards_to_specify = cards_to_specify
        self.specified_card_locations = specified_card_locations
        

        if len(self.cards_to_specify) > 0:
            self.position_cards_for_analysis()
            
    def shuffle(self, num_shuffles = 7):
        seed = None
        if self.debug:
            seed = 0
        np.random.seed(seed=seed)
        for _ in range(num_shuffles):
            np.random.shuffle(self.deck)


    def position_cards_for_analysis(self, cards_to_specify = [], specified_card_locations = []):

        if len(cards_to_specify) == 0:
            cards_to_specify = self.cards_to_specify
        
        if len(specified_card_locations) == 0:
            specified_card_locations = self.specified_card_locations
        
        if len(cards_to_specify) != len(specified_card_locations):
            raise Exception('count of specified cards does not match count of specified card locations')

        for i in range(len(cards_to_specify)):
            card = cards_to_specify[i]
            targ_locn = specified_card_locations[i]
            curr_locn = np.where(self.deck == card)[0][0]
            self.deck[targ_locn], self.deck[curr_locn] = self.deck[curr_locn], self.deck[targ_locn]

        


    