import numpy as np
from copy import copy

class Board(object):
    """The board of generalized TIC-TAC-TOE game.
    """
    BLANK_SPACE = '-'
    PLAYER_1 = 'O'
    PLAYER_2 = 'X'

    def __init__(self, board, moves):
        self.board = board
        self.moves = moves
        self.moved = False
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
                    raise ValueError("Illegal input board!")
        return state

    def copy(self):
        return Board(self.board, self.moves)

    def forecast_move(self, move, player):
        new_board = self.copy()
        new_board.apply_move(move, player)
        return new_board

    def move_is_legal(self, move):
        # TODO: Note the index starts from 0
        i = move[0]
        j = move[1]
        return (0 <= i < self.height and 0 <= j < self.width and
                self._board_state[i, j] == self.BLANK_SPACE and not self.moved)

    @property
    def legal_moves(self):
        return np.argwhere(self._board_state == self.BLANK_SPACE)

    def apply_move(self, move, player):
        if self.move_is_legal(move):
            self._board_state[move[0], move[1]] = player
            self.board = '\n'.join([''.join(row) for row in self._board_state]) + '\n'
            self.moves.insert(0, (player, tuple(move)))
            self.moved = True
        else:
            raise ValueError('Illegal move!')
    
    def is_winner(self, player):
        if self.moves and player == self.moves[0][0]:
            latest_move = self.moves[0][1]
            directions = (((0, 1), (0, -1)), ((1, 0), (-1, 0)),
                          ((1, 1), (-1, -1)), ((1, -1), (-1, 1)))
            for bi_directions in directions:
                count = 1
                for d_i, d_j in bi_directions:
                    i, j = latest_move
                    while True:
                        i, j = i + d_i, j + d_j
                        if (not self.move_is_legal((i, j)) \
                                and self._board_state[i, j] != player):
                            break
                        count += 1
                        if count == 5:
                            return True
            return False
        else: 
            raise ValueError('Input player is not activated!')
    
    @property
    def board_for_print(self):

        axises = list('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
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


b = '------------\n------------\n------------\n------------\n------------\n------------\n------------\n------------\n------------\n------------\n------------\n------------\n'

B = Board(b, ())

print(B.board_for_print)