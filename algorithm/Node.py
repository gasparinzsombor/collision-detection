from enum import unique
from Vector import Vector

class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def possible_locations(self, operations: list[Vector], number_of_nodes: int):
        possible_locations: list[Vector] = []
        for last_op in operations:
            remaining_operations = operations.copy()
            remaining_operations.remove(last_op)

            m = len(operations)
            n = number_of_nodes

            matrix = [[[False for _ in range(n)] for _ in range(n)] for _ in range(m)]
            matrix[0][0][0] = True

            for i in range(len(remaining_operations)):
                for x in range(n):
                    for y in range(n):
                        if matrix[i][x][y] == True:
                            matrix[i+1][x][y] = True
                            new_x = x+remaining_operations[i].x
                            new_y = y+remaining_operations[i].y
                            matrix[i+1][new_x][new_y] = True
            result = []
            for x in range(n):
                for y in range(n):
                    if matrix[len(remaining_operations)][x][y] == True:
                        result.append(Vector(x,y).add(last_op))
            possible_locations = possible_locations + result
            
        return list(set(possible_locations))