from flying_solo.utils.player import Player
from flying_solo.utils.board import Board
import math


def brs(alpha, beta, board, score, player, maximising_player, eval_fn, depth):
    """Best Reply Search

    Schadd, Maarten PD, and Mark HM Winands. "Best reply search for multiplayer games." IEEE Transactions on Computational Intelligence and AI in Games 3.1 (2011): 57-66.

    https://dke.maastrichtuniversity.nl/m.winands/documents/BestReplySearch.pdf

    Arguments:
        alpha {float} -- Alpha value
        beta {float} -- Beta value
        board {dict} -- Dictionary representation of the board
        score {dict} -- Dictionary representation of the scores
        player {string} -- Current player
        maximising_player {string} -- Player to search for
        eval_fn {function} -- State evaluation function
        depth {int} -- Depth to search to

    Returns:
        tuple -- value, action tuple
    """

    if Board.terminal_test(score) or depth == 0:
        sign = +1 if player == maximising_player else -1
        return sign * eval_fn(board, maximising_player, score), None

    best_a = None
    best_v = -math.inf

    actions = []
    if player == maximising_player:
        # Search maximising players moves
        actions.extend([(maximising_player, a)
                        for a in Board.available_actions(board, maximising_player)])
    else:
        # Search other players moves
        for colour in Board.COLOURS:
            if colour != maximising_player:
                actions.extend([(colour, a)
                                for a in Board.available_actions(board, colour)])

    def map(atype):
        if atype == "EXIT":
            return 0
        elif atype == "JUMP":
            return 1
        elif atype == "MOVE":
            return 2
        elif atype == "PASS":
            return 3

    actions.sort(key=lambda x: map(x[1][0]))  # Naive move ordering

    for colour, action in actions:
        captured = Board.apply_action(score, board, colour, action)

        if depth == 5 and score[maximising_player] == 4:
            return (0, action)  # Early exit if game won this turn

        next_player = maximising_player if colour != maximising_player else ""

        v, _ = brs(-beta, -alpha, board, score,
                   next_player, maximising_player, eval_fn, depth - 1)

        Board.reverse_action(score, board, colour, action, captured)

        curr_v = -v
        if curr_v > best_v:
            best_v = curr_v
            best_a = action

        alpha = max(alpha, curr_v)
        if alpha >= beta:
            break

    return best_v, best_a


class BRSPlayer(Player):
    DEPTH = 5

    def __init__(self, colour):
        super().__init__(colour)

    def action(self):
        """Returns best next action, as determined by a BRSPlayer.DEPTH limited best reply search

        Returns:
            tuple -- Chosen action
        """
        _, a = brs(-math.inf, math.inf, self.board,
                   self.score, self.colour, self.colour, Board.evaluate, BRSPlayer.DEPTH)
        return a
