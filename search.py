"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
640092 James Taranto
"""

import sys
import json
from queue import PriorityQueue
import os
import time

goals_global = {
    "red" : {(3, -3), (3, -2), (3, -1), (3, 0)},
    "green" : {(0, -3), (-1, -2), (-2, -1), (-3, 0)},
    "blue" : {(-3, 3), (-2, 3), (-1, 3), (0, 3)}
}

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def subtract(a, b):
    return (a[0]- b[0], a[1] - b[1])

def length(a):
    return int((abs(a[0]) + abs(a[1]) + abs(-a[0]-a[1]))/2)

def distance(a, b):
    return length(subtract(a, b))


def heuristic(state, goals):
    h = 0
    for piece in state:
        h += min([distance(piece, goal) for goal in goals])
    return h

def actions(state, blocks, board, goals):
    actions = []
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    for piece in state:
        if piece in goals:
            new_state = state.difference(set([piece]))
            actions.append((new_state, f"EXIT from {piece}."))
            continue
        for direction in directions:
            new = add(piece, direction)
            if new in board:
                if new in blocks | state:
                    jump = add(new, direction)
                    if jump not in blocks | state:
                        new_state = state.difference(set([piece])).union(set([jump]))
                        actions.append((new_state, f"JUMP from {piece} to {new}."))
                else:
                    new_state = state.difference(set([piece])).union(set([new]))
                    actions.append((new_state, f"MOVE from {piece} to {new}."))
    
    return actions

def a_star_search(start, blocks, board, goals):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()[1]

        if current == set():
            break

        for next in actions(current, blocks, board, goals):
            new_cost = cost_so_far[current] + 1
            if next[0] not in cost_so_far or new_cost < cost_so_far[next[0]]:
                cost_so_far[next[0]] = new_cost
                priority = new_cost + heuristic(next[0], goals)
                frontier.put((priority, next[0]))
                came_from[next[0]] = (current, next[1])


    return came_from, cost_so_far


 

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        colour = data['colour']
        ran = range(-3, +3+1)
        board = frozenset([(q,r) for q in ran for r in ran if -q-r in ran])
        goals = goals_global[colour]
        blocks = {tuple(x) for x in data['blocks']}
        start = frozenset(tuple(x) for x in data['pieces'])
        end = frozenset()
        board_dict = {key: colour for key in start}
        board_dict.update({key: 'block' for key in blocks})
        board_dict.update({key: 'goal' for key in goals})
        came_from, cost_so_far = a_star_search(start, blocks, board, goals)
        current = came_from[frozenset()]
        steps = []
        while current:
            steps.append(current)
            current = came_from[current[0]]
        steps.reverse()
        print_board(board_dict)
        time.sleep(1)
        for step in steps:
            board_dict = {key: colour for key in step[0]}
            board_dict.update({key: 'block' for key in blocks})
            print_board(board_dict)
            time.sleep(1)
            os.system('clear')



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
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()