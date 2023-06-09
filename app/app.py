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
from dataset.data import df_decremento_municipio, gdf_monitramento_dissolve
from flask import Flask
# from _components import grafico_acumulacao_ano
from plotly.colors import n_colors

# css para deixar o layout bonito
external_stylesheets = [dbc.themes.BOOTSTRAP]

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.title = 'HarpiaDashboard'

header = html.Header(
    [html.H1("Monitoramento Vegetação"), html.H2("Harpia")],
    className="header bg-primary text-white text-center p-0 m-0",
)

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

df_decremento_municipio.index = pd.to_datetime(df_decremento_municipio.index)

############################ Grafico de acumulação ############################
# Grafico de acumulação do desmatamento ao longo do tempo
df_decremento_municipio_ = (
    df_decremento_municipio[["area_ha"]].groupby(df_decremento_municipio.index).sum()
)
lista_ano = df_decremento_municipio.index.year.unique()[
    df_decremento_municipio.index.year.unique() > 2017
]

df_empty = pd.DataFrame()
for ano in lista_ano:
    df = df_decremento_municipio_.loc[df_decremento_municipio_.index.year == ano]
    df["timedelta"] = (
        df.index - (df.index.year.astype("str") + "-01-01").astype("datetime64[ns]")
    ) / 1000000
    df["cumsum"] = df.loc[:, "area_ha"].cumsum()
    df_empty = pd.concat([df_empty, df[["timedelta", "cumsum"]]])

# Construindo os graficos dos anos passados da série histórica
grafico_acumulado_tempo = go.Figure()

greys_custom = n_colors(
    "rgb(220, 220, 220)", "rgb(160, 160, 160)", len(lista_ano) + 1, colortype="rgb"
)

for year, color in zip(lista_ano[:-1], greys_custom):
    x_ = df_empty.loc[df_empty.index.year == year, "timedelta"]
    y_ = df_empty.loc[df_empty.index.year == year, "cumsum"]
    data = go.Scatter(
        x=x_,
        y=y_,
        mode="lines",
        name=year,
        legendgrouptitle={"text": "Ano"},
        marker={"color": color},
        opacity=0.7,
    )

    grafico_acumulado_tempo.add_trace(data)

x_ = df_empty.loc[df_empty.index.year == lista_ano[-1], "timedelta"]
y_ = df_empty.loc[df_empty.index.year == lista_ano[-1], "cumsum"]

data = go.Scatter(
    x=x_,
    y=y_,
    mode="lines",
    name=ano,
)

grafico_acumulado_tempo.add_trace(data)

grafico_acumulado_tempo.update_layout(
    title="Acumulado Desflorestamento por Tempo",
    xaxis={"title": "Data", "type": "date"},
    yaxis={"title": "Área (ha)"},
    xaxis_tickformat="%d-%m",
    modebar={
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
    separators=".",
    showlegend=True,
)
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
                    width=12,
                    className="bg-primary d-flex justify-content-between align-items-center",
                    style={"height": "6vh"},
                )
            ]
        ),
        dbc.Row([
            dbc.Col(
                [dl.Map([dl.TileLayer(), dl.GeoJSON(id="geojson-mapa")],
                    preferCanvas=True,maxBounds=[[-8.5272, -46.6294], [-18.3484, -37.3338]],
                )],
            width=7,
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
            width=5,
            style={"overflow-y": "scroll", "height": "90vh"},
            )
        ]),
        dbc.Row([
            dbc.Col([html.P("Footer")],
            width=12,
            className="bg-primary",
            style={"height": "4vh"}
            )
        ]),
        dcc.Store(id="monitoramento-municipio"),
    ],
    class_name="overflow-hidden",
    fluid=True,
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

    grafico_municipio = go.Figure(
        data=data_municipio,
        layout_title_text="Desflorestamento por Município",
        layout = {
            "title": {"text": "Desflorestamento por Município"},
            "xaxis": {"title": "Área (ha)"},
            "yaxis": {"title": "Município", "autorange": "reversed"},
        }
    )

    grafico_municipio.update_layout(template=template_graph)
    return grafico_municipio


if __name__ == "__main__":
    app.run_server(debug=True)
