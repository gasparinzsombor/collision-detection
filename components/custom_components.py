from data.network_model import create_network, generate_trace
import plotly.graph_objects as go

def create_custom_graph():
    g, pos = create_network()
    edge_trace, node_trace = generate_trace(g, pos)
    fig = go.Figure(data=[edge_trace, node_trace])
    return fig
