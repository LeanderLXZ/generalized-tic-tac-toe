import numpy as np
from players.players import Player
import DQN
from DQN.env import DQNBoard
from DQN.DQN import *
from QLearningTable.env import QBoard
from QLearningTable.RL_brain import *

class QLearningTablePlayer(Player):

    def __init__(self, filename):
        self.q_table = self.get_q_table(filename)
        self.player_mark = None

    def get_move(self, board, time_left, n_step):
        '''

        :param board:
        :param time_left:
        :return: a tuple represent the move that DQN choose
        '''

        # change the type of the board string
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
        '''
        load the data
        :param filename: the file which saves the data of Qtable
        :return:
        '''
        with open(filename, 'r') as f:
            return eval(f.read())

    def get_action(self, state, value):
        # choose an action from the table
        for k, v in self.q_table[state].items():
            if v == value:
                return k
class DQNPlayer(Player):
    def __init__(self, size, m, load):
        self.size = size
        self.dqn = DeepQNetwork(size ** 2, size ** 2, load)
        self.board = DQN.env.DQNBoard(size, m)

    def get_move(self, board, time_left, n_step):
        '''

        :param board:
        :param time_left:
        :return: a tuple represent the move that DQN choose
        '''

        # change the type of the board string
        board_str = ''.join(board.board.split('\n'))
        state = board_str
        # let dqn choose the action and learn
        action = self.dqn.choose_action(board_str)

        print('action', action)
        # RL take action and get next observation and reward
        reward, done = self.board.step(action, agent=False)
        state_ = self.board.get_state()
        self.dqn.store_transition(state, action, reward, state_)
        if self.dqn.memory_counter > MEMORY_CAPACITY:
            self.dqn.learn()

        # change integer to tuple
        x = int(action // self.size)
        y = int(action % self.size)

        return (x, y)

