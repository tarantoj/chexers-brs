from flying_solo.player import Player
from flying_solo.board import Board
from flying_solo.eval import evaluate
from collections import defaultdict
from copy import deepcopy
import math


def terminal_test(node):
    raise NotImplementedError


def brs(alpha, beta, node, turn, root_player, depth=4):
    if depth <= 0:
        return evaluate(node.board, Board.COLOURS[root_player], node.game_score)

    if turn == root_player:
        actions = Board.available_actions(node.board, node.colour)
        turn = BRSPlayer.MIN
    else:
        actions = []
        for colour in Board.COLOURS:
            if colour != Board.COLOURS[root_player]:
                actions.extend(Board.available_actions(node.board, colour))
        turn = root_player
    for action in actions:
        new_node = Node(node.board, node, node.game_score, node.next_player(), action)
        v = -brs(-beta, -alpha, new_node, turn, root_player, depth - 1)
        if v >= beta:
            return v
        alpha = max(alpha, v)

    return alpha


class Node:
    def __init__(self, board, parent, game_score, player, action):
        self.board = deepcopy(board)
        self.children = []
        self.parent = parent
        self.game_score = deepcopy(game_score)
        self.player = player
        self.colour = Board.COLOURS[player]
        # self.eval_score = evaluate(self.board, self.colour, self.game_score)
        self.action = action
        Board.apply_action(self.game_score, self.board, self.colour, action)

    def next_player(self):
        return (self.player + 1) % 3


class Tree:
    def __init__(self, board, game_score, player):
        self.root = Node(board, None, game_score, player, Board.PASS)


class BRSPlayer(Player):
    MIN = -1

    def __init__(self, colour):
        super().__init__(colour)
        self.player = Board.COLOURS.index(colour)
        self.tree = Tree(self.board, self.score, self.player)

    def action(self):
        best_val = -math.inf
        beta = math.inf
        best_a = None
        for action in Board.available_actions(self.board, self.colour):
            new_node = Node(
                self.tree.root.board,
                self.tree.root,
                self.tree.root.game_score,
                self.tree.root.next_player(),
                action,
            )
            v = brs(best_val, beta, new_node, new_node.player, self.player)
            if v > best_val:
                best_a = action
                best_val = v
        return best_a
