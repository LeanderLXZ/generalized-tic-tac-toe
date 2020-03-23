import numpy as np
from copy import copy


class GameError(Exception):
    """Subclass base exception for code clarity. """
    pass


class Board(object):
    """The board of generalized TIC-TAC-TOE game.
    """
    BLANK_SPACE = '-'
    PLAYER_1 = 'O'
    PLAYER_2 = 'X'

    def __init__(self, board, m, moves=None):
        self.m = m
        self.board = board
        self.moved = False
        self.moves = [] if moves is None else moves
        self.width = len(board.split('\n')[0])
        self.height = len(board.split('\n')[:-1])
        self._board_state = self.get_board_state()

        if self.moves == []:
            self.player = self.PLAYER_1
        elif moves[-1][0] == self.PLAYER_1:
            self.player = self.PLAYER_2
        elif moves[-1][0] == self.PLAYER_2:
            self.player = self.PLAYER_1
        else:
            raise GameError('Wrong move is found in moves!')
            
    def get_board_state(self):
        state = np.empty((self.height, self.width), dtype='str')
        for i, row in enumerate(self.board.split('\n')[:-1]):
            for j, cell in enumerate(row):
                if cell in [self.BLANK_SPACE, self.PLAYER_1, self.PLAYER_2]:
                    state[i, j] = cell
                else:
                    raise GameError("Illegal input board!")
        
        print(state)
        return state

    def on_the_board(self, move):
        return 0 <= move[0] < self.height and 0 <= move[1] < self.width 

    def move_is_legal(self, move):
        # TODO: Note the index starts from 0
        return (self.on_the_board and self._board_state[
            move[0], [move[1]]] == self.BLANK_SPACE and not self.moved)

    @property
    def legal_moves(self):
        return np.argwhere(self._board_state == self.BLANK_SPACE)

    def copy(self):
        return Board(copy(self.board), copy(self.m), copy(self.moves))

    def apply_move(self, move):
        if self.move_is_legal(move):
            self._board_state[move[0], move[1]] = self.player
            self.board = '\n'.join([''.join(row) for row in self._board_state]) + '\n'
            self.moves.append((self.player, tuple(move)))
            self.moved = True
        else:
            raise GameError('Illegal move! move: ', move)

    def get_moved_board(self, move):
        new_board = self.copy()
        new_board.apply_move(move)
        return new_board
    
    @property
    def is_winner(self):
        if self.moves:
            assert self.moves[-1][0] == self.player
             
            latest_move = self.moves[-1][1]
            directions = (((0, 1), (0, -1)), ((1, 0), (-1, 0)),
                          ((1, 1), (-1, -1)), ((1, -1), (-1, 1)))
            for bi_directions in directions:
                count = 1
                for d_i, d_j in bi_directions:
                    i, j = latest_move
                    while True:
                        i, j = i + d_i, j + d_j
                        if (not self.on_the_board((i, j)) \
                                or self._board_state[i, j] != self.player):
                            break
                        count += 1
                        if count == self.m:
                            return True
            return False
        else: 
            return False
    
    @property
    def is_loser(self):
        return not self.is_winner and len(self.legal_moves) == 0
    
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
