from datetime import date

from dash import dcc
import dash_mantine_components as dmc
from dataset.data import df_decremento_municipio

# Datas iniciais e finais do dataframe
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)

date_range_picker = dmc.DateRangePicker(
    id="date-picker-range",
    minDate=min_date,
    maxDate=max_date,
    value=[year_start, max_date],
    inputFormat="DD/MM/YYYY",
)
