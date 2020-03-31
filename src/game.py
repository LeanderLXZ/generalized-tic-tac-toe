import timeit
import numpy as numpy
from board import Board, GameError
from players import HumanPlayer, MinimaxPlayer, AlphaBetaPlayer, RLPlayer
from scores import null_score

TIME_LIMIT_MILLIS = 15000

def play_game(player_1, player_2, board_size, m, time_limit=TIME_LIMIT_MILLIS):

    init_board = ('-' * board_size[1] + '\n') * board_size[0]

    GameBoard = Board(init_board, m)
    print(GameBoard.board_for_print)

    time_millis = lambda: 1000 * timeit.default_timer()

    players = ((player_1, 'O'), (player_2, 'X'))
    
    player_1.assign_player_mark(players[0][1])
    player_2.assign_player_mark(players[1][1])
    player_idx = 1
    player_mark = 'X' 
    while not GameBoard.is_winner(player_mark) \
            and len(GameBoard.legal_moves) != 0:

        print('-' * 70)
        player_idx = player_idx ^ 1
        player_mark = players[player_idx][1] 
        print('Player \'{}\', please move!'.format(player_mark))

        while True:
            try:
                move_start = time_millis()
                time_left = lambda : time_limit - (time_millis() - move_start)
                move = players[player_idx][0].get_move(GameBoard, time_left)
                print('return', move)
                GameBoard = GameBoard.get_moved_board(move)
                print('Move: ', move)
                print('Last Move: ', GameBoard.last_move)
                print(GameBoard.board_for_print)
                break
            except (GameError, SyntaxError) as e:
                print(e)
                print('-' * 70)
                print('Do it again!')

    if GameBoard.is_winner('O'):
        print('The winner is Player \'O\'!') 
    elif GameBoard.is_winner('X'):
        print('The winner is Player \'X\'!') 
    else:
        print('Game over! No winner!') 


if __name__ == '__main__':

    P_1 = HumanPlayer()
    P_2 = MinimaxPlayer(search_depth=3, score_fn=null_score, timeout=10.)
    P_3 = AlphaBetaPlayer(search_depth=3, score_fn=null_score, timeout=10.) 
    P_4 = RLPlayer('../data/Qtable3.txt')

    play_game(P_1, P_3, (3, 3), 3)
