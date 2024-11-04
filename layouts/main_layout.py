from dash import html, dcc, callback, dash_table, Output, Input, State
import dash
from data.network_model import apply_coupling_on_graph, create_network, generate_trace
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
        dcc.Store(id='simulation-steps', data=[]),
        dcc.Store(id='current-step', data=0),
        dcc.Interval(id='simulation-interval', interval=5000, n_intervals=0, disabled=True), # 1 second interval
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
    [Output('log-table', 'data'), Output('graph', 'figure', allow_duplicate=True), Output('simulation-steps', 'data')],
    Input('start-algo-btn', 'n_clicks'),
    prevent_initial_call=True
)

def update_log_and_graph(n_clicks):
    g, pos, operations = create_network()
    res = a.do(g, operations)  # `res` contains the collision simulation results
    print(f"res: {res}")
    edge_trace, node_trace = generate_trace(g, operations)
    
    simulation_steps = []
    if len(res) > 0:
        # Generate intermediate states
        collision_node, _, couplings = res[0]
        g_step = g
        print(f"Initial couplings: {couplings}")
        # for coupling in couplings:
        for i in range(len(couplings)):
            coupling = couplings[i]
            # Modify the graph based on the current step (contraction or expansion)
            g_step, couplings, collision_node = apply_coupling_on_graph(g_step, coupling, couplings, collision_node)
            # Apply operations to `g_step` for the current `step`
            # e.g., handle contraction by removing a node, etc.
            # Generate traces for each step and store them
            edge_trace_step, node_trace_step = generate_trace(g_step, {}, collision_node)
            simulation_steps.append({'edge_trace': edge_trace_step, 'node_trace': node_trace_step})
    
    # Prepare initial figure
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

