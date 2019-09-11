from flying_solo.utils.player import Player
from flying_solo.utils.board import Board
from copy import copy


def best(board, colour, game_score):
    h = 0
    actions = Board.available_actions(board, colour)
    best_a = actions[0]
    for action in actions:
        new_game_score = copy(game_score)
        new_board = copy(board)
        Board.apply_action(new_game_score, new_board, colour, action)
        score = Board.evaluate(new_board, colour, new_game_score)
        if score > h:
            h = score
            best_a = action
    return best_a


class GreedyPlayer(Player):
    def __init__(self, colour):
        super().__init__(colour)

    def action(self):
        return best(self.board, self.colour, self.score)
