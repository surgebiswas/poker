import numpy as np
import random as random
from random import sample
import copy as cp
from HandEvaluator import HandEvaluator

class RationalBrain:
    def __init__(self, restore_from=[]):
        self.hand_evaluator = HandEvaluator() 
        
    def is_discard_round(self, possible_actions):
        splits = possible_actions[-1].split(":")
        return splits[0] == "DISCARD"
    
    def can_check(self, possible_actions):
        for i in range(len(possible_actions)):
            if possible_actions[i] == "CHECK":
                return True
        return False
            
    def can_put_money_in(self, possible_actions):
        for i in range(len(possible_actions)):
            splits = possible_actions[i].split(":")
            if splits[0] == "BET" or splits[0] == "RAISE":
                return True, splits[0], int(splits[1]), int(splits[2])
        return False, "", 0,  0
    
    def make_decision(self, bot):
        # bot is a poker player bot.
        # by passing bot, this function has access to the internals of bot
        # which includes various features.
        
        possible_actions = bot.possible_actions
        if self.is_discard_round(possible_actions):
            print("This is a discard round")
            # Just take a look at naive showdown probabilities and make the discard decision based on that.
            win_pct_discard_none = self.hand_evaluator.evaluate_showdown_probabilities(
               [bot.hand['hole1'], bot.hand['hole2']], bot.hand['board'], 100)
            win_pct_discard_1 = self.hand_evaluator.evaluate_showdown_probabilities(
                [bot.hand['hole2']], bot.hand['board'], 100)
            win_pct_discard_2 = self.hand_evaluator.evaluate_showdown_probabilities(
                [bot.hand['hole1']], bot.hand['board'], 100)
            
            prob_vec = np.asarray([win_pct_discard_none, win_pct_discard_1, win_pct_discard_2])
            print(prob_vec)
            action_idx = np.argmax(prob_vec)
            
            if action_idx == 0:
                action_str = "CHECK"
            elif action_idx == 1:
                action_str = "DISCARD:" + bot.hand['hole1']
            elif action_idx == 2:
                action_str = "DISCARD:" + bot.hand['hole2']
            
            print("ACTION_TAKEN -> " + action_str)
            return action_str
                
        else: # This is a quantitative bet round, where we have to decide how much money to put on the table (if any <=> fold)
            print("This is a Q-bet round")
            showdown_prob = self.hand_evaluator.evaluate_showdown_probabilities(
                [bot.hand['hole1'], bot.hand['hole2']], bot.hand['board'], 100)
            
            print("showdown prob:" + str(showdown_prob))
            if showdown_prob > 0.8:
                stake_is_worth = random.randint(170, 200)
            elif showdown_prob > 0.6 and showdown_prob < 0.8:
                stake_is_worth = random.randint(100, 169)
            elif showdown_prob > 0.5 and showdown_prob < 0.6:
                stake_is_worth = random.randint(50,100)
            elif showdown_prob > 0.3 and showdown_prob < 0.5:
                stake_is_worth = random.randint(10,50)
            else:
                stake_is_worth = 0
                
            # Available actions should be one of the following:
            # BET:minBet:maxBet
            # CALL
            # CHECK
            # FOLD
            # RAISE:minRaise:maxRaise
            current_stake = np.sum(bot.temporal_feature_matrix[0])*200
            villain_hero_differential = (bot.hand['pot_size'][-1] - current_stake)
            stake_difference = stake_is_worth - villain_hero_differential
            
            print("Current stake: " + str(current_stake))
            print("Stake worth: " + str(stake_is_worth))
            print("Stake diff: " + str(stake_difference))
            
            if stake_difference < 0:
                action_str =  "CHECK" if self.can_check(bot.possible_actions) else "FOLD"
            else:
                if stake_difference < 30:
                    action_str =  "CHECK" if self.can_check(bot.possible_actions) else "CALL"
                else: 
                    can_put_money_in, action_type, min_bet, max_bet = self.can_put_money_in(bot.possible_actions)
                    if action_type == "RAISE":
                        bet_val = max(min(stake_difference + current_stake, max_bet), min_bet)
                    else: 
                        bet_val = max(min(stake_difference, max_bet), min_bet)
                    
                    action_str =  action_type + ":" + str(bet_val)
            
            print("ACTION_TAKEN -> " + action_str)   
            return action_str
