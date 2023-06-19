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