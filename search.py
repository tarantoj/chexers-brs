"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
640092 James Taranto
"""

import sys
import json
import os
import time
import heapq

goals_global = {
    "red": {(3, -3), (3, -2), (3, -1), (3, 0)},
    "green": {(0, -3), (-1, -2), (-2, -1), (-3, 0)},
    "blue": {(-3, 3), (-2, 3), (-1, 3), (0, 3)}
}


def add(a, b):
    """[summary]

    Arguments:
        a {[type]} -- [description]
        b {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return (a[0] + b[0], a[1] + b[1])


def subtract(a, b):
    """[summary]

    Arguments:
        a {[type]} -- [description]
        b {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return (a[0] - b[0], a[1] - b[1])


def length(a):
    """[summary]

    Arguments:
        a {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return int((abs(a[0]) + abs(a[1]) + abs(-a[0]-a[1]))/2)


def distance(a, b):
    """[summary]

    Arguments:
        a {[type]} -- [description]
        b {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    # return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(abs(-a[0]-a[1]) - abs(-b[0]-b[1])))
    #print(f"a: {a}, b: {b}, dist: {length(subtract(a, b))}")
    return length(subtract(a, b))


""" def distance(a, b):
    return int((abs(a[0] - b[0]) 
                + abs(a[0] + a[1] - b[0] - b[1])
                + abs(a[1] - b[1])) / 2) """


def divup(n, d):
    """[summary]

    Arguments:
        n {[type]} -- [description]
        d {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return (n + d - 1) // d


def heuristic(state, heuristic_dict):
    """[summary]

    Arguments:
        state {[type]} -- [description]
        goals {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    h = 0
    for piece in state:
        h += heuristic_dict[piece]
    return h


def generate_heuristics(board, goals):
    """[summary]

    Arguments:
        board {[type]} -- [description]
        goals {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    heuristic_dict = {}
    for piece in board:
        h = 0
        if piece in goals:
            h += 1
        else:
            h += min([divup(distance(piece, goal), 2) for goal in goals])
        heuristic_dict[piece] = h

    return heuristic_dict


def generate_directions(valid_tiles):
    """[summary]

    Arguments:
        board {[type]} -- [description]
        blocks {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    direction_dict = {}
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    for tile in valid_tiles:
        move_directions = []
        jump_directions = []
        for direction in directions:
            move_direction = add(tile, direction)
            jump_direction = add(move_direction, direction)
            if move_direction in valid_tiles:
                move_directions.append(move_direction)
            else:
                move_directions.append(())
            if jump_direction in valid_tiles:
                jump_directions.append(jump_direction)
            else:
                jump_directions.append(())
        direction_dict[tile] = list(zip(move_directions, jump_directions))

    return direction_dict


def actions(state, goals, direction_dict):
    """[summary]

    Arguments:
        state {[type]} -- [description]
        goals {[type]} -- [description]
        direction_dict {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    actions = []
    for piece in state:
        if piece in goals:
            new_state = state.difference(set([piece]))
            actions.append((new_state, f"EXIT from {piece}."))
            continue
        for move, jump in direction_dict[piece]:
            if move:
                if move not in state:
                    new_state = state.difference(
                        set([piece])).union(set([move]))
                    actions.append(
                        (new_state, f"MOVE from {piece} to {move}."))
                elif jump and jump not in state:
                    new_state = state.difference(
                        set([piece])).union(set([jump]))
                    actions.append(
                        (new_state, f"JUMP from {piece} to {jump}."))
            elif jump and jump not in state:
                new_state = state.difference(set([piece])).union(set([jump]))
                actions.append((new_state, f"JUMP from {piece} to {jump}."))
    return actions


def a_star_search(start, goals, direction_dict, heuristic_dict):
    """[summary]

    Arguments:
        start {[type]} -- [description]
        goals {[type]} -- [description]
        direction_dict {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == frozenset():
            break

        for next in actions(current, goals, direction_dict):
            new_cost = cost_so_far[current] + 1
            if next[0] not in cost_so_far or new_cost < cost_so_far[next[0]]:
                cost_so_far[next[0]] = new_cost
                priority = new_cost + heuristic(next[0], heuristic_dict)
                heapq.heappush(frontier, (priority, next[0]))
                came_from[next[0]] = (current, next[1])

    return came_from


def pretty_print(steps, board_dict, blocks, colour):
    """[summary]

    Arguments:
        steps {[type]} -- [description]
        board_dict {[type]} -- [description]
        blocks {[type]} -- [description]
        colour {[type]} -- [description]
    """
    print_board(board_dict)
    time.sleep(1)
    for step in steps:
        board_dict = {key: colour for key in step[0]}
        board_dict.update({key: 'block' for key in blocks})
        print_board(board_dict)
        time.sleep(1)
        os.system('clear')


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        colour = data['colour']
        ran = range(-3, +3+1)
        board = frozenset([(q, r) for q in ran for r in ran if -q-r in ran])
        goals = goals_global[colour]
        blocks = {tuple(x) for x in data['blocks']}
        valid_goals = goals.difference(blocks)
        start = frozenset(tuple(x) for x in data['pieces'])
        valid_tiles = board.difference(blocks)
        direction_dict = generate_directions(valid_tiles)
        heuristic_dict = generate_heuristics(valid_tiles, goals)
        board_dict = {key: colour for key in start}
        board_dict.update({key: 'block' for key in blocks})
        board_dict.update({key: 'goal' for key in goals})
        came_from = a_star_search(
            start, valid_goals, direction_dict, heuristic_dict)
        current = came_from[frozenset()]
        steps = []
        while current:
            steps.append(current)
            current = came_from[current[0]]
        steps.reverse()
        for step in steps:
            print(step[1])
        #pretty_print(steps, board_dict, blocks, colour)


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
