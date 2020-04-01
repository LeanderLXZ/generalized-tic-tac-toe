import numpy as np
from players.players import Player


class RLPlayer(Player):
    
    def __init__(self, filename):
        self.q_table = self.get_q_table(filename)
        self.player_mark = None

    def get_move(self, board, time_left, n_step):

        board_str = ''.join(board.board.split('\n'))
        action = self.choose_action(board_str, board)
        if action:
            n = board.width
            x = int(action // n)
            y = int(action % n)
            return (x, y)
        else:
            return board.legal_moves[np.random.choice(len(board.legal_moves))]

    def choose_action(self, state, board):
        # action selection
        # exploitation, choose best action
        if state in self.q_table:
            value = max(self.q_table[state].values())
            action = self.get_action(state, value)
            return action
        else:
            return None
    
    def get_q_table(self, filename):
        with open(filename, 'r') as f:
            return eval(f.read())

    def get_action(self, state, value):
        
        for k,v in self.q_table[state].items():
            if v == value:
                return k
