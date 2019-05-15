class Board:
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
    ADJACENT_STEPS = [(-1, +0), (+0, -1), (+1, -1), (+1, +0), (+0, +1), (-1, +1)]
    MAX_TURNS = 256  # per player
    HEXES = {
        (q, r)
        for q in range(-3, +3 + 1)
        for r in range(-3, +3 + 1)
        if -q - r in range(-3, +3 + 1)
    }

    def __init__(self):
        self.board = {qr: " " for qr in Board.HEXES}
        for c in Board.COLOURS:
            for qr in Board.STARTING_HEXES[c]:
                self.board[qr] = c

    @staticmethod
    def available_actions(board, colour):
        """Return available actions for a colour on a board
        
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
            available_actions.append(("PASS", None))
        return available_actions

    @staticmethod
    def apply_action(score, board, colour, action):
        """Applies an action to a board
        
        Arguments:
            score {dict} -- dictionary of scores
            board {dict} -- dictionary representing board state
            colour {string} -- player to apply action to
            action {tuple} -- action to apply
        """
        atype, aargs = action
        if atype == "MOVE":
            qr_a, qr_b = aargs
            board[qr_a] = " "
            board[qr_b] = colour
        elif atype == "JUMP":
            qr_a, qr_b = (q_a, r_a), (q_b, r_b) = aargs
            qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
            board[qr_a] = " "
            board[qr_b] = colour
            board[qr_c] = colour
        elif atype == "EXIT":
            qr = aargs
            board[qr] = " "
            score[colour] += 1
        else:  # atype == "PASS":
            pass
