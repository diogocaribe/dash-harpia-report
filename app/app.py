"""Dashboard Harpia"""

# coding: utf-8

from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.express as px
from dash import Input, Output, dcc, html
from data import \
    df_decremento_municipio  # , geojson_monitoramento_dissolve, df_monitoramento_por_dia,

# css para deixar o layout bonito
external_stylesheets = ["./assets/style.css", "./assets/reset.css", dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header = html.Header(
    [html.H1("Monitoramento Vegetação"), html.H2("Harpia")], className="header"
)


# wms = dl.WMSTileLayer(
#     url="http://geoserver-homo.harpia.ba.gov.br/harpia/wms",
#     layers="monitoramento_dissolve_wmts",
#     format="image/png",
#     transparent=True,
# )

# leaflet_map = dl.Map(
#     [
#         dl.TileLayer(),
#         wms
#         #  dl.GeoJSON(data=geojson_monitoramento_dissolve,
#         #  zoomToBounds=True, zoomToBoundsOnClick=True)
#     ],
#     style={"width": "100%", "height": "500px"},
# )


# Grafico de acumulado de desflorestamento por dia
# fig = px.bar(df_decremento_municipio["area_ha"], title="Acumulado diário de Decremento")
# fig.update_layout(showlegend=False)
# grafico_decremento_dia = dcc.Graph(id="grafico-total", figure=fig)

# Por municiipio
df = px.data.tips()
fig1 = px.bar(df, x="total_bill", y="day", orientation="h")
grafico1 = dcc.Graph(id="grafico-municipio", figure=fig1)

footer = html.Footer(html.H2("Final"))

# Datas iniciais e finais da análise
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

app.layout = html.Div(
    children=[
        header,
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date
        ),
        dcc.Graph(id='mymap'),
        grafico1, 
        footer],
    className="main_layout"
)

@app.callback(
    Output('mymap', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)

def update_output(start_date, end_date):
    """
        Oi.
    """
    # print("Start date: " + start_date)
    # print("End date: " + end_date)
    dff = df_decremento_municipio["area_ha"].loc[datetime.strptime(start_date, '%Y-%m-%d').date():datetime.strptime(end_date, '%Y-%m-%d').date()]
    print(dff[:5])

    figure = px.bar(dff, title="Acumulado diário de Decremento")

    return figure


if __name__ == "__main__":
    app.run_server(debug=True)
