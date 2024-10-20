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



"""
    Returns relative position of w to v in direction vector
"""
def get_unit_vector(from_: tuple[int, int], to_: tuple[int, int]):
    return to_[0] - from_[0], to_[1] - from_[1]

def traverse_from_node(
        graph: Graph,
        v: tuple[int, int],
        operations: dict[tuple[tuple[int, int], tuple[int, int]], tuple[str, list[tuple[tuple[int, int], tuple[int, int]]]] | tuple[str, list]]
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
            # process here

            # print("==========")
            # print(path)
            prev = path[len(path) - 2]
            edge = get_edge(w, prev)
            operation = operations.get(edge)

            if operation is not None:
                unit_vector = get_unit_vector(prev, w)
                vec.insert_vector(unit_vector)
                #print(f"node: {w} operation: {operation} on edge {edge}")
            #else:
                #print(f"node: {w} no operation on edge {edge}")

            print(f"node: {w}, edge: {edge}, vec: {vec.multiset}")

            check_interception(vec.get_vectors(), len(graph.nodes))

            # add all neighbours to the stack
            if w in graph.nodes:
                for w0 in graph.neighbors(w):
                    if w0 not in visited:
                        new_vec = Vec(v, w0)
                        new_vec.multiset = vec.multiset.copy()
                        stack.append((w0, path + [w0], new_vec))

            maybe_new_node = get_op_potential_new_node(w, operations, graph.nodes)
            if maybe_new_node is not None:
                if graph.nodes.__contains__(maybe_new_node.get("edge")[0]):
                    new_node: tuple[int, int] = maybe_new_node.get("edge")[1]
                else:
                    new_node: tuple[int, int] = maybe_new_node.get("edge")[0]
                new_vec = Vec(v, new_node)
                new_vec.multiset = vec.multiset.copy()
                stack.append((new_node, path + [new_node], new_vec))




def check_interception(unit_vectors: list[tuple[int, int]], n: int) -> bool:
    dp = np.zeros((n+1, n+1, n+1), dtype=bool)
    dp[0][0][0] = True

    m = len(unit_vectors)

    for j in range(m):
        for i in range(0, j):
            pass

        for i in range(j+1, m):
            pass