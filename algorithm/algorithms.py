from networkx.classes import Graph
from utilities.utilities import Vec
import numpy as np

def get_op_potential_new_node(w: tuple[int, int], operations, nodes) -> dict[str, str | list[tuple[tuple[int, int], tuple[int, int]]] | tuple[tuple[int, int], tuple[int, int]]] | None:
    for edge, op_info in operations.items():
        if w in edge and (edge[0] not in nodes or edge[1] not in nodes):
            return {'operation': f'{op_info[0]}', 'parallel_edges': op_info[1], 'edge': edge}

    return None

def get_edge(u: tuple[int, int], v: tuple[int, int]):
    if u[0] == v[0]:
        return (v, u) if u[1] < v[1] else (u, v)

    elif u[1] == v[1]:
        return (u, v) if u[0] < v[0] else (v, u)


def determine_edge_orientation(edge):
    """
    Determine if the given edge is horizontal or vertical.

    :param edge: A tuple representing an edge ((x1, y1), (x2, y2)).
    :return: A string "horizontal" if the edge is horizontal, "vertical" if the edge is vertical.
    """
    (x1, y1), (x2, y2) = edge

    if y1 == y2:
        return "horizontal"  # The edge is horizontal if the y-coordinates are the same
    elif x1 == x2:
        return "vertical"  # The edge is vertical if the x-coordinates are the same
    else:
        raise ValueError("Invalid edge: The edge must be either horizontal or vertical.")


def unit_vector_for_movement(w, v, operation, edge):
    """
    Decide the unit vector for the movement of node `w` relative to node `v` based on the edge orientation.

    The edge orientation is determined automatically from the edge's coordinates.

    :param w: A tuple representing the position of node `w` (x_w, y_w).
    :param v: A tuple representing the position of node `v` (x_v, y_v).
    :param operation: A string indicating the operation on the edge ("contraction" or "expansion").
    :param edge: A tuple representing an edge ((x1, y1), (x2, y2)).
    :return: A tuple representing the unit vector of movement (<1, 0>, <0, 1>, <-1, 0>, <0, -1>).
    """
    # Determine if the edge is horizontal or vertical
    edge_orientation = determine_edge_orientation(edge)

    if edge_orientation == "horizontal":
        # Focus on the x-axis: movement left or right
        dx = w[0] - v[0]
        unit_x = dx // abs(dx) if dx != 0 else 0
        unit_y = 0  # No movement in the y-axis for a horizontal edge

    elif edge_orientation == "vertical":
        # Focus on the y-axis: movement up or down
        dy = w[1] - v[1]
        unit_x = 0  # No movement in the x-axis for a vertical edge
        unit_y = dy // abs(dy) if dy != 0 else 0

    # For contraction, we reverse the direction (move towards `v`)
    if operation == "contraction":
        return (-unit_x, -unit_y)

    # For expansion, use the unit vector as is (move away from `v`)
    elif operation == "expansion":
        return (unit_x, unit_y)

def traverse_from_node(
        graph: Graph,
        v: tuple[int, int],
        operations: dict[
            tuple[tuple[int, int], tuple[int, int]],
            tuple[str, list[tuple[tuple[int, int], tuple[int, int]]]] | tuple[str, list]
        ]
        # key is the two coord of an edge
        # value is a tuple of type of operation (expansion / contraction) and a list of coupled operations
        # the coupled operations are also part of the operations dict
    ):

    visited = set()
    stack: list[
        tuple[
            tuple[int, int], # coord of the actual node
            list[tuple[int, int]], # path from v starting point to actual node
            Vec # multiset of vectors on the path from v to actual node
        ]
    ] = [(v, [v], Vec(v,v))]
    while stack:
        (w, path, vec) = stack.pop()
        if w not in visited:
            visited.add(w)

            prev = path[len(path) - 2]
            edge = get_edge(w, prev)
            operation = operations.get(edge)

            if operation is not None:
                unit_vector = unit_vector_for_movement(w, v, operation[0], edge)
                vec.insert_vector(unit_vector)
                #print(f"node: {w} operation: {operation} on edge {edge}")
            #else:
                #print(f"node: {w} no operation on edge {edge}")

            print(f"node: {w}, edge: {edge}, vec: {vec.multiset}")

            if check_interception(vec.get_vectors(), len(graph.nodes), v, w):
                print(f"Collision detected between {v} and {w}")
            else:
                print(f"No collision between {v} and {w}")

            # add all neighbours to the stack
            if w in graph.nodes:
                for w0 in graph.neighbors(w):
                    if w0 not in visited:
                        new_vec = Vec(v, w0)
                        new_vec.multiset = vec.multiset.copy()
                        stack.append((w0, path + [w0], new_vec))

            # there is a possibility of creating a new node with expansion, in this case we have to add that node
            # to the stack and traverse that coordinate as well
            maybe_new_node = get_op_potential_new_node(w, operations, graph.nodes)
            if maybe_new_node is not None:
                if graph.nodes.__contains__(maybe_new_node.get("edge")[0]):
                    new_node: tuple[int, int] = maybe_new_node.get("edge")[1]
                else:
                    new_node: tuple[int, int] = maybe_new_node.get("edge")[0]
                new_vec = Vec(v, new_node)
                new_vec.multiset = vec.multiset.copy()
                stack.append((new_node, path + [new_node], new_vec))




def check_interception(unit_vectors: list[tuple[int, int]], n: int, target_v: tuple[int, int], start_w: tuple[int, int]) -> bool:
    m = len(unit_vectors)
    max_value = n

    w_start_x, w_start_y = start_w

    for j in range(m):
        remaining_vectors = unit_vectors[:j] + unit_vectors[j+1:]
        dp = [[[False for _ in range(max_value + 1)] for _ in range(max_value + 1)] for _ in range(m)]
        dp[0][w_start_x][w_start_y] = True

        for i in range(len(remaining_vectors)):
            v_x, v_y = remaining_vectors[i]

            for x in range(max_value + 1):
                for y in range(max_value + 1):
                    if dp[i][x][y]:
                        dp[i+1][x][y] = True

                        if x + v_x <= max_value and y + v_y <= max_value:
                            dp[i+1][x + v_x][y + v_y] = True

        vx_j, vy_j = unit_vectors[j]
        for x in range(max_value + 1):
            for y in range(max_value + 1):
                if dp[len(remaining_vectors) - 1][x][y]:
                    # Check if moving over vector τ_j causes a collision with v
                    final_x = x + vx_j
                    final_y = y + vy_j
                    if (final_x, final_y) == target_v:
                        return True  # Collision detected

    # No collision between w and v
    return False