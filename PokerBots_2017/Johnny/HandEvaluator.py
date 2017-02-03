import deuces as de
from deuces import Card
from deuces import Evaluator
from random import sample
import copy as cp

class HandEvaluator:
    def __init__(self):
        self.card_evaluator =  Evaluator()
    
    def evaluate_showdown_probabilities(self, hand, board, nsim):
            board_cards = [Card.new(j) for j in board]
            hand_cards = [Card.new(j) for j in hand]
            cards_in_play = cp.copy(board_cards)
            cards_in_play.extend(hand_cards)

            board_cards_to_draw = (5 - len(board))
            hand_cards_to_draw = (2 - len(hand)) 
            villain_cards_to_draw = 2
            num_cards_to_draw = board_cards_to_draw + hand_cards_to_draw + villain_cards_to_draw 

            deck = de.Deck()
            draw_deck = list(set(deck.cards)-set(cards_in_play))
            nwins = 0.0
            for i in range(nsim):
                rest_of_cards = sample(draw_deck, num_cards_to_draw)
                board_sim = cp.copy(board_cards)
                hand_sim = cp.copy(hand_cards)

                board_sim.extend(rest_of_cards[0:board_cards_to_draw])
                hand_sim.extend(rest_of_cards[board_cards_to_draw:(board_cards_to_draw+hand_cards_to_draw)])
                villain_hand = rest_of_cards[(board_cards_to_draw+hand_cards_to_draw):]

                villain_rank = self.card_evaluator.evaluate(board_sim,villain_hand)
                hero_rank = self.card_evaluator.evaluate(board_sim,hand_sim)

                nwins += hero_rank < villain_rank

            win_pct = nwins/nsim
            return win_pct