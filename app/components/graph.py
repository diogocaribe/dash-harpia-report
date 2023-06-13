from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure(
    data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
    layout=go.Layout(
        title=go.layout.Title(text="A Figure Specified By A Graph Object")
    )
)

graphs = dbc.Row([
    dcc.Graph(id="graph", figure=fig,
            style={"overflow-y": "scroll", "height": "93vh"})
])