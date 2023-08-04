"""Barra de graficos."""
from dash import dcc, html, Input, Output, callback
import numpy as np
import plotly.graph_objects as go
from .controller import date_range_picker

from .grafico_acumulado_ano import fig_acumulado_ano

import pandas as pd

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

graphs = html.Div(
    [
        html.Div(
            fig_acumulado_ano
            # , style={"height": "300px"}
        ),
        html.Div(
            children=[
                date_range_picker,
                dcc.Graph(
                    id="grafico-dia",
                    config={"displaylogo": False, "scrollZoom": False},
                ),
                dcc.Graph(
                    id="grafico-municipio",
                    config={"displaylogo": False, "scrollZoom": False},
                ),
            ]
        ),
    ]
)


# Callback no grafico de desmatamento diário
# TODO adicinar um filtro aninhado (chaincallback) para agrupar o tempo (D, M, Y)
@callback(
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
        title="<b>Evolução diária do desmatamento</b>",
        xaxis={"title": "Data"},
        yaxis={"title": "Área (ha)"},
    )

    grafico_dia = go.Figure(data=data_day, layout=layout)

    grafico_dia.update_layout(template=template_graph)
    grafico_dia.update_yaxes(fixedrange=False)
    grafico_dia.update_traces(
        hovertemplate="""Município: %{customdata}<br>Data: %{x}<br>Área (ha): %{value:.2f}<extra></extra>"""
    )

    return grafico_dia


# Callback no grafico de desmatamento por município
@callback(
    Output("grafico-municipio", "figure"),
    Input("monitoramento-municipio", "data"),
)
def update_output_grafico_municipio(dados):
    """
        Função para atualização do grafico de estatística por município.
    """
    dff = pd.read_json(dados, orient="split")

    dff_municipio = dff.groupby(["nome"]).sum().sort_values(by=["area_ha"], ascending=False).iloc[:15]

    data_municipio = go.Bar(
        y=dff_municipio.area_ha,
        x=dff_municipio.index,
        orientation="v",
        # text=dff_municipio.area_ha,
        # texttemplate="%{value:.2f}",
        hovertemplate="""Município: %{x}<br>Área (ha): %{value:.2f}<extra></extra>"""
    )

    grafico_municipio = go.Figure(
        data=data_municipio,
        layout={
            "title": {"text": "<b>Ranking por Município</b>"},
            "xaxis": {"title": "Município"},
            "yaxis": {"title": "Área (ha)"},
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
        },
    )


    return grafico_municipio