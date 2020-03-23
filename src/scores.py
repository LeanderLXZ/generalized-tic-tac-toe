def null_score(board):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    board : board.Board
            An instance of the generalized TIC-TAC-TOE board `Board` class 
            representing the current board state.

    Returns
    ----------
    float
        The heuristic value of the current board state.
    """

    if board.is_loser:
        return float("-inf")

    if board.is_winner:
        return float("inf")

    return 0.