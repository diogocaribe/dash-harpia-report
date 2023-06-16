"""Controllers"""
import dash_mantine_components as dmc
from ..dataset.data import max_date, min_date, year_start

date_range_picker = dmc.DateRangePicker(
    id="date-picker-range",
    minDate=min_date,
    maxDate=max_date,
    value=[year_start, max_date],
    inputFormat="DD/MM/YYYY",
)
