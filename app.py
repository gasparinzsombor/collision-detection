from dash import Dash
import layouts.load_layout as load_layout

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = load_layout.create_layout(app)

if __name__ == '__main__':
    app.run_server(debug=True)
