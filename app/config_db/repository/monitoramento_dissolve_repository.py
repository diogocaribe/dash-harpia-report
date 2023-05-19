from config_db.configs.connection import DBConnectionHandler
from config_db.entities.monitoramento_dissolve import MonitoramentoDissolve
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

import geopandas as gpd


class MonitoramentoDissolveRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(func.ST_AsGeoJSON(MonitoramentoDissolve)).all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception


    def gdf_select_all(self, epsg=4674):
        """
        Run a PostGIS query and return results as a GeoDataFrame
        :param engine: SQLAlchemy database connection engine
        :param query: Query to run
        :param params: Query parameter list
        :param geocolumn: Geometry column of query
        :param epsg: EPSG code of geometry output
        :return: GeoDataFrame
        """
        with DBConnectionHandler() as db:
            try:
                # data = db.session.query(MonitoramentoDissolve).all()
                data = gpd.GeoDataFrame.from_postgis(
                    sql="SELECT id, class_name, view_date, area_ha, geom FROM monitoramento_dissolve;",
                    con=db.get_engine(),
                    crs=epsg,
                    index_col=["view_date"],
                )
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception


    def select_all_geojson(self):
        """
            Consulta que retorna geojson que é lido pelo leaflet.
            SELECT row_to_json(fc)
            FROM (
                SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features
                FROM (SELECT 'Feature' As type, ST_AsGeoJSON(st_transform(lg.geom, 4326))::json As geometry, 
            (
                SELECT row_to_json(t) 
                FROM (SELECT id, view_date, class_name, area_ha) t
            )
            As properties
            FROM monitoramento_dissolve As lg) As f)  As fc;
        """
        with DBConnectionHandler() as db:
            try:
                sql = """
                    SELECT row_to_json(fc)
                    FROM (
                        SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features
                        FROM (SELECT 'Feature' As type, ST_AsGeoJSON(st_transform(lg.geom, 4326))::json As geometry, 
                    (
                        SELECT row_to_json(t) 
                        FROM (SELECT id, view_date, class_name, area_ha) t
                    )
                    As properties
                    FROM monitoramento_dissolve As lg) As f)  As fc;
                """
                con=db.get_engine()
                data = con.execute(sql)

                return data
            except Exception as exception:
                db.session.rollback()
                raise exception



