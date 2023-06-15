"""Barra de graficos."""
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from .controller import date_range_picker

fig = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
    layout=go.Layout(
        title=go.layout.Title(text="A Figure Specified By A Graph Object")
    ),
)

fig1 = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
    layout=go.Layout(
        title=go.layout.Title(text="A Figure Specified By A Graph Object")
    ),
)

graphs = html.Div([
        dcc.Graph(
            id="fig", figure=fig,
            config={"displaylogo": False, "scrollZoom": True},
        ),
        html.Div(
            children=[
                date_range_picker,
                dcc.Graph(
                    id="grafico-dia",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
                dcc.Graph(
                    id="grafico-municipio",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ]
        ),
])