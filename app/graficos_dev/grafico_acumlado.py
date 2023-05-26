from datetime import date
from data import df_decremento_municipio
import plotly.graph_objects as go


# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)

template_graph = {
    "layout": {
        "modebar": {
            "remove": ["zoom", "pan", "select", "zoomIn", "zoomOut", "lasso2d", "autoscale"]
        },
        "separators": ".",
        "showlegend": False,
    }
}


############################ Grafico de acumulação ############################
# Grafico de acumulação do desmatamento ao longo do tempo
dff_filter_acumulacao = df_decremento_municipio.query(
    "@year_start <= index <= @year_end"
)["area_ha"]
dff_acumulacao = (
    dff_filter_acumulacao.groupby([dff_filter_acumulacao.index]).sum().cumsum()
)
data_acumulacao = go.Scatter(
    x=dff_acumulacao.index,
    y=dff_acumulacao,
    mode="lines",
)
layout = go.Layout(
    title=f"Acumulado de Desflorestamento: {year_start}",
    xaxis={"title": "Data"},
    yaxis={"title": "Área (ha)", "hoverformat": ".2f"},
)

grafico_acumulado_tempo = go.Figure(data=data_acumulacao, layout=layout)
grafico_acumulado_tempo.update_layout(template=template_graph)

grafico_acumulado_tempo.update_xaxes(range=[year_start, year_end])

grafico_acumulado_tempo.show()