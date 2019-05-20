from flying_solo.utils.board import Board
from flying_solo.utils.player import Player
from flying_solo.eval import evaluate
import math


def terminal_test(score):
    """Test if game is over

    Arguments:
        score {[integer]} -- Dictionary of scores

    Returns:
        [Bool] -- [True if a player has won]
    """
    for colour in Board.COLOURS:
        if score[colour] == 4:
            return True

    return False


def best_reply_search(alpha, beta, board, score, turn, count, maximising_player, depth):
    if depth <= 0 or terminal_test(score):
        return (evaluate(board, turn, score), None)

    actions = []
    if turn == maximising_player:
        actions.extend([(a, maximising_player)
                        for a in Board.available_actions(board, maximising_player)])
    else:
        for c in Board.COLOURS:
            if c != maximising_player:
                actions.extend([(a, c)
                                for a in Board.available_actions(board, c)])
    best_a = None
    for move, colour in actions:
        if colour == maximising_player:
            next_turn = Board.next_colour(colour)
        else:
            next_turn = maximising_player
        captured = Board.apply_action(score, board, colour, move)
        (v, _) = best_reply_search(-beta, -alpha, board, score, next_turn,
                                   count, maximising_player, depth - 1)
        v = -v
        Board.reverse_action(score, board, colour, move, captured)
        if v >= beta:
            return (v, move)
        if alpha >= v:
            alpha = v
            best_a = move

    return (alpha, best_a)


class BRSPlayer(Player):
    def __init__(self, colour):
        super().__init__(colour)

    def action(self):
        _, best_a = best_reply_search(-math.inf, math.inf,
                                      self.board, self.score, self.colour, 0, self.colour, 5)
        return best_a
