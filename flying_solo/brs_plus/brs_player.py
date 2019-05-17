from flying_solo.player import Player
from flying_solo.board import Board
from flying_solo.eval import evaluate
from referee.game import _TEMPLATE_NORMAL as TEMPLATE
from collections import defaultdict
from copy import deepcopy
import math
import signal
import sys

DISPLAY = {  # something 5 characters wide for each colour:
    "red": " \033[1m(\033[91mR\033[0m\033[1m)\033[0m ",
    "green": " \033[1m(\033[92mG\033[0m\033[1m)\033[0m ",
    "blue": " \033[1m(\033[94mB\033[0m\033[1m)\033[0m ",
    " ": "     ",
}


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


def brs(alpha, beta, node, turn, root_player, depth):
    if depth <= 0:
        if turn == root_player:
            multiplier = 1
        else:
            multiplier = -1
        return multiplier * evaluate(
            node.board, Board.COLOURS[root_player], node.game_score
        )

    if node.children:
        children = node.children
        if turn == root_player:
            turn = BRSPlayer.MIN
        else:
            turn = root_player
    else:
        if turn == root_player:
            actions = Board.available_actions(node.board, Board.COLOURS[root_player])
            turn = BRSPlayer.MIN
            for action in actions:
                new_node = Node(
                    node.board,
                    node,
                    node.game_score,
                    node.next_player(),
                    action,
                    Board.COLOURS[root_player],
                )
                node.children.append(new_node)
        else:
            for colour in Board.COLOURS:
                if colour != Board.COLOURS[root_player]:
                    for action in Board.available_actions(node.board, colour):
                        new_node = Node(
                            node.board,
                            node,
                            node.game_score,
                            Board.COLOURS.index(colour),
                            action,
                            colour,
                        )
                        node.children.append(new_node)
            turn = root_player
        children = node.children

    for child in children:
        v = -brs(-beta, -alpha, child, turn, root_player, depth - 1)
        # print_board(v, child.board)
        if v >= beta:
            return v
        alpha = max(alpha, v)

    return alpha


def best_reply_search(tree, colour, depth):
    best_val = -math.inf
    beta = math.inf
    best_actions = defaultdict(list)
    if not tree.root.children:
        for action in Board.available_actions(tree.root.board, colour):
            new_node = Node(
                tree.root.board,
                tree.root,
                tree.root.game_score,
                tree.root.next_player(),
                action,
                colour,
            )
            tree.root.children.append(new_node)

    for child in tree.root.children:
        v = -brs(best_val, beta, child, child.player, tree.root.player, depth - 1)
        if v >= best_val:
            best_actions[v].append(child.action)
            best_a = child.action
            best_val = v
        # print(child.action)
        # print_board(best_val, child.board)
    # print(best_val)
    # print(best_a)
    mx = max(best_actions.keys())
    print(best_actions)
    print(best_actions[mx])
    return best_a


def ids(tree, colour, timelimit):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timelimit)
    best_a = None
    depth = 1
    try:
        while True:
            best_a = best_reply_search(tree, colour, depth)
            depth += 1
    except Exception as ex:
        print(ex)

    return best_a


class Node:
    def __init__(self, board, parent, game_score, player, action, c):
        self.board = deepcopy(board)
        self.children = []
        self.parent = parent
        self.game_score = deepcopy(game_score)
        self.player = player
        self.colour = Board.COLOURS[player]
        # self.eval_score = evaluate(self.board, self.colour, self.game_score)
        self.action = action
        Board.apply_action(self.game_score, self.board, c, action)

    def next_player(self):
        return (self.player + 1) % 3

    def prev_player(self):
        return (self.player - 1) % 3


class Tree:
    def __init__(self, board, game_score, player):
        self.root = Node(
            board, None, game_score, player, Board.PASS, Board.COLOURS[player]
        )


class BRSPlayer(Player):
    MIN = -1

    def __init__(self, colour):
        super().__init__(colour)
        self.player = Board.COLOURS.index(colour)
        print(self.player)

    def action(self):

        tree = Tree(self.board, self.score, self.player)
        return ids(tree, self.colour, 2)
