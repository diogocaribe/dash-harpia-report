"""Módulo de dados"""
from datetime import date

from config_db.repository.decremento_municipio_repository import \
    DecrementoMunicipioRepository
from config_db.repository.monitoramento_dissolve_repository import \
    MonitoramentoDissolveRepository

# Decremento (view_date, class_name)
monitoramentodissolverepo = MonitoramentoDissolveRepository()

# Solicitando os dados do monitoramento_dissolve como geopandas
gdf_monitramento_dissolve = monitoramentodissolverepo.gdf_select_all()

# Decremento Município
df_decremento_municipio = DecrementoMunicipioRepository().df_select_all()
df_decremento_municipio['nome'] = df_decremento_municipio['nome'].astype('string')

# Datas iniciais e finais do dataframe
max_date = df_decremento_municipio.index.max()
min_date = df_decremento_municipio.index.min()

# Datas iniciais e finais do ano corrente
current_year = date.today().year
year_start = date(current_year, 1, 1)
year_end = date(current_year, 12, 31)

# Calculando os valores de área decrementada por dia
# df_monitoramento_por_dia = df_decremento_municipio.loc[:,['area_ha']] \
#     .groupby(by='view_date').sum()
