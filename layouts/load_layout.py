# app.py
from dash import html, dcc, Output, Input, State, callback
import base64
import os

from layouts import main_layout

def create_layout(app):
    layout = html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-file-upload'),
        html.Button('Load Simulation', id='load-button', n_clicks=0, className='action-button'),
        html.Div(id='main-container')
    ], className='main-container')

    @app.callback(
        Output('output-file-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def save_uploaded_file(contents, filename):
        if contents:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            upload_directory = 'uploads'
            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)
            filepath = os.path.join(upload_directory, filename)
            with open(filepath, 'wb') as f:
                f.write(decoded)
            return f"File saved to: {filepath}"
        return "No file uploaded."

    @app.callback(
        Output('main-container', 'children'),
        Input('load-button', 'n_clicks'),
        State('output-file-upload', 'children')
    )
    def load_simulation_setup(n_clicks, file_details):
        if n_clicks > 0 and file_details:
            filepath = file_details.split(': ')[1]
            return main_layout.get_layout(app, filepath)
        return html.Div("Please upload a file and click 'Load Simulation'.")

    return layout
