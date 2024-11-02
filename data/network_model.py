import networkx as nx
import plotly.graph_objects as go
import algorithm.utilities.utilities
from algorithm.utilities.utilities import parse_graph

def create_network():
    G, operations = parse_graph("examples/example-graph-2.txt")

    return G, list(map(lambda node: (node.x, node.y), G.nodes)), operations


def generate_trace(G, operations):
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

def simulate_step(parsed_data):
    pass

def parse_simulation_data(d):
    pass

