class Mur:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Meuble:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def getCenter(self):
        return (x1 + x2) / 2, (y1 + y2) / 2


mur1 = Mur(0, 0, 0, 1)
