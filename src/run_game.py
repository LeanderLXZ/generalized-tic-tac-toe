import requests
import json
import time
from online_game import *

api_url = 'https://www.notexponential.com/aip2pgaming/api/index.php'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
headers1 = {'User-Agent' : user_agent,
           'x-api-key' : 'e2cc2a708b2ebaeaea75',
           'userId' : '932'}
headers2 = {'User-Agent' : user_agent,
           'x-api-key' : 'b63d17656c29409d6005',
           'userId' : '936'}

# time interval for requesting - second
time_interval_ = 1
# time limit for each step - milli second
time_limit_ = 30000
# timeout threshold for searching - milli second
timer_threshold_ = 100

team_id_ = '1218'
board_size_ = (12, 12)
m_ = 6

# Human Player
P_1 = HumanPlayer()

# Artificial Idiot
P_2 = MinimaxPlayer(
    score_fn=NullScore(),
    initial_moves_fn=null_im,
    limited_moves_fn=null_lm,
    timeout=timer_threshold_,
    verbose=False
)
P_3 = AlphaBetaPlayer(
    score_fn=NullScore(),
    initial_moves_fn=null_im,
    limited_moves_fn=null_lm,
    timeout=timer_threshold_,
    verbose=False
)

# Artificial Intelligence
P_4 = MinimaxPlayer(
    score_fn=AdvancedScore(m_, '../data/advanced_score/'),
    initial_moves_fn=advanced_im,
    limited_moves_fn=advanced_lm,
    timeout=timer_threshold_,
    verbose=False
)
P_5 = AlphaBetaPlayer(
    score_fn=AdvancedScore(m_, '../data/advanced_score/'),
    initial_moves_fn=advanced_im,
    limited_moves_fn=advanced_lm,
    timeout=timer_threshold_,
    verbose=False
)

def create_game(teamId1, teamId2):
    # our two teams: 1218, 1220
    data = {'teamId1' : str(teamId1),
            'teamId2' : str(teamId2),
            'type' : 'game',
            'gameType' : 'TTT'}
    r = requests.post(api_url, data=data, headers=headers1)
    return json.loads(r.text)


def make_move(teamId, gameId, move, headers):
    # TODO: make 'move' as tuple.
    # TODO: raise error if move failed.
    pass

    # move is str
    data = {'teamId' : str(teamId),
            'move' : move,
            'type' : 'move',
            'gameId' : str(gameId)}
    r = requests.post(api_url, data = data, headers=headers)
    return json.loads(r.text)

def get_moves(gameId, count, headers):
    api_url_new = api_url+'?type=moves&gameId={}&count={}'.format(str(gameId), str(count))
    r = requests.get(api_url_new, headers=headers)

    # TODO:
    #       None
    #       [('O', (1, 2)), ('X', None)]
    #       [('O', (1, 2)), ('X', (2, 3))]
    return json.loads(r.text)

def get_board_str(gameId, headers):
    r = requests.get(api_url+'?type=boardString&gameId={}'.format(str(gameId)), headers=headers)
    return json.loads(r.text)

def get_board_map(gameId, headers):
    r = requests.get(api_url+'?type=boardMap&gameId={}'.format(str(gameId)), headers=headers)
    return json.loads(r.text)

def get_my_games(headers):
    r = requests.get(api_url+'?type=myGames', headers=headers)
    return json.loads(r.text)

if __name__ == '__main__':

    myGames = get_my_games(headers1)['myGames']
    while True:
        new_game = get_my_games(headers1)['myGames'][-1]
        if new_game not in myGames:
            game_id = list(new_game.keys())[0]
            game_team = new_game[game_id].split(':')
            if game_team[0] == '1218':
                player_mark_ = 'O'
                opponent_team = game_team[1]
            elif game_team[1] == '1218':
                player_mark_ = 'X'
                opponent_team = game_team[0]
            print("New game with teamId: {}, gameId: {}".format(opponent_team, game_id))


            # Play the game
            try:
                OnlineGame(
                    board_size=board_size_,
                    m=m_,
                    player_mark=player_mark_,
                    team_id=team_id_,
                    game_id=game_id,
                    api_url=api_url,
                    headers=headers1,
                    time_interval=time_interval_,
                    time_limit=time_limit_
                ).play_game(P_5)
            except Exception as e:
                print(e)
                pass

            continue
        else:
            print("Waiting for a new game...")
            time.sleep(1)
            continue
