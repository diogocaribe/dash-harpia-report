"""Controllers"""
import dash_mantine_components as dmc
<<<<<<< HEAD
from ..dataset.data import max_date, min_date, year_start
=======
from dataset.data import max_date, min_date, year_start
>>>>>>> d9a39285dfdf5daccb23148e6f2f44ab4d514786

date_range_picker = dmc.DateRangePicker(
    id="date-picker-range",
    minDate=min_date,
    maxDate=max_date,
    value=[year_start, max_date],
    inputFormat="DD/MM/YYYY",
)
