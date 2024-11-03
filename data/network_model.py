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


def generate_trace(G: Graph, operations: Operations) -> tuple[list[go.Scatter], go.Scatter]:
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
                print(f"{node}: dist_to_remove: {dist_to_remove}, dist_to_keep: {dist_to_keep}")
                
                # Check if node is closer to remove_node than to keep_node
                if dist_to_remove <= dist_to_keep:
                    nodes_to_move.append(node)
            except nx.NetworkXNoPath:
                # If there's no path between nodes, ignore this node
                continue
    
    return nodes_to_move

def move_nodes(g: Graph, nodes: list, move_x: int, move_y: int):
    """Moves each node in the nodes list by (move_x, move_y)."""
    print(f"nodes: {nodes}, move_x: {move_x}, move_y: {move_y}")
    for node in nodes:
        move_node(g, node, move_x, move_y)
    
    print(f"Graph nodes: {g.nodes}")

def move_node(g: Graph, node: Node, move_x: int, move_y: int):
    new_node = Node(node.x + move_x, node.y + move_y)
    g.add_node(new_node)

    neighbors = list(g.neighbors(node))
    g.remove_node(node)

    print(f"neighbors for node {node}: {list(neighbors)}")
    for neighbor in neighbors:
        g.add_edge(new_node, neighbor)
    print(f"Neighbors of {new_node}: {list(g.neighbors(new_node))}")


def apply_coupling_on_graph(graph: nx.Graph, coupling: Coupling) -> nx.Graph:
    for operation in coupling:
        graph = apply_operation_on_graph(graph, operation)

    return graph

def apply_operation_on_graph(graph: nx.Graph, operation: Operation) -> nx.Graph:
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
            move_nodes(graph_copy, nodes_to_move, move_x, move_y)

    elif op_type == 'expansion':
        # Ensure both nodes are in the graph
        if node1 in graph_copy and node2 in graph_copy:
            # Calculate the position for the new node (midpoint between node1 and node2)
            new_x = (node1.x + node2.x) // 2
            new_y = (node1.y + node2.y) // 2
            new_node = Node(new_x, new_y)
            
            # Add the new node and connect it to node1 and node2
            graph_copy.add_node(new_node)
            graph_copy.add_edge(new_node, node1)
            graph_copy.add_edge(new_node, node2)
            
            # Identify nodes on the side of node1 (for example) to be moved by one
            nodes_to_move = identify_side_nodes(graph_copy, node1, new_node)
            
            # Determine movement direction (example: move nodes one unit in the x direction)
            move_x = 1 if node1.x < node2.x else -1
            move_y = 1 if node1.y < node2.y else -1
            
            # Move identified nodes
            move_nodes(graph_copy, nodes_to_move, move_x, move_y)
    
    nx.draw(graph_copy, with_labels=True)
    plt.savefig("graph.png")  # Save as an image
    
    return graph_copy

def parse_simulation_data(d):
    pass

