import math
import sys


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
    """Evaluate a board for a colour with exited pieces
    
    Arguments:
        board {dict} -- board dictionary
        colour {string} -- player colour
        game_score {dict} -- scores of games
    
    Returns:
        int -- evaluation of a board
    """
    h = 0
    eval_map = range(7, 0, -1)
    count = 0

    for qr in board:
        if board[qr] == colour:
            dist = exit_dist(qr, colour)
            h += eval_map[dist]
            count += 1
    count = count + game_score[colour]
    if count >= 4:
        h += game_score[colour] * 30
    else:
        h += game_score[colour] * -1
    return h