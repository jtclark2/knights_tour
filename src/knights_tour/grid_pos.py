class GridPos:
    """
    Coordinates of tiles/spaces on the board
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __add__(self, other):
        return GridPos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return GridPos(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other):
        return GridPos(self.x // other.x, self.y // other.y)

    def __abs__(self):
        return GridPos(abs(self.x), abs(self.y))

    def __repr__(self):
        return "coord(%r, %r)" % (self.x, self.y)
