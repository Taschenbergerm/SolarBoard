import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from app import indicator, report_table, dash_tabel
import pandas as pd
import numpy as np
white = i1 = i2 = i3 = "#ffffff"
df = pd.read_csv("test.csv")
df["state_code"] = np.where(df.status == "finished", 3,2)
df["state_code"] = np.where(df.status == "failed", 1, df.state_code)
master = df[df.feed == 0]
df = df.drop(master.index)
failed = df[df.state_code == 1 ].shape[0]
succeeded = df[df.state_code == 3 ].shape[0]
all = df.shape[0]

layout = [html.Div(
        [
            indicator(
                i1,
                "Status of today's Master",
                "master_state",
            ),
            indicator(
                i2,
                "Uploaded Today",
                "n_feeds",
            ),
            indicator(
                i3,
                "Failed Requests",
                "failed_feeds",
            ),
        ],
        className="row",
    ),
          html.Div(className="row", children=[
              html.Div(className="eigth columns table", children=dash_tabel(df.sort_values("state_code"))
                       ),
              html.Div(className="four columns summary")
          ])
          ]