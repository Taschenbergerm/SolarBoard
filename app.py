
import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True


def indicator(color, text, id_value):
    return html.Div(
        [

            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id=id_value,
                className="indicator_value"
            ),
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

def dash_tabel(df):
    return dt.DataTable(
        data=df.to_dict('rows'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        n_fixed_rows=1,
        style_as_list_view=True,

        style_table={
            'maxHeight': '1000',
            'overflowY': 'scroll'
        },
        style_data_conditional=[
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