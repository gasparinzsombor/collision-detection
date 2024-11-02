from dash import Dash
from layouts import main_layout

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = main_layout.get_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
