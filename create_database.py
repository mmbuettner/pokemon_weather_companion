from Enviroment import Enviroment

import psycopg2

env = Enviroment()

conn = psycopg2.connect(
    database = "postgres",
    user = "postgres",
    password = env.postgres_local_password,
    host = "localhost",
    port = "5432"
)

conn.autocommit = True

cursor = conn.cursor()

sql = f""" CREATE database {env.poke_go_pal_database_name} """

cursor.execute(sql)
print("Database has been created successfully.")

conn.close()