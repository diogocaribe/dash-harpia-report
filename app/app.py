"""Dashboard Harpia"""

# coding: utf-8

from datetime import date, datetime
import json

import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import numpy as np
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


leaflet_map = dl.Map(
    [
        dl.TileLayer(),
        dl.GeoJSON(
            data=json.loads(gdf_monitramento_dissolve.to_json()),
            zoomToBounds=True,
            zoomToBoundsOnClick=True,
        ),
    ],
    preferCanvas=True,
)

# Datas iniciais e finais do dataframe
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)

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
    showlegend=False,
    separators=".",
    modebar_remove=["zoom", "pan", "select", "zoomIn", "zoomOut", "lasso2d"],
)

grafico_acumulado_tempo = go.Figure(data=data_acumulacao, layout=layout)
###############################################################################

date_picker = html.Div(
    [
        dcc.DatePickerRange(
            id="my-date-picker-range",
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=year_start,
            end_date=max_date,
            number_of_months_shown=2,
            display_format="DD/MM/YYYY",
        ),
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H1("MONITORAMENTO VEGETAÇÃO"), html.H4("Harpia")],
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
                        )
                    ],
                    md=7,
                    # xs=12,
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
                                date_picker,
                                dcc.Graph(
                                    id="grafico-dia",
                                    config={"displaylogo": False, "scrollZoom": True},
                                ),
                            ]
                        ),
                        dcc.Graph(
                            id="grafico-municipio",
                            config={"displaylogo": False, "scrollZoom": True},
                        ),
                    ],
                    md=5,
                    # xs=12,
                    className="bg-light",
                ),
            ],
            style={"flexGrow": "1"},
        ),
        dbc.Row([dbc.Col([html.P("Footer")])]),
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
    [
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_output_mapa(start_date, end_date):
    """
    Oi.
    """
    date1 = datetime.strptime(start_date, "%Y-%m-%d").date()
    date2 = datetime.strptime(end_date, "%Y-%m-%d").date()

    dff = gdf_monitramento_dissolve.query("@date1 <= index <= @date2")

    map_geojson = dl.GeoJSON(
        data=json.loads(dff.to_json()),
        zoomToBounds=True,
        zoomToBoundsOnClick=True,
    )

    return map_geojson


# Callback no grafico de desmatamento diário
# TODO adicinar um filtro aninhado (chaincallback) para agrupar o tempo (D, M, Y)
@app.callback(
    Output("grafico-dia", "figure"),
    [
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_output_grafico_dia(start_date, end_date):
    """
    Oi.
    """
    date1 = datetime.strptime(start_date, "%Y-%m-%d").date()
    date2 = datetime.strptime(end_date, "%Y-%m-%d").date()

    dff = df_decremento_municipio.query("@date1 <= index <= @date2")

    data_day = go.Bar(
        x=dff.index,
        y=dff["area_ha"],
        customdata=np.stack(dff["nome"], axis=-1),
    )
    layout = go.Layout(
        title="Desflorestamento por Tempo",
        xaxis={"title": "Data"},
        yaxis={"title": "Área (ha)"},
        showlegend=False,
        separators=".",
        modebar_remove=["zoom", "pan", "select", "zoomIn", "zoomOut", "lasso2d"],
    )

    grafico_dia = go.Figure(data=data_day, layout=layout)

    grafico_dia.update_yaxes(fixedrange=False)
    grafico_dia.update_traces(
        hovertemplate="""Município: %{customdata}<br>Data:%{x}<br>Área (ha): %{value:.2f}<extra></extra>"""
    )
    grafico_dia.update_layout(
        xaxis={
            "rangeslider": {"visible": True},
            "type": "date",
        }
    )

    return grafico_dia


# Callback no grafico de desmatamento por município
@app.callback(
    Output("grafico-municipio", "figure"),
    [
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_output_grafico_municipio(start_date, end_date):
    """
    Oi.
    """
    date1 = datetime.strptime(start_date, "%Y-%m-%d").date()
    date2 = datetime.strptime(end_date, "%Y-%m-%d").date()

    dff = df_decremento_municipio.query("@date1 <= index <= @date2")

    dff_filter_municipio = df_decremento_municipio.query("@date1 <= index <= @date2")
    dff_municipio = (
        dff_filter_municipio.groupby(["nome"])
        .sum()
        .sort_values("area_ha", ascending=False)
    )
    data_municipio = go.Bar(
        x=dff_municipio.area_ha,
        y=dff_municipio.index,
        orientation="h",
    )
    layout = go.Layout(
        title="Desflorestamento por Município",
        xaxis={"title": "Área (ha)"},
        yaxis={"title": "Município", "autorange": "reversed"},
        showlegend=False,
        separators=".",
        modebar_remove=["zoom", "pan", "select", "zoomIn", "zoomOut", "lasso2d"],
    )

    grafico_municipio = go.Figure(data=data_municipio, layout=layout)

    return grafico_municipio


if __name__ == "__main__":
    app.run_server(debug=False)
