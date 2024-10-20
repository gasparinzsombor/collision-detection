from dash import Dash, Input, Output, State, no_update
from plotly import graph_objects as go
from layouts import main_layout

app = Dash(__name__, suppress_callback_exceptions=True)

layout, pos = main_layout.get_layout()
app.layout = layout

@app.callback(
    Output('graph', 'figure'),
    Input('add-node-btn', 'n_clicks'),
    State('node-id-input', 'value'),
    State('graph', 'figure')
)
def update_graph(n_clicks, node_id, existing_figure):
    if n_clicks and node_id is not None:
        fig = go.Figure(existing_figure)
        if node_id in pos:
            fig.add_trace(go.Scatter(
                x=[pos[node_id][0]],
                y=[pos[node_id][1]],
                mode='markers+text',
                text=f"u_{node_id}",
                textposition="top center",
                marker=dict(color='red', size=10, line=dict(color='DarkSlateGrey', width=2))
            ))
        return fig
    return no_update

if __name__ == '__main__':
    app.run_server(debug=True)
