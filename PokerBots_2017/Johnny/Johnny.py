import argparse
import socket
import sys
import numpy as np
import random as random
from random import sample
import copy as cp
from HandEvaluator import HandEvaluator
from Brains import RationalBrain

np.set_printoptions(linewidth=150)


class Johnny:
    """
    self.bot_name = bot_name in config file. Corresponds to PLAYER_X_NAME field.
    
    self.hand = a dictionary storing properties of the current hand. Has the following keys.
        hand_id = int. ID of hand.
        button = boolean. Are we the dealer?
        hole1 = hole card 1
        hole2 = hole card 2
        board = current known board cards 
        action_history = a list of the last actions. action_history[i] = another list that describes
                         the previous actions up until action point i.
        result = int. Chips won (can be a negative integer if we lost chips)
    
    self.state = A dictionary representing the our state in the current match. Has the following keys.
        my_bank = our current bankroll 
        their_bank = their current bankroll
        time_bank = cumulative time remaining in the match
        
        
    """
    
    
    def __init__(self, bot_name="P1", brain=RationalBrain):
        self.bot_name = bot_name
        self.brain = brain()
        self.state = {}
        self.reset_hand()
        
        
    def reset_hand(self):
        self.hand = {}
        self.hand['action_history'] = []
        self.hand['pot_size'] = []
        self.temporal_feature_matrix = []
        self.possible_actions = []
        
    
    
    
        
    ### ------- PARSING ------- ### 
    def parse_data(self, data):
        splits = data.split()
        packet_type = splits[0]
        
        if packet_type == "NEWHAND":
            self.parse_new_hand(splits)
        elif packet_type == "GETACTION":
            self.parse_get_action(splits)
        elif packet_type == "HANDOVER":
            self.parse_hand_over(splits)
            
    def parse_win_result(self, wr):
        splits = wr.split(":")
        amt = int(splits[1])
        winner = splits[2]
        
        if winner == self.bot_name:
            return amt/2
        else:
            return -amt/2
        
            
    def parse_hand_over(self, data_splits):
        # HANDOVER Stack1 Stack2 numBoardCards [boardCards] numLastActions [lastActions] timeBank
        # Can ignore Stack1 and Stack2 because we'll get it on the next NEWHAND packet.
        num_board_cards = int(data_splits[3])
        counter = 4
        self.hand['board'] = data_splits[counter:counter+num_board_cards]
        counter += num_board_cards
        
        num_last_actions = int(data_splits[counter])
        counter += 1
        self.hand['action_history'].append(data_splits[counter:counter+num_last_actions-1])
        self.hand['result'] = self.parse_win_result(data_splits[counter+num_last_actions-1])
        counter += num_last_actions
        
        self.state['time_bank'] = float(data_splits[-1])
        
    def check_for_hand_update_and_update_hand(self, last_actions):
        for i in range(len(last_actions)):
            splits = last_actions[i].split(":")
            if len(splits) == 4 and splits[0] == "DISCARD":
                # DISCARD:(oldcard):(newcard):PLAYER
                if self.hand['hole1'] == splits[1]:
                    self.hand['hole1'] = splits[2]
                else:
                    self.hand['hole2'] = splits[2]
                print("Updated hand ... ")
                print([self.hand['hole1'], self.hand['hole2']])    
                
                    
                    
    def parse_get_action(self, data_splits):
        # GETACTION potSize numBoardCards [boardCards] numLastActions [lastActions] numLegalActions [legalActions] timebank
        self.hand['pot_size'].append(int(data_splits[1]))
        
        num_board_cards = int(data_splits[2])
        counter = 3
        self.hand['board'] = data_splits[counter:counter+num_board_cards]
        counter += num_board_cards
        
        num_last_actions = int(data_splits[counter])
        counter += 1
        self.check_for_hand_update_and_update_hand(data_splits[counter:counter+num_last_actions]) # update hand if discard was made.
        self.hand['action_history'].append(data_splits[counter:counter+num_last_actions])
        counter += num_last_actions
        
        num_legal_actions = int(data_splits[counter])
        counter += 1
        self.possible_actions = data_splits[counter:counter+num_legal_actions]
        counter += num_legal_actions
        
        self.state['time_bank'] = float(data_splits[-1])

    def parse_new_hand(self, data_splits):
        # NEWHAND handId button holeCard1 holeCard2 myBank otherBank timeBank
        self.reset_hand()
        self.hand['hand_id'] = int(data_splits[1])
        self.hand['button'] = data_splits[2]
        self.hand['hole1'] = data_splits[3]
        self.hand['hole2'] = data_splits[4]
        
        self.state['my_bank'] = int(data_splits[5])
        self.state['their_bank'] = int(data_splits[6])
        self.state['time_bank'] = float(data_splits[7])
    ### ----------------------- ### 
      
    
    
    
    
    
    
    
    
    
    ### ------- FEATURE GENERATION ------- ###
    def update_temporal_feature_matrix(self):
        # Columns represent time steps in a hand.
        # Rows are as follows:
        # 0 - hero action
        # 1 - villain action
        # 2 - street
        # 3 - hero discard?
        # 4 - villain discard?
        al = [item for sublist in self.hand['action_history'] for item in sublist] # linearize action history list
        
        if len(al) > 0:
            if len(self.temporal_feature_matrix) > 0: # check if it's started to fill out.
                start_from_idx = self.temporal_feature_matrix.shape[1]
            else:
                self.temporal_feature_matrix = self.build_temporal_feature_vector(al[0])
                start_from_idx = 1

            for i in range(start_from_idx, len(al)):
                self.temporal_feature_matrix = np.hstack((self.temporal_feature_matrix, 
                                                          self.build_temporal_feature_vector(al[i])))
            
            
            
    def build_temporal_feature_vector(self, performed_action):
        # Performed actions to expect.
        # BET:amount[:actor]
        # CALL[:actor]
        # CHECK[:actor]
        # DEAL:STREET
        # FOLD[:actor]
        # POST:amount:actor
        # DISCARD[:actor]
        # RAISE:amount[:actor]
        # REFUND:amount:actor
        # SHOW:card1:card2:actor
        # TIE:amount:actor
        # WIN:amount:actor
        
        NFEATURES = 5
        STACKSIZE = 200
        hero_idx = 0
        villain_idx = 1
        street_idx = 2
        hero_discard_idx = 3
        villain_discard_idx = 4
        
        if len(self.temporal_feature_matrix) == 0: # if has not been initialized
            street = 0 # preflop
        else:
            street = np.max(self.temporal_feature_matrix[2])
            
              
        splits = performed_action.split(":")
        fv = np.zeros((NFEATURES,1))
        if splits[0] == "BET":
            actor_idx = self.get_actor_idx(splits[-1])    
            amount = float(splits[1])
            fv[actor_idx] = amount/STACKSIZE
            fv[street_idx] = street                    
        elif splits[0] == "CALL":
            actor_idx = self.get_actor_idx(splits[-1])    
            player_to_call = 1 - actor_idx
            call_amt = np.max(self.temporal_feature_matrix[player_to_call])
            fv[actor_idx] = call_amt
            fv[street_idx] = street
        elif splits[0] == "CHECK":
            actor_idx = self.get_actor_idx(splits[-1])   
            fv[actor_idx] = 0
            fv[street_idx] = street
        elif splits[0] == "DEAL":
            if splits[1] == "FLOP":
                street = 1
            elif splits[1] == "TURN":
                street = 2
            elif splits[1] == "RIVER":
                street = 3
            fv[street_idx] = street
        elif splits[0] == "FOLD":
            # Hand is now over. nothing to do here.
            pass
        elif splits[0] == "POST":
            actor_idx = self.get_actor_idx(splits[-1])  
            amount = float(splits[1])/STACKSIZE
            fv[actor_idx] = amount
            fv[street_idx] = street
        elif splits[0] == "DISCARD":
            actor_idx = self.get_actor_idx(splits[-1])  
            fv[actor_idx+3] = 1
            fv[street_idx] = street
        elif splits[0] == "RAISE":
            # Raise specifies the amount raised to, not the amount raised.
            actor_idx = self.get_actor_idx(splits[-1])  
            amount = float(splits[1])/STACKSIZE
            fv[actor_idx] = amount
            fv[street_idx] = street  
        elif splits[0] == "REFUND":
            # Hand is now over. nothing to do here.
            pass
        elif splits[0] == "SHOW":
            # Hand is now over. nothing to do here.
            pass
        elif splits[0] == "TIE":
            # Hand is now over. nothing to do here.
            pass
        elif splits[0] == "WIN":
            # Hand is now over. nothing to do here.
            pass
        
        return fv
    
    def get_actor_idx(self, actor):
        if actor == self.bot_name:
            actor_idx = 0
        else:
            actor_idx = 1
        return actor_idx
    

    ### ------------------------------- ###
    
    
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            print("PACKET -> ", data)
            self.parse_data(data)
            self.update_temporal_feature_matrix()
            
            
            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            word = data.split()[0]
            if word == "GETACTION":
                
                action = self.brain.make_decision(self)
                print(action)
                s.send(action + "\n")
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Johnny()
    bot.run(s)