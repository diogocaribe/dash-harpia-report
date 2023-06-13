from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()

fig.update_layout(template="plotly", paper_bgcolor="rgba(0,0,0,0)")

graphs = dbc.Row([
    dcc.Graph(id="graph", figure=fig,
               style={"overflow-y": "scroll", "height": "93vh"})
])