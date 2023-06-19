import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import Input, Output, callback, dcc, html
import json

map_ = dl.Map([dl.TileLayer(), dl.GeoJSON(id="geojson-mapa")],
            preferCanvas=True,
            maxBounds=[[-8.5272, -46.6294], [-18.3484, -37.3338]],
            id="leaflet-map",
            style={"height": "92vh"}
        )

map_ = dbc.Row([
    map_
])

# Callback mapa
@callback(
    Output("geojson-mapa", "children"),
    Input("monitoramento-dissolve", "data"),
)
def update_output_mapa(gdf):
    """
    Função para atualização dos dados do mapa.
    """
    map_geojson = dl.GeoJSON(
        data=json.loads(gdf),
        zoomToBounds=True,
        zoomToBoundsOnClick=True,
        options={"style":{"color":"red"}},
    )

    return map_geojson
