"""Package to treat data"""
import json

from config_db.repository.decremento_municipio_repository import \
    DecrementoMunicipioRepository
from config_db.repository.monitoramento_dissolve_repository import \
    MonitoramentoDissolveRepository

# Decremento (view_date, class_name)
monitoramentodissolverepo = MonitoramentoDissolveRepository()

# Solicitando os dados do monitoramento_dissolve como geopandas
gdf_monitramento_dissolve = monitoramentodissolverepo.gdf_select_all()
# Transformação para geojson para adicionar ao mapa --> Se for utilizar
geojson_monitoramento_dissolve = json.loads(gdf_monitramento_dissolve.to_json())

# Decremento Município
df_decremento_municipio = DecrementoMunicipioRepository().df_select_all()
df_decremento_municipio['nome'] = df_decremento_municipio['nome'].astype('string')

# Calculando os valores de área decrementada por dia
# df_monitoramento_por_dia = df_decremento_municipio.loc[:,['area_ha']] \
#     .groupby(by='view_date').sum()
