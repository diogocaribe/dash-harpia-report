from config_db.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime, DECIMAL
from geoalchemy2 import Geometry


class MonitoramentoDissolve(Base):
    __tablename__ = "monitoramento_dissolve"

    id = Column(Integer, primary_key=True)
    class_name = Column(String)
    view_date = Column(DateTime)
    area_ha = Column(DECIMAL(10, 2))
    geom = Column(Geometry('POLYGON'))

    def __repr__(self):
        return f"Monitoramento [titulo={self.class_name}, view_date={self.view_date}, geom={self.geom}]"
