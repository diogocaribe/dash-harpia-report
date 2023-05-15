"""Dashboard Harpia"""

# coding: utf-8

from datetime import date, datetime

import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from data import df_decremento_municipio, geojson_monitoramento_dissolve

# css para deixar o layout bonito
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header = html.Header(
    [html.H1("MONITORAMENTO VEGETAÇÃO"), html.H4("Harpia")],
    className="header bg-primary text-white text-center p-0 m-0",
)

# assinc_await
wms = dl.WMSTileLayer(
    url="http://geoserver-homo.harpia.ba.gov.br/harpia/wms",
    layers="monitoramento_dissolve",
    format="image/png",
    transparent=True,
)

leaflet_map = dl.Map(
    [
        dl.TileLayer(),
        wms
        # dl.GeoJSON(
        #     data=geojson_monitoramento_dissolve,
        #     zoomToBounds=True,
        #     zoomToBoundsOnClick=True,
        # ),
    ],
    # style={"width": "100%", "height": "100%"},
)

# Datas iniciais e finais do dataframe
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)

# Grafico de acumulação do desmatamento
dff = df_decremento_municipio["area_ha"].sort_index().cumsum(skipna=False)

data = go.Scatter(
    x=dff.index,
    mode="lines",
)
layout = go.Layout(
    title="Acumulado de Desflorestamento",
    xaxis={"title": "Data"},
    yaxis={"title": "Área (ha)"},
    showlegend=False,
    separators=".",
    modebar_remove=["zoom", "pan", "select", "zoomIn", "zoomOut", "lasso2d"],
)

figure_line = go.Figure(data=data, layout=layout)

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
                    [leaflet_map],
                    md=8,
                    xs=12,
                    style={"backgroundColor": "green"},
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="example-graph",
                            figure=figure_line,
                            config={"displaylogo": False, "scrollZoom": True},
                        ),
                        html.Div(
                            children=[
                                date_picker,
                                dcc.Graph(
                                    id="grafico-desmatamento-tempo",
                                    config={"displaylogo": False, "scrollZoom": True},
                                ),
                            ]
                        ),
                    ],
                    md=4,
                    xs=12,
                    style={"backgroundColor": "blue"},
                ),
            ],
            style={"flexGrow": "1"},
        ),
        dbc.Row([dbc.Col([html.P("FOOTER")])]),
    ],
    fluid=True,
    className="bg-primary text-white",
    style={
        "height": "100vh",
        # "backgroundColor": "yellow",
        "display": "flex",
        "flexDirection": "column",
    },
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
        modebar_remove=["zoom", "pan", "select", "zoomIn", "zoomOut", "lasso2d"],
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
