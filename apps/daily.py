import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd

import plotly.plotly as py
from plotly import graph_objs as go
from solarboard import get_queue

from app import app, indicator,  indicator_graph, report_table, dash_tabel, color_state

white = i1 = i2 = i3 = "#ffffff"

layout = html.Div([html.Div(
        [
            indicator(
                i1,
                "Status of today's Master",
                "master-state",
            ),
            indicator(
                i2,
                "Waiting / Failed / Total",
                "feeds",
            ),
            indicator_graph(
                i3,
                "Failed Requests",
                "failed-feeds",
            ),
        ],
        className="row"
    ),
          html.Div(className="row", children=[
              html.Div(className="eigth columns table", id="queue"),
              html.Div(className="four columns summary",
                       children=html.Button(id='masterbutton', n_clicks=0, children='Submit')
                       ),
              html.Div(id="out-sub")
          ]),
            html.Div(id="daily_df", style={"display": "none"}),
            html.Div(id="daily_header", style={"display": "none"}),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000,  # in milliseconds
            n_intervals=0
    )
]
)

@app.callback(Output('daily_df', 'children'),
              [Input("interval-component", "n_intervals")])
def update_hidden_table(n_intervals):
    df = get_queue()
    return df.to_json(orient="split")

@app.callback(Output("queue", "children"),
              [Input("daily_df", "children")])
def update_visble_table(daily_df):
    df = pd.read_json(daily_df, orient="split")
    return dash_tabel(df.sort_values("status_code", ascending=False), "id feed_id status".split())

@app.callback(Output("daily_header", "children"),
              [Input("daily_df", "children")])
def update_headerstates(daily_df):
    df = pd.read_json(daily_df, orient="split")
    state = df.query("feed_id == 0 ").status.values[0].capitalize()
    waiting = df.query("status == 'waiting'").shape[0]
    failed = df.query("status == 'failed'").shape[0]
    total = df.shape[0]

    return f"{state},{waiting}/{failed}/{total}"


@app.callback(Output("master-state", "children"),
              [Input("daily_header", "children")])
def update_master_state(header_values):
    return header_values.split(",")[0]


@app.callback(Output("feeds", "children"),
              [Input("daily_header", "children")])
def update_feed_count(header_values):

    return header_values.split(",")[1]


@app.callback(Output("failed-feeds", "figure"),
              [Input("daily_df", "children")])
def update_fail_count(daily_df):
    df = pd.read_json(daily_df, orient="split")
    labels = df.status.value_counts().index.values
    values = df.status.value_counts().values
    trace = go.Pie(labels=labels, values=values)
    layout = dict(margin=dict(l=15, r=10, t=0, b=5), legend=dict(orientation="h"), showlegend=False)
    return dict(data=[trace], layout=layout)

