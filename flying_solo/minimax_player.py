from flying_solo.player import Player

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
