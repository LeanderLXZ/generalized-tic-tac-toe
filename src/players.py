import numpy as np
from scores import null_score
from board import GameError


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


class HumanPlayer():

    def __init__(self):
        pass

    def get_move(self, board, time_left):
        input_move = input('Input a move (format: tuple): ')
        try:
           input_move = tuple([int(s) for s in input_move.split(' ')]) 
        except:
            try:
                input_move = eval(input_move)
                if type(input_move) is not tuple:
                    raise GameError('Illegal input! Please input a tuple!')
            except:
                raise GameError('Illegal input! Please input a tuple!')
        return input_move


class RLPlayer():
    
    def __init__(self, filename):
        self.q_table = self.get_q_table(filename)

    def get_move(self, board, time_left):

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


class MinimaxPlayer():
    """Class for minimax agents.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=2, score_fn=null_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.timer_threshold = timeout

    def get_move(self, board, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        board : board.Board
            A instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = board.legal_moves[np.random.choice(len(board.legal_moves))]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(board, self.search_depth)

        except SearchTimeout:
            print('Search timeout!')
            return best_move
    
    def minimax(self, board, depth):
        """Depth-limited minimax search algorithm.

        Parameters
        ----------
        board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = (-1, -1)
        for m in board.legal_moves:
            print('Now searing move {} ...'.format(m))
            v = self.min_value(board.get_moved_board(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
        return best_move

    def min_value(self, board, depth):
        """ Return the value for a win (+1) if the board is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_winner:
            return float("inf")
        if depth <= 0:
            return self.score(board)
        v = float("inf")
        for m in board.legal_moves:
            v = min(v, self.max_value(board.get_moved_board(m), depth - 1))
        return v

    def max_value(self, board, depth):
        """ Return the value for a loss (-1) if the board is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_loser:
            return float("-inf")
        if depth <= 0:
            return self.score(board)
        v = float("-inf")
        for m in board.legal_moves:
            v = max(v, self.min_value(board.get_moved_board(m), depth - 1))
        return v


class AlphaBetaPlayer(MinimaxPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, board, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = board.legal_moves[np.random.choice(len(board.legal_moves))]

        try:
            search_depth = 1
            while True:
                best_move = self.alphabeta(board, search_depth)
                search_depth += 1
        except SearchTimeout:
            print('Search timeout!')
            return best_move

    def alphabeta(self, board, depth, alpha=float("-inf"), beta=float("inf")):
        """Depth-limited minimax search with alpha-beta pruning.
        
        Parameters
        ----------
        board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = (-1, -1)
        for m in board.legal_moves:
            v = self.min_value(board.get_moved_board(m), alpha, beta, depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
            alpha = max(alpha, v)
        return best_move

    def min_value(self, board, alpha, beta, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_winner:
            return float("inf")
        if depth <= 0:
            return self.score(board)
        v = float("inf")
        for m in board.legal_moves:
            v = min(v, self.max_value(
                board.get_moved_board(m), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, board, alpha, beta, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if board.is_loser:
            return float("-inf")
        if depth <= 0:
            return self.score(board)
        v = float("-inf")
        for m in board.legal_moves:
            v = max(v, self.min_value(
                board.get_moved_board(m), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
