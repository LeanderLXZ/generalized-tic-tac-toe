import time

def print_time(method):
    
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('Time of \'{}\' : {:.3f} s'.format(method.__name__, te - ts))
        return result
    
    return timed

def get_opponent(player_mark):
    if player_mark == 'X':
        return 'O'
    elif player_mark == 'O':
        return 'X'
    else:
        return None
