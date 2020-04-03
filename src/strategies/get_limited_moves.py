import numpy as np
from utils import *


def null_lm(board, player_mark, n_step):
    return [tuple(m) for m in board.legal_moves]


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
    

def lm_consider_self(board, player_mark, n_step):
    
    # Radius setting 
    radius_sur = 2
    radius_star = 2
    
    last_moves = board.last_moves
    self_last_move = last_moves[player_mark]
    opp_mark = get_opponent(player_mark) 
    
    moves = surround_star_block(
        board, self_last_move, player_mark, opp_mark, radius_sur, radius_star)

    return moves
    
def advanced_lm(board, player_mark, n_step):
    
    # Radius setting
    center_radius = 1
    if n_step < 6:
        radius_sur = 1
        radius_star = 0
    elif n_step < 16:
        radius_sur = 1
        radius_star = 5
    else:
        radius_sur = 2
        radius_star = 6
    
    last_moves = board.last_moves
    self_last_move = last_moves[player_mark]
    opp_mark = get_opponent(player_mark) 
    opp_last_move = last_moves[opp_mark]
    
    moves = surround_star_block(
        board, self_last_move, player_mark, opp_mark, radius_sur, radius_star)
    moves_opp = surround_star_block(
        board, opp_last_move, opp_mark, player_mark, radius_sur, radius_star)

    # Combine two move areas together
    for m in moves_opp:
        if m not in moves:
            moves.append(m)
    
    # Consider the surronding moves
    for m in board.surround_moves:
        if m not in moves:
            moves.append(m)
    
    # For the beginning of the game, allow agent to do moves in center area
    if n_step < 6:
        board_width = board.width
        board_height = board.height
        center_move = (board_height // 2, board_width // 2)
        moves_center = surround_moves(board, center_move, center_radius)
        for m in moves_center:
            if m not in moves:
                moves.append(m)
    
    return moves
