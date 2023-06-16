"""Dashboard Harpia"""
import dash_bootstrap_components as dbc

from app import app

from .components import footer, graph, header, map_

server = app.server

app.layout = dbc.Container(
    [
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
        # dcc.Store(id="monitoramento-municipio"),
    ],
    class_name="overflow-hidden",
    fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True)
