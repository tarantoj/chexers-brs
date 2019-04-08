class Hex:
    def __init__(self, q, r, colour=""):
        self.q = q
        self.r = r
        self.s = -q-r
        self.colour = colour
        assert not (self.q + self.r + self.s != 0), "q + r + s must be 0"
    def __repr__(self):
        return f"({self.q}, {self.r}): {self.colour}"
        #return ''
    def __eq__(self, other):
        return self.q == other.q and self.r == other.r
    def __str__(self):
        return self.colour
    def __hash__(self):
        return hash((q, r))
    def __lt__(self, other):
        return 0
    def add(self, other):
        return Hex(self.q + other.q, self.r + other.r)
    def substract(self, other):
        return Hex(self.q - other.q, self.r - other.r)
    def get_colour(self):
        return self.colour
    def set_colour(self, colour):
        self.colour = colour
#    def neighbours(self):
#        neighbours = []
#        directions = [Hex(1, 0), Hex(1, -1), Hex(0, -1), Hex(-1, 0), Hex(-1, 1), Hex(0, 1)]
#        for direction in directions:
#            neighbour = self.add(direction)
#            neighbours.append(neighbour)
#        return neighbours
    @staticmethod
    def length(hex):
        return int((abs(hex.q) + abs(hex.r) + abs(hex.s))/2)
    def distance(self, other):
        return Hex.length(self.substract(other))
#    def move(self, other):
#        if not other.colour and other in self.neighbours():
#            other.colour = self.colour
#            self.colour = ""
#            print("MOVE from ({}, {}) to ({}, {})".format(self.q, self.r, other.q, other.r))
#        else:
#            print("Can't move")
#    def jump(self, other):
#        if other.colour and self.colour != other.colour:
#            print()

board = {}
ran = range(-3, +3+1)
for (q, r) in [(q,r) for q in ran for r in ran if -q-r in ran]:
    board[(q, r)] = Hex(q, r)


def get_board():
    return board

def set_piece(q, r, colour):
    board[(q, r)].set_colour(colour)

def get_piece(hex):
    return board[(hex.q, hex.r)]

def move(a, b):
    a_colour = a.get_colour()
    b_colour = b.get_colour()
    a.set_colour(b_colour)
    b.set_colour(a_colour)
    print("MOVE")

def moves(a):
    moves = []
    jumps = []

    directions = [
        Hex(1, 0), Hex(1, -1), Hex(0, -1),
        Hex(-1, 0), Hex(-1, 1), Hex(0, 1)
        ]

    for direction in directions:
        n = a.add(direction)
        try:
            neighbour = get_piece(n)
        except:
            print('except')
            continue
        else:
            print('break')
            continue
        if not neighbour.get_colour():
            moves.append(neighbour)
        elif neighbour.get_colour() != a.get_colour():
            jump = get_piece(neighbour.add(direction))
            if not jump.get_colour():
                jumps.append({'to': jump, 'over': neighbour})

    return {'moves': moves, 'jumps': jumps}
