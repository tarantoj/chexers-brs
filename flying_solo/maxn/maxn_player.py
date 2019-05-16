from flying_solo.player import Player
from flying_solo.board import Board
from collections import defaultdict
from copy import deepcopy
import math


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
            v-max  <- v
            best-a <- a
        return (v-max, best-a)
"""


def max_n(node, player, depth=3):
    """Max^N algorithm
    
    Arguments:
        board {[type]} -- [description]
        colour {[type]} -- [description]
    """
    if depth == 0:
        return (node.eval_score, None)

    best_a = None
    v_max = [-math.inf, -math.inf, -math.inf]
    player_colour = Board.COLOURS[player]
    for action in Board.available_actions(node.board, player_colour):
        new_game_score = deepcopy(node.game_score)
        new_board = deepcopy(node.board)
        Board.apply_action(new_game_score, new_board, player_colour, action)
        new_player = (player + 1) % 3
        new_node = Node(new_board, node, new_game_score, new_player, action)
        node.children.append(new_node)
        # print(f"turn: {player_colour}, score: {new_node.eval_score}, depth: {depth}")
        v_new, x = max_n(new_node, new_player, depth - 1)
        if v_new > v_max[new_player]:
            v_max[new_player] = v_new
            best_a = action
            # print(new_v_max)
            # print(new_node.action)

    return (v_max[new_player], best_a)


def subtract(a, b):
    """Return the subtraction of two coordinate pairs"""
    q_a, r_a = a
    q_b, r_b = b
    return (q_a - q_b, r_a - r_b)


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


def gen_eval_dict():
    colours = ["red", "green", "blue"]
    eval_map = [7, 6, 5, 4, 3, 2, 1]
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
                min([distance(qr, b) for b in FINISHING_HEXES[colour]])
            ]

    return eval_dict


eval_dict = gen_eval_dict()

""" def evaluate(board, eval_dict, player):
    h = 0
    pieces, turn = board
    colour = ["red", "green", "blue"][turn]
    for piece in pieces:
        qr, c = piece
        if c == colour:
            h += eval_dict[colour][qr]
 """


class Node:
    def __init__(self, board, parent, game_score, player, action):
        self.board = board
        self.children = []
        self.parent = parent
        self.game_score = game_score
        self.player = player
        self.colour = Board.COLOURS[player]
        self.eval_score = self.evaluate()
        self.action = action

    def evaluate(self):
        h = 0
        for qr in self.board:
            if self.board[qr] == self.colour:
                h += eval_dict[self.colour][qr]

        h += self.game_score[self.colour] * 8
        # print(h)
        return h


class Tree:
    def __init__(self, board, game_score, player):
        self.root = Node(board, None, game_score, player, None)


class MaxNPlayer(Player):
    def __init__(self, colour):
        super().__init__(colour)
        self.player = Board.COLOURS.index(colour)
        self.eval_dict = gen_eval_dict()

    def action(self):
        tree = Tree(self.board, self.score, self.player)
        node, action = max_n(tree.root, self.player)
        """ curr = node.parent
        while curr.parent:
            curr = curr.parent """
        return action
