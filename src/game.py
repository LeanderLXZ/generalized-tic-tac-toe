import timeit
import numpy as numpy

from board import Board, GameError

from players.players import HumanPlayer
from players.minimax import *

from strategies.scores import *
from strategies.get_initial_moves import *
from strategies.get_limited_moves import *


TIME_LIMIT_MILLIS = 15000


def play_game(player_1, player_2, board_size, m, time_limit=TIME_LIMIT_MILLIS):

    # Initialize a game board
    init_board = ('-' * board_size[1] + '\n') * board_size[0]
    gameBoard = Board(init_board, m)
    print(gameBoard.board_for_print)

    # Set the timer
    time_millis = lambda: 1000 * timeit.default_timer()

    # Two players
    players = ((player_1, 'O'), (player_2, 'X'))
    
    # Assign mark to players
    player_1.assign_player_mark(players[0][1])
    player_2.assign_player_mark(players[1][1])
    player_idx = 1
    player_mark = 'X' 
    
    while not gameBoard.is_winner(player_mark) \
            and len(gameBoard.legal_moves) != 0:

        print('-' * 70)
        player_idx = player_idx ^ 1
        player_mark = players[player_idx][1] 
        print('Player \'{}\', please move!'.format(player_mark))

        while True:
            try:
                # Set the timeer
                move_start = time_millis()
                time_left = lambda : time_limit - (time_millis() - move_start)
                
                # Get a move from player
                move = players[player_idx][0].get_move(gameBoard, time_left)
                
                # Generate a new board
                gameBoard = gameBoard.get_moved_board(move, player_mark)
                
                # Display information
                print('Step: ', gameBoard.n_step)
                print('Move: ', move)
                print('Last Move: ', gameBoard.last_moves[player_mark])
                print(gameBoard.board_for_print)
                
                break
            
            except GameError as e:
                print(e)
                print('-' * 70)
                print('Do it again!')

    # Game over
    print('=' * 70)
    if gameBoard.is_winner('O'):
        print('The winner is Player \'O\'!') 
    elif gameBoard.is_winner('X'):
        print('The winner is Player \'X\'!') 
    else:
        print('Game over! No winner!') 


if __name__ == '__main__':
    
    board_size_ = (12, 12)
    m_ = 6
    # time limit for each step - milli second
    time_limit_ = 30000
    # timeout threshold for searching - milli second
    timer_threshold_ = 10
    
    # Human Player
    P_1 = HumanPlayer()
    
    # Artificial Idiot
    P_2 = MinimaxPlayer(
        score_fn=NullScore(),
        initial_moves_fn=null_im,
        limited_moves_fn=null_lm,
        timeout=timer_threshold_, 
        verbose=True
    )
    P_3 = AlphaBetaPlayer(
        score_fn=NullScore(),
        initial_moves_fn=null_im,
        limited_moves_fn=null_lm,
        timeout=timer_threshold_, 
        verbose=True
    )
   
    # Artificial Intelligence
    P_4 = MinimaxPlayer(
        score_fn=AdvancedScore(m_, '../data/advanced_score/'),
        initial_moves_fn=advanced_im,
        limited_moves_fn=advanced_lm,
        timeout=timer_threshold_, 
        verbose=True
    )
    P_5 = AlphaBetaPlayer(
        score_fn=AdvancedScore(m_, '../data/advanced_score/'),
        initial_moves_fn=advanced_im,
        limited_moves_fn=advanced_lm,
        timeout=timer_threshold_,
        verbose=True
    )
    P_6 = AlphaBetaPlayer(
        score_fn=AdvancedScore(m_, '../data/advanced_score/'),
        initial_moves_fn=advanced_im,
        limited_moves_fn=advanced_lm,
        timeout=timer_threshold_, 
        verbose=True
    )
    
    # # Reinforcement Learning
    # from players.rl import *
    # P_7 = QLearningTablePlayer('../data/Qtable3.txt')
    # P_8 = DQNPlayer(12, 6, load = False)
    # # store data
    # P_8.dqn.save_net()
    # P_8.dqn.store_memory()

    # Play the game
    play_game(P_5, P_5, board_size_, m_, time_limit_)
