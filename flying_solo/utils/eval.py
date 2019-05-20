import math
import sys
from flying_solo.utils.board import Board


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

    # player wins, maximum outcome
    for c in Board.COLOURS:
        # winning state
        if c == colour:
            return math.inf
        # losing state
        else:
            return -math.inf

    h = 0
    eval_map = range(7, 0, -1)
    count = game_score[colour]
    pieces = set()

    for qr in board:
        if board[qr] == colour:
            pieces.add(qr)
            dist = exit_dist(qr, colour)
            h += eval_map[dist]
            count += 1
        elif board[qr] != " ":
            c = board[qr]
            dist = exit_dist(qr, c)
            h -= eval_map[dist]

    # Count adjacent pieces
    adjacent = 0
    for q, r in pieces:
        for dq, dr in Board.ADJACENT_STEPS:
            if (q + dq, r + dr) in pieces:
                adjacent += 1

    for c in Board.COLOURS:
        if c == colour:
            h += game_score[c] * 40
        else:
            h -= game_score[c] * 8

    return h+adjacent
