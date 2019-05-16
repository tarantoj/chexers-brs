import math


def exit_dist(qr, colour):
    """how many hexes away from a coordinate is the nearest exiting hex?"""
    q, r = qr
    if colour == "red":
        return 3 - q
    if colour == "green":
        return 3 - r
    if colour == "blue":
        return 3 - (-q - r)


def evaluate(board, colour, game_score):
    """Evaluate a board for a colour with a exited pieces
    
    Arguments:
        board {dict} -- board dictionary
        colour {string} -- player colour
        game_score {dict} -- scores of games
    
    Returns:
        int -- evaluation of a board
    """
    h = 0
    eval_map = [7, 6, 5, 4, 3, 2, 1]

    for qr in board:
        if board[qr] == colour:
            h += eval_map[math.ceil(exit_dist(qr, colour) / 2) + 1]

    h += game_score[colour] * 8
    return h
