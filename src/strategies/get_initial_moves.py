import numpy as np


def null_im(board):
    if board.n_step == 0:
        return tuple(board.legal_moves[
            np.random.choice(len(board.legal_moves))])
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


def advanced_im(board):
        
    radius = 0
    
    if board.n_step == 0:
        board_width = board.width
        board_height = board.height
        center_move = (board_height // 2, board_width // 2)
        moves = surround_moves(board, center_move, radius)
        return moves[np.random.choice(len(moves))]
    else:
        return None
