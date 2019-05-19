""" 
TODO: Zobrist hashing
random 64 bit int for each piece in each square
int for whos turn, red= none, green and blue
3*37+2 ints

maybe not

keep a dictionary of board states like referee code, store evaluations

evaluate state by inverse distance to goal and exited pieces.
captured pieces will then result in a greater or lower score, respectively

order moves to prioritise non-adjacent enemy pieces to avoid conflict

write a terminal test function

figure out a space efficient hashable state representation, including whos turn and what has exited
"""
