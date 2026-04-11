#pip install dash pandas plotly dash-bootstrap-components sqlalchemy openai

import base64, io, json
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, ALL
import plotly.express as px
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine

# ==============================
# APP SETUP
# ==============================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
df_global = pd.DataFrame()
charts = []

# ==============================
# HELPERS
# ==============================
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

def get_fig(chart, df, x, y, color):
    if chart == 'scatter':
        return px.scatter(df, x=x, y=y, color=color)
    if chart == 'line':
        return px.line(df, x=x, y=y, color=color)
    if chart == 'bar':
        return px.bar(df, x=x, y=y, color=color)
    if chart == 'histogram':
        return px.histogram(df, x=x, color=color)
    if chart == 'box':
        return px.box(df, x=x, y=y, color=color)

# ==============================
# LAYOUT
# ==============================
app.layout = dbc.Container([
    html.H2("AI BI Dashboard Builder"),

    dcc.Tabs([

    # ================= DATA TAB =================
    dcc.Tab(label="Data", children=[
        html.Br(),

        dcc.Upload(
            id='upload-data',
            children=html.Div(['Upload CSV']),
            style={'border':'1px dashed','padding':'20px'}
        ),

        html.Br(),

        dbc.Input(id="sql-string",
                  placeholder="Or connect SQL: sqlite:///mydb.db"),
        html.Button("Connect DB", id="connect-db"),

        html.Br(), html.Br(),
        html.Div(id='data-preview')
    ]),

    # ================= DASHBOARD TAB =================
    dcc.Tab(label="Dashboard", children=[

        dbc.Row([
        # -------- LEFT PANEL --------
        dbc.Col([
            html.H4("Filters"),
            dcc.Dropdown(id="filter-column"),
            dcc.Dropdown(id="filter-value", multi=True),

            html.Hr(),
            html.H4("New Chart"),

            dcc.Dropdown(['scatter','line','bar','histogram','box'],
                         'scatter', id='chart-type'),

            dcc.Dropdown(id='x-axis', placeholder="X axis"),
            dcc.Dropdown(id='y-axis', placeholder="Y axis"),
            dcc.Dropdown(id='color', placeholder="Color"),

            html.Br(),
            html.Button("Add Chart", id="add-chart"),
            html.Br(), html.Br(),

            html.Button("Save Dashboard", id="save"),
            html.Div(id="save-msg"),

            html.Hr(),
            html.H4("AI Insights"),
            html.Button("Recommend Charts", id="ai-btn"),
            html.Div(id="ai-output")

        ], width=3),

        # -------- RIGHT PANEL --------
        dbc.Col([
            html.Div(id="charts-container")
        ], width=9)

        ])
    ])
])
], fluid=True)

# ==============================
# LOAD DATA (CSV)
# ==============================
@app.callback(
    Output('data-preview','children'),
    Output('x-axis','options'),
    Output('y-axis','options'),
    Output('color','options'),
    Output('filter-column','options'),
    Input('upload-data','contents')
)
def load_csv(contents):
    global df_global
    if contents is None:
        return "Upload data", [],[],[],[]

    df_global = parse_contents(contents)
    cols = [{'label':c,'value':c} for c in df_global.columns]

    return dbc.Table.from_dataframe(df_global.head()), cols, cols, cols, cols

# ==============================
# LOAD SQL DATA
# ==============================
@app.callback(
    Output('data-preview','children', allow_duplicate=True),
    Input('connect-db','n_clicks'),
    State('sql-string','value'),
    prevent_initial_call=True
)
def connect_db(n, conn):
    global df_global
    engine = create_engine(conn)
    df_global = pd.read_sql("SELECT * FROM data", engine)
    return dbc.Table.from_dataframe(df_global.head())

# ==============================
# FILTER VALUES
# ==============================
@app.callback(
    Output('filter-value','options'),
    Input('filter-column','value')
)
def update_filter_values(col):
    if col is None or df_global.empty:
        return []
    return [{'label':v,'value':v} for v in df_global[col].unique()]

# ==============================
# ADD MULTIPLE CHARTS
# ==============================
@app.callback(
    Output('charts-container','children'),
    Input('add-chart','n_clicks'),
    State('chart-type','value'),
    State('x-axis','value'),
    State('y-axis','value'),
    State('color','value'),
    State('filter-column','value'),
    State('filter-value','value')
)
def add_chart(n, chart, x, y, color, fcol, fval):
    if n is None or df_global.empty:
        return []

    df = df_global.copy()
    if fcol and fval:
        df = df[df[fcol].isin(fval)]

    fig = get_fig(chart, df, x, y, color)
    charts.append(fig)

    return [dcc.Graph(figure=c) for c in charts]

# ==============================
# SAVE DASHBOARD
# ==============================
@app.callback(
    Output("save-msg","children"),
    Input("save","n_clicks")
)
def save_dashboard(n):
    if n is None:
        return ""
    with open("dashboard.json","w") as f:
        json.dump({"charts":len(charts)}, f)
    return "Dashboard saved!"

# ==============================
# AI RECOMMENDATIONS
# ==============================
@app.callback(
    Output("ai-output","children"),
    Input("ai-btn","n_clicks")
)
def ai_recommend(n):
    if n is None or df_global.empty:
        return ""

    numeric = df_global.select_dtypes(include="number").columns.tolist()
    cat = df_global.select_dtypes(include="object").columns.tolist()

    return html.Div([
        html.P("Recommended charts:"),
        html.Ul([
            html.Li(f"Scatter: {numeric[:2]}"),
            html.Li(f"Bar: {cat[:1]} vs {numeric[:1]}"),
            html.Li(f"Histogram: {numeric[:1]}")
        ])
    ])

# ==============================
if __name__ == '__main__':
    app.run(debug=True)