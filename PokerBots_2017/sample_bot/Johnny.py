import argparse
import socket
import sys

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
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
    
    
    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.hand = {}
        self.hand['action_history'] = []
        self.hand['pot_size'] = []
        
        self.state = {}
        
    
    def parse_data(self, data):
        splits = data.split()
        packet_type = splits[0]
        print packet_type
        
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
            return amt
        else:
            return -amt
        
            
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
        
            
    def parse_get_action(self, data_splits):
        # GETACTION potSize numBoardCards [boardCards] numLastActions [lastActions] numLegalActions [legalActions] timebank
        self.hand['pot_size'].append(int(data_splits[1]))
        
        num_board_cards = int(data_splits[2])
        counter = 3
        self.hand['board'] = data_splits[counter:counter+num_board_cards]
        counter += num_board_cards
        
        num_last_actions = int(data_splits[counter])
        counter += 1
        self.hand['action_history'].append(data_splits[counter:counter+num_last_actions])
        counter += num_last_actions
        
        num_legal_actions = int(data_splits[counter])
        counter += 1
        self.possible_actions = data_splits[counter:counter+num_legal_actions]
        counter += num_legal_actions
        
        self.state['time_bank'] = float(data_splits[-1])

    def parse_new_hand(self, data_splits):
        # NEWHAND handId button holeCard1 holeCard2 myBank otherBank timeBank
        self.hand['hand_id'] = int(data_splits[1])
        self.hand['button'] = data_splits[2]
        self.hand['hole1'] = data_splits[3]
        self.hand['hole2'] = data_splits[4]
        
        self.state['my_bank'] = int(data_splits[5])
        self.state['their_bank'] = int(data_splits[6])
        self.state['time_bank'] = float(data_splits[7])
    
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
            self.parse_data(data)
            
            # Parse data
            # Build features
            # Take action 

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            word = data.split()[0]
            if word == "GETACTION":
                # Currently CHECK on every move. You'll want to change this.
                s.send("CHECK\n")
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()
