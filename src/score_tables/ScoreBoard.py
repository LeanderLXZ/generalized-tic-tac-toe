import pickle

class ScoreBoard():

    def  __init__(self, m):
        # code_dict = code6.pkl, code8.pkl
        # score_dict = 6.pkl,8.pkl
        # straight_dict = straight_line_scores_O_6.pkl
        self.O_code_dict = self.load_code_dict('O_code_{}.pkl'.format(str(m)))
        self.X_code_dict = self.load_code_dict('X_code_{}.pkl'.format(str(m)))
        self.score_board = self.load_score_dict('{}.pkl'.format(str(m)))
        self.X_straight = self.load_score_dict('straight_line_scores_X_{}.pkl'.format(str(m)))
        self.O_straight = self.load_score_dict('straight_line_scores_O_{}.pkl'.format(str(m)))

    def load_code_dict(self, code_dict):
        with open (code_dict, 'rb') as f:
            code_dict = pickle.load(f)
            return code_dict

    def load_score_dict(self, score_dict):
        with open (score_dict, 'rb') as f:
            score_board = pickle.load(f)
            return score_board

    def load_straight_dict(self, straight_dict):
        with open (straight_dict, 'rb') as f:
            straight_score = pickle.load(f)
            return straight_score

    def decode(self, input_array, symbol):
        '''
        decode strings in the input_array

        :param input_array: 8 elements in one list,
        :return: a list

        '''
        n = len(input_array)
        decode_array = []
        if symbol == 'X':
            code_dict = self.X_code_dict
        elif symbol == 'O':
            code_dict = self.O_code_dict

        for i in range(n):
            encoded_string = input_array[i]
            decoded_string = code_dict[encoded_string]
            decode_array.append(decoded_string)

        return decode_array

    def get_line_score(self, straight_lines, symbol):
        '''
        get line score and return it
        :param straight_lines: array, 4 elements each contains 11 chars.
        :param symbol: 'X' or 'O'
        :return: int
        '''
        score = 0
        if symbol == 'X':
            line_dict = self.X_straight
        elif symbol == 'O':
            line_dict = self.O_straight

        for i in range(4):
            score += line_dict[straight_lines[i]]

        return score

    def get_score(self, input_array, straight_lines, symbol):
        '''
        according to the current state, this function will calculate a score

        :param input_array: input_array: 8 elements in one list,
        :param straight_lines: array, 4 elements each contains 11 chars.
        :return: score for current state

        '''
        # change to new array
        decode_array = self.decode(input_array, symbol)

        # get the score
        score = 0
        for i in range(8):
            s1 = str(i) + decode_array[i]
            for j in range(i+1,8):
                s2 = str(j) + decode_array[j]
                s = s1 + s2
                score += self.score_board[s]

        score += self.get_line_score(straight_lines)

        return score


scoreboard = ScoreBoard(6)
#print(scoreboard.X_code_dict)
#a = rd.sample(scoreboard.O_code_dict.keys(), 8)

a = ['OO-XX', 'X--XX', '-X-XX', 'X--XX', '-X-XX', '---XX', '---XX', 'X--XX']
print(scoreboard.get_score(a,'X'))
print(scoreboard.decode(a,'X'))




        