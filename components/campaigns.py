from ctypes import alignment
from dash import html, dcc
from dash.dependencies import Input, Output
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
print(campaign_status)

# =========  Layout  =========== #
layout = html.Div([
    dash_bootstrap_components.Row([
        dash_bootstrap_components.Col([
            
        ])
    ])
])


# ========== Callbacks ================
