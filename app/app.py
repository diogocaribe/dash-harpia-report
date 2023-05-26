"""Dashboard Harpia"""

# coding: utf-8

import json
from datetime import date, datetime

import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from data import df_decremento_municipio, gdf_monitramento_dissolve

# css para deixar o layout bonito
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header = html.Header(
    [html.H1("Monitoramento Vegetação"), html.H2("Harpia")],
    className="header bg-primary text-white text-center p-0 m-0",
)

# assinc_await

# Datas iniciais e finais do dataframe
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)

template_graph = {
    "layout": {
        "modebar": {
            "remove": [
                "zoom",
                "pan",
                "select",
                "zoomIn",
                "zoomOut",
                "lasso2d",
                "autoscale",
            ]
        },
        "separators": ".",
        "showlegend": False,
    }
}


############################ Grafico de acumulação ############################
# Grafico de acumulação do desmatamento ao longo do tempo
dff_filter_acumulacao = df_decremento_municipio.query(
    "@year_start <= index <= @year_end"
)["area_ha"]
dff_acumulacao = (
    dff_filter_acumulacao.groupby([dff_filter_acumulacao.index]).sum().cumsum()
)
data_acumulacao = go.Scatter(
    x=dff_acumulacao.index,
    y=dff_acumulacao,
    mode="lines",
)
layout = go.Layout(
    title="Acumulado de Desflorestamento",
    xaxis={"title": "Data"},
    yaxis={"title": "Área (ha)", "hoverformat": ".2f"},
)

grafico_acumulado_tempo = go.Figure(data=data_acumulacao, layout=layout)
grafico_acumulado_tempo.update_layout(template=template_graph)
grafico_acumulado_tempo.update_xaxes(range=[year_start, year_end])
###############################################################################

###############################################################################
######################### Botões para seleção #################################
###############################################################################
date_range_picker = dmc.DateRangePicker(
    id="date-picker-range",
    minDate=min_date,
    maxDate=max_date,
    value=[year_start, max_date],
    inputFormat="DD/MM/YYYY",
)

dropdown_temporal = dcc.Dropdown(
    options=["Diário", "Semanal", "Mensal", "Anual"], value="Diário", clearable=False
)
###############################################################################

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H2("Monitoramento Vegetação"), html.H5("Harpia")],
                    className="d-flex justify-content-between align-items-center",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dl.Map(
                            [dl.TileLayer(), dl.GeoJSON(id="geojson-mapa")],
                            preferCanvas=True,
                            maxBounds=[[-8.5272, -46.6294], [-18.3484, -37.3338]],
                        )
                    ],
                    md=7,
                    class_name="p-0",
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="grafico-acumulado-tempo",
                            figure=grafico_acumulado_tempo,
                            config={"displaylogo": False, "scrollZoom": True},
                        ),
                        html.Div(
                            children=[
                                date_range_picker,
                                dropdown_temporal,
                                dcc.Graph(
                                    id="grafico-dia",
                                    config={"displaylogo": False, "scrollZoom": True},
                                ),
                                dcc.Graph(
                                    id="grafico-municipio",
                                    config={"displaylogo": False, "scrollZoom": True},
                                ),
                            ]
                        ),
                    ],
                    md=5,
                    class_name="p-0",
                    style={
                        "overflow": "overlay",
                        "height": "90vh",
                    },
                ),
            ],
            className="flex-grow-1",
        ),
        dbc.Row([dbc.Col([html.P("Footer")])]),
        dcc.Store(id="monitoramento-municipio"),
    ],
    fluid=True,
    class_name="bg-primary text-white",
    style={
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
    },
)


# Callback mapa
@app.callback(
    Output("geojson-mapa", "children"),
    Input("date-picker-range", "value"),
)
def update_output_mapa(dates):
    """
    Função para atualização dos dados do mapa.
    """
    start_date = dates[0]
    end_date = dates[1]

    date1 = datetime.strptime(start_date, "%Y-%m-%d").date()
    date2 = datetime.strptime(end_date, "%Y-%m-%d").date()

    dff = gdf_monitramento_dissolve.query("@date1 <= index <= @date2")

    map_geojson = dl.GeoJSON(
        data=json.loads(dff.to_json()),
        zoomToBounds=True,
        zoomToBoundsOnClick=True,
    )

    return map_geojson


# DataStore monitoramento-desmatamento-municipio
@app.callback(
    Output("monitoramento-municipio", "data"),
    Input("date-picker-range", "value"),
)
def filter_data_monitoramento_municipio(dates):
    """
    Metodo que filtra os dados e retorna para os callbacks.
    """

    start_date = dates[0]
    end_date = dates[1]

    date1 = datetime.strptime(start_date, "%Y-%m-%d").date()
    date2 = datetime.strptime(end_date, "%Y-%m-%d").date()

    dff = df_decremento_municipio.query("@date1 <= index <= @date2")

    return dff.to_json(date_format="iso", orient="split")


# Callback no grafico de desmatamento diário
# TODO adicinar um filtro aninhado (chaincallback) para agrupar o tempo (D, M, Y)
@app.callback(
    Output("grafico-dia", "figure"),
    Input("monitoramento-municipio", "data"),
)
def update_output_grafico_dia(dados):
    """
    Grafico de atualização de dados do dia
    """
    dff = pd.read_json(dados, orient="split")

    data_day = go.Bar(
        x=dff.index,
        y=dff["area_ha"],
        customdata=np.stack(dff["nome"], axis=-1),
    )
    layout = go.Layout(
        title="Desflorestamento por Tempo",
        xaxis={"title": "Data"},
        yaxis={"title": "Área (ha)"},
    )

    grafico_dia = go.Figure(data=data_day, layout=layout)

    grafico_dia.update_layout(template=template_graph)
    grafico_dia.update_yaxes(fixedrange=False)
    grafico_dia.update_traces(
        hovertemplate="""Município: %{customdata}<br>Data:%{x}<br>Área (ha): %{value:.2f}<extra></extra>"""
    )

    return grafico_dia


# Callback no grafico de desmatamento por município
@app.callback(
    Output("grafico-municipio", "figure"),
    Input("monitoramento-municipio", "data"),
)
def update_output_grafico_municipio(dados):
    """
    Função para atualização do grafico de estatística por município.
    """
    dff = pd.read_json(dados, orient="split")

    dff_municipio = dff.groupby(["nome"]).sum().sort_values("area_ha", ascending=False)
    data_municipio = go.Bar(
        x=dff_municipio.area_ha,
        y=dff_municipio.index,
        orientation="h",
        text=dff_municipio.area_ha,
        texttemplate="%{value:.2f}",
    )
    layout = go.Layout(
        title="Desflorestamento por Município",
        xaxis={"title": "Área (ha)"},
        yaxis={"title": "Município", "autorange": "reversed"},
    )

    grafico_municipio = go.Figure(data=data_municipio, layout=layout)
    grafico_municipio.update_layout(template=template_graph)
    return grafico_municipio


if __name__ == "__main__":
    app.run_server(debug=True)
