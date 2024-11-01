from dash import html, dcc, callback
from data.network_model import create_network, generate_trace, simulate_step
from plotly import graph_objects as go
from dash import Dash, Input, Output, State, no_update, callback
from dash.exceptions import PreventUpdate
import algorithm.algorithms as a

def get_layout():
    g, pos, operations = create_network()
    edge_trace, node_trace = generate_trace(g)

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis_scaleanchor="y", yaxis_scaleratio=1
    )

    layout = html.Div([
        html.Div([
            html.H1('Collision Detection Algorithm Visualization'),
            html.P('Interactive demonstration with node grid and vector handling'),
        ], className='header'),

        html.Div([
            html.Div([
                dcc.Graph(id='graph', figure=fig, style={
                'height': '70vh',
                'transform': 'rotate(0deg)',  # Rotate 90 degrees counterclockwise
                'transform-origin': 'center center'  # Ensures the rotation is around the center
            }),
                html.Div(id='vector-display', className='vector-display', children='Vectors will be displayed here.'),
            ], className='visualization-area'),

            html.Div([

                html.H2('Simulation Controls'),
                html.Button('Start Simulation', id='start-simulation-btn', className='action-button'),
                html.Button('Pause Simulation', id='pause-simulation-btn', className='action-button'),
                dcc.Slider(0, 100, 5, value=50, id='speed-slider',
                    marks={i: str(i) for i in range(0, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    className='slider'
                )
            ], className='control-panel'),

            html.Div([
                html.H2('Algorithm Status'),
                html.Div(id='status-output', className='status-output', children='Simulation not started.'),
                html.H2('Performance Metrics'),
                html.Div(id='performance-metrics', className='performance-metrics', children='Metrics will be displayed here.'),
                html.H2('Detailed Log'),
                html.Div(id='detailed-log', className='detailed-log', children='Log will be updated here.'),
            ], className='information-panel')
        ], className='content-row'),
    ], className='main-container')

    return layout, pos


@callback(
    Output('graph', 'figure'),
    Input('start-simulation-btn', 'n_clicks'),
    prevent_initial_call=True
)
def update_simulation(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    g, pos, operations = create_network()
    edge_trace, node_trace = generate_trace(g, pos)

    result = a.do(g, operations)

    print(result)

    #node_trace.marker.color = ['red' if node in ['v', 'w'] else 'green' for node in g.nodes]
    #node_trace.marker.size = [40 if node in ['v', 'w'] else 40 for node in g.nodes]

    fig = go.Figure(data=[edge_trace, node_trace])
    # fig.update_layout(
    #     showlegend=False,
    #     hovermode='closest',
    #     margin=dict(b=0, l=0, r=0, t=0),
    #     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #     xaxis_scaleanchor="y", yaxis_scaleratio=1
    # )
    return fig