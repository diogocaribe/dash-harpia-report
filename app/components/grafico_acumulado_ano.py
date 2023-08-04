"""O que esta melhor bem feito"""
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dataset.data import df_decremento_municipio


df_decremento_municipio.index = pd.to_datetime(df_decremento_municipio.index)

df_decremento_municipio = (
    df_decremento_municipio[["area_ha"]].groupby(df_decremento_municipio.index).sum()
)

lista_ano = df_decremento_municipio.index.year.unique()[
    df_decremento_municipio.index.year.unique() > 2017
]

df_empty = pd.DataFrame()
for ano in lista_ano:
    df = df_decremento_municipio.loc[df_decremento_municipio.index.year == ano]
    df["timedelta"] = (
        df.index - (df.index.year.astype("str") + "-01-01").astype("datetime64[ns]")
    ) / 1000000
    df["cumsum"] = df.loc[:, "area_ha"].cumsum()

    df_empty = pd.concat([df_empty, df[["timedelta", "cumsum"]]])

# Construindo os graficos dos anos passados da série histórica
grafico_acumulado_tempo = go.Figure()

for year in lista_ano[:-1]:
    x_ = df_empty.loc[df_empty.index.year == year, "timedelta"]
    y_ = df_empty.loc[df_empty.index.year == year, "cumsum"]

    
    data = go.Scatter(
        x=x_,
        y=y_,
        mode="lines",
        name=year,
        legendgrouptitle={"text": "Ano"},
        opacity=0.4,
    )

    grafico_acumulado_tempo.add_trace(data)

x_ = df_empty.loc[df_empty.index.year == lista_ano[-1], "timedelta"]
y_ = df_empty.loc[df_empty.index.year == lista_ano[-1], "cumsum"]
data = go.Scatter(
    x=x_,
    y=y_,
    mode="lines",
    marker={"color": "red"},
    line={"width" : 3.5},
    name=ano,
)
grafico_acumulado_tempo.add_trace(data)


grafico_acumulado_tempo.update_layout(
    title="<b>Evolução anual do desmatamento</b>",
    xaxis={"title": "Data", "type": "date"},
    yaxis={"title": "Área (ha)"},
    xaxis_tickformat="%d-%b",
    modebar={
        "remove": [
            "zoom",
            "pan",
            "select",
            "zoomIn",
            "zoomOut",
            "lasso2d",
            "autoscale",
        ]
    },
    separators=".",
    showlegend=True,
)

grafico_acumulado_tempo.update_traces(
        hovertemplate="""<br>Data: %{x}<br>Área (ha): %{y:.2f}<extra></extra>"""
    )

fig_acumulado_ano = dcc.Graph(id="fig-acumulado", figure=grafico_acumulado_tempo,
                        config={"displaylogo": False, "scrollZoom": False}
                    )