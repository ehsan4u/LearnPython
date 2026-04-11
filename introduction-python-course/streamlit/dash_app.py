# pip install dash pandas plotly dash-bootstrap-components

import base64
import io
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df_global = pd.DataFrame()

# ---------- Layout ----------
app.layout = dbc.Container([
    html.H2("Data & Visualization Dashboard"),

    dcc.Tabs([

        # ======================
        # TAB 1 — DATA
        # ======================
        dcc.Tab(label="Data", children=[
            html.Br(),
            dcc.Upload(
                id='upload-data',
                children=html.Div(['Drag & Drop or ', html.A('Select CSV File')]),
                style={
                    'width': '100%', 'height': '60px',
                    'lineHeight': '60px', 'borderWidth': '1px',
                    'borderStyle': 'dashed', 'borderRadius': '5px',
                    'textAlign': 'center'
                },
                multiple=False
            ),
            html.Br(),
            html.Div(id='data-preview')
        ]),

        # ======================
        # TAB 2 — VISUALIZATION
        # ======================
        dcc.Tab(label="Visualization", children=[
            html.Br(),

            dbc.Row([
                # LEFT PANEL (Fields)
                dbc.Col([
                    html.H5("Chart Builder"),

                    html.Label("Chart Type"),
                    dcc.Dropdown(
                        id='chart-type',
                        options=[
                            'scatter', 'line', 'bar', 'histogram', 'box'
                        ],
                        value='scatter'
                    ),

                    html.Br(),
                    html.Label("X Axis"),
                    dcc.Dropdown(id='x-axis'),

                    html.Br(),
                    html.Label("Y Axis"),
                    dcc.Dropdown(id='y-axis'),

                    html.Br(),
                    html.Label("Color"),
                    dcc.Dropdown(id='color'),

                ], width=3),

                # RIGHT PANEL (Chart)
                dbc.Col([
                    dcc.Graph(id='graph')
                ], width=9)
            ])
        ])
    ])
], fluid=True)

# ---------- Upload callback ----------
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

@app.callback(
    Output('data-preview', 'children'),
    Output('x-axis', 'options'),
    Output('y-axis', 'options'),
    Output('color', 'options'),
    Input('upload-data', 'contents')
)
def update_data(contents):
    global df_global
    if contents is None:
        return "Upload a dataset to begin.", [], [], []

    df_global = parse_contents(contents)

    preview = html.Div([
        html.H5("Dataset Preview"),
        dbc.Table.from_dataframe(df_global.head(), striped=True, bordered=True)
    ])

    cols = [{'label': c, 'value': c} for c in df_global.columns]

    return preview, cols, cols, cols

# ---------- Chart callback ----------
@app.callback(
    Output('graph', 'figure'),
    Input('chart-type', 'value'),
    Input('x-axis', 'value'),
    Input('y-axis', 'value'),
    Input('color', 'value')
)
def update_chart(chart, x, y, color):
    if df_global.empty or x is None:
        return px.scatter(title="Upload data to start")

    if chart == 'scatter':
        fig = px.scatter(df_global, x=x, y=y, color=color)
    elif chart == 'line':
        fig = px.line(df_global, x=x, y=y, color=color)
    elif chart == 'bar':
        fig = px.bar(df_global, x=x, y=y, color=color)
    elif chart == 'histogram':
        fig = px.histogram(df_global, x=x, color=color)
    elif chart == 'box':
        fig = px.box(df_global, x=x, y=y, color=color)

    return fig

if __name__ == '__main__':
    app.run(debug=True)