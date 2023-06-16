"""Compenente."""
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import n_colors
from app.dataset.data import df_decremento_municipio


# dcc.Graph(
#         id="grafico-acumulado-tempo",
#         figure=grafico_acumulado_tempo,
#         config={"displaylogo": False, "scrollZoom": True},
#                     )

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

greys_custom = n_colors(
    "rgb(220, 220, 220)", "rgb(160, 160, 160)", len(lista_ano) + 1, colortype="rgb"
)

for year, color in zip(lista_ano[:-1], greys_custom):
    x_ = df_empty.loc[df_empty.index.year == year, "timedelta"]
    y_ = df_empty.loc[df_empty.index.year == year, "cumsum"]
    data = go.Scatter(
        x=x_,
        y=y_,
        mode="lines",
        name=year,
        legendgrouptitle={"text": "Ano"},
        marker={"color": color},
        opacity=0.7,
    )

    grafico_acumulado_tempo.add_trace(data)

x_ = df_empty.loc[df_empty.index.year == lista_ano[-1], "timedelta"]
y_ = df_empty.loc[df_empty.index.year == lista_ano[-1], "cumsum"]

data = go.Scatter(
    x=x_,
    y=y_,
    mode="lines",
    name=ano,
)

grafico_acumulado_tempo.add_trace(data)

grafico_acumulado_tempo.update_layout(
    title="Acumulado Desflorestamento por Tempo",
    xaxis={"title": "Data", "type": "date"},
    yaxis={"title": "Área (ha)"},
    xaxis_tickformat="%d-%m",
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

grafico_acumulado_tempo.show(config={"displaylogo": False})
