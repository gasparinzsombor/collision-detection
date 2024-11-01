import networkx as nx
import plotly.graph_objects as go

operations = {
    ((1, 6), (2, 6)): ("expansion", [((3, 8), (3, 7))]),
    ((3, 8), (3, 7)): ("expansion", [((1, 6), (2, 6))]),
    ((7, 7), (8, 7)): ("expansion", []),
    ((8, 6), (8, 5)): ("expansion", [((9, 6), (10, 6)), ((12, 5), (12, 4))]),
    ((9, 6), (10, 6)): ("contraction", [((8, 6), (8, 5)), ((12, 5), (12, 4))]),
    ((10, 8), (10, 7)): ("contraction", []),
    ((11, 8), (12, 8)): ("expansion", []),
    ((12, 5), (12, 4)): ("expansion", [((8, 6), (8, 5)), ((9, 6), (10, 6))]),
    ((12, 3), (12, 2)): ("contraction", []),
    ((10, 2), (11, 2)): ("expansion", [((6, 2), (7, 2)), ((5, 4), (5, 3))]),
    ((8, 2), (9, 2)): ("contraction", []),
    ((6, 2), (7, 2)): ("expansion", [((10, 2), (11, 2)), ((5, 4), (5, 3))]),
    ((5, 4), (5, 3)): ("expansion", [((10, 2), (11, 2)), ((6, 2), (7, 2))])
}


def create_network():
    G = nx.DiGraph()

    positions = {
        'a1': (1, 0), 'a2': (7, 0), 'a3': (8, 0), 'a4': (9, 0), 'a5': (10, 0),
        'b1': (1, 1), 'v': (2, 1), 'b3': (3, 1), 'b4': (4, 1), 'b5': (5, 1), 'b6': (6, 1), 'b7': (8, 1),
        'c1': (0, 2), 'c2': (1, 2), 'c3': (6, 2), 'c4': (7, 2), 'c5': (8, 2), 'c6': (9, 2), 'c7': (10, 2),
        'd1': (6, 3), 'd2': (10, 3),
        'w': (3, 4), 'e2': (6, 4), 'e3': (10, 4),
        'f1': (3, 5), 'f2': (10, 5),
        'g1': (1, 6), 'g2': (2, 6), 'g3': (3, 6), 'g4': (4, 6), 'g5': (5, 6), 'g6': (6, 6), 'g7': (7, 6), 'g8': (8, 6),
        'g9': (9, 6), 'g10': (10, 6)
    }


    G.add_nodes_from(positions.keys())
    G.add_edges_from([
        ('a2', 'a3'), ('a3', 'a4'), ('a4', 'a5'),
        ('b1', 'v'), ('v', 'b3'), ('b3', 'b4'), ('b4', 'b5'), ('b5', 'b6'),
        ('c1', 'c2'), ('c3', 'c4'), ('c4', 'c5'), ('c5', 'c6'), ('c6', 'c7'),
        ('g1', 'g2'), ('g2', 'g3'), ('g3', 'g4'), ('g4', 'g5'), ('g5', 'g6'), ('g6', 'g7'), ('g7', 'g8'), ('g8', 'g9'), ('g9', 'g10'),

     ('a1', 'b1'),('a3', 'b7'), ('b1', 'c2'), ('b6', 'c3'), ('b7', 'c5'),
    ('c3', 'd1'), ('d2', 'c7'), ('e2', 'd1'),
                          ('f1', 'g3'), ('f2', 'g10'), ('w', 'f1'),
                          ('d2', 'e3'), ('e3', 'f2'),

    ]
  )
    return G, positions


def generate_trace(G, positions, highlighted_nodes=None):
    if highlighted_nodes is None:
        highlighted_nodes = []

    x, y = [], []
    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        x.extend([x0, x1, None])
        y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=x,
        y=y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = [positions[node][0] for node in G]
    node_y = [positions[node][1] for node in G]
    node_colors = ['red' if node in highlighted_nodes else 'lightgreen' for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_colors,
            size=40,
            line_width=2,
            symbol='square'
        ),
        text=[node for node in G])

    return edge_trace, node_trace


def simulate_step(parsed_data):
    pass

def parse_simulation_data(d):
    pass

