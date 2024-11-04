from typing import Any
from webbrowser import Opera
from matplotlib.pyplot import scatter
import networkx as nx
from networkx import Graph
from networkx import neighbors
import plotly.graph_objects as go
import algorithm.utilities.utilities
from algorithm.utilities.utilities import parse_graph
from algorithm.Node import Node
from algorithm.algorithms import Edge, Operations, Operation, Coupling
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


def create_network() -> tuple[Graph, Any, Operations]:
    G, operations = parse_graph("examples/example-graph-1.txt")

    return G, list(map(lambda node: (node.x, node.y), G.nodes)), operations


def generate_trace(G: Graph, operations: Operations, collision_node: Node | None = None) -> tuple[list[go.Scatter], go.Scatter]:
    traces = []
    for edge in G.edges:
        x0, y0 = edge[0].as_tuple()
        x1, y1 = edge[1].as_tuple()
        color = 'black'
        width = 2
        operation = operations.get(edge) or operations.get((edge[1], edge[0]))
        if operation:
            operation_type = operation [0]
            if operation_type == 'expansion':
                color = 'red'
                width = 4
            elif operation_type == 'contraction':
                color = 'green'
                width = 4

        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=width, color=color),
            mode='lines',
            hoverinfo='none'
        )
        traces.append(edge_trace)

    node_x = [node.x for node in G.nodes]
    node_y = [node.y for node in G.nodes]
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='lightyellow',
            size=40,
            line=dict(width=2)
        ),
        text=[str(node) for node in G.nodes]
    )

    return traces, node_trace

def copy_graph(graph: nx.Graph) -> nx.Graph:
    """Creates a copy of the graph."""
    return graph.copy()

def transfer_neighbors(graph: nx.Graph, keep_node: Node, remove_node: Node):
    """Transfers all neighbors of remove_node to keep_node, avoiding self-loops."""
    for neighbor in list(graph.neighbors(remove_node)):
        if neighbor != keep_node:  # Avoid self-loop
            graph.add_edge(keep_node, neighbor)
    
def identify_side_nodes(graph: nx.Graph, keep_node: Node, remove_node: Node) -> list[Node]:
    """Identifies nodes on the side of the remove_node based on shortest path distance."""
    nodes_to_move = []
    for node in graph.nodes:
        if node != remove_node:
            # Calculate shortest path distance to keep_node and remove_node
            try:
                dist_to_remove = nx.shortest_path_length(graph, source=node, target=remove_node)
                dist_to_keep = nx.shortest_path_length(graph, source=node, target=keep_node)
                
                # Check if node is closer to remove_node than to keep_node
                if dist_to_remove <= dist_to_keep:
                    nodes_to_move.append(node)
            except nx.NetworkXNoPath:
                # If there's no path between nodes, ignore this node
                continue
    
    return nodes_to_move

def move_nodes(g: Graph, nodes_to_move: list, move_x: int, move_y: int) -> Graph:
    print(f"Nodes to move: {nodes_to_move}")
    new_graph = Graph()
    for node in nodes_to_move:
        new_node = Node(node.x + move_x, node.y + move_y)
        new_graph.add_node(new_node)


    remaining_nodes = set(g.nodes).difference(set(nodes_to_move))
    for node in remaining_nodes:
        if node not in new_graph:
            new_graph.add_node(node)

    for edge in g.edges:
        node1: Node = edge[0]
        node2: Node = edge[1]

        if node1 in nodes_to_move:
            node1 = Node(node1.x + move_x, node1.y + move_y)

        if node2 in nodes_to_move:
            node2 = Node(node2.x + move_x, node2.y + move_y)
        new_graph.add_edge(node1, node2)

    return new_graph

def apply_coupling_on_graph(graph: nx.Graph, coupling: Coupling, couplings: list[Coupling], collisison_node: Node) -> tuple[nx.Graph, list[Coupling], Node]:
    # for operation in coupling:
    print(f"Original couling: {coupling}")
    for i in range(len(coupling)):
        graph, coupling, couplings, collisison_node = apply_operation_on_graph(graph, coupling[i], coupling, couplings, collisison_node)
        print(f"Modified coupling: {coupling}")

    return (graph, couplings, collisison_node)

def apply_operation_on_graph(graph: nx.Graph, operation: Operation, coupling: Coupling, couplings: list[Coupling], collision_node: Node) -> tuple[nx.Graph, Coupling, list[Coupling], Node]:
    """Applies the given operation (e.g., contraction) on the graph copy."""
    # Unpack the operation details
    (node1, node2), op_type = operation
    
    # Copy the graph
    graph_copy = copy_graph(graph)
    
    if op_type == 'contraction':
        # Ensure both nodes are in the graph
        if node1 in graph_copy and node2 in graph_copy:
            # Decide which node to keep and which to remove
            keep_node, remove_node = node1, node2
            
            # Transfer neighbors from remove_node to keep_node
            transfer_neighbors(graph_copy, keep_node, remove_node)
            
            # Identify the nodes on the side of the removed node
            nodes_to_move = identify_side_nodes(graph_copy, keep_node, remove_node)

            # Remove the contracted node
            graph_copy.remove_node(remove_node)
            
            # Calculate movement vector
            move_x = keep_node.x - remove_node.x
            move_y = keep_node.y - remove_node.y
            
            # Move identified nodes
            graph_copy = move_nodes(graph_copy, nodes_to_move, move_x, move_y)

    elif op_type == 'expansion':
        # Ensure both nodes are in the graph
        if node1 in graph_copy and node2 in graph_copy:
            # Identify nodes to move on one side of node1 and node2
            nodes_to_move = identify_side_nodes(graph_copy, node1, node2)
            nodes_to_move.append(node2)
            print(f"Nodes to move: {nodes_to_move}")
            
            move_x = node2.x - node1.x
            move_y = node2.y - node1.y
            
            # # Move identified nodes to clear space for the new node
            graph_copy = move_nodes(graph_copy, nodes_to_move, move_x, move_y)
        
            new_node = node2
            moved_node = Node(node2.x + move_x, node2.y + move_y)
            graph_copy.remove_edge(node1, moved_node)
            graph_copy.add_node(new_node)
            graph_copy.add_edge(node1, new_node)
            graph_copy.add_edge(new_node, moved_node)

    coupling = transform_coupling(coupling, nodes_to_move, move_x, move_y)
    couplings = [transform_coupling(coup, nodes_to_move, move_x, move_y) for coup in couplings]

    if collision_node in nodes_to_move:
        collision_node = Node(collision_node.x + move_x, collision_node.y + move_y)
    
    return (graph_copy, coupling, couplings, collision_node)

def transform_coupling(coupling: Coupling, moved_nodes: list[Node], move_x: int, move_y: int) -> Coupling:
    print(f"movings: x: {move_x}, y: {move_y}")
    return [transform_operation(operation, moved_nodes, move_x, move_y) for operation in coupling]

def transform_operation(operation: Operation, moved_nodes: list[Node], move_x: int, move_y: int) -> Operation:
    ((node1, node2), op_type) = operation
    node1 = Node(node1.x + move_x, node1.y + move_y) if node1 in moved_nodes else node1
    node2 = Node(node2.x + move_x, node2.y + move_y) if node2 in moved_nodes else node2
    return ((node1, node2), op_type)

def parse_simulation_data(d):
    pass

