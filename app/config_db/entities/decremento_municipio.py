from config_db.configs.base import Base
from sqlalchemy import DECIMAL, Column, DateTime, Integer, String


class DecrementoMunicipio(Base):
    __tablename__ = "vw_decremento_municipio"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    view_date = Column(DateTime)
    area_ha = Column(DECIMAL(10, 2))

    def __repr__(self):
        return f"Decremento Municipal [titulo={self.class_name}, view_date={self.view_date}, area_ha={self.area_ha}]"

