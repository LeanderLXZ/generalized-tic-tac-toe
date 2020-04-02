import timeit
import time
import json
import requests

from board import Board, GameError

from players.players import HumanPlayer
from players.minimax import MinimaxPlayer, AlphaBetaPlayer
from players.rl import RLPlayer

from strategies.scores import *
from strategies.get_initial_moves import *
from strategies.get_limited_moves import *


class OnlineGame(object):
    
    BLANK_SPACE = '-'
    PLAYER_1 = 'O'
    PLAYER_2 = 'X'

    def __init__(self, 
                 board_size,
                 m,
                 player_mark, 
                 team_id, 
                 game_id,
                 api_url,
                 headers,
                 time_interval=3,
                 time_limit=300000):
        self.board_size = board_size
        self.m = m
        self.player_mark = player_mark
        self.opponent_mark = self.get_opponent(player_mark)
        self.team_id = team_id
        self.game_id = game_id
        self.api_url = api_url
        self.headers = headers
        self.time_interval = time_interval
        self.time_limit = time_limit
    
    def get_opponent(self, player_mark):
        if player_mark == self.PLAYER_1:
            return self.PLAYER_2
        elif player_mark == self.PLAYER_2:
            return self.PLAYER_1
        else:
            return None    

    def _wait_for_a_while(self):
        time_remaining = \
            self.time_interval - time.time() % self.time_interval
        time.sleep(time_remaining) 
        
    def make_move(self, move): 
        
        print('Now posting the move to server...')
        
        data = {'teamId' : str(self.team_id),
                'move' : '{},{}'.format(*move),  # '3,3'
                'type' : 'move',
                'gameId' : str(self.game_id)}
        
        while True:
            #Wait
            self._wait_for_a_while()
            
            # Get json file from server 
            r = requests.post(self.api_url, data=data, headers=self.headers)
            j = json.loads(r.text)
            
            # If get a correct response
            if j['code'] == 'OK':
                break
            # Meet errors
            if 'Game is no longer open' in j['message']:
                raise GameError('[E] Game is no longer open!')
            if 'Invalid game id' in j['message']:
                raise GameError('[E] Invalid game id!')
            
    def get_opponent_moved_board(self):
        
        print('Waiting for your opponent...')
        
        while True:
            # Wait
            self._wait_for_a_while()
            
            # Get json file from server
            api_url_new = self.api_url+'?type=moves&gameId={}&count={}'.format(
                str(self.game_id), str(2))
            r = requests.get(api_url_new, headers=self.headers)
            j = json.loads(r.text)
            
            # If get a correct response
            if j['code'] == 'OK':
                
                # Check if the opponent win
                board_str = self.get_board_str()
                GameBoard = Board(self.get_board_str(), 
                                  self.m, 
                                  last_moves=None)
                if GameBoard.is_winner(self.opponent_mark):
                    raise GameError('The winner is Player \'{}\'!'.format(
                        self.opponent_mark))
                
                # If the opponent has already done a move
                if j['moves'][0]['symbol'] != self.player_mark:
                    break
            
            # Meet errors
            else:
                if 'Game is no longer open' in j['message']:
                    raise GameError('[E] Game is no longer open!')
                if 'Invalid game id' in j['message']:
                    raise GameError('[E] Invalid game id!')
        
        # Modify the format of last_moves
        #       None
        #       {'O': (1, 2), 'X': None}
        #       {'O': (1, 2), 'X': (2, 3)}
        if len(j['moves']) == 1:
            last_moves = {self.player_mark: None,
                          self.opponent_mark: eval(j['moves'][0]['move'])}
        elif len(j['moves']) == 2:
            last_moves = {self.player_mark: eval(j['moves'][1]['move']),
                          self.opponent_mark: eval(j['moves'][0]['move'])}
        else:
            raise ValueError
        
        # Update last_moves of the board
        GameBoard.last_moves = last_moves
        
        return GameBoard
        
    def get_board_str(self):
        r = requests.get(self.api_url+'?type=boardString&gameId={}'.format(
            str(self.game_id)), headers=self.headers)
        j = json.loads(r.text)
        return j['output']
    
    def game_is_over(self, board):
        # win & lose
        if board.is_winner('O'):
            print('=' * 70)
            print('The winner is Player \'O\'!') 
            return True
        elif board.is_winner('X'):
            print('=' * 70)
            print('The winner is Player \'X\'!') 
            return True
        elif len(board.legal_moves) == 0:
            print('=' * 70)
            print('Game over! No winner!') 
            return True
        else:
            return False
        
    def play_game(self, player):
        
        # Set the timer
        time_millis = lambda: 1000 * timeit.default_timer()
        player.assign_player_mark(self.player_mark)
        
        # Initialize a new board
        init_board = ('-' * self.board_size[1] + '\n') * self.board_size[0]
        GameBoard = Board(init_board, self.m)
        print(GameBoard.board_for_print)
        
        # The step of gaming
        n_step = 0
        
        try:
            # Not the first player
            if self.player_mark != 'O':
                GameBoard = self.get_opponent_moved_board()
                n_step += 1
            
            # If game is not over, do moves
            while not self.game_is_over(GameBoard):
                move_start = time_millis()
                time_left = \
                    lambda : self.time_limit - (time_millis() - move_start)
                
                # get a move
                move = player.get_move(GameBoard, time_left, n_step)
                MovedBoard = GameBoard.get_moved_board(move, self.player_mark)
                print('-' * 70)
                print('Step: ', n_step)
                print('My Move ({}):'.format(self.player_mark), move)
                print(MovedBoard.board_for_print)
                
                # post to server
                self.make_move(move)
                n_step += 1
                
                # Game is over after my move
                if self.game_is_over(MovedBoard):
                    break
                
                # Get the move of opponents
                GameBoard = self.get_opponent_moved_board()
                n_step += 1
                
                print('-' * 70)
                print('Step: ', n_step)
                print('Opponent\'s Move ({}):'.format(self.opponent_mark),
                      GameBoard.last_moves[self.opponent_mark])
                print(GameBoard.board_for_print)
                
        except GameError as e:
            print('=' * 70)
            print('Game over!', e)
            if not self.game_is_over(GameBoard):
                print(GameBoard.board_for_print)


