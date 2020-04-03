import pickle
from os.path import join
from utils import *


class Score(object):
    
    def get_score(self, board, player_mark, n_step):
        raise NotImplementedError
    
class NullScore(Score):
    
    def get_score(self, board, player_mark, n_step):
        """This heuristic presumes no knowledge for non-terminal states, and
        returns the same uninformative value for all other states.

        Parameters
        ----------
        board : board.Board
                An instance of the generalized TIC-TAC-TOE board `Board` class 
                representing the current board state.

        Returns
        ----------
        float
            The heuristic value of the current board state.
        """

        if board.is_loser(player_mark):
            return float("-inf")

        if board.is_winner(player_mark):
            return float("inf")

        return 0.


class AdvancedScore(Score):
    
    def  __init__(self, m, data_dir='../data/advanced_score/'):
            
        self.O_code_dict = \
            self.load_code_dict(join(data_dir, 'O_code_{}.pkl').format(str(m)))
        self.X_code_dict = \
            self.load_code_dict(join(data_dir, 'X_code_{}.pkl').format(str(m)))
        self.score_board = self.load_score_dict(
            join(data_dir, '{}.pkl').format(str(m)))
        self.X_straight = self.load_score_dict(
            join(data_dir, 'straight_line_scores_X_{}.pkl').format(str(m)))
        self.O_straight = self.load_score_dict(
            join(data_dir, 'straight_line_scores_O_{}.pkl').format(str(m)))
        
        self.radius = m - 1

    def load_code_dict(self, code_dict):
        with open (code_dict, 'rb') as f:
            code_dict = pickle.load(f)
            return code_dict

    def load_score_dict(self, score_dict):
        with open (score_dict, 'rb') as f:
            score_board = pickle.load(f)
            return score_board

    def decode(self, input_array, mark):
        '''
        decode strings in the input_array

        :param input_array: 8 elements in one list,
        :return: a list

        '''
        n = len(input_array)
        decode_array = []
        if mark == 'X':
            code_dict = self.X_code_dict
        elif mark == 'O':
            code_dict = self.O_code_dict

        for i in range(n):
            encoded_string = input_array[i]
            decoded_string = code_dict[encoded_string]
            decode_array.append(decoded_string)

        return decode_array
    
    def star_4_drections(self, board, player_mark, r):
        
        # Last moves of current board
        last_moves = board.last_moves
        
        # Directions of different ways
        directions = (((0, 1), (0, -1)), ((1, 0), (-1, 0)),
                    ((1, 1), (-1, -1)), ((1, -1), (-1, 1)))
        
        # The list storing moves of different directions
        moves_list = [player_mark] * len(directions)
        
        # Get moves
        for i_direct, bi_directions in enumerate(directions):
            for i_bi, (d_i, d_j) in enumerate(bi_directions):
                count = 0
                i, j = last_moves[player_mark]
                while count < r:
                    i, j = i + d_i, j + d_j
                    if board.on_the_board((i, j)):
                        m = board.get_mark((i, j))
                    else:
                        m = get_opponent(player_mark)
                    if i_bi:
                        moves_list[i_direct] += m
                    else:
                        moves_list[i_direct] = m + moves_list[i_direct]
                    count += 1
        
        # ['--X--', '--X--', '--XOX', '--XX-']
        return moves_list

    def star_8_drections(self, board, player_mark, r):
        
        # Last moves of current board
        last_moves = board.last_moves
        
        # Directions of different ways
        directions = ((-1, 0), (-1, 1), (0, 1), (1, 1),
                      (1, 0), (1, -1), (0, -1), (-1, -1))
        
        # The list storing moves of different directions
        moves_list = [''] * len(directions)
        
        # Get moves
        for i_direct, (d_i, d_j) in enumerate(directions):
            count = 0
            i, j = last_moves[player_mark]
            while count < r:
                i, j = i + d_i, j + d_j
                if board.on_the_board((i, j)):
                    m = board.get_mark((i, j))
                else:
                    m = get_opponent(player_mark)
                moves_list[i_direct] += m
                count += 1
        
        # ['----O', 'X-OOO', '--OOO', '--OOO', 
        #  '--OOO', '--OOO', '----O', 'OX--O']
        return moves_list

    def star_8_drect_with_4_lines(self, board, player_mark, r):
        
        # Last moves of current board
        last_moves = board.last_moves
        
        # Directions of different ways
        directions = ((-1, 0), (-1, 1), (0, 1), (1, 1),
                      (1, 0), (1, -1), (0, -1), (-1, -1))
        
        # The list storing moves of different directions
        moves_list = [''] * len(directions)
        
        # Get moves
        for i_direct, (d_i, d_j) in enumerate(directions):
            count = 0
            i, j = last_moves[player_mark]
            while count < r:
                i, j = i + d_i, j + d_j
                if board.on_the_board((i, j)):
                    m = board.get_mark((i, j))
                else:
                    m = get_opponent(player_mark)
                moves_list[i_direct] += m
                count += 1

        # Get lines
        lines_list = []
        for i_left, i_right in [(0, 4), (1, 5), (2, 6), (3, 7)]:
            lines_list.append(
                moves_list[i_left][::-1] + player_mark + moves_list[i_right])

        # move_list:
        #     ['-XX-O', 'X-OOO', '--OOO', '--OOO', 
        #      'XXOOO', 'X-OOO', '----O', 'OX--O']
        # line_list:
        #     ['O-XX-XXXOOO', 'OOO-XXX-OOO', 
        #      'OOO--X----O', 'OOO--XOX--O']
        return moves_list, lines_list
    
    def _get_star_score(self, input_array, player_mark):
        """
        according to the current state, this function will calculate a score

        :param input_array: input_array: 8 elements in one list,
        :return: score for current state

        """
        # change to new array
        decode_array = self.decode(input_array, player_mark)

        # get the score
        score = 0.
        for i in range(8):
            s1 = str(i) + decode_array[i]
            for j in range(i+1,8):
                s2 = str(j) + decode_array[j]
                s = s1 + s2
                score += self.score_board[s]
        return score
    
    def _get_line_score(self, input_array, player_mark):
        """
        get line score and return it
        
        :param input_array: array, 4 elements each contains 11 chars.
        :param player_mark;'X' or 'O'
        :return: int
        
        """
        score = 0.
        if player_mark == 'X':
            line_dict = self.X_straight
        elif player_mark == 'O':
            line_dict = self.O_straight
        for i in range(4):
            if input_array[i] in line_dict.keys():
                score += line_dict[input_array[i]]
        return score

    def get_score(self, board, player_mark, n_step):
        
        # Win
        if board.is_loser(player_mark):
            return float("-inf")

        # Lose
        if board.is_winner(player_mark):
            return float("inf")
        
        # Get the mark of opponent
        opp_mark = get_opponent(player_mark) 
        
        # Score of my moves
        my_moves_star_8, my_moves_lines = \
            self.star_8_drect_with_4_lines(board, player_mark, self.radius)
        my_star_score = self._get_star_score(my_moves_star_8, player_mark)
        my_line_score = self._get_line_score(my_moves_lines, player_mark)

        # Score of opponent's moves
        opp_moves_star_8, opp_moves_lines = \
            self.star_8_drect_with_4_lines(board, opp_mark, self.radius)
        opp_star_score = self._get_star_score(opp_moves_star_8, opp_mark)
        opp_line_score = self._get_line_score(opp_moves_lines, player_mark)

        # Combine scores
        my_score = my_star_score + my_line_score
        opp_score = opp_star_score + opp_line_score
        score = my_score - opp_score
        
        return score
