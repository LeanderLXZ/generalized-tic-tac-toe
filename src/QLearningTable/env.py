import numpy as np


class QBoard:
    def __init__(self, size, m):
        print('size',size)
        self.action_space = np.arange(size ** 2 - 1)
        self.size = size
        self.m = m
        self.board = self.create_board()

    def create_board(self):
        return [['-'] * self.size for _ in range(self.size)]

    def draw_board(self):

        print()
        print('\t\t┌─┬─┬─┐')
        print('\t\t│' + self.board[0][0] + ' │' + self.board[0][1] + ' │' + self.board[0][2] + ' │')
        print('\t\t├─┼─┼─┤')
        print('\t\t│' + self.board[1][0] + ' │' + self.board[1][1] + ' │' + self.board[1][2] + ' │')
        print('\t\t├─┼─┼─┤')
        print('\t\t│' + self.board[2][0] + ' │' + self.board[2][1] + ' │' + self.board[2][2] + ' │')
        print('\t\t└─┴─┴─┘')
        print()

    def check_end(self, location, symbol):
        """
            judge the game is over or not
            return 'win','lost','draw','continue'
        """

        if symbol == 'O':
            result = 'win'
        else:
            result = 'lost'

        x = int(location // self.size)
        y = int(location % self.size)
        # judge row
        count = 0
        for i in range(self.size):
            if self.board[x][i] == symbol:
                count += 1
                if count == self.m:
                    return result
            else:
                count = 0

        # judge col
        count = 0
        for i in range(self.size):
            if self.board[i][y] == symbol:
                count += 1
                if count == self.m:
                    return result
            else:
                count = 0

        # judge cross left up  to right down
        small_one = min(x, y)
        a = x - small_one
        b = y - small_one
        count = 0
        while a <= self.size-1 and b <= self.size-1:
            if self.board[a][b] == symbol:
                count += 1
                if count == self.m:
                    return result
            else:
                count = 0
            a += 1
            b += 1

        # judge cross left down to right up
        a, b = x, y
        while(a<self.size-1 and b>0):
            a+=1
            b-=1

        while a >= 0 and b <= self.size-1:
            if self.board[a][b] == symbol:
                count += 1
                if count == self.m:
                    return result
            else:
                count = 0
            a -= 1
            b += 1

        for i in range(self.size):
            if '-' not in self.board[i]:
                return 'draw'

        return 'continue'

    def reset(self):
        # create a new board
        self.board = self.create_board()

    def get_reward(self, result):
        reward = 0
        done = False
        if result == 'win':
            reward = 100
            done = True

        elif result == 'lost':
            reward = 100
            done = True

        elif result == 'draw':
            reward = 10
            done = True

        return reward, done

    def step(self, action, agent = True):
        # action is a number represents location
        if agent:
            symbol = 'X'
            self.second_move(action)
        else:
            symbol = 'O'
            self.first_move(action)

        result = self.check_end(action, symbol)

        # reward function
        reward, done = self.get_reward(result)

        return reward, done, result

    # return state like 'xxoo'
    def get_state(self):
        state = ''
        for i in range(self.size):
            for j in range(self.size):
                state += self.board[i][j]
        return state

    # 'O'
    def first_move(self, location):
        x = int(location / self.size)
        y = int(location % self.size)
        self.board[x][y] = 'O'

    # 'X'
    def second_move(self, location):
        # our agent's turn
        x = int(location / self.size)
        y = int(location % self.size)
        self.board[x][y] = 'X'

