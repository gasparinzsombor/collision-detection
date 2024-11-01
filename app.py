from dash import Dash, Input, Output, State, no_update, callback
from dash.exceptions import PreventUpdate
from plotly import graph_objects as go
from layouts import main_layout
from data.network_model import create_network, generate_trace, simulate_step

app = Dash(__name__, suppress_callback_exceptions=True)

layout, pos = main_layout.get_layout()
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
