from flying_solo.player import Player
from flying_solo.board import Board
from collections import defaultdict
from copy import deepcopy
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
    h = 0
    eval_map = [7, 6, 5, 4, 3, 2, 1]

    for qr in board:
        if board[qr] == colour:
            h += eval_map[math.ceil(exit_dist(qr, colour) / 2) + 1]

    h += game_score[colour] * 8
    return h


def best(board, colour, game_score):
    best_a = ("PASS", None)
    h = 0
    for action in Board.available_actions(board, colour):
        new_game_score = deepcopy(game_score)
        new_board = deepcopy(board)
        Board.apply_action(new_game_score, new_board, colour, action)
        score = evaluate(new_board, colour, new_game_score)
        if score > h:
            h = score
            best_a = action
    return best_a


class GreedyPlayer(Player):
    def __init__(self, colour):
        super().__init__(colour)

    def action(self):
        return best(self.board, self.colour, self.score)
