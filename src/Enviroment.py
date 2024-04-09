import os
from google.cloud.sql.connector import Connector
import sqlalchemy

connector = Connector()

class Enviroment:
    def __init__(self):
        self.postgres_local_password = os.getenv("POSTGRES_LOCAL_PASSWORD")
        self.poke_go_pal_database_name = os.getenv("POKE_GO_PAL_DATABASE_NAME")
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        # self.engine = sqlalchemy.create_engine('')
        self.metadata_obj = sqlalchemy.MetaData()

        if self.postgres_local_password is None:
            raise RuntimeError("POSTGRES_LOCAL_PASSWORD is not set")
        if self.poke_go_pal_database_name is None:
            raise RuntimeError("POKE_GO_PAL_DATABASE_NAME not set")
        
        self.engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=self.getconn
        )
        
    def getconn(self):
        conn = connector.connect(
            "pokemon-weather-companion:us-central1:pwc-db",
            "pg8000",
            user="postgres",
            password=self.postgres_local_password,
            db="postgres",
        )
        conn.autocommit = True
        return conn
