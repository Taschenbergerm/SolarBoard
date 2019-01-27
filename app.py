import os
import pathlib as pl
import pandas as pd
import flask
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
VALID_USERNAME_PASSWORD_PAIRS = [
    ("data-solutions", "awesome"),
    ("complex", "marvelous")
]

static_image_route = 'static/'
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,server=server)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.config.suppress_callback_exceptions = True

def indicator(color, text, id_value):
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                children="INIT",
                id=id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        style={"background-color": color}
    )

def indicator_graph(color, text, id_value):
    return html.Div([
        html.P(
            text,
            className="twelve columns indicator_text"
        ),
        dcc.Graph(
            id=id_value,
            style={"height": "100%", "width": "98%"},
            config=dict(displayModeBar=False)
        )
    ],
        className="four columns indicator",
        style={"background-color": color}
    )
def report_table(table: pd.DataFrame, subset: list, mark: str ):
    df = table[subset]
    cols = df.drop(mark, axis=1).columns
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in cols])] +

        # Body
        [
            html.Tr(
                [
                    html.Td(df.iloc[i][col])
                    for col in cols
                ] + [html.Td(df.iloc[i][mark], className=f"marked {df.iloc[i][mark]}")]
            )
            for i in range(len(df))
        ],
        style={"background-color": "#ffffff", "margin-top": "5%"}
    )

def dash_tabel(data, subset):
    df = data[subset]
    return dt.DataTable(
        data=df.to_dict('rows'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        n_fixed_rows=1,
        style_as_list_view=False,
        style_cell={'textAlign': 'left'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'status',
                    'filter': 'status eq "finished"'
                },
                'backgroundColor': '#2a9c3c',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': 'status',
                    'filter': 'status eq "failed"'
                },
                'backgroundColor': '#f70007',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': 'status',
                    'filter': 'status eq "running"'
                },
                'backgroundColor': '#0071ff',
                'color': 'white',
            },
            {
                'if': {
                    'column_id': 'status',
                    'filter': 'status eq "waiting"'
                },
                'backgroundColor': '#c0c0c0',
                'color': 'white',
            },
        ]
    )

def color_state(state):
    return {"color":"#2a9c3c"}