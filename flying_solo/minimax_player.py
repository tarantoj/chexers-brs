from flying_solo.player import Player


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.children = []
        self.parent = parent
        self.score = self.evaluate()

    def evaluate(self):
        raise NotImplementedError


class Tree:
    def __init__(self, state):
        self.root = Node(state, None)


class MinimaxPlayer(Player):
    def action(self):
        raise NotImplementedError
