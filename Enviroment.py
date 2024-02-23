import os

class Enviroment:
    def __init__(self):
        self.postgres_local_password = os.getenv("POSTGRES_LOCAL_PASSWORD")
        self.poke_go_pal_database_name = os.getenv("POKE_GO_PAL_DATABASE_NAME")

        if self.postgres_local_password is None:
            raise RuntimeError("POSTGRES_LOCAL_PASSWORD is not set")
        if self.poke_go_pal_database_name is None:
            raise RuntimeError("POKE_GO_PAL_DATABASE_NAME not set")