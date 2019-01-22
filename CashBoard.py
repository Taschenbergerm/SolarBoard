import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from apps import daily, bulk, history

externel_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets= externel_css)
app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("Solactive Complex Board", className='apps-title'),

            html.Div(
                html.Img(
                    src='https://www.google.com/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F6%2F6f%2F%25C2%25A9_Solactive_AG_Logo_Color.svg%2F1200px-%25C2%25A9_Solactive_AG_Logo_Color.svg.png&imgrefurl=https%3A%2F%2Fde.wikipedia.org%2Fwiki%2FSolactive&docid=QDS7D4FDZvwdhM&tbnid=fxxt9BBGOlc5-M%3A&vet=10ahUKEwj8jLPW1P_fAhXSsaQKHdz3ByMQMwg_KAEwAQ..i&w=1200&h=505&bih=558&biw=1097&q=Solactive&ved=0ahUKEwj8jLPW1P_fAhXSsaQKHdz3ByMQMwg_KAEwAQ&iact=mrc&uact=8',
                    height="100%")
                , style={"float": "right", "height": "100%"})
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

if __name__ == '__main__':
    app.run_server(debug=True)