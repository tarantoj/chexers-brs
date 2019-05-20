from flying_solo.utils.player import Player
from flying_solo.utils.board import Board
from flying_solo.eval import evaluate
from referee.game import _TEMPLATE_NORMAL as TEMPLATE
from collections import defaultdict
from copy import deepcopy
import math
import signal
import sys
import random

DISPLAY = {  # something 5 characters wide for each colour:
    "red": " \033[1m(\033[91mR\033[0m\033[1m)\033[0m ",
    "green": " \033[1m(\033[92mG\033[0m\033[1m)\033[0m ",
    "blue": " \033[1m(\033[94mB\033[0m\033[1m)\033[0m ",
    " ": "     ",
}

history = {}


def print_board(score, board):
    cells = []
    ran = range(-3, +3 + 1)
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        cells.append(DISPLAY[board[qr]])
    print(TEMPLATE.format(score, *cells))


def handler(signum, frame):
    raise TimeoutError


def terminal_test(node):
    raise NotImplementedError


def brs(alpha, beta, score, board, maximising_colour, current_colour, depth):
    if depth <= 0:
        if maximising_colour == current_colour:
            return evaluate(board, maximising_colour, score)
        else:
            return -evaluate(board, maximising_colour, score)

    for colour in Board.COLOURS:
        if score[colour] == 4:
            if colour == maximising_colour:
                return -math.inf
            else:
                return math.inf

    if maximising_colour == current_colour:
        for action in Board.available_actions(board, maximising_colour):
            captured = Board.apply_action(
                score, board, maximising_colour, action)
            v = -brs(
                -beta,
                -alpha,
                score,
                board,
                maximising_colour,
                Board.next_colour(maximising_colour),
                depth - 1,
            )
            Board.reverse_action(
                score, board, maximising_colour, action, captured)
            if v >= beta:
                return v
            alpha = max(v, alpha)

    else:
        for colour in Board.COLOURS:
            if colour != maximising_colour:
                for action in Board.available_actions(board, colour):
                    captured = Board.apply_action(score, board, colour, action)
                    v = -brs(
                        -beta,
                        -alpha,
                        score,
                        board,
                        maximising_colour,
                        maximising_colour,
                        depth - 1,
                    )
                    Board.reverse_action(
                        score, board, colour, action, captured)
                    if v >= beta:
                        return v
                    alpha = max(v, alpha)

    return alpha


def best_reply_search(score, board, colour, depth):
    # best_a = None
    best_val = -math.inf
    best_actions = defaultdict(list)
    for action in Board.available_actions(board, colour):
        captured = Board.apply_action(score, board, colour, action)
        v = -brs(
            -math.inf,
            math.inf,
            score,
            board,
            colour,
            Board.next_colour(colour),
            depth - 1,
        )
        # print_board(v, board)
        Board.reverse_action(score, board, colour, action, captured)
        if v >= best_val:
            best_actions[v].append(action)
            # best_a = action
            best_val = v
    return random.choice(best_actions[best_val])


def ids(score, board, colour, timelimit):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timelimit)
    best_a = None
    depth = 1
    try:
        while True:
            best_a = best_reply_search(score, board, colour, depth)
            depth += 1
    except Exception as ex:
        print(ex)

    return best_a


class BRSPlayer(Player):
    MIN = -1

    def __init__(self, colour):
        super().__init__(colour)
        self.player = Board.COLOURS.index(colour)

    @staticmethod
    def snap(board):
        return ((qr, p) for qr, p in board.items() if p in Board.COLOURS)

    def action(self):

        return best_reply_search(self.score, self.board, self.colour, 5)
