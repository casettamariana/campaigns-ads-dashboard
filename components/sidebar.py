from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from app import app
import pandas as pd


from adapter_api_ads import AdapterApiAds


# =========  Data Ingestion  =========== #
api_token = open("environments/api_token").read()
is_localhost = open("environments/is_localhost").read()

api_ads = AdapterApiAds(api_token, is_localhost)

customers = api_ads.get_business()

style_sidebar = style={"box-shadow": "2px 2px 10px 0px rgba(6, 47, 97, 0.051)",
                    "margin": "10px",
                    "padding": "10px",
                    "height": "100vh"}

# =========  Layout  =========== #
layout = dbc.Card(
    [
        html.Img(src=app.get_asset_url("logo_dark.webp"), style={"width": "100px"}),
        html.Hr(), 
        dbc.Nav(
            [
                dcc.Dropdown(id="dropdown-empresas", options=[], value="1"),
                dbc.NavLink("Campaigns", href="/", active="exact"),
                dbc.NavLink("Ads", href="/ads", active="exact"),
                dbc.NavLink("Adsets", href="/adsets", active="exact"),
            ], vertical=True, pills=True, style={"margin-bottom": "50px"}),
        html.Hr(), 
        
    ], style=style_sidebar
)

@app.callback(
    Output("dropdown-empresas", "options"),
    Input("dropdown-empresas", "value")
)
def my_callback(selected_value):
    options_list = []
    
    for item in customers['data']:
        options_list.append({"label": item["name"], "value": item["id"]})

    return options_list
