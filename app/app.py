"""Dashboard Harpia"""

# coding: utf-8

from datetime import datetime, date

import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from data import (
    df_decremento_municipio,
)  # , geojson_monitoramento_dissolve, df_monitoramento_por_dia,

import numpy as np

# css para deixar o layout bonito
external_stylesheets = [
    # "./assets/style.css",
    # "./assets/reset.css",
    dbc.themes.BOOTSTRAP,
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header = html.Header(
    [html.H1("MONITORAMENTO VEGETAÇÃO"), html.H4("Harpia")],
    className="header bg-primary text-white p-2 mb-2 text-center",
)


# wms = dl.WMSTileLayer(
#     url="http://geoserver-homo.harpia.ba.gov.br/harpia/wms",
#     layers="monitoramento_dissolve_wmts",
#     format="image/png",
#     transparent=True,
# )

# leaflet_map = dl.Map(
#     [
#         dl.TileLayer(),
#         wms
#         #  dl.GeoJSON(data=geojson_monitoramento_dissolve,
#         #  zoomToBounds=True, zoomToBoundsOnClick=True)
#     ],
#     style={"width": "100%", "height": "500px"},
# )

footer = html.Footer(html.H2("Final"))

# Datas iniciais e finais do dataframe
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)


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
    ],
)

app.layout = html.Div(
    children=[
        header,
        date_picker,
        dcc.Graph(id="grafico-desmatamento-tempo"),
        # leaflet_map,
        footer,
    ],
    className="main_layout",
)


@app.callback(
    Output("grafico-desmatamento-tempo", "figure"),
    [
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_output(start_date, end_date):
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
        # marker={"color" : dff["area_ha"], "colorscale":'agsunset'}
    )
    layout = go.Layout(
        title="Desflorestamento por Tempo",
        xaxis={"title": "Data"},
        yaxis={"title": "Área (ha)"},
        showlegend=False,
        separators=".",
    )

    figure_day = go.Figure(data=data_day, layout=layout)
    figure_day.update_yaxes(fixedrange=False)
    figure_day.update_traces(
        hovertemplate="""Município: %{customdata}<br>Data:%{x}<br>Área (ha): %{value:.2f}<extra></extra>"""
    )

    figure_day.update_layout(
        xaxis={
            "rangeselector": {
                "buttons": list(
                    [
                        {
                            "count": 1,
                            "label": "1m",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {
                            "count": 6,
                            "label": "6m",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {
                            "count": 1,
                            "label": "YTD",
                            "step": "year",
                            "stepmode": "todate",
                        },
                        {
                            "count": 1,
                            "label": "1y",
                            "step": "year",
                            "stepmode": "backward",
                        },
                        {"step": "all"},
                    ]
                )
            },
            "rangeslider": {"visible": True},
            "type": "date",
        }
    )

    return figure_day


if __name__ == "__main__":
    app.run_server(debug=True)
