import numpy as np


def null_lm(board, player_mark):
    return board.legal_moves


def get_opponent(player_mark):
    if player_mark == 'X':
        return 'O'
    elif player_mark == 'O':
        return 'X'
    else:
        return None

def surround_moves(board, move, radius):
    legal_moves = board.legal_moves.tolist()
    
    moves = []
    dist = []
    for i in range(move[0] - radius, move[0] + radius + 1):
        for j in range(move[1] - radius, move[1] + radius + 1):
            if [i, j] in legal_moves:
                moves.append((i, j))
                dist.append(max(abs(move[0] - i), abs(move[1] - j)))

    moves = [tuple(m) for m in np.array(moves)[np.argsort(dist)]]

    return moves


def star_moves_block(board, moves, move, player_mark, opponent_mark, radius):
    
    directions = ((0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (-1, -1), (1, -1), (-1, 1))

    for d_i, d_j in directions:
        count = 0
        i, j = move
        while count < radius - 1 and board.on_the_board((i + d_i, j + d_j)):
            i, j = i + d_i, j + d_j
            if board.get_mark((i, j)) == opponent_mark:
                break
            if (i, j) in moves:
                continue
            if board.get_mark((i, j)) != player_mark:
                moves.append((i, j))
            count += 1
            
    return moves

def surround_star_block(board, move, player_mark, 
                        opponent_mark, radius_sur, radius_star):
    if move:
        moves = surround_moves(board, move, radius_sur)
        moves = star_moves_block(
            board, moves, move, player_mark, opponent_mark, radius_star)
        return moves
    else:
        return []
    
    
def lm_consider_both(board, player_mark):
    
    radius_sur = 2
    radius_star = 5
    
    last_moves = board.last_moves
    self_last_move = last_moves[player_mark]
    opp_mark = get_opponent(player_mark) 
    opp_last_move = last_moves[opp_mark]
    
    moves = surround_star_block(
        board, self_last_move, player_mark, opp_mark, radius_sur, radius_star)
    moves_opp = surround_star_block(
        board, opp_last_move, opp_mark, player_mark, radius_sur, radius_star)

    for m in moves_opp:
        if m not in moves:
            moves.append(m)
    
    return moves


def lm_consider_self(board, player_mark):
    
    radius_sur = 2
    radius_star = 5
    
    last_moves = board.last_moves
    self_last_move = last_moves[player_mark]
    opp_mark = get_opponent(player_mark) 
    
    moves = surround_star_block(
        board, self_last_move, player_mark, opp_mark, radius_sur, radius_star)

    return moves
