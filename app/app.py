"""Dashboard Harpia"""

# coding: utf-8

import dash
import dash_bootstrap_components as dbc
from flask import Flask

# css para deixar o layout bonito
external_stylesheets = [dbc.themes.BOOTSTRAP]

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.title = 'HarpiaDashboard'
