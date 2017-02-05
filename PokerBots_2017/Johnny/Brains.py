import numpy as np
import random as random
from random import sample
import copy as cp
from HandEvaluator import HandEvaluator


from keras.models import Sequential
from keras.layers import LSTM, Dense, Merge
from keras.optimizers import Adam
from keras.models import load_model


# Some useful methods.
def is_discard_round(possible_actions):
    splits = possible_actions[-1].split(":")
    return splits[0] == "DISCARD"

def can_check(possible_actions):
    for i in range(len(possible_actions)):
        if possible_actions[i] == "CHECK":
            return True
    return False

def can_call(possible_actions):
    for i in range(len(possible_actions)):
        if possible_actions[i] == "CALL":
            return True
    return False

def can_fold(possible_actions):
    for i in range(len(possible_actions)):
        if possible_actions[i] == "FOLD":
            return True
    return False

def can_put_money_in(possible_actions):
    for i in range(len(possible_actions)):
        splits = possible_actions[i].split(":")
        if splits[0] == "BET" or splits[0] == "RAISE":
            return True, splits[0], int(splits[1]), int(splits[2])
    return False, "", 0,  0








class AdaptiveBrain:
    def __init__(self, restore_from=[]):
        self.hand_evaluator = HandEvaluator()
        self.Q_gamma = 0.9
        self.new_state = []
        
        if restore_from:
            print("Restoring from: " + restore_from)
            self.Q = load_model(restore_from)
        else:
            self.Q = self.initialize_network()
        
    def initialize_network(self):
        TIMESTEPS = None
        TEMPORAL_DATADIM = 5
        STATIC_DATADIM = 1
        
        
        # Learns over the temporal feature matrix
        temporal_model = Sequential()
        temporal_model.add(LSTM(12, return_sequences=True,
                       input_shape=(TIMESTEPS, TEMPORAL_DATADIM)))  # returns a sequence of vectors of dimension 12
        temporal_model.add(LSTM(12, return_sequences=True))  # returns a sequence of vectors of dimension 12
        temporal_model.add(LSTM(12))  # return a single vector of dimension 12

        # Learns over static features.
        static_model = Sequential()
        static_model.add(Dense(5, input_dim=STATIC_DATADIM, activation="relu"))
        
        combined_model = Sequential()
        combined_model.add(Merge([temporal_model, static_model], mode='concat'))
        combined_model.add(Dense(10, activation='relu'))
        combined_model.add(Dense(3, activation='relu'))
        combined_model.add(Dense(1, activation='linear'))
        
        combined_model.compile(loss='mse', optimizer='adam')
        
        return combined_model
        
        
    def enumerate_next_action_vectors(self, bot):   
        BET_INCREMENT = 5
        STACKSIZE = 200.0
        possible_actions = bot.possible_actions
        
        last_in_pot_hero = bot.temporal_feature_matrix[0,-1];
        last_in_pot_villain = bot.temporal_feature_matrix[1,-1];
        street = bot.get_street()
        if is_discard_round(possible_actions):
            # Showdown probabilities of discarding.
            win_pct_discard_none = self.hand_evaluator.evaluate_showdown_probabilities(
               [bot.hand['hole1'], bot.hand['hole2']], bot.hand['board'], 100)
            win_pct_discard_1 = self.hand_evaluator.evaluate_showdown_probabilities(
                [bot.hand['hole2']], bot.hand['board'], 100)
            win_pct_discard_2 = self.hand_evaluator.evaluate_showdown_probabilities(
                [bot.hand['hole1']], bot.hand['board'], 100)
            
            a_none = np.asarray([last_in_pot_hero, last_in_pot_villain, street, 0, 0]).reshape((1,-1))
            a_discard = np.asarray([last_in_pot_hero, last_in_pot_villain, street, 1, 0]).reshape((1,-1))
            
            input_discard_none = [a_none, np.asarray([[win_pct_discard_none]])]
            input_discard_1 = [a_discard, np.asarray([[win_pct_discard_1]])]
            input_discard_2 = [a_discard, np.asarray([[win_pct_discard_2]])]
            
            inputs = [input_discard_none, input_discard_1, input_discard_2]
            action_strs = ['CHECK', 'DISCARD:' + bot.hand['hole1'], 'DISCARD:' + bot.hand['hole2']] 
        else:
            # Available actions should be one of the following:
            # BET:minBet:maxBet *
            # CALL*
            # CHECK *
            # FOLD *
            # RAISE:minRaise:maxRaise * 
            showdown_prob = self.hand_evaluator.evaluate_showdown_probabilities(
               [bot.hand['hole1'], bot.hand['hole2']], bot.hand['board'], 100)
            
            inputs = []
            action_strs = []
            
            # Folding
            #if can_fold(possible_actions):
            #    inputs.append([np.asarray([-1, -1, -1, -1, -1]).reshape((1,-1)), 
            #                   np.asarray([[showdown_prob]]) ])
            #    action_strs.append("FOLD")
            
            # Checking
            inputs.append([np.asarray([last_in_pot_hero, last_in_pot_villain, street, 0, 0]).reshape((1,-1)), 
                               np.asarray([[showdown_prob]]) ])
            if can_check(possible_actions):
                action_strs.append("CHECK")
            else: 
                action_strs.append("FOLD")
                
            # Calling
            if can_call(possible_actions):
                call_amt = bot.temporal_feature_matrix[1,-1]
                inputs.append([np.asarray([call_amt, last_in_pot_villain, street, 0, 0]).reshape((1,-1)), 
                               np.asarray([[showdown_prob]]) ])
                action_strs.append("CALL")

                
            
            # Betting or raising.
            cpmi, action_type, min_bet, max_bet = can_put_money_in(possible_actions)
            if cpmi:
                max_of_prev_street = bot.get_max_of_prev_street(0)
                for i in range(min_bet, max_bet+1, BET_INCREMENT):
                    inputs.append([np.asarray([float(i)/STACKSIZE + max_of_prev_street, last_in_pot_villain, street, 0, 0]).reshape((1,-1)), 
                                   np.asarray([[showdown_prob]]) ])
                    action_strs.append(action_type + ":" + str(i))

                if i != max_bet: # tack on the max_bet
                    i = max_bet
                    inputs.append([np.asarray([float(i)/STACKSIZE + max_of_prev_street, last_in_pot_villain, street, 0, 0]).reshape((1,-1)), 
                                   np.asarray([[showdown_prob]]) ])
                    action_strs.append(action_type + ":" + str(i))

        return inputs, action_strs
    
    
    def evaluate_Q_function(self, S, a):
        # S = state
        # a = action(s)
        
        Q_in_temporal = np.vstack((S, a[0][0])).reshape((1,-1,S.shape[1]))
        Q_in_static = a[0][1]
        
        for i in range(1,len(a)):
            q_i = np.vstack((S, a[i][0])).reshape((1,-1,S.shape[1]))
            Q_in_temporal = np.vstack( (Q_in_temporal, q_i) )
            Q_in_static = np.vstack( (Q_in_static, a[i][1]))
            
        possible_states = [Q_in_temporal, Q_in_static]
        return self.Q.predict(possible_states), possible_states
        
    def update_Q_function(self, bot):
        # self.new_state is the move we made in the last decision point.
        
        if len(self.new_state) > 0: # only update if tfm is initialized.
            print("YO!! Updating Q-function")
            actions, action_strs = self.enumerate_next_action_vectors(bot)
            Qvals, possible_states = self.evaluate_Q_function(bot.temporal_feature_matrix.T, actions)
            reward = bot.hand['winnings']

            if reward != 0: # hand is over -> terminal state. 
                target = reward
            else: # we're still playing the hand
                #newQ = self.Q.predict(self.new_state, batch_size=1)
                maxQ = np.max(Qvals)
                target = self.Q_gamma*maxQ # reward is zero, so our target is simply our expected future reward.
            
            print(target)
            self.Q.fit(self.new_state, np.asarray(target).reshape((1,1)), batch_size=1, nb_epoch=5, verbose=0)
            
    
    
    def learn_from_last_action(self, bot):
        self.update_Q_function(bot)
        
    def get_reward_for_folding(self, bot):
        return -self.bot.temporal_feature_matrix[0,-1]*200.0
        
    def get_epsilon_value(self):
        return 0.1
            
    def make_decision(self, bot):
        print("Making Q decision")
        actions, action_strs = self.enumerate_next_action_vectors(bot)
        
        # Evaluates Q-function over all non-folding actions.
        Qvals, possible_states = self.evaluate_Q_function(bot.temporal_feature_matrix.T, actions)
        
        if random.random() > self.get_epsilon_value():
            best_idx = np.argmax(Qvals)
        else: 
            print("woowowow taking random action!!")
            best_idx = random.randint(0,Qvals.shape[0]-1)
        
        best_temporal_in = possible_states[0][best_idx]
        best_static_in = possible_states[1][best_idx]
        self.new_state = [best_temporal_in.reshape((1,best_temporal_in.shape[0],best_temporal_in.shape[1])), 
                         best_static_in.reshape((1,1))]
        

        return action_strs[best_idx]



    
    
    
    
    
    
    
    
    
    
    
    

class RationalBrain:
    def __init__(self):
        self.hand_evaluator = HandEvaluator() 
        
    def make_decision(self, bot):
        # bot is a poker player bot.
        # by passing bot, this function has access to the internals of bot
        # which includes various features.
        
        possible_actions = bot.possible_actions
        if is_discard_round(possible_actions):
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
                action_str =  "CHECK" if can_check(bot.possible_actions) else "FOLD"
            else:
                if stake_difference < 30:
                    action_str =  "CHECK" if can_check(bot.possible_actions) else "CALL"
                else: 
                    can_put_money_in, action_type, min_bet, max_bet = can_put_money_in(bot.possible_actions)
                    if action_type == "RAISE":
                        bet_val = max(min(stake_difference + current_stake, max_bet), min_bet)
                    else: 
                        bet_val = max(min(stake_difference, max_bet), min_bet)
                    
                    action_str =  action_type + ":" + str(bet_val)
            
            print("ACTION_TAKEN -> " + action_str)   
            return action_str
