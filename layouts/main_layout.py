from dash import html, dcc
from data.network_model import create_network, generate_trace
from plotly import graph_objects as go

def get_layout():
    # Create network and position data
    g, pos = create_network()
    edge_trace, node_trace = generate_trace(g, pos)

    # Create the main graph for visualizing the node grid
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        xaxis_scaleanchor="y", yaxis_scaleratio=1
    )

    # Layout construction with enhanced CSS styles
    layout = html.Div([
        # Header
        html.Div([
            html.H1('Collision Detection Algorithm Visualization'),
            html.P('Interactive demonstration with node grid and vector handling'),
        ], className='header'),

        # Content Row
        html.Div([
            # Visualization Area: Central Graph for displaying the node grid and vectors
            html.Div([
                dcc.Graph(id='graph', figure=fig, style={'height': '70vh'}),
                html.Div(id='vector-display', className='vector-display', children='Vectors will be displayed here.'),
            ], className='visualization-area'),

            # Control Panel (Left Sidebar)
            html.Div([
                html.H2('Algorithm Parameters'),
                dcc.Input(id='node-id-input', type='number', placeholder='Enter node ID', min=0, max=len(g.nodes)-1, className='input-field'),
                dcc.Dropdown(
                    id='coupling-type',
                    options=[
                        {'label': 'Constant Size', 'value': 'constant'},
                        {'label': 'Horizontal Only', 'value': 'horizontal'},
                        {'label': 'Vertical Only', 'value': 'vertical'}
                    ],
                    placeholder='Select Coupling Type',
                    className='dropdown'
                ),
                html.Button('Generate Nodes and Vectors', id='generate-nodes-btn', className='action-button'),
                html.Div(id='output-container', className='output-container', children='Configure parameters and click "Generate".'),

                html.H2('Simulation Controls'),
                html.Button('Start Simulation', id='start-simulation-btn', className='action-button'),
                html.Button('Pause Simulation', id='pause-simulation-btn', className='action-button'),
                dcc.Slider(0, 100, 5, value=50, id='speed-slider',
                    marks={i: str(i) for i in range(0, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    className='slider'
                )
            ], className='control-panel'),

            # Information Panel (Right Sidebar)
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

