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
        
        if m == 6:
            self.O_code_dict = self.load_code_dict(
                join(data_dir, 'O_code_6.pkl'))
            self.X_code_dict = self.load_code_dict(
                join(data_dir, 'X_code_6.pkl'))
            self.score_board = self.load_score_dict(
                join(data_dir, '6.pkl'))
        elif m == 8:
            self.O_code_dict = self.load_code_dict(
                join(data_dir, 'O_code_8.pkl'))
            self.X_code_dict = self.load_code_dict(
                join(data_dir, 'X_code_8.pkl'))
            self.score_board = self.load_score_dict(
                join(data_dir, '8.pkl'))
            
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

    def _get_star_score(self, input_array, player_mark):
        """
        according to the current state, this function will calculate a score

        :param input_array: input_array: 8 elements in one list,
        :return: score for current state

        """
        # change to new array
        decode_array = self.decode(input_array, player_mark)

        # get the score
        score = 0
        for i in range(8):
            s1 = str(i) + decode_array[i]
            for j in range(i+1,8):
                s2 = str(j) + decode_array[j]
                s = s1 + s2
                score += self.score_board[s]

        return score

    def get_score(self, board, player_mark, n_step):
        
        if board.is_loser(player_mark):
            return float("-inf")

        if board.is_winner(player_mark):
            return float("inf")
        
        # ['--X--', '--X--', '--XOX', '--XX-']
        # moves_star_4 = self.star_4_drections(board, player_mark, self.radius)
        
        opp_mark = get_opponent(player_mark) 

        my_moves_star_8 = self.star_8_drections(board, player_mark, self.radius)
        my_score = self._get_star_score(my_moves_star_8, player_mark)

        opp_moves_star_8 = self.star_8_drections(board, opp_mark, self.radius)
        opp_score = self._get_star_score(opp_moves_star_8, opp_mark)

        score = my_score - opp_score
        
        return score
