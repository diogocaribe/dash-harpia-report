import pandas as pd
import plotly.express as px

df_decremento_municipio = pd.read_csv('app/graficos_dev/data/decremento_municipio_202305291512.csv', index_col="view_date") 

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

df_decremento_municipio = df_decremento_municipio[["area_ha"]].groupby(df_decremento_municipio.index).sum()

t1 = pd.DataFrame()

for ano in df_decremento_municipio.index.year.unique()[
    df_decremento_municipio.index.year.unique() > 2017
]:  

    df = df_decremento_municipio[df_decremento_municipio.index.year == ano]
    df["year"] = df.index.year
    df["timedelta"] = (df.index - (df.index.year.astype("str") + "-01-01").astype("datetime64[ns]"))/1000000
    df["cumsum"]= df["area_ha"].cumsum()

    t1 = pd.concat([t1, df[["year", "timedelta", "cumsum"]]])

fig = px.line(t1, x="timedelta", y="cumsum", color='year')

fig.update_layout(title="Desflorestamento por Tempo",
    xaxis={"title": "Data"},
    yaxis={"title": "Área (ha)"},
    xaxis_tickformat = '%d-%m'
)

fig.update_xaxes(type='date')

fig.show()