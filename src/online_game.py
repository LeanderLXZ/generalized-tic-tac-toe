import timeit
import time
import json
import requests
from board import Board, GameError
from players import HumanPlayer, MinimaxPlayer, AlphaBetaPlayer, RLPlayer
from scores import null_score


TIME_LIMIT_MILLIS = 300000
TIME_INTERVAL = 3


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
                 time_limit=TIME_LIMIT_MILLIS):
        self.board_size = board_size
        self.m = m
        self.player_mark = player_mark
        self.opponent_mark = self.get_opponent(player_mark)
        self.team_id = team_id
        self.game_id = game_id
        self.api_url = api_url
        self.headers = headers
        self.time_limit = time_limit
    
    def get_opponent(self, player_mark):
        if player_mark == self.PLAYER_1:
            return self.PLAYER_2
        elif player_mark == self.PLAYER_2:
            return self.PLAYER_1
        else:
            return None    
        
    def make_move(self, move): 
        
        print('Now posting the move to server...')
        
        data = {'teamId' : str(self.team_id),
                'move' : '{},{}'.format(*move),  # '3,3'
                'type' : 'move',
                'gameId' : str(self.game_id)}
        
        while True:
            time_remaining = TIME_INTERVAL - time.time() % TIME_INTERVAL
            time.sleep(time_remaining)
            
            r = requests.post(self.api_url, data=data, headers=self.headers)
            j = json.loads(r.text)
            if j['code'] == 'OK':
                break
            if 'Game is no longer open' in j['message']:
                raise GameError('[E] Game is no longer open!')
            if 'Invalid game id' in j['message']:
                raise GameError('[E] Invalid game id!')
            
    def get_last_moves(self):
        
        print('Waiting for opponent...')
        
        while True:
            time_remaining = TIME_INTERVAL - time.time() % TIME_INTERVAL
            time.sleep(time_remaining)
            
            api_url_new = self.api_url+'?type=moves&gameId={}&count={}'.format(
                str(self.game_id), str(2))
            r = requests.get(api_url_new, headers=self.headers)
            j = json.loads(r.text)
            if j['code'] == 'OK':
                if j['moves'][0]['symbol'] != self.player_mark:
                    break
            else:
                if 'Game is no longer open' in j['message']:
                    raise GameError('[E] Game is no longer open!')
                if 'Invalid game id' in j['message']:
                    raise GameError('[E] Invalid game id!')
        
        if len(j['moves']) == 1:
            return {self.player_mark: None,
                    self.opponent_mark: eval(j['moves'][0]['move'])}
        elif len(j['moves']) == 2:
            return {self.player_mark: eval(j['moves'][1]['move']),
                    self.opponent_mark: eval(j['moves'][0]['move'])}
        else:
            raise ValueError
        
    def get_board_str(self):
        r = requests.get(self.api_url+'?type=boardString&gameId={}'.format(
            str(self.game_id)), headers=self.headers)
        j = json.loads(r.text)
        return j['output']
    
    def game_is_over(self, board):
        # win & lose
        if board.is_winner('O'):
            print('The winner is Player \'O\'!') 
            return True
        elif board.is_winner('X'):
            print('The winner is Player \'X\'!') 
            return True
        elif len(board.legal_moves) == 0:
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
        
        try:
            # Not the first player
            if self.player_mark != 'O':
                last_moves = self.get_last_moves()
                GameBoard = Board(self.get_board_str(), 
                                  self.m, 
                                  last_moves=last_moves)
            
            # If game is not over, do moves
            while not self.game_is_over(GameBoard):
                move_start = time_millis()
                time_left = lambda : time_limit - (time_millis() - move_start)
                
                # get a move
                move = player.get_move(GameBoard, time_left)
                print('-' * 70)
                print('My Move ({}):'.format(self.player_mark), move)
                print(GameBoard.get_moved_board(
                    move, self.player_mark).board_for_print)
                
                # post to server
                self.make_move(move)
                
                # Game is over after my move
                if self.game_is_over(GameBoard):
                    break
                
                # get opponent's move
                #       None
                #       {'O': (1, 2), 'X': None}
                #       {'O': (1, 2), 'X': (2, 3)}
                last_moves = self.get_last_moves()
                
                # generate new board
                GameBoard = Board(self.get_board_str(), 
                                  self.m, 
                                  last_moves=last_moves)
                print('-' * 70)
                print('Opponent\'s Move ({}):'.format(
                    self.opponent_mark), last_moves[self.opponent_mark])
                print(GameBoard.board_for_print)
                
        except GameError as e:
            print('Game over! Error:', e)
            if not self.game_is_over(GameBoard):
                print(GameBoard.board_for_print)


if __name__ == '__main__':
    
    board_size_ = (12, 12)
    m_ = 6
    player_mark_ = 'O'
    team_id_ = '1218'
    game_id_ = '683'
    api_url_ = 'https://www.notexponential.com/aip2pgaming/api/index.php'
    headers_ = {
        'User-Agent' : 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'x-api-key' : 'e2cc2a708b2ebaeaea75',
        'userId' : '932'
    }
    
    P_1 = HumanPlayer()
    P_2 = MinimaxPlayer(score_fn=null_score, timeout=10.)
    P_3 = AlphaBetaPlayer(score_fn=null_score, timeout=1.) 
    P_4 = RLPlayer('../data/Qtable3.txt')

    OnlineGame(
        board_size=board_size_,
        m=m_,
        player_mark=player_mark_, 
        team_id=team_id_,
        game_id=game_id_,
        api_url=api_url_,
        headers=headers_,
    ).play_game(P_3)
