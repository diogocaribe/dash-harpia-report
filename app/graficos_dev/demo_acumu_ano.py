import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

date_rng = pd.date_range('2015-06-01', '2021-06-01', freq='1d')
rating = np.random.randint(0,10,(2193,)) + np.random.rand(2193)
df = pd.DataFrame({'Date': pd.to_datetime(date_rng), 'Rate':rating})
df['year'] = df['Date'].dt.year

fig = go.Figure()

start = ['2015-06-01','2016-06-01','2017-06-01','2018-06-01','2020-06-01']
end =   ['2016-06-01','2017-06-01','2018-06-01', '2019-06-01','2021-06-01']
years = df['year'].unique()

for idx, (s,e) in enumerate(zip(start, end)):
    tmp = df[(df['Date'] >= start[idx]) & (df['Date'] <= end[idx])]
    fig.add_trace(go.Scatter(x=date_rng[:-365],
                             y=tmp.Rate,
                             name=str(years[idx]),
                             mode='lines',
                            ))

fig.update_layout(height=600, xaxis_tickformat='%d-%b')
fig.update_xaxes(type='date')

fig.show()