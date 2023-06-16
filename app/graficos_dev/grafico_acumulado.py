from datetime import date, datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from data import df_decremento_municipio

df_decremento_municipio = pd.read_csv('app/data/decremento_municipio_202305291512.csv', index_col="view_date") 

template_graph = {
    "layout": {
        "modebar": {
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
        "separators": ".",
        "showlegend": True,
    }
}

df_decremento_municipio.index = pd.to_datetime(df_decremento_municipio.index)
df_decremento_municipio["year"] = df_decremento_municipio.index.year

min_date = df_decremento_municipio.index.date.min()
max_date = df_decremento_municipio.index.date.max()


df=pd.Series(name="area_ha", dtype="float64")
for ano in df_decremento_municipio.index.year.unique()[
    df_decremento_municipio.index.year.unique() > 2016
]:
    # Remover os anos de 2015 e 2016 (dados muito ruins)

    df_por_ano = df_decremento_municipio[df_decremento_municipio["year"] == ano]
    dff_acumulacao = df_por_ano["area_ha"].groupby([df_por_ano.index]).sum().cumsum()
    df = df.append(dff_acumulacao)

fig = go.Figure()

# Primeira data de cada dado no ano
start = ["2020-01-01", "2018-01-04", "2021-01-05" , "2022-01-05", "2019-01-01", "2023-01-10", "2017-12-27"]
# Ultima data de cada dado no ano
end =   ["2020-12-31", "2018-12-27", "2021-12-16", "2022-12-31", "2019-12-22",  "2023-05-03", "2017-01-26"]

years = df.index.year.unique()[df.index.year.unique()>2016].sort_values()

for idx, (s,e) in enumerate(zip(start, end)):
    tmp = df[(df.index >= start[idx]) & (df.index <= end[idx])]
    fig.add_trace(go.Scatter(x=tmp.index,
                             y=tmp,
                             name=str(years[idx]),
                             mode='lines',
                            ))

fig.update_layout(height=600, xaxis_tickformat='%d-%m')
fig.update_xaxes(type='date')

fig.show()