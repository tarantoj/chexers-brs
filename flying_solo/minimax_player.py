# from flying_solo.player import Player
from collections import defaultdict


"""
 Inputs: State s, Player ID p
 Output: (utility vector, best action)
 function MAXN(s, p):
    if CUTOFF-TEST(s):
        return (EVALUATE(s), no-action)
    v-max  <- (-inf, -inf, ..., -inf) # n dimensions
    best-a <- no-action
    for each Action a in ACTIONS(s):
        (v, *) <- MAXN(RESULT(s, a), NEXT(p))
        if v[p] > v-max[p]:
            v-max  <- vbest-a <- areturn (v-max, best-a)
"""


def subtract(a, b):
    """Return the subtraction of two coordinate pairs"""
    q1, r1 = a
    q2, r2 = b
    return (q1 - q2, r1 - r2)


def length(a):
    """Return the length of a coordinate"""
    q, r = a
    return int((abs(q) + abs(r) + abs(-q - r)) / 2)


def distance(a, b):
    """Return the distance between two coordinate pairs"""
    return length(subtract(a, b))


def divup(n, d):
    """Return the division of n by d, rounded up"""
    return (n + d - 1) // d


def eval_dict():
    colours = ["red", "green", "blue"]
    eval_map = [4, 3, 2, 1]
    FINISHING_HEXES = {
        "red": {(3, -3), (3, -2), (3, -1), (3, 0)},
        "green": {(-3, 3), (-2, 3), (-1, 3), (0, 3)},
        "blue": {(-3, 0), (-2, -1), (-1, -2), (0, -3)},
    }

    ran = range(-3, +3 + 1)
    hexes = {(q, r) for q in ran for r in ran if -q - r in ran}
    eval_dict = {colour: {qr: 9 for qr in hexes} for colour in colours}
    for colour in eval_dict:
        for qr in eval_dict[colour]:
            eval_dict[colour][qr] = eval_map[
                min([divup(distance(qr, b), 2) for b in FINISHING_HEXES[colour]])
            ]

    print(eval_dict)


eval_dict()


class Node:
    def __init__(self, state, parent, score):
        self.state = state
        self.children = []
        self.parent = parent
        self.score = score

    def evaluate(self):
        raise NotImplementedError


class Tree:
    def __init__(self, state):
        self.root = Node(state, None, 0)


class MinimaxPlayer(Player):
    def __init__(self, colour):
        super.__init__(colour)
        self.tree = Tree(self.snap(self.board))
        self.history = defaultdict(int, {self.snap(self.board): 1})

    def snap(self, board):
        return (
            # same colour pieces in the same positions
            tuple((qr, p) for qr, p in board.items() if p in self.colours),
            # on the same player's turn
            self.nturns % 3,
        )

    def action(self):
        raise NotImplementedError
