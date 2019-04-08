class Hex:
    def __init__(self, q, r, colour=""):
        self.q = q
        self.r = r
        self.s = -q-r
        self.colour = colour
        assert not (self.q + self.r + self.s != 0), "q + r + s must be 0"
    def __repr__(self):
        if self.colour: return self.colour
        return ''
    def __eq__(self, other):
        return self.q == other.q and self.r == other.r
    def __str__(self):
        return self.colour
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
#    @staticmethod
#    def length(hex):
#        return int((abs(hex.q) + abs(hex.r) + abs(hex.s))/2)
#    def distance(self, other):
#        return Hex.length(self.substract(other))
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
ran = range(-3, +3-1)
for (q, r) in [(q,r) for q in ran for r in ran if -q-r in ran]:
    board[(q, r)] = Hex(q, r)

def add_piece(q, r, colour):
    board[(q, r)].set_colour(colour)

def move(a, b):
    a_colour = a.get_colour()
    b_colour = b.get_colour()
    a.set_colour(b_colour)
    b.set_colour(b_colour)
    print("MOVE")
