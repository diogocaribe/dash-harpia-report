from datetime import date, datetime, timedelta

import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_mantine_components as dmc
from dash import Dash, dcc, html


external_stylesheets = [dbc.themes.BOOTSTRAP]


app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = dbc.Container(
    [
        # with é utilizado para definir o tamanho da row horizontalmente
        # Por default ("auto") ela ocupará toda a linha
        dbc.Row(
            [
                dbc.Col(
                    [html.P("Monitoramento Vegetação"), html.P("Harpia")],
                    width=12,
                    className="bg-primary d-flex justify-content-between align-items-center",
                    style={"height": "6vh"},
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [dl.Map(dl.TileLayer(), style={"height": "90vh"})],
                    width=7,
                    class_name="p-0",
                ),
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [html.P(texto_gigante)],
                                    title="Acumulado Desmatamento 2023",
                                ),
                                dbc.AccordionItem(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dmc.DateRangePicker(
                                                            id="date-range-picker",
                                                            label="Date Range",
                                                            description="Selecione o intervalo de interesse:",
                                                            minDate=date(2020, 8, 5),
                                                            inputFormat="DD/MM/YYYY",
                                                            value=[
                                                                datetime.now().date(),
                                                                datetime.now().date()
                                                                + timedelta(days=5),
                                                            ],
                                                            style={"width": 205},
                                                        ),
                                                    ]
                                                ),
                                                dcc.Dropdown(
                                                    options=["Dia", "Mês", "Ano"],
                                                    value="Dia",
                                                    style={"width": 205},
                                                ),
                                            ],
                                            className="d-flex justify-content-between align-items-end",
                                        ),
                                        html.Hr(),
                                        html.P(
                                            "This is the content of the second section"
                                        ),
                                    ],
                                    title="Análises Temporal",
                                ),
                                dbc.AccordionItem(
                                    [
                                        html.P(
                                            "This is the content of the second section"
                                        ),
                                    ],
                                    title="Análise Espaço Temporal",
                                ),
                            ]
                        ),
                    ],
                    width=5,
                    style={"overflow-y": "scroll", "height": "90vh"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.Footer("Teste")],
                    width=12,
                    className="bg-primary",
                    style={"height": "4vh"},
                )
            ]
        ),
    ],
    class_name="overflow-hidden",
    fluid=True,  # retira as margens e padding do container (ajustando na lateral da tela), em qualquer dispositivo
)


if __name__ == "__main__":
    app.run_server(debug=True)
