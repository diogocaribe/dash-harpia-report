from dotenv import dotenv_values, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
config = dotenv_values(".env")


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = f'postgresql+psycopg2://{config["DB_USER"]}:{config["DB_PASSWORD"]}@{config["DB_IP"]}:{config["DB_PORT"]}/{config["DB_NAME"]}'
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
