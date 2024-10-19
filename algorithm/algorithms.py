from networkx.classes import Graph
from utilities.utilities import Vec
import numpy as np

def get_op_potential_new_node(w: tuple[int, int], operations, nodes):
    for edge, op_info in operations.items():
        if w in edge and (edge[0] not in nodes or edge[1] not in nodes):
            return {'operation': f'{op_info[0]}', 'parallel_edges': op_info[1]}

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

def traverse_from_node(graph: Graph, v: tuple[int, int], operations, vector_trees):
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
            # add all neighbours to the stack
            for w0 in graph.neighbors(w):
                if w0 not in visited:
                    new_vec = Vec(v, w0)
                    new_vec.multiset = vec.multiset.copy()
                    stack.append((w0, path + [w0], new_vec))

            # if w is starting point then we should skip
            if w is v:
                continue

            # process here

            # print("==========")
            # print(path)
            prev = path[len(path) - 2]
            edge = get_edge(w, prev)
            operation = graph.get_edge_data(w,prev)

            if not operation:
                operation = get_op_potential_new_node(w, operations, graph.nodes)

            if operation is not None:
                unit_vector = get_unit_vector(prev, w)
                vec.insert_vector(unit_vector)

            check_interception(vec.get_vectors(), len(graph.nodes))



def check_interception(unit_vectors: list[tuple[int, int]], n: int) -> bool:
    dp = np.zeros((n+1, n+1, n+1), dtype=bool)
    dp[0][0][0] = True

    m = len(unit_vectors)

    for j in range(m):
        for i in range(0, j):
            pass

        for i in range(j+1, m):
            pass