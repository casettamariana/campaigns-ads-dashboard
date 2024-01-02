from ctypes import alignment
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components
from pyrsistent import b
from app import *

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

from adapter_api_ads import AdapterApiAds
import pandas as pd


# =========  Data Ingestion  =========== #
api_token = open("environments/api_token").read()
is_localhost = open("environments/is_localhost").read()

api_ads = AdapterApiAds(api_token, is_localhost)

campaign_status = pd.DataFrame(api_ads.get_campaigns_status())

# =========  Layout  =========== #
layout = html.Div([
    dash_bootstrap_components.Row([
        dash_bootstrap_components.Col([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Status"),
                    dbc.CardBody([
                        html.P("", id="ads-clicks"),
                    ], id="cb-status-ads")
                ], color="light", className="card-body-ads"),
            ], md=2),
        ])
    ])
])


@app.callback(
    Output("ads-clicks", "children"),
    Input("ads-clicks", "value"),
    State("ads-clicks", "children")
)
def update_ads_clicks(selected_value, current_value):
    selected_campaign_status = campaign_status[campaign_status['id'] == "120202267242370165"]

    status = selected_campaign_status.iloc[0]['status'] if not selected_campaign_status.empty else ""

    return f"{status}"