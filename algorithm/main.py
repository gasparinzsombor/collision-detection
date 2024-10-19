import networkx as nx
import matplotlib.pyplot as plt
import algorithms as a

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

    if (start, end) in operations:
        G.add_edge(start, end, operation=operations[(start,end)][0], parallel_edges=operations[(start,end)][1])
    else:
        G.add_edge(start, end)


# Draw the graph
pos = {node: (node[0], node[1]) for node in G.nodes()}
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=800)

plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)  # Show ticks
plt.show()

start = (4,7)

a.traverse_from_node(G, start, operations, list())


#
# for node in G.nodes:
#     print("=== From node: " + str(node) + " ===")
#     traverse_from_node(G,node, None)
#     print("===============================")
