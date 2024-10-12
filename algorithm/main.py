import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes import Graph


def get_operation_between(u: tuple[int, int], v: tuple[int, int], operations):
    try:
        if u[0] == v[0]:
            return operations[(v, u)] if u[1] < v[1] else operations[(u, v)]

        elif u[1] == v[1]:
            return operations[(u, v)] if u[0] < v[0] else operations[(v, u)]

        return None
    except KeyError:
        return None

def get_edge(u: tuple[int, int], v: tuple[int, int]):
    if u[0] == v[0]:
        return (v, u) if u[1] < v[1] else (u, v)

    elif u[1] == v[1]:
        return (u, v) if u[0] < v[0] else (v, u)



"""
    Returns relative position of w to v in direction vector
"""
# def get_relative_position(v: tuple[int, int], w: tuple[int, int]):
#     if v[0] > w[0]:
#         return Vector()

def traverse_from_node(graph: Graph, v: tuple[int, int], operations, vector_trees):
    visited = set()
    stack: list[tuple[tuple[int, int], list[tuple[int, int]]]] = [(v, [v])]
    while stack:
        (w, path) = stack.pop()
        if w not in visited:
            visited.add(w)
            for w0 in graph.neighbors(w):
                if w0 not in visited:
                    stack.append((w0, path + [w0]))

            if w is v:
                continue

            # process here
            print("==========")
            print(path)
            prev = path[len(path) - 2]
            operation = get_operation_between(w,prev, operations)
            edge = get_edge(w, prev)
            print(edge)
            print(operation)
            print("==========")



# Create a new graph
G = nx.Graph()

# Nodes were provided as instances of Node class; we will just use coordinates directly
nodes = [
    (3,2), (4, 2), (5, 2), (6, 2), (7,2), (8,2), (9,2), (10,2), (11,2), (12,2),
    (5,3), (12,3), (5, 4), (8, 4), (12, 4), (8, 5), (12, 5),
    (2, 6), (3, 6), (8,6), (9,6), (10,6), (11,6), (12,6),
    (3,7), (4,7), (5,7), (6,7), (7,7), (8,7), (10,7),
    (3,8), (9,8), (10,8), (11,8), (12,8)
]

# Add nodes to the graph
for node in nodes:
    G.add_node(node)

# Define edges with node coordinates directly
edges = [
    ((3,2), (4,2)), ((4,2), (5,2)), ((5,2), (6,2)), ((5,3), (5,2)),
    ((5,4), (5,3)), ((6,2), (7,2)), ((7,2), (8,2)), ((8,2), (9,2)),
    ((9,2), (10,2)), ((10,2), (11,2)), ((11,2), (12,2)), ((12,3), (12,2)),
    ((12,4), (12,3)), ((12,5), (12,4)), ((12,6), (12,5)), ((11,6), (12,6)),
    ((10,6), (11,6)), ((10,7), (10,6)), ((10,8), (10,7)), ((9,8), (10,8)),
    ((10,8), (11,8)), ((11,8), (12,8)), ((9,6), (10,6)), ((8,6), (9,6)),
    ((8,6), (8,5)), ((8,5), (8,4)), ((8,7), (8,6)), ((7,7), (8,7)),
    ((6,7), (7,7)), ((5,7), (6,7)), ((4,7), (5,7)), ((3,7), (4,7)),
    ((3,8), (3,7)), ((3,7), (3,6)), ((2,6), (3,6))
]

operations = {
    ((1,6), (2,6)) : ("expansion", [((3,8), (3,7))]),
    ((3,8), (3,7)): ( "expansion", [((1,6), (2,6))]),
    ((7,7), (8,7)): ( "expansion", []),
    ((8,6), (8,5)): ( "expansion", [((9,6), (10,6)), ((12,5),(12,4))]),
    ((9,6),(10,6)): ( "contraction", [((8,6), (8,5)), ((12,5),(12,4))]),
    ((10,8), (10,7)): ( "contraction", []),
    ((11,8),(12,8)): ( "expansion", []),
    ((12,5),(12,4)): ( "expansion", [((8,6),(8,5)),((9,6),(10,6))]),
    ((12,3),(12,2)): ("contraction",[]),
    ((10,2),(11,2)): ("expansion",[((6,2),(7,2)), ((5,4),(5,3))]),
    ((8,2),(9,2)): ("contraction",[]),
    ((6,2),(7,2)): ("expansion", [((10,2),(11,2)), ((5,4),(5,3))]),
    ((5,4),(5,3)): ( "expansion", [((10,2),(11,2)), ((6,2),(7,2))])
}

# Add edges to the graph
for edge in edges:
    start = edge[0]
    end = edge[1]
    G.add_edge(start, end)


# Draw the graph
pos = {node: (node[0], node[1]) for node in G.nodes()}
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=800)

plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)  # Show ticks
plt.show()

start = (4,7)

traverse_from_node(G, start, operations, list())


#
# for node in G.nodes:
#     print("=== From node: " + str(node) + " ===")
#     traverse_from_node(G,node, None)
#     print("===============================")
