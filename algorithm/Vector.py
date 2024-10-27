class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def __eq__(self, value):
        return self.x == value.x and self.y == self.y

    def __hash__(self):
        return hash((self.x, self.y))