"""Dashboard Harpia"""
import dash
import dash_bootstrap_components as dbc
from components import footer, graph, header, map_
from flask import Flask

from app import app

app.layout = dbc.Container(
    [
        dbc.Row([header.header]),
        dbc.Row(
            [
                dbc.Col([map_.map_],
                        width=7
                ),
                dbc.Col([graph.graphs],
                        width=5,
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
