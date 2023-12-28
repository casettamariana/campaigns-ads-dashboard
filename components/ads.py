from ctypes import alignment
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pyrsistent import b
from app import *

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

from adapter_api_ads import *



# =========  Data Ingestion  =========== #
api_token = open("environments/api_token").read()
is_localhost = open("environments/is_localhost").read()

api_ads = AdapterApiAds(api_token, is_localhost)

adset_status = pd.DataFrame(api_ads.get_ad_set_status())


# =========  Layout  =========== #
layout = html.Div([

            dbc.Row([
                dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Status"),
                            dbc.CardBody([
                                dbc.Button("", id="btn-ads-status"),
                            ], id="cb-status-ads")
                        ], color="light"),

                    ], md=2),

                dbc.Col([
                    dbc.Card([
                            dbc.CardHeader("Clicks"),
                            dbc.CardBody([
                                html.H4("", id="ads-clicks", style={"color": "var(--bs-info)"}),
                            ])
                        ], color="light"),

                    ], md=2),

                dbc.Col([
                    dbc.Card([
                            dbc.CardHeader("Spend"),
                            dbc.CardBody([
                                html.H4("", id="ads-spend", style={"color": "var(--bs-primary)"}),
                            ])
                        ], color="light"),
                    ], md=2),
                
                dbc.Col([
                    dbc.Card([
                            dbc.CardHeader("Conversion"),
                            dbc.CardBody([
                                html.H5("", id="ads-conversions", style={"color": "var(--bs-primary)"}),
                            ])
                        ], color="light"),
                    ], md=2),
            ]),

            dbc.Row([
                html.H4("Selecione o indicador:"),
                dcc.RadioItems(options=['Spend', 'CPC', 'CPM', 'Clicks', 'Conversion'], 
                            value='Conversion', id='ads-kind', 
                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),
                ], style={"margin-top": "50px"}),

            dbc.Row([            
                dbc.Col(dcc.Graph(id="graph-line-ads"), md=6),
                dbc.Col(dcc.Graph(id="graph-bar-ads"), md=6)
                ], style={"margin-top": "20px"}),
            ]) 

#========== Callbacks ================
@app.callback([
                Output("cb-status-ads", "children"),
                Output("ads-conversions", "children"),
            ], 
                [Input("dd-ads", "value"),
                ])
def render_page_content(ads):
    adset_id = adset_status[adset_status["name"] == ads]["id"].values[0]
    data_over_time = api_ads.get_data_over_time(adset_id)
    conversions = pd.DataFrame(data_over_time["data"])["conversion"].fillna(0).sum()

    return conversions
    


@app.callback([
                Output("graph-line-ads", "figure"),
                Output("graph-bar-ads", "figure"),
            ], 
                [Input("dd-ads", "value"),
                Input("ads-kind", "value"),
                Input(ThemeChangerAIO.ids.radio("theme"), "value")]
            )
def render_page_content(ads, adset_kind, theme):
    # ads = adset_status["name"].values[0]
    adset_id = adset_status[adset_status["name"] == ads]["id"].values[0]
    # adset_kind = "conversion"
    adset_kind = adset_kind.lower()   
    
    data_over_time = api_ads.get_data_over_time(adset_id)
    df_data = pd.DataFrame(data_over_time["data"])
    df_data["clicks"] = df_data["clicks"].astype(np.float64)
    
    fig_line = px.line(df_data, x="date_start", y=adset_kind, template=template_from_url(theme))
    fig_line.update_layout(margin=go.layout.Margin(l=0, r=0, t=0, b=0))
    
    return fig_line

    