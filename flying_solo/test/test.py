'''
improved best reply search with transposition tables

best reply search
http://mlanctot.info/files/papers/cg13-brsplus.pdf

alpha-beta pruning with transposition tables
https://en.wikipedia.org/wiki/Negamax

psuedocode for negamax

function negamax(node, depth, α, β, color) is
    alphaOrig := α

    (* Transposition Table Lookup; node is the lookup key for ttEntry *)
    ttEntry := transpositionTableLookup(node)
    if ttEntry is valid and ttEntry.depth ≥ depth then
        if ttEntry.flag = EXACT then
            return ttEntry.value
        else if ttEntry.flag = LOWERBOUND then
            α := max(α, ttEntry.value)
        else if ttEntry.flag = UPPERBOUND then
            β := min(β, ttEntry.value)

        if α ≥ β then
            return ttEntry.value

    if depth = 0 or node is a terminal node then
        return color × the heuristic value of node

    childNodes := generateMoves(node)
    childNodes := orderMoves(childNodes)
    value := −∞
    for each child in childNodes do
        value := max(value, −negamax(child, depth − 1, −β, −α, −color))
        α := max(α, value)
        if α ≥ β then
            break

    (* Transposition Table Store; node is the lookup key for ttEntry *)
    ttEntry.value := value
    if value ≤ alphaOrig then
        ttEntry.flag := UPPERBOUND
    else if value ≥ β then
        ttEntry.flag := LOWERBOUND
    else
        ttEntry.flag := EXACT
    ttEntry.depth := depth	
    transpositionTableStore(node, ttEntry)

    return value



TODO Implement transposition table
- hashable state
- function to generate new state from move
- transposition table must contain:
    - flag [exact, lowerbound or upperbound]
    - value
    - depth

TODO Write improved best reply search function
- work with smaller states of the board (set)
- write a function to create a new state from an action
- return the best action if killed early

TODO Implement iderative deepening
See brs_plus code for signal use
search function must be able to return a valid action if killed early

TODO Improve evaluation function
Take into account and weight the following
- Distance from exit
- # of pieces
- Adjacent pieces
- Score
'''

from flying_solo.utils.player import Player
from flying_solo.utils.board import Board
from collections import namedtuple

State = namedtuple('State', ['board_set', 'turn', 'scores'])


def snap(board, turn, scores):
    board_tuple = ((qr, p) for qr, p in board.items() if p in Board.COLOURS)


class BRSPlayer(Player):
    def __init__(self, colour):
        super().__init__(colour)
