import networkx as nx
import matplotlib.pyplot as plt
import algorithms as a
import utilities
import time

from Node import Node
from Vector import Vector
from algorithm.utilities.utilities import parse_graph

Edge = tuple[Node, Node]
Operations = dict[
            Edge,
            tuple[str, list[Edge]]
        ]

# def main():
#     nodes = [Node(0,0), Node(1,0), Node(2,0)]
#     operations = [Vector(1,0), Vector(1,0)]
#     print(Node(2,0).possible_locations(operations, 3))
def main():
    # Create a new graph

    # Nodes were provided as instances of Node class; we will just use coordinates directly
    # nodes: list[Node] = [
    #     Node(3, 2), Node(4, 2), Node(5, 2), Node(6, 2), Node(7, 2), Node(8, 2), Node(9, 2), Node(10, 2), Node(11, 2), Node(12, 2),
    #     Node(5, 3), Node(12, 3), Node(5, 4), Node(8, 4), Node(12, 4), Node(8, 5), Node(12, 5),
    #     Node(2, 6), Node(3, 6), Node(8, 6), Node(9, 6), Node(10, 6), Node(11, 6), Node(12, 6),
    #     Node(3, 7), Node(4, 7), Node(5, 7), Node(6, 7), Node(7, 7), Node(8, 7), Node(10, 7),
    #     Node(3, 8), Node(9, 8), Node(10, 8), Node(11, 8), Node(12, 8)
    # ]

    # nodes: list[Node] = [
    #     Node(2, 2), Node(3, 2), Node(4, 2),
    #     Node(2, 3), Node(3, 3), Node(4, 3),
    #     Node(4, 4)
    # ]

    # Add nodes to the graph
    # for node in nodes:
    #     G.add_node(node)

    # Define edges with node coordinates directly
    # edges: list[Edge] = [
    #     (Node(3, 2), Node(4, 2)), (Node(4, 2), Node(5, 2)), (Node(5, 2), Node(6, 2)), (Node(5, 3), Node(5, 2)),
    #     (Node(5, 4), Node(5, 3)), (Node(6, 2), Node(7, 2)), (Node(7, 2), Node(8, 2)), (Node(8, 2), Node(9, 2)),
    #     (Node(9, 2), Node(10, 2)), (Node(10, 2), Node(11, 2)), (Node(11, 2), Node(12, 2)), (Node(12, 3), Node(12, 2)),
    #     (Node(12, 4), Node(12, 3)), (Node(12, 5), Node(12, 4)), (Node(12, 6), Node(12, 5)), (Node(11, 6), Node(12, 6)),
    #     (Node(10, 6), Node(11, 6)), (Node(10, 7), Node(10, 6)), (Node(10, 8), Node(10, 7)), (Node(9, 8), Node(10, 8)),
    #     (Node(10, 8), Node(11, 8)), (Node(11, 8), Node(12, 8)), (Node(9, 6), Node(10, 6)), (Node(8, 6), Node(9, 6)),
    #     (Node(8, 6), Node(8, 5)), (Node(8, 5), Node(8, 4)), (Node(8, 7), Node(8, 6)), (Node(7, 7), Node(8, 7)),
    #     (Node(6, 7), Node(7, 7)), (Node(5, 7), Node(6, 7)), (Node(4, 7), Node(5, 7)), (Node(3, 7), Node(4, 7)),
    #     (Node(3, 8), Node(3, 7)), (Node(3, 7), Node(3, 6)), (Node(2, 6), Node(3, 6))
    # ]

    # edges: list[Edge] = [
    #     (Node(2, 2), Node(3, 2)), (Node(3, 2), Node(4, 2)), (Node(3, 3), Node(4, 3)),
    #     (Node(2, 3), Node(2, 2)), (Node(4, 3), Node(4, 2)), (Node(4, 4), Node(4, 3))
    # ]

    # operations = {
    #     (Node(1, 6), Node(2, 6)): ("expansion", [(Node(3, 8), Node(3, 7))]),
    #     (Node(3, 8), Node(3, 7)): ("expansion", [(Node(1, 6), Node(2, 6))]),
    #     (Node(7, 7), Node(8, 7)): ("expansion", []),
    #     (Node(8, 6), Node(8, 5)): ("expansion", [(Node(9, 6), Node(10, 6)), (Node(12, 5), Node(12, 4))]),
    #     (Node(9, 6), Node(10, 6)): ("contraction", [(Node(8, 6), Node(8, 5)), (Node(12, 5), Node(12, 4))]),
    #     (Node(10, 8), Node(10, 7)): ("contraction", []),
    #     (Node(11, 8), Node(12, 8)): ("expansion", []),
    #     (Node(12, 5), Node(12, 4)): ("expansion", [(Node(8, 6), Node(8, 5)), (Node(9, 6), Node(10, 6))]),
    #     (Node(12, 3), Node(12, 2)): ("contraction", []),
    #     (Node(10, 2), Node(11, 2)): ("expansion", [(Node(6, 2), Node(7, 2)), (Node(5, 4), Node(5, 3))]),
    #     (Node(8, 2), Node(9, 2)): ("contraction", []),
    #     (Node(6, 2), Node(7, 2)): ("expansion", [(Node(10, 2), Node(11, 2)), (Node(5, 4), Node(5, 3))]),
    #     (Node(5, 4), Node(5, 3)): ("expansion", [(Node(10, 2), Node(11, 2)), (Node(6, 2), Node(7, 2))])
    # }

    # operations = {
    #     (Node(2, 2), Node(3, 2)): ("contraction", []),
    #     (Node(4 ,3), Node(4, 2)): ("expansion", [])
    # }

    # Add edges to the graph
    # for edge in edges:
    #     start = edge[0]
    #     end = edge[1]
    #
    #     if (start, end) in operations:
    #         G.add_edge(start, end, operation=operations[(start, end)][0], parallel_edges=operations[(start, end)][1])
    #     else:
    #         G.add_edge(start, end)

    # g, operations = parse_graph("../examples/example-graph-1.txt")
    # # Draw the graph
    # pos = {node: (node.x, node.y) for node in g.nodes()}
    # nx.draw(g, pos, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=800)
    #
    # plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    # plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)  # Show ticks
    # plt.show()

    #start = Node(4,7)
    #start = Node(8,7)
    #a.traverse_from_node(G, start, operations)

    #g, ops = parse_graph("../examples/example-graph-2.txt")

    folder = "../examples/data/generated_graphs/"
    filename = "graph_type3_size"
    sizes = ["5", "12", "20", "30", "40"]
    runtimes = {}
    for i in range(0, len(sizes)):
        g, ops = parse_graph(folder + filename + sizes[i] + ".txt")
        start_time = time.time()
        result = a.do(g, ops)
        elapsed_time = time.time() - start_time

        runtimes[sizes[i]] = elapsed_time

    times = [runtimes[size] for size in sizes]
    plt.plot(sizes, times, label=f"Graph Type: only horizontal")

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds)")
    plt.title("Algorithm Runtime by Graph Type")
    plt.legend()
    plt.savefig("../plot/algorithm_runtime_mixed.png")
    plt.close()


if __name__ == "__main__":
    main()