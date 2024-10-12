from threading import Timer
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import networkx as nx

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a NetworkX graph
G = nx.Graph()

# Define positions of the nodes manually to create a similar layout as in the image
pos = {
    # Nodes for the outer rectangle
    0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0),
    5: (4, 1), 6: (4, 2), 7: (4, 3), 8: (4, 4),
    9: (3, 4), 10: (2, 4), 11: (1, 4), 12: (0, 4),
    13: (0, 3), 14: (0, 2), 15: (0, 1),

    # Inner connections
    16: (1, 1), 17: (2, 1), 18: (3, 1),
    19: (1, 3), 20: (2, 3), 21: (3, 3),
    22: (2, 2)
}

# Add edges to create a rectangular grid
edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
    (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 0),
    (1, 16), (16, 17), (17, 18), (18, 3),
    (13, 19), (19, 20), (20, 21), (21, 9),
    (17, 22), (22, 20)
]

G.add_edges_from(edges)

# Create Plotly figure
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[f"u_{i}" if i == 22 else "" for i in G.nodes()],
    textposition="top center",
    marker=dict(
        showscale=False,
        color='lightblue',
        size=30,
        line_width=2
    )
)

# Set layout for Plotly figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=0),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                ))

# Set graph to fixed aspect ratio
fig.update_layout(
    xaxis=dict(scaleanchor="y", scaleratio=1),
    yaxis=dict(scaleanchor="x", scaleratio=1)
)

# Dash layout
app.layout = html.Div([
    dcc.Graph(
        id='graph',
        figure=fig
    )
])

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

# Run the Dash app
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)