if __name__ == '__main__':
    
    board_size_ = (12, 12)
    m_ = 6
    player_mark_ = 'O'
    team_id_ = '1218'
    game_id_ = '742'
    api_url_ = 'https://www.notexponential.com/aip2pgaming/api/index.php'
    headers_ = {
        'User-Agent' : 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'x-api-key' : 'e2cc2a708b2ebaeaea75',
        'userId' : '932'
    }
    # time interval for requesting - second
    time_interval_ = 3 
    # time limit for each step - milli second
    time_limit_ = 3000
    # timeout threshold for searching - milli second
    timer_threshold_ = 100
    
    P_1 = HumanPlayer()
    P_2 = MinimaxPlayer(
        score_fn=NullScore(),
        initial_moves_fn=im_limited_center_random,
        limited_moves_fn=lm_consider_both,
        timeout=timer_threshold_
    )
    P_3 = AlphaBetaPlayer(
        score_fn=NullScore(),
        initial_moves_fn=im_limited_center_random,
        limited_moves_fn=lm_consider_both,
        timeout=timer_threshold_
    )
    
    P_5 = MinimaxPlayer(
        score_fn=NullScore(),
        initial_moves_fn=im_limited_center_random,
        limited_moves_fn=lm_consider_both,
        timeout=timer_threshold_
    )
    P_6 = AlphaBetaPlayer(
        score_fn=NullScore(),
        initial_moves_fn=im_limited_center_random,
        limited_moves_fn=lm_consider_both,
        timeout=timer_threshold_
    )

    OnlineGame(
        board_size=board_size_,
        m=m_,
        player_mark=player_mark_,
        team_id=team_id_,
        game_id=game_id_,
        api_url=api_url_,
        headers=headers_,
        time_interval=time_interval_,
        time_limit=time_limit_
    ).play_game(P_3)
