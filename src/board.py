import numpy as np
from copy import copy
from utils import *


class GameError(Exception):
    """Subclass base exception for code clarity. """
    pass


class Board(object):
    """The board of generalized TIC-TAC-TOE game.
    """
    BLANK_SPACE = '-'
    PLAYER_1 = 'O'
    PLAYER_2 = 'X'

    def __init__(self, board, m, last_moves=None):
        self.m = m
        self.board = board
        self.moved = False
        self.last_moves = last_moves if last_moves else {
            self.PLAYER_1: None,
            self.PLAYER_2: None
        }
        self.width = len(board.split('\n')[0])
        self.height = len(board.split('\n')[:-1])
        self._board_state = self.get_board_state()
            
    def get_board_state(self):
        state = np.empty((self.height, self.width), dtype='str')
        for i, row in enumerate(self.board.split('\n')[:-1]):
            for j, cell in enumerate(row):
                if cell in [self.BLANK_SPACE, self.PLAYER_1, self.PLAYER_2]:
                    state[i, j] = cell
                else:
                    raise GameError("illegal input board!")
        
        return state
    
    def get_mark(self, move):
        return self._board_state[move[0], move[1]]

    def on_the_board(self, move):
        return 0 <= move[0] < self.height and 0 <= move[1] < self.width 

    def move_is_legal(self, move):
        # Note the index starts from 0
        return (self.on_the_board and self._board_state[
            move[0], move[1]] == self.BLANK_SPACE and not self.moved)

    @property
    def legal_moves(self):
        return np.argwhere(self._board_state == self.BLANK_SPACE)
        
    def copy(self):
        return Board(copy(self.board), copy(self.m), copy(self.last_moves))

    def apply_move(self, move, player_mark):
        if self.move_is_legal(move):
            self._board_state[move[0], move[1]] = player_mark
            self.board = '\n'.join(
                [''.join(row) for row in self._board_state]) + '\n'
            self.last_moves[player_mark] = tuple(move)
            self.moved = True
        else:
            raise GameError('Illegal move! move: ', move)

    def get_moved_board(self, move, player_mark):
        new_board = self.copy()
        new_board.apply_move(move, player_mark)
        return new_board
    
    def is_winner(self, player_mark):
        if self.last_moves == {}:
            return False
        
        if self.last_moves[player_mark] is None:
            return False
        
        directions = (((0, 1), (0, -1)), ((1, 0), (-1, 0)),
                    ((1, 1), (-1, -1)), ((1, -1), (-1, 1)))
        
        for bi_directions in directions:
            count = 1
            for d_i, d_j in bi_directions:
                i, j = self.last_moves[player_mark]
                while True:
                    i, j = i + d_i, j + d_j
                    if (not self.on_the_board((i, j)) \
                            or self._board_state[i, j] != player_mark):
                        break
                    count += 1
                    if count == self.m:
                        return True
        return False
    
    def is_loser(self, player_mark):
        return self.is_winner(get_opponent(player_mark))
    
    @property
    def board_for_print(self):

        axises = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        out = '    ' + '   '.join(axises[:self.width]) + '\n\r'
        out += '  ' + '-' * (self.width * 4 + 1) + '\n\r'
        for i in range(self.height):
            out += axises[i] + ' | '
            for j in range(self.width):
                if self._board_state[i, j] == '-':
                    out += ' '
                else:
                    out += self._board_state[i, j]
                out += ' | '
            out += '\n\r'
            out += '  ' + '-' * (self.width * 4 + 1) + '\n\r'

        return out
