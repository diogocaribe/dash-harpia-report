from datetime import date, datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import df_decremento_municipio

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

# df_decremento_municipio.index.year.unique() > 2016

df = df_decremento_municipio[df_decremento_municipio.index.year> 2016]

t = df_decremento_municipio.sort_index()["area_ha"].groupby([df_decremento_municipio.index]).sum()
t1 = t.groupby([t.index.year]).cumsum()


data_day = go.Scatter(
    x=t.index,
    y=t1,
    mode='lines',
)
layout = go.Layout(
    title="Desflorestamento por Tempo",
    xaxis={"title": "Data"},
    yaxis={"title": "Área (ha)"},
    xaxis_tickformat='%d-%m'
)

fig = go.Figure(data=data_day, layout=layout)


# fig.update_layout(height=600, xaxis_tickformat='%d-%m')
fig.update_xaxes(type='date')

fig.show()