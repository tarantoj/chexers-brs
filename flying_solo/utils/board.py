import math


class Board:
    """
    Helper class for representing and manipulating a game board
    """
    COLOURS = ["red", "green", "blue"]
    STARTING_HEXES = {
        "red": {(-3, 3), (-3, 2), (-3, 1), (-3, 0)},
        "green": {(0, -3), (1, -3), (2, -3), (3, -3)},
        "blue": {(3, 0), (2, 1), (1, 2), (0, 3)},
    }
    FINISHING_HEXES = {
        "red": {(3, -3), (3, -2), (3, -1), (3, 0)},
        "green": {(-3, 3), (-2, 3), (-1, 3), (0, 3)},
        "blue": {(-3, 0), (-2, -1), (-1, -2), (0, -3)},
    }
    ADJACENT_STEPS = [(-1, +0), (+0, -1), (+1, -1),
                      (+1, +0), (+0, +1), (-1, +1)]
    HEXES = {
        (q, r)
        for q in range(-3, +3 + 1)
        for r in range(-3, +3 + 1)
        if -q - r in range(-3, +3 + 1)
    }
    PASS = ("PASS", None)

    def __init__(self):
        """
        Initialise internal board representation
        """
        self.board = {qr: " " for qr in Board.HEXES}
        for c in Board.COLOURS:
            for qr in Board.STARTING_HEXES[c]:
                self.board[qr] = c

    @staticmethod
    def available_actions(board, colour):
        """Return available actions for a colour on a board

        Modified from the supplied referee code


        Arguments:
            board {dict} -- dictionary representing board state
            colour {string} -- string representing player

        Returns:
            list -- Available actions
        """
        available_actions = []
        for qr in Board.HEXES:
            if board[qr] == colour:
                if qr in Board.FINISHING_HEXES[colour]:
                    available_actions.append(("EXIT", qr))
                q, r = qr
                for dq, dr in Board.ADJACENT_STEPS:
                    for i, atype in [(1, "MOVE"), (2, "JUMP")]:
                        tqr = q + dq * i, r + dr * i
                        if tqr in Board.HEXES:
                            if board[tqr] == " ":
                                available_actions.append((atype, (qr, tqr)))
                                break
        if not available_actions:
            available_actions.append(Board.PASS)
        return available_actions

    @staticmethod
    def apply_action(score, board, colour, action):
        """Applies an action to a board

        Modified from the supplied referee code

        Arguments:
            score {dict} -- Dictionary of scores
            board {dict} -- Dictionary representing board state
            colour {string} -- Player to apply action to
            action {tuple} -- Action to apply
        Returns:
            string -- Colour of captured piece for reversing action
        """
        atype, aargs = action
        captured = None
        if atype == "MOVE":
            qr_a, qr_b = aargs
            board[qr_a] = " "
            board[qr_b] = colour
        elif atype == "JUMP":
            qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
            qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
            board[qr_a] = " "
            board[qr_b] = colour
            captured = board[qr_c]
            board[qr_c] = colour
        elif atype == "EXIT":
            qr = aargs
            board[qr] = " "
            score[colour] += 1
        else:  # atype == "PASS":
            pass
        return captured

    @staticmethod
    def reverse_action(score, board, colour, action, captured):
        """Reverse an action applied to board

        Modified from the supplied referee code

        Arguments:
            score {dict} -- Dictionary of scores
            board {dict} -- Dictionary representing board state
            colour {string} -- Player to apply action to
            action {tuple} -- Action to apply
            captured {string} -- If action to reverse was a capture, the colour of the captured piece to restore
        """
        atype, aargs = action
        if atype == "MOVE":
            qr_a, qr_b = aargs
            board[qr_a] = colour
            board[qr_b] = " "
        elif atype == "JUMP":
            qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
            qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
            board[qr_a] = colour
            board[qr_b] = " "
            board[qr_c] = captured
        elif atype == "EXIT":
            qr = aargs
            board[qr] = colour
            score[colour] -= 1
        else:  # atype == "PASS":
            pass

    @staticmethod
    def terminal_test(scores):
        """Test if state is terminal

        Arguments:
            scores {dict} -- Game score dictionary

        Returns:
            bool -- True if game is over
        """
        for colour in Board.COLOURS:
            if scores[colour] == 4:
                return True
        return False

    @staticmethod
    def exit_dist(qr, colour):
        """Distance a given piece is from exiting

        Arguments:
            qr {tuple} -- Tuple representing piece
            colour {string} -- Colour of piece

        Returns:
            int -- Distance from exit
        """
        q, r = qr
        if colour == "red":
            return 3 - q
        if colour == "green":
            return 3 - r
        if colour == "blue":
            return 3 - (-q - r)

    @staticmethod
    def evaluate(board, colour, scores):
        """State evaluation function

        Arguments:
            board {dict} -- Board to evaluate
            colour {string} -- Player persepective to evaluate from
            scores {dict} -- Score of the state to evaluate

        Returns:
            float -- Score of the state
        """
        self_score = scores[colour]
        self_count = scores[colour]
        others_score = 0
        others_count = 0
        for c in Board.COLOURS:
            if c != colour:
                others_count += scores[c]
                others_score += scores[c]

        self_distances = 0
        others_distances = 0
        pieces = set()
        for qr in board:
            if board[qr] != " ":
                if board[qr] == colour:
                    pieces.add(qr)
                    self_count += 1
                    self_distances += math.sqrt(
                        (abs(Board.exit_dist(qr, board[qr]) - 6)))
                else:
                    others_distances += math.sqrt(
                        (abs(Board.exit_dist(qr, board[qr]) - 6)))
                    others_count += 1
        adjacent_bonus = 0
        for q, r in pieces:
            for dq, dr in Board.ADJACENT_STEPS:
                tqr = (q+dq, r+dr)
                if tqr in pieces:
                    adjacent_bonus += 1
        score_weight = 100 if (self_count-others_count) <= 0 else 10000
        count_weight = 1000
        distance_weight = 1
        adjacent_weight = 10
        return score_weight * (self_score - others_score) +\
            count_weight * (self_count - others_count) +\
            distance_weight * (self_distances - others_distances) +\
            adjacent_weight * (adjacent_bonus)
