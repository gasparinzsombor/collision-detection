import networkx as nx
import plotly.graph_objects as go

def create_network():
    g = nx.Graph()
    pos = {  # Node positions
        0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0),
        5: (4, 1), 6: (4, 2), 7: (4, 3), 8: (4, 4),
        9: (3, 4), 10: (2, 4), 11: (1, 4), 12: (0, 4),
        13: (0, 3), 14: (0, 2), 15: (0, 1),

        # Inner connections
        16: (1, 1), 17: (2, 1), 18: (3, 1),
        19: (1, 3), 20: (2, 3), 21: (3, 3),
        22: (2, 2)
    }
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
    (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 0),
    (1, 16), (16, 17), (17, 18), (18, 3),
    (13, 19), (19, 20), (20, 21), (21, 9),
    (17, 22), (22, 20)]
    g.add_edges_from(edges)

    return g, pos

def generate_trace(g, pos):
    edge_x, edge_y, node_x, node_y = [], [], [], []
    for edge in g.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    for node in g.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='#888'), hoverinfo='none', mode='lines')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=[f"u_{i}" for i in g.nodes()], textposition="top center",
                            marker=dict(showscale=False, color='lightblue', size=30, line_width=2))
    return edge_trace, node_trace

