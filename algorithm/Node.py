from Vector import Vector

Edge = tuple['Node', 'Node']

class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def possible_locations(operations: list[tuple[Vector, list[Edge]]], number_of_nodes: int):
        possible_locations: list[tuple[Vector, list[Edge]]] = []
        for last_op, edges in operations:
            remaining_operations = operations.copy()
            remaining_operations.remove((last_op,edges))

            m = len(operations)
            n = number_of_nodes
            p = n # padding on each side to avoid negative array indexes

            matrix = [[[(False,[]) for _ in range(n + 2*p)] for _ in range(n + 2*p)] for _ in range(m)]
            matrix[0][p][p] = True,[]

            for i in range(len(remaining_operations)):
                for x in range(p, n + p):
                    for y in range(p, n + p):
                        if matrix[i][x][y][0]:
                            matrix[i+1][x][y] = True, matrix[i+1][x][y][1]
                            new_x = x+remaining_operations[i][0].x
                            new_y = y+remaining_operations[i][0].y
                            matrix[i+1][new_x][new_y] = True, (matrix[i+1][x][y][1] + remaining_operations[i][1])
            result = []
            for x in range(p,n + p):
                for y in range(p, n + p):
                    if matrix[len(remaining_operations)][x][y][0]:
                        result.append((Vector(x-p,y-p).add(last_op),matrix[len(remaining_operations)][x][y][1] + edges))
            possible_locations = possible_locations + result
            
        return possible_locations
    
    def moved_by(self, vector: Vector):
        return Node(self.x + vector.x, self.y + vector.y)
    
    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    @staticmethod
    def from_tuple(tuple: tuple[int, int]):
        return Node(tuple[0], tuple[1])
    
    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y
    
    def __lt__(self, other):
         return (self.x, self.y) < (other.x, other.y)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f"N({self.x},{self.y})"