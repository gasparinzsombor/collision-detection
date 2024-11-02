from dash import html, dcc, callback, dash_table, Output, Input, State
from data.network_model import create_network, generate_trace
from plotly import graph_objects as go
import algorithm.algorithms as a

def get_layout():
    g, pos, operations = create_network()
    edge_trace, node_trace = generate_trace(g,operations)

    fig = go.Figure(data=[node_trace] + edge_trace , layout=dict(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis_scaleanchor="y", yaxis_scaleratio=1
    ))

    layout = html.Div([
        dcc.Store(id='algo-started', data={'started': False}),
        html.Div([
            html.H1('Collision Detection Algorithm Visualization'),
            html.P('Interactive demonstration with node grid'),
        ], className='header'),

        html.Div([
            dcc.Graph(id='graph', figure=fig),
            html.Div(id='vector-display', className='vector-display', children='Press the button!'),
        ], className='visualization-area'),

        html.Div([
            html.H2('Simulation Controls'),
            html.Button('Start Algorithm', id='start-algo-btn', className='action-button'),
            html.Div(id='sim-button-container'),
            html.H2('Detailed Log'),
            dash_table.DataTable(
                id='log-table',
                columns=[
                    {'name': 'Node 1', 'id': 'node1'},
                    {'name': 'Node 2', 'id': 'node2'},
                    {'name': 'Operations', 'id': 'operations'}
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_cell={'height': 'auto', 'minWidth': '300px', 'width': '300px', 'maxWidth': '300px', 'whiteSpace': 'normal'}
            )
        ], className='control-panel'),
    ], className='main-container')
    return layout


@callback(
    [Output('log-table', 'data'), Output('graph', 'figure')],
    Input('start-algo-btn', 'n_clicks'),
    prevent_initial_call=True
)

def update_log_and_graph(n_clicks):
    g, pos, operations = create_network()
    res = a.do(g, operations)
    edge_trace, node_trace = generate_trace(g, operations)
    print(res)
    data = [{
        'node1': f"N({op[0].x}, {op[0].y})",
        'node2': f"N({op[1].x}, {op[1].y})",
        'operations': '; '.join([', '.join([f"{action}" for action in sublist]) for sublist in op[2]])
    } for op in res]

    fig = go.Figure(data=[node_trace] + edge_trace, layout=dict(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis_scaleanchor="y", yaxis_scaleratio=1
    ))

    return data, fig

@callback(
    Output('algo-started', 'data'),
    Input('start-algo-btn', 'n_clicks'),
    prevent_initial_call=True
)
def set_algo_started(n_clicks):
    return {'started': True}

@callback(
    Output('sim-button-container', 'children'),
    Input('algo-started', 'data')
)
def display_sim_button(data):
    if data and data['started'] :
        return html.Button('Start Simulation', id='start-sim-btn', className='action-button')
    return ""

@callback(
    Output('vector-display', 'children'),
    Input('start-sim-btn', 'n_clicks'),
    prevent_initial_call=True
)
def dummy_action(n_clicks):
    return ""

