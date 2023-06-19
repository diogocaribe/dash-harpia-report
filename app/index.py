"""Dashboard Harpia"""
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output
from datetime import datetime

from app import app

from dataset.data import df_decremento_municipio, gdf_monitoramento_dissolve
from components import footer, graph, header, map_

server = app.server

app.layout = dbc.Container(
    [
        dcc.Store(id="monitoramento-municipio"),
        dcc.Store(id="monitoramento-dissolve"),
        dbc.Row([header.header]),
        dbc.Row(
            [
                dbc.Col(
                    [map_.map_],
                    width=7
                ),
                dbc.Col(
                    [graph.graphs],
                    width=5,
                    style={"overflow-y": "scroll", "height": "95vh"}
                )
            ]
        ),
        dbc.Row([footer.footer]),
    ],
    class_name="overflow-hidden",
    fluid=True
)

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


# DataStore monitoramento-desmatamento-municipio
@app.callback(
    Output("monitoramento-dissolve", "data"),
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
    
    dff = gdf_monitoramento_dissolve.query("@date1 <= index <= @date2")
    # dff['view_date'] = dff['view_date'].astype(str)

    return dff.to_json()


if __name__ == "__main__":
    app.run_server(debug=True)
