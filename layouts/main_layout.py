from dash import html, dcc, callback, dash_table, Output, Input, State
import dash
from data.network_model import apply_coupling_on_graph, create_network, generate_trace
from plotly import graph_objects as go
import algorithm.algorithms as a


def get_layout(app, filepath):
    # Store filepath in a dcc.Store for callback access
    layout = html.Div([
        dcc.Store(id='algo-started', data={'started': False}),
        dcc.Store(id='simulation-steps', data=[]),
        dcc.Store(id='current-step', data=0),
        dcc.Store(id='filepath', data=filepath),  # Store the filepath here
        dcc.Interval(id='simulation-interval', interval=5000, n_intervals=0, disabled=True),

        html.Div([
            html.H1('Collision Detection Algorithm Visualization'),
            html.P('Interactive demonstration with node grid'),
        ], className='header'),

        html.Div([
            dcc.Graph(id='graph', figure=generate_initial_figure(filepath)),
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
                style_cell={'height': 'auto', 'minWidth': '300px', 'width': '300px', 'maxWidth': '300px',
                            'whiteSpace': 'normal'}
            )
        ], className='control-panel'),
    ], className='main-container')

    return layout


def generate_initial_figure(filepath):
    # Generate initial figure based on filepath
    g, pos, operations = create_network(filepath)
    edge_trace, node_trace = generate_trace(g, operations)

    fig = go.Figure(data=[node_trace] + edge_trace, layout=dict(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis_scaleanchor="y", yaxis_scaleratio=1
    ))
    return fig


@callback(
    [Output('log-table', 'data'), Output('graph', 'figure', allow_duplicate=True), Output('simulation-steps', 'data')],
    Input('start-algo-btn', 'n_clicks'),
    State('filepath', 'data'),  # Retrieve the filepath here
    prevent_initial_call=True
)
def update_log_and_graph(n_clicks, filepath):
    g, pos, operations = create_network(filepath)
    res = a.do(g, operations)
    edge_trace, node_trace = generate_trace(g, operations)

    simulation_steps = []
    if len(res) > 0:
        collision_node, _, couplings = res[0]
        g_step = g
        for i in range(len(couplings)):
            coupling = couplings[i]
            g_step, couplings, collision_node = apply_coupling_on_graph(g_step, coupling, couplings, collision_node)
            collision_node2 = collision_node if i + 1 == len(couplings) else None
            edge_trace_step, node_trace_step = generate_trace(g_step, {}, collision_node2)
            simulation_steps.append({'edge_trace': edge_trace_step, 'node_trace': node_trace_step})

    fig = go.Figure(data=[node_trace] + edge_trace, layout=dict(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis_scaleanchor="y", yaxis_scaleratio=1
    ))

    data = [{
        'node1': f"N({op[0].x}, {op[0].y})",
        'node2': f"N({op[1].x}, {op[1].y})",
        'operations': '; '.join([', '.join([f"{action}" for action in sublist]) for sublist in op[2]])
    } for op in res]

    return data, fig, simulation_steps

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
    if data and data['started']:
        return html.Button('Start Simulation', id='start-sim-btn', className='action-button')
    return ""


@callback(
    Output('vector-display', 'children'),
    Input('start-sim-btn', 'n_clicks'),
    prevent_initial_call=True
)
def dummy_action(n_clicks):
    return ""


@callback(
    [Output('graph', 'figure'), Output('current-step', 'data')],
    [Input('simulation-interval', 'n_intervals')],
    [State('simulation-steps', 'data'), State('current-step', 'data')],
    prevent_initial_call=True
)
def run_simulation_step(n_intervals, simulation_steps, current_step):
    if current_step < len(simulation_steps):
        # Load the current step's traces
        step_data = simulation_steps[current_step]
        fig = go.Figure(data=[step_data['node_trace']] + step_data['edge_trace'], layout=dict(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            xaxis_scaleanchor="y", yaxis_scaleratio=1
        ))
        # Move to the next step
        return fig, current_step + 1
    else:
        # Stop the interval if we reach the end of steps
        return dash.no_update, current_step


@callback(
    Output('simulation-interval', 'disabled'),
    Input('start-sim-btn', 'n_clicks'),
    prevent_initial_call=True
)
def start_simulation(n_clicks):
    return False  # Enables the interval timer