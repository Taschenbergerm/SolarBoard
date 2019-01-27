import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import arrow
from app import app
from apps import daily, bulk, history

app.layout = html.Div(
    [
        # header
        html.Div([
            dcc.Interval(id="heartbeat", interval=1*1000, n_intervals=0),
            html.Span("Solactive Complex Board", className='apps-title'),
            html.Div(id="date", style={"margin-top": "2%"}),

        html.Div(
                html.Img(
                    src="https://www.solactive.com/wp-content/themes/solactive-2018/resources/assets/images/logo_solactive.svg",
                    height="100%",
                    style={"margin-top": "-20%"}
                    )
                , style={"float": "right", "height": "75%", "margin-top": "-3.5%"})
        ],
            className="row header",
            style={"background-color":"#10409c"}
        ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(label="Daily Duty", value="daily_tab"),
                    dcc.Tab(label="BulK Loader", value="bulk_tab"),
                    dcc.Tab(label="History", value="history_tab"),
                ],
                value="daily_tab",
            )

        ],
            className="row tabs_div"
        ),

        # divs that save dataframe for each tab
        #html.Div(daily.get_queue_df.to_json(orient="split"), id="daily_df", style={"display": "none"}),
        #html.Div(bulg.get_staging().to_json(orient="split"), id="bulk_df", style={"display": "none"}),  # leads df
        #html.Div(sf_manager.get_cases().to_json(orient="split"), id="cases_df", style={"display": "none"}),  # cases df

        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/plotly/dash-apps-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
            rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
            rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "daily_tab":
        return daily.layout
    elif tab == "bulk_tab":
        return bulk.layout
    elif tab == "history_tab":
        return history.layout
    else:
        return daily.layout


@app.callback(Output("date", "children"),
              [Input("heartbeat", "n_intervals")])
def update_date(n_interval):
    date = arrow.get().to("CET")
    time = arrow.get().to("CET").time()
    return f"{date.format('ddd Do of MMM')} {time.hour}:{time.minute}:{time.second:02}"

if __name__ == '__main__':
    app.run_server(debug=True)

