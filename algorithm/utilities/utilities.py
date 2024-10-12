import math

from sortedcontainers import SortedList


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def angle(self):
        return math.atan2(self.y, self.x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


class VectorTree:
    def __init__(self):
        self.vectors = SortedList(key=lambda vec: vec.angle() )
        self.sum_vector = Vector(0,0)

    def insert_vector(self, vector):
        self.vectors.add(vector)
        self.sum_vector += vector

    def remove_vector(self, vector):
        self.vectors.remove(vector)
        self.sum_vector -= vector

    def get_sum_vector(self):
        return self.sum_vector