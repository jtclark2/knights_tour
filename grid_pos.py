class grid_pos:
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
        return grid_pos(self.x + other.x, self.y + other.y)

    def __add__(self, other):
        return grid_pos(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return "coord(%r, %r)" % (self.x, self.y)

