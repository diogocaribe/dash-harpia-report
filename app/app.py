# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_leaflet as dl
from dash import dcc
from dash import html
from data import  df_decremento_municipio #, geojson_monitoramento_dissolve, df_monitoramento_por_dia,

import plotly.express as px


# css para deixar o layout bonito
external_stylesheets = [
    './assets/style.css', './assets/reset.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header = html.Header([
    html.H1('Monitoramento Vegetação'),
    html.H2(f'Harpia')
], className="header"
)


wms = dl.WMSTileLayer(url="http://geoserver-homo.harpia.ba.gov.br/harpia/wms", layers="monitoramento_dissolve_wmts",
                      format="image/png", transparent=True)

map = dl.Map([dl.TileLayer(), wms
            #   dl.GeoJSON(data=geojson_monitoramento_dissolve, zoomToBounds=True, zoomToBoundsOnClick=True)
            ],
    style={"width": "100%", "height": "500px"})


# Grafico de acumulado de desflorestamento por dia
fig = px.bar(df_decremento_municipio["area_ha"], title="Acumulado diário de Decremento")
fig.update_layout(showlegend=False)

grafico = dcc.Graph(id="grafico-total",
                figure=fig)


# POr municiipio
df = px.data.tips()
fig1 = px.bar(df, x="total_bill", y="day", orientation='h')

grafico1 = dcc.Graph(id="grafico-municipio",
            figure=fig1)

footer = html.Footer(html.H2('Final'))

app.layout = html.Div(children=[
                header,
                map,
                grafico,
                grafico1,
                footer
            ],
            className="main")

if __name__ == '__main__':
    app.run_server(debug=True)
