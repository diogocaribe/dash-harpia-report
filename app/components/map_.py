import dash_bootstrap_components as dbc
import dash_leaflet as dl

map_ = dl.Map([dl.TileLayer()],
            preferCanvas=True,
            maxBounds=[[-8.5272, -46.6294], [-18.3484, -37.3338]],
            style={"height": "93vh"}
        )

map_ = dbc.Row([
    map_
])